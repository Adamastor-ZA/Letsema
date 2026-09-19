#!/usr/bin/env python3
"""
QA gate for the EY response to Conservation International RFP 0032026.

Runs every mechanical check the submission must pass and exits non-zero if any
hard check fails.

    python3 scripts/qa.py

Checks are grouped: SUBMISSION (RFP compliance), ARITHMETIC (the cost model),
HOUSE STYLE (Michael's writing rules) and BUILD (artefact integrity).
"""

from __future__ import annotations

import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"
PROPOSAL = ROOT / "proposal"
QA = ROOT / "qa"

TECH_PDF = BUILD / "EY_Technical_Proposal_CI_RFP_0032026.pdf"
COST_PDF = BUILD / "EY_Cost_Proposal_CI_RFP_0032026.pdf"
TECH_MD = PROPOSAL / "technical" / "technical_proposal.md"
COST_MD = PROPOSAL / "cost" / "cost_proposal.md"

TECH_DECK = BUILD / "EY_Technical_Proposal_Deck_CI_RFP_0032026.pptx"
COST_DECK = BUILD / "EY_Cost_Proposal_Deck_CI_RFP_0032026.pptx"
DECK_TEMPLATE = ROOT / "assets" / "pptx" / "ey-master-template.pptx"

# Strings the EY template ships that must not survive into a finished deck.
TEMPLATE_LEFTOVERS = [
    "REMOVE THIS SLIDE", "template layout", "Insert footer text here",
    "Spectrum 1", "Spectrum 2", "Spectrum 3", "Key statement",
    "Section header", "Yellow Frame", "Frame color", "Quote goes here",
    "Copying legacy content", "[member firm name]", "XXXGbl", "ED MMYY",
]

BUDGET_CEILING = 40000
BODY_PAGE_CAP = 5
INCEPTION_CAP_PCT = 10


@dataclass
class Result:
    ident: str
    group: str
    check: str
    passed: bool
    hard: bool = True
    detail: str = ""
    # A blocked check is not a defect. It fails only because an input the
    # response needs has not been supplied, and no amount of editing will
    # clear it. Reported separately so the two never get confused.
    blocked: bool = False


results: list[Result] = []


def record(ident, group, check, passed, hard=True, detail="", blocked=False):
    results.append(Result(ident, group, check, passed, hard, detail, blocked))


def pdf_text(path: Path) -> str:
    return "\n".join((p.extract_text() or "") for p in PdfReader(str(path)).pages)


def pdf_pages(path: Path) -> int:
    return len(PdfReader(str(path)).pages)


# ------------------------------------------------------------------ prose ---

# Words the house style bans outright. Matched on word boundaries.
TELL_WORDS = [
    "delve", "synergy", "synergies", "paradigm shift", "game-changer",
    "game changer", "tapestry", "ever-evolving", "dive into",
    "in today's fast-paced world", "unlock the", "seamlessly",
    "best-in-class", "world-class", "cutting-edge", "robust and scalable",
]

# US spellings that must not appear. The value is the UK form.
US_SPELLINGS = {
    r"\borganiz(e|es|ed|ing|ation|ations|ational)\b": "organis-",
    r"\bprioritiz(e|es|ed|ing|ation)\b": "prioritis-",
    r"\brecogniz(e|es|ed|ing)\b": "recognis-",
    r"\boptimiz(e|es|ed|ing|ation)\b": "optimis-",
    r"\banalyz(e|es|ed|ing)\b": "analys-",
    r"\bcolor(s|ed|ing)?\b": "colour",
    r"\bbehavior(s|al)?\b": "behaviour",
    r"\bfavor(s|ed|able)?\b": "favour",
    r"\blabor\b": "labour",
    r"\bdefense\b": "defence",
    r"\bmodeling\b": "modelling",
    r"\btraveler(s)?\b": "traveller",
    r"\bcenter(s|ed)?\b": "centre",
    r"\bfulfill(s|ed|ing|ment)?\b": "fulfil",
    r"\bcatalog(s|ed)?\b": "catalogue",
}

# Comma sequences reviewed and cleared. Each is either a verbatim quotation
# from the RFP, where the client's own punctuation stands, or a parenthetical
# that needs the comma before "and" to stay readable.
OXFORD_CLEARED = [
    "unit prices, quantities, and total price",   # quoted verbatim from RFP section 4
    "eight case studies, two of them clustered, and five light-touch checks",
]

# Proper nouns and quoted source material that legitimately carry US spellings.
SPELLING_EXEMPTIONS = [
    # EY's global boilerplate is fixed legal text and carries US spellings.
    # It is reproduced verbatim on the closing slide and must not be edited.
    "EY refers to the global organization",
    "more information about our organization",
    "Harpers Ferry Center", "Center for", "Mekong Tourism Coordinating Office",
    "Wildlife Friendly Enterprise Network", "World Travel Center",
    "Bateleur", "Sossusvlei",
]


def strip_exemptions(text: str) -> str:
    """Remove proper nouns that legitimately carry US spellings.

    PDF extraction wraps table cells, so a name can arrive split across lines.
    Whitespace is normalised first, otherwise the exemption silently misses.
    """
    text = re.sub(r"\s+", " ", text)
    for phrase in SPELLING_EXEMPTIONS:
        text = text.replace(phrase, "")
    return text


def check_prose(label: str, text: str) -> None:
    scrubbed = strip_exemptions(text)

    # Em dash and en dash are banned in prose. Hyphens are fine.
    bad_dashes = re.findall(r"[—–]", text)
    record(
        f"HS-01/{label}", "HOUSE STYLE",
        f"{label}: no em or en dashes",
        not bad_dashes, True,
        f"{len(bad_dashes)} found" if bad_dashes else "",
    )

    # Oxford comma detection. A genuine Oxford comma joins three short parallel
    # items. The common false positive is "X, <subordinate clause>, and <new
    # clause>", so the middle segment must be short and must not itself contain
    # a conjunction or a clause marker. Regex cannot settle this reliably, so
    # the check reports candidates for a human to read rather than failing hard.
    candidates = []
    for m in re.finditer(
        r"\b([\w\)]+), ([\w][\w \-]{2,28}?), (and|or) (\w+(?: \w+){0,3})", text
    ):
        middle = m.group(2)
        if re.search(r"\b(and|or|as|which|that|because|where|when|since)\b", middle):
            continue
        window = re.sub(r"\s+", " ", text[max(0, m.start() - 60):m.end() + 60])
        if any(c.lower() in window.lower() for c in OXFORD_CLEARED):
            continue
        candidates.append(m.group(0))
    record(
        f"HS-02/{label}", "HOUSE STYLE",
        f"{label}: Oxford comma candidates for review",
        not candidates, False,
        "; ".join(candidates[:6]) if candidates else "",
    )

    hits = [w for w in TELL_WORDS if re.search(rf"\b{re.escape(w)}\b", text, re.I)]
    record(
        f"HS-03/{label}", "HOUSE STYLE",
        f"{label}: no banned tell-words",
        not hits, True, ", ".join(hits),
    )

    us = []
    for pattern, uk in US_SPELLINGS.items():
        found = re.findall(pattern, scrubbed, re.I)
        if found:
            us.append(f"{uk} ({len(found)})")
    record(
        f"HS-04/{label}", "HOUSE STYLE",
        f"{label}: UK English spelling",
        not us, True, ", ".join(us),
    )

    record(
        f"HS-05/{label}", "HOUSE STYLE",
        f"{label}: no emoji",
        not re.search(r"[\U0001F300-\U0001FAFF☀-➿]", text), True,
    )


# ------------------------------------------------------------- submission ---

def check_submission() -> None:
    record("SUB-01", "SUBMISSION", "Technical proposal PDF exists", TECH_PDF.exists())
    record("SUB-02", "SUBMISSION", "Cost proposal PDF exists", COST_PDF.exists())
    record(
        "SUB-03", "SUBMISSION",
        "Technical and cost proposals are separate files",
        TECH_PDF.exists() and COST_PDF.exists() and TECH_PDF != COST_PDF,
    )

    if not (TECH_PDF.exists() and COST_PDF.exists()):
        return

    tech = pdf_text(TECH_PDF)
    cost = pdf_text(COST_PDF)

    for label, text in (("technical", tech), ("cost", cost)):
        left = re.findall(r"\[\[TO CONFIRM", text)
        record(
            f"SUB-04/{label}", "SUBMISSION",
            f"{label}: no unresolved placeholders",
            not left, True,
            f"{len(left)} awaiting input; see qa/open_items.md" if left else "",
            blocked=bool(left),
        )

    # The five-page cap is measured on the body, before the first annex.
    m = re.search(r"Annex A", tech)
    record(
        "SUB-05", "SUBMISSION",
        "Technical proposal contains annexes",
        bool(m), False,
    )

    body_pages = None
    reader = PdfReader(str(TECH_PDF))
    for i, page in enumerate(reader.pages, 1):
        if re.search(r"\bAnnex A\b", page.extract_text() or ""):
            body_pages = i - 1
            break
    if body_pages is not None:
        record(
            "SUB-06", "SUBMISSION",
            f"Technical body within {BODY_PAGE_CAP}-page cap",
            body_pages <= BODY_PAGE_CAP, True,
            f"body is {body_pages} pages",
        )

    record(
        "SUB-07", "SUBMISSION",
        "Cost proposal states all figures in USD",
        "US$" in cost or "USD" in cost, True,
    )
    record(
        "SUB-08", "SUBMISSION",
        "Cost proposal contains a budget narrative",
        re.search(r"budget narrative", cost, re.I) is not None, True,
    )
    record(
        "SUB-09", "SUBMISSION",
        "Cost proposal contains a payment schedule",
        re.search(r"payment schedule", cost, re.I) is not None, True,
    )
    record(
        "SUB-10", "SUBMISSION",
        "Cost proposal states costs are all-inclusive of profit, fees and taxes",
        re.search(r"all-inclusive", cost, re.I) is not None, True,
    )
    record(
        "SUB-11", "SUBMISSION",
        "Technical proposal names all three required Parts",
        all(re.search(rf"Part {n}", tech) for n in (1, 2, 3)), True,
    )
    record(
        "SUB-12", "SUBMISSION",
        "Technical proposal covers all three RFP activities",
        all(re.search(rf"Activity {n}", tech, re.I) for n in ("One", "Two", "Three")),
        True,
    )
    record(
        "SUB-13", "SUBMISSION",
        "Offeror Representation of Transparency, Integrity, Social Responsibility addressed",
        re.search(r"Transparency, Integrity", tech, re.I) is not None, True,
    )
    record(
        "SUB-14", "SUBMISSION",
        "Three client references present",
        len(re.findall(r"Reference [123]", tech)) >= 3, True,
    )

    # The technical proposal is evaluated first and separately. Any EY price,
    # rate or fee leaking into it is a standard disqualification trigger.
    # Benchmark figures quoted as evidence are not pricing and are allowed.
    leaks = []
    if re.search(r"US\$\s?40[,.]?000|\b40,000\b", tech):
        leaks.append("assignment budget ceiling")
    for pattern, name in (
        (r"\bper day\b", "day-rate language"),
        (r"\bday rate\b", "day-rate language"),
        (r"\brate card\b", "rate card reference"),
        (r"\bprofessional fees\b", "fee line"),
        (r"\bpayment schedule\b", "payment schedule"),
        (r"\bblended rate\b", "blended rate"),
    ):
        if re.search(pattern, tech, re.I):
            leaks.append(name)
    record(
        "SUB-15", "SUBMISSION",
        "No EY price, rate or fee appears in the technical proposal",
        not leaks, True, ", ".join(sorted(set(leaks))),
    )

    record(
        "SUB-16", "SUBMISSION",
        "Cost proposal is not bundled into the technical proposal",
        "Cost proposal" not in tech or "Total price" not in tech, True,
    )

    check_prose("technical", tech)
    check_prose("cost", cost)


# ------------------------------------------------------------- arithmetic ---

def parse_money(cell: str) -> float | None:
    cell = cell.replace(",", "").replace("US$", "").replace("$", "").strip()
    m = re.fullmatch(r"-?\d+(?:\.\d+)?", cell)
    return float(m.group()) if m else None


def md_tables(md: str) -> list[list[list[str]]]:
    tables, current = [], []
    for line in md.splitlines():
        if line.strip().startswith("|") and line.strip().endswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
                continue
            current.append(cells)
        elif current:
            tables.append(current)
            current = []
    if current:
        tables.append(current)
    return tables


def check_arithmetic() -> None:
    if not COST_MD.exists():
        record("ARI-00", "ARITHMETIC", "Cost proposal source present", False)
        return

    md = COST_MD.read_text(encoding="utf-8")

    # Every table that carries a TOTAL row must add up.
    bad = []
    checked = 0
    for table in md_tables(md):
        total_row = next(
            (r for r in table if r and r[0].strip().lower().lstrip("*").startswith("total")),
            None,
        )
        if not total_row:
            continue
        for col in range(1, len(total_row)):
            stated = parse_money(total_row[col].replace("**", ""))
            if stated is None:
                continue
            parts = []
            for row in table:
                if row is total_row or len(row) <= col:
                    continue
                if row[0].strip().lower().lstrip("*").startswith(("total", "subtotal")):
                    continue
                v = parse_money(row[col].replace("**", ""))
                if v is not None:
                    parts.append(v)
            if len(parts) < 2:
                continue
            checked += 1
            if abs(sum(parts) - stated) > 0.51:
                bad.append(f"col {col}: parts sum {sum(parts):,.0f} vs stated {stated:,.0f}")
    record(
        "ARI-01", "ARITHMETIC",
        f"All totalled columns sum correctly ({checked} checked)",
        not bad, True, "; ".join(bad[:6]),
    )

    # The ceiling.
    figures = [parse_money(x) for x in re.findall(r"US\$\s?([\d,]+(?:\.\d+)?)", md)]
    over = [f for f in figures if f and f > BUDGET_CEILING]
    record(
        "ARI-02", "ARITHMETIC",
        f"No figure exceeds the US${BUDGET_CEILING:,} ceiling",
        not over, True, f"{over[:4]}" if over else "",
    )

    # Payment schedule: percentages sum to 100, inception at or below 10%.
    # Scoped to the payment schedule section, so the effort-by-deliverable
    # table (which also carries percentages) is not swept in.
    sched = re.search(
        r"^##[^\n]*payment schedule[^\n]*\n(.*?)(?=^##\s|\Z)", md, re.I | re.M | re.S
    )
    sched_md = sched.group(1) if sched else ""
    pct_rows = re.findall(r"\|([^|]*?)\|[^|]*\|[^|]*\|\s*\**(\d{1,3})%\**\s*\|", sched_md)
    if pct_rows:
        pcts = [
            int(p) for label, p in pct_rows
            if not label.strip().lower().lstrip("*").startswith("total")
        ]
        record(
            "ARI-03", "ARITHMETIC",
            "Payment schedule percentages sum to 100",
            sum(pcts) == 100, True, f"sum is {sum(pcts)}",
        )
        inception = [
            int(p) for label, p in pct_rows if re.search(r"inception", label, re.I)
        ]
        record(
            "ARI-04", "ARITHMETIC",
            f"Inception payment at or below {INCEPTION_CAP_PCT}%",
            all(p <= INCEPTION_CAP_PCT for p in inception) if inception else False,
            True, f"inception {inception}",
        )
    else:
        record("ARI-03", "ARITHMETIC", "Payment schedule percentages parsed", False)

    record(
        "ARI-05", "ARITHMETIC",
        "Cost figures use USD only, no other currency symbols",
        not re.search(r"(?<![A-Z])(?:R\d|ZAR|EUR|€|£)", md), True,
    )

    # Each payment amount must equal its stated percentage of the total.
    sched_rows = re.findall(
        r"\|([^|]+)\|[^|]*\|[^|]*\|\s*\**(\d{1,3})%\**\s*\|\s*\**([\d,]+)\**\s*\|",
        sched_md,
    )
    mismatches = []
    for label, pct, usd in sched_rows:
        if label.strip().lower().lstrip("*").startswith("total"):
            continue
        expected = BUDGET_CEILING * int(pct) / 100
        actual = parse_money(usd)
        if actual is not None and abs(actual - expected) > 0.51:
            mismatches.append(f"{label.strip()}: {pct}% of total is {expected:,.0f}, shown {actual:,.0f}")
    record(
        "ARI-06", "ARITHMETIC",
        f"Each payment equals its stated share of the total ({len(sched_rows)} rows)",
        not mismatches, True, "; ".join(mismatches[:4]),
    )

    # Day counts must reconcile between the fee table and the effort split.
    day_totals = [
        parse_money(m) for m in
        re.findall(r"\|\s*\*\*Total[^|]*\*\*\s*\|\s*\**(\d+)\**\s*\|", md)
    ]
    day_totals += [
        parse_money(m) for m in
        re.findall(r"\|\s*\*\*Total\*\*\s*\|\s*\|\s*\**(\d+)\**\s*\|", md)
    ]
    day_totals = [d for d in day_totals if d and d < 1000]
    record(
        "ARI-07", "ARITHMETIC",
        "Day counts reconcile across the fee and effort tables",
        len(set(day_totals)) <= 1 if day_totals else False, True,
        f"found {sorted(set(day_totals))}",
    )


# -------------------------------------------------------------- consistency ---

SCORED_CRITERIA = ["1.1", "1.2", "2.1", "2.2", "2.4", "3.1"]

# The only person named anywhere in either document. Everyone else is a
# placeholder until the EY bid team supplies them.
PERMITTED_NAMES = {"Michael Harris"}

# Organisations and places that legitimately sit in the same cell as a name.
# Stripped before the name scan, so "Michael Harris, Partner, EY Business
# Consulting, South Africa" does not read as three people.
PERMITTED_AFFILIATIONS = [
    "EY Business Consulting", "Business Consulting", "South Africa",
    "Conservation International",
]

# Phrases that would assert an EY credential, engagement or commercial fact.
# Each must sit next to a placeholder or it is an invented claim.
CREDENTIAL_ASSERTIONS = [
    r"\bEY has (?:delivered|advised|led|completed|worked)",
    r"\bwe have (?:delivered|advised|led|completed) ",
    r"\bour client(?:s)?\b",
    r"\bEY(?:'s)? standard (?:rate|commercial)",
    r"\bEY has been (?:appointed|engaged|retained)",
]

# CI's seven stated design aims, and the eight minimum skills from RFP
# section 3. A keyword each, sufficient to prove the topic is present.
DESIGN_AIMS = [
    "financially sustainable", "aggregated", "conservation-led", "data collection",
    "segment", "multi-stakeholder", "fill gaps",
]
KEY_SKILLS = [
    "destination branding", "financial modelling", "global exposure",
    "private sector", "business cases", "stakeholder management",
    "Africa region", "protected areas and conservation",
]


def check_consistency() -> None:
    if not (TECH_MD.exists() and COST_MD.exists()):
        return
    tech = TECH_MD.read_text(encoding="utf-8")
    cost = COST_MD.read_text(encoding="utf-8")

    # Every annex referenced in the body must exist as a heading.
    referenced = set(re.findall(r"\bAnnex ([A-F])\b", tech))
    defined = set(re.findall(r"^##\s+Annex ([A-F])\b", tech, re.M))
    missing = sorted(referenced - defined)
    record(
        "CON-01", "CONSISTENCY",
        f"Every annex cross-reference resolves ({len(defined)} annexes defined)",
        not missing, True, f"referenced but not defined: {missing}",
    )

    # The budget narrative must explain every direct cost line.
    lines = re.findall(r"^\| ([A-Z][^|]{6,70}?) \| (?:Purchase|Word|Interview|Hour) \|", cost, re.M)
    narrative = cost[cost.index("## 6. Budget narrative"):] if "## 6. Budget narrative" in cost else ""
    unexplained = [l.strip() for l in lines if l.strip().split(",")[0][:24] not in narrative]
    record(
        "CON-02", "CONSISTENCY",
        f"Budget narrative explains every direct cost line ({len(lines)} lines)",
        not unexplained, True, "; ".join(unexplained[:3]),
    )

    # Deliverable weeks must agree between the two documents.
    tech_weeks = set(re.findall(r"\(week (\d+)\)", tech))
    cost_weeks = set(re.findall(r"^\| (?:Inception report|Draft [^|]+|Final report[^|]*) \| (\d+) \|", cost, re.M))
    record(
        "CON-03", "CONSISTENCY",
        "Deliverable weeks agree across both documents",
        bool(tech_weeks) and tech_weeks == cost_weeks, True,
        f"technical {sorted(tech_weeks)} vs cost {sorted(cost_weeks)}",
    )

    # Structural integrity of the Markdown sources. A generator that splices a
    # block into the wrong place produces a document that still builds, still
    # reports the right page count and still passes every content check, so
    # these have to be tested directly.
    for label, src in (("technical", tech), ("cost", cost)):
        opens = len(re.findall(r"<div\b", src))
        closes = len(re.findall(r"</div>", src))
        record(
            f"CON-07/{label}", "CONSISTENCY",
            f"{label}: div tags balance in the source",
            opens == closes, True, f"{opens} open, {closes} close",
        )

        nums = [int(n) for n in re.findall(r"^#{2,3}\s+(\d+)\.", src, re.M)]
        record(
            f"CON-08/{label}", "CONSISTENCY",
            f"{label}: numbered sections run in order without gaps",
            nums == list(range(1, len(nums) + 1)), True,
            f"found {nums}",
        )

        marker = src.find('class="annex-start"')
        first_annex = src.find("\n## Annex ")
        record(
            f"CON-09/{label}", "CONSISTENCY",
            f"{label}: no annex heading appears before the annex break",
            marker != -1 and first_annex > marker, True,
            f"annex break at {marker}, first annex heading at {first_annex}",
        )

    # The brief's central rule is that nothing is invented. These enforce it.
    for label, src in (("technical", tech), ("cost", cost)):
        # Where a person would actually be named: the staffing table, and any
        # phrase of the form "Name, Title". Everywhere else, a capitalised pair
        # of words is far more likely to be an organisation or a place, so a
        # blanket bigram scan produces noise instead of findings.
        suspects = set()

        # The staffing table and the client-reference table are the only two
        # places a person is named. Scanning every table sweeps up the
        # organisations in the compliance and benchmark annexes instead.
        for heading, stop in (
            ("### 6. Team and management", "### 7."),
            ("## Annex B: Client references", "## Annex C"),
        ):
            if heading not in src:
                continue
            block = src[src.index(heading):]
            if stop in block:
                block = block[: block.index(stop)]
            for row in re.findall(r"^\|(?![-\s|]*\|).*\|$", block, re.M):
                for c in [x.strip() for x in row.strip().strip("|").split("|")][1:]:
                    if "[[TO CONFIRM" in c or not c or c == "-":
                        continue
                    for phrase in (*PERMITTED_NAMES, *PERMITTED_AFFILIATIONS):
                        c = c.replace(phrase, " ")
                    for n in re.findall(r"\b[A-Z][a-z]{2,} [A-Z][a-z]{2,}\b", c):
                        if n not in PERMITTED_NAMES:
                            suspects.add(n)

        for m in re.finditer(
            r"\b([A-Z][a-z]{2,} [A-Z][a-z]{2,}), (?:Partner|Director|Principal|"
            r"Associate|Manager|Senior|Lead)\b", src
        ):
            if m.group(1) not in PERMITTED_NAMES:
                suspects.add(m.group(1))

        invented = sorted(suspects)
        record(
            f"INV-01/{label}", "INTEGRITY",
            f"{label}: names no person other than {', '.join(PERMITTED_NAMES)}",
            not invented, True, ", ".join(invented[:6]),
        )

        asserted = []
        for pattern in CREDENTIAL_ASSERTIONS:
            for m in re.finditer(pattern, src, re.I):
                window = src[max(0, m.start() - 200):m.end() + 400]
                if "[[TO CONFIRM" not in window:
                    asserted.append(m.group(0))
        record(
            f"INV-02/{label}", "INTEGRITY",
            f"{label}: no EY credential or commercial claim without a placeholder",
            not asserted, True, "; ".join(sorted(set(asserted))[:4]),
        )

    missing_aims = [a for a in DESIGN_AIMS if a.lower() not in tech.lower()]
    record(
        "INV-03", "INTEGRITY",
        f"All seven of CI's design aims appear in the technical proposal",
        not missing_aims, True, f"missing: {missing_aims}",
    )
    missing_skills = [k for k in KEY_SKILLS if k.lower() not in tech.lower()]
    record(
        "INV-04", "INTEGRITY",
        "All eight required skills appear in the technical proposal",
        not missing_skills, True, f"missing: {missing_skills}",
    )

    cm = QA / "compliance_matrix.md"
    if cm.exists():
        text = cm.read_text(encoding="utf-8")

        # Every location the matrix points at must be a heading that exists.
        tech_sections = set(re.findall(r"^###\s+(\d+)\.", tech, re.M))
        tech_annexes = set(re.findall(r"^##\s+Annex ([A-Z])\b", tech, re.M))
        cost_sections = set(re.findall(r"^##\s+(\d+)\.", cost, re.M))
        cost_annexes = set(re.findall(r"^##\s+Annex ([A-Z])\b", cost, re.M))

        dangling = []
        for row in re.findall(r"^\|\s*(C-\d+)\s*\|[^|]*\|[^|]*\|([^|]*)\|", text, re.M):
            ident, where = row
            for doc, secs, annexes in (
                ("Technical Proposal", tech_sections, tech_annexes),
                ("Cost Proposal", cost_sections, cost_annexes),
            ):
                for seg in re.findall(rf"{doc}[^;]*", where):
                    for n in re.findall(r"sections? ((?:\d+(?:,| to | and )?\s*)+)", seg):
                        for num in re.findall(r"\d+", n):
                            if num not in secs:
                                dangling.append(f"{ident}: {doc} section {num}")
                    for a in re.findall(r"Annex ([A-Z])\b", seg):
                        if a not in annexes:
                            dangling.append(f"{ident}: {doc} Annex {a}")
        record(
            "CON-06", "CONSISTENCY",
            "Every compliance-matrix location resolves to a real heading",
            not dangling, True, "; ".join(sorted(set(dangling))[:5]),
        )

        # Every scored criterion must appear in the matrix.
        absent = [c for c in SCORED_CRITERIA if f"criterion {c}" not in text.lower()]
        record(
            "CON-04", "CONSISTENCY",
            "Every scored evaluation criterion appears in the compliance matrix",
            not absent, True, f"missing {absent}",
        )

    # Every placeholder the log transcribes must still exist verbatim in a
    # document. A log entry quoting text that has since been edited is a defect
    # in its own right: it is how a claim removed from a proposal survives in
    # the working files.
    gaps_path = ROOT / "work" / "analysis" / "gaps.json"
    if gaps_path.exists():
        import json as _json
        logged = [
            i.get("placeholderString", "-")
            for i in _json.loads(gaps_path.read_text(encoding="utf-8"))["items"]
        ]
        both = re.sub(r"\s+", " ", tech + " " + cost)
        stale = [
            l for l in logged
            if l.strip() not in ("-", "") and re.sub(r"\s+", " ", l).strip() not in both
        ]
        record(
            "CON-10", "CONSISTENCY",
            "Every placeholder quoted in the open-items log exists in a document",
            not stale, True, f"{len(stale)} stale: " + "; ".join(x[:60] for x in stale[:3]),
        )

    # The open-items log must account for every distinct placeholder.
    oi = QA / "open_items.md"
    if oi.exists():
        placeholders = set()
        for src in (tech, cost):
            placeholders |= set(re.findall(r"\[\[TO CONFIRM:\s*([^\]]{10,60})", src))
        log = oi.read_text(encoding="utf-8")
        unlogged = [p for p in placeholders if p.split(",")[0].strip()[:28].lower() not in log.lower()]
        record(
            "CON-05", "CONSISTENCY",
            f"Open-items log accounts for the placeholders ({len(placeholders)} distinct)",
            len(unlogged) <= len(placeholders) * 0.35, False,
            f"{len(unlogged)} not obviously matched",
        )


# ------------------------------------------------------------------ build ---

def check_build() -> None:
    for label, path in (("technical", TECH_PDF), ("cost", COST_PDF)):
        if not path.exists():
            continue
        reader = PdfReader(str(path))
        fonts = set()
        for page in reader.pages:
            res = page.get("/Resources", {})
            for name in (res.get("/Font") or {}):
                fonts.add(name)
        record(
            f"BLD-01/{label}", "BUILD",
            f"{label}: PDF opens and carries embedded fonts",
            len(reader.pages) > 0 and bool(fonts), True,
        )
        record(
            f"BLD-02/{label}", "BUILD",
            f"{label}: filename follows the submission convention",
            path.name.startswith("EY_") and "CI_RFP_0032026" in path.name, True,
        )

    for name in ("compliance_matrix.md", "open_items.md"):
        record(
            f"BLD-03/{name}", "BUILD",
            f"qa/{name} present",
            (QA / name).exists(), True,
        )

    # Every compliance row must point somewhere real.
    cm = QA / "compliance_matrix.md"
    if cm.exists():
        text = cm.read_text(encoding="utf-8")
        rows = sorted(set(re.findall(r"^\|\s*(C-\d+)\s*\|", text, re.M)))
        unmapped = re.findall(r"^\|\s*C-\d+\s*\|[^|]*\|[^|]*\|[^|]*\|\s*(?:TBC|TBD|\?|)\s*\|", text, re.M)
        record(
            "BLD-04", "BUILD",
            f"Compliance matrix populated ({len(rows)} rows)",
            len(rows) >= 40, True, f"{len(rows)} rows",
        )
        record(
            "BLD-05", "BUILD",
            "Every compliance row maps to a location in the response",
            not unmapped, True, f"{len(unmapped)} unmapped",
        )


def check_sources() -> None:
    """Every figure in the technical body must trace to a source or be ours."""
    script = Path(__file__).with_name("factcheck.py")
    if not script.exists():
        return
    proc = subprocess.run([sys.executable, str(script)], capture_output=True, text=True)
    m = re.search(r"not found in any source\s+(\d+)\s*(.*)", proc.stdout)
    count = int(m.group(1)) if m else -1
    record(
        "SRC-01", "SOURCES",
        "Every figure in the technical body traces to a source or is EY's own",
        count == 0, True, (m.group(2).strip() if m else "factcheck did not run"),
    )
    traced = re.search(r"traced to a source file\s+(\d+)", proc.stdout)
    authors = re.search(r"EY's own estimates\s+(\d+)", proc.stdout)
    if traced and authors:
        record(
            "SRC-02", "SOURCES",
            f"Figures checked: {traced.group(1)} sourced, {authors.group(1)} EY estimates",
            True, False,
        )


def deck_text(path: Path) -> tuple[str, list[str]]:
    """All text in a deck, plus its slide titles."""
    from pptx import Presentation

    prs = Presentation(str(path))
    chunks, titles = [], []
    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.has_text_frame:
                chunks.append(shape.text_frame.text)
                if (shape.is_placeholder
                        and str(shape.placeholder_format.type).startswith("TITLE")):
                    titles.append(shape.text_frame.text.strip())
            elif shape.has_table:
                chunks += [c.text for r in shape.table.rows for c in r.cells]
    return "\n".join(chunks), titles


def check_decks() -> None:
    """The PowerPoint versions answer to the same rules as the PDFs."""
    import collections

    for label, path in (("technical", TECH_DECK), ("cost", COST_DECK)):
        record(f"DCK-01/{label}", "DECKS", f"{label} deck exists", path.exists())
    if not (TECH_DECK.exists() and COST_DECK.exists()):
        return

    for label, path in (("technical", TECH_DECK), ("cost", COST_DECK)):
        text, titles = deck_text(path)

        # EY's accessibility standard requires a unique title on every slide.
        dupes = [t for t, n in collections.Counter(titles).items() if n > 1]
        record(
            f"DCK-02/{label}", "DECKS",
            f"{label} deck: every slide has a unique title ({len(titles)} titles)",
            not dupes, True, f"duplicated: {dupes[:3]}",
        )

        leftovers = [x for x in TEMPLATE_LEFTOVERS if x in text]
        record(
            f"DCK-03/{label}", "DECKS",
            f"{label} deck: no leftover EY template text",
            not leftovers, True, ", ".join(leftovers[:4]),
        )

        check_prose(f"{label} deck", text)

        if label == "technical":
            # Same separation rule as the PDF: benchmark figures are evidence,
            # EY's price for this assignment is not allowed anywhere in it.
            leaks = [
                name for pattern, name in (
                    (r"US\$\s?40[,.]?000", "assignment budget ceiling"),
                    (r"\bper day\b", "day-rate language"),
                    (r"\brate card\b", "rate card reference"),
                    (r"\bprofessional fees\b", "fee line"),
                    (r"\bblended rate\b", "blended rate"),
                    (r"\bpayment schedule\b", "payment schedule"),
                ) if re.search(pattern, text, re.I)
            ]
            record(
                "DCK-04", "DECKS",
                "No EY price, rate or fee appears in the technical deck",
                not leaks, True, ", ".join(leaks),
            )

        left = re.findall(r"\[\[TO CONFIRM", text)
        record(
            f"DCK-05/{label}", "DECKS",
            f"{label} deck: no unresolved placeholders",
            not left, True,
            f"{len(left)} awaiting input; see qa/open_items.md" if left else "",
            blocked=bool(left),
        )


# ------------------------------------------------------------------- main ---

def main() -> None:
    check_submission()
    check_arithmetic()
    check_consistency()
    check_sources()
    check_decks()
    check_build()

    width = max(len(r.check) for r in results) + 2
    current = None
    defects = 0
    blocked = 0
    warnings = 0

    for r in results:
        if r.group != current:
            current = r.group
            print(f"\n{current}")
            print("-" * (width + 24))
        if r.passed:
            mark = "PASS"
        elif r.blocked:
            mark = "WAIT"
            blocked += 1
        elif r.hard:
            mark = "FAIL"
            defects += 1
        else:
            mark = "WARN"
            warnings += 1
        detail = f"  {r.detail}" if r.detail and not r.passed else ""
        print(f"  [{mark}] {r.ident:<18} {r.check:<{width}}{detail}")

    total = len(results)
    passed = sum(1 for r in results if r.passed)
    rule = "=" * (width + 26)
    print(f"\n{rule}")
    print(f"  {passed}/{total} passed   {defects} defect(s)   "
          f"{blocked} blocked on missing input   {warnings} warning(s)")
    if blocked and not defects:
        print("  No defects. The response is not submittable until the blocked")
        print("  items in qa/open_items.md are supplied by the EY bid team.")
    print(f"{rule}\n")

    sys.exit(1 if (defects or blocked) else 0)


if __name__ == "__main__":
    main()
