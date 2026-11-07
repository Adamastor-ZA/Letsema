"""Draft v7 content edits (Michael, 7 November 2026): fewer tables. Groups 1 to 4 of the table review.

1. Delete ten tables whose content the report already carries: the six Chapter 2 "findings for the tree" recaps
   (every figure in them is in the numbered findings above), the three Chapter 3 pillar overviews (they repeat the
   executive-summary pillar tables and Appendix A2) and the stakeholder priority areas (held in full in A6).
2. Turn 20 short body tables into narrative, and fold Table 1.7 (deliverables) into the documents table in A9.
3. Merge the three results-chain tables into one, and the funding columns of Table 4.5 into the initiatives table.
4. Turn six short appendix tables into narrative.

Narrative keeps every figure, open item and source; sources are written in the house citation form, so the renderer
footnotes them. A check at the end confirms every number in each converted table appears in its replacement text.
Run once on the v6 content. Writes redteam/applied_v7.json.
"""
import json, glob, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
C = os.path.join(HERE, '..', 'content')
FILES = {os.path.relpath(f, C): json.load(open(f)) for f in sorted(glob.glob(os.path.join(C, '*', '*.json')))}
LOG, CHECKS = [], []
P = lambda t: {'type': 'p', 'text': t}


def tindex(f, title):
    idx = [i for i, b in enumerate(FILES[f]['blocks']) if b['type'] == 'table' and b['caption'] == title]
    assert len(idx) == 1, (f, title, idx)
    return idx[0]


def nums(s):
    return set(re.findall(r'\d+(?:[.,]\d+)*', s))


def table_text(b):
    return ' '.join([b.get('message') or '', b.get('source') or ''] + [' '.join(map(str, r)) for r in b['rows']])


def replace_table(group, f, title, blocks, check=True, skip=()):
    """Swap a table for narrative blocks (or nothing), log it and queue the figure check."""
    i = tindex(f, title)
    old = FILES[f]['blocks'][i]
    FILES[f]['blocks'][i:i + 1] = blocks
    new_text = ' '.join(b.get('text', '') + ' '.join(b.get('items', [])) for b in blocks)
    LOG.append({'group': group, 'file': f, 'table': title, 'action': 'narrative' if blocks else 'deleted', 'before': table_text(old), 'after': new_text})
    if check and blocks: CHECKS.append((f, title, nums(table_text(old)) - set(skip), new_text))
    return old


def edit_text(group, f, find, repl, n=1):
    hits = [b for b in FILES[f]['blocks'] if find in b.get('text', '') or find in b.get('source', '')]
    total = sum(b.get('text', '').count(find) + b.get('source', '').count(find) for b in hits)
    assert total == n, (f, find[:60], total)
    for b in hits:
        for k in ('text', 'source'):
            if find in b.get(k, ''): b[k] = b[k].replace(find, repl)
    LOG.append({'group': group, 'file': f, 'table': None, 'action': 'text edit', 'before': find, 'after': repl})


# ======================================================================================================== Group 1
for f, title in [('ch2/01_demand.json', 'Demand findings for the tree'), ('ch2/02_aviation.json', 'Aviation findings for the tree'),
                 ('ch2/03_benchmarking.json', 'Benchmark findings for the tree'), ('ch2/04_stakeholders.json', 'Stakeholder findings for the tree'),
                 ('ch2/05_infrastructure.json', 'Spatial findings for the tree'), ('ch2/06_inclusion.json', 'Inclusion findings for the tree')]:
    replace_table('1 delete (recap of the numbered findings above)', f, title, [])
replace_table('1 delete (held in full in Appendix A6)', 'ch2/04_stakeholders.json', 'Stakeholder priority areas', [])
edit_text('1 consequential', 'ch2/04_stakeholders.json',
          'which frame the questions the later phases were to test (Stakeholder Insights Report, Mar 2026, p14).',
          'which frame the questions the later phases were to test (Stakeholder Insights Report, Mar 2026, p14). Appendix A6 lists them with their lines of enquiry.')
DECK = '[Summary of Findings, 14 Oct 2026, pp15 to 16: deck page reference to be confirmed]'
for f, title, line in [
    ('ch3/10_pillar1.json', 'Pillar 1 focus areas', 'Pillar 1 holds six focus areas: three carried through as Validated and three were reworded toward conversion.'),
    ('ch3/20_pillar2.json', 'Pillar 2 focus areas', 'Pillar 2 holds six focus areas: the air entry was reworded, cruise is new and the four others carried through as Validated.'),
    ('ch3/30_pillar3.json', 'Pillar 3 focus areas', 'Pillar 3 holds eight focus areas, the widest spread of dispositions in the tree.')]:
    replace_table('1 delete (repeats the executive-summary pillar table and Appendix A2)', f, title,
                  [P(f'{line} The entries follow, and the executive summary lists them with their initiatives. Dispositions are as recorded at the 14 October 2026 review {DECK}.')], check=False)

# ======================================================================================================== Group 2
# Executive summary
replace_table('2 narrative', 'exec/01_summary.json', 'How the tree changed', [
    P("Nine changes turned eighteen December entries into twenty focus areas, each driven by a named workstream. The air access and cruise entry split in two: focus area 7, Win direct routes and add seats on full routes, is Reworded, and focus area 8, Grow cruise calls and ports, is New. Focus area 19, Lead removal of infrastructure, visa and safety deficits, keeps its December title but moves from supply to governance. Focus area 20, Develop workforce and service skills, was added and is Flagged, untested."),
    P("Five entries were Reworded to the lever the evidence supports. Develop the Seasonality and Spread Proposition became focus area 2, Create green-season demand with MICE and events. Facilitate Adoption Along the Path to Purchase became focus area 3, Make the whole province findable and bookable. Pivot to Growth Markets (China, India, ME, ASEAN) became focus area 4, Convert India and China hub traffic. Ensure Sustainable Destination Management became focus area 14, Manage climate risk and sustainable tourism. Review Institutional Arrangements (Wesgro, DEDAT, CTT) became focus area 16, Align institutional stakeholders across all three tiers. Drive Community and SME Inclusion became focus area 13, Embed local destination bodies for community inclusion, Refined and held at concept level (Current State Diagnostic, Dec 2025, p64; dispositions as recorded at the 14 October 2026 review; section 1.4)."),
], skip={'64'})
replace_table('2 narrative', 'exec/01_summary.json', 'Actions for the first 24 months', [
    P("Twelve actions can start in the first 24 months, nine of them inside Wesgro's current mandate and budget, and each opens a seat, a baseline or a booking path a later initiative needs. Section 4.5 lists them with their funding routes; owners and start dates are proposals for Steerco to confirm."),
    P("**Seats and season, from 2027 H1.** Air Access holds winter seats with demand through joint green-season marketing with carriers on the full routes (I6, I2). It also tracks the runway programme quarterly and models capacity against demand to 2035 (I6). The Convention Bureau publishes a green-season events calendar and aims bids at May to September (I2)."),
    P("**Governance and baselines, from 2027 H1.** The Wesgro CEO's office and DEDAT constitute Steerco and table the first national escalation agenda (I15, I17). Research agrees the data-sharing protocol with ACSA, SA Tourism, Stats SA and Cape Town Tourism (I16), runs a bookability census of provincial product by district (I3) and requests visitor counts and capacity from the five flagship sites (I11). DEDAT, with Wesgro Research, commissions the tourism labour analysis behind the jobs ambition (I18)."),
    P("**Product and inclusion, from 2027 H2.** Tourism packages the Garden Route and Route 62 with a shuttle transfer sold inside the itinerary (I8, I9), and the Southern Line as a visitor product with the City and PRASA (I8). It chooses two or three pilot communities and agrees who funds a seller with a stake in each (I12). From 2028 H1, the LTOs, with Tourism, give each pilot community one live booking route before any promotion (I12, I3)."),
], skip={'4.5'})
replace_table('2 narrative', 'exec/01_summary.json', 'The main risks', [
    P("The risks that matter most sit outside Wesgro's control, so the response is early warning and a route to the tier that can act. Restrictive bilateral air agreements and the US carrier cap are the one risk rated high on both likelihood and impact; the response is an escalation agenda with stated asks and route work inside existing rights."),
    P("Three risks are rated medium likelihood and high impact. If runway relief at Cape Town International slips past about 2033, the response is quarterly milestone tracking, more frequency and larger aircraft, with George for domestic connections. If visa processing for growth markets does not improve, the escalation agenda carries it and processing time is tracked each year. Safety incidents or perception that deter visitors meet safety gates before pilot launches and escalation to SAPS. Climate events that close sites and routes are rated high likelihood and medium impact; a climate risk register and itineraries routed around closures are the response. Likelihood and impact are Letsema's assessment, and section 4.8 holds the full register."),
], skip={'4.8'})

# Chapter 1
edit_text('2 consequential', 'ch1/01_mandate.json', 'The table below sets each original ambition against the baseline in hand and the form in which the strategy now carries it.',
          'The study reframed the arrivals ambition on evidence and carried the other three ambitions forward with their baselines still to be fixed.')
replace_table('2 narrative', 'ch1/01_mandate.json', 'The four headline ambitions', [
    P("**Arrivals.** The ambition was 2.8 million international visitors by 2035 (Inception Report, Nov 2025, p4). The baseline in hand is 1.44m international passenger arrivals at Cape Town International in FY24/25 (Current State Diagnostic, Dec 2025, p25) and the model base of 1,498,829 in 2025 (Market Assessment Report, May 2026, p19). The strategy carries it as growth to 2.5 million: 2,516,282 on the accelerated case and 2,175,778 on the base case by 2035 (p19). The Diagnostic's 5.7 million arrivals and R54.7 billion spend is recorded as superseded (Current State Diagnostic, Dec 2025, p5)."),
    P("**Jobs.** The ambition was 300,000 tourism-linked jobs, and no deliverable carries a Western Cape tourism employment figure. The strategy carries it to Chapter 5 with its baseline set by the labour analysis it commissions under workforce and service skills (focus area 20, flagged)."),
    P("**SMMEs.** The ambition was 10,000 SMMEs onboarded, with no baseline or definition printed [Wesgro to confirm the baseline count and definition of SMMEs onboarded]. It is carried as community inclusion, measured in visitor spend reaching priority communities rather than a count of firms (section 2.6 and Chapter 5)."),
    P("**Airlift and cruise.** The ambition was twice the airlift and cruise volumes. For airlift, the growth model draws inbound capacity at 1.8 million seats (Market Assessment Report, May 2026, p20); for cruise, the baseline is 79 vessels in the 2024/25 season (Current State Diagnostic, Dec 2025, p37). Airlift is carried as the seats and routes needed to lift the 1.8 million seat line, and cruise as calls and ports (section 3.2.1) [Cruise Cape Town to confirm the call target and its definition]."),
], skip={'2.6', '3.2.1'})
edit_text('2 consequential', 'ch1/02_system_today.json', ' The table below sets out who holds what.', '')
replace_table('2 narrative', 'ch1/02_system_today.json', 'The tourism system by tier', [
    P("Wesgro's six units sit inside a system of fifteen external organisations whose decision rights are split across three spheres of government and industry (Inception Report, Nov 2025, p7, organisations as shown on the stakeholder map and grouped by this report; Current State Diagnostic, Dec 2025, p58). The six units are Cape Town Air Access, Cruise Cape Town, the Convention Bureau, Destination Marketing, Research and Tourism. Between them they cover route development, cruise, business events bids, destination marketing, research and tourism promotion for Cape Town and the Western Cape."),
    P("The Western Cape Government (Economic Development and Tourism) and the City of Cape Town make up provincial and city government. The provincial tier sets jobs, inclusion and spatial outcomes, runs sector development and safety programmes and plans infrastructure and resilience. The local tier delivers services and manages precincts. It also readies events and place experience and handles congestion, by-laws and community impact."),
    P("South African Tourism, Airports Company South Africa, Transnet and the South African Maritime Safety Authority sit at the national tier. It holds visa rules and border compliance. It also holds air service agreements and route rights, sets national brand and investment priorities and runs airport capacity and port operations."),
    P("Cape Town Tourism, the V&A Waterfront, CapeNature, South African National Parks and the Table Mountain Aerial Cableway are the destination and attraction bodies. They carry demand generation and destination marketing as well as product quality and visitor experience at the flagship sites. The private operators, MSC Cruises, Cape Grace, Pullman Hotels and Resorts (Cape Town City Centre) and Southern Sun, carry route and product viability and commercial performance. They also set pricing and service standards. Together they form the industry tier."),
])
# 1.7 folds into the A9 document register.
old17 = replace_table('2 fold into A9', 'ch1/04_approach.json', 'Interim deliverables and SLA clauses', [], check=False)
edit_text('2 consequential', 'ch1/04_approach.json', 'Nine dated documents carry the evidence, and the table below dates each by its cover.',
          'Nine dated documents carry the evidence. Appendix A9 dates each by its cover and gives the version in hand and the SLA clauses it answers. Chapter 2 summarises them: the Market Assessment Report and the Demand-Side Analysis in 2.1, the MIDAS Aviation Market Assessment in 2.2, the Global Benchmarking Report in 2.3, the Stakeholder Insights Report in 2.4, the Infrastructure Report in 2.5 and the SME and Community Inclusion Plan in 2.6. The Inception Report frames 1.1 and 1.4, and the Current State Diagnostic frames 1.2 and is folded into 2.1 and 2.5.')
a33 = FILES['appendices/09_a9_glossary.json']['blocks'][tindex('appendices/09_a9_glossary.json', 'Documents and sources cited')]
a33['columns'] = [{'header': 'Document', 'width': 2.6, 'align': 'left'}, {'header': 'Author', 'width': 1.5, 'align': 'left'}, {'header': 'Date cited', 'width': 1.6, 'align': 'left'},
                  {'header': 'Status', 'width': 1.0, 'align': 'left'}, {'header': 'Version in hand and SLA clauses', 'width': 2.6, 'align': 'left'}]
match = {'Inception Report': 'Inception Report', 'Current State Diagnostic': 'Current State Diagnostic', 'Stakeholder Insights Report': 'Stakeholder Insights Report',
         'Global Benchmarking Report': 'Global Benchmarking Report', 'MIDAS Aviation Market Assessment': 'MIDAS Aviation Market Assessment',
         'Market Assessment Report': 'Market Assessment Report', 'Demand-Side Analysis': 'Demand-Side Analysis', 'Infrastructure Report': 'Infrastructure Report',
         'SME and Community Inclusion Plan': 'SME and Community Inclusion Plan'}
notes = {}
for r in old17['rows']:
    key = [k for k in match if r[0].startswith(k)][0]
    notes[key] = f'{r[2]}. SLA clauses: {r[3]}'
used = set()
for row in a33['rows']:
    key = next((k for k in match if row[0].startswith(k) and not (k == 'Market Assessment Report' and row[0].startswith('MIDAS'))), None)
    row.append(notes[key] if key and key not in used else '')
    if key: used.add(key)
assert used == set(notes), set(notes) - used
old_src = a33['source']
a33['source'] += ' Versions in hand from the cover pages and file dates of each document; SLA Annexure B clause numbers [to be checked against the signed Annexure B].'
LOG.append({'group': '2 fold into A9', 'file': 'appendices/09_a9_glossary.json', 'table': 'Documents and sources cited', 'action': 'column added from Table 1.7', 'before': '', 'after': json.dumps(notes, ensure_ascii=False)})
CHECKS.append(('appendices/09_a9_glossary.json', 'Interim deliverables and SLA clauses (folded)', nums(table_text(old17)) - {'1.1', '1.2', '1.4', '2.1', '2.2', '2.3', '2.4', '2.5', '2.6'},
               table_text(a33) + ' ' + LOG[-2]['after']))
LOG.append({'group': '2 fold into A9', 'file': 'appendices/09_a9_glossary.json', 'table': 'Documents and sources cited', 'action': 'source extended', 'before': old_src, 'after': a33['source']})

edit_text('2 consequential', 'ch1/05_how_to_read.json', 'The report moves from context to evidence to recommendations to delivery, and the table below gives the route through it for each reader.',
          'The report moves from context to evidence to recommendations to delivery.')
replace_table('2 narrative', 'ch1/05_how_to_read.json', 'Chapter map and readers', [
    P("The executive summary gives the case in short: the growth case to 2035, the constraints that cap it, the twenty focus areas by pillar, the first 24 months and the headline indicators. It stands alone, for the Board, Exco and the February 2027 launch audience. Chapter 1 is for every reader, and is the chapter of the body a Board member should read if they read no other. It sets out what Wesgro asked for, where the system stands after recovery, why the next step is constrained by peak capacity and how the study ran."),
    P("Chapter 2 summarises what each interim deliverable asked, did and found, with the evidence that survived into the hypothesis tree. It serves readers checking the evidence behind a Chapter 3 entry, and each section closes with a box naming the focus areas it supports. Chapter 3 takes the twenty focus areas in turn: the December hypothesis, its disposition, the evidence, what Wesgro does, what it asks of partners and what it escalates nationally. The Board and Exco can read it entry by entry and the programme owner in full; section 3.4 gives the sequence."),
    P("Chapter 4 sets out which initiatives run, in what order, owned by whom, at what cost and with which decision gates, for the programme owner, Steerco and the partners named in the RACI. Chapter 5 sets out how progress is measured, through indicators, baselines, targets, data sources, the scorecard and the 2030 mid-term review, for Wesgro Research, the programme office and Steerco. Appendices A1 to A9 hold the traceability table, the demand model, the benchmark cases, readiness scores, the community fact base, stakeholder inputs, charters, the toolkit and references, for analysts and anyone checking a figure."),
], skip={'3.4', '2026'})
replace_table('2 narrative', 'ch1/05_how_to_read.json', 'Disposition labels and counts', [
    P("Seven labels record what the evidence did to each December hypothesis, and ten of the twenty focus areas carry Validated: the evidence confirmed the hypothesis as written. One is Refined, where the evidence confirmed the hypothesis and sharpened its content. Six are Reworded: the evidence confirmed the hypothesis and the entry was renamed to what the evidence showed. One is New, added in October 2026 with no December entry behind it. One is Moved: confirmed, but placed in another theme because its levers sit with another tier. One is Flagged: untested, and carried as a question for analysis still to be commissioned. None is Withdrawn, the label for an entry dropped because the evidence did not support it. The labels are as recorded at the 14 October 2026 review [Summary of Findings, 14 Oct 2026, pp15 to 16: deck page reference to be confirmed against the final deck], and the counts come from the traceability table in Appendix A1."),
], skip={'10', '1', '6', '0'})

# Chapter 2
replace_table('2 narrative', 'ch2/02_aviation.json', 'Carrier launches since 2014', [
    P("By 2026 scheduled seats, the five largest are Airlink to various regional points (441,602), Ethiopian Airlines to Addis Ababa (437,430), Turkish Airlines to Istanbul (240,200), United Airlines to Newark and Washington (172,190) and Kenya Airways to Nairobi (127,138). The other seven are Delta Air Lines to Atlanta (110,612), Norse Atlantic UK to London Gatwick (103,428), LATAM Airlines Group to São Paulo (47,084), Air Tanzania to Dar es Salaam and Victoria Falls (37,716), Safair to Windhoek (32,130), Proflight Zambia to Livingstone (14,600) and Eswatini Air to Manzini (3,700) (\"The Capetown Market\")."),
], skip={'2014', '2026', '12'})
replace_table('2 narrative', 'ch2/03_benchmarking.json', 'Comparator lessons for the province', [
    P("Each comparator's lesson translates into a change the Western Cape would have to make (Global Benchmarking Report, Mar 2026, p20, p28, p35, p42, p49, p56). Chile's gateway-led air connectivity means treating air access as core economic infrastructure, with a permanent public-private air access fund and lobbying for air service liberalisation and simpler visas (p28). New Zealand's demand-engineered air access means ring-fencing marketing budgets around priority long-haul corridors, with an aviation partnership framework and early-stage route support (p56). Melbourne and Victoria's event-led demand means one event acquisition and calendar strategy across Wesgro, the Convention Bureau, the City and the Province, with conference bidding aligned to sector strengths (p20)."),
    P("Singapore's hub conversion and quality uplift means government, aviation, events and industry working to shared KPIs, under a province-wide quality and standards framework led by Wesgro (p42). Valencia's governed quality and sector councils mean a provincial quality charter phased by district, certification visible on booking platforms and standing sector councils for wine, MICE, adventure and culture (p49). Kenya's gateway diversification and conservation-led product mean treating MICE as a system lever, aligning city, provincial and national actors around a gateway strategy and building conservation and community inclusion into the offer (p35)."),
])
replace_table('2 narrative', 'ch2/04_stakeholders.json', 'Attributed high-rated insights', [
    P("Eight attributed insights, all rated High, carry the weight of the stakeholder evidence (Stakeholder Insights Report, Mar 2026, appendix tables; the insights are the project team's statements, attributed to the organisation engaged). The Department of Economic Development reports that restrictive bilateral air agreements are limiting airlift growth and leave the province less competitive than peer destinations (p24). It rates Western Cape and Cape Town tourism funding materially below peer destinations for destination management and destination marketing, and finds that MFMA Circular No. 131 has disrupted established municipal funding mechanisms for local tourism bodies (p25). The Department of Tourism notes that there is no approved official methodology for provincial tourism GDP and jobs estimates (p37)."),
    P("CapeNature takes approximately 70% of its reservations through the call centre rather than the online platform (p42). Robben Island Museum puts the cost of weather and climate disruption at roughly R16 million a year in cancelled trips (p33). The West Coast District describes a mandate disconnect between the district, local municipalities and LTOs that has left tourism development without clear ownership (p39). The Table Mountain Cableway reports peak-period queues of up to three hours up and two hours down, which detract from the visitor experience (p36). [Open item: each organisation named here to approve its paraphrase before publication.]"),
])
replace_table('2 narrative', 'ch2/05_infrastructure.json', 'Cruise ports and stance', [
    P("Cape Town's cruise berth has spare capacity, Mossel Bay is ready for day stops and Saldanha Bay is a watching brief (Infrastructure Report, Jul 2026, p110 to p112). Cape Town, where the stance is to protect, handled 83 calls and about 127,000 passengers in 2024/25, about 40% of a season capacity of 150 or more calls, for R1.79bn of impact; its limits are a 300m ship length, the South-Easter wind and no shore power. Mossel Bay, to back now, handled 21 calls and about 13,000 passengers and opened a R22m passenger facility in November 2025; it has no cruise quay, so ships anchor and tender, and only small and mid-sized ships call. Saldanha Bay, to watch, has had 3 trial calls; it shares the ore terminal and has no cruise berth or passenger facility."),
])
replace_table('2 narrative', 'ch2/05_infrastructure.json', 'Remaining gaps by region', [
    P("Each region carries a remaining gap that no committed investment closes (Infrastructure Report, Jul 2026, ratings p28, p41, p52, p63, p74, p85; gaps and investments p32, p43, p54, p65, p76, p87). The Cape Metro, rated 4.5, has the R11.3bn airport overhaul, the R20bn V&A Granger Bay expansion and the R3.3bn MyCiTi Phase 2. Last-mile transit to Chapman's Peak, Constantia and Cape Point, small-operator online booking and township product remain open. The Cape Winelands, rated 3.4, has the R8bn first phase of Cape Winelands Airport by 2028 and a wider precinct of R16bn to R20bn, but no transit inside the wine triangle, little non-wine product and no pricing for domestic visitors. The Garden Route, rated 3.4, has the R310m George terminal by 2028 and a R9.4m landing-system upgrade, but no international carrier, a winter trough and no transport between towns."),
    P("The Overberg, rated 2.7, has the R81.7m Agulhas lighthouse precinct and the R17m Malgas road, but lacks accommodation towards De Hoop, bookability east of Hermanus and year-round product. The West Coast, rated 2.5, has the completed R693m Malmesbury bypass and the R4bn Saldanha port upgrade, which serves iron ore; it lacks accommodation depth and digital payments, and has no airport. The Central Karoo and Route 62, rated 1.9, have the R62 reconstruction under way and rural broadband to 2026, but lack accommodation depth and emergency support, and have no airport."),
])
replace_table('2 narrative', 'ch2/06_inclusion.json', 'Inclusion benchmark cases', [
    P("Five benchmark cases show that sellers outlast programmes and that capital without an operator earns nothing (SME and Community Inclusion Plan, Sep 2026, p7 to p11). In Santa Marta in Rio de Janeiro, about 20 resident guides ran the tours by 2015 and outside jeep firms had left: access and safety are preconditions, not product, and resident sellers outlast programmes (p7). Medellín's Comuna 13 drew 1.98 million visitors in 2025, 52% of them international, with about 300 professional guides; mobility built for residents became the stage, but carrying-capacity limits came late (p8). On Vilakazi Street in Soweto, ten restaurants employ more than 800 people; public-realm works amplify existing assets, but benefits concentrate on street-front owners (p9)."),
    P("Costa Rica's community network turned over more than USD 800,000 in 2013 and dissolved at the end of 2018: a selling entity is the engine and must survive donor exit (p10). Kliptown in Soweto received R436 million and drew about 4,000 museum visitors a year by 2017, because capital built before an operator yields no operating income (p11)."),
])
replace_table('2 narrative', 'ch2/06_inclusion.json', 'Community archetypes and responses', [
    P("Most long-listed communities sit near a node with something already worth visiting, and each archetype carries its own response (SME and Community Inclusion Plan, Sep 2026, p15, p17; p4 prints 48 and 8 for the two assets-underused rows). Near a node with assets underused, 49 long-listed and 11 shortlisted communities need integration through itinerary slots, procurement and events, with sellers organised. Near a node with no assets, 43 long-listed and 6 shortlisted communities need one anchor asset under a covenant, then integration, with a seller first. Remote communities with underused assets, 7 long-listed and 2 shortlisted, need access opened and the asset placed on a route product the LTO already sells. Remote communities with no assets, 8 long-listed and 1 shortlisted, need procurement and skills first, and an asset only once a route product exists."),
])

# Chapter 3
edit_text('2 consequential', 'ch3/40_integrated.json', 'Each step up the case therefore rests on a set of moves, and the table below maps each set to the focus areas that deliver it.',
          'Each step of the growth case therefore rests on a named set of interventions, and each set draws on focus areas in all three pillars.')
replace_table('2 narrative', 'ch3/40_integrated.json', 'Growth paths and their interventions', [
    P("The conservative path, 1,822,634 arrivals in 2035, holds existing air access with no added frequencies or routes and continues trade and marketing, with growth in the mature markets and current corridors; focus areas 5 and 7 hold that base. The base path adds 353,144 arrivals to reach 2,175,778. It assumes Emirates, Qatar, Ethiopian and Turkish Airlines add frequency and capacity and existing Wesgro programmes expand, while India, China and regional Africa grow through hub connections; focus areas 1 to 7, 9 and 10 deliver it. The accelerated path adds a further 340,504 to reach 2,516,282. It needs direct India and China routes secured and dedicated activation in India, China, the USA and the GCC, with India, China and the Middle East growing ahead of their source markets; focus areas 4, 7, 16 and 19 deliver it on top of the base (Demand-Side Analysis, Jun 2026, p19, p20; Market Assessment Report, May 2026, p19, the 2025 base; increments computed from the printed end points; the mapping to focus areas is this report's)."),
])
edit_text('2 consequential', 'ch3/40_integrated.json', ' The table below sets the order. Chapter 4 turns it into eighteen initiatives with owners, phases and decision gates.',
          ' The first phase works the seats and the booking path before the base case crosses the model\'s seat line, and the direct routes wait for runway relief. Chapter 4 turns the sequence into eighteen initiatives with owners, phases and decision gates.')
replace_table('2 narrative', 'ch3/40_integrated.json', 'What moves in each phase', [
    P("**Activate, 2027 to 2028,** comes before the base case crosses the model's seat line around 2030. Seats are held and added on the full routes (focus areas 5, 6 and 7), the green-season calendar is set (2) and the bookability census and onboarding run (3). Two or three inclusion pilots start (13), Steerco, the data protocol and the escalation agenda are set up (16, 18 and 19) and the labour analysis is commissioned (20)."),
    P("**Expand, 2029 to 2031,** brings hub conversion at scale (4), corridor product and mobility (9 and 10), the quality charter (11) and flagship flow management (12), along with cruise product (8) and the investment pipeline at financial close (15). The 2030 mid-term review tests the seat line, and terminal relief arrives from about 2032."),
    P("**Sustain, 2032 to 2035,** takes direct India and China routes to carriers as runway capacity arrives (4 and 7), scales inclusion once its thresholds are met (13) and embeds climate risk and LTO funding (14). Runway relief arrives about 2033, and the accelerated case depends on the direct routes (Demand-Side Analysis, Jun 2026, p21; Infrastructure Report, Jul 2026, p103; phase years as set in section 4.2)."),
], skip={'1', '20', '4.2'})

# Chapter 4
replace_table('2 narrative', 'ch4/01_portfolio.json', 'Levels of the plan', [
    P("Seven levels run from the vision to the measures, and each has a fixed count in this plan. One vision says where the province is going: grow international arrivals from 1.5m in 2025 toward 2.5m by 2035. Three pillars say what must change, such as Reshape demand. Six themes say in which part of the system, such as source market growth and diversification. Twenty focus areas say where the evidence says to act, such as Convert India and China hub traffic. Eighteen initiatives say what Wesgro and its partners do, such as I4 India and China hub conversion. The 112 actions say who does what, by tier, such as activation inside Xiaohongshu, Douyin and MakeMyTrip. The indicators, 7 at impact, 25 at outcome and 36 at output level, say how Steerco knows, such as T2-06 India and China hub arrivals. The counts come from Chapter 3, the action tables and the traceability table in Appendix A1."),
], skip={'1', '3', '6', '20', '18'})

# Chapter 5
replace_table('2 narrative', 'ch5/05_tracking.json', 'Reporting calendar and cycles', [
    P("Reporting runs on a fixed calendar tied to Steerco and the Board. Each month, the leads send Tier 3 outputs, initiative status and the seats and arrivals feeds to the programme office as a dashboard update. Each quarter, the programme office takes Tier 2 outcomes where available, the risks rated high and the escalation responses to Steerco in the scorecard. Each year, Steerco takes Tier 1 impact against both paths, the plan refresh and gate status to the Board in an outlook report, made public at the business outlook event. At each gate, Steerco sends the Board a gate paper on the tests in section 4.7."),
], skip={'3', '2', '1', '4.7'})
replace_table('2 narrative', 'ch5/06_evaluation.json', 'Evaluation questions by pillar', [
    P("Each pillar carries two evaluation questions, one on results and one on the assumptions behind them. For Reshape demand: did arrivals, spend per visitor and the green-season share move with the activation, and in which markets and segments? Is conversion still the constraint, or has access overtaken it in the growth markets? For Transform supply: did seats, readiness and bookability rise outside the Metro, and did visitors follow? Did the airport relief arrive on time, and did the second gateways carry the load meanwhile? For Build enabling capability: did the pilots meet their thresholds, and did community spend rise? Did the national asks get answers, and did the data protocol deliver the baselines?"),
], skip={'1', '2', '3'})
replace_table('2 narrative', 'ch5/07_toolkit.json', 'The M&E toolkit files', [
    P("The four files are the indicator register, the baseline workbook, the scorecard template and the dashboard data model (SLA clauses 1.1.10.2 and 1.1.15.3) [clause wording to be checked against the signed Annexure B]. The indicator register holds all 68 indicators with their definition, unit, source, frequency, owner, baseline and target by year and path. The baseline workbook holds the baseline values with page references to the deliverables, and the computed values with their method. Wesgro Research owns both. The programme office owns the scorecard template, which carries the quarterly Steerco scorecard and the annual Board outlook. It also owns the dashboard data model: the feeds, refresh frequency and manual-entry forms for the dashboard in section 5.5."),
], skip={'5.5'})

# ======================================================================================================== Group 3
f = 'ch5/01_results_chain.json'
bl = FILES[f]['blocks']
ids = [tindex(f, f'Pillar {k} results chain') for k in (1, 2, 3)]
t1, t2, t3 = (bl[i] for i in ids)
merged = dict(t1)
merged['caption'] = 'Results chain by initiative'
merged['message'] = ('Pillar 1 initiatives (I1 to I5) move arrivals, market mix, spend and the green-season share. Pillar 2 initiatives (I6 to I11) move seats, '
                     'cruise volumes and the share of visitors and spend outside the Metro. Pillar 3 initiatives (I12 to I18) move community spend and jobs, '
                     'and supply the governance and data every other indicator relies on.')
merged['rows'] = t1['rows'] + t2['rows'] + t3['rows']
before = ' || '.join(table_text(t) for t in (t1, t2, t3))
for i in sorted(ids, reverse=True): bl.pop(i)
bl.insert(ids[0], merged)
LOG.append({'group': '3 merge', 'file': f, 'table': 'Pillar 1 to 3 results chain', 'action': 'merged into one table', 'before': before, 'after': table_text(merged),
            'captions': ['Pillar 1 results chain', 'Pillar 2 results chain', 'Pillar 3 results chain', 'Results chain by initiative']})
CHECKS.append((f, 'Results chain (merged)', nums(before) - {'1', '2', '3'}, table_text(merged)))
edit_text('3 consequential', f, 'The three tables below give the chain for each pillar.', 'The table below gives the chain for each initiative, pillar by pillar.')

fi, ff = 'ch4/01_portfolio.json', 'ch4/06_funding.json'
ini = FILES[fi]['blocks'][tindex(fi, 'The eighteen initiatives')]
fund = replace_table('3 merge into the initiatives table', ff, 'Funding routes by initiative', [], check=False)
src_names = ['Wesgro operating', 'Provincial and municipal', 'National and SOE', 'Private capital']
byc = {r[0]: r for r in fund['rows']}
ini['columns'] = [{'header': 'Code', 'width': 0.6, 'align': 'left'}, {'header': 'Initiative', 'width': 2.6, 'align': 'left'}, {'header': 'Focus areas', 'width': 0.8, 'align': 'left'},
                  {'header': 'Proposed lead', 'width': 1.9, 'align': 'left'}, {'header': 'Phase 1 role', 'width': 1.3, 'align': 'left'},
                  {'header': 'Main funding', 'width': 1.7, 'align': 'left'}, {'header': 'Supporting funding', 'width': 1.7, 'align': 'left'}]
for r in ini['rows']:
    fr = byc[r[0]]
    r.append('; '.join(n for n, v in zip(src_names, fr[2:]) if v == '●') or 'None')
    r.append('; '.join(n for n, v in zip(src_names, fr[2:]) if v == '○') or 'None')
old_ms = (ini['message'], ini['source'])
ini['message'] = ini['message'] + ' Thirteen draw mainly on Wesgro\'s operating budget, and four need private capital as a main source.'
ini['source'] += ' Funding routes from the initiative charters (section 4.3); rand values are not estimated.'
main_counts = {n: sum(1 for r in ini['rows'] if n in r[5].split('; ')) for n in src_names}
assert main_counts['Wesgro operating'] == 13 and main_counts['Private capital'] == 4, main_counts
LOG.append({'group': '3 merge', 'file': fi, 'table': 'The eighteen initiatives', 'action': 'funding columns added from Table 4.5', 'before': table_text(fund), 'after': json.dumps(main_counts)})
LOG.append({'group': '3 merge', 'file': fi, 'table': 'The eighteen initiatives', 'action': 'message and source extended', 'before': ' || '.join(old_ms), 'after': ' || '.join((ini['message'], ini['source']))})
edit_text('3 consequential', ff, 'This section therefore sets the funding route for each initiative and leaves the rand bands to be set with Wesgro Finance and DEDAT',
          'Thirteen initiatives draw mainly on Wesgro\'s operating budget, and four need private capital as a main source; the initiatives table in section 4.1 gives each one\'s main and supporting funding routes. This section leaves the rand bands to be set with Wesgro Finance and DEDAT')

# ======================================================================================================== Group 4
replace_table('4 narrative', 'appendices/02_a2_demand_model.json', 'Model printouts and limits', [
    P("The model prints its seat line and six base-case year points but no seat table, annual series or group split for the other scenarios. The seat line is 1.8 million inbound seats, drawn as a line labelled 1.8M and called current, with no year or seat definition (Market Assessment Report, May 2026, p20; Demand-Side Analysis, Jun 2026, p21). Neither deck states the year the line is crossed: 2028 (1,673,855) sits below the line and 2030 (1,802,929) is the first point above it (Market Assessment Report, May 2026, p20; Demand-Side Analysis, Jun 2026, p21)."),
    P("No seat table is printed: there are no seats by route or year, no load factors and no frequencies (Market Assessment Report, May 2026, p17, p20; Demand-Side Analysis, Jun 2026, p18). Nor is an annual series: 2026, 2027, 2029, 2031 and 2033 are absent, and the June chart starts at 2024, not 2025 (Market Assessment Report, May 2026, p20; Demand-Side Analysis, Jun 2026, p21). The conservative and accelerated scenarios appear at 2035 only, with no group split, no year points and no per-market rates (Market Assessment Report, May 2026, p19; Demand-Side Analysis, Jun 2026, p20)."),
    P("The calendar or financial basis and the source series of the 1,498,829 base are not stated, and the 2025 bars are not marked as actuals or model values (Market Assessment Report, May 2026, p19, p20; Demand-Side Analysis, Jun 2026, p22 to p25). ACSA passenger arrivals (1.57m in FY25/26), SAT tourist arrivals, OAG air arrivals and model arrivals are not reconciled (Demand-Side Analysis, Jun 2026, p8, p11, p13, p20, p27)."),
])
replace_table('4 narrative', 'appendices/03_a3_benchmark.json', 'Comparator system types', [
    P("All six cases align coordination, marketing and access, but each builds its system around a different anchor (Global Benchmarking Report, Mar 2026, p61 for the system types; p59 to p60 for the three components, condensed)."),
    P("**Melbourne and Victoria: events-led.** Coordination institutionalises events and a knowledge-led brand as a cross-government economic development tool. Marketing integrates city branding, intellectual capital and events into a single demand proposition. The event calendar is used to de-risk and stimulate aviation demand."),
    P("**Chile: connectivity-led.** Coordination is anchored around a single strategic constraint, long-haul access. Marketing runs unified national branding with defined regional identities and multi-region itinerary packaging. Liberal aviation policy and major hub investment position Santiago as a single efficient long-haul hub."),
    P("**Kenya: product-led.** Coordination aligns tourism with national priorities in conservation, trade and diplomacy. Marketing is segment-specific and grounded in a designed product system. Access reduces entry friction, with Nairobi as a multipurpose regional and global hub."),
    P("**Singapore: orchestrated experience.** A centrally orchestrated system under STB works through structured public-private partnerships. Marketing packages experiences (events, precincts, lifestyle) into seamless high-value propositions. Aviation, infrastructure and visitor experience are integrated into a single seamless gateway."),
    P("**Valencia: governance-led.** Governance is decentralised and sector-led. Marketing expands the reasons to visit: gastronomy, culture, sport, wellness and business events. Connectivity supports a multi-product destination system and dispersal."),
    P("**New Zealand: value-led.** Tourism, aviation and policy are integrated around shared demand objectives. Marketing shifts from volume to value by selling scarce, high-quality experiences. Long-haul demand converts only when marketing, aviation and distribution are aligned."),
])
replace_table('4 narrative', 'appendices/04_a4_readiness.json', 'Readiness index weights', [
    P("Attractiveness carries 40% of the stated weight and readiness and accessibility carry 30% each (Infrastructure Report, Jul 2026, p17). Attractiveness and quality asks how compelling the tourism offer is, through visitor ratings, uniqueness, price positioning and experience depth. Readiness and capacity asks whether the region can service and convert demand, through capacity and digital discovery. Accessibility asks whether visitors can reach and move through the destination, through airport proximity, gateway travel time and public transport availability. The scale runs from 1 'Very weak' and 2 'Weak' through 3 'Functional' and 4 'Strong' to 5 'Leading', and the stated method is: \"Average indicator scores within each dimension, then combine dimensions using the agreed weights\" (p17)."),
])
replace_table('4 narrative', 'appendices/05_a5_inclusion.json', 'Community share of spend', [
    P("The 20 communities hold 18.4% of Western Cape residents but a documented floor of R4m to R10m a year in visitor spend, while 1% of FY2025 foreign direct spend would land R259m (SME and Community Inclusion Plan, Sep 2026, p5; values as printed, with no tracing method or denominator printed). They also hold 15.4% of employed residents; both shares come from Census 2011. Foreign direct spend traced to businesses trading inside the communities is a floor of 0.02% to 0.04%, which the plan documents as R4m to R10m landing in the 20 communities a year."),
    P("At 1%, FY2025 foreign direct spend would land R259m in the communities, which implies R25.9 billion of FY2025 foreign direct spend (computed). At 1% of the 2035 spend ambition the figure is R547m, which implies R54.7 billion of spend in 2035 (computed). The plan cites the Demand-Side Analysis (16 Sep 2026) and Diagnostic Report v2 for that scenario (SME and Community Inclusion Plan, Sep 2026, p5). The Diagnostic sets the ambition as 5.7 million international arrivals and R54.7 billion of tourism spend by 2035 (Current State Diagnostic, Dec 2025, p5), a different case from the 2.5 million this report carries; Appendix A2 sets out the demand model's own 2035 cases."),
], skip={'2'})
replace_table('4 narrative', 'appendices/05_a5_inclusion.json', 'Inclusion cases and lessons', [
    P("The plan finds that local selling mechanisms lasted while assets and training without a durable route to market did not, but Costa Rica's selling network did not survive donor exit (SME and Community Inclusion Plan, Sep 2026, p7 to p12, p30; the Rio, Medellín, Vilakazi Street and Kliptown cards print no source line, and the plan pools their sources on p12)."),
    P("**Rio de Janeiro, Santa Marta and Rocinha.** The Rio Top Tour's first phase cost about R$230,000 (R$184,000 federal, R$46,000 state). The Cantagalo elevator cost about R$89 million and the Providência cable car R$75 million in a R$163 million package, and almost 10,000 officers were deployed at peak (p7). The tours drew about 4,500 visitors in their first month in 2010, and about 20 resident guides were working by 2015. In 2014, 81% of foreign visitors spent up to R$10 in Rocinha. The cable car stood idle for eight years and security collapsed in 2017, yet Rocinha drew 544,000 visitors in 2023. Access and safety were preconditions, not product, and resident guides continued after the programme that launched them (p30)."),
    P("**Medellín, Comuna 13.** Metrocable Line J (2008) cost about 96.9 billion pesos and the escalators (2011) about 10 billion pesos, with maintenance above 260 million pesos a year; the integrated urban programme passed 100 billion pesos by 2020 (p8). Comuna 13 drew 1.66 million visitors in 2022 and 1.98 million in 2025, 52% of them international, with more than 1,000 businesses and about 300 guides. A 2023 study put its capacity at 667 visitors a day. The lesson is to fund a mandate, a capacity ceiling and a community body alongside the escalator; residents developed the product first (p30)."),
    P("**Soweto, Vilakazi Street.** The Hector Pieterson Museum cost R23.2 million, the Mandela House restoration about R9 million from corporate donors and Orlando Stadium about R280 million; the public-realm cost is not disclosed (p9). The street drew about 1,000 tourists a day by January 2010. Sakhumzi grew from four employees in 2001 to about 110 in 2019, and the ten restaurants provide more than 800 jobs, though the Mandela House company was liquidated. Upgrades amplified existing assets but benefits concentrated on street-front owners, so design governance and a resident precinct entity belong at the outset."),
    P("**Costa Rica, ACTUAR.** UNDP GEF small grants funded the network from the 1990s. Law 8724 (2009) gave ICT duties without a budget, and no state funding for the selling network has been identified (p10). ACTUAR, founded in 2001, turned over more than USD 800,000 in 2013 for more than 30 member communities and dissolved at the end of 2018; its benefits \"stopped at association members\". A management entity with its own selling channel was the engine, and it did not survive donor exit."),
    P("**Soweto, Kliptown.** Kliptown received R436 million in its first allocation. The JDA spent about R497 million from 2001 to 2010 plus R40 million to 2013, Walter Sisulu Square cost R160 million to R180 million and a 48-room hotel R24 million (p11). The business case projected almost 200,000 international visitors a year, but the museum drew about 4,000 a year by 2017 and the hotel traded above break-even only during the 2010 FIFA World Cup. Local small businesses took 5% of construction contract value, and the site was looted in 2021. Heritage converts to local income only when operator, trader and guide product, security and services are funded before the ribbon is cut."),
])
replace_table('4 narrative', 'appendices/06_a6_stakeholders.json', 'Later-phase engagement list', [
    P("The later-phase list names the demand-side voices that phase 1 lacks, but marks all six demand-side engagements as proposed (Stakeholder Insights Report, Mar 2026, p16; entries, spellings and markets in brackets as printed). The 13 supply-side stakeholders, seven of them with a phase 1 table, are: Tourism offices of each District; Table Mountain Aerial Cableway; Robben Island Museum; Hospitality Providers; Conference Venue Operators; CapeNature; SANParks; CBRTA; Ikhwa ttu; CCID; CTICC; FEDHASA; V&A Waterfront."),
    P("The 6 proposed demand-side engagements, none with a phase 1 table, are: Trip.com Group (China, ASEAN); Thomas Cook India (India, Middle East outbound); DNATA Travel (Middle East, India, ASEAN); China International Travel Service (China); Emirates (China, India, Middle East, ASEAN); SATSA. The 11 enabling-environment stakeholders engaged or in progress, five of them with a phase 1 table, are: Department of Economic Development and Tourism; Ministry of Mobility; South African Tourism; SouthAfrica.net; We Do Tourism; SATOvito; Statistics South Africa; Google (Government Affairs and Public Policy); Cape Town International Airport; Winelands Airport; George Airport. The appendix tables print SATVITO, C-BRTA, !Khwa ttu and Cape Nature."),
], skip={'1', '0', '7', '5'})

# ======================================================================================================== Cross-references
order = [('exec', 'ES'), ('ch1', '1'), ('ch2', '2'), ('ch3', '3'), ('ch4', '4'), ('ch5', '5'), ('appendices', 'A')]
num_of = {}
for d, lab in order:
    n = 0
    for f in sorted(k for k in FILES if k.startswith(d + '/')):
        for b in FILES[f]['blocks']:
            if b['type'] == 'table':
                n += 1; num_of[b['caption']] = f'{lab}.{n}'
xref = [('ch2/06_inclusion.json', '(Table A.21)', f"(Table {num_of['Community shortlist criteria']})"),
        ('ch4/08_risks.json', '(Table 4.5)', f"(Table {num_of['The eighteen initiatives']})"),
        ('ch5/02_indicators.json', 'on the dates in Table 5.9.', f"on the dates in Table {num_of['Data gaps and owners']}."),
        ('ch1/04_approach.json', 'restate Tables 1.4, 2.11 and A.20', f"restate Tables {num_of['District economy, assets and access']}, {num_of['District strengths and weaknesses']} and {num_of['Asset counts by district']}"),
        ('ch4/06_funding.json', 'count of initiatives by main funding source from the table above.', f"count of initiatives by main funding source from Table {num_of['The eighteen initiatives']}.")]
for f, a, b2 in xref:
    hit = [blk for blk in FILES[f]['blocks'] if a in json.dumps(blk, ensure_ascii=False)]
    assert len(hit) == 1, (f, a, len(hit))
    s = json.dumps(hit[0], ensure_ascii=False).replace(a, b2)
    hit[0].clear(); hit[0].update(json.loads(s))
    LOG.append({'group': 'cross-reference', 'file': f, 'table': None, 'action': 'renumbered reference', 'before': a, 'after': b2})

# ======================================================================================================== Sentence splits
# Long sentences in the new narrative and its neighbours, split at a semicolon or a "but" clause.
SPLITS = [
    ("with growth in the mature markets and current corridors; focus areas 5 and 7 hold that base.", "with growth in the mature markets and current corridors. Focus areas 5 and 7 hold that base."),
    ("grow through hub connections; focus areas 1 to 7, 9 and 10 deliver it.", "grow through hub connections. Focus areas 1 to 7, 9 and 10 deliver it."),
    ("growing ahead of their source markets; focus areas 4, 7, 16 and 19 deliver it on top of the base", "growing ahead of their source markets. Focus areas 4, 7, 16 and 19 deliver it on top of the base"),
    ("for R1.79bn of impact; its limits are a 300m ship length", "for R1.79bn of impact. Its limits are a 300m ship length"),
    ("opened a R22m passenger facility in November 2025; it has no cruise quay", "opened a R22m passenger facility in November 2025. It has no cruise quay"),
    ("and a wider precinct of R16bn to R20bn, but no transit inside the wine triangle, little non-wine product and no pricing for domestic visitors.", "and a wider precinct of R16bn to R20bn. It still has no transit inside the wine triangle, little non-wine product and no pricing for domestic visitors."),
    ("and a R9.4m landing-system upgrade, but no international carrier, a winter trough and no transport between towns.", "and a R9.4m landing-system upgrade. It still has no international carrier, a winter trough and no transport between towns."),
    ("to 5 'Leading', and the stated method is:", "to 5 'Leading'. The stated method is:"),
    ("(I16), runs a bookability census of provincial product by district (I3) and requests visitor counts", "(I16). It also runs a bookability census of provincial product by district (I3) and requests visitor counts"),
    ("for destination management and destination marketing, and finds that MFMA Circular No. 131", "for destination management and destination marketing. It also finds that MFMA Circular No. 131"),
    ("a different case from the 2.5 million this report carries; Appendix A2 sets out", "a different case from the 2.5 million this report carries. Appendix A2 sets out"),
    ("inside Wesgro's current mandate and budget, and each opens a seat, a baseline or a booking path", "inside Wesgro's current mandate and budget. Each opens a seat, a baseline or a booking path"),
    ("rated high on both likelihood and impact; the response is an escalation agenda", "rated high on both likelihood and impact. The response is an escalation agenda"),
    ("the R4bn Saldanha port upgrade, which serves iron ore; it lacks accommodation depth", "the R4bn Saldanha port upgrade, which serves iron ore. It lacks accommodation depth"),
]
for a, b2 in SPLITS:
    hits = [(f, blk) for f, d in FILES.items() for blk in d['blocks'] if a in blk.get('text', '')]
    assert len(hits) == 1, (a[:60], len(hits))
    f, blk = hits[0]; blk['text'] = blk['text'].replace(a, b2)
    LOG.append({'group': 'sentence split', 'file': f, 'table': None, 'action': 'text edit', 'before': a, 'after': b2})

# Column widths (inches) for the two tables that gained columns, so no header breaks mid-word.
WIDTHS = {('ch4/01_portfolio.json', 'The eighteen initiatives'): {'Code': 0.8, 'Initiative': 2.4, 'Focus areas': 0.8, 'Proposed lead': 1.9, 'Phase 1 role': 1.3, 'Main funding': 1.7, 'Supporting funding': 1.7},
          ('appendices/09_a9_glossary.json', 'Documents and sources cited'): {'Document': 2.4, 'Author': 1.5, 'Date cited': 1.5, 'Status': 1.35, 'Version in hand and SLA clauses': 2.5}}
for (f, title), w in WIDTHS.items():
    t = FILES[f]['blocks'][tindex(f, title)]
    for c in t['columns']: c['width'] = w[c['header']]

# ======================================================================================================== Checks and write
fails = []
for f, title, need, text in CHECKS:
    missing = sorted(n for n in need if n not in nums(text) and n.replace(',', '') not in text.replace(',', ''))
    if missing: fails.append((f, title, missing))
for x in fails: print('FIGURE CHECK:', x)
assert not fails, 'figures missing from narrative'
for f, d in FILES.items():
    with open(os.path.join(C, f), 'w') as fh:
        json.dump(d, fh, indent=1, ensure_ascii=False); fh.write('\n')
json.dump({'log': LOG, 'numbers_after': num_of}, open(os.path.join(HERE, 'applied_v7.json'), 'w'), indent=1, ensure_ascii=False)
print(len(LOG), 'edits; tables now', len(num_of), '; figure check passed on', len(CHECKS), 'conversions')
