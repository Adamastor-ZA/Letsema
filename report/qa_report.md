# QA report: draft v2

7 November 2026. Results of checks 3 to 8 in section 8 of the red-team brief, run on `outputs/Unlocking_Tourism_Growth_Final_Report_DRAFT_v2.docx` and `.pdf` against draft v1 rebuilt unchanged from the same source. Text extracts are in `qa/`: `v1.txt` and `v2.txt` (`pdftotext -layout`), with `v1_raw.txt` and `v2_raw.txt` (`-raw`) for page lookups. Pages are PDF pages, which equal the printed footer numbers.

## Build

The docx is built by `build/report.js` through the project's `build.sh` (two passes for the contents pages; LibreOffice converts to PDF). The brief's `/home/claude/build/` and `soffice.py` do not exist in this project; the build lives at `report/build/` and `build.sh` calls `soffice` directly. `NODE_PATH=$(npm root -g)` is set by `build.sh`. The DRAFT FOR DISCUSSION header is on every page of v2.

## Check 3: unexplained changes ("change nothing else")

Method: every paragraph of each .docx (body text and table cells) was extracted and the two sequences aligned with `difflib` (`build/redteam/diff_v1_v2.py`). Each changed paragraph was matched against the edit log (`build/redteam/applied.json`), which records every edit the patch script made, with its change ID.

| Measure | Result |
| --- | --- |
| Paragraphs in v1 / v2 | 7,663 / 7,729 |
| Changed paragraphs mapped to a change ID or a logged Consequential edit | 347 |
| Contents, list-of-figures and list-of-tables lines whose only change is a page number | 141 |
| Unexplained changed paragraphs | **0** |
| Reverted | None needed |

Figures are images, so they were checked separately: seven chart files changed (`build/assets/svg`), and each maps to a change ID. These are ES.2, 1.4, 2.1 and 5.2 (C1.1 label, P3 axis, P2 and P3 notes), 2.5 (M2), 4.1 (P4) and 4.3 (C6.4). Every other figure, the hypothesis tree (Figure ES.1) included, is unchanged byte for byte.

Table rows: a row check (`build/redteam/rows_check.py`) looked for every row of every table in the PDF text. In v1 six rows were missing, all in Table 5.2 (P1). In v2 none are missing.

The source edits sit in one script (`build/redteam/apply_v2.py`), so each one can be traced to its find string, its expected count and its replacement. The JSON formatting of the content modules was normalised in a separate commit beforehand, with no content change, so the v2 diff shows only real edits.

## Check 4: grep checks on v2

Counts in the PDF text, v1 against v2.

| Term | v1 | v2 | Remaining hits and reason |
| --- | --- | --- | --- |
| seat ceiling | 31 | 0 | |
| hard ceiling at 1.8 | 4 | 2 | Both verbatim quotations of the source decks, kept under rule 4: p46 ("a hard ceiling at 1.8 million inbound seats") and p167 (both decks quoted in A2) |
| about 65% | 7 | 0 | |
| About 30,000 (2025) | 1 | 0 | |
| two jobs per 100 | 4 | 0 | |
| Plan decision | 1 | 0 | |
| Michael | 1 | 0 | |
| agreed report structure | 7 | 0 | |
| agreed structure | 2 | 0 | |
| house style | 2 | 0 | |
| Auckland Park | 1 | 0 | |
| unsigned Open Skies | 2 | 0 | |
| 2024 Ghana visa waiver | 3 | 0 | |
| Treasury Circular 131 | 10 | 0 | |
| Chilean model | 3 | 0 | |
| George as second gateway | 2 | 0 | |
| SAT is in turmoil | 1 | 0 | |
| national marketing body is weak | 2 | 0 | |
| US$1,650 | 2 | 0 | |
| 13 million international visitors | 1 | 0 | |
| misprints | 2 | 0 | |

## Check 5: rendering

Pages were rendered to images and inspected.

| Item | v2 page | Result |
| --- | --- | --- |
| Table 5.2 | 150 | Rows I6 to I11 show. Cause in v1: the header row sat alone at the foot of p147 and LibreOffice dropped the rows after it. The header row is now kept with the first body row (`helpers.js`). |
| Figure ES.2 | 18 | True time axis (2025, 2028, 2031, 2035 at their real distances); label "1.8m seat line (model)"; spacing note gone; nothing cut off |
| Figure 1.4 | 34 | True time axis (2034 and 2035 one year apart); new label; the note that ran off the edge is now the end of the source line |
| Figure 2.1 | 45 | True time axis; new label; its own note (straight lines between printed points) is unchanged and fits |
| Figure 2.5 | 55 | Chile 40.4, Singapore 21, Kenya 14.6, reference bar 11 labelled "World, 2024 (UN Tourism)"; bar order and colours unchanged |
| Figure 4.1 | 119 | All eighteen full initiative names show, on two lines where needed |
| Figure 4.3 | 145 | The new co-chair label overflowed the box on the first v2 render; set at 17px for that one label, it now fits. Nothing else moved |
| Table 4.7 | 147 to 148 | Fourteen rows. "Likelihood" and "Medium" break mid-word in their narrow columns, as in v1 (not changed) |
| Table ES.5 | 19 | New title; Steerco row owner "Wesgro CEO's office; DEDAT" |
| Table ES.6 | 20 | T1-01 model value, T1-03 nominal and constant-rand labels, T1-04 set by the labour analysis, T1-05 38.1%, T1-07 R4m to R10m; new source note |
| Decisions | 20 to 21 | "The Wesgro Board decides:" with items 1 to 5, then "The Board recommends ...:" with items 6 and 7, numbered on through the split |
| v1 p44 gap (P13) | 44 to 45 | **Not fixed.** No forced page break or extra keep setting causes it. The gap is left by Figure 2.2, which is too tall for the rest of the page and moves whole because its image is kept with its caption. In v2 the gap falls on p45, and p44 ends about a third empty because Figure 2.1 moved down. Removing the keep would split a figure from its caption, and the brief rules out moving content |

## Check 6: style of new text

Dashes in the PDF text: em dashes 0 in v1 and 0 in v2; en dashes 2 in v1 and 2 in v2, both inside verbatim Benchmarking Report quotations on p56 ("Public–Private Air Access Fund"; "public–private structure"). v2 has no more than v1.

Inserted text (`build/redteam/style_scan.py`, 303 new sentences):

- Banned words: none, except the proper name "Unlocking Tourism Steerco" in the C6.4 text the brief supplies (the study's own name, as in the report title).
- Dashes: none.
- Oxford commas: one, in the brief's own C3.1 text ("returning residents, or OAG"); removed. The other eleven comma flags were reviewed and are clause commas, not list commas.
- Sentences over 25 words: 28. Of these, 27 are the brief's wording kept verbatim. The other is the Figure 2.5 source note, a list of citations (Consequential, M2).
- UK spelling throughout the new text; citations in the report's form.

`qa_structure.py` passes with zero issues on v2. `qa_text.js` raises the same kinds of heuristic flags as at v1 (bracketed open items, clause commas, long source lines); none of the new flags is a style breach in the sense of rule 7.

## Check 7: matching toplines

| Focus area | Chapter 3 | Executive summary | Match |
| --- | --- | --- | --- |
| FA2 | 3.1.1, p74 | Table ES.2, p16 | Word for word |
| FA6 | 3.1.2, p83 | Table ES.2, p16 | Word for word |
| FA13 | 3.3.1, p99 | Table ES.4, p17 | Word for word |
| FA16 | 3.3.2, p105 | Table ES.4, p17 | Word for word |

FA2 and FA6 sit in Table ES.2 (Pillar 1), not ES.3 as the brief has it. `qa_structure.py` also confirms all twenty toplines appear verbatim in the executive summary.

## Check 8: page count

| Part | v1 | v2 |
| --- | --- | --- |
| Front matter | 12 | 12 |
| Executive summary | 9 | 9 |
| 1 Context | 20 | 21 |
| 2 Analysis summaries | 28 | 28 |
| 3 Findings and recommendations | 46 | 46 |
| 4 Execution plan | 31 | 32 |
| 5 Monitoring and evaluation | 11 | 11 |
| Appendices A1 to A9 | 34 | 34 |
| **Total** | **191** | **193** |
