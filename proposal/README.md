# EY response to Conservation International RFP 0032026

Brand-delivery support models for emerging protected areas in Africa.

Engagement partner: Michael Harris, Partner, EY Business Consulting, South Africa.

## What gets submitted

Two PDFs, submitted separately as the RFP requires.

| File | Contents |
|---|---|
| `build/EY_Technical_Proposal_CI_RFP_0032026.pdf` | Parts 1, 2 and 3 in a five-page body, then annexes |
| `build/EY_Cost_Proposal_CI_RFP_0032026.pdf` | Detailed budget, budget narrative, payment schedule |

A third item, the signed Offeror Representation of Transparency, Integrity and
Social Responsibility, is a CI-issued form. It is not generated here; see
`qa/open_items.md`.

## How to change something

Everything is authored in Markdown. Edit the source, rebuild, re-check.

```bash
python3 scripts/build.py          # rebuild both PDFs into ./build
python3 scripts/build.py cost     # rebuild one
python3 scripts/qa.py             # run the QA gate; non-zero exit means a hard failure
```

`scripts/build.py` reports the page count of each document and flags the
technical proposal if its body exceeds the five-page cap. The cap is measured
on the pages before Annex A, which is the strictest reading of the RFP.

## Layout

```
inputs/     the three source files, untouched
work/       inputs converted to Markdown, plus the analysis spine
proposal/   the Markdown sources for both documents
assets/     ey.css, the EY document style
scripts/    build.py and qa.py
qa/         compliance_matrix.md and open_items.md
build/      generated PDFs and intermediate HTML; safe to delete
```

## Placeholders

Anything the inputs do not supply is marked `[[TO CONFIRM: what is needed]]`
and logged in `qa/open_items.md` with an owner and a severity. Placeholders
render as yellow highlights in the PDF so they cannot be missed, and
`scripts/qa.py` fails the build while any survive. Nothing is invented to fill
a gap.

Most of the outstanding items are EY credentials, named staff, client
references and the rate card. That matters more than it sounds: 60 of the 70
technical points sit in experience, work samples, geographical reach and staff
qualifications, and none of that material was in the inputs.

## Typeface

The EY brand font is EY Interstate, taken from the theme of the PowerPoint in
`inputs/`. It is not installed in this build environment, so the CSS falls
back to Inter, which is metrically close. Rebuilding on a machine with EY
Interstate installed restores the brand font with no other change.
