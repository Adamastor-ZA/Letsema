# Draft v7: fewer tables

7 November 2026. Groups 1 to 4 of the table review, at Michael's request. Group 5 is not applied. Every figure, open item and source in a converted table is kept, and the sources now sit in footnotes.

| | v6 | v7 |
| --- | --- | --- |
| Numbered tables | 112 | 72 |
| In the body | 79 | 45 |
| In the appendices | 33 | 27 |
| Footnotes | 635 | 693 |
| Pages | 203 | 195 |

Table numbers below are the v6 numbers.

## 1. Deleted: already said elsewhere (10 tables)

- **The six Chapter 2 "findings for the tree" tables** (2.2, 2.4, 2.7, 2.10, 2.15 and 2.19). Each repeated the numbered findings above it. All 168 figures in them appear in the section's prose or its other tables.
- **The three Chapter 3 pillar overviews** (3.1, 3.8 and 3.15). They repeated ES.2 to ES.4 and the traceability table in Appendix A2. One paragraph each replaces them.
- **Stakeholder priority areas** (2.8). Appendix A6 holds the same list with its lines of enquiry, and the section now says so.

## 2. Narrative in the body (21 tables)

- **Executive summary:** ES.1 how the tree changed, ES.5 the first-24-month actions and ES.7 the main risks. The full versions stay in the tables now numbered 1.4, 4.3 and 4.5.
- **Chapter 1:** 1.1 the headline ambitions, 1.5 the system by tier, 1.8 the chapter map and 1.9 the disposition labels. Table 1.7, the deliverables, folds into the documents table in A9 as a new column, "Version in hand and SLA clauses". Section 1.4 now names the Chapter 2 section that summarises each document.
- **Chapter 2:** 2.3 carrier launches, 2.6 comparator lessons, 2.9 the attributed insights, 2.13 cruise ports, 2.14 remaining gaps, 2.16 inclusion cases and 2.17 archetypes.
- **Chapters 3 to 5:** 3.24 growth paths, 3.25 what moves in each phase, 4.1 levels of the plan, 5.10 the reporting calendar, 5.11 evaluation questions and 5.12 the toolkit files.

## 3. Merged (3 fewer tables)

- The three results-chain tables (5.1 to 5.3) are now one, "Results chain by initiative" (Table 5.1). Its key message joins the three pillar messages.
- The funding columns of Table 4.5 move into "The eighteen initiatives" (now Table 4.1) as "Main funding" and "Supporting funding". Thirteen initiatives draw mainly on Wesgro's operating budget and four on private capital, as before. Section 4.6 now points to Table 4.1.

## 4. Narrative in the appendices (6 tables)

A.9 model printouts and limits, A.13 comparator system types, A.16 readiness index weights, A.24 community share of spend, A.25 inclusion cases and lessons, and A.27 the later-phase engagement list. The other appendix tables stay as reference tables.

## Other edits

- Nine sentences that introduced or relied on a removed table now introduce the narrative or say where the content sits.
- Five cross-references renumbered: (Table A.21) to (Table A.18), (Table 4.5) to (Table 4.1), Table 5.9 to 5.7, "Tables 1.4, 2.11 and A.20" to "1.3, 2.3 and A.17", and the source line of Figure 4.2 now names Table 4.1.
- Fourteen long sentences split, in the new narrative and the paragraphs around it.
- Column widths set for the two tables that gained columns, so no header breaks mid-word.
- The cover and document control now read version 7. Versions 5 and 6 still said version 4. The version now follows the output file name.

62 of the 72 remaining tables have new numbers. The map from v6 to v7 numbers is in `build/redteam/applied_v7.json` under `numbers_after`.

## Group 5, not applied

The 20 Chapter 3 evidence tables (now 3.1 to 3.20) and the 20 action grids stay as they are. Turning them into prose would take the body to 25 tables, at the cost of the at-a-glance audit layout.

## Checks

- **Figures kept:** every number in each of the 28 tables turned into narrative, folded or merged appears in its replacement text. The funding merge keeps the counts of 13 and 4.
- **Deletions held elsewhere:** all 168 figures in the six Chapter 2 recaps appear in their sections. Every disposition, initiative and figure in the three pillar overviews appears in the executive-summary pillar tables or the Chapter 3 entries. Table 2.8 gave one of the four questions for each of eight areas; A6 gives all four.
- **Nothing else changed:** `diff_v6_v7.py` aligns the v6 and v7 content block by block. All 41 removed blocks are logged tables, and the 64 added blocks are the 63 new paragraphs and the merged table. Thirteen paragraphs match their v7 text exactly once the logged edits are applied. The three tables kept with changes differ only in their logged edits: the added columns, the extended message and source lines, and one renumbered cross-reference. Unexplained changes: 0.
- **Repeatable:** `apply_v7.py` run on the v6 content gives the v7 content exactly.
- **Cross-references:** every "Table X.Y" in v7 points to the same table as in v6, except the two that now point to Table 4.1. Every "table below" or "table above" has a table next to it.
- **Build:** contents 145 of 145 entries mapped; 693 footnotes defined and referenced once each; no citation-like parentheses left in prose; all 72 table titles and 21 figure titles are three to six words; every table row renders; `qa_structure.py` passes with zero issues; DRAFT FOR DISCUSSION on all 195 pages.

## Open points

The open items in the converted tables are carried into the narrative in square brackets. Examples are the deck page reference for the disposition labels and the SLA clause numbers, which are still to be checked against the signed Annexure B.
