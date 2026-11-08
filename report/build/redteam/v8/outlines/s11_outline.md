# Section 1.1 v8: outline

Module: `content/ch1/01_mandate.json` (id 1.1, title "Mandate and objective"). Draft goes to `redteam/v8/drafts/s11.json`, which `apply_v8.py` maps to `ch1/01_mandate.json`. Test it with `python3 check_v8_draft.py v8/drafts/s11.json --strict-callouts`. The checker only warns on call-outs in `ch1/`, so pass the flag to hold 1.1 to the exec and Chapter 2 standard.

Michael's note: 1.1 "spends far too much time on data reconciliation and versioning. Bury this at the end of the section in a short paragraph or two."

Shape: the mandate, the objective, the four ambitions and how the strategy carries each, Wesgro's outcome metrics and alignment come first, in plain statements. Reconciliation and versioning drop out of those parts. They go into a two-paragraph closing note, into footnote notes or into Appendix A2. The table "Arrivals figures in circulation" moves to a new closing subsection of A2.

Budget: 1,300 to 1,800 words of prose, counted as the checker counts them (citations and open items included). v7 is 2,106 words of prose plus the table. The indicative wording below was run through the checker with the sources and relocations set out in section 4. After the red-team revision (7 Nov) it gives 0 errors, 1,771 words, a median sentence of 16 words and a longest sentence of 30 (the quoted first strategy statement). About 1,440 words remain once citations and open items are taken out, so that is what the reader sees. The closing note is about 255 of them, under a fifth of the section. Do not add to it. If the draft grows, cut the closing note's footnote notes first, then the base-case assumption sentence in the arrivals paragraph.

Expected checker warnings, both acceptable: one "possible Oxford comma" (the mission is quoted verbatim: "strengthen competitiveness, and create jobs") and up to two sentences of 29 to 35 words.

## 1. Rules the drafter must hold (specific to 1.1)

- **No deliverable named in the text.** "The Diagnostic", "the demand model", "the June deck", "the inception report" and "the SLA" are all out of the running text. The source lives in the citation and any versioning detail goes in a footnote note: a lowercase note of four or more words after a semicolon. "The growth model" and "the model" are the analysis, not a deliverable, and may stay.
- **Full citations only.** v7 [13], [16], [23] and [24] use short forms such as `(p18)`, `(p19)` and `(p25)`, which fail the checker. Write every one in full.
- **The SLA citation.** `(SLA Annexure B, clause 1.1.14.2)` fails the checker as an undated citation. Carry the clause as a note on the Inception Report citation: `(Inception Report, Nov 2025, p22; the requirement itself sits in SLA Annexure B, clause 1.1.14.2)`.
- **Quotes that close a sentence.** Put the full stop outside the closing quote mark (`services".`). The checker's splitter does not break after `."`, so a quote that closes with `."` merges two sentences into one. In the trial this produced a false 54-word error.
- **The objective is a 43-word quote.** Split it at "by 2035" across two sentences ("It continues "through ..."") so that neither runs past 35 words. It is still quoted in full and verbatim.
- **The fourth strategy statement** opens with "Unlock" (a banned word that the checker flags even inside quotes) and carries a spaced hyphen. Paraphrase its markets and quote only its closing clause.
- **Stale cross-reference.** v7 [18] points to "section 2.6", and `apply_v8.py` asserts that no module cites sections 2.5 to 2.9. Point it to section 2.4 instead. Community inclusion is focus area 13 under Pillar 3, which 2.4 feeds. Confirm against the `ch2_4` draft that the inclusion evidence lands there. Because "2.6" then appears nowhere, list [18] under `relocations` (kept in place) rather than `sources`, and check its open item by hand (section 4).
- **Nine open items** survive word for word with their content (section 5). Three of them live in the closing note.

## 2. Headings and paragraphs

Indicative wording is given for every paragraph. The drafter may tighten it but should keep the beats, the numbers and the open items.

### h2 "1.1 Mandate and objective"

**[lead]** Beat: the ask, then the evidence-based goal, with nothing on reconciliation.

> Wesgro commissioned a strategy to "double international tourist arrivals to the Western Cape by 2035" (Inception Report, Nov 2025, p4). The evidence reframes that goal as growth to 2.5 million arrivals, paced by gateway capacity in the summer peak and by demand in the green season.

v7: ch1/01 [1], split into two sentences (v7 ran it as one 42-word sentence). "Reframes that goal", not "reframes it": after the split, "it" could read as the strategy.

### h3 "Wesgro's mandate" (about 215 words, two paragraphs)

**P1. Mission and vision.** Topic sentence on the agency's wider brief. The mission and vision are quoted, followed by the two points that shape the strategy: growth is a means to jobs, and Wesgro acts through partners.

> Wesgro promotes tourism, trade and investment for Cape Town and the Western Cape, so the tourism goal sits inside a wider economic brief. Its mission is to work "together with partners, drive inclusive and sustainable economic growth, strengthen competitiveness, and create jobs in Cape Town and the Western Cape". Its vision is to "be a leading regional tourism, trade and investment promotion agency" (Inception Report, Nov 2025, p5). Two points in the mission shape this strategy. Growth is a means to jobs, and Wesgro acts through partners rather than holding the levers itself.

v7: ch1/01 [3], [4]. The two p5 citations merge into one footnote.

**P2. The four strategy statements that bear on the study, in prose.** The eight-item bullet list is replaced. Statements one, six and seven are quoted, and the fourth is paraphrased (see the rules above). The paragraph closes with the link to the pillars.

> Four of Wesgro's eight strategy statements bear directly on this study (Inception Report, Nov 2025, p5). The first sets the destination proposition: "Ensure that Cape Town and the Western Cape is top of mind as a leading business and tourism destination with premium products and services". The fourth names new markets and buyers in China, ASEAN, India, Brazil and the Middle East, "while maintaining a continued focus on established markets". The sixth is to "Track and address systemic challenges influencing economic competitiveness". The seventh is to "Provide economic data, insights & analytics for the Western Cape". The first and fourth frame Pillar 1; the sixth and seventh give Wesgro standing on the constraints and data gaps that Pillars 2 and 3 address.

v7: ch1/01 [5], [6], [7]. **Cut:** the bullet list itself. Also cut are the four statements that do not bear on the study: investment priority areas, reinvestment by existing businesses, catalytic delivery models and digital transformation. So is v7's "quoted here as printed" line.

### h3 "The study objective and its four ambitions" (about 525 words, seven paragraphs)

This heading merges v7's "The study objective and the original ambitions" with the four run-in ambition paragraphs.

**P3. The objective, quoted in full.** It fixes the three pillars, and a pivot names the one term that did not survive.

> The objective, set in November 2025, is "To develop an evidence-based tourism strategy that will double international tourist arrivals to the Western Cape by 2035". It continues "through a holistic approach that drives demand, strengthens supply and enables inclusive, sustainable and geographically dispersed growth aligned with WESGRO's strategic priorities" (Inception Report, Nov 2025, p4). The objective fixes the three pillars the report keeps throughout: demand, supply and enablement. Of its terms, only the doubling did not survive the evidence.

v7: ch1/01 [9]. The last sentence is new and draws on 1.5 [10] and [17].

**P4. The four ambitions, plainly stated.**

> Four headline ambitions sat under the objective: 2.8 million international visitors, 300,000 tourism-linked jobs, 10,000 SMMEs onboarded and twice the airlift and cruise volumes (Inception Report, Nov 2025, p4). The strategy keeps all four, but the evidence changed how each is carried.

v7: ch1/01 [10], first sentence. **Moved to the closing note:** the rest of [10] ("None carried a base year ..."; the 5.7 million and R54.7 billion restatement) and all of [11] (the 1.44 million baseline and the 2.88 million comparison).

**P5. Arrivals, from the growth model.** The model's three end points, what the accelerated case needs, 2.5 million as that case rounded, and the date it was tabled with Wesgro. The 2024-base version goes in a footnote note.

> **Arrivals.** The growth model tested the doubling and supports 2.2 million to 2.5 million by 2035. From 1,498,829 arrivals in 2025, its base case reaches 2,175,778 by 2035 and its accelerated case 2,516,282, above a conservative floor of 1,822,634 (Market Assessment Report, May 2026, p19; the June version prints the same 2035 points from a 2024 base). The base case holds Wesgro's effort at 2025 intensity. The accelerated case needs confirmed direct routes to India and China, above-baseline activation and more hub capacity into Cape Town; without the routes, volume reverts to base (Market Assessment Report, May 2026, p18, p19). Growth to 2.5 million is that case rounded, and it is the goal the report carries. The reframing was tabled with Wesgro on 14 October 2026 [Summary of Findings, 14 Oct 2026, page to be confirmed against the final deck].

v7: ch1/01 [12], [13], [15] (first sentence and open item) and [16] (the arrivals run-in). **Footnote note:** the June 2024 base. **Cut:** the base case's "selective frequency gains on existing routes and continued hub expansion" and "the model's own footnote is blunt". Both are held in A2's table "Growth model scenario definitions". **Moved to the closing note:** [16]'s 1.44m baseline, the model base as a second baseline and the 5.7 million recorded as superseded.

**P6. Arrivals, the seat line.** The summative closer for arrivals: a supply programme before a marketing programme.

> Even the base case runs into the model's seat line. The model draws inbound capacity at 1.8 million seats, and the base case first passes that line at the 2030 year point, at 1,802,929 arrivals (Market Assessment Report, May 2026, p20). Growth to 2.5 million is therefore a supply programme before it is a marketing programme, and every chapter of this report returns to that point.

v7: ch1/01 [14], unchanged in substance.

**P7. Jobs, carried to the labour analysis.**

> **Jobs.** The ambition was 300,000 tourism-linked jobs, yet the evidence holds no Western Cape tourism employment figure (section 2.4). The strategy carries jobs to Chapter 5 without a baseline. A labour analysis, which Wesgro and DEDAT should commission in 2027, will set one (focus area 20, flagged).

v7: ch1/01 [17]. "No deliverable carries" becomes "the evidence holds no". The year 2027 comes from ch3/38 [11], which says Wesgro and DEDAT "should commission" the analysis: it is a recommendation, so do not write "commissioned in 2027" as if it had happened. The cross-reference to 2.4 follows the Chapter 2 outline, where 2.4 holds "Nobody can yet count tourism jobs".

**P8. SMMEs, carried as community inclusion measured in spend.**

> **SMMEs.** The ambition was 10,000 SMMEs onboarded, with no baseline or definition printed [Wesgro to confirm the baseline count and definition of SMMEs onboarded]. The strategy carries it as community inclusion, measured in visitor spend reaching priority communities rather than a count of firms (section 2.4 and Chapter 5).

v7: ch1/01 [18]. The only change is the cross-reference, from section 2.6 to section 2.4. If the `ch2_4` draft does not hold the inclusion evidence, use "(focus area 13 and Chapter 5)".

**P9. Airlift and cruise, carried as seats, routes and calls.** The summative closer for all four ambitions.

> **Airlift and cruise.** The ambition was twice the airlift and cruise volumes. Airlift is carried as the seats and routes needed to lift the model's 1.8 million seat line (Market Assessment Report, May 2026, p20). Cruise is carried as calls and ports (section 3.2.1), from a base of 79 vessels in the 2024/25 season (Current State Diagnostic, Dec 2025, p37) [Cruise Cape Town to confirm the call target and its definition]. Of the four ambitions, only arrivals carries a target the evidence supports today. The other three go forward with their baselines still to be fixed.

v7: ch1/01 [19], plus [15]'s second sentence reworked as the closer.

### h3 "Wesgro's outcome metrics" (about 240 words, three paragraphs)

**P10. The six metrics in prose.** The six-item bullet list goes. The two tourism metrics come first, the other four follow in two sentences, and the period open item comes last.

> Wesgro measures itself against six strategic outcomes, each with one metric (Inception Report, Nov 2025, p6). Two are tourism metrics: 800,000 to 1 million new international tourist arrivals and 161 business event bids secured, with an estimated economic value of R4.5 billion. Three more cover a 120 million audience reached, R30 billion of new investment and R9.1 billion of new export declarations. The sixth asks for a future-fit and trusted Wesgro, with a clean audit, satisfied clients and low culture entropy. None of the six carries a period [Wesgro to confirm the period over which the six outcome metrics are measured].

v7: ch1/01 [21], [22]. **Cut:** the bullet form. The outcome names are compressed and every number is kept.

**P11. The arrivals metric against the two paths.**

> The period decides how the arrivals metric compares with the growth case. Over ten years, 800,000 to 1 million new arrivals sits between the two paths, which add 676,949 and 1,017,453 from 2025 to 2035 (Market Assessment Report, May 2026, p19). Yet over the five years to 2030 it sits well above the base case, which adds about 304,000 by then (Market Assessment Report, May 2026, p20; computed).

v7: ch1/01 [23]. The computation (1,802,929 against 1,498,829) moves into `computed`, since both figures are already in P5 and P6. "Yet" marks the pivot: the same metric reads as on track or as a stretch depending on the period.

**P12. The business-events metric and the green season.**

> The business-events metric ties to the green-season case. International association meetings in Cape Town rose from 33 in 2022 to 58 in 2024 and are "primarily hosted between May and November" (Market Assessment Report, May 2026, p26). That window takes in five of the six green-season months, April to September (Market Assessment Report, May 2026, p25). Chapter 5 measures the same two things through its arrivals and association-meeting indicators (T1-01 and T2-02).

v7: ch1/01 [24]. **Changed claim:** v7 says "Chapter 5 fixes the period for both metrics and sets them against the growth case on one basis". No Chapter 5 module does that: ch5/02 and ch5/03 carry T1-01 and T2-02 but never mention Wesgro's six metrics or their period. The new last sentence states only what Chapter 5 does.

### h3 "Alignment with provincial strategy" (about 340 words, three paragraphs)

**P13. The requirement and the contract clauses.**

> The study's contract requires this report and its recommendations to align with two documents: the Growth for Jobs Strategy (G4J) and Wesgro's FY26 to FY30 plan (Inception Report, Nov 2025, p22; the requirement itself sits in SLA Annexure B, clause 1.1.14.2). This report is the Final Research Report under clause 1.1.14, and Chapter 5 answers the monitoring and evaluation clauses 1.1.4 and 1.1.10 [clause references to be checked against the signed SLA Annexure B, whose wording is not in hand].

v7: ch1/01 [26]. **Footnote note:** clause 1.1.14.2. **Cut:** "The inception report carries the same instruction". It is now one sentence with one citation.

**P14. G4J: its target, then the gap in method.** How the gap in measure works is left to the closing note.

> The Growth for Jobs Strategy 2023, approved by Cabinet, designates tourism a primary tradable sector for the province (Current State Diagnostic, Dec 2025, p5). Its arrivals target is 3 million international tourist arrivals by 2035 on the South African Tourism basis, built as 2 million in 2019 plus 1 million (Wesgro, presentation to the parliamentary committee, 1 Apr 2026; public source). [G4J 2023 document to be read and the 3 million target confirmed against it.] If the model counts on the same basis, that target sits above both of its paths. The gap is first one of method. G4J adds 1 million to the 2 million of 2019, while the growth model builds up market by market against the seats and routes the gateway can carry. Whether the gap is also one of measure turns on what the model counts, so the 2.5 million cannot be set against the 3 million without conversion.

v7: ch1/01 [27] and [28] (last sentence only). **Cut:** "among the first documents Wesgro supplied to the study" (process detail). **Moved to the closing note:** the rest of [28]: the 1,538,142 SA Tourism count, the 11.1% rise (as a footnote note) and the contrast between the airport series and the SA Tourism series. The new wording also removes a v7 tension. v7 says the 3 million sits above both paths "if the model counts on the SA Tourism basis", then says flatly that the two "count different things". The measure question and the alignment verdict now share one sentence (28 words), so the body spends one sentence, not two, on what the model counts; the detail waits for the closing note.

**P15. The FY26 to FY30 plan and the gate timing.**

> Wesgro's FY26 to FY30 plan is the second test. A Wesgro five-year strategy was supplied to the study, but no plan document is in hand (Inception Report, Nov 2025, p34). Until it is, alignment can be stated only in principle [Wesgro to supply the FY26 to FY30 plan and its tourism targets, so that the Chapter 5 baselines and the Chapter 4 phase gates can be mapped to the plan cycle]. Yet the timing already fits. Chapter 4 sets its first decision gate at the end of 2028, inside the plan period and before the base case crosses the model's seat line.

v7: ch1/01 [29]. "At the level the inception report gives it" becomes "only in principle". ch4/02 [3] puts the end-2028 gate in FY2028/29.

### h3 "A note on the numbers" (two paragraphs, drafted in full below)

v7 blocks absorbed: ch1/01 [10] (second and third sentences), [11], [16] (baseline and superseded clauses), [28] (all but its last sentence), [30] (heading, replaced), [31], [33], [34] and [35]. The table [32] moves to A2.

## 3. The closing note, drafted in full

Both paragraphs pass the checker: 0 errors, no call-outs, no short-form citations, and every number already present in v7. Once citations are taken out they run to 124 and 132 words, or about 151 and 146 with their open items, which print in the text. That is the ceiling: if either grows, cut it back before touching the body. Every footnote note was confirmed to land in the footnote with `helpers.js` `citeSplit`, and nothing spills inline.

**[p]**

> The arrivals figures around this strategy do not reconcile. Neither the 2.8 million ambition of November 2025 nor the 5.7 million arrivals and R54.7 billion of spend stated in December names a series or a base year (Inception Report, Nov 2025, p4; Current State Diagnostic, Dec 2025, p5; the report records the second statement as superseded). Twice the 1.44 million airport arrivals of FY24/25 is 2.88 million, close to the first and far from the second (Current State Diagnostic, Dec 2025, p25; computed). Eight figures now circulate and count four things: ambitions, airport passengers, South African Tourism's tourist arrivals and the model's arrivals, as Appendix A2 sets out. The model's 2025 base of 1,498,829 sits just below South African Tourism's 1,538,142 (Wesgro Research, Western Cape Tourism Performance: Annual 2025; public source; the 2025 count rose 11.1% on the year). Yet its market groups step up from 2024 at the model's own growth rates. The report therefore treats the base as a model value until its basis is confirmed (Market Assessment Report, May 2026, p19; the steps match the growth rates to within 0.2 points, computed from Appendix A2). [Open item: Skift to confirm in writing what the model counts (SA Tourism tourist arrivals, ACSA passengers including returning residents or OAG origin-and-destination flows) and how the Hubs group is built.]

**[p]**

> The report follows three rules; first, airport passenger arrivals at Cape Town International, the province's gateway, are the baseline and tracking series, by fiscal year (Current State Diagnostic, Dec 2025, p26, p41; the source uses Cape Town air arrivals as its provincial proxy). FY24/25, at 1.44 million, is the recovery baseline in section 1.2 and the baseline year in Chapter 5. Second, the model's 2025 base and its 2035 points are the target series. Third, South African Tourism's provincial count is used once, to read across to the G4J target. The FY25/26 actual of 1.57 million shows why the rules matter: it sits above the model's 2025 base and below its 2028 base-case point of 1,673,855 (Market Assessment Report, May 2026, p10, p20). Yet the two differ in measure and period, so the gap is no evidence that the model is cautious. The report quotes them side by side and never adds one to the other [model owner to confirm the series and year basis behind the 2025 base of 1,498,829].

Why paragraph 1 changed from the first trial: the trial wording said the base "sits just below South African Tourism's 1,538,142. The report therefore treats it as a model value". Sitting near a count is no reason to call a figure a model value, so "therefore" did not follow; the reason (each group's 2025 value is its 2024 value grown at the model's own rate) had gone into the footnote. The reason is back in the text in one plain sentence, so "therefore" now follows from it, and the 0.2-point check stays in the note. The trial also packed two sources and three notes into one parenthesis; each source now carries its own. "One caution follows" in paragraph 2 was throat-clearing; the FY25/26 actual now opens its own point. The gateway rationale from v7 [31] returns as a three-word appositive.

The footnotes these produce:
- "Inception Report, Nov 2025, p4; Current State Diagnostic, Dec 2025, p5; the report records the second statement as superseded."
- "Wesgro Research, Western Cape Tourism Performance: Annual 2025, public source; the 2025 count rose 11.1% on the year."
- "Market Assessment Report, May 2026, p19; the steps match the growth rates to within 0.2 points, computed from Appendix A2."
- "Current State Diagnostic, Dec 2025, p26, p41; the source uses Cape Town air arrivals as its provincial proxy."

## 4. The table's new home in Appendix A2, and the draft's bookkeeping

A2 now ends with h3 "Seat line and model limits", whose last paragraph (A2 [27]) says that the airport, SA Tourism, OAG and model series are not reconciled. The new subsection follows it directly. Carry it in `s11.json` as `appendix_blocks`, which `apply_v8.py` appends to the module:

```json
"appendix_blocks": {"module": "appendices/02_a2_demand_model.json", "blocks": [
  {"type": "h3", "text": "Arrivals figures and their bases"},
  {"type": "p", "text": "Eight arrivals figures circulate around this strategy, and they count four things: ambitions, airport passengers, South African Tourism's tourist arrivals and the model's arrivals. The table below fixes each figure and states how the report uses it. It keeps an airport count apart from a provincial tourist count, and an ambition apart from a projection. Section 1.1 sets out the three rules behind the last column."},
  {"type": "ref", "src": ["ch1/01_mandate.json", 32]}
]}
```

The lead-in passes the checker when run as its own draft (0 errors, 0 warnings, 71 words); `check_v8_draft.py` does not read `appendix_blocks`, so run it that way. It now names the four things, in the same words as closing paragraph 1. The paragraph above it in A2 lists four series that include OAG, and without the names a reader would take the table's four to be those. The table travels as a ref with its caption, message line, rows and source line unchanged. The heading is not "Arrivals figures in circulation", so it does not repeat the caption beneath it.

Draft keys, as used in the trial run:

```json
"sources": [["ch1/01_mandate.json", 0], ... every index 0 to 35 except 18 and 32 ...],
"relocations": [
  {"src": ["ch1/01_mandate.json", 32], "to": "Appendix A2, new closing subsection \"Arrivals figures and their bases\" (appendix_blocks)", "reason": "Reference table; Michael asked for the reconciliation to be buried, and the closing note of 1.1 points to it", "carries_all": true},
  {"src": ["ch1/01_mandate.json", 18], "to": "kept in place as the SMMEs paragraph of 1.1; only its cross-reference changes from section 2.6 to section 2.4", "reason": "Chapter 2 now has four sections; listing [18] as a source would require the stale number 2.6"}
]
```

Because [18] is not under `sources`, the checker will not test its open item. Check by hand that "[Wesgro to confirm the baseline count and definition of SMMEs onboarded]" is present.

## 5. Open items: all nine survive word for word

| v7 block | Open item | Lands in |
|---|---|---|
| [15] | [Summary of Findings, 14 Oct 2026, page to be confirmed against the final deck] | P5, the arrivals paragraph |
| [18] | [Wesgro to confirm the baseline count and definition of SMMEs onboarded] | P8, SMMEs |
| [19] | [Cruise Cape Town to confirm the call target and its definition] | P9, airlift and cruise |
| [21] | [Wesgro to confirm the period over which the six outcome metrics are measured] | P10, the metrics |
| [26] | [clause references to be checked against the signed SLA Annexure B, whose wording is not in hand] | P13, the requirement |
| [27] | [G4J 2023 document to be read and the 3 million target confirmed against it.] | P14, G4J |
| [29] | [Wesgro to supply the FY26 to FY30 plan and its tourism targets, so that the Chapter 5 baselines and the Chapter 4 phase gates can be mapped to the plan cycle] | P15, FY26 to FY30 plan |
| [33] | [Open item: Skift to confirm in writing what the model counts (SA Tourism tourist arrivals, ACSA passengers including returning residents or OAG origin-and-destination flows) and how the Hubs group is built.] | Closing note, paragraph 1 |
| [35] | [model owner to confirm the series and year basis behind the 2025 base of 1,498,829] | Closing note, paragraph 2 |

ch5/03 [6] cites "which Skift is to confirm (section 1.1)", and that item stays in 1.1. 1.5 [10] cites "the growth model supports 2.2 million to 2.5 million by 2035 (section 1.1)", which P5 now states in those words.

## 6. v7 block disposition (ch1/01)

| v7 | Type | Fate |
|---|---|---|
| [0] | h2 | Kept |
| [1] | lead | Kept, split into two sentences |
| [2] | h3 | Kept |
| [3], [4] | p | P1, with the citations merged |
| [5] | p | Into P2; "quoted here as printed" cut |
| [6] | bullets | Into P2 as prose; the four non-tourism statements cut; the fourth paraphrased |
| [7] | p | Into P2 |
| [8] | h3 | Renamed "The study objective and its four ambitions" |
| [9] | p | P3, with the quote split over two sentences |
| [10] | p | First sentence into P4; the rest into closing note paragraph 1 |
| [11] | p | Closing note paragraph 1 |
| [12], [13] | p | P5; base-case detail cut (held in A2's scenario table); short citations written in full |
| [14] | p | P6 |
| [15] | p | First sentence and open item into P5; second sentence into the P9 closer |
| [16] | p | Its 2.5 million clause into P5; baselines and "superseded" into the closing note and a footnote note |
| [17] | p | P7; "commissions" kept as a recommendation (2027), cross-reference to 2.4 added |
| [18] | p | P8, cross-reference 2.6 to 2.4 (listed as a relocation, see section 4) |
| [19] | p | P9 |
| [20] | h3 | Kept |
| [21], [22] | p, bullets | P10 as prose; every number kept |
| [23] | p | P11 |
| [24] | p | P12; the unsupported Chapter 5 claim replaced |
| [25] | h3 | Kept |
| [26] | p | P13; SLA clause into a footnote note |
| [27] | p | P14; "among the first documents" cut |
| [28] | p | Last sentence into P14; the rest into closing note paragraph 1 (11.1% as a footnote note) |
| [29] | p | P15 |
| [30] | h3 | Replaced by "A note on the numbers" |
| [31] | p | Closing note paragraph 2 (gateway clause as an appositive, proxy rationale as a footnote note); its opening lines go into the A2 lead-in |
| [32] | table | Moved to A2 (relocation, carries_all, ref in appendix_blocks) |
| [33] | p | Closing note paragraph 1; the step from 2024 stays in the text as the reason for "model value", and the 0.2-point check goes into a footnote note |
| [34] | p | Closing note paragraph 2 (the three rules, now enumerated first, second, third) |
| [35] | p | Closing note paragraph 2 |

## 7. Knock-ons outside this draft (for the orchestrator)

1. **Table numbering.** `helpers.js` numbers tables by position, and the appendix tables run on from A.1 across all nine appendices. With Table 1.1 gone, "District economy, assets and access" becomes Table 1.2. The arrivals table becomes Table A.9 in A2, after A.8 "Base-case spend by group", and every appendix table after it moves on by one: A3's four tables become A.10 to A.13, A4's five become A.14 to A.18 and A5's "Community shortlist criteria" becomes A.19. Two references go stale.
   - **ch2/06 [11] cites "(Table A.18)"** for the 35% weight on proximity and access in the shortlist score, and `ch2_outline.md` carries it into 2.4 ("Organisation, not distance, keeps spend out"). After the move, A.18 is "Asset counts by district", so the reference points at the wrong table and no check fails. The ch2_4 draft must cite Table A.19, or name the caption. `ch2_outline.md` also says that "Tables 1.3, 2.3 and A.17" in 1.4 [26] "still holds". That stops being true once 1.1 loses its table.
   - **The open item in ch1/04 [26]** reads "restate Tables 1.3, 2.3 and A.17". Here 1.3 becomes 1.2 and A.17 becomes A.18. Open items survive word for word, so this is the orchestrator's call. The item's content (which tables to restate) does not change; only the labels move. A logged knock-on edit in `apply_v8.py` that rewrites the numbers to 1.2 and A.18 (and 2.3 to whatever the Chapter 2 build gives) is the cleanest fix. Record it as a deliberate exception.
   Section 1.1's own text cites no table number.
2. **Executive summary outline.** In the "kept out" list of `es_outline.md`, the arrivals-measures footnote points to "section 1.1 (the closing paragraphs and table ...)". It should now read "section 1.1 and Appendix A2". Its proposed footnote note ("as section 1.1 sets out") still holds.
3. **Section 1.5 [16] and [17] and the 1.2 box "Three arrivals measures"** still restate the airport and model bases. They are left as they are. They do not conflict with the closing note, which applies the same three rules.
4. `pagemap.json` and `headings.json` regenerate on the next build. No content module cites the table by number.
