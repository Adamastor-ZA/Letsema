# Build plan: Unlocking Tourism Growth, final research report

2 November 2026. For Michael's review before drafting starts (brief, step 1). Version 1; the evidence checks in section 6 will be updated once the readers finish.

## 1. What this session has and what it lacks

The brief assumes a working folder, a build system and a skills folder. None of those exist in this cloud session. The repository at `Adamastor-ZA/Letsema` is a GitHub Pages shell with no report material. What exists is the set of uploads below, converted to text in a scratchpad and about to be verified page by page. All outputs will be written into the repository under `report/` on the designated branch, because that is the only location the app can open.

### 1.1 In hand

| Input | Cover date and status | Pages | Role in the report |
| --- | --- | --- | --- |
| `structure.md` | 2 Nov 2026 | n/a | Contract for the report |
| Demand-Side Analysis (final, file dated 01.10) | Cover reads June 2026 | 57 slides | 2.1, 3.1, 3.4, Chapter 5 targets |
| Market Assessment Report | May 2026 | 61 slides | Predecessor of the Demand-Side Analysis; not in the brief's table; used as a working analysis and as the record of the December tree |
| Current State Diagnostic v2 | December 2025 | 68 slides | 1.2, folded into 2.1 and 2.5; December tree on its penultimate pages |
| MIDAS Aviation Market Assessment (final draft, file dated 20.04.26) | Word file, no page numbers | 272 paragraphs, 21 charts | 2.2, 3.2.1 |
| Global Benchmarking Report | 24 March 2026 | 64 slides | 2.3, precedent lines, 4.6 |
| Stakeholder Insights Report (phase 1) | 12 March 2026 | 47 slides | 2.4, 3.3, 4.8, 5.4 |
| SME and Community Inclusion Plan | File dated 9 October 2026 | 58 slides | 2.6, 3.3.1, Chapter 4 pilots, 5.2, A5 |
| Inception Report | 27 November 2025 | 37 slides | 1.1, 1.4, Chapter 2 "what was asked" lines, 4.4 |
| Skift memos: Digital and Search Insights (10 Dec 2025), Segmentation Analysis v2.0 (12 Mar 2026), African Market Analysis v1 (16 Mar 2026) | Working analyses | Word files | Cited only where a deliverable lacks the figure |
| Writing-style skill | Loaded from the synced skills store | n/a | Applied throughout |

### 1.2 Pending

The Infrastructure Report (spatial and infrastructure readiness, June 2026 draft) is still to be added. Until it arrives, 2.5, focus areas 9 to 12 and 14, the readiness-score indicators in 5.2 and Appendix A4 cannot be drafted. Everything else can proceed.

### 1.3 Missing, with the workaround I will apply

| Missing input | What it was meant to supply | Workaround |
| --- | --- | --- |
| Summary of Findings deck, 14 October 2026 | The updated tree (pp15 to 16), dispositions, the eight changes and evidence, the six-week plan, headline figures | Dispositions and one-line reasons come from the Chapter 3 table in `structure.md`, which was drafted from the deck. The December to October changes are reconstructed by comparing the December tree as printed in the Diagnostic, the Market Assessment, the Demand-Side Analysis and the Stakeholder report with the October list. Deck citations are written as (Summary of Findings, 14 Oct 2026, pp15 to 16) and flagged for confirmation. Any figure the structure attributes only to the deck (the 250-call cruise plan, 70% of community product sold by phone, the 104.9% monthly total) is sought in the deliverables first; if absent, it carries a placeholder and an open item |
| SLA Annexure B, signed | Clause wording for 1.1.1 to 1.1.15 | Clause numbers are used as the structure doc and brief give them. The "what was asked" line in each Chapter 2 section is drafted from the Inception Report's phase descriptions and marked for a check against the SLA text |
| Rwanda 2021 and South Africa 2020 recovery plans | Chapter shapes for 4 and 5 | The structure doc already describes the shapes (taxonomy, portfolio table, Gantt, tactical wins, bottom-up costs; targets table by year, dashboard, operating principles). Those shapes are followed from that description. No content was ever to be copied |
| Working folder (district call notes, tree v4, demand model workbook, geocoded inclusion layer, mobility factbase, cruise reports, `Supply_Infrastructure.xlsx`) | Secondary evidence | Entries that need a working-folder figure carry a placeholder and an open item |
| Wesgro and government data (Mero 2024, Pero 2025, G4J 2023, StratEcon cruise reports) | Tier 3 of the source hierarchy | Cited through the deliverable that carries them (the Diagnostic carries Mero, G4J and the cruise contribution study) |
| Build system at `/home/claude/build/` | docx-js helpers and assembler | Rebuilt in the repository under `report/build/` with the same architecture, on docx-js 9.7.1 which is installed globally. Tested: numbered lists render, table headers repeat, the DRAFT header renders, LibreOffice 24.2 converts to PDF |
| Brand fonts | EB Garamond Bold, Raleway Bold | Installed in the sandbox as static Regular, Medium, SemiBold and Bold cuts generated from the Google Fonts variable files; the PDF embeds them. The docx names the fonts, so Wesgro's machines will substitute if they lack them |
| `/mnt/user-data/outputs/` | Output location | Does not exist here; outputs go to `report/outputs/` in the repository |

## 2. Section list, page budgets and inputs

Body target is 140 to 160 pages at A4, 11 point. Budgets below sum to about 152 pages before appendices.

| Section | Pages | Draws on | Notes |
| --- | --- | --- | --- |
| Cover, foreword placeholder, contents, lists, abbreviations | 6 | Inception cover; structure | Foreword marked for Wesgro |
| Scope and objectives | 2 | Inception pp3 to 5; structure | 2.5m reframing stated once |
| Executive summary | 10 to 12 | Chapter 3 toplines in tree order; Demand-Side scenarios; Chapter 4 phase 1; Chapter 5 Tier 1 | Written last; tree redrawn as Figure 1 |
| 1.1 Mandate and objective | 4 | Inception pp3 to 6 (2.8m, 300k jobs, 10k SMMEs, 2x airlift and cruise; mission, vision, eight strategy pillars, outcome metrics); structure for the 2.5m reframing | G4J 2023 and the FY26 to FY30 plan cited through the Diagnostic and Inception |
| 1.2 The system today | 8 | Diagnostic (arrivals FY15/16 to FY24/25, spend, length of stay, source markets, 72.5% Metro GDPR, district GDPR shares, cruise 79 vessels and 127,178 passengers in 24/25, rail and utility constraints); Demand-Side pp7 to 10; MIDAS (Asia against Africa airline count); Inception p7 stakeholder map | Two figures, three tables |
| 1.3 From recovery to growth | 2 | Demand-Side scenario pages; Benchmarking p7 growth norms | Ends on the new markets, new seasons, new regions sentence |
| 1.4 Approach and method | 4 | Inception pp11 to 13 and phase plans; deliverable dates as printed on covers; Stakeholder report (organisations engaged); structure | Six-week completion plan needs the deck; placeholder |
| 1.5 How to read this report | 2 | Structure | Disposition labels including Reworded and Flagged |
| 2.1 Demand-side analysis and market strategy | 9 | Demand-Side Analysis in full; Diagnostic concentration, seasonality and segment pages; Segmentation memo where the deliverable is silent | Growth model, scenarios, groups, spend, segments, India and China route to market |
| 2.2 Aviation market assessment | 7 | MIDAS in full | Citations by section and figure, since the Word file has no page numbers |
| 2.3 Global benchmarking | 8 | Benchmarking report in full; Inception benchmarking section for the screen | Final comparator set stated: see decision 1 |
| 2.4 Stakeholder insights | 7 | Stakeholder report in full | Theme tally, quotes with attribution |
| 2.5 Spatial and infrastructure readiness | 9 | Infrastructure Report [pending]; Diagnostic regional profiles | Shared lead-in with 2.6 on the size of the tourism economy |
| 2.6 SME and community inclusion | 9 | Inclusion plan in full | Concept level; no formalisation, 80:20 or private ownership language |
| 3.1 Reshape Demand | 21 | Six entries at 3 pages plus a one-page introduction | |
| 3.2 Transform Supply | 21 | Six entries plus introduction | Entries 9 to 12 wait for the Infrastructure Report |
| 3.3 Build Enabling Capability | 26 | Eight entries plus introduction | Entry 20 written as a commissioning recommendation |
| 3.4 The integrated case | 3 | Demand-Side scenario and base-case pages | Closes on sequencing |
| 4.1 to 4.8 Execution plan | 27 | Chapter 3; structure's description of the reference shapes; Stakeholder report for risks | Charters at one page each, 15 to 20 pages, may move to A7 if the budget binds |
| 5.1 to 5.7 M&E framework | 17 | Demand-Side model for targets; all deliverables for baselines; Inception p22 | Jobs method: decision 4 |
| Appendices A1 to A9 | Extra | As structure | Only what the body does not carry |

## 3. Decisions the structure leaves open, with the answer I propose

1. **Comparator set for 2.3.** The Benchmarking Report's deep dives are Chile, Melbourne and Victoria, Valencia, Singapore, Kenya and New Zealand. Porto and Vancouver do not appear in it at all. The Diagnostic already records the intention to add Namibia and Kenya. Section 2.3 is written on the report's six, with one sentence on how the set moved from the inception list, and the change is logged in `discrepancies.md`.
2. **Initiative numbering.** Continuous, I1 to In, as the structure prefers for the M&E toolkit. Indicator codes T1-01 onwards, T2-01 onwards and T3-01 onwards. Both appear in `traceability.csv`.
3. **Phase boundaries.** Calendar years as the structure states: Activate 2027 to 2028, Expand 2029 to 2031, Sustain 2032 to 2035. Each phase description maps the boundary to Wesgro fiscal years, so the Phase 1 gate at the end of 2028 falls inside the last year of the FY26 to FY30 plan and a year before the base case reaches the 1.8m seat ceiling in 2030.
4. **Jobs target.** The 300,000 jobs ambition has no labour analysis behind it and focus area 20 is flagged. The deliverables in hand carry only partial employment figures (cruise direct jobs, the CTICC contribution). Unless the Diagnostic or the pending Infrastructure Report carries a provincial tourism employment baseline that can be tied to spend, jobs is carried as a baseline-only Tier 1 indicator with the ratio method described and the gap owned by the labour analysis that focus area 20 commissions. If a baseline exists, the target is set by holding the jobs-to-spend ratio constant against the Demand-Side spend projection and the ratio and source are shown.
5. **Model base year and the market-group figures.** The Demand-Side Analysis projects from a 2024 base of 1,445,031 arrivals to 1,822,634, 2,175,778 and 2,516,282 in 2035. The market-group increments in the structure doc (+179k, +207k, +110k, +176k, +5k) reconcile to the May Market Assessment's 2025 base of 1,498,829, not to the final deliverable, whose increments are about +194k, +224k, +119k, +187k and +6k. The report uses the final deliverable and logs the conflict. The FY25/26 actual of 1.57m already shown in the deliverable is noted in `open_items.md` as a question for the model owner, since it sits above the 2028 base-case point.
6. **Seasonality share.** The 65% October to March figure derives from the 2025 month-of-travel table whose shares sum to 104.9%; the Market Assessment's 2024 figure is 61% on a Cape Town air-arrivals basis. The report uses 65% with the provisional flag and logs both.
7. **Five-market share.** The same slide shows 63% in the graphic and 61% in the text. The report uses 63%, as the structure does, and logs the conflict.
8. **Foreword.** A one-page placeholder addressed to the Wesgro CEO. Letsema can ghost-write it on request; it is not drafted in this pass.
9. **One document or two.** One document. Chapter 5 is the written framework and 5.7 specifies the Excel toolkit; the toolkit workbook itself is outside this build and is listed as an open item.
10. **Citation convention for the MIDAS report.** By numbered section and figure, because the Word file carries no page numbers; stated in 1.5.
11. **Governance focus-area wording.** The December tree reads "Review Institutional Arrangements (Wesgro, DEDAT, CTT)" in the Diagnostic and "(local, provincial and national)" in later decks. The October wording, "Align institutional stakeholders across all three tiers", is used and the drift is recorded in the disposition line.
12. **Date citations.** Each deliverable is cited with the date printed on its cover, which differs from the brief for the MIDAS report (file dated 20 April 2026 against March 2026) and the Inclusion Plan (file dated 9 October against September). Both are logged.
13. **Draft marking.** "DRAFT FOR DISCUSSION" in the header of every page, plus a draft line on the cover.

## 4. How the report is built

The build lives in `report/build/`: `helpers.js` for styles, fonts, captions and numbering (including the `n_policy` pattern and the `n_90` reference registered in `report.js`), `report.js` as the assembler, and one module per chapter (`exec_summary.js`, `ch1_context.js`, `ch2_analysis.js`, `ch3_findings.js`, `ch4_execution.js`, `ch5_me.js`, `appendices.js`). Figures are redrawn as SVG from the extracted data and rendered to PNG through the installed Chromium, since no plotting library is available. PDF conversion runs through LibreOffice, and QA uses `pdftotext` and `pdftoppm`.

Drafting follows the brief's order. The evidence base comes first: every deliverable is read in full by one reader, every figure in the resulting extract is re-checked against the source page by a second, adversarial reader, and a reconciliation pass tests every figure the structure doc cites against the deliverables. Chapter sections are then drafted from the verified extracts, never from the deck or from memory, and each Chapter 3 entry is checked against the six-part template and the traceability table before the pillar is sent.

## 5. QA before return

As the brief sets out: banned words and punctuation; numbered lists numbered; table headers kept with their rows; captions and sources on every figure and table; 20 entries with six parts; every initiative in 4.2, 4.3 and 4.4; every Tier 1 and Tier 2 indicator with a baseline or a dated gap; executive summary claims matched to Chapter 3 toplines; no figure sourced to the deck where a deliverable carries it; page count by chapter against budget.

## 6. Evidence checks completed so far

To be completed when the readers report. Already established from a first reading: the base-year conflict in decision 5; the 61% against 63% and the 104.9% total in decisions 6 and 7; the comparator set in decision 1; the absence of Porto and Vancouver from the Benchmarking Report; the Diagnostic's cruise figures (79 vessels, 127,178 passengers, 1,789 direct jobs in 2024/25, pending verification of the chart reading).

## 7. Traceability skeleton

`report/traceability.csv` holds the 20 focus areas with pillar, theme, disposition and one-line reason from the structure doc, the December entry each descends from, the workstream, and empty initiative and indicator columns. Nineteen descend from the eighteen December entries (air and cruise split; path to purchase, seasonality, growth markets, sustainability and institutional arrangements reworded; inclusion refined; the deficits entry moved from theme 2.1 to 3.2) and one, workforce and service skills, is new and flagged. That is nine changes against the deck's eight; the deck will settle the count.
