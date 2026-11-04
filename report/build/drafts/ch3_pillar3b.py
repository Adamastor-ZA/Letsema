"""FIRST-DRAFT GENERATOR ONLY. After the figure check (4 Nov 2026) the JSON files in content/ are the source of record; do not re-run this script.
Chapter 3, Pillar 3: intro (30_pillar3.json) and theme 3.2, focus areas 16 to 20 (34_fa16.json to 38_fa20.json).
Sources: report/evidence/factsheet_t32.md (4 November 2026), factsheet_t31.md, tree.md, jobs_research.md."""
from ch3_lib import theme, entry, write

T32 = "Theme 3.2 · Governance and leadership"

intro = [
    {"type": "pagebreak"},
    {"type": "h2", "text": "3.3 Pillar 3: Build enabling capability"},
    {"type": "lead", "text": "Pillar 3 decides whether the other two can be delivered and shared: who benefits, who pays, who decides and who measures."},
    {"type": "p", "text": "The December tree asked the pillar to build an inclusive, well-governed tourism system that supports sustainable growth, returns and development (Current State Diagnostic, Dec 2025, p64). The evidence found each part of that system thin."},
    {"type": "bullets", "items": [
        "**Inclusion.** Twenty township and rural communities hold 18.4% of the province's residents but receive a traced 0.02% to 0.04% of foreign direct spend (SME and Community Inclusion Plan, Sep 2026, p5).",
        "**Investment.** The capital pipeline funds airports, ports, roads and rail, and none of it reaches tourism product, bookability or community assets (Infrastructure Report, Jul 2026, p32 to p87).",
        "**Governance.** Visas and air service agreements sit with national government, and mobility mandates are split across three tiers (Current State Diagnostic, Dec 2025, p58; Stakeholder Insights Report, Mar 2026, p23).",
        "**Measurement.** No approved methodology exists for provincial tourism GDP and jobs (Stakeholder Insights Report, Mar 2026, p37).",
    ]},
    {"type": "p", "text": "This pillar changed most between December and October, and now holds eight focus areas. The inclusion entry was refined and held at concept level. Sustainability was reworded to climate risk and local destination funding, and institutional review to three-tier alignment. The deficits entry moved in from Pillar 2, and workforce skills was added and flagged as untested."},
    {"type": "p", "text": "The evidence here is mostly qualitative. It rests on attributed stakeholder statements, the Diagnostic's one-slide tier table, the Inclusion Plan and the Infrastructure Report's gap tables, so this pillar carries more open items than the other two."},
    {"type": "table", "caption": "Pillar 3 holds eight focus areas, the widest spread of dispositions in the tree.",
     "source": "Chapter 3 entries 13 to 20. Dispositions as recorded at the 14 October 2026 review [Summary of Findings, 14 Oct 2026, pp15 to 16: deck page reference to be confirmed].",
     "columns": [
         {"header": "Focus area", "width": 2.6, "align": "left"},
         {"header": "Disposition", "width": 1.1, "align": "left"},
         {"header": "What the evidence showed", "width": 3.4, "align": "left"},
         {"header": "Initiative", "width": 0.8, "align": "left"},
     ],
     "rows": [
         ["13 Embed local destination bodies for community inclusion", "Refined", "Organisation, not distance or product, binds in eleven of twenty communities", "I12"],
         ["14 Manage climate risk and sustainable tourism", "Reworded", "Climate already closes sites and routes; local tourism bodies depend on disrupted municipal funding", "I13"],
         ["15 Crowd in capital with targeted investment strategies", "Validated", "No committed capital reaches tourism product, bookability or community assets", "I14"],
         ["16 Align institutional stakeholders across all three tiers", "Reworded", "Air rights and visas sit nationally, and mandates are split across three tiers", "I15"],
         ["17 Strengthen industry and government collaboration", "Validated", "Fifteen of sixteen organisations raised collaboration, and JAMS already exists", "I15"],
         ["18 Expedite tourism-enabling policy and data sharing", "Validated", "No approved provincial jobs method and no single view of the visitor", "I16"],
         ["19 Lead removal of infrastructure, visa and safety deficits", "Moved", "The best-evidenced barriers, with most of the levers held nationally", "I17"],
         ["20 Develop workforce and service skills", "Flagged", "The jobs ambition has no baseline and no labour analysis", "I18"],
     ], "boldFirstCol": True},
]
write("30_pillar3.json", "3.3", "Pillar 3: Build enabling capability", intro)

fa16 = {
    "kicker": f"{T32} · Focus area 16",
    "name": "Align institutional stakeholders across all three tiers",
    "topline": "Air service agreements and visas sit with national government, mandates are split across three tiers and the national marketing body is weak, so the province needs one shared agenda with clear decision rights.",
    "hypothesis": [
        "**December 2025.** Review Institutional Arrangements (Wesgro, DEDAT, CTT) (Current State Diagnostic, Dec 2025, p64), reprinted from March 2026 as Review Institutional Arrangements (local, provincial and national).",
        "**October 2026: Reworded.** Air rights and visas sit nationally. The review of three named bodies widened to alignment across national, provincial and local government. The stakeholder evidence on bilateral agreements and split mandates, the Diagnostic's tier table and MIDAS's account of route designation drove the change.",
    ],
    "evidence_caption": "The levers the growth case needs are spread across three tiers, and the bodies that hold them are thin or out of step.",
    "evidence_source": "Current State Diagnostic, Dec 2025 (Diag); Stakeholder Insights Report, Mar 2026 (SIR; statements attributed to organisations, not quotations); MIDAS Aviation Market Assessment, Mar 2026; Infrastructure Report, Jul 2026 (IR). No national government body has an appendix table in the first phase of engagement.",
    "evidence_rows": [
        ["National holds air rights and visas", "The national tier holds visa rules and border compliance, and air service agreements and route rights; the province holds jobs, safety programmes and infrastructure planning", "Diag p58"],
        ["Bilateral agreements bind", "Restrictive bilateral air agreements limit airlift and leave the province less competitive than peers (Department of Economic Development)", "SIR p24"],
        ["Chinese routes are state decisions", "Chinese routes follow government-to-government agreements, and the designated airline may learn of its designation late", "MIDAS, Chinese Market"],
        ["Capacity has eroded", "Tourism institutional capacity has eroded at provincial and municipal level over a decade; SA Tourism's weakness constrains otherwise sound international strategies", "SIR p25"],
        ["Mandates are split", "Mobility responsibilities are split across three tiers; a district, local and LTO mandate disconnect leaves tourism development without a clear owner", "SIR p23, p39"],
        ["The capital is national", "ACSA's runway (R6.39bn, about 2033), Transnet's port plans and PRASA's R21.1bn rail programme all sit with national SOEs", "IR p100, p103, p112"],
    ],
    "evidence_after": [
        "What is needed, in the Diagnostic's own words, is a shared growth agenda with clear decision rights and joint delivery plans (Current State Diagnostic, Dec 2025, p58). No deliverable maps decision rights by tier beyond that one slide. The national view in this report is inferred from provincial and local voices, not heard directly (Stakeholder Insights Report, Mar 2026, p16).",
    ],
    "recommendation": [
        "Wesgro should convene the shared agenda and hold the evidence the national tier needs, rather than try to own levers it cannot. A Tourism Growth Steerco at Wesgro CEO level, with DEDAT and Cape Town Tourism, gives the province one voice and one route to national decisions (section 4.7). MIDAS shows the route work this needs: early relationships with Indian carriers and the Indian authorities, and with China's state-owned carriers through the government-to-government process (MIDAS Aviation Market Assessment, Mar 2026, Indian and Chinese Market Opportunity).",
    ],
    "actions": [
        ["Wesgro", "Constitute the Tourism Growth Steerco with DEDAT and Cape Town Tourism, and agree a decision-rights map by tier from the Diagnostic's tier table", "Wesgro CEO's office; DEDAT; Cape Town Tourism"],
        ["Wesgro", "Hold standing relationships with Indian carriers and authorities, with China Southern and China Eastern and with Riyadh Air", "Air Access"],
        ["Wesgro", "Track the national capital programmes that bind the plan (runway, ports and rail) and report on them each quarter", "Air Access; Research"],
        ["Partners", "Settle district, local and LTO mandates, restore a tourism development function where it has lapsed and revisit the Discover Garden Route partnership", "District municipalities; municipalities; LTOs"],
        ["Partners", "Test a dedicated transport authority model for tourism-enabling mobility", "Department of Mobility"],
        ["National", "Agree with the province how marketing and data roles divide between national and provincial bodies", "SA Tourism; Department of Tourism"],
    ],
    "benchmark": "Every comparator places air rights with a national body, among them Chile's civil aviation board and Singapore's aviation authority (Global Benchmarking Report, Mar 2026, p23, p38). Valencia embeds municipal, provincial and regional authorities in one decision-making system led by Visit València, and the required change for the Western Cape is to embed tourism governance in permanent public-private structures (p47, p49).",
    "link": "**Initiative I15**, Tourism Growth Steerco and three-tier alignment, carries this entry with focus area 17 (section 4.3). **Indicator** T2-21 escalation items answered by the national tier at outcome level (section 5.2).",
}
blocks = theme("3.3.2", "Governance and leadership", [
    "The second enabling theme covers who decides and how the plan is run. It holds five focus areas, the most of any theme. They are three-tier alignment, industry collaboration, data and policy, the national deficits moved in from Pillar 2 and workforce skills, which was added in October and flagged as untested.",
]) + entry(fa16, pagebreak=False)
write("34_fa16.json", "3.3.2", "Align institutional stakeholders across all three tiers", blocks)

fa17 = {
    "kicker": f"{T32} · Focus area 17",
    "name": "Strengthen industry and government collaboration",
    "topline": "Fifteen of the sixteen organisations engaged raised collaboration, and the channels already exist in JAMS, the bid teams and the tour-operator forums, so the task is to turn existing forums into one joint plan.",
    "hypothesis": [
        "**December 2025.** Strengthen Industry >> Government Collaboration (Current State Diagnostic, Dec 2025, p64), reprinted from March 2026 as Strengthen Industry > Government Collaboration (Public and Private).",
        "**October 2026: Validated.** Fifteen of sixteen organisations. The stakeholder theme tally drove the disposition. The count is this report's reconstruction from the appendix tables: it counts organisations with at least one collaboration insight, not insight rows, and the deck prints no tally.",
    ],
    "evidence_caption": "Collaboration is wanted almost everywhere and already works in places, but the forums are marketing-led and the trade's voice is missing.",
    "evidence_source": "Stakeholder Insights Report, Mar 2026 (SIR; organisation count reconstructed from the appendix tables); Demand-Side Analysis, Jun 2026 (DSA).",
    "evidence_rows": [
        ["Almost everyone raised it", "15 of the 16 organisations raised at least one collaboration insight, 23 rows in all", "SIR p20 to p46"],
        ["A channel exists", "Tourism associations already coordinate through JAMS with Wesgro, the Western Cape Government and the City of Cape Town (FEDHASA)", "SIR p31"],
        ["Out of step", "Misalignment between public tourism institutions and key industry bodies is weakening collaboration (Department of Economic Development)", "SIR p25"],
        ["Forums are marketing-led", "Provincial and regional forums are dominated by destination marketing rather than development, and support is not tailored to districts (West Coast District Municipality)", "SIR p39"],
        ["Joint selling works", "Stakeholders collaborate well on bids; 36 conference bids secured in 2024/25 are expected to bring 27,000+ delegates and R745 million by 2028", "SIR p46; DSA p36"],
        ["The trade is missing", "No airline, OTA or tour operator took part in the first phase; six demand-side engagements, from Trip.com Group to Emirates, were proposed", "SIR p16"],
    ],
    "evidence_after": [
        "Mossel Bay shows what local collaboration delivers. Its cruise calls rose from four before COVID to 27 a season through closer coordination and better excursion packaging, and it credits its public-private tourism model with faster decisions (Stakeholder Insights Report, Mar 2026, p20, p21). The province's route record is the larger example: 17 mainline international routes added from 2015 to 2025, which MIDAS attributes to Wesgro's relationship-driven route development (MIDAS Aviation Market Assessment, Mar 2026, International Comparisons).",
    ],
    "recommendation": [
        "Wesgro should use the forums that exist rather than build new ones, and give them a development agenda and a joint plan. JAMS lets consultation cascade across the associations more efficiently than approaching each body separately (Stakeholder Insights Report, Mar 2026, p31). The Benchmarking Report's model is Valencia's sector councils, where sector-led committees keep development market-driven (Global Benchmarking Report, Mar 2026, p48, p49).",
    ],
    "actions": [
        ["Wesgro", "Use JAMS as the single consultation channel to the associations, and add the Tour Guides Association", "Wesgro CEO's office; FEDHASA"],
        ["Wesgro", "Set up sector councils for wine, business events, adventure and culture inside Steerco's structure", "Tourism; Convention Bureau; industry bodies"],
        ["Wesgro", "Run the demand-side engagement round with Trip.com Group, Thomas Cook India, DNATA Travel, China International Travel Service, Emirates and SATSA", "Destination Marketing; Air Access"],
        ["Partners", "Supply academic and sector champions for international bids", "CTICC; universities"],
        ["Partners", "Give regional forums a development agenda and tailor provincial support to district needs", "District municipalities; DEDAT; LTOs"],
        ["National", "Include provincial assets in SA Tourism's campaigns for emerging source markets", "SA Tourism"],
    ],
    "benchmark": "Valencia runs sector-led executive committees, with the regional business confederation on its governing board, so that tourism development is market-driven rather than bureaucratically led (Global Benchmarking Report, Mar 2026, p45, p48). Singapore's tourism board, airport group and national airline work under one coordinated strategy with shared KPIs (p40, p42).",
    "link": "**Initiative I15**, Tourism Growth Steerco and three-tier alignment (section 4.3). **Indicator** T2-22 industry partners signed up to the joint plan at outcome level (section 5.2).",
}
write("35_fa17.json", "3.3.2", "Strengthen industry and government collaboration", entry(fa17))

fa18 = {
    "kicker": f"{T32} · Focus area 18",
    "name": "Expedite tourism-enabling policy and data sharing",
    "topline": "No approved method exists for provincial tourism GDP and jobs, operators cannot see their own customers and four arrivals measures run unreconciled, so a data-sharing protocol is the precondition for every target.",
    "hypothesis": [
        "**December 2025.** Expedite Tourism-Enabling Policy and Data Sharing (Current State Diagnostic, Dec 2025, p64).",
        "**October 2026: Validated.** Already underway. The stakeholder evidence drove the disposition: data and policy is the largest theme in the stakeholder record. The platforms are indeed underway, but no deliverable describes a data-sharing protocol or a policy revision in progress at provincial level [data-sharing protocol or policy revision in progress, with owner and start date: Wesgro Research and DEDAT to confirm].",
    ],
    "evidence_caption": "Data is the largest theme in the stakeholder record, and the gaps run from national methodology to operators' own customer records.",
    "evidence_source": "Stakeholder Insights Report, Mar 2026 (SIR; organisation count reconstructed from the appendix tables); Current State Diagnostic, Dec 2025 (Diag).",
    "evidence_rows": [
        ["The largest theme", "15 of 16 organisations and 30 insight rows, the most of any theme, 16 of them rated High", "SIR p20 to p46"],
        ["No provincial method", "No approved methodology for provincial tourism GDP and jobs; official tourism data lag after Covid-era method changes (Department of Tourism)", "SIR p37"],
        ["National capacity is short", "Tourism satellite account timeliness is constrained, with 749 Stats SA vacancies cited", "SIR p30"],
        ["No single view", "No single view of visitor behaviour; stakeholders collect different metrics at different frequencies with different definitions", "Diag p56, p57"],
        ["Operators cannot see customers", "Third-party ticketing channels do not share visitor-level data; Robben Island cannot link marketing spend to visitor acquisition", "SIR p36, p33"],
        ["Platforms exist", "JAMS, the provincial tourism statistics committees and a cross-agency task team exist; the Cape Town Tourism and Google collaboration is still exploratory", "SIR p29, p30, p31, p37"],
    ],
    "evidence_after": [
        "The policy side is as thin. The Department of Economic Development reports a provincial tourism policy gap, with limited legislation and out-of-date master-planning frameworks (Stakeholder Insights Report, Mar 2026, p25). The Demand-Side Analysis uses four arrivals measures without reconciling them: ACSA passenger arrivals, SA Tourism tourist arrivals, OAG air arrivals and the model's international arrivals (Demand-Side Analysis, Jun 2026, p11, p13, p20, p27).",
    ],
    "recommendation": [
        "Wesgro should agree a data-sharing protocol with each data holder and run one indicator register and dashboard, as section 5.5 sets out. The Infrastructure Report puts it plainly: a data layer is the prerequisite, without which no intervention can be targeted or measured (Infrastructure Report, Jul 2026, p5). Skift's tracking design is ready to adopt: quarterly digital tracking, annual or twice-yearly brand research and a dashboard that cross-references campaigns, airline capacity and hotel trends (Skift Digital and Search Insights memo, 10 Dec 2025, section 6).",
    ],
    "actions": [
        ["Wesgro", "Agree data-sharing terms with ACSA, SA Tourism, Stats SA, Cape Town Tourism, the site operators and the booking platforms", "Research"],
        ["Wesgro", "Run one indicator register and dashboard, with quarterly digital tracking and annual brand research", "Research; programme office"],
        ["Wesgro", "Measure meetings, incentives and exhibitions, and add Nigeria and Ghana to the growth model", "Research; Convention Bureau"],
        ["Partners", "Close the provincial tourism policy gap and embed tourism in IDPs and spatial plans, with reporting", "DEDAT; municipalities"],
        ["Partners", "Share visitor-level data from ticketing and reservation systems", "Attraction operators; CapeNature"],
        ["National", "Approve a provincial tourism GDP and jobs methodology and resource the tourism satellite account", "Department of Tourism; Stats SA"],
    ],
    "benchmark": "New Zealand's route-accountable model rests partly on shared data platforms between tourism bodies and airlines, and it recorded more than 16,000 incremental bookings (Global Benchmarking Report, Mar 2026, p54). Valencia is the realism check: integrating data systems across institutions there created technical and organisational challenges (p45).",
    "link": "**Initiative I16**, data-sharing protocol and visitor intelligence (section 4.3). **Indicator** T2-23 automated data feeds in the dashboard at outcome level (section 5.2).",
}
write("36_fa18.json", "3.3.2", "Expedite tourism-enabling policy and data sharing", entry(fa18))

fa19 = {
    "kicker": f"{T32} · Focus area 19",
    "name": "Lead removal of infrastructure, visa and safety deficits",
    "topline": "Visas, air rights, the runway and policing sit with national government, so the province leads by escalation backed with evidence, and delivers the safety programmes and basic services that are its own.",
    "hypothesis": [
        "**December 2025.** Lead Removal of Infrastructure, Visa and Safety Deficits, under theme 2.1 (Current State Diagnostic, Dec 2025, p64).",
        "**October 2026: Moved.** The entry moved from supply to governance because its levers sit nationally. The stakeholder evidence, the Demand-Side barriers and MIDAS all place visas and air rights with national government; the move itself was decided at the October review [Summary of Findings, 14 Oct 2026: the deck's stated reason for the move to confirm]. The rationale holds for visas and air rights, while safety programmes are a provincial function and basic services a local one (Current State Diagnostic, Dec 2025, p58).",
    ],
    "evidence_caption": "The deficits are the best-evidenced barriers in the stakeholder record, and most of the levers sit with national government or SOEs.",
    "evidence_source": "Stakeholder Insights Report, Mar 2026 (SIR; organisation counts reconstructed from the appendix tables); Current State Diagnostic, Dec 2025 (Diag; Skift, Barriers to visiting Cape Town, 2024, as cited); Infrastructure Report, Jul 2026 (IR); Demand-Side Analysis, Jun 2026 (DSA); Skift African Market Analysis, 16 Mar 2026 (working analysis; arrivals to South Africa, not Cape Town).",
    "evidence_rows": [
        ["Raised widely", "10 of 16 organisations raised the theme; across all themes, safety perception came from seven organisations, visas from four and utilities from four", "SIR p20 to p46"],
        ["Visas hold back growth markets", "Visa issues constrain growth from India and recovery from China; regional African event demand is visa-constrained", "SIR p36, p45"],
        ["Safety is cross-cutting", "Perceptions of crime feature in overseas sales conversations; township product and shared mobility are held back by safety perception", "SIR p46, p34, p22"],
        ["Safety and visas top the barriers", "Skift's barrier research ranks crime and personal safety first and visa and entry requirements second; e-visa reforms are promising but unproven for the province", "Diag p55, p34"],
        ["The gateway binds", "The single runway caps movements at about 30 an hour and relief lands from about 2032; immigration processing at peak needs work", "IR p101 to p103; DSA p54"],
        ["Visa reform moves arrivals", "The 2024 Ghana visa waiver drove 36,656 arrivals to South Africa", "Skift African, s4.6"],
    ],
    "evidence_after": [
        "Inside communities, safety is a launch gate. Nine of the 20 shortlisted communities record a safety-perception gap and five record extortion, and the Inclusion Plan makes a formal safety assessment a separate requirement before launch (SME and Community Inclusion Plan, Sep 2026, p30, p35). Congestion costs the Metro an estimated R2.8 billion a year, and water scarcity acts as a hard ceiling on visitor load in high-growth nodes (Current State Diagnostic, Dec 2025, p38).",
    ],
    "recommendation": [
        "Wesgro should run a standing escalation agenda, with each item stated as a decision, the national body that owns it and the date the province asks for, backed by market evidence. The Stakeholder Insights Report's next round already frames that evidence: the access barriers across air, visas and onward travel, and the safety issues most damaging to demand (Stakeholder Insights Report, Mar 2026, p14). The Diagnostic asks for dedicated tourism safety units and programmes in the Metro (Current State Diagnostic, Dec 2025, p41).",
    ],
    "actions": [
        ["Wesgro", "Table an escalation agenda at Steerco: visa categories and processing for China, India, the Middle East and Africa; air service agreements; immigration throughput at Cape Town International", "Wesgro CEO's office; DEDAT"],
        ["Wesgro", "Build the market-by-market evidence for each ask, from visa processing times to safety perception in source markets", "Research; Destination Marketing"],
        ["Wesgro", "Carry a visitor-safety narrative in marketing, and apply the four launch gates to any community product Wesgro sells", "Destination Marketing; Tourism"],
        ["Partners", "Set up dedicated tourism safety units and programmes, with safety compacts in pilot communities", "Western Cape Government; municipalities; SAPS"],
        ["Partners", "Fix basic services, water and connectivity at remote reserves and in tourism towns", "Municipalities; CapeNature"],
        ["National", "Decide on visa processing, air service agreements and immigration counters, and make station security a rail line item", "Home Affairs; Department of Transport; PRASA"],
    ],
    "benchmark": "Kenya reduces entry friction to position Nairobi as a regional and global hub, and every comparator was scored on ease of access and visas (Global Benchmarking Report, Mar 2026, p59, p11). The required change for the Western Cape, drawn from Chile, is to lobby actively for air service liberalisation and simplified visa regimes (p28).",
    "link": "**Initiative I17**, access and safety escalation agenda (section 4.3). **Indicators** T2-24 visa processing time for priority markets and T2-21 escalation items answered at outcome level (section 5.2).",
}
write("37_fa19.json", "3.3.2", "Lead removal of infrastructure, visa and safety deficits", entry(fa19))

fa20 = {
    "kicker": f"{T32} · Focus area 20",
    "name": "Develop workforce and service skills",
    "topline": "The 300,000 tourism-linked jobs ambition has no baseline and no labour analysis behind it, so the first step is to commission that analysis, and the skills plan follows from it.",
    "hypothesis": [
        "**December 2025.** No December entry; skills appear in no printed version of the tree.",
        "**October 2026: Flagged, untested.** The jobs goal has no labour analysis. The entry was added in October because the 300,000-jobs ambition has no labour analysis behind it, and skills constraints surfaced only as side mentions (Inception Report, Nov 2025, p4). As agreed in the report structure, it is written as a recommendation to commission the analysis, not as a finding.",
    ],
    "evidence_caption": "No deliverable carries a provincial tourism employment figure, and the skills evidence is a handful of statements and two training programmes.",
    "evidence_source": "Inception Report, Nov 2025 (Inc); Stakeholder Insights Report, Mar 2026 (SIR); SME and Community Inclusion Plan, Sep 2026 (SCIP); Current State Diagnostic, Dec 2025 (Diag; Western Cape Cruise Liner Industry Economic Contribution 2024/25 Season, as cited).",
    "evidence_rows": [
        ["The ambition has no base", "300,000 tourism-linked jobs, one of four headline ambitions, with no base year, baseline or target year", "Inc p4"],
        ["No provincial method", "No approved methodology for provincial tourism GDP and jobs estimates (Department of Tourism)", "SIR p37"],
        ["Skills gaps near reserves", "Low baseline skills in communities near reserves need substantial upskilling before service standards can be met (CapeNature)", "SIR p43"],
        ["Municipal capacity is stretched", "Local municipalities face skills and staffing constraints, and skills support is not tailored to districts (West Coast District Municipality)", "SIR p39"],
        ["Training exists in places", "20 CATHSSETA site guides certified in Mbekweni in August 2026; a hospitality academy in Prince Albert from early 2026", "SCIP p42, p51"],
        ["One provincial series", "1,234 direct cruise jobs in the Western Cape in 2024/25, the only provincial tourism jobs figure in a deliverable", "Diag p37"],
    ],
    "evidence_after": [
        "Public sources give the scale the analysis must work from: direct tourism employment of 106,707 in Cape Town in 2024 and 953,981 nationally (City of Cape Town, Economic Value of Tourism, 2025; Stats SA Tourism Satellite Account, provisional, 2026; public sources). The provincial figure may already be in the project's files, because the Inception Report lists the Western Cape Pero 2025 and the district Mero 2024 among the documents Wesgro supplied (Inception Report, Nov 2025, p34) [provincial tourism employment from the Pero 2025: Wesgro Research to extract].",
    ],
    "recommendation": [
        "Wesgro and DEDAT should commission a tourism labour analysis in 2027. It should fix a provincial employment baseline, test the 300,000 ambition and identify the occupations and skills the growth case needs. Until it reports, Chapter 5 carries jobs as a ratio-based measure on Wesgro's own rule of two jobs per 100 international passengers (section 5.3). The skills plan then runs through the quality charter, where the Benchmarking Report places work-force capability (Global Benchmarking Report, Mar 2026, p42).",
    ],
    "actions": [
        ["Wesgro", "Commission the labour analysis with DEDAT: baseline, definition, occupations, skills gaps and the training pipeline", "Research; DEDAT"],
        ["Wesgro", "Extract the tourism employment table from the Pero 2025, and obtain the method note for the jobs-per-passenger ratio", "Research; Air Access"],
        ["Wesgro", "Build a workforce strand into the provincial quality charter (focus area 11)", "Tourism"],
        ["Partners", "Run training partnerships around reserves and in pilot communities, building on the CATHSSETA guide certification and the Prince Albert academy", "CapeNature; CATHSSETA; training providers; municipalities"],
        ["Partners", "Help newly trained guides stay in the sector with bookings from existing itineraries", "LTOs; tour operators"],
        ["National", "Approve a provincial tourism jobs methodology and resource the tourism satellite account", "Department of Tourism; Stats SA"],
    ],
    "benchmark": "Singapore's hotel industry transformation map, run by the tourism board with the hotel association and backed by dedicated funds, lifted service quality and spend per visitor (Global Benchmarking Report, Mar 2026, p41). None of the six comparators carries a labour analysis or a tourism employment target, so the sizing step has no precedent in the benchmark set.",
    "link": "**Initiative I18**, tourism labour analysis and skills plan (section 4.3). **Indicators** T1-04 tourism jobs at impact level, carried as a ratio-based projection until the analysis reports, and T2-25 labour analysis published at outcome level (section 5.2).",
}
write("38_fa20.json", "3.3.2", "Develop workforce and service skills", entry(fa20))
print("pillar 3 intro and theme 3.2 written")
