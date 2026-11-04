"""Chapter 3, Pillar 1: Reshape demand. Writes content/ch3/10_pillar1.json and 11_fa01.json to 16_fa06.json.
Sources: report/evidence/factsheet_t11.md, factsheet_t12.md, tree.md, discrepancies.md (3 November 2026)."""
from ch3_lib import theme, entry, write

T11 = "Theme 1.1 · Traveller, brand and proposition"
T12 = "Theme 1.2 · Source market growth and diversification"

# ---------------------------------------------------------------- pillar intro
intro = [
    {"type": "h2", "text": "3.1 Pillar 1: Reshape demand"},
    {"type": "lead", "text": "Demand is not what holds Pillar 1 back; conversion is. The province is known in its mature markets, under-sold in its growth markets and hard to book outside its core."},
    {"type": "p", "text": "The December tree gave the pillar one objective: break through the market, seasonality and spread ceilings by reshaping the brand toward new traveller segments (Current State Diagnostic, Dec 2025, p64). The evidence confirmed all three ceilings."},
    {"type": "bullets", "items": [
        "**Markets.** Five markets supplied 63% of overseas arrivals in 2025, and the UK, Germany and the USA supplied 52% between them (Demand-Side Analysis, Jun 2026, p13).",
        "**Seasons.** June held 6.4% of the year's international seats at Cape Town International in 2025, against 10.8% in December (MIDAS Aviation Market Assessment, Mar 2026, Seasonality).",
        "**Spread.** Most rural properties have no OTA presence and are invisible to the market (Infrastructure Report, Jul 2026, p95).",
    ]},
    {"type": "p", "text": "What changed between December and October is the diagnosis. The Market Assessment counts about 97 million high-value travellers in 34 markets with an interest in South Africa, of whom about 1.4 million convert into arrivals (Market Assessment Report, May 2026, p41). The Diagnostic had already named the constraint as conversion and access, not only awareness (Current State Diagnostic, Dec 2025, p30). Three of the six entries were reworded toward conversion: green-season seats, bookable product and hub traffic already in the air."},
    {"type": "p", "text": "Pillar 1 carries most of the base case. Between 2025 and 2035 the base case adds 676,949 arrivals (Market Assessment Report, May 2026, p20 to p23). The four hub markets supply 206,584, the mature markets 178,780, the acceleration markets 175,818, regional Africa 110,298 and the strategic group 5,469. None of it lands without seats, so the air access entry in Pillar 2 runs beside this pillar from the first phase."},
    {"type": "table", "caption": "Pillar 1 holds six focus areas: three carried through as Validated and three were reworded toward conversion.",
     "source": "Chapter 3 entries 1 to 6. Dispositions as recorded at the 14 October 2026 review [Summary of Findings, 14 Oct 2026, pp15 to 16: deck page reference to be confirmed].",
     "columns": [
         {"header": "Focus area", "width": 2.6, "align": "left"},
         {"header": "Disposition", "width": 1.1, "align": "left"},
         {"header": "What the evidence showed", "width": 3.4, "align": "left"},
         {"header": "Initiative", "width": 0.8, "align": "left"},
     ],
     "rows": [
         ["1 Respond to growth segment traveller preferences", "Validated", "Four segments with named home markets; the province scores 3.7 to 4.6 out of 5 on its ability to win them", "I1"],
         ["2 Create green-season demand with MICE and events", "Reworded", "June holds 6.4% of the year's seats; international meetings cluster from May to November", "I2"],
         ["3 Make the whole province findable and bookable", "Reworded", "The outer routes and every shortlisted community fall short on online bookability", "I3"],
         ["4 Convert India and China hub traffic", "Reworded", "About 101,000 travellers a year already fly in through Dubai, Doha and Addis Ababa", "I4"],
         ["5 Increase yield in mature markets", "Validated", "Five mature long-haul routes run above 80% load, and carriers on full routes raise fares before seats", "I1"],
         ["6 Build a regional foundation (Africa)", "Validated", "Regional routes run above 80% load; Nigerian and Ghanaian visitors spend R31,000 and R27,700 each", "I5"],
     ], "boldFirstCol": True},
]
write("10_pillar1.json", "3.1", "Pillar 1: Reshape demand", intro)

# ---------------------------------------------------------------- FA01
fa01 = {
    "kicker": f"{T11} · Focus area 1",
    "name": "Respond to growth segment traveller preferences",
    "topline": "Four traveller segments, each concentrated in named home markets, give Wesgro a sharper target than country alone, and the province scores 3.7 to 4.6 out of 5 on its ability to win them.",
    "hypothesis": [
        "**December 2025.** Respond to Growth Segment Traveller Preferences (Current State Diagnostic, Dec 2025, p64). The wording is unchanged in every reprint of the tree.",
        "**October 2026: Validated.** Four segments were confirmed against markets of high incidence. The Skift segmentation of March 2026 drove the disposition, and the Market Assessment carried it into the demand work.",
    ],
    "evidence_intro": ["The segmentation rests on a May 2025 survey of more than 25,000 outbound travellers in 17 priority markets (Skift Segmentation Analysis, Mar 2026, Research Methodology)."],
    "evidence_caption": "Four segments are sized, scored and tied to home markets, and the highest-yield segment is the smallest.",
    "evidence_source": "Skift Segmentation Analysis, Mar 2026 (working analysis, cited by section); Market Assessment Report, May 2026 (MA). Trip spend in the currency printed, which the documents do not name. The 1.4 million carries no year or source line.",
    "evidence_rows": [
        ["Four segments are sized", "Curious Explorers about 30m, Creative Connectors about 25m, Discerning Connoisseurs about 19m and Reflective Adventurers about 23m addressable long-haul travellers across 34 markets", "Skift, Executive Summary; MA p43"],
        ["The province can win them", "Ability-to-win 4.6, 4.1, 4.0 and 3.7 out of 5.0, scored on product fit, brand fit, competition and ease of air access", "Skift, Ability-to-Win Assessment"],
        ["Each segment has home markets", "Curious Explorers are 30% of UK and US travellers; Reflective Adventurers 33% of German; Creative Connectors 32% of Indian; Discerning Connoisseurs 40% of UAE", "Skift, Segment Incidence by Market; MA p43"],
        ["The smallest segment yields most", "Discerning Connoisseurs spend $8,500 to $14,000 a long-haul trip, three to four times the other segments", "Skift, segment 03; MA p51"],
        ["Each segment books differently", "Creative Connectors book 42% through OTAs; Discerning Connoisseurs 42% through luxury travel advisors and 6% through OTAs", "Skift, Travel Behaviour and Spend; MA p49, p52"],
        ["Conversion is the gap", "About 97 million addressable travellers across 34 markets; about 1.4 million convert into arrivals", "MA p41"],
    ],
    "evidence_after": [
        "Two limits qualify the word confirmed. The segmentation leaves out the domestic market and seven African markets, Nigeria, Kenya and Ghana among them, and Skift calls its findings directional rather than definitive (Skift Segmentation Analysis, Mar 2026, Research Methodology and Disclaimer). No Western Cape validation exists yet.",
        "Stakeholders also name segments outside the four: medical tourism, township culture, eco-adventure and international MICE (Stakeholder Insights Report, Mar 2026, p34, p35, p42, p45). These are product interests that cut across the segments, and the report treats them that way rather than as a fifth segment.",
    ],
    "recommendation": [
        "Wesgro should market by segment within market, not by market alone, and judge results by value as well as volume. The UK and Germany anchor the near term with a combined pool of about 12.5 million, and the USA is the largest single pool outside China (Skift Segmentation Analysis, Mar 2026, Strategic Implications). The Department of Economic Development asks for the same shift, toward a value and spend lens over arrivals (Stakeholder Insights Report, Mar 2026, p24).",
    ],
    "actions": [
        ["Wesgro", "Set segment targets inside each priority market: Curious Explorers in the UK and USA, Reflective Adventurers in Germany, Creative Connectors in India, Discerning Connoisseurs in the UAE", "Destination Marketing; Research"],
        ["Wesgro", "Move spend from broad awareness to trade-led conversion through each segment's own channels, from luxury advisors to mobile-first OTAs", "Destination Marketing; trade and OTA partners"],
        ["Wesgro", "Commission destination-specific research to validate the segments, extend it to the domestic and African markets and build the segments into brand tracking", "Research"],
        ["Partners", "Develop segment-matched product: heritage and township experiences, creative districts, private-access wine and food, and a certified wellness and trail network", "Product owners; CapeNature; SANParks; LTOs"],
        ["National", "Agree one segment frame with SA Tourism for long-haul campaigns, so provincial and national spend target the same travellers", "SA Tourism"],
    ],
    "benchmark": "New Zealand gives each priority market a role, such as the USA as its high-yield growth engine, and judges performance on revenue per visitor and length of stay over arrivals (Global Benchmarking Report, Mar 2026, p53, p55). The required change for the Western Cape is to replace the arrivals KPI with yield-based metrics and build partnerships with specialist distribution networks (p56).",
    "link": "**Initiative I1**, segment-led activation and yield in mature markets, carries this entry with focus area 5 (section 4.3). **Indicators** T1-01 international arrivals and T1-02 arrivals by market group at impact level, and T2-01 segment home-market arrivals at outcome level (section 5.2).",
}
blocks = theme("3.1.1", "Traveller, brand and proposition", [
    "The first theme is about whom the Western Cape sells to, when and how. It holds three focus areas: the segments, the green season and the bookability of the province. The theme name carries through from December unchanged.",
]) + entry(fa01, pagebreak=False)
write("11_fa01.json", "3.1.1", "Respond to growth segment traveller preferences", blocks)

# ---------------------------------------------------------------- FA02
fa02 = {
    "kicker": f"{T11} · Focus area 2",
    "name": "Create green-season demand with MICE and events",
    "topline": "The green season is a seat problem and an events problem at once: June holds 6.4% of the year's international seats, while international meetings already cluster in the months leisure travel leaves empty.",
    "hypothesis": [
        "**December 2025.** Develop the Seasonality and Spread Proposition (Current State Diagnostic, Dec 2025, p64), reprinted from March 2026 as Develop seasonality, spread and Mega events proposition (Stakeholder Insights Report, Mar 2026, p7).",
        "**October 2026: Reworded.** June holds 6.4% of seats, and ICCA meetings cluster from May to November. Spread moved to focus areas 3 and 10, and business events replaced mega events as the lever. MIDAS's seasonality analysis and the Demand-Side MICE landscape drove the change.",
    ],
    "evidence_intro": ["Seats and visitors both fall away from April to September. Business events do not."],
    "evidence_caption": "Leisure demand and seats trough from May to September, while international meetings peak from September to November.",
    "evidence_source": "MIDAS Aviation Market Assessment, Mar 2026 (scheduled seats); Current State Diagnostic, Dec 2025 (Diag; Wesgro Visitor Tracking Survey 2024, while the Market Assessment, p25, prints the same split on a Cape Town overseas air-arrivals basis); Demand-Side Analysis, Jun 2026 (DSA); Stakeholder Insights Report, Mar 2026 (SIR). The ICCA months are summed from the printed monthly counts. The 2025 ICCA row of 65 covers Stellenbosch and Cape Town and is not comparable.",
    "evidence_rows": [
        ["June has the fewest seats", "June 6.4% of 2025 international seat capacity at Cape Town International; May to September 6.4% to 6.9% a month; November 10.3% and December 10.8%", "MIDAS, Seasonality"],
        ["Visitors follow the seats", "61% of 2024 overseas visitors travelled from October to March and 39% from April to September", "Diag p32"],
        ["Meetings fill the trough", "109 of 136 ICCA meetings in Cape Town from 2022 to 2024 fell between May and November; September to November alone held 74", "DSA p37"],
        ["The meetings base is growing", "ICCA meetings 33 in 2022, 46 in 2023 and 58 in 2024 (41,571 participants); 37 UIA association meetings in 2025, 58% of South Africa's", "DSA p37, p38"],
        ["Business events lift yield", "International business-event delegates spend R6,400 a day; Cape Town hotel occupancy was 53% in June 2023", "DSA p34"],
        ["The venue confirms the gap", "June to August and December to January are structurally weak for MICE, and peak-date constraints lose events", "SIR p45, p46 (CTICC)"],
    ],
    "evidence_figures": [
        {"type": "figure", "id": "fig_3_fa02_months",
         "caption": "International meetings peak from September to November, when seats and overseas visitors are still climbing out of the winter trough.",
         "source": "MIDAS Aviation Market Assessment, Mar 2026, Seasonality (share of 2025 international seat capacity at Cape Town International); Demand-Side Analysis, Jun 2026, p12 (month of travel, Western Cape overseas visitors, 2025) and p37 (ICCA meetings in Cape Town by month, 2022 to 2024, shares of 136 computed from the printed counts).",
         "chart": {"type": "line",
                   "categories": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
                   "series": [
                       {"name": "Seats", "values": [9.8, 8.8, 9.7, 7.8, 6.9, 6.4, 6.9, 6.9, 6.9, 8.7, 10.3, 10.8], "color": "#0B3C5D"},
                       {"name": "Visitors", "values": [11.5, 9.9, 10.3, 6.9, 6.8, 6.1, 6.7, 6.5, 7.0, 9.2, 11.3, 12.7], "color": "#7A9E7E"},
                       {"name": "Meetings", "values": [0.7, 2.9, 3.7, 5.1, 8.8, 4.4, 6.6, 5.9, 17.6, 19.9, 16.9, 7.4], "color": "#E07A1F"}],
                   "unit": "%", "yMin": 0,
                   "footnote": "Share of the year by month. Seats and visitors 2025; meetings 2022 to 2024. Printed visitor shares sum to 104.9%."}},
    ],
    "evidence_after": [
        "Two limits matter. The baseline the report uses is the printed 61% to 39% split for 2024; the 65% October to March share in earlier project material appears in no deliverable [Summary of Findings, 14 Oct 2026: source of the 65% to confirm]. And only conferences are measured: meetings are absent from provincial statistics, incentive volumes are unverified and exhibitions are unquantified (Demand-Side Analysis, Jun 2026, p36).",
    ],
    "recommendation": [
        "Wesgro should build an April to September events spine and sell it with the seats. The Diagnostic proposed the spine itself, anchored on a small set of flagship weeks, with green-season flight, stay and experience packages sold through airline and trade partners (Current State Diagnostic, Dec 2025, p32). The Demand-Side Analysis adds the routes by segment: off-peak conference bids in sectors where the province is strong, cooler-season incentive packages for Indian and Gulf planners, and winter midweek packages for corporate meetings (Demand-Side Analysis, Jun 2026, p40).",
    ],
    "actions": [
        ["Wesgro", "Publish a green-season events calendar and aim Convention Bureau bids at May to September in the province's strongest sectors", "Convention Bureau; Destination Marketing"],
        ["Wesgro", "Package green-season flight, stay and experiences with airlines and trade, and test cooler-season incentive packages with Indian and Gulf planners", "Air Access; Destination Marketing; airlines"],
        ["Wesgro", "Measure meetings, incentives and exhibitions, which provincial statistics do not cover today", "Research; CTICC"],
        ["Partners", "Programme lifestyle events in December and January and keep peak dates for international events; market flower, fynbos and whale events earlier", "CTICC; Overberg and West Coast LTOs"],
        ["Partners", "Agree one event acquisition and calendar strategy across Wesgro, the Convention Bureau, the City and the Province", "City of Cape Town; DEDAT"],
        ["National", "Ease visas for regional African delegates, whose event demand the venue operator rates as visa-constrained", "Home Affairs; SA National Convention Bureau"],
    ],
    "benchmark": "Victoria curates a portfolio of global, cultural, regional and business events that generate repeat, predictable demand spikes across the year, and Melbourne's monthly arrivals stay between 7% and 12% of the year (Global Benchmarking Report, Mar 2026, p17, p18). The required change for the Western Cape is a unified event acquisition and calendar strategy across Wesgro, the Convention Bureau, the City and the Province, with a proactive conference bidding pipeline (p20).",
    "link": "**Initiative I2**, green-season events and business-events calendar (section 4.3). **Indicators** T1-05 green-season share at impact level, and T2-02 ICCA meetings and T2-03 May to September seat share at outcome level (section 5.2).",
}
write("12_fa02.json", "3.1.1", "Create green-season demand with MICE and events", entry(fa02))

# ---------------------------------------------------------------- FA03
fa03 = {
    "kicker": f"{T11} · Focus area 3",
    "name": "Make the whole province findable and bookable",
    "topline": "Outside the Cape Peninsula, the Winelands and the Garden Route, most product cannot be booked where travellers book, so interest the province has already earned has nowhere to land.",
    "hypothesis": [
        "**December 2025.** Facilitate Adoption Along the Path to Purchase (Current State Diagnostic, Dec 2025, p64).",
        "**October 2026: Reworded.** Community product is unbookable, CapeNature takes about 70% of its reservations by phone and rural stock has OTA gaps. The focus moved from source-market platforms to the province's own product being invisible and unbookable. The Inclusion Plan, the stakeholder interviews and the Infrastructure Report drove the change.",
    ],
    "evidence_caption": "Bookability holds on the three core routes and falls away on the outer routes and in every shortlisted community.",
    "evidence_source": "Infrastructure Report, Jul 2026 (IR; the ~40% has no printed scope or source); SME and Community Inclusion Plan, Sep 2026 (SCIP; ratings compiled from the community profiles, LTO confirmation outstanding); Stakeholder Insights Report, Mar 2026 (SIR). The 70% is CapeNature's own reservation mix, not a provincial share.",
    "evidence_rows": [
        ["Three of six routes are bookable", "Digital and bookability rated Ready on the Cape Peninsula, Garden Route and Cape Winelands routes; Developing on the Whale Coast; Gap on the West Coast and Route 62", "IR p30, p40, p51, p62, p73, p84"],
        ["Rural stock is invisible", "Most rural properties have no OTA presence; outer-district stock has near-zero visibility on booking platforms", "IR p93, p95"],
        ["Small operators lack booking", "About 40% or more of smaller operators lack online booking, a gap no capital programme addresses", "IR p32"],
        ["No community is bookable", "None of 19 profiled communities rates Ready on digital and bookability; 8 rate Developing and 11 Gap", "SCIP p20 to p26, p40 to p51"],
        ["Community product sells by phone", "Four Zwelihle guides sell by phone with no shared booking channel; Visit Knysna lists nine township guides as phone contacts", "SCIP p34, p47"],
        ["Large attractions rely on phones", "CapeNature takes about 70% of its reservations through its call centre rather than its online platform", "SIR p42"],
    ],
    "evidence_after": [
        "No deliverable counts bookable products. The platform scan planned at inception produced no output (Inception Report, Nov 2025, p15, p17), so the indicator this entry needs most, the share of provincial product listed on OTAs by district, has no baseline yet [bookable-product count by district: Wesgro Research to build; see section 5.4].",
    ],
    "recommendation": [
        "Wesgro should treat bookability as infrastructure: count it, close it district by district and then place it on the platforms each market uses. The Inclusion Plan sets a community's first deliverable as one live booking route, published operating dates, a named customer contact and a simple record of bookings and local revenue (SME and Community Inclusion Plan, Sep 2026, p33). Growth markets book on their own platforms: Trip.com and Fliggy in China, MakeMyTrip in India and Almosafer in the Gulf (Demand-Side Analysis, Jun 2026, p45, p47, p49).",
    ],
    "actions": [
        ["Wesgro", "Run a bookability census of provincial product by district and publish it as the baseline", "Research; LTOs"],
        ["Wesgro", "Run a digital onboarding drive for small operators and cellars on the West Coast, Route 62 and the Overberg", "Tourism; district municipalities"],
        ["Wesgro", "Deepen OTA partnerships with Trip.com, Almosafer and Booking.com, and list packaged regional itineraries on them", "Destination Marketing; OTAs"],
        ["Partners", "Give each pilot community one live booking route before any promotion (focus area 13)", "LTOs; community sellers"],
        ["Partners", "Move CapeNature reservations online and complete cashless payments at reserve level", "CapeNature"],
        ["National", "Extend rural broadband under SA Connect, and lift the national rule that blocks bank-card payments on the George bus", "National government"],
    ],
    "benchmark": "New Zealand packages regional clusters into bookable long-haul itineraries and pairs regional operators with specialist global travel designers (Global Benchmarking Report, Mar 2026, p55). The transferable lesson the deck draws for the Western Cape is to use Cape Town as a gateway that spreads value across the province through bookable regional experiences (p51).",
    "link": "**Initiative I3**, bookable province programme (section 4.3); the community booking routes run through **I12** (focus area 13). **Indicators** T2-04 share of operators bookable online and T2-05 CapeNature online booking share (section 5.2).",
}
write("13_fa03.json", "3.1.1", "Make the whole province findable and bookable", entry(fa03))

# ---------------------------------------------------------------- FA04
fa04 = {
    "kicker": f"{T12} · Focus area 4",
    "name": "Convert India and China hub traffic",
    "topline": "About 101,000 Indian and Chinese travellers a year already reach Cape Town through Gulf and African hubs, and with no direct Indian route likely before 2030, converting that flow is the lever available now.",
    "hypothesis": [
        "**December 2025.** Pivot to Growth Markets (China, India, ME, ASEAN) (Current State Diagnostic, Dec 2025, p64).",
        "**October 2026: Reworded.** About 101,000 travellers a year already fly in via hubs. The Middle East and ASEAN left the title, and the lever narrowed from pivoting to converting traffic already in the air. The Demand-Side route-to-market work and MIDAS drove the change. The Middle East stays in the growth model's acceleration group.",
    ],
    "evidence_caption": "India and China reach Cape Town only through hubs, and the direct route that would change that is at least five years away.",
    "evidence_source": "Demand-Side Analysis, Jun 2026 (DSA); MIDAS Aviation Market Assessment, Mar 2026 (weighted GDS bookings, twelve months to November 2025); Market Assessment Report, May 2026 (MA, 2025 base). The 101,000 is the sum of the two printed estimates; the hub tables beneath them sum to 97,579 and carry no year.",
    "evidence_rows": [
        ["India flies in through hubs", "About 71,000 Indian travellers a year reach Cape Town via hubs; Addis Ababa and Dubai carry more than 80% of them", "DSA p48; MIDAS, Indian Market"],
        ["China flies in through hubs", "About 30,000 Chinese travellers a year via Dubai, Addis Ababa, Doha and Singapore (MIDAS: 29,600 in 2025)", "DSA p46; MIDAS, Chinese Market"],
        ["No Indian route before 2030", "Air India and IndiGo have no aircraft to spare before the end of the decade, and no South African airline can fly the sector", "MIDAS, Indian Market; DSA p48"],
        ["A Chinese route is a state decision", "Chinese routes follow government-to-government agreements; Guangzhou is the likely start, with China Southern or China Eastern", "MIDAS, Chinese Market"],
        ["Hub routes have room", "Load factor Dubai 72.3%, Addis Ababa 71.9% and Doha 65.2%, year to November 2025; the hub markets add 206,584 arrivals in the base case to 2035", "MIDAS, Seasonality; MA p20"],
        ["Growth is fast from a low base", "India 76,547 to 165,260 and China with Hong Kong 43,412 to 92,598, base case, 2025 to 2035", "MA p22; DSA p23"],
    ],
    "evidence_after": [
        "The accelerated case depends on what this entry cannot deliver alone. Without confirmed direct routes, the Demand-Side Analysis says, volume reverts to base (Demand-Side Analysis, Jun 2026, p20). The entry therefore works the hub flow now and builds the route case for later.",
    ],
    "recommendation": [
        "Wesgro should run India and China as conversion markets through the hubs and as relationship markets for the direct route. MIDAS recommends early relationship-building with Indian carriers and the Indian authorities, and treating China as a long-term investment in which awareness and indirect volume come before any non-stop service (MIDAS Aviation Market Assessment, Mar 2026, Indian and Chinese Market Opportunity). The Demand-Side Analysis adds activation inside Xiaohongshu, Douyin and MakeMyTrip, and trade-led conversion over broad awareness (Demand-Side Analysis, Jun 2026, p55).",
    ],
    "actions": [
        ["Wesgro", "Secure added frequency from Emirates, Qatar Airways and Ethiopian Airlines, with joint market support tied to Indian and Chinese sales", "Air Access; hub carriers"],
        ["Wesgro", "Activate inside Xiaohongshu, Douyin and MakeMyTrip with market-specific itineraries and Trip.com packages", "Destination Marketing; OTAs; trade"],
        ["Wesgro", "Build long-term route cases for the India and China corridors and keep a standing relationship with Indian carriers, China Southern and China Eastern", "Air Access"],
        ["Partners", "Ready the product for both markets: Mandarin and Indian-language guiding, Alipay and WeChat Pay, visible vegetarian options", "Product owners; attractions; hospitality bodies"],
        ["National", "Escalate visa processing for China and India, and the route designation for China that is decided government to government", "Home Affairs; Department of Transport"],
    ],
    "benchmark": "Singapore converts transit into visits through its Stopover Programme and Free Singapore Tour, run by the tourism board, Changi Airport Group and Singapore Airlines under one strategy (Global Benchmarking Report, Mar 2026, p40). New Zealand ties marketing budgets to named long-haul corridors and designs campaigns to support route breakeven, recording more than 16,000 incremental bookings and a return of about NZD 55m in 2023/24 (p54).",
    "link": "**Initiative I4**, India and China hub conversion (section 4.3), with the direct-route cases run under **I6** (focus area 7). **Indicators** T1-02 arrivals by market group at impact level and T2-06 India and China hub arrivals at outcome level (section 5.2).",
}
blocks = theme("3.1.2", "Source market growth and diversification", [
    "The second theme is about which markets grow the base. It holds one focus area per market group: India and China, which reach the province through hubs; the mature long-haul markets; and regional Africa. The theme name carries through from December unchanged.",
]) + entry(fa04, pagebreak=False)
write("14_fa04.json", "3.1.2", "Convert India and China hub traffic", blocks)

# ---------------------------------------------------------------- FA05
fa05 = {
    "kicker": f"{T12} · Focus area 5",
    "name": "Increase yield in mature markets",
    "topline": "The mature markets already pay the most and fill the fullest routes, so growth there comes from more value per visitor and more seats on existing routes, not from more marketing.",
    "hypothesis": [
        "**December 2025.** Increase Yield in Mature Markets (UK, Europe, N. America) (Current State Diagnostic, Dec 2025, p64).",
        "**October 2026: Validated.** Full routes. The October title drops the list of markets. MIDAS drove the disposition: the mature long-haul routes run above 80% load, and carriers on full routes raise fares before they add seats.",
    ],
    "evidence_caption": "The highest-spending visitors come from the slowest-growing markets on the fullest routes.",
    "evidence_source": "MIDAS Aviation Market Assessment, Mar 2026 (year to November 2025); Demand-Side Analysis, Jun 2026 (DSA); Market Assessment Report, May 2026 (MA, 2025 base). No deliverable carries fare, revenue-per-seat or yield data.",
    "evidence_rows": [
        ["Five mature routes are full", "Load factor Newark 88.6%, Atlanta 84.3%, Frankfurt 83.0%, Heathrow 83.0% and Washington 80.2%; eleven of the 27 tabled routes run above 80%", "MIDAS, Seasonality"],
        ["Carriers price before they add", "Rather than increase capacity, carriers will seek higher selling fares rather than add new services", "MIDAS, In Conclusion"],
        ["Mature visitors spend most", "Average spend in the province USA R32,900, UK R26,500 and Germany R25,600, against Zimbabwe R8,500 (2024)", "DSA p14"],
        ["The province earns a premium", "13% to 16% of national arrivals by quarter in 2025, but 20% to 27% of national foreign direct spend", "DSA p11"],
        ["Five markets dominate", "The top five supplied 63% of overseas arrivals in 2025, and the UK, Germany and USA 52%", "DSA p13"],
        ["Growth is steady", "Mature group 587,287 to 766,067 arrivals in the base case, 2025 to 2035", "MA p21; DSA p22"],
    ],
    "evidence_after": [
        "The yield lever rests on MIDAS's reading of carrier behaviour, and no deliverable models a yield uplift. The entry therefore sets yield as an indicator to establish, not a target to hit, until spend per visitor by market is tracked every year [yield baseline: SAT spend per visitor by market as an annual series; only 2024 is printed].",
    ],
    "recommendation": [
        "Wesgro should protect share and raise value per visitor in the mature markets, and work the full routes for frequency and gauge before it chases new ones. The Demand-Side Analysis frames the job as protecting share, increasing yield and driving regional dispersal while new growth markets are developed (Demand-Side Analysis, Jun 2026, p17). MIDAS sees tactical room for added frequency on some routes and larger aircraft from some airlines (MIDAS Aviation Market Assessment, Mar 2026, In Conclusion).",
    ],
    "actions": [
        ["Wesgro", "Make the case to carriers on the five full routes for added frequency or larger aircraft, backed by green-season marketing", "Air Access; airlines"],
        ["Wesgro", "Sell Discerning Connoisseur product through luxury advisors and high-end operators in the UK, USA, Germany, France and Switzerland", "Destination Marketing; trade"],
        ["Wesgro", "Add a yield measure, spend per visitor by market with length of stay, beside arrivals in Wesgro's own targets", "Research"],
        ["Partners", "Invest in premium product outside the Metro and in the midscale branded accommodation the province lacks (focus areas 11 and 15)", "Accommodation investors; hospitality bodies"],
        ["National", "Escalate the cap on US carriers, the unsigned Open Skies agreement and the bilateral agreements that limit airlift", "Department of Transport"],
    ],
    "benchmark": "New Zealand runs yield-based performance, putting revenue per visitor and length of stay ahead of arrivals growth and selling premium regional itineraries through specialist travel designers (Global Benchmarking Report, Mar 2026, p55). Its total visitor spend grew 9.2% in the year to March 2025, against arrivals growth of 5.9% (p53).",
    "link": "**Initiative I1**, segment-led activation and yield in mature markets (section 4.3), with the frequency case run under **I6** (focus area 7). **Indicators** T1-03 direct foreign spend at impact level and T2-07 mature-market spend per visitor at outcome level (section 5.2).",
}
write("15_fa05.json", "3.1.2", "Increase yield in mature markets", entry(fa05))

# ---------------------------------------------------------------- FA06
fa06 = {
    "kicker": f"{T12} · Focus area 6",
    "name": "Build a regional foundation (Africa)",
    "topline": "Regional Africa is the province's steadiest volume and its least developed premium market: Zimbabwe and Namibia supply 62% of African arrivals, while Nigerian and Ghanaian visitors spend R31,000 and R27,700 each.",
    "hypothesis": [
        "**December 2025.** Build a Regional Foundation (Africa) (Current State Diagnostic, Dec 2025, p64).",
        "**October 2026: Validated.** Regional routes are full, and Nigerian and Ghanaian visitors spend R31,000 and R27,700 each. The Demand-Side African opportunity section, the Skift African memo and MIDAS's regional route loads drove the disposition.",
    ],
    "evidence_caption": "African demand is a Southern African volume base with two high-spending West African markets and regional routes above 80% load.",
    "evidence_source": "Demand-Side Analysis, Jun 2026 (DSA; SA Tourism 2024 Departure Survey and 2025 performance report); MIDAS Aviation Market Assessment, Mar 2026 (year to November 2025); Skift African Market Analysis, 16 Mar 2026 (working analysis, by section); Market Assessment Report, May 2026 (MA). The printed spend averages do not reproduce from the totals and visitor counts on the same slide; the report quotes the printed averages.",
    "evidence_rows": [
        ["A Southern African base", "323,971 African arrivals across 16 markets in 2024; Zimbabwe and Namibia supplied 62%", "DSA p27"],
        ["Two high-spend markets", "Spend per visitor Nigeria R31,000, Ghana R27,700 and Kenya R16,900; African visitors spent R4.2bn in 2025", "DSA p29, p30"],
        ["Regional routes are full", "Luanda 86.2% and 83.4%, Maputo 83.3%, Gaborone 82.3%, Mauritius 81.8% and Harare 81.3%; MIDAS names all five markets for added capacity", "MIDAS, Seasonality"],
        ["The pool is large", "Nigeria 310,000 to 510,000 and Kenya 240,000 to 400,000 addressable adult trips a year; Ghana 55,000 to 100,000", "Skift African, s3"],
        ["South Africa is considered", "10.9% consideration share among Nigerian and 13.4% among Kenyan outbound travellers, second only to Dubai in Kenya", "Skift African, s4.2, s4.3"],
        ["Regional growth is steady", "Regional group 292,514 to 402,812 arrivals in the base case, 2025 to 2035, with Kenya the strongest upside", "MA p23; DSA p24"],
    ],
    "evidence_after": [
        "Three cautions apply. Nigeria and Ghana have no row in the growth model, so no 2035 arrivals figure exists for the two highest-spending African markets [Nigeria and Ghana arrivals targets: not modelled; Wesgro Research to add both]. The Skift memo places Ghana in its watch tier for brand seeding rather than conversion (Skift African Market Analysis, 16 Mar 2026, s5). And regional travellers tend to stop in Johannesburg rather than continue to Cape Town (Stakeholder Insights Report, Mar 2026, p35).",
    ],
    "recommendation": [
        "Wesgro should run Africa as two markets: a regional volume base held through capacity and value, and a premium growth market in Nigeria and Kenya won through conversion. Skift makes Nigeria the priority for luxury, status-driven and conference travel and Kenya the priority for business mobility and premium urban breaks, both through premium activation and the trade (Skift African Market Analysis, 16 Mar 2026, s5). Regional demand also helps the green season, because trips are shorter in lead time and easier to convert (Current State Diagnostic, Dec 2025, p31).",
    ],
    "actions": [
        ["Wesgro", "Make the capacity case on the five full regional routes with Airlink, Ethiopian Airlines, Kenya Airways and the other regional carriers", "Air Access; airlines"],
        ["Wesgro", "Run premium, trade-led activation in Nigeria and Kenya for leisure, weddings and conferences with leisure extensions", "Destination Marketing; Convention Bureau; trade"],
        ["Wesgro", "Add Nigeria and Ghana to the growth model and commission consumer research for Botswana, Zambia, Ghana and Rwanda", "Research"],
        ["Partners", "Convert rest-of-Africa travellers who stop in Johannesburg with onward packages, and give regional delegates leisure extensions", "Cape Town Tourism; CTICC; tour operators; Cross-Border Road Transport Agency"],
        ["National", "Escalate visas for African markets, building on the 2024 Ghana visa waiver, and liberalisation of regional air routes", "Home Affairs; Department of Transport"],
    ],
    "benchmark": "Kenya draws 41% of its arrivals from Africa, mainly Uganda and Tanzania, and positions Nairobi as East Africa's aviation, diplomatic and business hub through Kenya Airways' regional network (Global Benchmarking Report, Mar 2026, p32, p34). The transferable changes the deck draws for the Western Cape are to treat MICE as a system lever and to align city, provincial and national actors around one gateway strategy (p35).",
    "link": "**Initiative I5**, regional Africa programme (section 4.3), with the regional capacity case run under **I6** (focus area 7). **Indicators** T1-02 arrivals by market group at impact level and T2-08 African arrivals and spend at outcome level (section 5.2).",
}
write("16_fa06.json", "3.1.2", "Build a regional foundation (Africa)", entry(fa06))
print("pillar 1 written")
