# Change log: draft v1 to draft v2

7 November 2026. Internal working record for Michael. Brief: "apply the red-team changes to Unlocking Tourism Growth, draft v1 to v2". Skip line: D1. Decisions D2 to D9 at their defaults.

Source edited: the content modules in `report/build/content/` (the JSON files the renderer reads), through one script, `report/build/redteam/apply_v2.py`, which holds every find string, its expected count and its replacement. The build lives at `report/build/` (not `/home/claude/build/`); the PDF comes from the project's `build.sh`, which converts with LibreOffice directly (there is no `soffice.py`). Renderer changes: `helpers.js` (P1 table header; numbered lists that carry on, for C6.1), `content_render.js` (passes that option) and `charts.js` (P3 time axis; P4 two-line Gantt labels).

Result: 291 logged edits. Every find matched the count the brief lists, or the extra match is explained below (C1.1, M7, M9). v1 has 191 pages and v2 193. Page numbers below are PDF pages, which equal the printed footer numbers.

## Summary by change ID

| ID | Status | v2 pages | Note |
| --- | --- | --- | --- |
| C1.1 | Done | 13, 18, 23, 25, 34, 43, 45, 46, 48, 85, 86, 115 and more | Every find in the table applied at the count listed, plus the chart label in all four charts |
| C1.2 | Done | 34, 167 | Both inserts made: the caveat paragraph after the Figure 1.4 source note (now holding the P2 note) and before "The routes that exist are full.", and the sentence in A2. |
| C1.3 | Done | 30, 35, 52, 86, 115, 145 | All six places changed |
| C2 | Done, one find adjusted for the D1 skip | 18, 22, 33, 34, 40, 71, 115 | All rows applied |
| C3 | Done | 20, 24, 26, 151, 154, 155, 192 | All six items done |
| C4.1 | Done | 13, 20, 30, 44, 48, 74, 75, 155 | All rows applied |
| C4.2 | Done | 20, 154, 155 | All three cells and the source note changed; the Spend paragraph is inserted directly after "Arrivals." in section 5.3 |
| C4.3 | Done | 20, 23, 113, 114, 151, 154, 155, 156 | All rows applied (D4: T1-04 kept, baseline and path removed) |
| C5 | Done | 28, 31, 39, 43, 49, 50, 54, 58, 63, 64, 86, 172 and more | All known instances applied; the sweep terms found no further passage that met the rule |
| C6.1 | Done, decision 1 kept for the D1 skip | 21 | List replaced with the Board decisions (1 to 5) and the recommendations (6 and 7), numbered on through the split |
| C6.2 | Done | 19, 142 | Both titles changed |
| C6.3 | Done (closed by C6.1) | 21 | Decision 3 now reads "first-24-month"; this also closes P6. |
| C6.4 | Done | 19, 106, 112, 142, 145, 188 | All rows applied (D2) |
| M1 | Skipped |  | Skipped: D1 is on Michael's skip line |
| M2 | Done | 35, 54, 55, 56, 57, 170, 171 | All rows applied, including the Figure 2.5 bars and the reference bar |
| M3 | Done | 36, 41, 79, 81, 103 | Qualifiers added in the three entries; no label, count, table or tree graphic changed |
| M4 | Done | 16, 48, 74 | Topline changed in both places (Chapter 3 and Table ES.2, which carries the Pillar 1 toplines) and both row labels changed. |
| M5 | Done | 39, 61 | Both open items added. |
| M6 | Done | 39 | Open item replaced |
| M7 | Done | 87, 127, 150, 151, 152, 156, 190 | All rows applied |
| M8 | Done | 17, 20, 67, 70, 99 | All rows applied |
| M9 | Done | 87, 104, 127, 144, 185, 188 | All rows applied |
| M10 | Done | 20, 30, 35, 53, 65, 66, 86, 115, 147 | All rows applied (D9) |
| M11 | Done | 147, 148 | Four rows added after the existing ten |
| M12 | Done | 16, 28, 30, 56, 57, 71, 83, 94 | All rows applied; both toplines match. |
| M13 | Done, one sentence omitted for the D1 skip | 13, 17, 32, 105 | ES opening replaced by the three paragraphs, except the sentence "The base path is the plan's target and the accelerated path its stretch.", omitted because D1 is on the skip line |
| P1 | Done | 150 | Rows I6 to I11 existed in the source |
| P2 | Done | 34 | The Figure 1.4 note now ends the figure's source line, wording kept. |
| P3 | Done | 18, 34, 45, 154 | charts.js lineChart gains a timeAxis option that places each year point at its calendar distance (2025 to 2035); points, labels, colours and y-axis unchanged |
| P4 | Done | 119 | The labels were cut in the chart data itself, not only by the renderer |
| P5 | Done | 42 | Both items moved, wording kept |
| P6 | Done (closed by C6.1) | 21 |  |
| P7 | Done | 165 | Table A.4 prints +323,805 and the sentence about the misprint is removed (logged in reconciliation_log.md under C5) |
| P8 | Done (closed by C1.3) | 30, 35, 52 |  |
| P9 | Done | 35 | p34 sentence inserted |
| P10 | Done (closed by C6.4) | 145 |  |
| P11 | Done | 170 |  |
| P12 | Done | 172 |  |
| P13 | Blocked |  | Investigated, not changed |
| P14 | Done (closed by C5) | 43, 49, 54, 58, 63, 67, 172, 183 |  |
| P15 | Done | 74 |  |
| P16 | Done | 84, 111, 185 |  |
| P17 | Done | 82, 184 |  |
| P18 | Done | 17, 60, 61, 101 | All ten occurrences changed: the first body mention (p58, with the date), p60 and the eight others. |
| P19 | Done | 25, 26 | Paragraph, Table 1.2 row (figure, source, open item) and the Table 1.2 source list changed |
| P20 | Done | 101 |  |
| Sources | Done | 25, 26, 35, 55, 87, 192, 193 | Nine rows added after the existing public sources, before the SLA row; the brief's "Type" is the table's Status column |

## Detail by change ID

### C1.1: Done

Every find in the table applied at the count listed, plus the chart label in all four charts. The p25 find ("before the base case reaches the seat ceiling") also sits inside the p115 title and the p118 sentence, which the brief names separately; those two longer finds were applied first, so the p25 find then matched once. The glossary term keeps its alphabetical place. Two further seat-line hits from the sweep were changed (marked Sweep); the remaining "ceiling" hits are listed under Sweeps.

| v1 page | v2 page | Before | After |
| --- | --- | --- | --- |
| 115 | 116 | before the base case reaches the seat ceiling, and the direct routes wait for runway relief | before the base case crosses the model's seat line, and the direct routes wait for runway relief |
| 118 | 119 | two years before the base case reaches the seat ceiling at its 2030 point | two years before the base case crosses the model's seat line around 2030 |
| 13 | 13 | Current air access caps inbound seats at 1.8 million, and the base case passes that ceiling at its 2030 point; runway re ... p21; Infrastructure Report, Jul 2026, p103). | The growth model draws current air access as a line at 1.8 million inbound seats, and the base case crosses it around 20 ... sport, as reported by Travel News, Aug 2026). |
| 18 | 18 | scales what works and meets the seat ceiling at the 2030 mid-term review | scales what works and meets the model's seat line at the 2030 mid-term review |
| 18, 152 | 18, 154 | and the base path passes the 1.8m seat ceiling before 2031 | and the base path crosses the model's 1.8m seat line before 2031 |
| 18, 152 | 18, 154 | and the base path passes the 1.8m seat ceiling before 2031 | and the base path crosses the model's 1.8m seat line before 2031 |
| 152 | 154 | (2028 and 2035 points; 1.8m ceiling) | (2028 and 2035 points; 1.8m seat line) |
| 23 | 23 | Even the base case runs into a ceiling. Current air access caps inbound capacity at 1.8 million seats, and the base case first passes that line at the 2030 plotted year | Even the base case runs into the model's seat line. The growth model draws inbound capacity at 1.8 million seats, and th ... rst passes that line at the 2030 plotted year |
| 23 | 23 | inbound capacity capped at 1.8 million seats | inbound capacity drawn at 1.8 million seats |
| 23 | 23 | lift the 1.8 million ceiling | lift the 1.8 million seat line |
| 25 | 25 | before the base case reaches the seat ceiling | before the base case crosses the model's seat line |
| 34 | 34 | The binding supply is seats. Current air access places a hard ceiling at 1.8 million inbound seats, and the base case | The binding supply is peak capacity at the gateway. The growth model draws current air access as a line at 1.8 million inbound seats, and the base case |
| 34 | 34 | The chart below sets the base case against that ceiling. | The chart below sets the base case against that line. |
| 34 | 34 | The base case crosses the 1.8m inbound seat ceiling at the 2030 plotted year, two years before the earliest relief at Cape Town International. | The base case crosses the model's 1.8m seat line at the 2030 plotted year, before runway relief on the planning date of about 2033. |
| 34 | 34 | Seat ceiling as drawn on the same slide. | Seat line as drawn on the same slide. |
| 42 | 43 | Concentration, seasonality and seats cap growth before demand does, and the base case meets the 1.8m inbound seat ceiling by 2030. | Concentration, seasonality and peak seats cap growth before demand does, and the base case crosses the model's 1.8m seat line by 2030. |
| 44 | 45 | The base case passes the 1.8m inbound seat ceiling at the 2030 year point | The base case crosses the model's 1.8m seat line at the 2030 year point |
| 44 | 45 | and the seat ceiling as drawn | and the seat line as drawn |
| 45 | 46 | 4. Seats bind before demand does. | 4. Seats bind at the peak before demand does. |
| 45 | 46 | with 1,802,929 arrivals (Market Assessment Report, May 2026, p20). | with 1,802,929 arrivals (Market Assessment Report, May 2026, p20). The line is the model's assumption, not a measured cap (section 1.3). |
| 47 | 48 | Seats bind by 2030 | Seat line crossed by 2030 |
| 47 | 48 | 1.8m inbound seats; | 1.8m inbound seats as drawn; |
| 84 | 85 | Current air access caps inbound seats at 1.8 million, and the base case passes that ceiling at the 2030 year point (Demand-Side Analysis, Jun 2026, p21). | The growth model draws current air access as a line at 1.8 million inbound seats, and the base case crosses it at the 20 ... n 2026, p21); the runway binds at peak hours. |
| 85 | 86 | The network is full on its best routes, the airport is full at its runway, and relief lands after the base case passes the seat ceiling. | The network is full on its best routes, the airport is full at its runway at peak, and planned relief lands after the base case crosses the model's seat line. |
| 85 | 86 | A seat ceiling in 2030 | A seat line in 2030 |
| 85 | 86 | Current air access caps inbound seats at 1.8 million; the base case passes it at the 2030 year point (1,802,929) | The model draws current air access at 1.8 million inbound seats; the base case crosses it at the 2030 year point (1,802,929) |
| 114 | 115 | The gateway binds first. Current air access places a hard ceiling at 1.8 million inbound seats, and the base case passes it at the 2030 year point | The gateway binds first, at peak. The growth model draws current air access as a line at 1.8 million inbound seats, and the base case crosses it at the 2030 year point |
| 115 | 116 | Before the base case reaches the seat ceiling at the 2030 point | Before the base case crosses the model's seat line around 2030 |
| 115 | 116 | The 2030 mid-term review tests the ceiling | The 2030 mid-term review tests the seat line |
| 115 | 116 | seat ceiling from Demand-Side Analysis | seat line from Demand-Side Analysis |
| 119 | 120 | Phase 2 scales what Phase 1 proved and meets the seat ceiling. | Phase 2 scales what Phase 1 proved and meets the model's seat line. |
| 144 | 146 | Arrivals against the base path at the seat ceiling (T1-01) | Arrivals against the base path at the model's seat line (T1-01); peak-hour runway headroom |
| 144 | 146 | Re-sequence Phase 2 if the ceiling binds early or relief slips | Re-sequence Phase 2 if peak capacity binds early or relief slips |
| 157 | 159 | a mid-term review in 2030, when the seat ceiling binds | a mid-term review in 2030, when the base case crosses the model's seat line |
| 157 | 159 | It falls in 2030 because that is when the base case reaches the 1.8 million seat ceiling (Demand-Side Analysis, Jun 2026 ... onal (Infrastructure Report, Jul 2026, p103). | It falls in 2030 because that is when the base case crosses the model's 1.8 million seat line (Demand-Side Analysis, Jun ... date (Infrastructure Report, Jul 2026, p103). |
| 162 | 164 | and its base case passes the 1.8 million seat ceiling at the 2030 year point | and its base case crosses the 1.8 million seat line the model draws, at the 2030 year point |
| 165 | 167 | Seat ceiling and model limits | Seat line and model limits |
| 165 | 167 | The model prints its seat ceiling and six base-case year points | The model prints its seat line and six base-case year points |
| 165 | 167 | Seat ceiling | Seat line |
| 165 | 167 | Year the ceiling binds | Year the line is crossed |
| 190 | 192 | Seat ceiling | Seat line |
| 190 | 192 | The 1.8 million inbound seats that current air access provides, as drawn in the Demand-Side Analysis | The 1.8 million inbound seats the growth model draws as current air access, as drawn in the Demand-Side Analysis; a model assumption, not a measured cap (section 1.3) |
| 34 | 34 | 1.8m inbound seat ceiling | 1.8m seat line (model) |
| 44 | 45 | 1.8m inbound seat ceiling | 1.8m seat line (model) |
| 18, 152 | 18, 154 | 1.8m inbound seat ceiling | 1.8m seat line (model) |
| 18, 152 | 18, 154 | 1.8m inbound seat ceiling | 1.8m seat line (model) |
| 114 | 115 | If the supply moves slip, the case stops at the ceiling. | If the supply moves slip, the case stops at the seat line. | Sweep
| 119 | 120 | tests arrivals against the base path when the ceiling binds | tests arrivals against the base path when the base case crosses the model's seat line | Sweep

### C1.2: Done

Both inserts made: the caveat paragraph after the Figure 1.4 source note (now holding the P2 note) and before "The routes that exist are full.", and the sentence in A2.

| v1 page | v2 page | Before | After |
| --- | --- | --- | --- |
| new | 34 | (insert) | The line is the model's assumption, not a measured cap. At Cape Town International's 79% average load factor, 1.8 millio ... al slot headroom at Cape Town International.] |
| 165 | 167 | Neither deck prints the seats behind the line or a load factor that converts seats into arrivals. | Neither deck prints the seats behind the line or a load factor that converts seats into arrivals. At the 79% average loa ... assumption, not a measured cap (section 1.3). |

### C1.3: Done

All six places changed. The planning date stays about 2033 (D3). The risk rows "Runway relief at Cape Town International slips past about 2033" (Tables ES.7 and 4.7) are left as instructed.

| v1 page | v2 page | Before | After |
| --- | --- | --- | --- |
| 30 | 30 | and ACSA's programme of about R11.3bn brings relief only from about 2032 to 2034 (Infrastructure Report, Jul 2026, p101 to p103). | and ACSA's programme of about R11.3bn brings relief from about 2032 for the international terminal and about 2033 for th ... sport, as reported by Travel News, Aug 2026). |
| 34 | 35 | and ACSA's programme of about R11.3bn brings relief only from about 2032 (p101 to p103). | and ACSA's programme of about R11.3bn brings relief from about 2032 for the terminal and about 2033 for the runway (p101 to p103). |
| 51 | 52 | The R6.39bn runway relocation adds about 40% more movements an hour but completes around 2033, and relief across the airport lands from about 2032 (p103). | The R6.39bn runway relocation lifts capacity from 30 to 45 movements an hour, a 50% rise, and completes around 2033 on t ... Portfolio Committee on Transport, Aug 2026). |
| 85 | 86 | the runway about 2033 | the runway about 2033; ACSA's latest schedule shows the runway by December 2029 |
| 85 | 86 | IR p101 to p103 | IR p101 to p103; ACSA, Aug 2026 |
| 114 | 115 | and about 2033 for the runway (Infrastructure Report, Jul 2026, p103). | and about 2033 for the runway (Infrastructure Report, Jul 2026, p103). ACSA now schedules the realigned runway for Decem ... sport, as reported by Travel News, Aug 2026). |
| 144 | 145 | confirm route cases for India and China | confirm route cases for India and China, and bring them into Phase 2 if ACSA awards the runway contract on its December 2029 schedule |

### C2: Done, one find adjusted for the D1 skip

All rows applied. The p13 thesis line is handled under M13. At p22 the thesis clause is replaced but "growth to 2.5 million arrivals" is kept instead of "between 2.2 million and 2.5 million", because D1 is on the skip line and the brief says to keep every goal statement as it is.

| v1 page | v2 page | Before | After |
| --- | --- | --- | --- |
| 22 | 22 | the evidence has reframed that ambition as growth to 2.5 million arrivals, set by supply rather than demand. | the evidence has reframed that ambition as growth to 2.5 million arrivals, paced by gateway capacity in the summer peak and by demand in the green season. |
| 33 | 33 | The recovery is complete, and the growth that follows is capped by supply rather than demand. | The recovery is complete; gateway capacity caps growth in the summer peak, and demand and conversion cap it in the green season. |
| 33 | 34 | Demand without seats | Seats in summer, demand in winter |
| 33 | 34 | Growth is now supply-constrained, not demand-constrained. | Growth is now supply-constrained in the summer peak and demand-constrained in the green season, when airlines withdraw s ... Market Assessment, Mar 2026, "Seasonality"). |
| 40 | 40 | why the next step is supply-constrained | why the next step is constrained by peak capacity |
| 18 | 18 | Marketing cannot make up for missing seats, because carriers on full routes raise fares instead (MIDAS Aviation Market Assessment, Mar 2026, In Conclusion). | On the eleven full routes, marketing cannot make up for missing seats, because carriers raise fares instead (MIDAS Aviat ... t base-case arrivals, it can ("Seasonality"). |
| 114 | 115 | Demand work cannot make up the gap, because marketing into full routes raises fares rather than seats (MIDAS Aviation Market Assessment, Mar 2026, In Conclusion). | On the full routes, demand work cannot make up the gap, because marketing raises fares rather than seats (MIDAS Aviation ... ub routes, which have seats to spare, it can. |
| 70 | 71 | Demand is not what holds Pillar 1 back; conversion is. | Latent interest is not what holds Pillar 1 back; turning it into bookings is. |

### C3: Done

All six items done. The C3.1 paragraph sits directly after the Table 1.2 source note. One comma was removed from the brief's text ("returning residents, or OAG" became "returning residents or OAG") under rule 7, no Oxford comma.

| v1 page | v2 page | Before | After |
| --- | --- | --- | --- |
| new | 26 | (insert) | The model's 2025 base of 1,498,829 sits close to, but below, SA Tourism's 1,538,142 for 2025 (Wesgro Research, Western C ... tion flows) and how the Hubs group is built.] |
| 24 | 24 | (Wesgro, presentation to the parliamentary committee, 1 Apr 2026; public source). [G4J 2023 document | (Wesgro, presentation to the parliamentary committee, 1 Apr 2026; public source). If the model counts arrivals on the SA ... tes the gateway can carry. [G4J 2023 document |
| 153 | 155 | tourist arrivals on the model's basis, and international passenger arrivals at Cape Town International. | arrivals on the growth model's basis, which Skift is to confirm (section 1.1), and international passenger arrivals at Cape Town International. |
| 190 | 192 | On the growth model's basis, tourist arrivals; | On the growth model's basis, which Skift is to confirm; |
| 152 | 154 | 1,498,829 (2025) | 1,498,829 (2025, model value) |
| 20 | 20 | 1,498,829 (2025) | 1,498,829 (2025, model value) |
| 149 | 151 | SA Tourism | SA Tourism [Open item: SA Tourism cannot report the Hubs group; Skift to define it.] |

### C4.1: Done

All rows applied. The p30 find spans two paragraphs in the source: the replacement closes the first paragraph and the second keeps its 2024 sentence. Table 1.3's source note now says the 2025 shares are normalised to 100% for the October to March share. Table 2.2's source key gains "Diag", which its new source cell uses (Consequential). p28 is unchanged.

| v1 page | v2 page | Before | After |
| --- | --- | --- | --- |
| 13 | 13 | and about 65% of overseas visitor travel falls between October and March, a provisional figure | and about 62% of overseas visitor travel falls between October and March |
| 30 | 30 | October to March together account for about 65% of the year. | October to March together account for about 62% of the year once the twelve printed shares, which sum to 104.9%, are sca ... to confirm the 2025 month-of-travel shares]. |
| 30 | removed | That 65% is derived, not printed. The twelve monthly shares on the 2025 slide sum to 104.9%, so the October to March fig ... to confirm the 2025 month-of-travel shares]. | (deleted) |
| 30 | 30 | between 61% and 65% | between 61% and 62% |
| 30 | 30 | 65% | 62% |
| 30 | 30 | (Stats SA and SAT 2025; the printed shares sum to 104.9%, so the 2025 row and its October to March share are provisional) | (Stats SA and SAT 2025; the printed shares sum to 104.9%, and the October to March share is computed with the 2025 shares normalised to 100%) |
| 43 | 44 | October to March hold about 65% on that table, a provisional figure because its twelve shares sum to 104.9%. On a Cape T ... 9% (Market Assessment Report, May 2026, p25). | October to March hold about 62% on that table once its twelve shares, which sum to 104.9%, are normalised. The 2024 Wesg ... 9% (Current State Diagnostic, Dec 2025, p32). |
| 47 | 48 | October to March about 65%, 2025 (provisional; shares sum to 104.9%); 61%, Jan to Aug 2024, Cape Town overseas air arrivals | October to March about 62%, 2025 (normalised; printed shares sum to 104.9%); 61%, 2024, Wesgro Visitor Tracking Survey |
| 47 | 48 | DSA p12; MA p25 | DSA p12; Diag p32 |
| 73 | 74 | About 65% of 2025 overseas visitor travel fell between October and March (provisional) | About 62% of 2025 overseas visitor travel fell between October and March (normalised) |
| 73 | removed | , while the Market Assessment, p25, prints the same split on a Cape Town overseas air-arrivals basis | (deleted) |
| 74 | 75 | The October to March share is about 65% for 2025, but the figure is provisional: it is computed from a month-of-travel t ... 104.9% (Demand-Side Analysis, Jun 2026, p12). | The October to March share is about 62% for 2025, computed from a month-of-travel table whose shares sum to 104.9% and normalised (Demand-Side Analysis, Jun 2026, p12). |
| 20 | 20 | About 35% (2025, provisional); 39% (2024) | 38.1% (2025, normalised); 39% (2024) |
| 153 | 154 | About 35% (2025, provisional; 38.1% normalised); 39% (2024) | 38.1% (2025, normalised); 39% (2024) |
| 153 | 155 | Green season. Plan decision 6 sets the October to March share at about 65% for 2025, provisional, which puts the green s ... confirm: switch the T1-05 baseline to 38.1%]. | Green season. The 2025 month table sums to 104.9%. Normalised, it gives 61.9% for October to March and 38.1% for the gre ... 2025, p32). T1-05 uses 38.1% as its baseline. |

### C4.2: Done

All three cells and the source note changed; the Spend paragraph is inserted directly after "Arrivals." in section 5.3. The brief's Table 5.6 is Table 5.7 in the report.

| v1 page | v2 page | Before | After |
| --- | --- | --- | --- |
| 152 | 154 | R25.9bn (FY2025) | R25.9bn (FY2025, nominal) |
| 20 | 20 | R25.9bn (FY2025) | R25.9bn (FY2025, nominal) |
| 152 | 154 | R40.6bn (base, modelled) | R40.6bn (base, modelled, constant 2024 rand) |
| 20 | 20 | R40.6bn (base, modelled) | R40.6bn (base, modelled, constant 2024 rand) |
| 152 | 154 | R33.7bn in 2030 (base, modelled) | R33.7bn in 2030 (base, modelled, constant 2024 rand) |
| new | 155 | (insert) | Spend. T1-03's path holds spend per arrival fixed, so its targets are in constant 2024 rand, while SA Tourism reports no ... spend path on the FY2025 actual of R25.9bn.] |
| 20 | 20 | Tourism jobs have no provincial baseline; the labour analysis (I18) sets one by Gate 1. | Tourism jobs have no provincial baseline; the labour analysis (I18) sets one by Gate 1. T1-03 targets are in constant 2024 rand. |

### C4.3: Done

All rows applied (D4: T1-04 kept, baseline and path removed). The brief's Table 5.6 is Table 5.7 and its "Table 5.8" methodology row sits in Table 5.9; the row is deleted and the provincial employment row kept. Consequential: Table 5.4 T1-04 source, Table 5.9 title count, Table 1.1 jobs row, the ES.6 and 5.7 titles and the 5.3 topline, each of which said jobs carry a ratio or targets.

| v1 page | v2 page | Before | After |
| --- | --- | --- | --- |
| 152 | 154 | Tourism jobs (ratio) | Tourism jobs |
| 20 | 20 | Tourism jobs (ratio) | Tourism jobs |
| 20 | 20 | About 30,000 (2025) | Set by the labour analysis (I18) |
| 153 | 154 | About 30,000 jobs supported (2025) | Set by the labour analysis (I18) |
| 152 | 154 | 33,500 / 35,000 | Set at Gate 1 |
| 20 | 20 | 33,500 / 35,000 | Set at Gate 1 |
| 152 | 154 | 37,400 / 40,900 | Set at Gate 1 |
| 152 | 154 | 43,500 / 50,300 | Set at Gate 1 |
| 20 | 20 | 43,500 / 50,300 | Set at Gate 1 |
| 20 | 20 | Jobs use Wesgro's ratio of two jobs per 100 international passengers (public source), a ratio-based projection until the labour analysis reports. | Tourism jobs have no provincial baseline; the labour analysis (I18) sets one by Gate 1. |
| 153 | 155 | T1-04: Wesgro's ratio of two jobs per 100 international passengers, applied to T1-01 (computed; public source, see the note below). | T1-04: baseline and targets to be set by the labour analysis (I18). |
| 153 | 155 | The Tier 1 measure is therefore jobs supported by international air arrivals, on Wesgro's own rule of thumb of two jobs ... ased projection, not a labour-market measure. | T1-04 therefore carries no baseline or modelled path until the labour analysis sets a provincial measure (I18). |
| 153 | removed | The ratio does not reach the 300,000 tourism-linked jobs in the Inception Report's ambition, because it counts only jobs ... ir arrivals (Inception Report, Nov 2025, p4). | (deleted) |
| 112 | 113 | Until it reports, Chapter 5 carries jobs as a ratio-based measure on Wesgro's own rule of two jobs per 100 international passengers (section 5.3). | Until it reports, Chapter 5 carries jobs without a baseline or target. |
| 113 | 114 | carried as a ratio-based projection until the analysis reports | with its baseline set by the analysis |
| 149 | 151 | Jobs supported by international air arrivals, on Wesgro's ratio, until the labour analysis sets a provincial measure | Tourism jobs in the Western Cape, on the measure the labour analysis sets (I18) |
| 154 | removed | Methodology for two jobs per 100 passengers / T1-04 / Air Access / Mid 2027 / Cape Town Air Access note | (deleted) |

### C5: Done

All known instances applied; the sweep terms found no further passage that met the rule. Passages that may meet it but match no sweep term are left and listed under Seen, not changed (items 2 to 5). The two caveats the brief keeps (Nigeria and Ghana spend averages; readiness accessibility basis) stay as single lines. SLA Annexure B and the 14 October deck are not in the build's input folders, so their open items are left as they are. Every removed passage, with its v1 page, is in reconciliation_log.md.

| v1 page | v2 page | Before | After |
| --- | --- | --- | --- |
| 38 | removed | The reconciliation behind this rule logged 55 discrepancies between the agreed structure and the deliverables, seven of ... ved where it is used, with both values shown. | (deleted) |
| 38 | removed | Four carry a later file date than their cover, which the report records rather than hides. | (deleted) |
| 38 | 39 | SLA Annexure B clause numbers as assigned in the agreed report structure of 2 November 2026 [to be checked against the signed Annexure B] | SLA Annexure B clause numbers [to be checked against the signed Annexure B] |
| 42 | 43 | The agreed report structure assigns this work to SLA Annexure B clause | This work answers SLA Annexure B clause |
| 48 | 49 | The agreed report structure assigns this work to SLA Annexure B clause | This work answers SLA Annexure B clause |
| 53 | 54 | The agreed report structure assigns this work to SLA Annexure B clause | This work answers SLA Annexure B clause |
| 57 | 58 | The agreed report structure assigns this work to SLA Annexure B clause | This work answers SLA Annexure B clause |
| 61 | 62 | The agreed report structure assigns this work to SLA Annexure B clause | This work answers SLA Annexure B clause |
| 66 | 67 | The agreed report structure assigns this work to SLA Annexure B clause | This work answers SLA Annexure B clause |
| 49 | 50 | Sixteen ran at 75% or more, the count the agreed structure attributes to the 80% line (computed from the same table). | Sixteen ran at 75% or more (computed from the same table). |
| 52 | removed | The structure's "16 of 27 above 80%" is corrected to eleven. | (deleted) |
| 85 | 86 | The October record gives the reason as 16 of 27 routes above 80% and fares before seats. MIDAS, the source, prints eleve ... ct 2026: the deck's basis for 16 to confirm]. | The reason is full routes and fares before seats: eleven routes run above 80% load and sixteen at 75% or more (MIDAS Aviation Market Assessment, Mar 2026, "Seasonality"). |
| 28 | 28 | The same slide prints 61% in its text; the report uses 63%, the sum of the printed shares, and logs the conflict. | The report uses 63%, the sum of the printed shares. |
| 31 | 31 | (the Winelands gauge misprints 40.3%; 7,730 of 50,332 is 15.4%) | (Winelands share computed: 7,730 of 50,332 is 15.4%) |
| 63 | 64 | (the Winelands gauge misprints 40.3%; 7,730 of 50,332 is 15.4%) | (Winelands share computed: 7,730 of 50,332 is 15.4%) |
| 174 | 176 | The main gauge on the Cape Winelands asset slide prints 40.3%, the Cape Metro's share, while the slide's text layer carr ... s 15.4% (computed). This appendix uses 15.4%. | This appendix uses 15.4%, computed from the count (7,730 of 50,332). |
| 48 | 49 | The body of the report counts fourteen new routes since 2014, a difference this report logs. | Other study documents count new routes from 2014 on a different basis. |
| 167 | removed | It printed ranks 7 to 30 with scores and reasons for exclusion; ranks 1 to 6 and their scores appear nowhere (p31). | (deleted) |
| 172 | 174 | Overall rating. The printed overall ratings do not follow the stated weights. Applied to the printed dimension scores, 4 ... values behind the calibration claimed on p15. | Overall rating. The overall ratings are the Infrastructure Report's evidence-informed judgement, not a weighted formula, so this report does not re-derive them. |
| 62 | 63 | The printed overall ratings do not reproduce from the weighted dimension scores, so this report quotes them as printed. | The overall ratings are the Infrastructure Report's evidence-informed judgement, not a weighted formula, so this report does not re-derive them. |
| 171 | removed | ; the label 'Road Netowrk' is corrected | (deleted) |
| 174 | removed | The slides spell Cederberg 'Cederburg' and title both p72 and p73 'West Coast / Overberg'. | (deleted) |
| 179 | removed | Slide titles print Mossell Bay, Dep Mobility, Dep Economic Development, Statistic SA, Table Mountain Ariel Cable and Cape Nature. | (deleted) |
| 170 | 172 | house style | this report's style |
| 181 | 183 | house style | this report's style |
| 42 | 43 | This report uses the 2025 base and logs the difference. | This report uses the 2025 base. | Sweep

### C6.1: Done, decision 1 kept for the D1 skip

List replaced with the Board decisions (1 to 5) and the recommendations (6 and 7), numbered on through the split. Decision 1 keeps its v1 wording ("Adopt growth to 2.5 million arrivals by 2035 as the plan's goal, with the base and accelerated paths as its targets.") because D1 is on the skip line. No cross-reference to an old decision number exists; the new M11 risk row cites Decision 3 on the new numbering. The paragraph "Several items remain open..." is kept.

| v1 page | v2 page | Before | After |
| --- | --- | --- | --- |
| 20 | 21 | Adopt growth to 2.5 million arrivals by 2035 as the plan's goal, with the base and accelerated paths as its targets. / C ... ration processing at Cape Town International. | The Wesgro Board decides: / Adopt growth to 2.5 million arrivals by 2035 as the plan's goal, with the base and accelerat ... nd I12, and that the site operators lead I11. |

### C6.2: Done

Both titles changed. Table 4.4's rows are unchanged.

| v1 page | v2 page | Before | After |
| --- | --- | --- | --- |
| 19 | 19 | Twelve actions can start inside Wesgro's current mandate and budgets, and each opens a seat, a baseline or a booking path a later initiative needs. | Twelve actions can start in the first 24 months, nine of them inside Wesgro's current mandate and budget, and each opens ... e or a booking path a later initiative needs. |
| 141 | 142 | Twelve actions can start by mid-2028 inside Wesgro's current mandate, and each one opens | Twelve actions can start by mid-2028, nine of them inside Wesgro's current mandate and budget, and each one opens |

### C6.3: Done (closed by C6.1)

Decision 3 now reads "first-24-month"; this also closes P6.

### C6.4: Done

All rows applied (D2). The I15 charter does not describe the chair, so its Partners cell is unchanged (its Dependencies cell is listed under Seen, not changed). Consequential: the Figure 4.3 label is longer than the box at 20px, so that one label is set at 17px; nothing else in the diagram moved.

| v1 page | v2 page | Before | After |
| --- | --- | --- | --- |
| 144 | 145 | A Tourism Growth Steerco chaired at Wesgro CEO level, with DEDAT and Cape Town Tourism as standing members and the City ... alities and the industry bodies at the table. | A Tourism Growth Steerco co-chaired by Wesgro's CEO and DEDAT's Head of Department, with Cape Town Tourism as a standing ... ing Tourism Steerco that oversees this study. |
| 144 | 145 | Chair: Wesgro CEO. With DEDAT and Cape Town Tourism | Co-chairs: Wesgro CEO and DEDAT HOD. With Cape Town Tourism |
| 182 | 184 | Constitute the Tourism Growth Steerco with DEDAT and Cape Town Tourism, and agree a decision-rights map by tier | Constitute the Tourism Growth Steerco, co-chaired with DEDAT and with Cape Town Tourism as a standing member, and agree a decision-rights map by tier |
| 105, 186 | 106, 188 | Constitute the Tourism Growth Steerco with DEDAT and Cape Town Tourism, and agree a decision-rights map by tier | Constitute the Tourism Growth Steerco, co-chaired with DEDAT and with Cape Town Tourism as a standing member, and agree a decision-rights map by tier |
| 141 | 142 | Wesgro CEO's office | Wesgro CEO's office; DEDAT |
| 19 | 19 | Wesgro CEO's office | Wesgro CEO's office; DEDAT |

### M1: Skipped

Skipped: D1 is on Michael's skip line. p26 and the Figure ES.1 header are unchanged. Goal statements naming 2.5 million are kept (see Sweeps).

### M2: Done

All rows applied, including the Figure 2.5 bars and the reference bar. Consequential: the p35 range end (4% to 35% became 4% to 40%), the Kenya bar label (no longer a range midpoint) and the Figure 2.5 source note. The open item sits directly after the Table 2.5 source note. Table A.12 keeps its printed values.

| v1 page | v2 page | Before | After |
| --- | --- | --- | --- |
| 35 | 35 | Chile grew about 35%, Singapore about 19%, Kenya 12.8 to 14.6%, Valencia 13 to 14% and New Zealand about 12%. | Chile grew 40.4%, Singapore 21%, Kenya 14.6%, Valencia 13 to 14% and New Zealand about 12%, against global growth of 11% ... Tourism, World Tourism Barometer, Jan 2025). |
| 53 | 54 | (Global Benchmarking Report, Mar 2026, p7). | (Global Benchmarking Report, Mar 2026, p7). UN Tourism's own figures put global growth at 11% in 2024, while recovery wa ... ld Tourism Barometer, Jan 2025 and Jan 2026). |
| 53 | 54 | 1. Five of the six comparators grew well above the norm. Chile grew about 35% between 2023 and 2024, Singapore about 19% ... % (Global Benchmarking Report, Mar 2026, p9). | 1. Two of the six comparators grew well above the world. Chile grew 40.4% between 2023 and 2024 and Singapore 21%, again ... Dec 2025; Singapore Tourism Board, Feb 2025). |
| 53 | 55 | Five of the six comparators grew above the 3% to 5% global norm in 2023 to 2024, each through a primary lever of its own. | Against global growth of 11% in 2024, only Chile and Singapore grew clearly faster, and three of the six were still below 2019. |
| 53 | 55 | About 35% | 40.4% |
| 53 | 55 | About 82% recovered | 116% of 2019; 55.6% of arrivals overland, 40% from Argentina |
| 53 | 55 | About 19% | 21% |
| 53 | 55 | Slightly below; spend recovered | 86% of 2019; receipts at a record |
| 53 | 55 | 12.8% to 14.6% | 14.6% |
| 54 | 55 | p53 (New Zealand arrivals), p17 (Australian forecast) and p61 (system type). | p53 (New Zealand arrivals), p17 (Australian forecast) and p61 (system type). Chile: Sernatur, Anuario de Turismo 2024 (D ... th: Kenya Tourism data as reported, May 2025. |
| new | 55 | (insert) | [Open item: add one comparator that underperformed, as the Inception Report's plan asked (Inception Report, Nov 2025, p16).] |
| 54 | 55 | Five of the six comparators grew three to nine times the roughly 4% global rate of 2024 to 2025. | Against global growth of 11% in 2024, Chile and Singapore grew two to four times as fast, and Kenya, Valencia and New Zealand slightly faster. |
| 54 | 55 | Chile / Singapore / Kenya (range midpoint) / Valencia (range midpoint) / New Zealand (holiday arrivals) / Melbourne (Australian forecast) / Global, 2024 to 2025 | Chile / Singapore / Kenya (range midpoint) / Valencia (range midpoint) / New Zealand (holiday arrivals) / Melbourne (Australian forecast) / World, 2024 (UN Tourism) |
| 55 | 56 | It received 13 million international visitors in 2024, 19% more than in 2023, and visitor spend reached $31.3 billion (p39). | It received 16.5 million international visitors in 2024, 21% more than in 2023, and tourism receipts reached a record of ... billion (Singapore Tourism Board, Feb 2025). |
| 56 | 57 | Singapore: stopover programme; 13m arrivals (+19%) and $31.3bn spend, 2024 | Singapore: stopover programme; 16.5m arrivals (+21%) and about S$29bn receipts, 2024 |
| 56 | 57 | p39, p40 | p39, p40; STB, Feb 2025 |
| 56 | 57 | Norm 3% to 5% a year; Chile about 35%, Singapore about 19%, Valencia 13% to 14% | World 11% in 2024; Chile 40.4%, Singapore 21%, Valencia 13% to 14% |
| 168 | 170 | Five of the six printed growth rates exceed the 3% to 5% global norm, and four of the six cases pair structural demand creation with demand activation. | Five of the six printed growth rates exceed the report's 3% to 5% norm, two clearly beat 2024's actual global growth of ... tural demand creation with demand activation. |
| 169 | 171 | raises value per traveller without increasing arrivals. | raises value per traveller without increasing arrivals. Corrected 2024 figures: Chile 40.4% (116% of 2019), Singapore 21% (86% of 2019), Kenya 14.6% (section 2.2). |

### M3: Done

Qualifiers added in the three entries; no label, count, table or tree graphic changed. Table 1.9 sits in section 1.5 (pp40 to 41 in v1), so "What the evidence argued against." follows it there, as a bold run-in like the report's other run-ins.

| v1 page | v2 page | Before | After |
| --- | --- | --- | --- |
| 78 | 79 | October 2026: Reworded. | October 2026: Reworded, with the scope narrowed. |
| 80 | 81 | October 2026: Validated. Full routes. | October 2026: Validated, without fare or yield data. Full routes. |
| 102 | 103 | October 2026: Validated. No pipeline. | October 2026: Validated, on inference. No pipeline. |
| 36 | 36 | The Stakeholder Insights Report mapped all 223 of its insight statements to tree entries before aggregating them (Stakeholder Insights Report, Mar 2026, p5, p20 to p46). | The Stakeholder Insights Report mapped all 223 of its insight statements to tree entries before aggregating them (Stakeh ... ; they do not on their own validate an entry. |
| new | 41 | (insert) | What the evidence argued against. No entry was withdrawn, but the evidence narrowed or overturned three parts of the Dec ... rence from the pipeline tables (section 3.3). |

### M4: Done

Topline changed in both places (Chapter 3 and Table ES.2, which carries the Pillar 1 toplines) and both row labels changed.

| v1 page | v2 page | Before | After |
| --- | --- | --- | --- |
| 16, 73 | 16, 74 | The green season is a seat problem and an events problem at once: June holds 6.4% of the year's international seats, whi ... er in the months leisure travel leaves empty. | The green season is a seat problem and an events problem at once. June holds 6.4% of the year's international seats, and ... meetings now peak from September to November. |
| 16 | 16 | The green season is a seat problem and an events problem at once: June holds 6.4% of the year's international seats, whi ... er in the months leisure travel leaves empty. | The green season is a seat problem and an events problem at once. June holds 6.4% of the year's international seats, and ... meetings now peak from September to November. |
| 73 | 74 | Meetings fill the trough | Meetings sit beside the trough |
| 47 | 48 | Business events fill the green season | Business events can fill the green season |

### M5: Done

Both open items added.

| v1 page | v2 page | Before | After |
| --- | --- | --- | --- |
| 39 | 39 | the six demand-side engagements were proposed for phase 2 (Stakeholder Insights Report, Mar 2026, p16). | the six demand-side engagements were proposed for phase 2 (Stakeholder Insights Report, Mar 2026, p16). [Open item: test ... e Town and Cape Town Tourism before Steerco.] |
| 60 | 61 | Insights are the project team's statements, attributed to the organisation engaged. | Insights are the project team's statements, attributed to the organisation engaged. [Open item: each organisation named ... o approve its paraphrase before publication.] |

### M6: Done

Open item replaced. Supply_Infrastructure.xlsx is not in the build's input folders, so the 50,332 count could not be tested; no count or share is restated.

| v1 page | v2 page | Before | After |
| --- | --- | --- | --- |
| 39 | 39 | [Supply dataset limits to confirm: neither part of the Infrastructure Report, Jul 2026 (p1 to p114) states that the data ... ers; the source of this statement is needed.] | The supply dataset behind the Infrastructure Report (Supply_Infrastructure.xlsx) holds no geography below district, and ... .20 and the district shares drawn from them.] |

### M7: Done

All rows applied. The Baseline column of Table 5.5 confirms the seven without a baseline are T2-04, T2-18, T2-20, T2-21, T2-23, T2-24 and T2-25. The new line points to Table 5.9, the table with the dated gaps (the brief calls it Table 5.8). The find "T2-10 routes above 80% load" also matched Table 5.2 (p147), which the brief does not list; renamed there to match (Consequential).

| v1 page | v2 page | Before | After |
| --- | --- | --- | --- |
| 150 | 152 | India 71,000; China 29,600 (2025) | India 76,547; China with Hong Kong 43,412 (2025, model value) |
| 150 | 151 | MIDAS, The Indian Market Opportunity; The Chinese Market Opportunity | MA p20, p22 |
| 149 | 152 | 323,971 arrivals (2024); R4.2bn spend (2025) | 292,514 arrivals (2025, model value, regional group); R4.2bn spend (2025) |
| 149 | 151 | DSA p27, p29 | MA p20; DSA p29 |
| 149 | 151 | Spend traced to businesses trading inside the 20 shortlisted communities, as a share of foreign direct spend | Spend traced to businesses trading inside the pilot communities, as a share of foreign direct spend; widened to the 20 shortlisted communities once a source covers them |
| 188 | 190 | Routes above 80% load | Seats added on routes above 80% load |
| 149 | 151 | Routes above 80% load | Seats added on routes above 80% load |
| 150 | 152 | 11 of 27 (year to Nov 2025) | 11 routes above 80% (year to Nov 2025); seats added from the capacity-against-demand model (I6) |
| 86 | 87 | T2-10 routes above 80% load | T2-10 seats added on full routes |
| 86, 126 | 87, 127, 150 | T2-10 routes above 80% load | T2-10 seats added on full routes |
| 154 | 156 | Re-score in 2029 and 2032 | Re-score in 2029 and 2032 [Open item: publish the scoring formula before the 2029 re-score; the Infrastructure Report's ... l ratings are judgement-based (Appendix A4).] |
| new | 152 | (insert) | The seven without a baseline are T2-04, T2-18, T2-20, T2-21, T2-23, T2-24 and T2-25. Each carries no target until its baseline exists, on the dates in Table 5.9. |

### M8: Done

All rows applied. The 0.02% to 0.04% figures in the Chapter 2 and 3 bodies and Appendix A5 are left, as instructed.

| v1 page | v2 page | Before | After |
| --- | --- | --- | --- |
| 17, 98 | 17, 99 | Twenty communities hold 18.4% of the province's residents but a traced 0.02% to 0.04% of foreign direct spend, and in el ... int is organisation, not distance or product. | Twenty communities hold 18.4% of the province's residents but receive only a small documented share of foreign direct sp ... int is organisation, not distance or product. |
| 17 | 17 | Twenty communities hold 18.4% of the province's residents but a traced 0.02% to 0.04% of foreign direct spend, and in el ... int is organisation, not distance or product. | Twenty communities hold 18.4% of the province's residents but receive only a small documented share of foreign direct sp ... int is organisation, not distance or product. |
| 20 | 20 | 0.02% to 0.04% (floor) | R4m to R10m a year (documented floor) |
| new | 99 | (insert) | [Open item: the Inclusion Plan to set out how the R4m to R10m floor was traced.] |
| 66 | 67 | Distance is the binding constraint in none of the 20 (p30). | Distance is the binding constraint in none of the 20 (p30). Proximity and access carried 35% of the shortlist score (Tab ... is result is partly built into the selection. |
| 69 | 70 | Archetypes abbreviated: N = near a node (45 minutes or less); R = remote; A = assets underused; 0 = no community-based product. | Archetypes abbreviated: N = near a node (45 minutes or less); R = remote; A = assets underused; 0 = no community-based p ... as the V&A Waterfront or the CBD, not CTIA.] |
| 98 | 99 | Walter Sisulu Square cost R160 million to R180 million before an operator was in place | Walter Sisulu Square cost R160 million to R180 million, out of the R436 million first allocated to Kliptown (section 2.6), before an operator was in place |

### M9: Done

All rows applied. The p103 find also matched its verbatim copy in Appendix A7 (p186); applied to both, because A7 reproduces the Chapter 3 actions word for word and the brief pairs the two pages for every other A7 action it changes (M9 row 1, C6.4, P16, P17). Revert the A7 row if you want the strict count rule.

| v1 page | v2 page | Before | After |
| --- | --- | --- | --- |
| 182 | 184 | Set up a public-private air access fund for route support, on the Chilean model | Scale and ring-fence Cape Town Air Access's route fund as a public-private fund for route support, with a set size and governance |
| 86, 183 | 87, 185 | Set up a public-private air access fund for route support, on the Chilean model | Scale and ring-fence Cape Town Air Access's route fund as a public-private fund for route support, with a set size and governance |
| 182 | 184 | Set up the public-private air access fund with ring-fenced corridor budgets (focus area 7) | Scale Cape Town Air Access's route fund into the public-private air access fund, with ring-fenced corridor budgets (focus area 7) |
| 103, 186 | 104, 188 | Set up the public-private air access fund with ring-fenced corridor budgets (focus area 7) | Scale Cape Town Air Access's route fund into the public-private air access fund, with ring-fenced corridor budgets (focus area 7) |
| 86 | 87 | The required change for the Western Cape is a permanent, well-funded public-private air access fund and active lobbying for air service liberalisation (p28). | For the Western Cape the lesson splits by tier. The province can scale its existing route fund; open skies and private a ... Sernatur, Anuario de Turismo 2024, Dec 2025). |
| 143 | 144 | The air access fund draws public and private money on the Chilean model (I6; Global Benchmarking Report, Mar 2026, p28). | The air access fund scales Cape Town Air Access's existing route fund with public and private money (I6). |
| 121, 122, 123, 124 and more | 127 | Rand band to be set (section 4.6). | Rand band to be set (section 4.6). [Open item: Air Access to give the current size and funders of its route fund.] |

### M10: Done

All rows applied (D9). p157 ("did the second gateways carry the load meanwhile?") is left as it is.

| v1 page | v2 page | Before | After |
| --- | --- | --- | --- |
| 146 | 147 | George as second gateway | George for domestic connections |
| 20 | 20 | George as second gateway | George for domestic connections |
| 114 | 115 | and from George, whose terminal doubles by 2028 (focus areas 5, 6 and 7) | and, for domestic connections, from George, whose terminal doubles by 2028 or 2029 (focus areas 5, 6 and 7) |
| 30 | 30 | George, above its design limit at 911,000 passengers in 2025, doubles by 2028 (p104, p105) | George, above its design limit at 911,000 passengers in 2025, doubles by 2028 or 2029, with construction from October 2026 (p104, p105; George Herald, Jul 2026) |
| 34 | 35 | George, domestic only, doubles by 2028 | George, domestic only, doubles by 2028 or 2029 |
| 51 | 53 | doubles it to about 2 million by 2028 | doubles it to about 2 million by 2028 or 2029 |
| 52 | 53 | George to about 2m by 2028 | George to about 2m by 2029 |
| 64 | 65 | terminal doubles capacity by 2028 | terminal doubles capacity by 2028 or 2029 |
| 65 | 66 | George R310m by 2028 | George R310m by 2029 |
| 85 | 86 | George is solved by 2028 (R310m, to about 2m passengers) | George doubles by 2028 or 2029 (R310m, to about 2m passengers) |

### M11: Done

Four rows added after the existing ten. Check of the existing rows: six sit outside Wesgro's control, read as risks whose remedy sits with another body (runway with ACSA; air agreements, visas and LTO funding with national government; safety with SAPS; water and power with utilities); the other four are mitigated through Wesgro's own programmes. Six confirmed, so the lead reads ten of fourteen. Consequential: the Table 4.7 title count and its source key (DSA). No other risk count exists; Table ES.7 is unchanged. **Michael to review the four new ratings (likelihood and impact), which are Letsema's assessment.**

| v1 page | v2 page | Before | After |
| --- | --- | --- | --- |
| new | 147 | (insert) | Gulf hub disruption cuts connecting capacity / Hub routes carry 53% of arrivals on the ten largest routes (DSA p13) / Me ... irect-route cases ready (I4, I6) / Air Access |
| new | 147 | (insert) | A downturn in the core markets / The UK, Germany and the USA supply 52% of overseas arrivals (DSA p13) / Medium / High / ... markets (I1, I4, I5) / Destination Marketing |
| new | 147 | (insert) | Wesgro's operating budget is cut / Thirteen initiatives draw mainly on Wesgro's operating budget (Table 4.5) / Medium / ... e 1 (Decision 3) / Wesgro CEO's office; DEDAT |
| new | 148 | (insert) | Resident pushback in the Metro / Public debate on locals' costs and access (Hypertext, Apr 2026) / Medium / Medium / Spr ... timent / City of Cape Town; Cape Town Tourism |
| 146 | 147 | Six of the ten material risks sit outside Wesgro's control | Ten of the fourteen material risks sit outside Wesgro's control |

### M12: Done

All rows applied; both toplines match.

| v1 page | v2 page | Before | After |
| --- | --- | --- | --- |
| 16, 82 | 16, 83 | Regional Africa is the province's steadiest volume and its least developed premium market: Zimbabwe and Namibia supply 6 ... aian visitors spend R31,000 and R27,700 each. | Regional Africa is the province's steadiest volume and its least developed premium market: Zimbabwe and Namibia supply 6 ... st African visitors spend the most per visit. |
| 16 | 16 | Regional Africa is the province's steadiest volume and its least developed premium market: Zimbabwe and Namibia supply 6 ... aian visitors spend R31,000 and R27,700 each. | Regional Africa is the province's steadiest volume and its least developed premium market: Zimbabwe and Namibia supply 6 ... st African visitors spend the most per visit. |
| 70 | 71 | Regional routes run above 80% load; Nigerian and Ghanaian visitors spend R31,000 and R27,700 each | Regional routes run above 80% load; West African visitors spend the most per visit |
| 82 | 83 | Nigeria R31,000, Ghana R27,700 and Kenya R16,900 | Nigeria R31,000, Ghana R27,700 and Kenya R16,900 (printed averages; they do not reconcile with the printed totals) |
| 28 | 28 | Self-catering at 17.4% and guesthouses at 9.7% lead accommodation choice, ahead of hotels at 3.6% (p27). | Self-catering at 17.4% and guesthouses at 9.7% lead accommodation choice, ahead of hotels at 3.6% (p27); together these shares cover under a third of respondents. |
| 93 | 94 | The only accommodation figure in hand is a demand share: 3.6% of 2024 visitors stayed in hotels, against 17.4% in self-catering (Current State Diagnostic, Dec 2025, p27). | The only accommodation figure in hand is a demand share from the 2024 visitor survey: 3.6% of respondents named hotels a ... le (Current State Diagnostic, Dec 2025, p27). |
| 30 | 30 | Cape Town hotel occupancy was 53% in June 2023 (Demand-Side Analysis, Jun 2026, p34). | Cape Town hotel occupancy was 53% in June 2023 (Demand-Side Analysis, Jun 2026, p34). [Open item: Wesgro Research to supply June 2025 occupancy.] |
| 55 | 56 | Kenya earned about US$1,650 per visitor in 2024 by building conservation and community participation into one governed product system (p32, p33). | Kenya earned about US$1,460 per visitor in 2024 (Demand-Side Analysis, Jun 2026, p15) by building conservation and commu ... bal Benchmarking Report, Mar 2026, p32, p33). |
| 56 | 57 | Kenya: about US$1,650 per visitor | Kenya: about US$1,460 per visitor |
| 56 | 57 | p32, p56 | p32, p56; DSA p15 |

### M13: Done, one sentence omitted for the D1 skip

ES opening replaced by the three paragraphs, except the sentence "The base path is the plan's target and the accelerated path its stretch.", omitted because D1 is on the skip line. The doubling mandate stays in section 1.1. Tone rows applied; the FA16 topline matches in both places.

| v1 page | v2 page | Before | After |
| --- | --- | --- | --- |
| 13 | 13 | The Western Cape can grow international arrivals from about 1.5 million in 2025 to between 2.2 million and 2.5 million b ... Y25/26 (Demand-Side Analysis, Jun 2026, p11). | The Western Cape can grow international arrivals from about 1.5 million in 2025 to 2.2 million by 2035 on the base path, ... should do and how progress will be measured. |
| 32 | 32 | The Diagnostic records specific dysfunctions, "SAT is in turmoil" among them, and the added pressure of a lack of fiscal space (Current State Diagnostic, Dec 2025, p58). | Stakeholders described strain at SA Tourism and a lack of fiscal space (Current State Diagnostic, Dec 2025, p58). |
| 17, 104 | 17, 105 | and the national marketing body is weak, so the province needs one shared agenda with clear decision rights. | and the national marketing body is under strain, so the province needs one shared agenda with clear decision rights. |
| 17 | 17 | and the national marketing body is weak, so the province needs one shared agenda with clear decision rights. | and the national marketing body is under strain, so the province needs one shared agenda with clear decision rights. |

### P1: Done

Rows I6 to I11 existed in the source. The cause was rendering: the table's header row fell alone at the foot of v1 p147, and LibreOffice then dropped the rows after it. Fix in helpers.js: the header row is kept with the first body row. A row check over every table in v1 found Table 5.2 the only one affected; in v2 every row of every table is in the PDF text.

### P2: Done

The Figure 1.4 note now ends the figure's source line, wording kept.

| v1 page | v2 page | Before | After |
| --- | --- | --- | --- |
| 34 | 34 | chart footnote: The model prints only these six year points and no seat table beneath the 1.8m line, so the crossing fal ... as 2035 end points only and are not plotted. | Market Assessment Report, May 2026, p20 (base case by year from a 2025 base of 1,498,829; the 2028 to 2035 points are id ... as 2035 end points only and are not plotted. |

### P3: Done

charts.js lineChart gains a timeAxis option that places each year point at its calendar distance (2025 to 2035); points, labels, colours and y-axis unchanged. The ES.2 and 5.2 spacing note is removed.

| v1 page | v2 page | Before | After |
| --- | --- | --- | --- |
| 18, 34, 44, 152 | 18, 34, 45, 154 | evenly spaced year points | exec/01_summary.json: footnote removed ("Milestone years only; the intervals are three, three and four years."); exec/01 ... 4: x positions on calendar years 2025 to 2035 |

### P4: Done

The labels were cut in the chart data itself, not only by the renderer. Full names restored from the section 4.3 charter titles, and ganttChart wraps a long name to two lines (rows grow from 44 to 54px).

| v1 page | v2 page | Before | After |
| --- | --- | --- | --- |
| 118 | 119 | labels cut short in the data | I1: "Segment-led activation and yield in" to "Segment-led activation and yield in mature markets"; I2: "Green-season eve ... ta-sharing protocol and visitor intelligence" |

### P5: Done

Both items moved, wording kept. Section 1.5 has no open-items list, so they close section 1.5 as bracketed items.

| v1 page | v2 page | Before | After |
| --- | --- | --- | --- |
| 13 | 42 | [Summary of Findings, 14 Oct 2026, slides 3 and 4: align these five constraints with the deck's own list once the deck i ... ce to be confirmed] (Figure ES.1 source, p14) | [Summary of Findings, 14 Oct 2026, slides 3 and 4: align these five constraints with the deck's own list once the deck i ... 5 to 16: deck page reference to be confirmed] |

### P6: Done (closed by C6.1)

### P7: Done

Table A.4 prints +323,805 and the sentence about the misprint is removed (logged in reconciliation_log.md under C5). The rest of that note is unchanged (see Seen, not changed).

| v1 page | v2 page | Before | After |
| --- | --- | --- | --- |
| 163 | 165 | +328,805 | +323,805 |
| 163 | removed | The May deck prints Conservative absolute growth of +328,805, but its own end points give +323,805; its 10-year CAGRs do ... ed; Market Assessment Report, May 2026, p19). | (deleted) |

### P8: Done (closed by C1.3)

### P9: Done

p34 sentence inserted. At p48 the paragraph has no separate source note, so "Other study documents count new routes from 2014 on a different basis." takes the place of the deleted C5 sentence.

| v1 page | v2 page | Before | After |
| --- | --- | --- | --- |
| 34 | 35 | and the network averaged 76.0% on the printed total (MIDAS Aviation Market Assessment, Mar 2026, "Seasonality"). | and the network averaged 76.0% on the printed total (MIDAS Aviation Market Assessment, Mar 2026, "Seasonality"). MIDAS t ... November 2025; 29 serve the airport in 2026. |

### P10: Done (closed by C6.4)

### P11: Done

| v1 page | v2 page | Before | After |
| --- | --- | --- | --- |
| 169 | 170 | New Zealand, Auckland Park | New Zealand |

### P12: Done

| v1 page | v2 page | Before | After |
| --- | --- | --- | --- |
| 170 | 172 | formalise conservation and community inclusion as part of the tourism value proposition | build conservation and community inclusion into the tourism value proposition |
| 170 | 172 | shortened only by cutting | shortened by cutting, with one verb paraphrased |

### P13: Blocked

Investigated, not changed. No forced page break sits after Figure 2.1. The space is left by the next figure (Figure 2.2), which is too tall for the rest of the page and moves whole, because its image is kept with its caption and source. Removing that setting would split a figure from its caption, and the brief rules out moving content. In v2 the same gap falls on p45, and p44 now ends about a third empty because Figure 2.1 moved down. Options for Michael: allow Figure 2.2 at a smaller width, or let a paragraph move ahead of it.

### P14: Done (closed by C5)

### P15: Done

| v1 page | v2 page | Before | After |
| --- | --- | --- | --- |
| 73 | 74 | The 2025 ICCA row of 65 covers Stellenbosch and Cape Town and is not comparable. | The 2025 ICCA row of 65 covers Stellenbosch and Cape Town and is not comparable. [Open item: Wesgro Convention Bureau to ... y total of 137 with the 136 monthly records.] |

### P16: Done

| v1 page | v2 page | Before | After |
| --- | --- | --- | --- |
| 182 | 184 | building on the 2024 Ghana visa waiver | building on the Ghana visa waiver of November 2023 |
| 83, 183 | 84, 185 | building on the 2024 Ghana visa waiver | building on the Ghana visa waiver of November 2023 |
| 110 | 111 | The 2024 Ghana visa waiver drove 36,656 arrivals to South Africa | Ghanaian arrivals reached 36,656 in 2024, the first full year of the visa waiver that took effect on 1 November 2023 |

### P17: Done

| v1 page | v2 page | Before | After |
| --- | --- | --- | --- |
| 182 | 184 | Escalate the cap on US carriers, the unsigned Open Skies agreement and the bilateral agreements that limit airlift | Escalate the cap on US carriers, the absence of an Open Skies agreement and the bilateral agreements that limit airlift |
| 81, 182 | 82, 184 | Escalate the cap on US carriers, the unsigned Open Skies agreement and the bilateral agreements that limit airlift | Escalate the cap on US carriers, the absence of an Open Skies agreement and the bilateral agreements that limit airlift |

### P18: Done

All ten occurrences changed: the first body mention (p58, with the date), p60 and the eight others.

| v1 page | v2 page | Before | After |
| --- | --- | --- | --- |
| 58 | 60 | National Treasury Circular 131 | National Treasury's MFMA Circular No. 131 of 31 March 2025 |
| 60 | 61 | National Treasury Circular 131 | MFMA Circular No. 131 |
| 159 | 161 | Treasury Circular 131 | MFMA Circular No. 131 |
| 182 | 184 | Treasury Circular 131 | MFMA Circular No. 131 |
| 17, 100 | 17, 101 | Treasury Circular 131 | MFMA Circular No. 131 |
| 100 | 101 | Treasury Circular 131 | MFMA Circular No. 131 |
| 17, 58, 60, 100 and more | 17, 60, 61, 101 and more | Treasury Circular 131 | MFMA Circular No. 131 |
| 17, 58, 60, 100 and more | 17, 60, 61, 101 and more | Treasury Circular 131 | MFMA Circular No. 131 |
| 146 | 147 | Treasury Circular 131 | MFMA Circular No. 131 |
| 17 | 17 | Treasury Circular 131 | MFMA Circular No. 131 |

### P19: Done

Paragraph, Table 1.2 row (figure, source, open item) and the Table 1.2 source list changed. The Hypertext row stays in the A9 sources table (M11 cites it). The 106,707 Cape Town jobs figure is unchanged.

| v1 page | v2 page | Before | After |
| --- | --- | --- | --- |
| 25 | 25 | about 1.5 million international tourist arrivals in 2025, an 11.1% increase (Hypertext, Apr 2026, reporting the Provincial Minister; public source) | 1,538,142 international tourist arrivals in 2025, an 11.1% increase (Wesgro Research, Western Cape Tourism Performance: Annual 2025, from SA Tourism data; public source) |
| 25 | removed | [Wesgro Research to confirm the 2025 SAT figure and the series behind it.] | (deleted) |
| 25 | 25 | About 1.5m | 1,538,142 |
| 25 | 25 | Hypertext, Apr 2026, reporting the Provincial Minister; public source | Wesgro Research, Western Cape Tourism Performance: Annual 2025; public source |
| 25 | 25 | Hypertext, Apr 2026, reporting the Provincial Minister; public source | Wesgro Research, Western Cape Tourism Performance: Annual 2025; public source |
| 25 | removed | [Wesgro Research to confirm the figure and its series] | (deleted) |

### P20: Done

| v1 page | v2 page | Before | After |
| --- | --- | --- | --- |
| 100 | 101 | De Rust's pass-through trade cut | De Rust's pass-through trade cut; a temporary one-lane reopening is targeted for December 2026 |
| 100 | 101 | SCIP p24 | SCIP p24; Western Cape Government, Jul 2026 |

### Sources: Done

Nine rows added after the existing public sources, before the SLA row; the brief's "Type" is the table's Status column. Table A.33 title now counts fifteen public and reference sources and the A9 lead twenty-eight documents.

| v1 page | v2 page | Before | After |
| --- | --- | --- | --- |
| new | 192 | (insert) | Western Cape Tourism Performance: Annual 2025 / Wesgro Research (SA Tourism data) / 2026 / Public source |
| new | 193 | (insert) | Q1 2026/27 performance presentation to the Portfolio Committee on Transport, as reported by Travel News / ACSA / August 2026 / Public source |
| new | 193 | (insert) | Parliamentary reply on Cape Town International runway capacity / Minister of Transport / April 2025 / Public source |
| new | 192 | (insert) | Anuario de Turismo 2024 / Sernatur, Chile / December 2025 / Public source |
| new | 193 | (insert) | Singapore achieves historical high in tourism receipts in 2024 / Singapore Tourism Board / February 2025 / Public source |
| new | 193 | (insert) | World Tourism Barometer / UN Tourism / January 2025 and January 2026 / Public source |
| new | 193 | (insert) | George Airport expansion reporting / George Herald / July 2026 / Public source |
| new | 193 | (insert) | Meiringspoort temporary reinstatement / Western Cape Government / July 2026 / Public source |
| new | 193 | (insert) | Kenya 2024 tourism performance, as reported / The Star (Kenya) / May 2025 / Public source |
| 190 | 192 | Twelve study documents, six public and reference sources and one deck not yet in hand support the report. | Twelve study documents, fifteen public and reference sources and one deck not yet in hand support the report. |
| 190 | 192 | nineteen documents | twenty-eight documents |

## Consequential edits

Each was forced by a named change and is logged under its parent ID.

| Parent | v1 page | v2 page | Before | After | Why |
| --- | --- | --- | --- | --- | --- |
| C4.1 | 47 | 48 | DSA: Demand-Side Analysis, Jun 2026. | DSA: Demand-Side Analysis, Jun 2026. Diag: Current State Diagnostic, Dec 2025. | Table 2.2 source key gains "Diag", which the new source cell uses. |
| C4.3 | 149 | 151 | Wesgro ratio; Stats SA TSA | Labour analysis (I18); Stats SA TSA | Table 5.4, T1-04 Source cell named the ratio the change removes. |
| C4.3 | 154 | 156 | Eleven data gaps stand between the plan and a full baseline | Ten data gaps stand between the plan and a full baseline | Table 5.9 title count after the row deletion. |
| C4.3 | 23 | 23 | Carried to Chapter 5 as a ratio-based projection, pending the labour analysis the strategy commissions | Carried to Chapter 5 with its baseline set by the labour analysis the strategy commissions | Table 1.1 (p23), found by the "ratio-based" grep; worded as the brief words p113. |
| C4.3 | 20 | 20 | Arrivals and jobs carry targets on both paths, while season, spread and community spend start from dated baselines. | Arrivals carry targets on both paths, while jobs wait on the labour analysis and season, spread and community spend start from dated baselines. | Table ES.6 title: jobs no longer carry targets. |
| C4.3 | 152 | 154 | Arrivals and jobs carry targets on both paths; spend carries the working analysis's base path; the other Tier 1 indicators carry dated baselines first. | Arrivals carry targets on both paths; spend carries the working analysis's base path; jobs and the other Tier 1 indicators set baselines first. | Table 5.7 title (the brief's Table 5.6): jobs no longer carry targets. |
| C4.3 | 152 | 154 | The arrivals targets come straight from the growth model, the jobs targets from a stated ratio, and the other Tier 1 targets wait for baselines that do not yet exist. | The arrivals targets come straight from the growth model, while the jobs and other Tier 1 targets wait for baselines that do not yet exist. | Section 5.3 topline: the jobs ratio is removed. |
| M2 | 35 | 35 | so the comparator range runs from about 4% to 35%. | so the comparator range runs from about 4% to 40%. | p35: the range end follows Chile's corrected 40.4% in the sentence before. |
| M2 | 54 | 55 | Kenya (range midpoint) | Kenya | Figure 2.5 category label: 14.6 is no longer a range midpoint. |
| M2 | 54 | 55 | Global Benchmarking Report, Mar 2026, p7 (global rate, UN Tourism World Tourism Barometer, January 2025) and p9 (compara ... t: Kenya 12.8% to 14.6%, Valencia 13% to 14%. | Global Benchmarking Report, Mar 2026, p9 (comparators); Sernatur, Dec 2025 (Chile); Singapore Tourism Board, Feb 2025 (S ... bar shows its midpoint: Valencia 13% to 14%. | Figure 2.5 source note follows the new bar values. |
| M7 | 147 | 150 | T2-10 routes above 80% load | T2-10 seats added on full routes | Third match of the find, in Table 5.2 (p147), which the brief does not list; the indicator is renamed there to match. |
| M11 | 146 | 147 | Ten risks could move the plan off its path | Fourteen risks could move the plan off its path | Table 4.7 title count. |
| M11 | 146 | 148 | Current State Diagnostic, Dec 2025 (Diag); Stakeholder Insights Report, Mar 2026 (SIR); | Current State Diagnostic, Dec 2025 (Diag); Demand-Side Analysis, Jun 2026 (DSA); Stakeholder Insights Report, Mar 2026 (SIR); | Table 4.7 source key gains "DSA", which two new rows cite. |
| C6.4 | 144 | 145 | font-size="20" on the Steerco label | font-size="17" on the Steerco label | Figure 4.3: the longer co-chair label (610px at 20px) overflowed its 560px box; set at 17px so it fits. Box, position and colours unchanged. |

## Sweeps

Pages in this section and the next are v2 pages.

**C1.1, "ceiling".** After the table, 15 hits remain in the content modules. None refers to the seat line outside a quotation:

- Quotations kept verbatim: "a hard ceiling at 1.8 million inbound seats" (2.1, p46) and the A2 quotation of both decks (p167).
- Water: the "hard ceiling" water scarcity sets on visitor load (1.2, p32, a quotation; 3.3.2, p111).
- The airport or runway, not the seat line: "Cape Town International itself is now the physical ceiling" (p30), "they set the ceiling the airlines fly into" (p49), Table 2.4 row "Airport is the ceiling" (p53) and the Pillar 2 topline "Supply sets the ceiling on the growth case" (p85).
- The model's lever names as the deck prints them: "the airlift ceiling" (p43) and "an airlift capacity ceiling" (p164); "Source-market growth sets the ceiling" (p164) is a different ceiling.
- Other meanings: "market, seasonality and spread ceilings" (Pillar 1 objective, p71), "a capacity ceiling" for a community site (A5, p180), and the internal figure id `fig_base_case_seat_ceiling`, which never prints.
- Changed under the rule (Sweep rows above): "the case stops at the ceiling" (3.4) and "when the ceiling binds" (4.2).

**C4.1, "65%".** All ten "65%" strings in v1 meant the October to March share, and all ten are changed (C4.1 detail). The only "65%" in v2 is "65% to 72% load" in the new C2 text (p18). The Doha 65.2% load factor (p79) and p28's 61% are untouched.

**C4.3, jobs.** "two jobs", "ratio-based" and "30,000 jobs": no hits left. The India and China "about 30,000" traveller figures are untouched. Four mentions of the jobs ratio remain outside the brief's terms (see Seen, not changed).

**C5.** Every sweep term was searched. Hits outside the known instances: "typo" (a false match on "typology", p67) and "do not reproduce" in the FA6 source note and Table A.1, both the Nigeria and Ghana caveat the brief keeps. "Plan decision", "Michael", "agreed structure", "agreed report structure", "house style", "misprint", "appear nowhere", "do not follow the stated weights", "reconciliation", "discrepanc", "logs the" and "this report logs" have no hits left.

**M1 (skipped), "goal" near 2.5 million.** Three statements name 2.5 million as the goal and are kept: decision 1 (ES, p20), section 1.1 ("it is the goal the report carries", p23) and the Table 1.1 row "Growth to 2.5 million" (p23). Two other "goal" hits concern jobs (FA20 and A1).

**C6.1, decision numbers.** No "Decision N" cross-reference existed in v1. The one in v2 is the new M11 row, which cites Decision 3 on the new numbering.

**M11, risk counts.** No "ten risks" or "ten material risks" outside 4.8; the Table 4.7 title count is updated (Consequential).

## Seen, not changed

Noticed while working; not named in the brief, so left exactly as they are.

1. Table 1.3 row label "2025 (provisional)" (p30): the row's October to March cell is now the normalised 62%.
2. Section 1.5, "The five-market share, printed as both 63% and 61% on one slide, is one case ... Nothing is averaged and nothing is reconciled silently." (p42), and Table 2.2 "top five 63% (61% in the slide text)" (p48): both report the slide conflict C5 removed at p28, but neither matches a sweep term.
3. Section 1.5, "Four cover dates differ from their file dates ..." (p41): the same point as the 1.4 sentence C5 deleted.
4. Internal-record wording outside the sweep terms: "the difference is logged" (1.4, p38) and "No document in hand records why, and the change is logged." (2.3, p54).
5. A2 note on the June deck's printed CAGRs against its end points (p165): an erratum left after the P7 sentence was removed.
6. Table 3.9 source note: "76.0% is the printed network total and the 27 rows sum to 75.0%" (p86).
7. Table 2.7 row "Growth above the norm is designed" (p57): the new cell cites the world 11% and the corrected Chile and Singapore figures, but its Pages cell still reads "p7, p8, p9".
8. The jobs ratio outside the C4.3 terms: the FA20 action and its A7 copy ("obtain the method note for the jobs-per-passenger ratio", pp114, 189), two I18 charter rows ("the method note for the jobs ratio obtained"; "the jobs indicator moved from the ratio to a provincial measure", p139), and the A9 source "Air access releases: jobs and spend per 100 international passengers" (p193), which no passage now cites.
9. Section 5.3 opens its second jobs paragraph with "The report restates the 300,000 ..." (p155) now that the sentence that introduced the 300,000 is removed under C4.3.
10. D2 against older wording: the I15 charter Dependencies "DEDAT and Cape Town Tourism as standing members" (p136), section 4.4 "DEDAT is a standing member of Steerco" (p141) and the FA16 recommendation "A Tourism Growth Steerco at Wesgro CEO level, with DEDAT and Cape Town Tourism" (p106).
11. D9 against older wording: Table 3.9 row label "Second gateways" (p86) and the I6 charter Expand row "growth at George" (p127).
12. Table 3.1 cell for FA2, "international meetings cluster from May to November" (p71), close to the topline M4 rewrote.
13. A6 source note "The deck does not print the number 16." (p181).
14. Table 4.7's narrow columns break "Likelihood" and "Medium" mid-word (pp147 to 148), as in v1.
15. The Pillar 2 topline "Supply sets the ceiling on the growth case." (p85) keeps the supply-first thesis that C2 narrowed elsewhere.
16. `report/open_items.md` and `report/discrepancies.md` are outside the report and were not updated for v2: open item 3 (the deck's basis for 16) left the report under C5, and v2 adds new open items (C1.2, C3, C4.2, M2, M5, M6, M7, M8, M9, M12, P15).
