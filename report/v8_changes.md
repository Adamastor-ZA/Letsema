# Draft v8: a story up front, a discussion in Chapter 2

8 November 2026. Three changes at Michael's request: the executive summary told as a story; section 1.1 rid of its data reconciliation; and Chapter 2 rebuilt as a discussion in four parts, with the interim deliverables moved out of the text and into the footnotes. The rest of the report is unchanged, apart from the knock-on edits listed below.

| | v7 | v8 |
| --- | --- | --- |
| Pages | 195 | 194 |
| Executive summary | 10 pages | 11 pages |
| Chapter 1 | 21 pages | 19 pages |
| Chapter 2 | 26 pages, six sections | 25 pages, four parts |
| Footnotes | 693 | 681 |
| Tables and figures | 72 and 21 | 72 and 21 |

## 1. Executive summary

The summary now reads as one argument, from where the province stands to what the Board decides. It opens with no heading, on the record 1.57 million arrivals at Cape Town International and an airport that is now full at the peak. The headings carry the story:

1. The province earns a premium from a narrow base
2. The limits are physical and institutional
3. What 2.5 million arrivals would take
4. The strategy makes three shifts
5. Twenty focus areas at a glance
6. Seats and bookings move first
7. How the Board will track progress
8. What could knock it off course
9. What the Board is asked to decide

The three pillar tables, the hypothesis tree, the arrivals paths chart and the impact indicators table are carried over unchanged. The pillar tables still hold the twenty Chapter 3 findings word for word. The Board's decision lists are also unchanged. The entry-by-entry account of how the tree changed is now one sentence pointing to section 1.4, where Table 1.4 holds it. The two figures now appear in story order, so the arrivals paths chart is Figure ES.1 and the tree Figure ES.2.

The rewrite also corrects five points that a cold read found in v7:
- **Risks:** the v7 summary said three risks were rated medium likelihood and high impact, and named climate as the only high-likelihood, medium-impact risk. The section 4.8 register rates six of the first kind and two of the second; the summary now says so.
- **Base path:** it assumes Wesgro holds its current effort, as sections 1.1, 1.3 and 5.3 say. It does not need a bigger programme.
- **Recovery:** it is complete on the airport count. A footnote gives South African Tourism's provincial count, which is still below 2019.
- **Growth for Jobs:** the province's 3 million target is now named, with its open item.
- **Spend:** a paragraph under the impact table gives the airport baseline and explains why R40.6bn is not measured from R25.9bn. It carries section 5.3's rebase open item word for word.

## 2. Section 1.1, Mandate and objective

The section now runs straight through the mandate, the objective, the four ambitions and how each is carried, Wesgro's outcome metrics and the alignment with Growth for Jobs and the FY26 to FY30 plan. The headings state claims, for example "Of four ambitions, only arrivals has a target the evidence supports".

The data reconciliation sits in one closing paragraph, "How the report counts arrivals". It names the four kinds of arrivals figure, sets out the three rules the report follows and keeps both open items on the model's basis. The detail moved to a new closing subsection of Appendix A2, "Arrivals figures and their bases". That covers the eight figures in circulation (the table formerly numbered 1.1, now A.9), the ambitions that do not reconcile, the model base against South African Tourism's count, and the FY25/26 caution. Four of Wesgro's six outcome metrics are not tourism metrics, so they moved to a footnote.

## 3. Chapter 2, Analysis and insights

The chapter was "Analysis summaries": six sections, one per deliverable, each with "What was asked", "What was done" and "Findings that survived into the tree". It is now a discussion in four parts, each an argument under headings that state its findings:

- **2.1 Global benchmarks and their lessons.** All the comparator evidence now sits here: the six destinations, the eight peer airports and the community-inclusion cases. Each lesson closes on the change it asks of the Western Cape.
- **2.2 Demand-side factors.** Markets, spend, seasonality, the growth paths, segments, India and China hub flows, booking platforms, Africa and business events. This part feeds Pillar 1.
- **2.3 Supply-side factors.** The seat line, full routes, hubs, winter seats and fares, the runway, cruise, the flagships, readiness by district, beds and booking, and where committed capital goes. This part feeds Pillar 2.
- **2.4 The enabling environment.** National levers, funding and mandates, climate costs, collaboration and data, the missing jobs count and community inclusion. This part feeds Pillar 3.

A short introduction sets out the four parts. Stakeholder evidence no longer has a section of its own. It runs through all four parts, attributed to the organisations that gave it, and the paraphrase-approval open item sits in the introduction. Each part closes with a box, "What this means for the strategy", which carries every focus-area line of the v7 boxes with the same verbs.

No interim deliverable is named in the text. Each is cited in the footnotes, and notes about a source (model bases, the comparator screen, engagement phases) ride in those footnotes too. The SLA clause sentences left the chapter; the documents table in A9 already lists the clauses, and a note under it now carries the open item on clause wording. Versioning detail already held in Appendices A2, A3 and A6 stays there. Every figure and table is carried over unchanged.

## Knock-on edits

- **Chapter 1:** sections 1.4 and 1.5 now describe the new Chapter 2 and the new summary. Section 1.3 now says Cape Town's 79% load factor is joint highest with Lanseria, as the evidence says.
- **Cross-references into Chapter 2** point to the new parts, in Appendices A3 and A5, focus area 13 and the section 5.3 baselines table. The Chapter 2 column of the traceability table in Appendix A1, and `traceability.csv`, map each focus area to the parts whose boxes name it.
- **Table renumbering:** moving Table 1.1 to Appendix A2 renumbers later tables. The open item in section 1.4 that names Tables 1.3, 2.3 and A.17 now reads 1.2, 2.3 and A.18, which are the same tables. This is the one edit made inside an open item.
- **Table message:** the key message of "Touring route readiness" now matches its table. The Winelands and Garden Route routes fall short on safety, not on bookability or accommodation. The message of "Four traveller segments" no longer mentions "the deck".
- **Chapter title:** set in the build, and in the QA script that looks it up.

## How it was done and checked

Agents drafted each piece from plans that a second agent had critiqued. Each draft was then adversarially reviewed for fidelity and voice, fixed, and read cold as the rendered PDF.

- **Drafts:** `redteam/check_v8_draft.py` passes all six with zero errors. It checks the house style, sentences under 36 words, and that no deliverable is named in the text. It also checks that citations are in full form, that every figure and open item of the absorbed v7 text survives, and that no number is invented. Across Chapter 2 as a whole, every v7 block is absorbed or relocated, and every figure and table appears exactly once.
- **Rendered text:** no deliverable is named in the body of the summary, section 1.1 or Chapter 2, apart from one open item, which stays word for word.
- **Nothing else changed:** `redteam/diff_v7_v8.py` finds 42 modules unchanged, 10 changed only by logged edits and no unexplained differences. All 16 distinct open items from the old summary, section 1.1 and Chapter 2 survive word for word.
- **Build:** 146 of 146 contents entries mapped. 681 footnotes, each defined and referenced once. All 72 table titles and 21 figure titles are three to six words, and every table row renders. `qa_structure.py` passes with zero issues, including all 20 toplines word for word in the summary. DRAFT FOR DISCUSSION is on all 194 pages.
- **Repeatable:** `redteam/apply_v8.py` rebuilds v8 from the v7 content and the drafts in `redteam/v8/drafts`. The plans are in `redteam/v8/outlines`.

## Open points

- Sections 1.2 to 1.5 still name the deliverables in their text (35 places, mostly in 1.4, which describes the approach). The same footnote treatment could apply there if you want Chapter 1 to read the same way.
- Chapter 2 is about the same length in words as v7 (about 9,500 with citations). The cut from method and versioning was spent on the argument each part now makes.
- The Chapter 3 topline for focus area 8 gives Cape Town's cruise berth as "about 40% of its season capacity", beside 83 calls against a capacity of 150 or more. The source prints the 40% without stating its basis, and 83 of 150 is 55%, so a reader may query it. Chapter 2 now gives the call count in the text and notes the 40% and its missing basis in a footnote. The topline is unchanged; the basis is worth confirming with the source before publication.
