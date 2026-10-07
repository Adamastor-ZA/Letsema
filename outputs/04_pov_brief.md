# Brief: write the point of view on cost reduction through centralisation at Absa Financial Services

Execute this brief. It produces two outputs: a detailed point of view as a Word document and a short deck as a PowerPoint file. It builds only on the evidence base already in this folder. It does not re-run the research.

## Role and audience

You are writing for an EY partner who will present a point of view (POV) to the managing executive of Absa Financial Services (AFS). The managing executive owns the insurance, advice and investment businesses of Absa Group and has concluded an operating model review that calls for a degree of centralisation. They want to know what centralisation is worth, where the money is, what it will cost to get, and what they should ask their own finance function before committing to a number. They are time-poor, numerate and will have their chief financial officer and chief actuary check every figure. Write as a senior adviser who has done the work, not as a vendor.

## Inputs (read all before writing)

1. `00_summary.md`: the one-page synthesis and the five hypotheses.
2. `01_framework.md`: the MECE cost tree, lever classification, the entity and licence map with the contradictions to the client's own description, what does not centralise cleanly, and the scoping decisions.
3. `02_afs_cost_structure.md`: the AFS cost base from public information, the reconciliation, the pool mapping, the addressable base and the ten management information items.
4. `03_benchmark.md`: the peer benchmark, normalisation rules, gap sizing and precedents.
5. `afs_cost_benchmark.xlsx`: every figure, live. Use the Gap sizing and AFS cost base tabs for numbers; every number you quote must trace to a data_id on the Raw data tab or to a labelled assumption on the Normalisation tab.
6. `verification_report.md`: what was checked and the three labelling notes.
7. `source_log.csv`: the 249 sources with URLs and pages.

## Rules

1. No number without a source. Quote figures exactly as they appear in the workbook and cite the data_id or the assumption name in a footnote or source line. Do not round a range into a point estimate.
2. Keep the three tags. A figure is Fact, Derived or Assumption (dagger) and the reader must be able to see which. Every assumption carries its low, base and high.
3. State the accounting basis the first time a figure appears: IFRS 17, segment basis, cash view, economic. Never put the reported 40 percent cost-to-income ratio next to an insurer expense ratio.
4. Every rand figure for savings is a hypothesis range, never a target. Say so in the executive summary, on the sizing page of the deck and in the recommendation.
5. Separate the three perimeters without fail: Insurance SA (the underwriters and head office), the advice and investment block, and the bank. Say where each saving lands.
6. Do not invent operating detail. Where the public record is silent (headcount, policies, attributable split, recharges, reinsurance, entity FY2025), say it is silent and point to the management information request.
7. UK English, answer first, short sentences, no em dashes, no Oxford commas. Prose over bullets in the document; prose-bullets in the deck.
8. Do not use the words leverage, synergy, journey, unlock, ecosystem or landscape.

## Output 1: the detailed point of view (Word, about 20 to 25 pages plus appendices)

Write it as `05_pov_afs_centralisation.docx`, A4 portrait, Arial, with landscape sections for the wide tables. Structure:

1. Executive summary (one page). The answer, the range, the three places the money sits, the two decisions the managing executive must take, and the first management information request. Someone who reads only this page must leave with the case.
2. What AFS is today (two pages). The verified entity and licence map from `01_framework.md` section 1, the three corrections to the client's own description (Kenya still underwrites at FY2025, the asset management licences left in 2022, four insurance licences with one closed in 2025), the 2026 move to three pan-African business units, and the segment perimeter changes. One table.
3. The cost base (four pages). Insurance SA FY2023 to 1H2026 on the stated basis, the division view, the head office, the intermediary block, the intra-group flows, and the top-down and bottom-up reconciliation. Use the tables from `02_afs_cost_structure.md` sections A to F. End on the pool mapping (section G) and the addressable base (section H).
4. Where AFS stands against peers (four pages). The normalisation rules in plain words, then the four comparisons that carry the argument: as-reported overhead by division, the comparable expense ratio, acquisition cost with and without the bank fee, and the non-life combined ratio before and after overhead. One chart per comparison, built from the Benchmark tab. Name the peer group and the count under each chart.
5. The five hypotheses (five pages, one each). For each: the claim, the evidence with data_ids, the tree cells it maps to, the lever class (direct, adjacent, independent), the rand range, the regulatory constraint that binds it from `01_framework.md` section 7, and the management information that would confirm or kill it.
6. What centralisation can and cannot do (two pages). The direct, adjacent and independent split (18, 25 and 11 cells), what does not centralise cleanly, the VAT warning, and the point that leakage is independent of the operating model.
7. The size of the prize and what it costs (two pages). The envelope R252m to R754m with its components, the precedent evidence (table from `03_benchmark.md` section 5, trimmed to the eight programmes with a base), the cost to achieve by lever mix, and the capital line kept separate.
8. Recommendation and next steps (one page). The two decisions (perimeter for the economics, and whether licences and platforms are in or out of the programme), the ten management information items as a request list with owner and timing, and a 90-day plan to convert the hypothesis range into a target.
9. Appendices. The full cost tree with classification; the full benchmark tables; the precedents table; the assumptions register from the Normalisation tab with low, base and high and rationale; the source log; the verification summary.

Build the Word file with the docx skill. Charts are images rendered from the workbook data with the dataviz skill, brand-neutral palette, one series per peer group, AFS highlighted. Tables keep the data_id column. Put a one-line source under every table and chart.

## Output 2: the short deck (PowerPoint, 12 to 15 slides)

Write it as `06_pov_afs_centralisation.pptx` using the pptx-master skill with the EY profile and the EY master template. Every content slide follows the house pattern: an ALL-CAPS topic header, one topline thesis sentence in lean declarative prose, three to five prose-bullets that evidence it, a source line, and the DRAFT watermark. Slides:

1. Title.
2. THE ANSWER. Centralisation is worth a hypothesis range of R252m to R754m a year, base R468m, about a third of Insurance SA profit before tax; the money is in the non-life book, the head office and the advice business, not in life or in acquisition.
3. WHAT AFS IS. The licence map and the three corrections.
4. THE COST BASE. Insurance SA FY2025 in one waterfall: revenue to service expenses to overhead to profit, with the head office called out.
5. THE OVERHEAD IS NON-LIFE AND HEAD OFFICE. Division overhead ratios against peer medians.
6. THE UNDERWRITING IS GOOD AND THE OVERHEAD SPENDS IT. Combined ratio before and after overhead against the South African non-life set.
7. ACQUISITION IS A TRANSFER PRICE. Acquisition ratio with and without the R774m bank fee against composite peers.
8. THE ADVICE BUSINESS IS THE BIGGER PROBLEM. FY2023 cost against income, the loss, and the captive broker reference.
9. WHAT CENTRALISATION TOUCHES. The 9 by 6 grid coloured direct, adjacent, independent, with the counts.
10. WHAT WILL NOT CENTRALISE. The seven constraints in one slide, VAT included.
11. THE SIZE OF THE PRIZE. Low, base, high by component, with the precedent range beside it.
12. WHAT IT COSTS AND HOW LONG. Cost to achieve by lever mix from the precedents; three-year shape.
13. WHAT WE NEED FROM MANAGEMENT. The ten items, with the first three starred.
14. DECISIONS AND NEXT 90 DAYS.
15. Appendix: assumptions register and sources.

Charts in the deck are the same images as in the document. Numbers on slides match the document to the rand.

## Checks before delivery

1. Every figure in both outputs traces to the workbook. Run a script that extracts every number from the document and the deck and matches it to a cell on the Gap sizing, AFS cost base, Benchmark or Normalisation tabs or to a data_id; list any that do not match and fix them.
2. The executive summary and slide 2 say the same thing in the same numbers.
3. Every table and chart carries a source line.
4. Search both files for em dashes, Oxford commas and the banned words, and remove them.
5. Render both files to PDF and look at every page for overflow, orphaned headings and unreadable tables.
6. Commit both files to the outputs folder with the Word and PowerPoint originals; do not commit the rendering scratch files.

## What not to do

Do not re-run the peer research or change the peer set. Do not change any assumption without saying so in the assumptions register. Do not present the benchmark gap as a target or the bank fee as a saving. Do not fold Kenya or the sold entities back into the base. Do not quote the 40 percent cost-to-income ratio as an expense ratio. Do not write the client's name as anything other than Absa Financial Services or AFS.
