#!/usr/bin/env python3
"""
Write Annex E of the technical proposal: the compliance matrix, condensed to
the three columns a CI evaluator needs.

    python3 scripts/make_annex_e.py

The working copy at qa/compliance_matrix.md keeps the evidence and risk
columns, which are for the EY bid team rather than for CI.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "work" / "analysis" / "compliance.json"
TECH = ROOT / "proposal" / "technical" / "technical_proposal.md"
COST = ROOT / "proposal" / "cost" / "cost_proposal.md"

# The technical proposal is evaluated separately and before the cost proposal,
# so its compliance annex must carry no cost content. The cost requirements go
# to the cost proposal's own annex instead, and the two together cover the RFP.
TECH_GROUPS = [
    ("mandatory-submission", "Submission completeness"),
    ("format", "Format and submission rules"),
    ("eligibility", "Offeror eligibility, RFP section 3"),
    ("technical-content", "Technical proposal content"),
    ("evaluation", "Evaluation criteria, RFP section 6"),
]
COST_GROUPS = [("cost-content", "Cost proposal content")]

# Any figure would be pricing in the technical file; the requirement reads
# just as well without it.
MONEY = re.compile(r"US\$\s?[\d,]+(?:\.\d+)?")


def cell(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "")).replace("|", "/").strip()


def table(rows: list[dict], scrub_money: bool) -> list[str]:
    out = ["| ID | Requirement | Where it is met |", "|---|---|---|"]
    for r in rows:
        req = cell(r["requirement"])
        where = cell(r["whereMet"])
        if scrub_money:
            req = MONEY.sub("the published ceiling", req)
            where = MONEY.sub("the published ceiling", where)
        out.append(f"| {r['id']} | {req} | {where} |")
    return out


def render(rows: list[dict], groups, heading: str, blurb: str,
           scrub_money: bool) -> tuple[str, int]:
    by_type: dict[str, list[dict]] = {}
    for r in rows:
        by_type.setdefault(r["type"], []).append(r)
    out = [heading, "", blurb, ""]
    n = 0
    for key, title in groups:
        group = by_type.get(key)
        if not group:
            continue
        n += len(group)
        out += [f"### {title}", ""] + table(group, scrub_money) + [""]
    return "\n".join(out), n


def splice(path: Path, start_marker: str, end_marker: str, body: str) -> None:
    """Replace the block from start_marker up to the next end_marker after it.

    The end marker must be searched for FROM the start marker. Searching the
    whole document finds an earlier occurrence and splices the annex into the
    middle of the page, which is exactly what happened before this was fixed.
    """
    doc = path.read_text(encoding="utf-8")
    start = doc.index(start_marker)
    end = doc.find(end_marker, start + len(start_marker))
    if end == -1:
        end = len(doc)
    path.write_text(doc[:start] + body + "\n" + doc[end:], encoding="utf-8")


def main() -> None:
    rows = json.loads(SRC.read_text(encoding="utf-8"))["rows"]

    tech_body, tech_n = render(
        rows, TECH_GROUPS, "## Annex E: Compliance matrix",
        "Every requirement in RFP 0032026 that bears on this technical proposal, "
        "mapped to the place where it is met. The cost requirements are mapped in "
        "the same way in Annex C of the separate Cost Proposal.",
        scrub_money=True,
    )
    splice(TECH, "## Annex E: Compliance matrix", "## Annex F:", tech_body)

    cost_body, cost_n = render(
        rows, COST_GROUPS, "## Annex C: Compliance matrix, cost requirements",
        "Every cost requirement in RFP 0032026, mapped to the place in this cost "
        "proposal where it is met. The technical requirements are mapped in Annex E "
        "of the separate Technical Proposal.",
        scrub_money=False,
    )
    cost_doc = COST.read_text(encoding="utf-8")
    if "## Annex C: Compliance matrix" in cost_doc:
        splice(COST, "## Annex C: Compliance matrix", "\n</div>", cost_body)
    else:
        COST.write_text(cost_doc.replace("\n</div>\n", "\n" + cost_body + "\n</div>\n"),
                        encoding="utf-8")

    print(f"Annex E: {tech_n} technical requirements; "
          f"Cost Annex C: {cost_n} cost requirements")


if __name__ == "__main__":
    main()
