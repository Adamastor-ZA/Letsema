#!/usr/bin/env python3
"""
Rewrite the compliance matrix's "where it is met" column onto the real
structure of the two proposal documents.

The analysis agent that produced the matrix assumed its own section numbering.
The documents are the source of truth, so this maps the agent's references onto
the headings that actually exist. Ordered longest-pattern-first, so that
"Part 1, section 2.4" is rewritten before "Part 1, section 2".

    python3 scripts/remap_locations.py

Re-run it after renumbering a section, then regenerate the matrix with
scripts/make_qa_docs.py.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "work" / "analysis" / "compliance.json"

T = "Technical Proposal"
C = "Cost Proposal"

SKILLS = {
    "a": "brand development and destination branding",
    "b": "business planning, business models and financial modelling",
    "c": "global exposure in tourism and brand management",
    "d": "working with the private sector and securing investment",
    "e": "presentation of business cases and pitching",
    "f": "stakeholder management and partnerships",
    "g": "experience of the Africa region and tourism landscape",
    "h": "experience in protected areas and conservation",
}

# (pattern, replacement). Order matters: most specific first.
RULES: list[tuple[str, str]] = [
    # output files
    (r"Two output files:.*?\.pdf",
     "Two separate PDFs: EY_Technical_Proposal_CI_RFP_0032026.pdf and "
     "EY_Cost_Proposal_CI_RFP_0032026.pdf"),

    # the Representation is a separate submission item, not an annex
    (rf"{T} Annex D\b",
     "Submitted separately alongside both PDFs, per RFP section 4; "
     f"referenced at {T} section 12"),

    # Part 3 skill rows
    *[(rf"{T} Part 3, section 5\.1\({k}\)",
       f"{T} @@SKILLS@@, skill row: {v}")
      for k, v in SKILLS.items()],

    # Part 3 sections
    (rf"{T} Part 3, sections 5\.1 and 5\.2", f"{T} sections 8 and 9, with @@SKILLS@@"),
    (rf"{T} Part 3, section 5\.1", f"{T} section 8, with @@SKILLS@@"),
    (rf"{T} Part 3, section 5\.2", f"{T} section 9, with @@ASSIGNMENTS@@"),
    (rf"{T} Part 3, section 5\.3", f"{T} section 11, with @@REFS@@"),
    (rf"{T} Part 3, section 5\.4", f"{T} section 6"),
    (rf"{T} Part 3, section 5\.5", f"{T} section 10"),

    # Part 2
    (rf"{T} Part 2, section 4\.2", f"{T} section 6"),
    (rf"{T} Part 2, section 4", f"{T} section 6"),

    # Part 1 sections. 2.4 and 2.x before bare 2.
    (rf"{T} Part 1, section 2\.4", f"{T} section 5"),
    (rf"{T} Part 1, sections? 2\.1 and 2\.2", f"{T} sections 3 and 4"),
    (rf"{T} Part 1, section 2\.2 and 2\.4", f"{T} sections 3, 4 and 5"),
    (rf"{T} Part 1, section 2\.1", f"{T} section 3 (Activity One)"),
    (rf"{T} Part 1, section 2\.2", f"{T} section 3 (Activity Two) and section 4"),
    (rf"{T} Part 1, section 2\.3", f"{T} section 3, interviews and appetite test"),
    (rf"{T} Part 1, sections 1-2", f"{T} sections 1 to 5"),
    (rf"{T} Part 1, section 1", f"{T} section 1"),
    (rf"{T} Part 1, section 2\b", f"{T} section 3"),
    (rf"{T} Part 1, section 3", f"{T} section 9, with @@ASSIGNMENTS@@"),
    (rf"{T} Part 1 body", f"{T} body, sections 1 to 12, before @@CVS@@"),

    # bare "Part 1, section x" (no document prefix)
    (r"\bPart 1, sections? 2\.1 and 2\.2", f"{T} sections 3 and 4"),
    (r"\bPart 1, section 2\.2", f"{T} section 3 (Activity Two) and section 4"),
    (r"\bPart 1, section 2\.1", f"{T} section 3 (Activity One)"),

    # Annex letters the agent used, resolved through sentinels so that letters
    # emitted by the rules above are never re-mapped on a later pass.
    (r"\bAnnex F Gantt\b", "@@PLAN@@"),
    (r"the detailed plan in Annex F", "the detailed plan in @@PLAN@@"),
    (r"\bAnnex E \(samples of work\)", "@@ASSIGNMENTS@@ and @@SCAN@@"),
    (r"\bAnnex C \((?:global reach|country footprint map|Africa footprint)\)",
     f"{T} section 10"),
    (r"\bAnnex C country footprint map", f"{T} section 10"),
    (r"\bAnnex B \(three-year column\)", "@@ASSIGNMENTS@@, last three years"),
    (r"\bAnnex B \(five-year column\)", "@@ASSIGNMENTS@@, last five years"),
    (r"\bAnnex B\b(?!:)", "@@ASSIGNMENTS@@"),
    (r"\bAnnex A\b(?!:)", "@@CVS@@"),

    # cost proposal
    (r"Cost Annex 1 \(LOE derivation\)", f"{C} @@COSTLOE@@"),
    (rf"{C} Table 1 columns: unit, unit price USD, quantity, line total USD",
     f"{C} sections 2 and 3, columns: unit, quantity, unit price US$, total US$"),
    (rf"{C} Table 1 grand total and section 1", f"{C} section 1, summary table"),
    (rf"{C} Table 2 \(payment schedule\)", f"{C} section 5"),
    (rf"{C} Table 2 \(milestone 1, capped at 10%\)", f"{C} section 5, milestone 1"),
    (rf"{C} Table 2 \(milestone ([0-9]+)\)", rf"{C} section 5, milestone \1"),
    (rf"{C} Table 2 \(final milestone\)", f"{C} section 5, final milestone"),
    (rf"{C} Table 2", f"{C} section 5"),
    (rf"{C} throughout - Table 1, Table 2 and narrative",
     f"{C} sections 1 to 6"),
    (rf"{C} in full - Table 1, Table 2, sections 3, 4 and 5",
     f"{C} in full, sections 1 to 9"),
    (rf"{C} section 1 \(basis of price\)", f"{C} section 1"),
    (rf"{C} section 3, one narrative entry per Table 1 line",
     f"{C} section 6, one narrative entry per line item"),
    (rf"{C} section 5 \(assumptions and supporting detail\)", f"{C} section 9"),
    (rf"{C} section 5 \(stated assumption and unit price for [^)]*\)", f"{C} section 9"),
    (rf"{C} section 4 \(tax statement\)", f"{C} section 7"),
    (rf"{C} section 1 and Table 1 grand total", f"{C} section 1, summary table"),
    (r"plus the stakeholder engagement plan in Part 1, section 2\.3",
     f"plus the interview and appetite-test method at {T} section 3"),
    (r"\(team structure\) and Part 3, section 5\.4", "(team structure) and section 8"),
    (rf"{C} Table 1", f"{C} sections 2 and 3"),
]


SENTINELS = {
    "@@CVS@@": "Annex A",            # curricula vitae
    "@@REFS@@": "Annex B",           # client references
    "@@SKILLS@@": "Annex C",         # capability against the eight skills
    "@@ASSIGNMENTS@@": "Annex C",    # relevant assignments, inside Annex C
    "@@PLAN@@": "Annex D",           # detailed work plan
    "@@SCAN@@": "Annex F",           # benchmark scan extract
    "@@COSTLOE@@": "Annex B",        # cost proposal: effort by week
}


def main() -> None:
    data = json.loads(SRC.read_text(encoding="utf-8"))
    changed = 0
    for row in data["rows"]:
        # The rules rewrite the agent's numbering into this repository's own
        # annex letters, so running them over already-rewritten text would
        # remap those letters again. Each row is therefore stamped once.
        if row.get("locationRemapped"):
            continue
        before = row["whereMet"]
        after = before
        for pattern, repl in RULES:
            after = re.sub(pattern, repl, after)
        for sentinel, real in SENTINELS.items():
            after = after.replace(sentinel, real)
        after = re.sub(r"\s{2,}", " ", after).strip()
        row["locationRemapped"] = True
        if after != before:
            row["whereMet"] = after
            changed += 1
    SRC.write_text(json.dumps(data, indent=1), encoding="utf-8")

    stale = [
        r["id"] for r in data["rows"]
        if re.search(r"Part [123], section|Table [12]\b|Annex 1\b", r["whereMet"])
    ]
    print(f"remapped {changed}/{len(data['rows'])} rows")
    if stale:
        print("still using the old numbering:", ", ".join(stale))
    else:
        print("no stale references remain")


if __name__ == "__main__":
    main()
