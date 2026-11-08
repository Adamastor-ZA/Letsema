# Executive summary v8: outline

Module: `content/exec/01_summary.json` (id 0, title "Executive summary"). Draft goes to `redteam/v8/drafts/` in the checker's format and is tested with `check_v8_draft.py` (strict call-outs are always on for `exec/`).

Shape: a hook, then nine headed beats that read as one argument. Where the province stands, what caps growth, what 2.5 million would take, the three shifts, the twenty focus areas at a glance, what happens first, how progress is tracked, what could knock it off course and what the Board decides. New prose budget: about 2,400 words as the checker counts them, citations included (range 2,000 to 2,600), of which the hook is about 300; plus the carried tables and figures. No new bullets. The only lists are the two carried numbered lists of decisions.

Rules the drafter must hold (from the brief and the checker):
- Each headline number is told once. The hook carries 1.57m, 79%, 17 routes, 97 million and 1.4 million, 11 of 27 above 80%, about 30 movements an hour, June 6.4% against December 10.8% and the missing online presence of rural product. Sections 2.1 and 2.2 do not restate them; they add the next layer. The carried tables and figures may repeat a number, and later sections may call back to one in a clause.
- The draft's `sources` key lists only exec blocks absorbed in full ([1], [2], [5], [22], [24], [25], [27] to [30], [33], [36], [37], [43] and the compressed [3], [8], [16]). The chapter blocks named under "v7 blocks" below are raw material and stay in their chapters. Listing them as sources makes the checker demand every number and open item they hold, such as 1.2 [21]'s month-of-travel item and 1.3 [10]'s slot-headroom item.
- No deliverable named in the body text. That covers "MIDAS", "the deck", "the June deck", "Skift's survey" and "interim deliverables", and also the plain "the aviation/infrastructure/benchmarking report". Sources stay in citation parentheses. A note on a source rides after a semicolon, lowercase and at least four words long.
- Short-form citations, `(p19, p20)` or `("Seasonality")`, fail the checker in new prose. Write them out in full. v7 [22] has both.
- Every number in new prose must already appear in the report. Computed figures carry `; computed` in the parenthesis (the 1.6 times premium and the 53% hub share in 2.1). The 3.8% and 5.3% growth rates are printed in the source, not computed (2.3 beat 3).
- Sentences run 15 to 25 words, never over 35. No Oxford comma, no dashes, no banned words.
- Spell out on first use, because the summary stands alone: Airports Company South Africa (ACSA); the Department of Economic Development and Tourism (DEDAT); local tourism organisations (LTOs); the Tourism Growth Steerco. Keep "MICE" only where the carried tables use it.
- Keep the five constraints countable as five. Section 1.5 [22] carries the open item "[Summary of Findings, 14 Oct 2026, slides 3 and 4: align these five constraints with the deck's own list once the deck is in hand.]", which points at them.
- Do not import open items from other chapters with the figures they qualify (for example 1.2's June occupancy item); leave out those figures instead. The one open item in the v7 summary, "[Open item: Wesgro Finance to give an indicative rand band for the first 24 months.]", rides in decision 3 and survives because that list is carried as a ref.

---

## 1. The hook (drafted in full)

The two paragraphs open the summary with no heading above them, directly after the "Executive summary" divider. That way the first line the reader meets is the story, not a label. Paragraph 1 is a `lead` block and paragraph 2 a `p` block. Both pass `check_v8_draft.py` with 0 errors and 0 warnings (301 words, median sentence 15, longest 24). (Fallback if layout needs a heading on the first page: put them under h2 "The recovery has filled the system".)

Why this version. The earlier draft of this hook opened on 80,400 passengers in FY20/21, a pandemic trough every Board member already knows, and reached the tension only in its sixth sentence. This one puts the record and the full airport in the first two sentences, so the problem arrives with the news. It also names conversion beside capacity, because 97 million interested against 1.4 million arriving is a conversion gap and the report's own diagnosis is seats in summer, bookings in winter and beyond the Metro. The 2.5 million is conditional on seats, as the accelerated path is. The 1.44m and the arrivals-basis note ride in footnotes, so the reconciliation never reaches the text.

> **[lead]** A record 1.57 million international passengers arrived at Cape Town International in FY25/26, against 1.16 million in FY19/20, before the pandemic (Demand-Side Analysis, Jun 2026, p11; Current State Diagnostic, Dec 2025, p25; the same series stood at 1.44 million in FY24/25). Its average load factor of 79% in 2025 was the highest of South Africa's five largest airports (MIDAS Aviation Market Assessment, Mar 2026, "The South African Market"). Between 2015 and 2025 the airport added 17 mainline international routes, more than any of eight peer airports (MIDAS Aviation Market Assessment, Mar 2026, "International Comparisons"). The recovery is complete. The next stage is harder, because the system that delivered it is now full.

> **[p]** Interest is not what holds the province back. About 97 million high-value travellers in 34 markets are interested in South Africa, yet only about 1.4 million of them convert into arrivals (Market Assessment Report, May 2026, p41). Seats and bookings stand in the way. In the summer peak, eleven of 27 international routes run above 80% load and one runway caps movements at about 30 an hour (MIDAS Aviation Market Assessment, Mar 2026, "Seasonality"; Infrastructure Report, Jul 2026, p101). In winter, carriers pull seats: June holds 6.4% of the year's international capacity, against 10.8% in December (MIDAS Aviation Market Assessment, Mar 2026, "Seasonality"). Beyond the Metro, most rural properties are missing from the online travel agents where visitors book (Infrastructure Report, Jul 2026, p95). The evidence supports growth from about 1.5 million arrivals in 2025 to 2.5 million by 2035, if the province can win the seats (Market Assessment Report, May 2026, p19; Demand-Side Analysis, Jun 2026, p20; the growth model counts arrivals on a different basis from the airport series, as section 1.1 sets out). That makes the plan a supply programme before it is a marketing programme.

Raw material: ch1/03 [3], [4], [5], [7], [11], [12], [13], [17]; ch1/02 [3]; ch1/01 [14] (the closing line); exec [1], [2], [5].

---

## 2. Headings and beats

### 2.1 h2 "The province earns a premium from a narrow base" (about 200 words)

The earlier heading "Five markets, six months, one metro" was a slogan the reader has to decode. The new one is the section's topic sentence in short.

Beats:
1. Topic sentence: the Western Cape earns more per visitor than the rest of South Africa, from a narrow base.
2. (Cut. The hook now carries the airport series and its footnote carries the 1.44m and the arrivals-basis note, so this section neither repeats the arrivals history nor needs a second basis note.)
3. The premium. Foreign direct spend rose 14% in a year, from R22.7bn in FY2024 to R25.9bn in FY2025. The province takes about a quarter of national foreign spend from about a seventh of arrivals, roughly 1.6 times the national average per visitor (computed). That is about US$890 per arrival, against US$500 for the rest of South Africa.
4. Five markets: 63% of overseas arrivals, and the UK, Germany and the USA alone 52%. Most visitors arrive through someone else's hub: the routes through Dubai, Doha, Addis Ababa and Istanbul carry 53% of arrivals on the ten largest routes (computed).
5. Six months: October to March carries between 61% and 62% of overseas visitor travel, as the 1.2 table message puts it. Cite both years and flag the 2025 figure in the footnote: `(Current State Diagnostic, Dec 2025, p25, p32; Demand-Side Analysis, Jun 2026, p12; the 2025 shares are provisional and scaled to 100%)`. A bare "about 62%" would import the 2025 figure without 1.2 [21]'s open item "[Wesgro Research to confirm the 2025 month-of-travel shares]", which this outline's own rule forbids. The range keeps exec [5]'s 62 in the draft for the checker.
6. One metro: Cape Town holds 20,281 of the province's 50,332 tourism assets (40.3%), and international visitors land and disperse there. (Not "every": cruise visitors arrive by sea.)
7. Closer: growth now needs new markets, new seasons and new regions.

v7 blocks: ch1/02 [1], [9], [10], [14], [17], [22], [24] (message line only), [32], [33]; ch1/03 [21] (closer). No carried table or figure.

### 2.2 h2 "The limits are physical and institutional" (about 320 words)

Opening line: "Five constraints cap the case, and none of them is a shortage of visitors." Then one short paragraph per constraint, each opening on the constraint as its topic sentence. This replaces the v7 bullet list (exec [5]) with prose and keeps every citation from it, including the ACSA and Travel News source. The hook has already given the reader the headline number for routes, runway and season, so each paragraph here adds the next layer rather than repeating it.
1. **The gateway.** The growth model draws air access as a line at 1.8 million inbound seats, and the base path crosses it around 2030. The line is the model's assumption. What binds in practice is the runway at peak hours (call back to the hook's figure in a clause, do not restate it). Relief comes from about 2032 for the terminal and about 2033 for the runway. ACSA now schedules the realigned runway for December 2029, subject to contract award, so the plan keeps about 2033 as its planning date and treats the earlier date as upside. Keep "subject to contract award": 1.2 [27] and 3.4 [5] both carry it, and without it the upside reads as a commitment. The alternatives arrive late or uncertain: George is domestic only and doubles by 2028 or 2029, and Cape Winelands Airport targets 2028 with no named carrier.
2. **Full routes.** The routes the hook counted are the mature long-haul ones: Newark at 88.6%, Atlanta at 84.3% and Frankfurt and London Heathrow at 83.0% (ch1/03 [11]). Carriers on full routes raise fares before they add seats.
3. **Seasons.** The winter gap is a seat problem and a demand problem at once. Seats and visitors fall away in the same months, and connecting traffic is "especially critical in the low season", which ties the winter schedule to the hub carriers' own priorities (ch2/02 [20]). Do not restate June against December or the October to March share; the hook and 2.1 carry them.
4. **Reach.** Accessibility falls from 4.7 out of 5 in the Cape Metro to 1.0 in the Central Karoo. Beyond the Metro and the Garden Route the province is effectively car-only, and one touring route of six is rated Ready. Even CapeNature takes about 70% of its reservations by call centre. (The online travel agent point is in the hook.)
5. **Levers held elsewhere.** National government and its state-owned companies hold visas, air service agreements and the airport and port programmes. Decision rights split across three tiers, and no approved method exists for provincial tourism GDP and jobs.
6. Closer (one line, the summative turn into section 2.3): most of the five sit outside a marketing budget, and the two that bind hardest sit outside the province.

v7 blocks: exec [5] (all five items, absorbed in full); ch1/03 [10] (the "model's assumption" point only; its slot-headroom item stays with 1.3), [11], [12], [13], [14], [16], [17]; ch2/02 [20]; ch3/40 [5] (planning date and upside); ch1/02 [27], [42], [49]. No carried table or figure.

### 2.3 h2 "What 2.5 million arrivals would take" (about 330 words, plus the figure)

Beats:
1. The ask and the reframing. Wesgro commissioned a strategy to "double international tourist arrivals to the Western Cape by 2035" (Inception Report, Nov 2025, p4). The evidence reframes that ambition as growth to 2.5 million, paced by the gateway in the summer peak and by demand and conversion in the green season and beyond the Metro. This keeps the substance of the v7 lead, exec [1], and section 1.5's rule that "double" appears only as a quote of the mandate.
2. Three paths from 1,498,829 in 2025 to 2035: conservative 1,822,634, base 2,175,778 (about 2.2 million) and accelerated 2,516,282. They differ by intervention, not by demand potential.
3. What each path needs. The base path needs Emirates, Qatar, Ethiopian and Turkish Airlines to keep adding capacity and Wesgro's programmes to expand. That implies 3.8% a year. The accelerated path also needs direct India and China routes, plus dedicated activation in India, China, the USA and the Gulf. That implies 5.3% a year. Cite both rates to (Market Assessment Report, May 2026, p19), as ch1/03 [20] and ch2/01 do; they are printed rates, not this report's computation, so they carry no "; computed". Without confirmed routes, volume reverts to base. Expand v7's short forms into full citations: (Demand-Side Analysis, Jun 2026, p19, p20).
4. **[figure ref: exec [23], fig_0_paths "Arrivals paths to 2035", carried verbatim with its callout and source line.]** It sits straight after beat 3. One sentence after it reads the chart: the base path meets the seat line before 2031, and only the accelerated path clears 2.5 million.
5. Where marketing works and where it does not. On the eleven full routes, marketing cannot make up for missing seats, because carriers raise fares instead. On the hub routes, at 65% to 72% load, it can. The hub markets also supply 206,584 of the 676,949 arrivals the base path adds, more than any other group. Expand `("Seasonality")` into the full MIDAS citation.
6. What faster-growing destinations did (the benchmark lesson that feeds all three pillars; section 2.1 holds it in full). Global tourism grows 3% to 5% a year under stable conditions. Chile grew 40.4% and Singapore 21% in 2024 against 11% for the world. The comparators that outgrew the world aimed institutions, marketing and air access at one binding constraint. For Chile that constraint was long-haul access. The Western Cape's has the same shape: seats into one gateway airport (ch2/03 [22], [23]; the earlier wording here gave Chile the "one gateway airport", which the source says of the Western Cape).
7. Closer: seats decide which path the province takes, and marketing decides how well they are filled.

v7 blocks: exec [1], [2], [22] (absorbed in full); ch3/40 [3], [4]; ch1/01 [1], [12], [13]; ch1/03 [19], [20]; ch3/10 [5]; ch2/03 [1], [9], [22], [23]. Figure: exec [23] here.

### 2.4 h2 "The strategy makes three shifts" (about 340 words)

Opening (inline enumeration, Michael's form): "The strategy makes three shifts, one for each pillar; first, demand work moves from awareness to conversion. Second, supply work moves from new attractions to seats and finished experiences. Third, the enabling work moves from separate mandates to shared decisions, capital and data."

1. **Pillar 1: Reshape demand.** The province is known in its mature markets, under-sold in its growth markets and hard to book outside its core. Three of the six focus areas were reworded toward conversion: green-season seats, bookable product and hub traffic already in the air. About 101,000 Indian and Chinese travellers a year already reach Cape Town through Gulf and African hubs. Precedent in one sentence: Singapore turns transit into visits through its stopover programme, and Melbourne uses its events calendar to steady demand and pull air capacity.
2. **Pillar 2: Transform supply.** Supply sets the ceiling on the growth case. The pillar keeps one capacity entry at the gateway, frequency and larger aircraft on the full routes ahead of runway relief. It adds five entries about reach, product and experience. Evidence: cruise brings about R1.79bn a year with Cape Town's berth at about 40% of its season capacity. The flagship sites are near their limits, Boulders near carrying capacity and Cableway queues up to three hours. (Not "one touring route of six" again: 2.2 Reach carries it.) The task is to turn existing assets into complete visitor experiences, not to build new attractions. Precedent: Chile treats air access as core economic infrastructure, with a permanent public-private air access fund.
3. **Pillar 3: Build enabling capability.** This pillar decides whether the other two can be delivered and shared, and it does so by answering four questions; first, who benefits. Twenty communities hold 18.4% of residents but receive a traced 0.02% to 0.04% of foreign direct spend. Second, who pays: the capital pipeline funds airports, ports, roads and rail, and none of it reaches tourism product. Third, who decides: visas and air service agreements sit nationally, so the province leads by escalation backed with evidence. Fourth, who measures: no approved method exists for provincial tourism GDP and jobs, and the 300,000 jobs ambition has no baseline. Precedent: New Zealand manages regional capacity to protect pricing, and the leading comparators measure value, not arrivals (ch2/03 [21]; the source has New Zealand recommending yield-based metrics, not reporting that it uses them).
4. Closer paragraph, and the section's last words: the three pillars make one case. Demand work fills seats only if the seats exist, and supply work pays only if the product can be booked. Both need the enabling base to last.

The process lines and the tree figure that used to follow the closer move to the head of 2.5. Placed here, they turned a summative close into a method note. The optional beat on what the evidence narrowed is dropped: 2.3 already carries the move from doubling to 2.5 million and 2.7 the jobs question, and the four-markets point is process.

v7 blocks: ch3/10 [1], [4], [5]; ch3/20 [2], [4], [5], [6]; ch3/30 [2], [4], [5]; ch3/40 [2], [8]; ch3/14 [5] (paraphrase only; the topline itself is in the Pillar 1 table); ch3/22 [3], ch3/26 [3] (paraphrase only); ch2/03 [16], [18], [19], [21], [22]. No carried figure. Paraphrase the toplines here; do not repeat them word for word, because the tables below carry them.

### 2.5 pagebreak, then h2 "Twenty focus areas at a glance" (about 90 words, plus the tree and three tables)

1. Process, compressed to two sentences and a pointer (this replaces exec [3], [8], [10] to [13]). The twenty focus areas come from testing the December 2025 hypothesis tree against the evidence. Its eighteen entries became twenty under the same three pillars and six themes: ten carried through as Validated and none was withdrawn. Section 1.4 sets out each change and the evidence behind it. This is also where the reader learns what the Disposition column means, so it belongs beside the tables.
2. **[figure ref: exec [9], fig_0_tree "The updated hypothesis tree", carried verbatim.]**
3. Lead-in of one or two sentences. Each table gives a focus area's disposition, the one-sentence finding that opens its Chapter 3 entry, unchanged, and the initiative that delivers it. Chapter 3 holds the evidence, the actions by tier and the benchmark precedent.
4. **[table ref: exec [17] "Pillar 1: Reshape demand"]**
5. **[table ref: exec [18] "Pillar 2: Transform supply"]**
6. **[table ref: exec [19] "Pillar 3: Build enabling capability"]**

All three tables are carried verbatim as refs: rows, message lines and source lines. They hold the twenty toplines that `qa_structure.py` check 4 requires. Tree and tables together form the one reference block in the summary, straight after the shifts, so the argument in 2.4 reads without a break and the initiative codes used in 2.6 and the decisions are defined before they appear. v7 blocks: exec [3], [8] (compressed), [9] (figure), [14] (pagebreak), [16] (compressed), [17], [18], [19].

### 2.6 pagebreak, then h2 "Seats and bookings move first" (about 330 words)

1. Topic sentence: air access and bookability move first, because every other lever runs through them.
2. Three phases. Activate (2027 to 2028) holds and adds seats on the full routes and builds the green-season calendar. It counts and closes the bookability gap, starts two or three inclusion pilots and sets up Steerco, the data protocol and the national escalation agenda. Expand (2029 to 2031) scales what works and meets the seat line at the 2030 mid-term review. Sustain (2032 to 2035) takes the direct route cases to carriers as runway capacity arrives. Gate 1, at the end of 2028, falls two years before the base path crosses the seat line.
3. Eighteen initiatives carry the plan, one per focus area except where one owner delivers two. Wesgro is accountable for twelve. DEDAT, the Department of Mobility, municipalities, LTOs and site operators lead the other six. Thirteen draw mainly on Wesgro's operating budget. None has yet been costed, and setting the rand bands is the first funding task (section 4.6).
4. The first 24 months, as one paragraph that opens: "Twelve actions can start in the first 24 months, nine of them inside Wesgro's current mandate and budget, in three strands; first, ..." The strands, each one or two sentences with owners and initiative codes kept in parentheses:
   - Seats and season, from 2027 H1. Air Access holds winter seats through joint green-season marketing with carriers on the full routes and tracks the runway quarterly (I6, I2). The Convention Bureau publishes a green-season events calendar and aims bids at May to September (I2).
   - Governance and baselines, from 2027 H1. The Wesgro CEO's office and DEDAT constitute Steerco and table the first escalation agenda (I15, I17). Research agrees the data-sharing protocol with ACSA, SA Tourism, Stats SA and Cape Town Tourism, runs a bookability census by district and requests visitor counts from the five flagship sites (I16, I3, I11). DEDAT commissions the labour analysis (I18).
   - Product and inclusion, from 2027 H2. Tourism packages the Garden Route and Route 62 with a shuttle transfer, and the Southern Line as a visitor product with the City and PRASA (I8, I9). It chooses two or three pilot communities, each with one live booking route before any promotion from 2028 H1 (I12, I3).
5. Closer: each action opens a seat, a baseline or a booking path a later initiative needs, and Steerco confirms owners and dates (section 4.5).

v7 blocks: exec [24], [25], [27], [28], [29], [30] (absorbed in full; the bold run-ins of [28] to [30] become the inline "first, second, third"); ch3/40 [9] to [12]; ch4/02 [3]; ch4/01 [4], [5]; ch4/05 [2], [3]; ch4/06 [2]. No carried table or figure. The 24-month table stays in section 4.5.

### 2.7 h2 "How the Board will track progress" (about 200 words, plus the table)

1. Topic sentence: the Board will judge the plan on seven impact indicators, and today only arrivals and spend carry a modelled value for 2035. (The earlier wording restated the carried table's message line, which the reader meets a few lines later.)
2. The structure: seven impact indicators, twenty-five outcome and thirty-six output indicators. Steerco receives a quarterly scorecard and the Board an annual outlook against both paths. Gates at the end of 2028 and 2031, a mid-term review in 2030 and a terminal evaluation in 2035 decide what each phase funds.
3. **[table ref: exec [34] "Impact indicators and targets", carried verbatim.]** It sits after beat 2.
4. Discuss the table, do not restate it. Spend has a modelled base path in constant 2024 rand. Jobs wait on the labour analysis, so the 300,000 ambition is tested before it becomes a target. The green-season share starts at 38.1%. The share outside the Metro has no baseline until the data protocol delivers one in 2027. The community share starts from a documented floor of R4m to R10m a year, with 1% (R259m) as a reference point, not an adopted target.
5. Closer: Gate 1 turns the missing baselines into targets, so the first two years must produce data as well as results. (The earlier closer repeated beat 4's point on jobs and the share outside the Metro.)

v7 blocks: exec [33] (absorbed in full); ch5/03 [2], [3], [7], [8], [10], [11]; ch4/07 [6], [7]. Table: exec [34] here. Keep "(section 5.3)" if the drafter points onward.

### 2.8 h2 "What could knock it off course" (about 220 words)

1. Topic sentence: ten of the fourteen material risks sit outside Wesgro's control. The response is early warning and a route to the tier that can act.
2. The one risk rated high on both likelihood and impact: restrictive bilateral air agreements and the US carrier cap. The response is an escalation agenda with stated asks, plus route work inside existing rights.
3. **Correction to v7.** exec [37] says "Three risks are rated medium likelihood and high impact". The register in section 4.8 rates six that way. Enumerate them in three pairs (inline form):
   - First, two sit with the national tier and ACSA. Runway relief may slip past about 2033 (quarterly milestone tracking, frequency and larger aircraft, George for domestic connections). Visa processing may not improve (escalation agenda, processing time tracked each year).
   - Second, two sit in the markets. Gulf hub disruption would cut connecting capacity (spread hub work across Dubai, Doha, Addis Ababa and Istanbul; keep direct-route cases ready). A downturn in the UK, Germany and the USA would hit 52% of overseas arrivals (rebalance activation toward Africa and the hub markets).
   - Third, two sit closer to delivery. Safety incidents or perception (safety gates before pilot launches, escalation to SAPS). A cut to Wesgro's operating budget, on which thirteen initiatives draw (rand bands and a stop list before Gate 1, which is decision 3).
4. **Second correction.** v7 names only climate as high likelihood and medium impact. The register also rates the collapse of LTO funding under MFMA Circular No. 131 that way. Climate: a climate risk register and itineraries routed around closures. LTO funding: stable funding agreements with a development mandate.
5. Close with Letsema's assessment and the pointer: likelihood and impact are Letsema's assessment, Steerco reviews the register each quarter and section 4.8 holds it in full. Summative line: the plan cannot remove these risks, but it can see them early and send each to the tier that can act.

v7 blocks: exec [36], [37] (absorbed in full, with the two corrections); ch4/08 [2], [3], [4] (rows 1 to 5, 7, 11, 12, 13). No carried table.

### 2.9 h2 "What the Board is asked to decide" (about 100 words new, plus the carried lists)

1. Bridge, one sentence: the Board is asked to take five decisions and to make two recommendations to the Provincial Minister, DEDAT and the municipalities.
2. **[ref: exec [39] "The Wesgro Board decides:"]**
3. **[ref: exec [40], the five decisions, numbered; decision 3 carries "[Open item: Wesgro Finance to give an indicative rand band for the first 24 months.]"]**
4. **[ref: exec [41] "The Board recommends to the Provincial Minister, DEDAT and the municipalities:"]**
5. **[ref: exec [42], the two recommendations, numbered]**
6. Closer (the story ends at the next decision): Gate 1, at the end of 2028, is where the Board next decides. It asks whether seats on the full routes have held, whether the bookability baseline exists and is moving, and whether any pilot has met its thresholds. (From ch4/02 [7]; write it as two sentences and drop the comma before the final "and".)
7. A `note` block that rewords exec [43] without "the October deck's". For example: "Several items remain open, from page references still to confirm to the source of the 250-call cruise plan and a provincial employment baseline. Each is marked in square brackets where it occurs and listed with an owner in the open-items register that accompanies this report." Keep 250.

All four decision blocks (exec [39] to [42]) are carried word for word as refs. The h2 replaces exec [38] "What Steerco and the Board are asked to decide", which runs to eight words and names Steerco, though the lists are the Board's.

---

## 3. Disposition of every v7 block (exec/01_summary.json)

| v7 block | Type | v8 disposition |
|---|---|---|
| [0] | h2 "The case in brief" | Dropped; the hook opens unheaded |
| [1] | lead | Absorbed: hook (1.5m to 2.5m) and 2.3 beat 1 (2.2m, gateway in summer, demand in green season) |
| [2] | p | Absorbed: hook (1.57m in the text; 1.44m and the arrivals-basis note in its footnotes), 2.3 beat 2 (model base and paths) |
| [3] | p | Compressed into 2.5 beat 1; detail lives in 1.4 lead [1] and [7] to [12] |
| [4] | h3 "Five constraints cap the case" | Replaced by h2 "The limits are physical and institutional"; "five constraints" kept in its first line |
| [5] | bullets | Absorbed as five prose paragraphs in 2.2, all citations kept |
| [6] | pagebreak | Dropped |
| [7] | h2 "Strategy on a page" | Replaced by h2 "The strategy makes three shifts" |
| [8] | p | Compressed into 2.5 beat 1 (ten Validated, none withdrawn) |
| [9] | figure fig_0_tree | Ref at the head of 2.5, before the pillar tables |
| [10] | h3 "How the tree changed since December" | Cut |
| [11], [12], [13] | p | Relocated (carries_all) to section 1.4: table "December entries and October changes" (ch1/04 [13]) and paragraphs ch1/04 [11], [12] |
| [14] | pagebreak | Reused before 2.5 |
| [15] | h2 "Twenty focus areas" | Replaced by h2 "Twenty focus areas at a glance" |
| [16] | p | Compressed to the 2.5 lead-in (beat 3) |
| [17], [18], [19] | tables | Refs in 2.5, verbatim |
| [20] | pagebreak | Reused before 2.6 |
| [21] | h2 "The growth case and its sequence" | Split into 2.3 and 2.6 |
| [22] | p | Absorbed in 2.3 (short citations written in full) |
| [23] | figure fig_0_paths | Ref in 2.3 after beat 3 |
| [24], [25] | p | Absorbed in 2.6 |
| [26] | h3 "The first 24 months" | Cut as a heading; content in 2.6 beat 4 |
| [27] to [30] | p | Absorbed in 2.6 beat 4 as one inline-enumerated paragraph |
| [31] | pagebreak | Dropped (renderer decides) or kept before 2.7 if 2.6 runs long |
| [32] | h2 "How progress will be measured" | Replaced by h2 "How the Board will track progress" |
| [33] | p | Absorbed in 2.7 |
| [34] | table "Impact indicators and targets" | Ref in 2.7 |
| [35] | h3 "The main risks" | Replaced by h2 "What could knock it off course" |
| [36], [37] | p | Absorbed in 2.8, with the two count corrections |
| [38] | h2 | Replaced by h2 "What the Board is asked to decide" |
| [39] to [42] | p, numbered | Refs in 2.9, word for word |
| [43] | p | Reworded as the closing `note` in 2.9 (drops "the October deck's", keeps 250) |

---

## 4. What is cut or compressed, and where it still lives

- **The study's process line**, "tested an eighteen-entry hypothesis tree against seven deliverables and four working analyses" (exec [3]). Compressed to one clause at the head of 2.5. Lives in section 1.4: lead [1], "The hypothesis tree" [7] to [12] and the phases [3] to [5].
- **The entry-by-entry account of how the tree changed** (exec [10] to [13]): the nine changes, the split of air access and cruise, the move of focus area 19, the new focus area 20 and the six rewordings with their December titles. Cut to two sentences and a pointer. Lives in section 1.4 (ch1/04 [11], [12] and the table "December entries and October changes", ch1/04 [13]). It also lives in each Chapter 3 entry's "October 2026" paragraph and in Appendix A1 (traceability table).
- **Disposition counts** (exec [8]: ten Validated, six Reworded, one each Refined, New, Moved and Flagged). Compressed to "ten carried through as Validated and none was withdrawn". The counts are visible in the tree figure and the three pillar tables, defined in section 1.5 [9] and counted in Appendix A1.
- **What each Chapter 3 entry contains** (exec [16]). Compressed to the lead-in in 2.5. Lives in section 1.5 [5] and Chapter 3.
- **The five-constraint bullet list** (exec [5]). Converted to prose, not cut. Every figure and citation stays.
- **The first-24-month detail** (exec [27] to [30]: three bold-led paragraphs). Compressed into one inline-enumerated paragraph with owners and codes. The full list with funding routes and what each action opens lives in section 4.5 (table "First-24-month actions and funding", ch4/05 [4]).
- **The phase detail** (exec [24]). Tightened. Lives in sections 3.4 [9] to [12] and 4.2 (Gantt figure fig_4_gantt and the phase paragraphs).
- **Risk detail** (exec [36], [37]). Rewritten with corrected counts and named in pairs. The full register of fourteen risks, with evidence, mitigation and owner, lives in section 4.8 (ch4/08 [4]).
- **The arrivals-measures reconciliation.** Not in the v7 summary beyond one sentence, and kept out of the text: the hook's footnote notes carry the 1.44m and say the model counts on a different basis, "as section 1.1 sets out". Section 1.1's closing note and Appendix A2 (new closing subsection, which now holds the table "Arrivals figures in circulation", per `s11_outline.md`) hold it, with the 1.2 box "Three arrivals measures".
- **The 2025 month-of-travel share.** The text gives October to March as between 61% and 62%, with the 2025 figure flagged provisional in its footnote; 1.2 [21] keeps the open item on the 2025 shares.
- **Headings retired:** "The case in brief", "Strategy on a page", "How the tree changed since December", "Twenty focus areas", "The growth case and its sequence", "The first 24 months", "How progress will be measured", "The main risks" and "What Steerco and the Board are asked to decide". No other module cites these headings; the Chapter 3 pillar openings say only that "the executive summary lists them with their initiatives", which stays true.

## 5. Knock-on edits outside this module (for the parent; not made here)

- Section 1.5 [4] describes the summary as "the growth case to 2035, the constraints that cap it, the twenty focus areas by pillar, the first 24 months and the headline indicators". It should add the three shifts, the risks and the Board's decisions.
- Section 1.5 [22]'s open item refers to "these five constraints". The v8 summary keeps them countable as five in 2.2, so the item still has a referent.
- The risk counts corrected in 2.8 (six rated medium likelihood and high impact; two rated high likelihood and medium impact) come straight from the section 4.8 register. Nothing in Chapter 4 changes.
