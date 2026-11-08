# Draft v10: no Board decisions in the summary; a research project, not a strategy

8 November 2026. Two changes at Michael's request.

| | v9 | v10 |
| --- | --- | --- |
| Pages | 210 | 210 |
| Executive summary | 11 pages | 10 pages |
| Footnotes | 845 | 845 |
| Contents entries | 146 | 145 |

## 1. The Board decisions leave the executive summary

The section "What the Board is asked to decide" is gone: its heading, its introduction, the two lead-in lines, the two numbered lists and the closing paragraph on Gate 1. The summary now ends on the main risks, followed by the note on open items.

Two loose ends are tied off:
- **Stop list:** the summary's risk paragraph mentions a stop list, which only the deleted decisions explained. Section 4.6 now explains it: Wesgro Finance and DEDAT agree before Gate 1 what Wesgro deprioritises to fund the initiatives. The summary points there.
- **Rand band open item:** the item "[Open item: Wesgro Finance to give an indicative rand band for the first 24 months.]" sat inside the deleted decisions. It now sits in section 4.6.

The risk register's pointer "(Decision 3)" now reads "(section 4.6)". Section 1.5 no longer says the summary ends with the Board's decisions.

## 2. The work is a research project that develops an action plan

- **Subtitle:** the report's subtitle is now "An Action Plan for the Western Cape to 2035", on the cover, the running header and the document control table. The cover still reads "Final research report" above it.
- **Text:** every reference to the work as a strategy is reworded, in 41 places. The new wording depends on context: the research, this report, the study, the recommendations, the plan or the action plan. For example:
  - the summary heading is now "The action plan makes three shifts";
  - section 1.1 opens "Wesgro commissioned research and an action plan to 'double international tourist arrivals...'";
  - "This strategy plans on about 2033" became "The plan's phasing assumes about 2033";
  - section 1.4's final phase "consolidated the research into this report".
- **Chapter 2 boxes:** the four boxes are now titled "What this means for the focus areas".
- **Section 4.1:** its heading is now "From focus areas to initiatives".

What stays, because it does not describe this work:
- other bodies' strategies: the Growth for Jobs Strategy, Wesgro's own strategy statements and five-year strategy, and the comparators' hub, brand and gateway strategies;
- the event-calendar and route strategies the plan proposes;
- the growth model's "Strategic growth" market group;
- focus area 15's title, "Crowd in capital with targeted investment strategies";
- the study objective quoted from the inception report ("an evidence-based tourism strategy..."), which stays word for word. The next sentence now says what the research does: it builds the evidence the objective calls for, and Chapters 3 and 4 turn it into recommendations and an action plan.

## Checks

- **Remaining uses:** `redteam/apply_v10.py` finds no reference to the work as a strategy, and no decision wording left in the summary. All 63 uses of "strateg-" left in the rendered text were read one by one; each is another body's strategy, a market-group name, a focus-area title or a quotation.
- **Nothing else changed:** comparing v10 with v9 module by module, 19 modules changed, and every changed block is named by an edit in `redteam/v10/edits.json`.
- **Build:** 145 of 145 contents entries mapped; 845 footnotes, each defined and referenced once; every table row renders. `qa_structure.py` passes with zero issues, with all 20 findings word for word in the summary. DRAFT FOR DISCUSSION is on all 210 pages.
- **Repeatable:** `redteam/apply_v10.py` rebuilds v10 from the v9 content and the edit list. A drafter, an adversarial reviewer and a fixer prepared the edits.

## Open point

The new subtitle is my wording. If you prefer another, such as "Research and Action Plan for the Western Cape to 2035", it is one line in `build/report.js` and two in `build/front_matter.js`.
