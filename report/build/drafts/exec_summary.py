"""FIRST-DRAFT GENERATOR ONLY. After the figure check (4 Nov 2026) the JSON files in content/ are the source of record; do not re-run this script.
Executive summary, written last. Toplines are lifted verbatim from the Chapter 3 lead under each focus-area h3,
so the summary cannot drift from the body. Writes content/exec/01_summary.json and removes the WIP status box."""
import csv, json, os, glob

HERE = os.path.dirname(__file__)
CH3 = os.path.join(HERE, '..', 'content', 'ch3')
OUT = os.path.join(HERE, '..', 'content', 'exec')
TR = {r['fa_id']: r for r in csv.DictReader(open(os.path.join(HERE, '..', '..', 'traceability.csv')))}

# ---- toplines, verbatim from Chapter 3
TOP = {}
for f in sorted(glob.glob(os.path.join(CH3, '*.json'))):
    bl = json.load(open(f))['blocks']
    for i, b in enumerate(bl):
        if b['type'] == 'kicker' and 'Focus area' in b['text']:
            n = int(b['text'].rsplit('Focus area', 1)[1].strip())
            assert bl[i + 1]['type'] == 'h3' and bl[i + 2]['type'] == 'lead'
            TOP[f"FA{n:02d}"] = (bl[i + 1]['text'], bl[i + 2]['text'])
assert len(TOP) == 20, len(TOP)

DISP = {r: TR[r]['disposition'].split()[0].strip(',') for r in TR}


def fa_table(ids, caption):
    rows = [[f"{int(fa[2:])} {TOP[fa][0]}", DISP[fa], TOP[fa][1], TR[fa]['initiative_ids']] for fa in ids]
    return {"type": "table", "caption": caption,
            "source": "Chapter 3 toplines, quoted verbatim; dispositions as recorded at the 14 October 2026 review. Sources for each figure are in the Chapter 3 entry.",
            "columns": [{"header": "Focus area", "width": 1.9, "align": "left"}, {"header": "Disposition", "width": 1.1, "align": "left"},
                        {"header": "What the evidence shows and what follows", "width": 4.2, "align": "left"}, {"header": "Initiative", "width": 0.9, "align": "left"}],
            "rows": rows, "boldFirstCol": True}


def short(name):
    return name


tree = {"type": "tree", "goal": "Accelerating tourism growth: toward 2.5 million international arrivals by 2035",
        "pillars": [
            {"name": "1 Reshape demand", "objective": "More segments, markets, months and places",
             "themes": [{"name": "1.1 Traveller, brand and proposition", "areas": [{"code": f"{int(x[2:])}", "name": TOP[x][0], "disposition": DISP[x]} for x in ["FA01", "FA02", "FA03"]]},
                        {"name": "1.2 Source market growth", "areas": [{"code": f"{int(x[2:])}", "name": TOP[x][0], "disposition": DISP[x]} for x in ["FA04", "FA05", "FA06"]]}]},
            {"name": "2 Transform supply", "objective": "Seats, reach, product and experience",
             "themes": [{"name": "2.1 Access and infrastructure", "areas": [{"code": f"{int(x[2:])}", "name": TOP[x][0], "disposition": DISP[x]} for x in ["FA07", "FA08", "FA09"]]},
                        {"name": "2.2 Product and capacity", "areas": [{"code": f"{int(x[2:])}", "name": TOP[x][0], "disposition": DISP[x]} for x in ["FA10", "FA11", "FA12"]]}]},
            {"name": "3 Build enabling capability", "objective": "Inclusion, capital, governance and data",
             "themes": [{"name": "3.1 Inclusion and sustainability", "areas": [{"code": f"{int(x[2:])}", "name": TOP[x][0], "disposition": DISP[x]} for x in ["FA13", "FA14", "FA15"]]},
                        {"name": "3.2 Governance and leadership", "areas": [{"code": f"{int(x[2:])}", "name": TOP[x][0], "disposition": DISP[x]} for x in ["FA16", "FA17", "FA18", "FA19", "FA20"]]}]},
        ]}

blocks = [
    {"type": "h2", "text": "The case in brief"},
    {"type": "lead", "text": "The Western Cape can grow international arrivals from about 1.5 million in 2025 to between 2.2 million and 2.5 million by 2035. Supply, not demand, sets the pace."},
    {"type": "p", "text": "Wesgro commissioned an evidence-based strategy to double international tourist arrivals to the Western Cape by 2035 (Inception Report, Nov 2025, p4). The study tested an eighteen-entry hypothesis tree against seven deliverables and four working analyses between December 2025 and October 2026. This report sets out what the evidence found, what Wesgro and its partners should do and how progress will be measured."},
    {"type": "p", "text": "The evidence reframes the ambition as growth to 2.5 million arrivals, set by supply rather than demand. From 1,498,829 arrivals in 2025 the growth model reaches 2,175,778 on the base path and 2,516,282 on the accelerated path in 2035 (Market Assessment Report, May 2026, p19; Demand-Side Analysis, Jun 2026, p20). International passenger arrivals at Cape Town International, the series ACSA reports, stood at 1.44m in FY24/25 and 1.57m in FY25/26 (Demand-Side Analysis, Jun 2026, p11)."},
    {"type": "h3", "text": "Five constraints cap the case"},
    {"type": "bullets", "items": [
        "**The gateway.** Current air access caps inbound seats at 1.8 million, and the base case passes that ceiling at its 2030 point; runway relief at Cape Town International lands about 2033 (Demand-Side Analysis, Jun 2026, p21; Infrastructure Report, Jul 2026, p103).",
        "**Full routes.** Eleven of 27 tabled international routes run above 80% load, and carriers on full routes raise fares before they add seats (MIDAS Aviation Market Assessment, Mar 2026, Seasonality; In Conclusion).",
        "**Seasons.** June holds 6.4% of the year's international seats, and about 65% of overseas visitor travel falls between October and March, a provisional figure (MIDAS Aviation Market Assessment, Mar 2026, Seasonality; Demand-Side Analysis, Jun 2026, p12).",
        "**Reach.** Accessibility falls from 4.7 out of 5 in the Cape Metro to 1.0 in the Central Karoo, and one touring route of six is rated Ready (Infrastructure Report, Jul 2026, p88 to p90, p30).",
        "**Levers held elsewhere.** Visas, air service agreements and the airport and port programmes sit with national government and SOEs, and no approved method exists for provincial tourism GDP and jobs (Current State Diagnostic, Dec 2025, p58; Stakeholder Insights Report, Mar 2026, p37).",
    ]},
    {"type": "note", "text": "[Summary of Findings, 14 Oct 2026, slides 3 and 4: align these five constraints with the deck's own list once the deck is in hand.]"},
    {"type": "pagebreak"},
    {"type": "h2", "text": "Strategy on a page"},
    {"type": "p", "text": "The updated hypothesis tree holds three pillars, six themes and twenty focus areas. Ten focus areas carried through as Validated and six were reworded to the lever the evidence supports. Of the other four, one was refined, one is new, one moved between pillars and one is flagged for analysis still to be commissioned."},
    {"type": "figure", "id": "fig_0_tree", "caption": "The updated hypothesis tree: three pillars, six themes and twenty focus areas, each with its disposition from the October 2026 review.",
     "source": "Current State Diagnostic, Dec 2025, p64 (December tree); dispositions as recorded at the 14 October 2026 review [Summary of Findings, 14 Oct 2026, pp15 to 16: deck page reference to be confirmed]; traceability table, Appendix A1.",
     "chart": tree},
    {"type": "h3", "text": "How the tree changed since December"},
    {"type": "p", "text": "Eight December entries changed scope, place or form, and one focus area was added. The changes point the same way: from general ambitions to the specific lever the evidence supports, and from provincial supply to national escalation where the lever sits nationally."},
    {"type": "table", "caption": "Nine changes turned eighteen December entries into twenty focus areas, each driven by a named workstream.",
     "source": "Current State Diagnostic, Dec 2025, p64 (December entries); dispositions as recorded at the 14 October 2026 review; section 1.4.",
     "columns": [{"header": "December 2025 entry", "width": 2.5, "align": "left"}, {"header": "October 2026 focus area", "width": 2.7, "align": "left"}, {"header": "Change", "width": 1.6, "align": "left"}],
     "rows": [
         ["Close the Air Access and Cruise Capacity Gaps", "7 Win direct routes and add seats on full routes; 8 Grow cruise calls and ports", "Split: air Reworded, cruise New"],
         ["Lead Removal of Infrastructure, Visa and Safety Deficits", "19, same title, under Governance and leadership", "Moved from supply to governance"],
         ["None", "20 Develop workforce and service skills", "Added; Flagged, untested"],
         ["Develop the Seasonality and Spread Proposition", "2 Create green-season demand with MICE and events", "Reworded"],
         ["Facilitate Adoption Along the Path to Purchase", "3 Make the whole province findable and bookable", "Reworded"],
         ["Pivot to Growth Markets (China, India, ME, ASEAN)", "4 Convert India and China hub traffic", "Reworded"],
         ["Ensure Sustainable Destination Management", "14 Manage climate risk and sustainable tourism", "Reworded"],
         ["Review Institutional Arrangements (Wesgro, DEDAT, CTT)", "16 Align institutional stakeholders across all three tiers", "Reworded"],
         ["Drive Community and SME Inclusion", "13 Embed local destination bodies for community inclusion", "Refined, held at concept level"],
     ], "boldFirstCol": True},
    {"type": "pagebreak"},
    {"type": "h2", "text": "Twenty focus areas"},
    {"type": "p", "text": "Each focus area below carries the one-sentence finding that opens its Chapter 3 entry, unchanged. The entry itself gives the December hypothesis, the evidence with page references, the recommendation split between Wesgro, its partners and the national tier, a benchmark precedent and the initiative and indicators it leads to."},
    fa_table(["FA01", "FA02", "FA03", "FA04", "FA05", "FA06"], "Pillar 1, Reshape demand: conversion, not awareness, holds back the growth markets, the green season and the province beyond its core."),
    fa_table(["FA07", "FA08", "FA09", "FA10", "FA11", "FA12"], "Pillar 2, Transform supply: the gateway binds first, and beyond the Metro the product exists but is hard to reach, book or stay in."),
    fa_table(["FA13", "FA14", "FA15", "FA16", "FA17", "FA18", "FA19", "FA20"], "Pillar 3, Build enabling capability: inclusion, capital, governance and data are thin, and several levers sit with national government."),
    {"type": "pagebreak"},
    {"type": "h2", "text": "The growth case and its sequence"},
    {"type": "p", "text": "The three paths differ by intervention, not by demand potential (Demand-Side Analysis, Jun 2026, p19). The base path needs hub carriers to keep adding capacity and Wesgro's programmes to expand. The accelerated path also needs direct India and China routes and dedicated activation in India, China, the USA and the Gulf; without confirmed routes, volume reverts to base (p20). Marketing cannot make up for missing seats, because carriers on full routes raise fares instead (MIDAS Aviation Market Assessment, Mar 2026, In Conclusion)."},
    {"type": "figure", "id": "fig_0_paths", "caption": "Only the accelerated path clears 2.5 million arrivals in 2035, and the base path passes the 1.8m seat ceiling before 2031.",
     "source": "Market Assessment Report, May 2026, p19 (2025 base); Demand-Side Analysis, Jun 2026, p20, p21. The 2031 base value and the accelerated and conservative milestones are computed (section 5.3).",
     "chart": {"type": "line", "categories": ["2025", "2028", "2031", "2035"],
               "series": [{"name": "Accelerated", "values": [1498829, 1750871, 2045297, 2516282], "color": "#1F7A8C"},
                          {"name": "Base", "values": [1498829, 1673855, 1871637, 2175778], "color": "#0B3C5D"},
                          {"name": "Conservative", "values": [1498829, 1589411, 1685468, 1822634], "color": "#7A9E7E"}],
               "unit": "", "yMin": 1400000, "refLines": [{"value": 1800000, "label": "1.8m inbound seat ceiling"}],
               "footnote": "Milestone years only; the intervals are three, three and four years."}},
    {"type": "p", "text": "Air access and bookability move first, because every other lever runs through them. Phase 1, Activate (2027 to 2028), holds and adds seats on the full routes, builds the green-season calendar and counts and closes the bookability gap. It also starts two or three inclusion pilots and sets up Steerco, the data protocol and the national escalation agenda. Phase 2, Expand (2029 to 2031), scales what works and meets the seat ceiling at the 2030 mid-term review. Phase 3, Sustain (2032 to 2035), takes the direct route cases to carriers as runway capacity arrives."},
    {"type": "p", "text": "Eighteen initiatives carry the plan, one per focus area except where one owner delivers two. Wesgro is accountable for twelve; DEDAT, the Department of Mobility, municipalities and site operators lead the other six. Thirteen draw mainly on Wesgro's operating budget. None has yet been costed, and setting the rand bands is the first funding task (section 4.6)."},
    {"type": "h3", "text": "The first 24 months"},
    {"type": "table", "caption": "Twelve actions can start inside Wesgro's current mandate and budgets, and each opens a seat, a baseline or a booking path a later initiative needs.",
     "source": "Section 4.5. Owners and start dates are proposals for Steerco to confirm.",
     "columns": [{"header": "Action", "width": 4.4, "align": "left"}, {"header": "Initiative", "width": 0.9, "align": "left"}, {"header": "Proposed owner", "width": 1.7, "align": "left"}, {"header": "Start", "width": 0.8, "align": "left"}],
     "rows": [
         ["Hold winter seats with demand: joint green-season marketing with carriers on the full routes", "I6, I2", "Air Access", "2027 H1"],
         ["Publish a green-season events calendar and aim bids at May to September", "I2", "Convention Bureau", "2027 H1"],
         ["Track the runway programme quarterly and model capacity against demand to 2035", "I6", "Air Access", "2027 H1"],
         ["Constitute Steerco and table the first national escalation agenda", "I15, I17", "Wesgro CEO's office", "2027 H1"],
         ["Agree the data-sharing protocol with ACSA, SA Tourism, Stats SA and Cape Town Tourism", "I16", "Research", "2027 H1"],
         ["Run a bookability census of provincial product by district", "I3", "Research", "2027 H1"],
         ["Request visitor counts and capacity from the five flagship sites", "I11", "Research", "2027 H1"],
         ["Commission the tourism labour analysis behind the jobs ambition", "I18", "DEDAT, with Wesgro Research", "2027 H1"],
         ["Package the Garden Route and Route 62 with a shuttle transfer sold inside the itinerary", "I8, I9", "Tourism", "2027 H2"],
         ["Package the Southern Line as a visitor product with the City and PRASA", "I8", "Tourism", "2027 H2"],
         ["Choose two or three pilot communities and agree who funds a seller with a stake in each", "I12", "Tourism", "2027 H2"],
         ["Give each pilot community one live booking route before any promotion", "I12, I3", "LTOs, with Tourism", "2028 H1"],
     ], "boldFirstCol": False},
    {"type": "pagebreak"},
    {"type": "h2", "text": "How progress will be measured"},
    {"type": "p", "text": "Seven impact indicators, twenty-five outcome indicators and thirty-six output indicators measure the plan. Steerco receives a quarterly scorecard, and the Board an annual outlook against both paths. Gates at the end of 2028 and 2031, a mid-term review in 2030 and a terminal evaluation in 2035 decide what each phase funds."},
    {"type": "table", "caption": "Arrivals and jobs carry targets on both paths, while season, spread and community spend start from dated baselines.",
     "source": "Section 5.3. Computed values are marked *. Jobs use Wesgro's ratio of two jobs per 100 international passengers (public source), a ratio-based projection until the labour analysis reports.",
     "columns": [{"header": "Impact indicator", "width": 1.8, "align": "left"}, {"header": "Baseline", "width": 2.0, "align": "left"}, {"header": "2028 base / accelerated", "width": 1.4, "align": "left"}, {"header": "2035 base / accelerated", "width": 1.6, "align": "left"}],
     "rows": [
         ["T1-01 International arrivals", "1,498,829 (2025)", "1,673,855 / 1,750,871*", "2,175,778 / 2,516,282"],
         ["T1-02 Arrivals by market group", "Five groups, 2025", "Base path by group", "Base path by group; accelerated not split"],
         ["T1-03 Direct foreign spend", "R25.9bn (FY2025)", "Not printed", "R40.6bn (base, modelled)"],
         ["T1-04 Tourism jobs (ratio)", "About 30,000 (2025)", "33,500 / 35,000*", "43,500 / 50,300*"],
         ["T1-05 Green-season share", "About 35% (2025, provisional); 39% (2024)", "Level set at Gate 1", "Rising"],
         ["T1-06 Share outside the Metro", "Not in hand; due in 2027", "Baseline set", "Rising"],
         ["T1-07 Community share of spend", "0.02% to 0.04% (floor)", "Pilots measured", "1% (R259m) reference point"],
     ], "boldFirstCol": True},
    {"type": "h3", "text": "The main risks"},
    {"type": "table", "caption": "The risks that matter most sit outside Wesgro's control, so the response is early warning and a route to the tier that can act.",
     "source": "Section 4.8; likelihood and impact are Letsema's assessment.",
     "columns": [{"header": "Risk", "width": 3.0, "align": "left"}, {"header": "Likelihood and impact", "width": 1.5, "align": "left"}, {"header": "Response", "width": 3.3, "align": "left"}],
     "rows": [
         ["Bilateral air agreements and the US carrier cap stay restrictive", "High; high", "Escalation agenda with stated asks; route work inside existing rights"],
         ["Runway relief at Cape Town International slips past about 2033", "Medium; high", "Quarterly milestone tracking; frequency and gauge; George as second gateway"],
         ["Visa processing for growth markets does not improve", "Medium; high", "Escalation agenda; processing time tracked each year"],
         ["Safety incidents or perception deter visitors", "Medium; high", "Safety gates before pilot launches; escalation to SAPS"],
         ["Climate events close sites and routes", "High; medium", "Climate risk register; itineraries routed around closures"],
     ], "boldFirstCol": True},
    {"type": "h2", "text": "What Steerco and the Board are asked to decide"},
    {"type": "numbered", "items": [
        "Adopt growth to 2.5 million arrivals by 2035 as the plan's goal, with the base and accelerated paths as its targets.",
        "Constitute the Tourism Growth Steerco at Wesgro CEO level with DEDAT and Cape Town Tourism, and confirm the eighteen initiative leads.",
        "Approve the twelve first-year actions inside current budgets, and ask Wesgro Finance and DEDAT to set rand bands for every initiative.",
        "Commission the bookability census and the tourism labour analysis in 2027, so the plan's missing baselines exist by Gate 1.",
        "Table the first national escalation agenda on visas, air service agreements and immigration processing at Cape Town International.",
    ]},
    {"type": "p", "text": "Several items remain open, from the October deck's page references to the source of the 250-call cruise plan and a provincial employment baseline. Each is marked in square brackets where it occurs and listed with an owner in the open-items register that accompanies this report."},
]
os.makedirs(OUT, exist_ok=True)
wip = os.path.join(OUT, '00_wip_status.json')
if os.path.exists(wip):
    os.remove(wip)
with open(os.path.join(OUT, '01_summary.json'), 'w') as f:
    json.dump({"id": "0", "title": "Executive summary", "blocks": blocks}, f, indent=1, ensure_ascii=False)
    f.write('\n')
print("executive summary written; toplines:", len(TOP))
