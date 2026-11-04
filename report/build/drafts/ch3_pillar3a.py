"""FIRST-DRAFT GENERATOR ONLY. After the figure check (4 Nov 2026) the JSON files in content/ are the source of record; do not re-run this script.
Chapter 3, Pillar 3, theme 3.1: focus areas 13 to 15. Writes content/ch3/31_fa13.json to 33_fa15.json.
Sources: report/evidence/factsheet_t31.md, tree.md, discrepancies.md (3 November 2026).
Inclusion rules from the brief: concept level only; no Wesgro-funded hub; no trade-mission incentives;
none of the banned inclusion terms."""
from ch3_lib import theme, entry, write

T31 = "Theme 3.1 · Investment, inclusion and sustainability"

fa13 = {
    "kicker": f"{T31} · Focus area 13",
    "name": "Embed local destination bodies for community inclusion",
    "topline": "Twenty communities hold 18.4% of the province's residents but a traced 0.02% to 0.04% of foreign direct spend, and in eleven the binding constraint is organisation, not distance or product.",
    "hypothesis": [
        "**December 2025.** Drive Community and SME Inclusion (Current State Diagnostic, Dec 2025, p64).",
        "**October 2026: Refined.** A seller with a stake, 20 communities and R259m at 1%. The SME and Community Inclusion Plan drove the refinement. As agreed with Wesgro on 24 September 2026, the entry stays at concept level, and roles and funding are set in Chapter 4.",
    ],
    "evidence_caption": "The shortlisted communities sit close to visitors but earn almost nothing from them, and most lack a body that can sell.",
    "evidence_source": "SME and Community Inclusion Plan, Sep 2026 (SCIP; desk research 17 to 23 September 2026, ratings from the community side with LTO confirmation outstanding). The R259m is 1% of the R25.9bn FY2025 foreign direct spend in the Demand-Side Analysis, Jun 2026, p11. The plan does not describe how the spend floor was traced. The multiple of today's floor is computed.",
    "evidence_rows": [
        ["Close to demand", "93 of 107 long-listed communities lie within 45 minutes of a tourism node or corridor; distance is the binding constraint in none of the 20", "SCIP p16, p30"],
        ["Almost no spend", "18.4% of residents (Census 2011) against a traced floor of 0.02% to 0.04% of foreign direct spend, about R4m to R10m a year", "SCIP p5"],
        ["Organisation binds", "Organisation is the binding constraint in 11 of 20 communities, and 10 have no identified active tourism body", "SCIP p28, p30"],
        ["Product sells by phone", "No profiled community rates Ready on digital and bookability; Zwelihle's four resident guides sell by phone with no shared channel", "SCIP p20 to p26, p34"],
        ["Safety is a gate", "9 of 20 communities record a safety-perception gap and 5 record extortion (SAPS 2025/26 station data)", "SCIP p27, p30"],
        ["The prize", "1% of FY2025 foreign direct spend is R259m a year, about 26 to 65 times today's documented floor", "SCIP p5"],
    ],
    "evidence_after": [
        "The plan's five cases set the order of action: a seller with a stake, a safe and workable visit, product that keeps spend in the community, then exposure (SME and Community Inclusion Plan, Sep 2026, p12). Kliptown in Soweto shows the cost of the reverse order. Walter Sisulu Square cost R160 million to R180 million before an operator was in place, and drew about 4,000 museum visitors a year by 2017 against a business case of almost 200,000 international visitors (p11).",
    ],
    "recommendation": [
        "Wesgro should connect community product to the demand it already moves, and leave the building of selling bodies to municipalities, LTOs and the communities themselves. The plan's model has three parts: a selling capability that works, a link to demand that already exists and gates that must be passed before activation and investment (SME and Community Inclusion Plan, Sep 2026, p32). Two or three pilot communities test it, and it scales only after agreed thresholds are met (p32). The plan's sequence runs from validating the offer and opening a booking route, through a safety plan and a fixed-date test, to investment after demand and scale through channels (p31).",
    ],
    "actions": [
        ["Wesgro", "Put pilot community product into the itineraries, calendars and channels Wesgro already runs, such as the Langa and Kayamandi routes and the Mal'va festival listing", "Tourism; Destination Marketing"],
        ["Wesgro", "Choose the two or three pilots with partners on the plan's readiness criteria, and keep the record of bookings, visitors and locally retained revenue", "Research; Tourism"],
        ["Partners", "Form or fund a local selling body in each pilot community, with one live booking route, published dates and a named customer contact", "Municipalities; LTOs; community sellers"],
        ["Partners", "Attach maintenance and marketing covenants to public assets before any re-letting or upgrade", "Municipalities"],
        ["National", "Commit SAPS to the launch safety plans the pilots need, and open ACSA and other national procurement to businesses trading inside the communities", "SAPS; ACSA"],
    ],
    "benchmark": "Kenya writes community participation into its tourism governance and investment system through community conservancies, with benefits across rural communities among the listed outcomes (Global Benchmarking Report, Mar 2026, p33). The plan's own cases carry the figures: Medellín's Comuna 13 drew 1.98 million visitors in 2025 around resident-run product, while Kliptown shows what capital before an operator buys (SME and Community Inclusion Plan, Sep 2026, p8, p11).",
    "link": "**Initiative I12**, community inclusion pilots (section 4.3), with booking routes shared with **I3** (focus area 3). **Indicators** T1-07 community share of foreign direct spend at impact level and T2-17 communities with a live booking route at outcome level (section 5.2).",
}
blocks = theme("3.3.1", "Investment, inclusion and sustainability", [
    "The first enabling theme covers who benefits from growth, how it is paid for and how it lasts. It holds three focus areas: community inclusion, climate risk and investment. The inclusion entry stays at concept level, as agreed with Wesgro on 24 September 2026; roles and funding sit in Chapter 4.",
]) + entry(fa13, pagebreak=False)
write("31_fa13.json", "3.3.1", "Embed local destination bodies for community inclusion", blocks)

fa14 = {
    "kicker": f"{T31} · Focus area 14",
    "name": "Manage climate risk and sustainable tourism",
    "topline": "Climate is already costing the province sites, routes and revenue, while the local tourism bodies that would manage the response depend on municipal funding that Treasury Circular 131 has disrupted.",
    "hypothesis": [
        "**December 2025.** Ensure Sustainable Destination Management (Current State Diagnostic, Dec 2025, p64).",
        "**October 2026: Reworded.** LTOs are unfunded and the Meiringspoort flood cut a route. Destination-management funding and dated climate losses replaced a general sustainability entry. The stakeholder evidence on LTO funding and climate losses drove the change, with the Inclusion Plan's De Rust profile for the flood.",
    ],
    "evidence_caption": "Climate losses are dated and site-specific, and the bodies that manage destinations locally have no stable funding.",
    "evidence_source": "Stakeholder Insights Report, Mar 2026 (SIR; statements attributed to organisations, not quotations); SME and Community Inclusion Plan, Sep 2026 (SCIP); Infrastructure Report, Jul 2026 (IR); Current State Diagnostic, Dec 2025 (Diag). No deliverable quantifies climate risk province-wide.",
    "evidence_rows": [
        ["LTOs depend on municipalities", "Most local tourism bodies are not operationally sustainable without municipal funding, and Treasury Circular 131 has disrupted that route (Department of Economic Development)", "SIR p25"],
        ["LTO budgets go to marketing", "LTO contracts and budgets are weighted toward destination marketing, leaving little for tourism development (West Coast District Municipality)", "SIR p39"],
        ["A flood cut a route", "Meiringspoort closed since the flood of 6 May 2026; rebuild R421m over about 26 months; De Rust's pass-through trade cut", "SCIP p24"],
        ["Weather costs a flagship", "Weather cancellations cost Robben Island roughly R16m a year, on management's estimate", "SIR p33"],
        ["Sites are closing", "Flooding, fire and extreme heat are closing CapeNature sites and restricting trails; high winds close the Cableway for a significant part of the year", "SIR p43, p36"],
        ["Every district has a climate risk", "Water security in the Metro and the Garden Route; wildflower predictability on the West Coast; whale migration and sea levels in the Overberg; summer heat in the Central Karoo", "IR p31, p64, p75, p86; Diag p43"],
    ],
    "evidence_after": [
        "No deliverable puts a provincial figure on tourism revenue at risk from weather or water [provincial estimate of tourism revenue at risk: none in hand], and none counts the LTOs or their grant funding [number of Western Cape LTOs and their municipal funding before and after Circular 131: DEDAT to supply]. The only working sustainability standard on record is Mossel Bay's membership inspections, which check water-wise and green practices (Stakeholder Insights Report, Mar 2026, p20).",
    ],
    "recommendation": [
        "Wesgro should treat climate as a destination-management risk it reports on and plans around, and press for stable funding of the local bodies that do the work. The deliverables diagnose this entry more than they prescribe for it. The Diagnostic asks for a climate-smart wine region, a nature-positive test bed in the Overberg and resilience investment on the Garden Route (Current State Diagnostic, Dec 2025, p43, p45, p49). CapeNature is already reassessing asset formats and siting to cut losses from flood, fire and heat (Stakeholder Insights Report, Mar 2026, p43).",
    ],
    "actions": [
        ["Wesgro", "Keep a climate and weather risk register for tourism sites and routes, starting with the Robben Island, Cableway and CapeNature losses and the Meiringspoort closure", "Research; site operators"],
        ["Wesgro", "Build sustainability checks into the provincial quality charter (focus area 11) on the Mossel Bay model", "Tourism; LTOs"],
        ["Wesgro", "Route itineraries and marketing around closures, starting with alternatives to Meiringspoort until the pass reopens", "Destination Marketing; Garden Route and Klein Karoo LTOs"],
        ["Partners", "Give LTOs a stable funding agreement with a development mandate, written into IDPs with reporting", "Municipalities; district municipalities; DEDAT"],
        ["Partners", "Make reserve and attraction assets climate-resilient, with off-grid power at remote sites", "CapeNature; site operators"],
        ["National", "Resolve the effect of Treasury Circular 131 on municipal funding of local tourism bodies, and complete the Meiringspoort rebuild", "National Treasury; the road authority"],
    ],
    "benchmark": "No benchmark case carries a climate-adaptation or local destination-body funding lever. The nearest are Kenya's tourism-funded conservation financing, a self-financing system that supports conservation and sustains demand, and Valencia's SICTED quality system with its environmental compliance frameworks (Global Benchmarking Report, Mar 2026, p33, p47).",
    "link": "**Initiative I13**, climate resilience and destination management, including LTO funding (section 4.3). **Indicators** T2-18 LTOs with a funding agreement and T2-19 weather losses at flagship sites at outcome level (section 5.2).",
}
write("32_fa14.json", "3.3.1", "Manage climate risk and sustainable tourism", entry(fa14))

fa15 = {
    "kicker": f"{T31} · Focus area 15",
    "name": "Crowd in capital with targeted investment strategies",
    "topline": "The province has a capital pipeline for airports, ports, roads and rail, but none of it reaches tourism product, bookability, accommodation depth or community assets, which is where the growth case needs investment.",
    "hypothesis": [
        "**December 2025.** Crowd-In Capital with Targeted Investment Strategies (Current State Diagnostic, Dec 2025, p64).",
        "**October 2026: Validated.** No pipeline. The Infrastructure Report's pipeline and gap-closure tables drove the disposition, with the stakeholder view that funding sits below peers and the Chilean and New Zealand benchmarks. The reason is an inference: the report lists a large capital pipeline, and its gap columns show that none of it reaches tourism product.",
    ],
    "evidence_caption": "Capital is committed to gateways and transport, and each district's tourism gaps carry no committed capital.",
    "evidence_source": "Infrastructure Report, Jul 2026 (IR; the ~R11.3bn CTIA headline itemises to R9.94bn on p103); Stakeholder Insights Report, Mar 2026 (SIR); SME and Community Inclusion Plan, Sep 2026 (SCIP). No deliverable gives a Western Cape tourism funding-gap figure.",
    "evidence_rows": [
        ["The Metro pipeline", "About R30bn or more planned: ~R11.3bn at Cape Town International, R20bn for the V&A Granger Bay expansion and R3.3bn for MyCiTi Phase 2; SME bookability and township product sit outside every capital programme", "IR p32"],
        ["Airports are funded", "R310m George terminal by 2028; Cape Winelands Airport ~R8bn private phase 1, with funding not yet locked in", "IR p43, p106"],
        ["Tourism gaps are not", "No committed capital for West Coast accommodation and payments, De Hoop accommodation, Whale Coast bookability, Overberg year-round product or Route 62 accommodation", "IR p65, p76, p87"],
        ["Port capital is for freight", "Of the port capital listed, only the R22m Mossel Bay reception facility is for cruise", "IR p112"],
        ["Funding is below peers", "Western Cape tourism funding is materially below peer destinations, and a tourism levy and blended finance are under consideration", "SIR p25, p23"],
        ["Capital first fails", "Kliptown's Walter Sisulu Square cost R160m to R180m before an operator and drew about 4,000 museum visitors a year by 2017", "SCIP p11"],
    ],
    "evidence_after": [
        "The instrument this entry calls for was planned and not delivered. The Inception Report scoped an investment opportunity framework that would score gaps against return, jobs and inclusion, with a roadmap of quick wins, medium-term plays and long-term moves (Inception Report, Nov 2025, p18, p20). The gap-closure tables are its input [Western Cape tourism funding against the peer set: DEDAT and Wesgro budget data needed].",
    ],
    "recommendation": [
        "Wesgro should build the tourism investment pipeline the gap tables imply, and commit capital only where demand has been shown. The Inclusion Plan's rule applies across the portfolio: invest after demand, and attach a maintenance and marketing covenant to any public asset (SME and Community Inclusion Plan, Sep 2026, p31, p15). The benchmarks offer the vehicles: Chile's private concession for its gateway airport and New Zealand's route incentives tied to bookings (Global Benchmarking Report, Mar 2026, p26, p54).",
    ],
    "actions": [
        ["Wesgro", "Build a tourism investment pipeline from the gap-closure tables, scored for return, jobs and inclusion, and take it to investors", "Wesgro investment promotion; Tourism; DEDAT"],
        ["Wesgro", "Prepare investment cases for mid-scale and conference-capable hotels in secondary nodes and for accommodation at De Hoop and on Route 62", "Wesgro investment promotion; private investors"],
        ["Wesgro", "Set up the public-private air access fund with ring-fenced corridor budgets (focus area 7)", "Air Access; DEDAT; City of Cape Town; private sector"],
        ["Partners", "Test a tourism levy and blended-finance vehicles for destination management and mobility", "DEDAT; City of Cape Town"],
        ["Partners", "Attach covenants to public assets before re-letting or upgrading them, and invest in community assets only after demand is proven", "Municipalities"],
        ["National", "Hold ACSA, PRASA and Transnet to their published capital dates, and add tourism use to the port plans", "ACSA; PRASA; Transnet"],
    ],
    "benchmark": "Chile funded a ~US$900 million expansion of its gateway airport through a private concession awarded by its Ministry of Public Works (Global Benchmarking Report, Mar 2026, p26). Melbourne's event-led demand drew 21% growth in hotel rooms, 5,000 new rooms and the entry of global hotel brands (p18).",
    "link": "**Initiative I14**, tourism investment pipeline (section 4.3). **Indicator** T2-20 pipeline projects at financial close at outcome level (section 5.2).",
}
write("33_fa15.json", "3.3.1", "Crowd in capital with targeted investment strategies", entry(fa15))
print("pillar 3 theme 3.1 written")
