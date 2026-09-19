# EY response to Conservation International RFP 0032026

Brand-delivery support models for emerging protected areas in Africa.

Engagement partner: Michael Harris, Partner, EY Business Consulting, South Africa.

## What gets submitted

Two PDFs, submitted separately as the RFP requires, plus one form CI must issue.

| File | Contents |
|---|---|
| `build/EY_Technical_Proposal_CI_RFP_0032026.pdf` | Parts 1, 2 and 3 in a five-page body, then Annexes A to F |
| `build/EY_Cost_Proposal_CI_RFP_0032026.pdf` | Budget, budget narrative, payment schedule, Annexes A to C |
| Offeror Representation of Transparency, Integrity and Social Responsibility | CI-issued form, not generated here. See `qa/open_items.md` OI-01. |

The technical proposal carries no price, rate or fee. Only the financial
proposals of bidders who qualify technically are opened, so the two files are
kept strictly separate and `scripts/qa.py` fails the build if pricing leaks
into the technical file.

## How to change something

Everything is authored in Markdown. Edit the source, rebuild, re-check.

```bash
python3 scripts/build.py          # rebuild both PDFs into ./build
python3 scripts/build.py cost     # rebuild one
python3 scripts/qa.py             # run the QA gate; non-zero exit means work remains
```

`build.py` reports each document's page count and flags the technical proposal
if its body runs past five pages. The cap is measured on the pages before
Annex A.

Three generators sit behind the working documents. Run them after editing
anything in `work/analysis/`:

```bash
python3 scripts/make_qa_docs.py   # regenerates everything in qa/, including STATUS.md
python3 scripts/make_annex_e.py   # the compliance annex inside each PDF
python3 scripts/build.py && python3 scripts/qa.py
```

`qa/STATUS.md` is the one-page view: what builds, what the QA gate says, how
many open items there are and who owns them, the blockers, and what to do
next. It is generated, so it is never out of date with the documents.

## Layout

```
inputs/     the three source files, untouched
work/       inputs converted to Markdown, plus analysis/ holding the content spine as JSON
proposal/   the Markdown sources for both documents
assets/     ey.css, the EY document style
scripts/    build, QA and the generators
qa/         STATUS.md, compliance matrix, open items, checkpoints and QA checks
build/      generated PDFs and intermediate HTML; safe to delete
```

## The five-page cap

The RFP prints "max 5 pages (excluding annexes)" in the Part 1 row of its
submission table, which leaves it ambiguous whether the cap covers Part 1 alone
or the whole technical proposal. This response takes the strict reading and
keeps the entire body, Parts 1 to 3, within five pages, with all evidence in
annexes. That reading cannot lose points under either interpretation. It is
also logged as a clarification question for CI.

## Placeholders and what is missing

Anything the inputs do not supply is marked `[[TO CONFIRM: what is needed]]`
and logged in `qa/open_items.md` with an owner, a severity and the checkpoint
it must be resolved by. Placeholders render as yellow highlights in the PDF so
they cannot be missed, and the QA gate reports them as blocked rather than as
defects, because they are missing inputs rather than faults in the work.
Nothing is invented to fill a gap.

Two things about the gaps are worth knowing before reading anything else.

The first is where the marks are. Relevant experience, services in the last
three years with samples, geographical reach and staff qualifications carry 60
of the 70 technical marks between them, and all of it rests on EY credentials,
client references, CVs and work samples that were not in the inputs. The five
pages EY can write unaided are worth 10 marks. Clearance, consent and CV
collection are the critical path, not drafting.

The second is that the RFP itself is incomplete. The copy supplied begins at
Section 2, so the instructions to bidders are absent, and the "Level of Effort
and Cost of Services" section ends mid-sentence after the budget ceiling. There
is no submission deadline, no submission address and no point of contact. Those
are blockers, not details.

## Provenance of the brief

The build brief supplied to this repository was truncated. It ended inside
Section 2 and Sections 3 to 10 are absent entirely. Sections 11 and 12, the
partner review checkpoints and the QA checks that define done, are referenced
by the brief but were never supplied. `qa/checkpoints_and_qa.md` reconstructs
both from the RFP and normal bid practice, clearly labelled as a reconstruction
for Michael to correct rather than a record of what was agreed.

## Typeface

The EY brand font is EY Interstate, taken from the theme of the PowerPoint in
`inputs/`. It is not installed in this build environment, so `assets/ey.css`
falls back to Inter, which is metrically close. Rebuilding on a machine with EY
Interstate installed restores the brand font with no other change. The EY logo
asset was not supplied either; the masthead reserves its position and
proportion.
