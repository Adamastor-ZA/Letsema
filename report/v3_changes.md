# Draft v3: figure titles and footnotes

7 November 2026. Two presentation changes to draft v2, at Michael's request. The wording and figures of the report are otherwise unchanged from v2; `change_log.md` and `qa_report.md` remain the record of the red-team pass.

## 1. Figure titles and callouts

Every figure now has a title of three to six words. Fifteen of the 21 figures (the data charts) carry the key message in a callout drawn on the chart: a shaded box with a teal rule, placed in space the data leaves free. Two charts with no free space (Figure 2.3, route loads, and Figure 4.1, the Gantt) carry the callout in a strip above the plot. The hypothesis tree, the governance diagram, the results chain and the scorecard layout take a title only, since their message is the diagram itself.

| Figure | Title | Callout |
| --- | --- | --- |
| ES.1 | The updated hypothesis tree | None |
| ES.2 | Arrivals paths to 2035 | Only the accelerated path clears 2.5m by 2035; the base path crosses the seat line before 2031. |
| 1.1 | Airport arrivals, FY15/16 to FY25/26 | Arrivals passed the pre-pandemic peak in FY23/24 and reached 1.57m in FY25/26. |
| 1.2 | Overseas arrivals by market, 2025 | Five markets supply 63% of overseas arrivals; the UK, Germany and the USA alone supply 52%. |
| 1.3 | Spend per visitor by market, 2024 | The USA spends R32,900 a visit, 3.9 times Zimbabwe's R8,500. |
| 1.4 | Base case against the seat line | The base case crosses the model's 1.8m seat line in 2030, before runway relief in about 2033. |
| 2.1 | Growth scenarios to 2035 | The base case crosses the seat line in 2030; only the accelerated case reaches 2.5m by 2035. |
| 2.2 | Base-case growth by market group | Hub and acceleration markets supply 382,402 of the 676,949 arrivals the base case adds. |
| 2.3 | Route load factors to November 2025 | Eleven of 27 routes ran above 80% load in the year to November 2025, and sixteen at 75% or more. |
| 2.4 | International seats by month, 2025 | December carries 10.8% of the year's international seats; June carries 6.4%. |
| 2.5 | Comparator growth, 2023 to 2024 | Chile and Singapore grew two to four times the world's 11%; Kenya, Valencia and New Zealand slightly faster. |
| 2.6 | Themes raised by stakeholder organisations | Industry-government collaboration and data sharing each drew 15 of the 16 organisations. |
| 2.7 | Readiness and accessibility by district | Both scores fall with each step away from the Cape Metro. |
| 2.8 | Binding constraints in 20 communities | Organisation binds in 11 of the 20 communities; distance binds in none. |
| 3.1 | Meetings, seats and visitors by month | Meetings peak from September to November, while seats and visitors climb out of the winter trough. |
| 4.1 | Initiative timeline, 2027 to 2035 | Three initiatives start in implementation in 2027, eleven by 2028 and all eighteen by 2029. |
| 4.2 | Initiatives by main funding source | Wesgro's operating budget is the main source for 13 initiatives, and private capital for the four capital-heavy ones. |
| 4.3 | Delivery governance structure | None |
| 5.1 | Results chain for the plan | None |
| 5.2 | Arrivals paths and milestones to 2035 | Only the accelerated path clears 2.5m by 2035; the base path crosses the seat line before 2031. |
| 5.3 | Quarterly scorecard layout | None |

Each callout restates the v2 caption's message in shorter form; no new figure is introduced. Source lines under the figures are unchanged. Table titles are unchanged.

## 2. Citations as footnotes

All 635 citations in the body text are now numbered footnotes, in one sequence through the report. The citation leaves the sentence and its reference mark follows the punctuation that closed it. Short forms are written out in full in the footnote: "(p22)" becomes "Demand-Side Analysis, Jun 2026, p22", and "("Seasonality")" becomes "MIDAS Aviation Market Assessment, Mar 2026, "Seasonality"", taken from the last study document cited in the same section. Public sources never anchor a short form.

What stays inline: cross-references such as (section 4.3), (focus area 7), (I6) or (Table A.21); data notes such as (computed) or (Census 2011); open items in square brackets, including any citation inside one; and the source lines under tables and figures, and table cells, which already carry their sources. The sentence in section 1.5 that describes the citation form now says citations sit in footnotes.

The content modules keep the citations in their inline form, so the source of record does not change; the conversion runs in the renderer (`build/helpers.js`, `citeSplit`).

## Checks

- 635 footnotes defined and 635 referenced, each once; none empty.
- No citation-like parenthesis left in any body, lead, note, list, box or quote paragraph.
- All 21 figure titles are three to six words.
- Every table row renders (row check on the PDF text).
- `qa_structure.py` passes with zero issues; all twenty toplines still match the executive summary.
- Pages: 201 (v2: 193). Footnotes add about eight pages.
