"""FIRST-DRAFT GENERATOR ONLY. After the figure check (4 Nov 2026) the JSON files in content/ch3 are the source of record; do not re-run this script.
Chapter 3, Pillar 2: Transform supply. Writes content/ch3/20_pillar2.json and 21_fa07.json to 26_fa12.json.
Sources: report/evidence/factsheet_t21.md, factsheet_t22.md, tree.md, discrepancies.md (3 November 2026)."""
from ch3_lib import theme, entry, write

T21 = "Theme 2.1 · Accessibility, connectivity and infrastructure"
T22 = "Theme 2.2 · Product and destination capacity"

intro = [
    {"type": "pagebreak"},
    {"type": "h2", "text": "3.2 Pillar 2: Transform supply"},
    {"type": "lead", "text": "Supply sets the ceiling on the growth case. The airport caps arrivals before its relief arrives, and outside the Metro the product exists but is hard to reach, book or stay in."},
    {"type": "p", "text": "The December tree asked the pillar to remove mobility, infrastructure and product constraints so as to expand the province's physical carrying capacity (Current State Diagnostic, Dec 2025, p64). The evidence confirmed the objective and located each constraint."},
    {"type": "bullets", "items": [
        "**The gateway.** Current air access caps inbound seats at 1.8 million, and the base case passes that ceiling at the 2030 year point (Demand-Side Analysis, Jun 2026, p21). New terminal space at Cape Town International is due about 2032 and the runway about 2033 (Infrastructure Report, Jul 2026, p103).",
        "**The regions.** Accessibility scores fall from 4.7 in the Cape Metro to 1.0 in the Central Karoo, and one touring route of six is rated Ready (Infrastructure Report, Jul 2026, p88 to p90, p29).",
        "**The product.** The constraint is less about creating new attractions and more about turning existing assets into complete, accessible visitor experiences (Infrastructure Report, Jul 2026, p114).",
    ]},
    {"type": "p", "text": "Two structural changes happened in this pillar. The December entry on air access and cruise split in two, because MIDAS gave air access its own evidence base. The Infrastructure Report found cruise to be a product and marketing lever, with Cape Town's berth at about 40% of its season capacity (Infrastructure Report, Jul 2026, p110). The entry on infrastructure, visa and safety deficits moved to Pillar 3 because its levers sit nationally (section 3.3.2)."},
    {"type": "p", "text": "The Infrastructure Report reads transport as a connectivity and dispersal challenge, not a province-wide capacity crisis, with Cape Town International the key gateway risk (Infrastructure Report, Jul 2026, p114). Pillar 2 follows that reading: one capacity entry at the gateway and five entries about reach, product and experience."},
    {"type": "table", "caption": "Pillar 2 holds six focus areas: the air entry was reworded, cruise is new and the four others carried through as Validated.",
     "source": "Chapter 3 entries 7 to 12. Dispositions as recorded at the 14 October 2026 review [Summary of Findings, 14 Oct 2026, pp15 to 16: deck page reference to be confirmed].",
     "columns": [
         {"header": "Focus area", "width": 2.6, "align": "left"},
         {"header": "Disposition", "width": 1.1, "align": "left"},
         {"header": "What the evidence showed", "width": 3.4, "align": "left"},
         {"header": "Initiative", "width": 0.8, "align": "left"},
     ],
     "rows": [
         ["7 Win direct routes and add seats on full routes", "Reworded", "Eleven of 27 routes run above 80% load, fares rise before seats, and runway relief lands about 2033", "I6"],
         ["8 Grow cruise calls and ports", "New", "Cape Town's berth runs at about 40% of season capacity; growth comes through product and marketing", "I7"],
         ["9 Accelerate tourism-enabling internal mobility", "Validated", "Accessibility falls from 4.7 in the Metro to 1.0 in the Central Karoo", "I8"],
         ["10 Support diversified route and product development", "Validated", "Assets outside the Metro are not turned into product, and one route of six is Ready", "I9"],
         ["11 Align visitor experience in-destination", "Validated", "No mid-scale branded tier sits between luxury estates and basic self-catering", "I10"],
         ["12 Balance impact on nature-based attractions", "Validated", "Boulders is near carrying capacity and Cableway queues reach three hours", "I11"],
     ], "boldFirstCol": True},
]
write("20_pillar2.json", "3.2", "Pillar 2: Transform supply", intro)

# ---------------------------------------------------------------- FA07
fa07 = {
    "kicker": f"{T21} · Focus area 7",
    "name": "Win direct routes and add seats on full routes",
    "topline": "Eleven of 27 international routes run above 80% load and carriers raise fares before seats, so the province must win frequency and larger aircraft now, ahead of runway relief in about 2033.",
    "hypothesis": [
        "**December 2025.** Close the Air Access and Cruise Capacity Gaps (Current State Diagnostic, Dec 2025, p64). The air half of the entry became this focus area and the cruise half became focus area 8.",
        "**October 2026: Reworded.** The October record gives the reason as 16 of 27 routes above 80% and fares before seats. MIDAS, the source, prints eleven routes above 80%; sixteen is the count at 75% or more, and the report uses both on that basis [Summary of Findings, 14 Oct 2026: the deck's basis for 16 to confirm]. MIDAS and the Infrastructure Report's air-access section drove the change.",
    ],
    "evidence_caption": "The network is full on its best routes, the airport is full at its runway, and relief lands after the base case passes the seat ceiling.",
    "evidence_source": "MIDAS Aviation Market Assessment, Mar 2026 (twelve months to November 2025; 76.0% is the printed network total and the 27 rows sum to 75.0%); Demand-Side Analysis, Jun 2026 (DSA); Infrastructure Report, Jul 2026 (IR).",
    "evidence_rows": [
        ["Routes are full", "11 of 27 tabled routes above 80% load and 16 at 75% or more; network load 76.0%", "MIDAS, Seasonality"],
        ["Fares before seats", "Carriers on full routes will seek higher fares rather than add services, though there is tactical room for added frequency and larger aircraft", "MIDAS, In Conclusion"],
        ["A record to build on", "17 mainline international routes added from 2015 to 2025, ahead of Santiago (14), Valencia (12) and Calgary (8)", "MIDAS, International Comparisons"],
        ["A seat ceiling in 2030", "Current air access caps inbound seats at 1.8 million; the base case passes it at the 2030 year point (1,802,929)", "DSA p21"],
        ["Relief lands late", "The single runway caps movements at about 30 an hour; ACSA's ~R11.3bn programme brings the international terminal about 2032 and the runway about 2033", "IR p102, p103"],
        ["Second gateways", "George is solved by 2028 (R310m, to about 2m passengers); Cape Winelands is an upside bet with no firm named carrier", "IR p104 to p109"],
    ],
    "evidence_after": [
        "The Infrastructure Report puts the timing problem in one line: the certain fix is the latest, and the earliest big-capacity option is the least certain (Infrastructure Report, Jul 2026, p109). No airline took part in the first phase of stakeholder engagement, so the carriers' own view of frequency and gauge is still to be tested (Stakeholder Insights Report, Mar 2026, p16).",
    ],
    "recommendation": [
        "Wesgro should split the air agenda by horizon. Until about 2032 the job is to fill and enlarge what already flies: frequency and larger aircraft on the full routes, hub-carrier capacity and the five regional routes MIDAS names. After that, the job is to have direct India and China route cases ready when runway capacity arrives. The Demand-Side Analysis lists the moves: added frequency from Emirates, Qatar Airways and Ethiopian Airlines, long-term route cases for India and China, and coordinated airline incentives through Cape Town Air Access (Demand-Side Analysis, Jun 2026, p54).",
    ],
    "actions": [
        ["Wesgro", "Run a seat-retention and frequency programme on the full routes, with joint marketing tied to route performance", "Air Access; Destination Marketing; airlines"],
        ["Wesgro", "Set up a public-private air access fund for route support, on the Chilean model", "Air Access; DEDAT; City of Cape Town; private sector"],
        ["Wesgro", "Treat runway delivery as the first risk: track approvals and milestones quarterly and commission a capacity-against-demand model to 2035", "Air Access; Research"],
        ["Partners", "Deliver the runway, terminals and George upgrade on the published dates; close the funding and name a carrier at Cape Winelands", "ACSA; Cape Winelands Airport"],
        ["National", "Escalate bilateral air service agreements, the cap on US carriers and immigration processing at Cape Town International", "Department of Transport; Home Affairs"],
    ],
    "benchmark": "Chile treated its gateway airport as economic infrastructure: a private concession funded a ~US$900 million expansion at Santiago, and international seats grew ~40% to 50% between 2013 and 2019 under open-skies agreements (Global Benchmarking Report, Mar 2026, p23, p25, p26). The required change for the Western Cape is a permanent, well-funded public-private air access fund and active lobbying for air service liberalisation (p28).",
    "link": "**Initiative I6**, route development and seat retention with a public-private air access fund (section 4.3). **Indicators** T1-01 international arrivals at impact level, and T2-09 seats and routes and T2-10 routes above 80% load at outcome level (section 5.2).",
}
blocks = theme("3.2.1", "Accessibility, connectivity and infrastructure", [
    "The first supply theme covers how visitors reach the province and move through it. It holds three focus areas: air access, cruise and internal mobility. The December entry on visa and safety deficits left this theme for section 3.3.2.",
]) + entry(fa07, pagebreak=False)
write("21_fa07.json", "3.2.1", "Win direct routes and add seats on full routes", blocks)

# ---------------------------------------------------------------- FA08
fa08 = {
    "kicker": f"{T21} · Focus area 8",
    "name": "Grow cruise calls and ports",
    "topline": "Cruise already brings about R1.79bn a year with Cape Town's berth at about 40% of its season capacity, so growth comes from ships, excursions and regional day stops, not from port capital.",
    "hypothesis": [
        "**December 2025.** Close the Air Access and Cruise Capacity Gaps (Current State Diagnostic, Dec 2025, p64), the cruise half of the entry.",
        "**October 2026: New.** The October record gives 79 calls in 2024/25 and a plan to 250. The Infrastructure Report's cruise and ports section drove the split from air access: cruise runs well below berth capacity and is a product and marketing lever, a different problem from the airport.",
    ],
    "evidence_caption": "Cape Town's berth has room, ship size and wind are the constraints, and port capital is going to freight.",
    "evidence_source": "Current State Diagnostic, Dec 2025 (Diag; Western Cape Cruise Liner Industry Economic Contribution 2024/25 Season, cited through the Diagnostic); Infrastructure Report, Jul 2026 (IR); Stakeholder Insights Report, Mar 2026 (SIR). The Diagnostic counts 79 vessels and the Infrastructure Report 83 calls for the same season; passengers and economic impact agree. Mossel Bay's 27 a season is its own figure; the Infrastructure Report prints 21.",
    "evidence_rows": [
        ["Calls and passengers", "79 vessels and 127,178 passengers in 2024/25, up from 67 vessels in 2023/24", "Diag p37"],
        ["A berth with room", "Cape Town's equipped berth ran at about 40% of a season capacity of 150 or more calls; 83 calls and R1.79bn economic impact in 2024/25", "IR p110"],
        ["Ship size and wind bind", "300m maximum ship length at the equipped berth; the South-Easter delays berthing; no shore power", "IR p110"],
        ["Regional ports extend the route", "Mossel Bay 21 calls and about 13,000 passengers, with a R22m reception facility opened in November 2025; Saldanha Bay 3 trial calls into an ore terminal", "IR p111"],
        ["Port capital is for freight", "Cape Town's container expansion and Saldanha's R4bn iron-ore expansion add no cruise capacity; the R22m Mossel Bay facility is the only cruise capital", "IR p112"],
        ["Packaging works", "Mossel Bay calls rose from four before COVID to 27 a season through closer coordination and better excursion packaging, with Wesgro credited", "SIR p20, p21"],
    ],
    "evidence_after": [
        "The plan to 250 calls in the October record appears in no deliverable. Cape Town's season capacity is about 150 calls, so 250 would need a second berth, a longer season or the regional ports counted in, and no document describes any of these [plan to 250 cruise calls: source, horizon and definition to confirm with Cruise Cape Town]. The report carries the 2024/25 baseline and holds the target open until the source is in hand.",
    ],
    "recommendation": [
        "Wesgro should grow cruise through ships, excursions and regional day stops. The Infrastructure Report's own conclusion is to grow it through product and marketing, not capital works (Infrastructure Report, Jul 2026, p112). Cape Town anchors the itinerary, and Mossel Bay and Saldanha Bay extend it west and east as day stops rather than home ports (p111). The Inception Report names home porting and expedition vessels as the segments that bring longer stays and higher local spend (Inception Report, Nov 2025, p9).",
    ],
    "actions": [
        ["Wesgro", "Market Cape Town to lines whose ships fit the 300m berth and to expedition and home-porting operators, with pre- and post-cruise stays", "Cruise Cape Town; Destination Marketing"],
        ["Wesgro", "Back Mossel Bay now with packaged excursions and line marketing; keep Saldanha Bay on watch until demand is proven", "Cruise Cape Town; Mossel Bay municipality"],
        ["Wesgro", "Put community and regional product on cruise-operator channels, starting with a bookable walk in the Knysna townships", "Cruise Cape Town; LTOs"],
        ["Partners", "Manage berth scheduling and wind delays at Cape Town, plan for shore power and review the 300m limit", "Transnet National Ports Authority; V&A Waterfront"],
        ["National", "Put cruise into port planning, since current Western Cape port capital carries no cruise capacity", "Transnet"],
    ],
    "benchmark": "The Benchmarking Report has no cruise case, and its final screening replaced the cruise criterion used at inception with ease of access and visas (Global Benchmarking Report, Mar 2026, p11; Inception Report, Nov 2025, p30). The nearest analogue is Singapore's stopover programme, in which the tourism board, the airport and the airline share one strategy to turn transit passengers into visitors (p40).",
    "link": "**Initiative I7**, cruise growth through product (section 4.3). **Indicator** T2-11 cruise calls and passengers at outcome level, with the target held open until the 250-call plan is sourced (section 5.2).",
}
write("22_fa08.json", "3.2.1", "Grow cruise calls and ports", entry(fa08))

# ---------------------------------------------------------------- FA09
fa09 = {
    "kicker": f"{T21} · Focus area 9",
    "name": "Accelerate tourism-enabling internal mobility",
    "topline": "Accessibility falls from 4.7 out of 5 in the Cape Metro to 1.0 in the Central Karoo, and beyond the Metro and the Garden Route the province is effectively car-only.",
    "hypothesis": [
        "**December 2025.** Accelerate Tourism-Enabling Internal Mobility (Current State Diagnostic, Dec 2025, p64).",
        "**October 2026: Validated.** Access decays from 4.7 to 1.0. The Infrastructure Report's comparative regional analysis and the Department of Mobility's evidence to the stakeholder programme drove the disposition. The 4.7 is the Metro's score on attractions and services; on transport it scores 5.0.",
    ],
    "evidence_caption": "Access falls away with distance from Cape Town, and the rail and road assets that exist are not run for visitors.",
    "evidence_source": "Infrastructure Report, Jul 2026 (IR; comparative regional analysis on a 1 to 5 scale); Stakeholder Insights Report, Mar 2026 (SIR; the theme count is reconstructed from the appendix tables, which print no tally).",
    "evidence_rows": [
        ["Access decays with distance", "Accessibility Cape Metro 4.7 (5.0 on transport), Cape Winelands 3.3, Garden Route 3.0, Overberg 2.0, West Coast 1.7, Central Karoo 1.0", "IR p88 to p90"],
        ["One corridor, mostly car-only", "The N2 is the only continuous inter-regional tourism corridor; beyond the Metro and the Garden Route the province is effectively car-only", "IR p98, p99"],
        ["Rail exists but not for visitors", "Metrorail runs 104 of 121 stations and 22.7m trips (FY2025), but no rail reaches the airport and the Southern Line's visitor branding dates to 2007", "IR p100"],
        ["The Metro's last mile is unfunded", "MyCiTi Phase 2 (R3.3bn) does not reach Chapman's Peak, Constantia or Cape Point south", "IR p32"],
        ["No shuttles between towns", "No inter-town shuttle on the Garden Route despite obvious demand; no public tourism transport between Hermanus, Stanford, Elim and Agulhas", "IR p90, p67"],
        ["Stakeholders rank it high", "18 insight rows from 8 of 16 organisations, 10 rated High, including public transport and airport transfer times", "SIR p22, p20 to p46"],
    ],
    "evidence_after": [
        "The Infrastructure Report's conclusion frames the entry: transport is primarily a connectivity and dispersal challenge, not a province-wide capacity crisis (Infrastructure Report, Jul 2026, p114). The Department of Mobility adds that mobility responsibilities are split across three tiers of government (Stakeholder Insights Report, Mar 2026, p23).",
    ],
    "recommendation": [
        "Wesgro should not try to build transport. It should make the transport that exists usable for visitors and aggregate the demand that makes shuttles viable. The Southern Line is a ready-made, low-cost scenic corridor through Muizenberg, Kalk Bay, Boulders and Simon's Town (Infrastructure Report, Jul 2026, p100). On the West Coast, operators say a shared shuttle needs demand aggregation and booking integration to work (Stakeholder Insights Report, Mar 2026, p41).",
    ],
    "actions": [
        ["Wesgro", "Package the Southern Line as a visitor product, with refreshed branding and day passes", "Tourism; Destination Marketing; City of Cape Town; PRASA"],
        ["Wesgro", "Aggregate demand and bookings for corridor shuttles, starting on the Garden Route and between Cape Town, Darling and the West Coast", "Tourism; district municipalities; private operators"],
        ["Wesgro", "Sell the transfer inside the itinerary on the N2 and R62 routes, so visitors without a car can buy the trip", "Destination Marketing; operators"],
        ["Partners", "Complete the Central Line recovery, MyCiTi Phase 2 and the unfunded last mile to Cape Point, with integrated ticketing", "City of Cape Town; PRASA; Department of Mobility"],
        ["Partners", "Take forward the Cape Town to George rapid rail assessment and extend the George public transport model", "Department of Mobility"],
        ["National", "Lift the national rule that blocks bank-card payments on the George bus, and fund passenger rail beyond the Metro", "National government; PRASA"],
    ],
    "benchmark": "No benchmark case carries an internal mobility lever with figures. The nearest is Chile, where a domestic air network links Santiago to Patagonia, Atacama, Valparaíso and the wine valleys, run as a designed portfolio rather than standalone attractions (Global Benchmarking Report, Mar 2026, p25, p27).",
    "link": "**Initiative I8**, corridor mobility (section 4.3). **Indicators** T1-06 share of arrivals and spend outside the Metro at impact level, and T2-12 accessibility score by district and T2-13 corridor transfer products at outcome level (section 5.2).",
}
write("23_fa09.json", "3.2.1", "Accelerate tourism-enabling internal mobility", entry(fa09))

# ---------------------------------------------------------------- FA10
fa10 = {
    "kicker": f"{T22} · Focus area 10",
    "name": "Support diversified route and product development",
    "topline": "The province does not lack attractions; it lacks finished experiences around them, with assets outside the Metro left without guides, interpretation or bookable product and one touring route of six rated Ready.",
    "hypothesis": [
        "**December 2025.** Support Diversified Route and Product Development (Current State Diagnostic, Dec 2025, p64).",
        "**October 2026: Validated.** Idle assets and cold zones. The Infrastructure Report's spatial maps and route scorecards drove the disposition, and 11 of the 16 organisations in the stakeholder programme raised the theme. Cold zones is the report's own term; idle assets paraphrases its finding that assets are inactivated or underused.",
    ],
    "evidence_caption": "Assets are spread across the province, but product, packaging and investment stop at the core routes.",
    "evidence_source": "Infrastructure Report, Jul 2026 (IR; route ratings are approximate and the asset count carries no year); Stakeholder Insights Report, Mar 2026 (SIR; organisation count reconstructed from the appendix tables).",
    "evidence_rows": [
        ["Assets are spread", "50,332 mapped tourism assets; the Cape Metro holds 40.3% and the five other districts the rest", "IR p2, p23"],
        ["Assets are not activated", "Overberg and West Coast marine and wildflower assets have no guided tours, interpretation centres or bookable product; the Central Karoo and northern inland are attraction deserts", "IR p93"],
        ["Cold zones in every district", "Industrial belts with zero tourism conversion in the Metro; the inland Garden Route north of the N2; the Rûens interior; the N1 transit corridor in the Central Karoo", "IR p24, p35, p68, p79"],
        ["One route is Ready", "Cape Peninsula Ready; Garden Route, Cape Winelands, Whale Coast and Route 62 Developing; West Coast and Cederberg Emerging", "IR p29, p39, p50, p61, p72, p83"],
        ["No capital for product", "Non-wine diversification in the Winelands is strategy, not committed capital; De Hoop lacks accommodation investment; Overberg year-round product is unfunded", "IR p54, p76"],
        ["Stakeholders see concentration", "11 of 16 organisations raised the theme; the offer is seen as concentrated around Cape Town and a narrow set of icons", "SIR p11"],
    ],
    "evidence_after": [
        "The Infrastructure Report's own conclusion is that the constraint is less about creating new attractions and more about turning existing assets into complete, accessible visitor experiences (Infrastructure Report, Jul 2026, p114). No deliverable counts the assets that have no product around them [assets with no bookable product or guided access, by district: needs the Wesgro supply database behind the 50,332 count].",
    ],
    "recommendation": [
        "Wesgro should deepen the three corridors closest to ready, the Garden Route, the Cape Winelands and the Overberg, and package the two outer routes as slow-travel products. The Infrastructure Report places the strongest regional opportunity in deepening existing corridors through connectivity, packaging and service depth (Infrastructure Report, Jul 2026, p114). Dispersal needs deliberate corridor investment, not organic spillover from Cape Town (p5). Stellenbosch and George can anchor regional business events (Demand-Side Analysis, Jun 2026, p41).",
    ],
    "actions": [
        ["Wesgro", "Package bookable multi-day itineraries on each of the six touring routes, starting with the Whale Coast east of Hermanus, Route 62 and the West Coast", "Tourism; Destination Marketing; LTOs"],
        ["Wesgro", "Activate cold-zone assets with guided tours, interpretation and bookable product, beginning with the marine and wildflower assets", "Tourism; CapeNature; SANParks; LTOs"],
        ["Wesgro", "Build regional conference offers in Stellenbosch and George, with stays before and after Cape Town events", "Convention Bureau"],
        ["Partners", "Invest in accommodation and service depth beyond Hermanus, in Route 62's secondary towns and beyond Langebaan and Paternoster (focus area 15)", "Accommodation investors; municipalities"],
        ["Partners", "Refresh flagship product: Robben Island beyond the prison tour; the Cableway's lower station", "Robben Island Museum; Table Mountain Aerial Cableway"],
        ["National", "Complete SA Connect rural broadband and SANParks precinct projects such as the R81.7m Agulhas lighthouse precinct", "National government; SANParks"],
    ],
    "benchmark": "Chile ran Santiago, Valparaíso, the wine valleys and Patagonia as one portfolio, which raised global awareness, earned revenue in the shoulder season and lengthened stays as visitors explored several regions (Global Benchmarking Report, Mar 2026, p27). The required change for the Western Cape is to sell experiences as curated journeys and move from asset marketing to experience-led packaging (p28).",
    "link": "**Initiative I9**, corridor product development (section 4.3). **Indicators** T1-06 share of arrivals and spend outside the Metro at impact level and T2-14 readiness by district at outcome level (section 5.2).",
}
blocks = theme("3.2.2", "Product and destination capacity", [
    "The second supply theme covers what visitors find once they arrive: product beyond the icons, the quality of the stay and the limits of the flagship sites. All three December entries carried through as Validated.",
]) + entry(fa10, pagebreak=False)
write("24_fa10.json", "3.2.2", "Support diversified route and product development", blocks)

# ---------------------------------------------------------------- FA11
fa11 = {
    "kicker": f"{T22} · Focus area 11",
    "name": "Align visitor experience in-destination",
    "topline": "The province offers luxury estates and basic self-catering with no mid-scale branded tier between them, and service, interpretation and language readiness thin out with distance from Cape Town.",
    "hypothesis": [
        "**December 2025.** Align Visitor Experience In-Destination (Current State Diagnostic, Dec 2025, p64).",
        "**October 2026: Validated.** Mid-scale gap. The Infrastructure Report's accommodation mapping, the stakeholder evidence on service quality and the Valencia and Singapore benchmarks drove the disposition. The gap is stated in words; no deliverable counts mid-scale rooms.",
    ],
    "evidence_caption": "The experience breaks at the middle of the accommodation market, at the service counter and at the arrival gate.",
    "evidence_source": "Infrastructure Report, Jul 2026 (IR); Stakeholder Insights Report, Mar 2026 (SIR); Demand-Side Analysis, Jun 2026 (DSA); Current State Diagnostic, Dec 2025 (Diag; Mentionlytics sentiment data).",
    "evidence_rows": [
        ["No mid-scale tier", "Province-wide, no midscale branded product sits between luxury estates and basic self-catering; mid-market stock is effectively absent outside Stellenbosch", "IR p95, p47"],
        ["Accommodation range thins", "Accommodation range Ready on three routes, Developing on the Whale Coast and Route 62, and Gap on the West Coast", "IR p30, p40, p51, p62, p73, p84"],
        ["A two-tier system", "Strong product sits where visitors cannot easily reach or afford it; accommodation readiness 4.7 in the Metro against 2.0 in the Central Karoo", "IR p89"],
        ["Service is uneven", "Mossel Bay calls restaurant quality and service a major weakness; CapeNature is wary of scaling international demand because service readiness is uneven", "SIR p20, p43"],
        ["Growth markets need adapting", "Limited Mandarin-language services; little visibility of vegetarian options or Indian-language guides; no Arabic-language booking or local-currency options", "DSA p51"],
        ["The arrival is the weak point", "The international airport is the most negative node in Cape Town's online mentions; immigration processing and peak-hour throughput need work", "Diag p22; DSA p54"],
    ],
    "evidence_after": [
        "Two measures are missing. No deliverable counts mid-scale rooms or beds [mid-scale room count by district: needs the Wesgro supply database or an accommodation audit], and none prints a visitor satisfaction score. The only accommodation figure in hand is a demand share: 3.6% of 2024 visitors stayed in hotels, against 17.4% in self-catering (Current State Diagnostic, Dec 2025, p27).",
    ],
    "recommendation": [
        "Wesgro should lead a province-wide quality and standards framework and make the investment case for mid-scale accommodation in secondary nodes. The Benchmarking Report assigns the framework to Wesgro in so many words: a province-wide quality and standards framework that aligns all tourism stakeholders under consistent benchmarks led by Wesgro (Global Benchmarking Report, Mar 2026, p42). Valencia shows the form: a provincial quality charter, phased by district, with certification visible on booking platforms (p49).",
    ],
    "actions": [
        ["Wesgro", "Set up a provincial quality charter, phased by district, with certification visible on booking platforms and support for SMMEs to comply", "Tourism; DEDAT; industry bodies"],
        ["Wesgro", "Prepare for growth markets: multilingual guiding, digital payments and culturally relevant product for Chinese, Indian and Gulf visitors", "Tourism; Destination Marketing"],
        ["Wesgro", "Make the investment case for mid-scale and conference-capable hotels in George and Mossel Bay, east of Hermanus and on Route 62 (focus area 15)", "Tourism; private investors"],
        ["Partners", "Close service and interpretation gaps at named sites: Robben Island interpretation, CapeNature service readiness, restaurant quality in Mossel Bay", "Attraction operators; municipalities; CATHSSETA"],
        ["National", "Improve immigration processing and peak-hour throughput at Cape Town International, and deliver the terminal relief due about 2032", "Home Affairs; ACSA"],
    ],
    "benchmark": "Singapore's tourism board used a hotel industry transformation map, a hotel rejuvenation fund and the Hotels Act to move the destination from short stopovers toward longer stays and higher spend (Global Benchmarking Report, Mar 2026, p41). Valencia's Qualitur programme and SICTED quality system raised service consistency, reputation and repeat visitation (p47).",
    "link": "**Initiative I10**, visitor experience and quality standards (section 4.3). **Indicator** T2-15 routes rated Ready at outcome level (section 5.2).",
}
write("25_fa11.json", "3.2.2", "Align visitor experience in-destination", entry(fa11))

# ---------------------------------------------------------------- FA12
fa12 = {
    "kicker": f"{T22} · Focus area 12",
    "name": "Balance impact on nature-based attractions",
    "topline": "Boulders is near carrying capacity and Cableway queues reach three hours, so growth at the flagship nature sites must come from managing flows and steering visitors to under-marketed reserves.",
    "hypothesis": [
        "**December 2025.** Balance Impact on Nature-Based Attractions (Current State Diagnostic, Dec 2025, p64).",
        "**October 2026: Validated.** Flagship limits. The stakeholder evidence on Boulders and Table Mountain and the Infrastructure Report's record of flagship congestion drove the disposition. The operators and the province state the limits; no deliverable prints a visitor cap or carrying-capacity figure for any flagship site.",
    ],
    "evidence_caption": "The flagship sites are at or near their limits, the overflow reserves are under-marketed and climate is already closing sites.",
    "evidence_source": "Stakeholder Insights Report, Mar 2026 (SIR; insight statements by organisation, not quotations); Infrastructure Report, Jul 2026 (IR).",
    "evidence_rows": [
        ["Boulders is near capacity", "Some nature-based attractions, Boulders among them, are already near carrying capacity, so more volume there is undesirable (Department of Economic Development)", "SIR p24"],
        ["The summit cannot grow", "Environmental restrictions limit permanent expansion on Table Mountain's summit; peak queues run up to three hours up and two hours down", "SIR p36; IR p28"],
        ["Overflow is under-marketed", "Peak-season congestion at flagship sites while overflow reserves remain under-marketed", "IR p88"],
        ["Tourism funds conservation", "CapeNature's ecotourism income pays for alien clearing, fire response and species protection, and public funding alone will not suffice", "SIR p43, p44"],
        ["Climate already bites", "Flooding, fire and heat are closing CapeNature sites; weather cancellations cost Robben Island roughly R16m a year", "SIR p43, p33"],
        ["Seasonal windows are narrow", "Whale season peaks from September to November; climate change threatens the predictability of the wildflower season", "IR p67, p64"],
    ],
    "evidence_after": [
        "No deliverable prints annual visitors or permitted capacity for Table Mountain, Boulders, Robben Island, Cape Point or Kirstenbosch [flagship visitor counts and capacity: request from SANParks, the Cableway, Robben Island Museum and SANBI]. The only printed daily cap in hand is the City's permit system at the Witzands dunes near Atlantis, which is 80% pre-booked online (SME and Community Inclusion Plan, Sep 2026, p41).",
    ],
    "recommendation": [
        "Wesgro should stop marketing volume to the flagship sites and use them as the hook that sends visitors elsewhere. The Department of Economic Development wants further growth directed to under-visited parts of the province rather than constrained flagships (Stakeholder Insights Report, Mar 2026, p24). The Peninsula route's own opportunities are to disperse visitors beyond the highest-volume attractions and to expand shoulder-season experiences (Infrastructure Report, Jul 2026, p30). The site operators hold the flow tools, from digital flow management to tiered pricing (Demand-Side Analysis, Jun 2026, p3; Stakeholder Insights Report, Mar 2026, p44).",
    ],
    "actions": [
        ["Wesgro", "Market the under-used reserves, and the Southern Line to Boulders and Simon's Town, as alternatives to peak-hour flagship visits", "Destination Marketing; CapeNature; PRASA"],
        ["Wesgro", "Request visitor counts and capacity for the five flagship sites and publish them as the baseline", "Research; site operators"],
        ["Wesgro", "Report spend per visitor and length of stay for nature product alongside visitor numbers", "Research"],
        ["Partners", "Introduce digital visitor-flow management at the Cableway, Boulders and Cape Point, and tiered pricing where mandates allow", "Table Mountain Aerial Cableway; SANParks; CapeNature"],
        ["Partners", "Make reserve product climate-resilient by reassessing asset formats and siting", "CapeNature"],
        ["National", "Agree a visitor management plan for Table Mountain National Park and Boulders with the City and the operators", "SANParks"],
    ],
    "benchmark": "Kenya treats conservation as national economic infrastructure, with tourism-funded conservation financing and community conservancies that sustain demand and environmental integrity (Global Benchmarking Report, Mar 2026, p33). New Zealand uses land-use controls and premium curation on the principle that capacity discipline protects long-term pricing power (p55).",
    "link": "**Initiative I11**, flagship site demand management (section 4.3). **Indicator** T2-16 peak queue at the Cableway at outcome level, with flagship visitor counts added once the baseline is in hand (section 5.2).",
}
write("26_fa12.json", "3.2.2", "Balance impact on nature-based attractions", entry(fa12))
print("pillar 2 written")
