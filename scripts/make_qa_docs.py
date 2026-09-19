#!/usr/bin/env python3
"""
Generate qa/compliance_matrix.md and qa/open_items.md from the analysis JSON
in work/analysis/. Re-run after editing the JSON to regenerate both.

    python3 scripts/make_qa_docs.py
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ANALYSIS = ROOT / "work" / "analysis"
QA = ROOT / "qa"


def load(name: str) -> dict | None:
    p = ANALYSIS / f"{name}.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def cell(s: str) -> str:
    return (s or "").replace("|", "\\|").replace("\n", " ").strip()


def compliance_matrix() -> None:
    d = load("compliance")
    if not d:
        print("skip compliance_matrix: work/analysis/compliance.json not found")
        return

    rows = d["rows"]
    by_type: dict[str, list[dict]] = {}
    for r in rows:
        by_type.setdefault(r["type"], []).append(r)

    order = [
        "mandatory-submission", "format", "eligibility",
        "technical-content", "cost-content", "evaluation",
    ]
    titles = {
        "mandatory-submission": "Mandatory submission items",
        "format": "Format and submission rules",
        "eligibility": "Offeror eligibility (RFP section 3)",
        "technical-content": "Technical proposal content",
        "cost-content": "Cost proposal content",
        "evaluation": "Evaluation criteria (RFP section 6)",
    }

    out = [
        "# Compliance matrix",
        "",
        "EY response to Conservation International RFP 0032026, brand-delivery",
        "support models for emerging protected areas in Africa.",
        "",
        f"Every requirement in the RFP, mapped to where it is met. {len(rows)} rows.",
        "Regenerate with `python3 scripts/make_qa_docs.py`.",
        "",
        "Risk column: the risk of failing this requirement as the response currently stands.",
        "",
    ]

    high = [r for r in rows if r["risk"].lower().startswith("high")]
    if high:
        out += [
            f"## Open risk: {len(high)} requirement(s) at high risk",
            "",
            "| ID | Requirement | Why it is at risk |",
            "|---|---|---|",
        ]
        for r in high:
            out.append(f"| {r['id']} | {cell(r['requirement'])[:150]} | {cell(r['risk'])} |")
        out.append("")

    seen = set()
    for t in order + sorted(set(by_type) - set(order)):
        group = by_type.get(t)
        if not group or t in seen:
            continue
        seen.add(t)
        out += [
            f"## {titles.get(t, t.replace('-', ' ').capitalize())}",
            "",
            "| ID | RFP source | Requirement | Where it is met | Evidence needed | Risk |",
            "|---|---|---|---|---|---|",
        ]
        for r in group:
            out.append(
                f"| {r['id']} | {cell(r['source'])} | {cell(r['requirement'])} | "
                f"{cell(r['whereMet'])} | {cell(r['evidenceNeeded'])} | {cell(r['risk'])} |"
            )
        out.append("")

    if d.get("formatRules"):
        out += ["## Hard format rules", ""]
        out += [f"{i}. {cell(x)}" for i, x in enumerate(d["formatRules"], 1)]
        out.append("")

    if d.get("ambiguities"):
        out += [
            "## Clarification questions for Conservation International",
            "",
            "Genuine ambiguities in the RFP text. These should be put to CI before",
            "submission, in one consolidated request.",
            "",
        ]
        out += [f"{i}. {cell(x)}" for i, x in enumerate(d["ambiguities"], 1)]
        out.append("")

    (QA / "compliance_matrix.md").write_text("\n".join(out), encoding="utf-8")
    print(f"wrote qa/compliance_matrix.md ({len(rows)} rows, {len(high)} high risk)")


def checkpoints() -> None:
    d = load("governance")
    if not d:
        print("skip checkpoints: work/analysis/governance.json not found")
        return

    out = [
        "# Review checkpoints and QA checks",
        "",
        "EY response to Conservation International RFP 0032026.",
        "",
        "## Status of this document",
        "",
        d["reconstructionNote"],
        "",
        "## Partner review checkpoints",
        "",
        "Michael Harris, Partner, EY Business Consulting, South Africa, reviews at",
        "each checkpoint below. Each carries a decision, not a read-through.",
        "",
    ]
    for c in d["checkpoints"]:
        out += [
            f"### {c['id']}: {c['name']}",
            "",
            f"**Reviewed** {c['whatIsReviewed']}",
            "",
            f"**Decision** {c['decision']}",
            "",
            f"**Blocks** {c['blocksWhat']}",
            "",
        ]

    auto = [c for c in d["qaChecks"] if c["automatable"].strip().lower().startswith("y")]
    manual = [c for c in d["qaChecks"] if not c["automatable"].strip().lower().startswith("y")]

    out += [
        "## QA checks",
        "",
        f"{len(d['qaChecks'])} checks. {len(auto)} are mechanically verifiable and are",
        "implemented in `scripts/qa.py`; run it with `python3 scripts/qa.py`. The",
        f"remaining {len(manual)} need a human and are listed separately below.",
        "",
        "### Automated",
        "",
        "| ID | Check | How it is verified |",
        "|---|---|---|",
    ]
    for c in auto:
        out.append(f"| {c['id']} | {cell(c['check'])} | {cell(c['how'])} |")
    out += [
        "",
        "### Manual",
        "",
        "| ID | Check | How it is verified |",
        "|---|---|---|",
    ]
    for c in manual:
        out.append(f"| {c['id']} | {cell(c['check'])} | {cell(c['how'])} |")
    out.append("")

    (QA / "checkpoints_and_qa.md").write_text("\n".join(out), encoding="utf-8")
    print(f"wrote qa/checkpoints_and_qa.md ({len(d['checkpoints'])} checkpoints, "
          f"{len(auto)} automated + {len(manual)} manual checks)")


def status() -> None:
    """A one-page live status, generated from the QA gate and the open items."""
    gaps = load("gaps")
    comp = load("compliance")
    if not (gaps and comp):
        print("skip status: analysis files missing")
        return

    qa_run = subprocess.run(
        [sys.executable, str(Path(__file__).with_name("qa.py"))],
        capture_output=True, text=True,
    )
    summary = ""
    for line in qa_run.stdout.splitlines():
        if "passed" in line and "defect" in line:
            summary = line.strip()

    build_run = subprocess.run(
        [sys.executable, str(Path(__file__).with_name("build.py"))],
        capture_output=True, text=True,
    )

    items = gaps["items"]
    by_sev: dict[str, list[dict]] = {}
    by_owner: dict[str, int] = {}
    for i in items:
        by_sev.setdefault(i["severity"].split()[0].lower(), []).append(i)
        by_owner[i["owner"]] = by_owner.get(i["owner"], 0) + 1

    blockers = by_sev.get("blocker", [])

    out = [
        "# Status",
        "",
        "EY response to Conservation International RFP 0032026. Generated by",
        "`python3 scripts/make_qa_docs.py`; do not edit by hand.",
        "",
        "## Build",
        "",
        "```",
        build_run.stdout.strip() or "build did not run",
        "```",
        "",
        "## QA gate",
        "",
        "```",
        summary or "qa did not run",
        "```",
        "",
        "A check reported as blocked is waiting on an input, not on a fix. The",
        "response is structurally complete; it is not submittable until the items",
        "below are supplied.",
        "",
        "## Open items",
        "",
        f"{len(items)} in total, across {len(comp['rows'])} compliance requirements.",
        "",
        "| Severity | Count |",
        "|---|---|",
    ]
    for sev in ("blocker", "high", "medium", "low"):
        if sev in by_sev:
            out.append(f"| {sev.capitalize()} | {len(by_sev[sev])} |")
    out += ["", "| Owner | Count |", "|---|---|"]
    for owner, n in sorted(by_owner.items(), key=lambda kv: -kv[1]):
        out.append(f"| {owner} | {n} |")

    out += [
        "",
        "## Blockers",
        "",
        "Nothing else in the bid can be finished until these land.",
        "",
        "| ID | Item | Owner |",
        "|---|---|---|",
    ]
    for i in blockers:
        out.append(f"| {i['id']} | {cell(i['item'])[:170]} | {cell(i['owner'])} |")

    out += [
        "",
        "## What to do next",
        "",
        "1. Put the consolidated clarification request to CI. The RFP copy held "
        "begins at Section 2 and its final section ends mid-sentence, so the "
        "submission deadline, address and level-of-effort text are all unknown. "
        "The questions are at the end of `qa/compliance_matrix.md`.",
        "2. Start client reference consent and work-sample clearance. These have "
        "the longest lead times and they carry the most marks.",
        "3. Name the team and collect CVs. Criterion 3.1 cannot be scored without "
        "them and it is worth 15 marks.",
        "4. Settle the consortium question on destination branding and "
        "protected-area experience, which are the two of the eight required "
        "skills a mainstream consulting credential is least likely to satisfy.",
        "5. Get the rate discount approved and the tax treatment confirmed.",
        "6. Work the checkpoints in `qa/checkpoints_and_qa.md`, correcting them "
        "first, since they are a reconstruction of a brief section that was never "
        "supplied.",
        "",
    ]
    (QA / "STATUS.md").write_text("\n".join(out), encoding="utf-8")
    print(f"wrote qa/STATUS.md ({len(items)} open items, {len(blockers)} blockers)")


SEVERITY_ORDER = {"blocker": 0, "high": 1, "medium": 2, "low": 3}


def open_items() -> None:
    d = load("gaps")
    if not d:
        print("skip open_items: work/analysis/gaps.json not found")
        return

    items = sorted(
        d["items"],
        key=lambda i: (SEVERITY_ORDER.get(i["severity"].lower().split()[0], 9), i["id"]),
    )

    counts: dict[str, int] = {}
    for i in items:
        k = i["severity"].lower().split()[0]
        counts[k] = counts.get(k, 0) + 1
    tally = ", ".join(f"{v} {k}" for k, v in sorted(counts.items(), key=lambda kv: SEVERITY_ORDER.get(kv[0], 9)))

    out = [
        "# Open items",
        "",
        "EY response to Conservation International RFP 0032026.",
        "",
        "Every input the response needs and does not have. Nothing in the proposal",
        "is invented to fill one of these; each appears in the documents as a",
        "`[[TO CONFIRM: ...]]` placeholder, rendered as a yellow highlight in the",
        "PDF, and `scripts/qa.py` fails the build while any remain.",
        "",
        f"**{len(items)} open items:** {tally}.",
        "",
        "Regenerate with `python3 scripts/make_qa_docs.py`.",
        "",
        "| ID | Item | Why it matters | Owner | Severity | Needed by |",
        "|---|---|---|---|---|---|",
    ]
    for i in items:
        out.append(
            f"| {i['id']} | {cell(i['item'])} | {cell(i['why'])} | {cell(i['owner'])} | "
            f"{cell(i['severity'])} | {cell(i['dueBy'])} |"
        )
    out.append("")

    out += ["## Placeholder strings in the documents", "",
            "| ID | Placeholder as it appears |", "|---|---|"]
    for i in items:
        ph = i.get("placeholderString", "-")
        if ph and ph.strip() != "-":
            out.append(f"| {i['id']} | `{cell(ph)}` |")
    out.append("")

    if d.get("clarificationQuestionsToCI"):
        out += [
            "## Questions for Conservation International",
            "",
            "To be put to CI in one consolidated request before submission.",
            "",
        ]
        out += [f"{n}. {cell(q)}" for n, q in enumerate(d["clarificationQuestionsToCI"], 1)]
        out.append("")

    (QA / "open_items.md").write_text("\n".join(out), encoding="utf-8")
    print(f"wrote qa/open_items.md ({len(items)} items)")


if __name__ == "__main__":
    QA.mkdir(exist_ok=True)
    # Collecting from the workflow journal rewrites compliance.json from the
    # agent's raw output, which drops the location remap. Re-apply it first;
    # the remap is idempotent so running it here is always safe.
    subprocess.run(
        [sys.executable, str(Path(__file__).with_name("remap_locations.py"))],
        check=True, capture_output=True,
    )
    compliance_matrix()
    open_items()
    checkpoints()
    status()
