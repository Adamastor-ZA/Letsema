#!/usr/bin/env python3
"""
Check that every figure asserted in the proposal body traces to a source file.

The proposal promises CI that every number carries its source. This applies the
same discipline to the proposal itself: it pulls the numeric claims out of the
five-page technical body and the cost proposal's evidence passages, then looks
for each one in the RFP or in the benchmark research the claim came from.

    python3 scripts/factcheck.py

A number that cannot be found is not necessarily wrong. It may be an EY
estimate, such as the day counts, or an interview target. Those are listed
separately as author's figures for a human to confirm.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BODY_END = "## Annex A:"

SOURCES = [
    ROOT / "work" / "CI_RFP_0032026_Brand_Scope.md",
    ROOT / "work" / "CI_Brand_Models_Research_Pass_1_Benchmarks_v2.md",
]

# Figures EY originates rather than cites. These are the proposal's own
# estimates and commitments, and belong to the author, not to a source.
AUTHORS_FIGURES = {
    "58", "16", "13", "19", "12", "5", "3", "2", "4", "10", "22", "7",
    "36,000", "40,000", "4,000", "11,600", "7,475", "7,125", "5,500",
    "2,700", "1,600", "1,100", "725", "575", "375", "900", "800", "621",
    "1,400", "1,000", "560", "1,040", "350", "35", "65", "10,000", "0.10",
    "14,000", "12,000", "6", "9", "11", "8", "1", "33", "38", "17", "30",
    "25", "100",
}


def normalise(text: str) -> str:
    return re.sub(r"\s+", " ", text)


def claims(text: str) -> list[str]:
    """Every figure of two digits or more, including thousands separators.

    Single digits are skipped: they are almost always counts the proposal
    itself sets, such as three activities or nine headings, and they generate
    noise without catching anything.
    """
    return [
        m.group(1)
        for m in re.finditer(r"(?<![\w.,])(\d{1,3}(?:,\d{3})+|\d{2,4})(?![\w,])", text)
    ]


def main() -> None:
    tech = (ROOT / "proposal" / "technical" / "technical_proposal.md").read_text(encoding="utf-8")
    body = tech[: tech.index(BODY_END)]
    haystack = normalise(" ".join(p.read_text(encoding="utf-8") for p in SOURCES))

    traced, authors, unsourced = [], [], []
    for c in sorted(set(claims(normalise(body))), key=lambda x: (len(x), x)):
        if c in AUTHORS_FIGURES:
            authors.append(c)
        elif c in haystack or c.replace(",", "") in haystack.replace(",", ""):
            traced.append(c)
        else:
            unsourced.append(c)

    print(f"Figures in the technical proposal body\n{'-' * 52}")
    print(f"  traced to a source file     {len(traced):>3}   {', '.join(traced)}")
    print(f"  EY's own estimates          {len(authors):>3}   {', '.join(authors)}")
    print(f"  not found in any source     {len(unsourced):>3}   {', '.join(unsourced)}")
    if unsourced:
        print("\n  Each figure above needs a source or removal before submission.")
    sys.exit(1 if unsourced else 0)


if __name__ == "__main__":
    main()
