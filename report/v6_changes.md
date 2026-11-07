# Draft v6: smoothed lines and rounded corners

7 November 2026. Draft v5 with two changes to the figures. The text is identical to v5.

- **Smoothed lines.** Every line graph (Figures ES.2, 1.1, 1.4, 2.1, 3.1 and 5.2, and the trend lines in the Figure 5.3 scorecard) now draws a monotone cubic curve in place of straight segments. The curve passes through every data point and never rises above or dips below the values either side of it, so the smoothing adds no false peaks or troughs: the FY20/21 low in Figure 1.1 stays at its printed value.
- **Rounded corners.** Bars, stacked columns (rounded at the outer corners only, so segments still meet cleanly), Gantt cells and phase bands, legend swatches, callout boxes and the hypothesis-tree boxes now take a corner radius of 8 units on the 1,600-unit chart width (about 0.8mm on the page), capped at a third of a shape's short side. The governance, results-chain and scorecard diagrams were already rounded.

Word tables, the key-message callouts above tables and the summary boxes stay square: Word cannot round the corners of a table or a shaded paragraph.

Checks: 203 pages; no text change against v5; contents map all 185 entries; 635 footnotes intact; every table row renders; DRAFT FOR DISCUSSION on every page; `qa_structure.py` passes with zero issues.
