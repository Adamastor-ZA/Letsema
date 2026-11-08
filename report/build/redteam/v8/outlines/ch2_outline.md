# Chapter 2 v8: outline

Chapter title: **Analysis and insights** (apply_v8.py sets it in ch2_analysis.js, smoke_test.js and qa_structure.py).

Four drafts replace the six v7 modules. Each is a JSON draft in `redteam/v8/drafts/` in the format `check_v8_draft.py` reads; run it on all four with `--chapter2`.

| Part | Draft | Module | id | title (h2 text is "2.n " + title) | Budget |
|---|---|---|---|---|---|
| Intro + 2.1 | ch2_1.json | ch2/01_benchmarks.json | 2.1 | Global benchmarks and their lessons | 210 + 1,850 |
| 2.2 | ch2_2.json | ch2/02_demand.json | 2.2 | Demand-side factors | 1,760 |
| 2.3 | ch2_3.json | ch2/03_supply.json | 2.3 | Supply-side factors | 2,600 |
| 2.4 | ch2_4.json | ch2/04_enabling.json | 2.4 | The enabling environment | 2,020 |

Budgets count what the checker counts as new prose (p, lead, h2, h3 and box text, citations, footnote notes and open items included; refs excluded). Total about 8,440 against 8,988 in v7 on the same count. The 1,108 words of deliverable method, SLA clauses and versioning that leave the chapter (see the allocation file) and the merged repeats are partly offset by about 600 words, net of merged repeats, that the rules add back: 91 short-form citations written in full (about four words each), footnote notes that carry relocated detail, and an implication sentence per h3 plus a closer per part. The per-h3 figures below sum to each part's budget; a draft more than 10% over a part budget should cut repetition, not findings. Every finding, figure, table and open item stays.

Block references below are `module [index]`, with modules shortened to ch2/01 (demand), ch2/02 (aviation), ch2/03 (benchmarking), ch2/04 (stakeholders), ch2/05 (infrastructure) and ch2/06 (inclusion). `ch2_allocation.json` holds the full block map: "parts" are a draft's `sources`, "split" entries are `partial_sources` of each draft they name, and "relocations" go in one draft's `relocations`.

## Rules every drafter holds

- **No deliverable named in the text.** That rules out "MIDAS expects", "the deck", "the report's summary", "Skift's survey", "the plan treats" and "the aviation report". It also rules out a deliverable by description ("the December baseline", "the March report", "the benchmarking work"), which the checker does not catch. Write the finding in the province's terms and let the citation carry the source. "The survey" or "the model" alone is fine. The organisations that gave stakeholder insights are named; that is evidence, not a call-out.
- **Each h3 argues.** It opens on its claim, gives the evidence and ends on what the evidence means for the Western Cape, in one sentence. Each part ends on a one-sentence closer that says what its pillar must do, then its box.
- **Appendix tables by caption, not number.** The s11 draft moves a table into Appendix A2, so every appendix table from A.9 on renumbers. Point to an appendix table by appendix and caption, e.g. "(Appendix A5, 'Community shortlist criteria')", never "(Table A.18)".
- **Citations in full**, e.g. (Demand-Side Analysis, Jun 2026, p55). The v7 blocks are full of short forms such as (p14) and ("Seasonality"); every one is rewritten in full in new prose or the checker fails it.
- **Footnote notes** follow the source after a semicolon, start lowercase, run to four words or more and hold no semicolon of their own. A note that starts with a capitalised name ("Melbourne's 4.3% ...") falls back into the text, so start it "the 4.3% for Melbourne ...".
- **Every number in an absorbed block survives** in the draft, in text, citation or footnote note, page numbers included. Figures and tables are carried as `ref` blocks. A computed figure keeps "computed" in its parenthesis.
- **Open items word for word.** Chapter 2 holds eleven; where each goes is listed under its part, and the SLA item under Relocations.
- **No v7 section numbers.** "section 2.5" and "section 2.6" must not survive (apply_v8.py stops on them). Cross-references point to the new 2.1 to 2.4 or to Chapters 1, 3 to 5.
- **Two quotes carry en dashes** in v7: "Public–Private Air Access Fund" (ch2/03 [16]) and "public–private structure led by Visit València" (ch2/03 [20]). Write them with a hyphen, as Appendix A3 already does.
- **Lessons recalled in a phrase.** 2.2 to 2.4 may recall a 2.1 lesson in a clause with "(section 2.1)"; they do not retell the case.
- **Stakeholder statements** are the project team's paraphrases, attributed to organisations, never to people. The first stakeholder citation in 2.3 and in 2.4 may carry the note "; insights are the project team's statements, attributed to the organisation engaged".
- House style: UK English; no em or en dashes; no Oxford comma; sentences of 15 to 25 words, never above 35; topic sentence first; inline enumeration for two to four points; no banned words or intensifiers.

---

## Chapter introduction (three short paragraphs before the 2.1 h2, in ch2/01_benchmarks.json)

The two-sentence introduction, as the first paragraph:

> This chapter sets out what the analysis found, in four parts that together build the case for the strategy in Chapter 3. Section 2.1 draws lessons from comparator destinations; sections 2.2, 2.3 and 2.4 then examine demand, supply and the enabling environment, on which Pillars 1, 2 and 3 rest.

Paragraph 2, the argument in brief (about 60 words). Demand is not what holds the province back. Seats at the peak, product beyond the Metro and the institutions that hold both are. The fastest-growing comparators organised around their binding constraint; the three parts that follow locate the Western Cape's.

Paragraph 3, how the evidence is used (about 110 words with its citation, note and open item). Sources from ch2/04 [5] and the open item from ch2/04 [22].
- "Stakeholder evidence runs through every part. In all, 16 organisations, from Mossel Bay to the CTICC, contributed 223 rated insights, 115 rated High, 102 Medium and 6 Low (Stakeholder Insights Report, Mar 2026, p4, p17, p20 to p46, counted; the first of four engagement phases ran from January to March 2026)." The engagement phases ride in the note; Appendix A6 holds the rest.
- One sentence: each statement is the project team's paraphrase, attributed to the organisation that made it. Then, word for word: **[Open item: each organisation named here to approve its paraphrase before publication.]** "Named here" now reads as "named in this chapter", which is what the approval needs, because the eight paraphrases it covered in v7 now sit in 2.3 and 2.4.
- One sentence: each part closes with a box, "What this means for the strategy", that says what its evidence does to the focus areas: Validates, Rewords, Refines, Supports or Supplies precedent for.

---

## 2.1 Global benchmarks and their lessons (ch2/01_benchmarks.json; about 1,850 words)

Feeds all three pillars. Thesis: the fastest growers fixed their binding constraint first and built one system around it; the Western Cape's constraint is seats into one gateway, and in its communities it is the missing seller. Each h3 states a lesson, shows the case and ends on the change it asks of the Western Cape, so the six changes are told once, where their evidence sits, and need no closing list (Appendix A3's table "Transferable levers by case" holds all twelve levers in the source's words).

**Lead.** "The destinations that grew fastest ran institutions, marketing and air access as one system aimed at a single binding constraint. For the Western Cape that constraint is seats into one gateway; in its townships and rural settlements it is the lack of a local seller." (ch2/03 [1], ch2/06 [16])

**Opening paragraph (about 130 words), method and the bar.** ch2/03 [5], [6], [9].
- Method, two sentences, no deliverable named. The six comparators (Chile; Melbourne and Victoria; Valencia; Singapore; Kenya; Auckland and New Zealand) came from a screen of 30 destinations against 12 criteria in four groups (market and access; destination and product structure; growth and inclusion; performance). Each was read for its demand profile, two proven growth levers and how far they transfer. Footnote notes on that citation: "an earlier baseline had proposed adding Namibia and Kenya, and the final set kept Kenya only" (with Current State Diagnostic, Dec 2025, p62; from relocated ch2/03 [7]). Also: "examples from outside the set are cited as public sources and labelled as such".
- The bar: growth of 3% to 5% a year is the norm under stable conditions, above 5% marks structural acceleration and 10% or more a structural shift. UN Tourism puts 2024 at 11%, a recovery year, and 2025 at about 4%. Growth counts as structural only when it is "driven by deliberate changes to demand drivers, access conditions or product systems, rather than cyclical recovery or short-term promotion".

### Structural growth is rare, even among the leaders
Against 11% global growth in 2024, only Chile (40.4%) and Singapore (21%) grew at two to four times the world's rate. Kenya (14.6%), Valencia (13% to 14%) and New Zealand (about 12%) ran slightly ahead, and three of the six were still below 2019. Implication: the Western Cape should measure itself against deliberate, structural growth, not against recovery. Footnote note on the growth sentence: "the 4.3% for Melbourne is an Australia-wide forecast of average annual growth, and New Zealand's 12% matches its 2025 holiday-arrivals growth, with total arrivals up 5.9%".
- Draws on: ch2/03 [11]; ref ch2/03 [12] (table "Comparator growth and recovery") after the first paragraph; ch2/03 [13] open item **[Open item: add one comparator that underperformed, as the Inception Report's plan asked (Inception Report, Nov 2025, p16).]** directly after the table; ref ch2/03 [14] (figure "Comparator growth, 2023 to 2024") to close the h3. About 220 words.

### Cape Town already wins more routes than its peers
Against eight secondary airports chosen for peripheral geography and inbound tourism (Calgary, Christchurch, Edinburgh, Keflavik, Larnaca, Marrakech, Santiago and Valencia), Cape Town added 17 mainline international services between 2015 and 2025, more than Santiago (14), Valencia (12) or Calgary (8). Yet winning routes is not the same as holding seats through the winter, and the comparators that grew fastest did more than win routes. The pivot leads into the next h3; 2.3 shows that the routes now run full.
- Draws on: ch2/02 [7] (the eight; the note that the aviation assessment is cited by section can drop, since section 1.4 [17] says so); ch2/02 [10], comparator half (footnote note: "other study documents count new routes from 2014 on a different basis"). About 110 words.

### The leaders treat air access as infrastructure
Chile concentrated access on Santiago, which handles about 90% to 95% of 5.2 million international arrivals (airport traffic from about 16 million passengers in 2010 to more than 26 million in 2019). A 2015 concession funded about US$900 million of expansion under open-skies agreements. New Zealand "shifted from awareness-driven marketing to route accountable demand generation": it tied budgets to long-haul corridors, designed campaigns around airline breakeven and shoulder-season loads and reports more than 16,000 incremental bookings and about NZ$55 million in return in 2023/24, with early route incentives and data shared with airlines. The changes they ask of the Western Cape, as inline enumeration: treat air access as "core economic infrastructure, not a tourism add-on", with a permanent public-private air access fund; lobby for air service liberalisation and simpler visas; ring-fence marketing budgets to priority long-haul corridors, with an aviation partnership framework and early-stage route support.
- Draws on: ch2/03 [15], [16], [17]; ch2/03 [24] (the Chile and New Zealand sentences, p28, p56). About 260 words.

### Transit and events can be turned into demand
Singapore turns transit into visits through a stopover programme run "under a coordinated strategy" by the tourism board, Changi Airport Group and Singapore Airlines: 16.5 million visitors in 2024, 21% up, and record receipts of about S$29 billion. Kenya made Nairobi East Africa's aviation, diplomatic and business hub, and its main airport now carries 68% of arrivals. Melbourne curates events that "generate repeat, predictable demand spikes across the year" and uses its calendar to de-risk aviation demand, with hotel stock up 21%, about 5,000 rooms. The changes: one event acquisition and calendar strategy across Wesgro, the Convention Bureau, the City and the Province, with conference bidding aligned to sector strengths; MICE treated as a system lever, with city, provincial and national actors aligned on one gateway strategy; government, aviation, events and industry working to shared KPIs under a province-wide quality and standards framework led by Wesgro. Implication: the Western Cape has the hub traffic and the green-season gap to apply all three.
- Draws on: ch2/03 [18], [19]; ch2/03 [24] (the Melbourne sentence, p20) and [25] (the Singapore sentence, p42, and the first two clauses of the Kenya sentence, p35). About 260 words.

### Quality and value are governed, not encouraged
Valencia put a destination-wide quality system under "a permanent public-private structure led by Visit València" and grew to 3.5 million international visitors in 2024, 13.9% up on 2023 and 24.4% above 2019. New Zealand manages regional capacity to protect price and recommends that destinations "replace arrival growth with yield-based regional performance metrics". Kenya earned about US$1,460 per visitor in 2024 by building conservation and community participation into one governed product. The changes: a provincial quality charter phased by district, with certification visible on booking platforms and standing sector councils for wine, MICE, adventure and culture; yield, not arrivals, as the regional measure; conservation and community inclusion built into the offer. Implication: quality, price and yield are managed outcomes, not by-products of volume.
- Draws on: ch2/03 [20], [21]; ch2/03 [25] (the Valencia sentence, p49, and the last clause of the Kenya sentence, p35). About 220 words.

### In communities, sellers outlast programmes and capital
Five cases test what lasted. In Santa Marta in Rio de Janeiro, about 20 resident guides ran the tours by 2015 and outside jeep firms had left: access and safety are preconditions, not product, and resident sellers outlast programmes. Medellín's Comuna 13 drew 1.98 million visitors in 2025, 52% international, with about 300 professional guides, though carrying limits came late. Vilakazi Street's ten restaurants employ more than 800 people, but benefits concentrate on street-front owners. Costa Rica's network turned over more than USD 800,000 in 2013 and dissolved at the end of 2018 after donors left. Kliptown received a first allocation of R436 million, was projected to draw almost 200,000 international visitors a year and drew about 4,000 museum visitors a year by 2017. The order that works: "a seller with a stake, a safe and workable visit, product that keeps spend in the community, then exposure". Implication: in the communities, the seller comes before the asset (2.4 applies it).
- Draws on: ch2/06 [8] sentence 3 (split), [16], [17], [18], [19]; merge the twice-told Kliptown and Costa Rica figures into one telling. About 240 words.

### The system matters more than any lever
Growth comes from "a coordinated destination system in which governance, demand generation and access reinforce one another", and Chile's worked best "when anchored around a single strategic constraint", long-haul access. Yet coordination is hard everywhere: Victoria's national and state bodies clash over roles and branding, Valencia struggles to join its data across institutions and Kenya's collaboration between government, industry and financiers is "mixed". The Western Cape's constraint has Chile's shape, seats into one gateway airport. Summative closer (one sentence, the part's closer): the common thread is order, the binding constraint first and the seller before the asset.
- Draws on: ch2/03 [22], [23]. The opening sentence of ch2/03 [24] ("Each comparator's lesson translates into a change ...") drops: each change now closes its own h3, and its pages (p20, p28, p35, p42, p49, p56) ride in those h3s' citations. About 150 words.

**Box "What this means for the strategy"** (from ch2/03 [26], finding numbers dropped, plus one line; about 170 words):
1. **Supplies precedent for FA07, Win direct routes and add seats on full routes, and FA15, Crowd in capital with targeted investment strategies.** Chile's airport concession and air access fund; New Zealand's route-tied marketing.
2. **Supplies precedent for FA04, Convert India and China hub traffic.** Singapore's stopover conversion and Kenya's hub strategy.
3. **Supplies precedent for FA02, Create green-season demand with MICE and events.** Melbourne's events-led system and unified calendar.
4. **Supplies precedent for FA11, Align visitor experience in-destination, and FA03, Make the whole province findable and bookable.** Valencia's governed quality and certification visible on booking platforms.
5. **Supplies precedent for FA05, FA12 and FA14.** Yield-based metrics, capacity discipline and conservation-led product.
6. **Supports FA16, FA17 and FA18.** One coordinated system of governance, marketing and access, with shared data between tourism bodies and airlines.
7. **Supplies precedent for FA13, Embed local destination bodies for community inclusion.** Resident sellers outlasted the programmes that launched them, and capital built before an operator, as in Kliptown, earned no operating income. Keep this line: the benchmark cases that v7 ch2/06 [26] item 1 cited (finding 5) now sit in 2.1, and 2.4's FA13 line keeps the rest of that item's evidence.

---

## 2.2 Demand-side factors (ch2/02_demand.json; about 1,760 words)

Feeds Pillar 1 (FA01 to FA06). Thesis: interest is there; concentration, the calendar and conversion are the problem. Word budget: lead 45, opening 70, h3s 1,430, closer 40, box 115, headings 60.

**Lead.** "Interest in the Western Cape is broad and growing. Yet demand is concentrated in five markets and six months. Its growth markets fly in through other carriers' hubs and book on platforms where Western Cape product is hard to find." (ch2/01 [1]) The chapter introduction already says "Demand is not what holds the province back", so the lead does not repeat it.

**Opening paragraph (about 70 words), method.** ch2/01 [8]. A 2025 survey of more than 25,000 travellers in 34 outbound markets, 17 of them Wesgro priority markets, with 800 to 1,600 respondents in each; desk review of Wesgro, Statistics South Africa and Google search data; more than 20 market-facing discussions. Two sentences.

### Five markets carry the province and pay most
The UK, Germany, the USA, the Netherlands and France supplied 63% of overseas arrivals in 2025, and the first three alone 52%. The pattern is not new: the same five held 61% of Cape Town overseas air arrivals from January to August 2024. The same markets pay most, from R32,900 a visitor for the USA and R26,500 for the UK down to R8,600 for Namibia and R8,500 for Zimbabwe, "tying future value growth to slower-growing source markets". Implication: hold yield in the mature markets while growth comes from elsewhere.
- Draws on: ch2/01 [13], [14]. Footnote note on the 63%: "the slide prints 61% in its text, and 63% is the sum of its printed shares". The 2024 figure cites (Current State Diagnostic, Dec 2025, p29) in the province's terms; "the December baseline" does not appear in the text. About 140 words.

### Six months carry nearly two thirds of demand
December, January and November took 12.7%, 11.5% and 11.3% of 2025 overseas visitors and June 6.1%; October to March hold about 62%, and the 2024 Wesgro Visitor Tracking Survey gives 61% and 39%. Growth therefore depends on "improving conversion in Apr-Sep rather than pushing incremental demand into already busy peak months". Recall in a phrase that airlines pull seats in the same months (section 2.3).
- Draws on: ch2/01 [15], [16]. Footnote note on the 62%: "the twelve printed monthly shares sum to 104.9% and are normalised here" (keep "computed"). About 130 words.

### Growth depends on barriers removed, not demand
The model builds a rate for each source market from four levers (outbound growth, the province's penetration, the airlift ceiling and structural conditions such as currency and visas), anchored on OAG aviation data and global traveller data. "The difference between scenarios is not demand potential, but the extent to which structural barriers are removed." From the 2025 base it reaches 1,822,634, 2,175,778 or 2,516,282 arrivals by 2035, 2.0%, 3.8% and 5.3% a year. The accelerated step rests on direct routes to India and China, above-baseline activation and more hub capacity. Without them, "volume reverts to base". Implication: the upside is bought by removing barriers, and the base case meets the model's seat line at the 2030 year point (section 2.3).
- Draws on: ch2/01 [9], [17]; ref ch2/01 [18] (figure "Growth scenarios to 2035") after the end-point sentence. Footnote note on the 2025 base: "the June version prints the same 2035 points from a 2024 base" (from relocated ch2/01 [10]). About 190 words.

### Hub and acceleration markets add the most arrivals
In the base case hub markets add 206,584 arrivals between 2025 and 2035, mature markets 178,780, acceleration markets 175,818, regional markets 110,298 and Japan and South Korea 5,469. India more than doubles from 76,547 to 165,260 and China with Hong Kong from 43,412 to 92,598, both at 8% a year. Spend follows the mix: at R24,500 a visitor in mature markets and R8,500 in regional ones, modelled foreign spend rises from R27.12bn in 2024 to R40.59bn in 2035. Implication: volume grows fastest where spend per visitor is lowest.
- Draws on: ch2/01 [19]; ref ch2/01 [20] (figure "Base-case growth by market group") after the arrivals sentence; ch2/01 [21]. About 140 words.

### Four segments can spread demand across the map and the year
About 97 million addressable travellers fall into four values-based segments, each with home markets: Curious Explorers in the UK and the USA, Creative Connectors in India, Discerning Connoisseurs in China and the UAE and Reflective Adventurers in Germany. Curious Explorers and Discerning Connoisseurs are "most aligned to the Western Cape's offering". Yet the segments matter for spread and season as much as for volume: Curious Explorers offer the "strongest opportunity for geographic dispersal beyond Cape Town", and Reflective Adventurers can steady the year through outdoor and wellness travel.
- Draws on: ch2/01 [23]; ref ch2/01 [24] (table "Four traveller segments") after the pairings; ch2/01 [25]. About 140 words.

### India and China already arrive through hubs
About 71,000 Indian travellers and about 30,000 Chinese reach Cape Town through other carriers' hubs each year, about 101,000 journeys. Half the Indians start in Mumbai, and Addis Ababa and Dubai carry 81% of them. Direct Indian service is "unlikely before 2030 due to aircraft constraints at Air India and IndiGo", and Guangzhou and China Southern are the likeliest first Chinese route. Australia (61,000 indirect travellers) and Saudi Arabia (137,000 passengers, with Riyadh Air's planned hub) come next. Implication, as inline enumeration: convert the traffic already in the air now; build early relationships with Indian carriers and government authorities; treat China as a long-term investment in awareness and indirect volume. Recall Singapore's stopover conversion (section 2.1).
- Draws on: ch2/01 [26]; ch2/02 [23] (split, without the government-to-government quote); ch2/02 [24]. Footnote note on the China count: "the aviation assessment counts about 29,600 travellers from China". About 200 words.

### Each market books on its own platforms
Chinese travellers discover on Douyin and Xiaohongshu and book on Trip.com, Qunar and Fliggy; Indians book through MakeMyTrip, Booking.com and Expedia; much Gulf travel runs through private advisors and concierge agencies. Each market has its own gap: India lacks a direct flight to Mumbai or Delhi and Indian-friendly adaptation, and the Gulf lacks Arabic-language booking and local-currency pricing (visas sit in 2.4). Yet the Department of Economic Development rates destination platforms behind international practice in online presence and AI adoption, and the Overberg says its nearness to Cape Town is not packaged before visitors book flights. Implication: activate inside those platforms and shift spend "toward trade-led conversion rather than broad awareness campaigns".
- Draws on: ch2/01 [27] (split, without the visa clause), [28]; ch2/04 [18] sentence 2 (split). About 170 words.

### Africa is a base and a growth market
The province recorded 323,971 arrivals from 16 reported African markets in 2024, 62% from Zimbabwe and Namibia, and African visitors spent R4.2bn in 2025, Nigerians R31,000 and Ghanaians R27,700 a visit. Nigeria, Kenya and Ghana are the priority growth markets; Nigeria's addressable market is modelled at 310,000 to 510,000 adult trips a year and Kenya's at 240,000 to 400,000. Namibia and Zimbabwe "add stability, repeat demand and counter-seasonal volume". Implication: Africa is a regional foundation that is both base and growth.
- Draws on: ch2/01 [29], [30]. Footnote on the priority-markets sentence: (Demand-Side Analysis, Jun 2026, p30; Skift African Market Analysis memo, Mar 2026, section 2; the memo places Ghana among fourth-tier watch markets for brand seeding rather than conversion). About 160 words.

### Business events are the green-season lever
International association meetings in Cape Town rose from 33 in 2022 to 58 in 2024, and 109 of the 136 held over the three years fell between May and November. Cape Town ranked 35th in the 2024 ICCA ranking and hosted 37 of South Africa's 64 UIA-recorded meetings in 2025, while hotel occupancy was 53% in June 2023. Yet MICE is four businesses with different buyers and lead times, only conferences are measured and meetings are "absent from consolidated provincial statistics". Stellenbosch and George can host the extra nights delegates spend in the regions. Implication: the lever needs one calendar and its own measures, as Melbourne's did (section 2.1).
- Draws on: ch2/01 [31], [32]. About 160 words.

**Closer** (two sentences, about 40 words, each under 35): "The strategy does not need more awareness. Pillar 1 must fill the green season, convert hub traffic inside each market's platforms, hold yield in the mature markets and build the African base; seats and selling (sections 2.3 and 2.4) decide whether that demand lands."

**Box "What this means for the strategy"** (from ch2/01 [33] items 1 to 6; about 115 words):
1. **Validates FA01, Respond to growth segment traveller preferences.** Four segments, each with named home markets.
2. **Supports FA02, Create green-season demand with MICE and events.** Business events cluster from May to November, when leisure demand is weakest. The seat side of the case sits in 2.3.
3. **Supports FA03, Make the whole province findable and bookable.** Conversion runs through market-specific platforms that Western Cape product must reach.
4. **Rewords FA04, Convert India and China hub traffic.** About 101,000 hub journeys a year and no direct Indian route before 2030.
5. **Validates FA05, Increase yield in mature markets.** The highest-spending visitors come from the slowest-growing markets.
6. **Validates FA06, Build a regional foundation (Africa).** A large regional base and two high-yield growth markets.

---

## 2.3 Supply-side factors (ch2/03_supply.json; about 2,600 words)

Feeds Pillar 2 (FA07 to FA12). Thesis: supply sets the ceiling. The gateway is the summer constraint; reach, beds and booking are the regional one. The argument runs from the air gateway (seats, routes, hubs, fares, runway, port) to the flagships that fill with it, then outward to the regions the peak should spill into and the capital that does not reach them. Word budget: lead 45, opening 160, h3s 2,060, closer 45, box 230, headings 70. It is the longest part because every load factor, seat count and district score must survive; cut repetition first if it runs over.

**Lead.** "Supply sets the ceiling on growth. The gateway fills at the peak before its relief arrives, and airlines raise fares before they add seats. Beyond the Metro the product exists but is hard to reach, book or stay in." (ch2/02 [1], ch2/05 [1])

**Opening paragraph (about 160 words), method and the stakeholder verdict.** ch2/02 [6], ch2/05 [8], [9], [10], ch2/04 [13] sentence 1, ch2/04 [1] (split).
- Seat and booking data cover every Cape Town route, with bookings from the airlines' distribution systems to November 2025. Footnote note: "bookings are weighted to the full market and will not always reconcile exactly with airport published data".
- On the ground, 50,332 tourism assets are mapped across six regions in three layers (attractions, services and enabling infrastructure), from Wesgro's supply database, SANParks and CapeNature data and open geographic sources, on the premise that "destination performance is constrained by the weakest layer". Then, word for word: **[Dataset limits, including the absence of geography below district level, to be confirmed against the supply dataset notes.]**
- Each district is scored from 1 to 5 on attractiveness (40%), readiness and capacity (30%) and accessibility (30%). Footnote note: "the scores are evidence informed rather than formula derived, and missing data is not scored as poor performance".
- Stakeholders rate supply constraints the most severe: 44 of the 68 insights under Transform Supply are rated High, against 23 of 64 under Reshape Demand. First stakeholder citation, so it carries the attribution note.

### Seats bind at the peak before demand does
The model draws current air access as "a hard ceiling at 1.8 million inbound seats", and the base case first passes it at the 2030 year point with 1,802,929 arrivals, after 1,673,855 in 2028. The line is the model's assumption, not a measured cap (section 1.3). Even 2.1 million by 2035 needs deliberate added capacity. Growth to 2.5 million is a supply programme before it is a marketing one.
- Draws on: ch2/01 [22]. Footnote note on the year points: "only six year points are printed, so the crossing falls between 2028 and 2030". About 130 words.

### Cape Town's routes already run full
Twenty-nine international routes serve Cape Town in 2026, and its share of South Africa's international capacity rose from 10% in 2010 to 25% (section 2.1 shows it out-winning its peers). The routes run full: 11 of 27 ran above 80% load in the year to November 2025, led by Newark (88.6%), Atlanta (84.3%) and Frankfurt and Heathrow (83.0%), and sixteen at 75% or more. Cape Town's 79% average is the joint highest of South Africa's five largest airports, with Lanseria, against about 70% nationally, 75% for Africa and 84% globally. Regional routes are fuller still: Luanda ran at 86.2% and 83.4%, Maputo 83.3%, Gaborone 82.3%, Mauritius 81.8% and Harare 81.3%, all named for more capacity. Domestically, Durban runs at 90.0% and other routes between 70% and 80%. Cape Town faces "a 'what next' moment": tactical gains remain in frequency and aircraft size, and the next phase needs long-term gains over short-term wins.
- Draws on: ch2/02 [10] (split, routes and share), [11], [16], [17]; ref ch2/02 [18] (figure "Route load factors to November 2025") after the load sentences; ch2/02 [22]. Footnote note on the network total: (MIDAS Aviation Market Assessment, Mar 2026, "Seasonality", computed; the printed network total is 76.0% on 3,816,797 seats, while the 27 listed rows sum to 75.0%). About 240 words.

### The network runs through hubs, not Asia
The seven largest international markets are all hubs, with 2.7 million seats in 2026 against 2.0 million in 2019. Western Europe holds 38% of international capacity, the Middle East 23%, Southern Africa 17%, Eastern Africa 14% and North America 6%. Most hub passengers connect: Emirates above 80% and Qatar Airways nine in ten. Seven of the twelve carriers that launched since 2014 fly to African points, led by Airlink to regional points (441,602 seats in 2026) and Ethiopian to Addis Ababa (437,430), then Turkish to Istanbul (240,200), United to Newark and Washington (172,190) and Kenya Airways to Nairobi (127,138). Yet no seat flies direct to Asia: one airline serves Cape Town from Asia against ten from Africa. Implication: growth-market traffic depends on other carriers' priorities.
- Draws on: ch2/02 [12], [13], [14], [15]. Footnote note for the other seven carriers, without nested brackets: "the other seven are Delta Air Lines to Atlanta with 110,612 seats, Norse Atlantic UK to London Gatwick with 103,428, LATAM Airlines Group to São Paulo with 47,084, Air Tanzania to Dar es Salaam and Victoria Falls with 37,716, Safair to Windhoek with 32,130, Proflight Zambia to Livingstone with 14,600 and Eswatini Air to Manzini with 3,700". About 240 words.

### Airlines raise fares and cut winter seats
Carriers are expected to "increase revenues via higher selling fares rather than add new services", which "will frustrate that desire for increased visitors". Footnote note: "the assessment carries no fare data, so the claim rests on its author's judgement of airline behaviour". In winter they withdraw seats: June carried 6.4% of 2025 international seats and December 10.8%, with May, July, August and September at 6.9% each. Connecting traffic is "especially critical in the low season", which ties the winter schedule to the hub carriers' own priorities. Implication: new seats must be won route by route and season by season, as New Zealand did with marketing built around airline breakeven and shoulder-season loads (section 2.1).
- Draws on: ch2/02 [19], [20]; ref ch2/02 [21] (figure "International seats by month, 2025") after the monthly shares. About 170 words.

### The runway sets the outer limit
Cape Town International's single runway has no parallel taxiway and caps movements at about 30 an hour, and two of the airport's seven parts are full. The R6.39bn runway relocation lifts that to 45, a 50% rise, around 2033, with terminal relief from about 2032; ACSA's latest schedule shows the runway finished by December 2029. George handled 911,000 passengers in 2025, above its design limit, and a R310m terminal doubles it to about 2 million by 2028 or 2029. Cape Winelands Airport targets 2028 on an R8bn first phase with no firm airline. "The certain fix is the latest, and the earliest big-capacity option is the least certain." Yet no stakeholder named the airport as a constraint, and no airline or airport voice was among the 16 organisations: a gap in the record, not a finding. Implication: the outer limit is a national lever held by ACSA (section 2.4).
- Draws on: ch2/02 [25], [26]; ch2/04 [19] sentences 1 and 3. About 220 words.

### Cruise needs product, not berths
Cape Town's single berth handled 83 calls and about 127,000 passengers in 2024/25, about 40% of a season capacity of 150 or more calls, for R1.79bn of impact; its limits are a 300m ship length, the South-Easter and no shore power. Mossel Bay handled 21 calls and about 13,000 passengers and opened a R22m passenger facility in November 2025. It has no quay, so ships anchor and tender and only small and mid-sized ships call; its tourism body reports calls up from four before COVID to 27 a season. Saldanha Bay has had 3 trial calls, shares the ore terminal and has no cruise berth or passenger facility, and its R4bn upgrade serves iron ore. Implication: protect Cape Town, back Mossel Bay and watch Saldanha. Cruise grows "through product and marketing, not capital works".
- Draws on: ch2/05 [24], [25] (merge the repeated Cape Town figures); ch2/04 [19] sentence 2. About 190 words.

### The flagships are full in season
Table Mountain Aerial Cableway queues run up to three hours up and two hours down at peak, Chapman's Peak suffers disruptions and the December to January peak "overwhelms transport and accommodation capacity". Boulders is "already near carrying capacity" and summit expansion on Table Mountain is severely limited. Yet Cape Point and the township attractions are underused. Implication: the peak must spread to product that has room, under the capacity discipline New Zealand applies (section 2.1); the next two h3s show why the regions cannot yet take it.
- Draws on: ch2/05 [22]; ch2/04 [13] sentence 3; ch2/04 [17] sentence 1 and ch2/04 [22] Cableway (splits). Merge the two queue figures (two to three hours; up to three hours up and two down). Placed before the regional h3s so that the peak leads into the case for dispersal. About 140 words.

### Readiness and access fall away from the Metro
Readiness halves between the Metro and the periphery: the Cape Metro rates 4.5 out of 5, the Winelands and the Garden Route 3.4, the Overberg 2.7, the West Coast 2.5 and the Central Karoo 1.9. Accessibility falls fastest, from 4.7 for attractions in the Metro (5.0 on transport) through 3.3, 3.0, 2.0 and 1.7 to 1.0 in the Central Karoo. The Metro is gateway and dispersal point: it holds 20,281 of the 50,332 assets (40.3%), five of the six highest-volume attractions, the only international airport and rapid transit, and generates 72.5% of provincial GDPR. Beyond it and the Garden Route the visitor drives. Public transport is "effectively absent" on the West Coast and in the Overberg, the Winelands have no transit between estates, Central Karoo access "sits at the floor" and Metro rail is "functionally unusable for tourism". Stakeholders call weak transport and last-mile access "structural barriers to visitor movement within and beyond Cape Town". Implication: "dispersal needs deliberate corridor investment, not organic spillover from Cape Town".
- Draws on: ch2/05 [12], [13]; ref ch2/05 [14] (figure "Readiness and accessibility by district") after the accessibility sentence; ch2/05 [15], ch2/05 [3] (split, the 72.5%); ref ch2/05 [16] (table "District strengths and weaknesses") after the gateway sentence; ch2/05 [17]; ch2/04 [13] sentence 2. About 260 words.

### Strong regional assets lack beds and booking
The West Coast has the province's highest natural-asset attractiveness and the Central Karoo its most unique niche assets, yet both score lowest on readiness. Inland areas north of the N2 on the Garden Route are tourism-inactive and the Metro's industrial belts show "zero tourism conversion". In the Winelands, mid-market accommodation "is effectively absent outside Stellenbosch" and a "luxury-skewed product mix excludes mid-market and family segments". Beds are thin beyond Langebaan and Paternoster and thin at international grade on Route 62, and no bed count sizes the gap. Booking fails first in the regions: 40% or more of the Metro's smaller operators lack online booking, CapeNature takes about 70% of its reservations by phone and Route 62 has the lowest bookability of the six touring routes. The West Coast route rates Gap on digital payments; only the Cape Peninsula route is rated ready. Implication: the regions need beds and a booking route before they need marketing, with quality made visible on booking platforms as in Valencia (section 2.1).
- Draws on: ch2/05 [18], [19], [20], [10] (touring-route method: six routes rated Ready, Developing or Gap on access, accommodation, safety and bookability; footnote note "the July final supersedes a June draft"); ref ch2/05 [21] (table "Touring route readiness") after the bookability sentences; ch2/04 [18] sentence 1 and ch2/04 [22] CapeNature (splits). About 240 words.

### Committed capital funds the airports, not the regions
The Metro's pipeline exceeds R30bn, led by ACSA's R11.3bn airport overhaul, the R20bn V&A Granger Bay expansion and the R3.3bn MyCiTi Phase 2; the George terminal and Cape Winelands Airport add air capacity, as the runway h3 sets out (recall them by name, without repeating their figures). Each region still carries a gap no committed money closes: in the Metro, last-mile transit to Chapman's Peak, Constantia and Cape Point, small-operator booking and township product; in the Winelands, transit inside the wine triangle, non-wine product and domestic pricing; on the Garden Route, an international carrier, winter product and transport between towns; in the Overberg, beds towards De Hoop, booking east of Hermanus and year-round product; on the West Coast, accommodation depth, digital payments and an airport; in the Central Karoo and on Route 62, accommodation depth, emergency support and an airport. Name each region's committed works once (Winelands precinct R16bn to R20bn; R9.4m landing system; R81.7m Agulhas precinct; R17m Malgas road; completed R693m Malmesbury bypass; R4bn Saldanha port, by recall to the cruise h3; R62 reconstruction and rural broadband to 2026). Implication: the pipeline funds airports, ports and roads, not tourism product, and funding sits in 2.4.
- Draws on: ch2/05 [23], [26], [27] (merge the repeated Metro, George and Cape Winelands Airport figures, which the runway h3 already carries; keep each region's rating). About 230 words.

**Closer** (two sentences, about 45 words): "Supply, not demand, sets the pace: the gateway decides how fast the province grows in summer, and reach, beds and booking decide where growth can land. Pillar 2 therefore starts with seats into the gateway and then builds the corridors, beds and booking beyond it."

**Box "What this means for the strategy"** (about 230 words). Pillar 2 lines first, then the air evidence for Pillar 1.
1. **Rewords FA07, Win direct routes and add seats on full routes, and supplies its binding constraint.** Eleven routes above 80%, fares before seats and a runway that binds until about 2032; the base case passes the model's seat line at the 2030 year point. (ch2/02 [27] item 1; ch2/01 [33] item 7, FA07 clause)
2. **Supports FA07, FA08, Grow cruise calls and ports, and FA15.** Airport capital is committed; cruise needs product, not berths; regional gaps have no committed capital. (ch2/05 [28] item 5)
3. **Validates FA09, Accelerate tourism-enabling internal mobility, and stakeholder evidence supports it.** Accessibility decays from 4.7 to 1.0 and public transport is absent beyond the Metro and the Garden Route; stakeholders name last-mile access. (ch2/05 [28] item 1; ch2/04 [23] item 4)
4. **Validates FA10, Support diversified route and product development, and FA11, Align visitor experience in-destination.** Strong assets in cold zones and a missing mid-market; stakeholders' account of a narrow product set supports FA10. (ch2/05 [28] item 2; ch2/04 [23] item 4)
5. **Validates FA12, Balance impact on nature-based attractions.** Flagships full at peak while alternatives are underused; stakeholder reports of flagships at capacity support it. (ch2/05 [28] item 3; ch2/04 [23] item 4)
6. **Supports FA03, Make the whole province findable and bookable.** Bookability fails first in the regions, and stakeholders report product that cannot be booked online. (ch2/05 [28] item 4; ch2/04 [23] item 4)
7. **Supports FA02, rewords FA04 and validates FA05 and FA06 from the air side.** Winter seats fall to 6.4% of the year in June. No direct Asian route runs before 2030, so conversion runs through the hubs. The mature long-haul routes are the fullest, and five regional routes run above 80% and are named for more capacity. (ch2/02 [27] items 2 to 5)

---

## 2.4 The enabling environment (ch2/04_enabling.json; about 2,020 words)

Feeds Pillar 3 (FA13 to FA20). Thesis: the system that decides who decides, who pays, who measures and who benefits is thin, and in the communities the missing piece is a seller. The argument runs from who holds the levers, through who pays and who measures, to who sells in the communities. Word budget: lead 45, h3s 1,630, closer 40, box 230, headings 75.

**Lead.** "The enabling system is thinnest where the strategy needs it most. The decisive levers sit nationally, local bodies have lost their funding and nobody can yet count tourism jobs. In the communities, organisation rather than distance keeps visitor spend out." (ch2/06 [1], ch2/04 [1] split)

No separate method paragraph: the stakeholder method sits in the chapter introduction, and the community method sits inside its own h3.

### The binding levers sit with national government
The Department of Economic Development reports that "restrictive bilateral air agreements are limiting airlift growth", leaving the province less competitive than its peers, and Chinese routes are "frequently an extension of government-to-government relations"; the runway sits with ACSA (section 2.3). Chinese and Gulf travellers face slow, document-heavy visa processes, and four organisations raised visas, among them the Cableway for India and China and the CTICC for African events. SA Tourism's institutional weakness constrains international marketing. Section 1.2 maps which tier holds which lever. Implication: the province leads by escalation backed with evidence, as Chile lobbied for liberalisation and simpler visas (section 2.1), not by owning these levers.
- Draws on: ch2/04 [16] sentences 1 and 2, [21] (air agreements; merged, not repeated); ch2/01 [27] visa clause (split); ch2/02 [23] government-to-government quote (split). First stakeholder citation in 2.4, so it carries the attribution note. About 190 words.

### Funding, capacity and mandates have all thinned
The Department of Economic Development rates destination funding "materially below peer destinations" for destination management and marketing, and finds that tourism institutional capacity "has eroded over the past decade at both provincial and municipal level", both rated High. National Treasury's MFMA Circular No. 131 of 31 March 2025 has since disrupted municipal funding for local tourism bodies, most of which "are not operationally sustainable without municipal funding support". Mandates blur at district level: the West Coast District Municipality reports "a mandate disconnect" between district, local municipalities and LTOs that leaves tourism development without an owner. Implication: the committed capital in 2.3 reaches airports, ports and roads, not the bodies that sell and manage the destination, which is why fiscal pressure is turning attention to a tourism levy and blended finance.
- Draws on: ch2/04 [14], [15], [21] (funding and MFMA; merged, not repeated); ch2/04 [22] West Coast (split). About 210 words.

### Climate losses already fall on the flagships
Robben Island loses about R16 million a year to weather-cancelled trips, and CapeNature reports flooding, fire and heat closing sites. Implication: climate risk is an operating cost for the province's best-known product today, so sustainable destination management must be funded as risk management, not as a later add-on.
- Draws on: ch2/04 [17] sentence 2 and ch2/04 [22] Robben Island (splits). Split from v7's single funding-and-climate h3 so that each claim stands on its own evidence. About 90 words.

### Collaboration platforms exist; data does not flow
Fifteen of the 16 organisations raised industry and government collaboration and fifteen raised policy and data sharing, which also carries the most insights (30) and the most High ratings (16). The data architecture is "too fragmented, lagged and proxy-based to provide a reliable view of visitor volumes, spend, spread or economic impact at provincial level". Yet platforms exist: FEDHASA points to JAMS, through which tourism associations coordinate with Wesgro, the Western Cape Government and the City of Cape Town. Implication: the gap is a data-sharing protocol, not another forum; coordination is hard everywhere (section 2.1).
- Draws on: ch2/04 [9]; ref ch2/04 [10] (figure "Themes raised by stakeholder organisations") after the first sentence; ch2/04 [11]; ch2/04 [1] (split). About 160 words.

### Nobody can yet count tourism jobs
The national Department of Tourism reports that "there is no approved official methodology for provincial tourism GDP and jobs estimates", and Stats SA cites 749 vacancies behind delays to the tourism satellite account, with provincial flows inferred partly from ports-of-entry data. Inside the communities no profile counts tourism employment; the figures are node-side, such as about 4,700 formal Town Centre jobs for 82,393 employed Mitchells Plain residents, and need rests on fifteen-year-old Census data. CapeNature, the West Coast District and the Overberg raise skills gaps, yet no labour analysis sits behind them. Implication: the 300,000-jobs ambition (section 1.1) has no baseline yet, so measurement comes before targets, and yield-based metrics of the kind New Zealand uses (section 2.1) need the same data.
- Draws on: ch2/04 [12]; ch2/06 [24]; the skills sentence cites (Stakeholder Insights Report, Mar 2026, p27, p39, p43), from the ch2/04 [23] item 5 reason. The v7 point is that no labour analysis sits behind the skills gaps; do not restate it as a claim about the jobs ambition. About 180 words.

### Communities hold people, not spend
Foreign visitors spent R25.9bn in FY2025, yet the 20 shortlisted communities, with 18.4% of residents and 15.4% of employed residents, receive 0.02% to 0.04% of foreign direct spend, about R4m to R10m a year on the documented floor; 1% would bring R259m. Inclusion counts activity inside the community (a tour, a meal, a bed or a market), not a commute to a hotel job. Method, two sentences: a long-list of 107 communities with 2.81 million people in 2011, 48% of the province, from Census sub-places of 1,500 people or more with unemployment of 25% or more plus named mission, fishing and farm settlements; five weighted criteria (need, tourism potential, proximity, readiness and access) give 20, five in the Metro and three per district.
- Draws on: ch2/05 [3] (split, the R25.9bn); ch2/06 [10], [6] (definition only; the purpose quote drops), [7]; ch2/06 [8] sentences 1 and 2 (split) as one footnote note on the method sentence, with no semicolon of its own: "the evidence joins Census 2011 sub-places to an OpenStreetMap asset layer of September 2026 with road travel times and municipal plans, and need rests on Census 2011 because Census 2022 is not published below ward level and asked no income question" (SME and Community Inclusion Plan, Sep 2026, p14, p15, p16). About 190 words.

### Organisation, not distance, keeps spend out
Of the 107, 93 lie within 45 minutes of one of 35 tourism nodes or three corridors; Langa is 12 minutes from Cape Town International and Zwelihle seven from Hermanus, and distance binds in none of the 20. Yet proximity and access carried 35% of the shortlist score, so the result is partly built in (Appendix A5, "Community shortlist criteria"; not "Table A.18", which the s11 move renumbers). Organisation binds in 11: ten have no active tourism body and nine show no benefit residents can see. Product exists without a seller: Langa's walk rates above 4.8 on global platforms, but city firms sell most of the 23 Langa walks on Viator; Zwelihle's four guides sell by phone; the Mitchells Plain festival drew 27,800 visitors in November 2025 with no local operator or LTO behind it. Implication: the communities cannot yet be found or booked on the channels visitors use.
- Draws on: ch2/06 [11], [12], [13]; ref ch2/06 [14] (figure "Binding constraints in 20 communities") after the "Organisation binds in 11" sentence. About 190 words.

### Safety is the second gate
Nine of the 20 record a safety-perception gap and five record extortion, and "tourism activity alone cannot resolve crime or extortion". Seven organisations raised safety as a barrier across transport, township tourism and international selling. Implication: safety is a launch requirement in its own right, so no pilot opens until it is met.
- Draws on: ch2/06 [15]; ch2/04 [16] sentence 3. About 90 words.

### Each community type needs a different first move
Most long-listed communities sit near a node with something worth visiting. Near a node with assets underused (49 long-listed, 11 shortlisted), the first move is a seller and a slot in the node's itineraries, procurement and events. Near a node with nothing inside (43 and 6), one anchor asset under a covenant, but only once a seller is in place. Remote with assets underused (7 and 2), open access and put the asset on a route the LTO already sells. Remote with nothing (8 and 1), procurement and skills first, an asset only once a route product exists.
- Draws on: ch2/06 [20], [21]; ref ch2/06 [25] (table "The 20 shortlisted communities", carrying its open item **[Open item: re-measure Metro travel times to a visitor node such as the V&A Waterfront or the CBD, not CTIA.]** in its source line) at the end of the h3. Keep the [21] citation note "p4 prints 48 and 8 for the two assets-underused rows". About 180 words.

### A seller with a stake comes first
The model is a functioning selling capability, a link to demand the node already has and launch gates for safety, access and a viable operating model. It pilots in two or three of six profiled communities and scales only once bookings, local spend, delivery and safety meet thresholds agreed before launch. The first deliverable is deliberately small: "one live booking route, published operating dates, a named customer contact and a simple record of bookings and local revenue". Most first moves carry no budget line; roles and funding are in Chapter 4. Implication: the order the cases support (section 2.1) becomes the order of delivery.
- Draws on: ch2/06 [22], [23]. About 150 words.

**Closer** (two sentences, about 40 words): "None of these gaps is a shortage of visitors; each is a question of who decides, who pays, who measures and who sells. Pillar 3 builds those answers, and Pillars 1 and 2 depend on them."

**Box "What this means for the strategy"** (about 230 words). Pillar 3 lines in focus-area order, then the cross-pillar line. Ten lines in the first plan become eight: the two FA16 and FA19 lines merge (both reasons kept, the aviation item's "supports FA16" folding into "rewords FA16"), as do the two FA20 lines.
1. **Refines FA13, Embed local destination bodies for community inclusion.** The binding constraint is a seller with a stake, then a safe way in, then demand pulled from the adjacent node. (ch2/06 [26] item 1)
2. **Rewords FA14, Manage climate risk and sustainable tourism, and supports FA15, Crowd in capital.** Unfunded local tourism bodies and climate losses at flagship sites. (ch2/04 [23] item 3)
3. **Supports FA10, Support diversified route and product development, and FA15, Crowd in capital.** Assets follow sellers and route products, not the reverse. (ch2/06 [26] item 3)
4. **Rewords FA16, Align institutional stakeholders across all three tiers, and supports FA19, Lead removal of infrastructure, visa and safety deficits.** Air rights, visas and SA Tourism sit nationally, Chinese routes follow government-to-government agreements and airport capacity sits with ACSA; mandates blur at district level. (ch2/04 [23] item 2; ch2/02 [27] item 6)
5. **Supplies the visa barriers for FA19, and supports it on safety.** Chinese and Gulf travellers face slow, document-heavy visa processes, and safety and extortion gate activation in up to nine communities. (ch2/01 [33] item 7, FA19 clause; ch2/06 [26] item 4)
6. **Validates FA17, Strengthen industry and government collaboration, and FA18, Expedite tourism-enabling policy and data sharing.** Each raised by 15 of 16 organisations, with existing platforms such as JAMS to build on. (ch2/04 [23] item 1)
7. **Supplies the case for FA20, Develop workforce and service skills, as a question, and supports FA20 and FA18 on measurement.** Skills gaps raised by CapeNature, the West Coast and the Overberg have no labour analysis behind them (Stakeholder Insights Report, Mar 2026, p27, p39, p43); no count of tourism jobs exists inside the communities, and need rests on Census 2011. (ch2/04 [23] item 5; ch2/06 [26] item 5)
8. **Supports FA03, Make the whole province findable and bookable.** Community product sells by phone or through city operators. (ch2/06 [26] item 2)

Box check: all 34 v7 box items land in a new box with their verb and reason (in 2.3 and 2.4 some share a line), and FA01 to FA20 each appear at least once. apply_v8.py rebuilds the A1 "Chapter 2" column from these boxes. The placement gives, for example, FA03 in 2.2, 2.1, 2.3 and 2.4, FA05 in 2.2, 2.1 and 2.3, FA13 in 2.4 and 2.1 and FA15 in 2.4, 2.1 and 2.3, which is where the evidence now sits.

---

## Relocations and the edits they need outside Chapter 2

Full list in the allocation file (45 entries: 25 retired v7 headings, 20 content blocks). Points to act on:
- **SLA clauses (six blocks).** ch2/01 [5], ch2/02 [4], ch2/03 [3], ch2/04 [3], ch2/05 [6] and ch2/06 [4] go to the A9 documents table. That table already lists every clause number by document; I checked each one. The open item **[Clause wording to be checked against the signed Annexure B.]** is not in A9 word for word, so the 2.4 draft adds it once as a note under the documents table (`appendix_blocks`, module `appendices/09_a9_glossary.json`), e.g. "The SLA clause numbers in the last column, 'Version in hand and SLA clauses', are those each document answers. [Clause wording to be checked against the signed Annexure B.]" A9 ends with that table, so an appended note sits directly under it. carries_all is false for all six, and the checker does not test relocated open items, so check the A9 note by hand.
- **Comparator-set versioning.** ch2/03 [7] and [8] go to Appendix A3, which holds the inception six, the ranks and the swaps. The December baseline's Namibia line (Current State Diagnostic, Dec 2025, p62) is not in A3; it rides as a footnote note in the 2.1 opening paragraph.
- **Model bases.** ch2/01 [10] goes to A2's "Model end points by base year" table, which holds both bases. 2.2 carries the June version as a footnote note.
- **Engagement record.** ch2/04 [6] goes to A6 [5]. ch2/04 [7] goes to section 1.4 [23], which holds the open item word for word with the full stop outside the bracket, and to A6 [9] to [11]. ch2/04 [20] goes to A6's lines-of-enquiry table. The phases from ch2/04 [5] ride as a footnote note in the chapter introduction.
- **Duplicates retired.** ch2/05 [4] and ch2/06 [2] repeat ch2/06 [10], which 2.4 absorbs with every figure. Their v7 cross-references must not survive.
- **Knock-ons already in apply_v8.py:** ch1/04 [19], ch1/05 [5], A3 "Kenya 14.6% (section 2.2)" becomes 2.1, A5 shortlist reference becomes 2.4, ch3/31 Kliptown reference becomes 2.1, ch5/03 group path becomes 2.2, plus the A1 column and the chapter title. **Not covered:** ch1/01 [18] says "(section 2.6 and Chapter 5)". The s11 draft must point that line to section 2.4, or apply_v8.py stops on the stale reference.
- Table and figure numbers renumber by position. Chapter 2's tables run Comparator growth (2.1), Four traveller segments (2.2), District strengths and weaknesses (2.3), Touring route readiness (2.4) and The 20 shortlisted communities (2.5), so "2.3" in section 1.4 [26] ("Tables 1.3, 2.3 and A.17") still holds. Its "1.3" and "A.17" do not: the s11 draft removes Table 1.1 and moves a table into A2 (s11 outline, section 7, item 1), so that open item needs the knock-on edit the s11 outline asks for. For the same reason 2.4 cites the shortlist weights by caption, not as "Table A.18" (now A.19). No module outside Chapter 2 cites a Chapter 2 figure or table by number.

## Where this departs from the allocation guidance

1. **The seat line (ch2/01 [22]) opens 2.3, not 2.2.** It is the gateway constraint Pillar 2 rests on. 2.2 keeps the scenario figure, whose callout names the line, and recalls the crossing in one clause.
2. **Visas and route politics go to 2.4.** The market-by-market visa clause (ch2/01 [27]) and the government-to-government quote on Chinese routes (ch2/02 [23]) go to 2.4. Hub flows, conversion and the India and China route outlook stay in 2.2, and the network facts (hubs, no Asian capacity) stay in 2.3.
3. **The stakeholder method and the paraphrase open item sit in the chapter introduction**, inside the 2.1 module, because the paraphrases now spread over 2.2 to 2.4. Fallback: 2.4 holds six of the eight v7 paraphrases, so the item can close the 2.4 h3 "Nobody can yet count tourism jobs", after the last of them.
4. **R25.9bn of foreign spend anchors 2.4's community share, not 2.2.**
5. **Flagship capacity goes to 2.3; flagship climate losses go to 2.4 (FA14).** The Department of Economic Development's platform finding and the Overberg packaging point go to 2.2 (conversion); CapeNature's 70% goes to 2.3 (bookability).
6. **Box lines follow the evidence, not only the pillar.** 2.3 and 2.4 boxes carry a few Pillar 1 lines (FA02, FA03, FA04, FA05, FA06). The 2.1 box adds one line (FA13 precedent), kept because the benchmark cases behind v7's FA13 line now sit in 2.1. The 2.4 box merges its two FA16 and FA19 lines and its two FA20 lines, keeping every reason.
7. **2.1 tells each comparator's change once, inside its lesson.** The v7 benchmarking module told the Chile change twice ([16] and [24]) and listed all six changes again at the end ([24], [25]). Each change now closes the h3 that holds its evidence, the closing list h3 ("The lessons point to seats and sellers") is cut and its summative line closes "The system matters more than any lever". Appendix A3's "Transferable levers by case" table holds every lever in the source's words.
8. **2.3 puts the flagships before the regions.** The peak at the Cableway, Boulders and Chapman's Peak sets up the case for dispersal, and the readiness, beds and booking h3s then show why the regions cannot yet take it.
9. **2.4 splits funding from climate.** MFMA Circular No. 131 joins the funding h3; Robben Island and CapeNature's climate losses stand as their own short h3, so neither claim rides on the other.

## Word budget

| Part | h3s | New prose | v7 words it absorbs (checker count) |
|---|---|---|---|
| Introduction | none | 210 | about 70 (ch2/04 [5]) plus the open item from one split |
| 2.1 | 7 | 1,850 | about 1,720 (ch2/03 sources, ch2/02 [7], ch2/06 [16] to [19], splits) |
| 2.2 | 9 | 1,760 | about 1,510 (1,258 in full plus splits) |
| 2.3 | 10 | 2,600 | about 2,690 (2,377 in full plus splits) |
| 2.4 | 10 | 2,020 | about 1,870 (1,502 in full plus splits) |
| Total | 36 | about 8,440 | 7,880 kept, 1,108 relocated, of 8,988 |

The budgets are realistic only with the add-backs counted: the 91 short-form citations in the absorbed blocks (27, 15, 28 and 21 by part) gain about four words each when written in full, and the footnote notes that carry relocated detail (the seven carriers alone run to about 55 words) count as prose. 2.3 comes in about 90 words under its v7 intake only because it merges the twice-told cruise, airport and Metro capital figures. Counted with `redteam/check_v8_draft.py`, which reports each draft's words of new prose.
