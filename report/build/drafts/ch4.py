"""Chapter 4 Execution plan: 4.1, 4.2, 4.4 to 4.8. Writes content/ch4/01 to 08 (except 03, the charters, in ch4_charters.py).
Rules: leads are proposals for Steerco to confirm; no rand cost is invented (funding routes only, bands are open items);
phase years from plan decision 3; initiative list from traceability.csv."""
import json, os

OUT = os.path.join(os.path.dirname(__file__), '..', 'content', 'ch4')
os.makedirs(OUT, exist_ok=True)


def write(name, sid, title, blocks):
    with open(os.path.join(OUT, name), 'w') as f:
        json.dump({"id": sid, "title": title, "blocks": blocks}, f, indent=1, ensure_ascii=False)
        f.write('\n')


# code, name, focus areas, pillar, proposed lead, partners, Gantt cells
INIT = [
    ("I1", "Segment-led activation and yield in mature markets", "1, 5", 1, "Destination Marketing", "Research; trade and OTA partners; SA Tourism", "D I I I I I I I I"),
    ("I2", "Green-season events and business-events calendar", "2", 1, "Convention Bureau", "Destination Marketing; CTICC; City of Cape Town; DEDAT; LTOs", "D I I I I I I I I"),
    ("I3", "Bookable province programme", "3", 1, "Tourism", "Research; LTOs; district municipalities; OTAs; CapeNature", "D I I I I I I I I"),
    ("I4", "India and China hub conversion", "4", 1, "Destination Marketing", "Air Access; hub carriers; OTAs; trade", "D I I I I I I I I"),
    ("I5", "Regional Africa programme", "6", 1, "Destination Marketing", "Air Access; Convention Bureau; regional carriers; trade", "D I I I I I I I I"),
    ("I6", "Route development and seat retention, with a public-private air access fund", "7", 2, "Air Access", "DEDAT; City of Cape Town; ACSA; airlines; private sector", "I I I I I I I I I"),
    ("I7", "Cruise growth through product", "8", 2, "Cruise Cape Town", "Transnet National Ports Authority; V&A Waterfront; Mossel Bay municipality; cruise lines", "D I I I I I I I I"),
    ("I8", "Corridor mobility", "9", 2, "Tourism, with the Department of Mobility", "City of Cape Town; PRASA; district municipalities; private operators", "D D I I I I I I I"),
    ("I9", "Corridor product development", "10", 2, "Tourism", "LTOs; district municipalities; CapeNature; SANParks; private investors", "D D I I I I I I I"),
    ("I10", "Visitor experience and quality standards", "11", 2, "Tourism, with DEDAT", "Industry bodies; CATHSSETA; attraction operators", "D D I I I I I I I"),
    ("I11", "Flagship site demand management", "12", 2, "Site operators, with Wesgro Research", "SANParks; Table Mountain Aerial Cableway; CapeNature; Robben Island Museum; City of Cape Town", "D D I I I I I I I"),
    ("I12", "Community inclusion pilots", "13", 3, "Municipalities and LTOs, with Wesgro Tourism", "Municipalities; LTOs; community sellers; SAPS", "D I I I I I I I I"),
    ("I13", "Climate resilience and destination management, including LTO funding", "14", 3, "DEDAT, with Wesgro Research", "Municipalities; district municipalities; CapeNature; site operators", "D D I I I I I I I"),
    ("I14", "Tourism investment pipeline", "15", 3, "Wesgro investment promotion", "DEDAT; Tourism; private investors; municipalities", "D D I I I I I I I"),
    ("I15", "Tourism Growth Steerco and three-tier alignment", "16, 17", 3, "Wesgro CEO's office", "DEDAT; Cape Town Tourism; City of Cape Town; district municipalities; industry bodies", "I I I I I I I I I"),
    ("I16", "Data-sharing protocol and visitor intelligence", "18", 3, "Research", "Stats SA; SA Tourism; ACSA; Cape Town Tourism; booking platforms", "D I I I I I I I I"),
    ("I17", "Access and safety escalation agenda", "19", 3, "Wesgro CEO's office, with DEDAT", "Home Affairs; Department of Transport; SAPS; ACSA; SA Tourism", "I I I I I I I I I"),
    ("I18", "Tourism labour analysis and skills plan", "20", 3, "Research, with DEDAT", "CATHSSETA; industry bodies; training providers", "D D I I I I I I I"),
]
YEARS = [str(y) for y in range(2027, 2036)]

# ---------------------------------------------------------------- 4.1
rows41 = [[c, n, fa, lead, "Implement" if cells.split()[0] == 'I' else ("Design, then implement" if cells.split()[1] == 'I' else "Design")]
          for c, n, fa, p, lead, part, cells in INIT]
b41 = [
    {"type": "h2", "text": "4.1 From strategy to initiatives"},
    {"type": "lead", "text": "Twenty focus areas become eighteen initiatives, one per focus area except where one owner delivers two."},
    {"type": "p", "text": "The plan follows one chain from vision to measure. Each level answers a different question. The pillar says what must change and the focus area says where; the initiative says what Wesgro and its partners do, and the indicator says how Steerco will know it has happened (section 5.1)."},
    {"type": "table", "caption": "Seven levels run from the vision to the measures, and each level has a fixed count in this plan.",
     "source": "Chapter 3; traceability table, Appendix A1. Action count from the Chapter 3 action tables.",
     "columns": [{"header": "Level", "width": 1.4, "align": "left"}, {"header": "Count", "width": 0.8, "align": "right"}, {"header": "What it answers", "width": 2.8, "align": "left"}, {"header": "Example", "width": 2.8, "align": "left"}],
     "rows": [
         ["Vision", "1", "Where the province is going", "Grow international arrivals from 1.5m in 2025 toward 2.5m by 2035"],
         ["Pillars", "3", "What must change", "Reshape demand"],
         ["Themes", "6", "In which part of the system", "Source market growth and diversification"],
         ["Focus areas", "20", "Where the evidence says to act", "Convert India and China hub traffic"],
         ["Initiatives", "18", "What Wesgro and its partners do", "I4 India and China hub conversion"],
         ["Actions", "82", "Who does what, by tier", "Activate inside Xiaohongshu, Douyin and MakeMyTrip"],
         ["Indicators", "7, 25 and 36", "How Steerco knows, at impact, outcome and output level", "T2-06 India and China hub arrivals"],
     ], "boldFirstCol": True},
    {"type": "p", "text": "Two merges take twenty focus areas to eighteen initiatives. Segment-led marketing and mature-market yield share one owner and one set of channels, so focus areas 1 and 5 form initiative I1. Institutional alignment and industry collaboration share one forum, so focus areas 16 and 17 form I15. Every other focus area has its own initiative, numbered I1 to I18 in one sequence so that the M&E toolkit can track them on one list."},
    {"type": "p", "text": "Leads are proposed, not agreed. They follow the Wesgro units named in the Inception Report's stakeholder map and the actions in Chapter 3, and Steerco confirms them at its first meeting [Steerco to confirm initiative leads and partners]. Six initiatives have a partner as the accountable lead, because the main lever sits outside Wesgro's mandate: corridor mobility, quality standards, flagship sites, the community pilots, climate and LTO funding, and skills."},
    {"type": "table", "caption": "Eighteen initiatives cover the twenty focus areas, and eleven of them are in implementation by 2028.",
     "source": "Chapter 3 entries; proposed leads for Steerco to confirm. Phase 1 role from the Gantt in section 4.2.",
     "columns": [{"header": "Code", "width": 0.6, "align": "left"}, {"header": "Initiative", "width": 3.0, "align": "left"}, {"header": "Focus areas", "width": 0.9, "align": "left"}, {"header": "Proposed lead", "width": 2.0, "align": "left"}, {"header": "Phase 1 role", "width": 1.4, "align": "left"}],
     "rows": rows41, "boldFirstCol": True},
]
write("01_portfolio.json", "4.1", "From strategy to initiatives", b41)

# ---------------------------------------------------------------- 4.2
gantt_rows = []
for c, n, fa, p, lead, part, cells in INIT:
    short = n if len(n) <= 42 else n[:40].rsplit(' ', 1)[0]
    gantt_rows.append({"code": c, "name": short, "cells": dict(zip(YEARS, cells.split()))})
b42 = [
    {"type": "pagebreak"},
    {"type": "h2", "text": "4.2 Sequencing and phases"},
    {"type": "lead", "text": "Three phases run to 2035, and the first is weighted to the moves that change the 2030 constraint: seats, bookability, green-season events and the inclusion pilots."},
    {"type": "p", "text": "The phases follow calendar years: Activate from 2027 to 2028, Expand from 2029 to 2031 and Sustain from 2032 to 2035. Each phase ends at a decision gate tied to the Chapter 5 indicators (section 4.7). The first gate, at the end of 2028, falls in Wesgro's FY2028/29, two years before the base case reaches the seat ceiling at its 2030 point (Demand-Side Analysis, Jun 2026, p21)."},
    {"type": "figure", "id": "fig_4_gantt", "caption": "Three initiatives start in implementation in 2027, eleven are in implementation by 2028 and all eighteen by 2029.",
     "source": "Letsema, initiative portfolio (sections 4.1 and 4.3). Design means scoping, data, agreements and pilots; implement means delivery at scale.",
     "chart": {"type": "gantt", "years": YEARS, "phases": [{"name": "Activate", "from": "2027", "to": "2028"}, {"name": "Expand", "from": "2029", "to": "2031"}, {"name": "Sustain", "from": "2032", "to": "2035"}], "rows": gantt_rows}},
    {"type": "h3", "text": "Phase 1: Activate, 2027 to 2028"},
    {"type": "p", "text": "Phase 1 works inside Wesgro's mandate and budget and on the levers that move before the airport can. It holds and adds seats on the full routes and builds the air access fund (I6). It publishes the green-season calendar (I2), counts and starts to close the bookability gap (I3) and starts two or three inclusion pilots (I12). Steerco, the data-sharing protocol and the escalation agenda start in the first quarter (I15, I16, I17), because every other initiative reports through them."},
    {"type": "p", "text": "The marketing initiatives (I1, I4, I5) and cruise (I7) spend 2027 on design: segment targets, hub-carrier agreements, the Nigeria and Kenya plans and excursion products. Seven initiatives use both years for design (I8 to I11, I13, I14, I18). Their first task is a baseline or a case that no deliverable holds: corridor mobility, product, quality, flagship capacity, climate risk and LTO funding, the investment pipeline and the labour analysis. The gate at the end of 2028 asks whether seats on the full routes have held, whether the bookability baseline exists and is moving, and whether any pilot has met its thresholds."},
    {"type": "h3", "text": "Phase 2: Expand, 2029 to 2031"},
    {"type": "p", "text": "Phase 2 scales what Phase 1 proved and meets the seat ceiling. Hub conversion, regional Africa and segment marketing run at scale. Corridor mobility and product move from design to delivery, on the Garden Route, the Winelands and the Overberg first. The quality charter is adopted and phased by district, and the investment pipeline reaches financial close on its first projects. The mid-term review in 2030 tests arrivals against the base path when the ceiling binds, and checks that the runway is on its published dates (section 5.6)."},
    {"type": "h3", "text": "Phase 3: Sustain, 2032 to 2035"},
    {"type": "p", "text": "Phase 3 runs as relief arrives at Cape Town International: the international terminal about 2032 and the runway about 2033 (Infrastructure Report, Jul 2026, p103). The direct India and China route cases built since 2027 go to carriers as capacity frees up, which is the step the accelerated case depends on. Inclusion pilots that met their thresholds scale through channels, climate risk and LTO funding are embedded in municipal planning, and the terminal evaluation in 2035 closes the plan (section 5.6)."},
]
write("02_sequencing.json", "4.2", "Sequencing and phases", b42)

# ---------------------------------------------------------------- 4.4 RACI
RACI = {
    # Wesgro, Province, City/CTT, Districts/LTOs, SOEs, SAT, National depts, Industry and site operators
    "I1": "A/R C I I - C - C", "I2": "A/R C R R - I - C", "I3": "A/R C C R - - I C",
    "I4": "A/R I I - C C C C", "I5": "A/R I I - C C C C", "I6": "A/R R R - C I C C",
    "I7": "A/R I C C R - - C", "I8": "R A R R R - C C", "I9": "A/R C C R - - C C",
    "I10": "R A C C - - - R", "I11": "R C C C - - C A", "I12": "R C R A - - C C",
    "I13": "R A C R - - C R", "I14": "A/R R C C C - - C", "I15": "A/R R R R C C C R",
    "I16": "A/R C R C R R R C", "I17": "A/R R C C C C R C", "I18": "R A C C - - C R",
}
raci_rows = [[c, n] + RACI[c].split() for c, n, *_ in INIT]
b44 = [
    {"type": "pagebreak"},
    {"type": "h2", "text": "4.4 Roles and accountabilities"},
    {"type": "lead", "text": "Wesgro is accountable for twelve initiatives and does part of the work in all eighteen; for the other six, the accountable lead sits with another tier, and the plan names it."},
    {"type": "p", "text": "The matrix below assigns each initiative to the four roles: responsible (R) for doing the work, accountable (A) for the result, consulted (C) before decisions and informed (I) of progress. Where Wesgro is accountable and does the work itself, the cell reads A/R. Assignments are proposals for Steerco to confirm, built from the actions in Chapter 3."},
    {"type": "table", "caption": "Wesgro is accountable for twelve initiatives; provincial departments, municipalities or site operators are accountable for six, and SOEs or national departments do part of the work in four.",
     "source": "Letsema, from the Chapter 3 action tables; proposed for Steerco to confirm. Province: DEDAT and the Department of Mobility. SOEs: ACSA, Transnet and PRASA. National: Home Affairs, Transport, National Treasury and SAPS. Industry: industry bodies, airlines, CapeNature, SANParks and attraction operators.",
     "columns": [{"header": "Code", "width": 0.55, "align": "left"}, {"header": "Initiative", "width": 2.6, "align": "left"},
                 {"header": "Wesgro", "width": 0.62, "align": "center"}, {"header": "Province", "width": 0.62, "align": "center"},
                 {"header": "City, CTT", "width": 0.62, "align": "center"}, {"header": "Districts, LTOs", "width": 0.62, "align": "center"},
                 {"header": "SOEs", "width": 0.55, "align": "center"}, {"header": "SAT", "width": 0.5, "align": "center"},
                 {"header": "National", "width": 0.62, "align": "center"}, {"header": "Industry, sites", "width": 0.62, "align": "center"}],
     "rows": raci_rows, "boldFirstCol": True},
    {"type": "h3", "text": "National government and the state-owned entities"},
    {"type": "p", "text": "Four levers sit outside the province and cannot be bought or marketed into place: air service agreements and route rights, visa rules and border processing, the airport and port capital programmes, and policing (Current State Diagnostic, Dec 2025, p58; Infrastructure Report, Jul 2026, p103, p112). The plan treats them as an escalation agenda (I17), carried by Steerco through DEDAT to the national departments and SOEs. Each item is stated as a decision, an owner and a date the province is asking for. Wesgro's own route work (I6) runs inside the existing agreements meanwhile."},
    {"type": "h3", "text": "Provincial government"},
    {"type": "p", "text": "DEDAT is co-chair of Steerco and the accountable lead where the lever is policy or funding rather than promotion: quality standards (I10), LTO funding and climate risk (I13) and the labour analysis (I18). The Department of Mobility leads the transport half of corridor mobility (I8). Wesgro's units lead the demand, access, product and data initiatives and report through the programme office."},
    {"type": "h3", "text": "District and local government"},
    {"type": "p", "text": "Municipalities and LTOs hold the assets, the selling bodies and the visitor services that the regional and inclusion initiatives depend on. They lead the community selling bodies in the pilots (I12), attach covenants to public assets (I12, I14) and carry the route and product work in their districts (I3, I9). The City of Cape Town and Cape Town Tourism are partners on events, mobility and data (I2, I8, I16) and sit on Steerco."},
    {"type": "h3", "text": "The private sector and site operators"},
    {"type": "p", "text": "Airlines decide frequency and gauge, hotel investors decide the mid-scale tier, and attraction operators manage their own capacity. The plan gives them the evidence and the demand case. It asks for the decisions it cannot make for them: seats on full routes (I6), investment in secondary nodes (I14) and visitor-flow management at flagship sites, where the operators are accountable (I11)."},
]
write("04_raci.json", "4.4", "Roles and accountabilities", b44)

# ---------------------------------------------------------------- 4.5 Tactical wins
b45 = [
    {"type": "pagebreak"},
    {"type": "h2", "text": "4.5 Tactical wins for the first 24 months"},
    {"type": "lead", "text": "Twelve actions can start in 2027 inside Wesgro's current mandate, and each one unlocks a baseline, a seat or a booking path that a later initiative needs."},
    {"type": "p", "text": "The list is weighted the way Phase 1 is: seats, bookability, the green season, inclusion pilots and the data the rest of the plan reports on. Start dates are proposals in half-years. No action needs new capital; the funding route column says where the money comes from."},
    {"type": "table", "caption": "Twelve first-year actions use existing mandates and budgets and unlock the baselines and booking paths the later initiatives need.",
     "source": "Letsema, from the Chapter 3 action tables and the initiative charters (section 4.3). Owners and start dates are proposals for Steerco to confirm.",
     "columns": [{"header": "Action", "width": 2.8, "align": "left"}, {"header": "Initiative", "width": 0.7, "align": "left"}, {"header": "Proposed owner", "width": 1.4, "align": "left"}, {"header": "Start", "width": 0.7, "align": "left"}, {"header": "Funding route", "width": 1.1, "align": "left"}, {"header": "What it unlocks", "width": 2.0, "align": "left"}],
     "rows": [
         ["Hold winter seats with demand: joint green-season marketing with carriers on the full routes", "I6, I2", "Air Access", "2027 H1", "Wesgro operating", "Seats kept in May to September, when carriers cut first"],
         ["Publish a green-season events calendar and aim bids at May to September", "I2", "Convention Bureau", "2027 H1", "Wesgro operating", "A demand spine for the trough months"],
         ["Track the runway programme quarterly and commission a capacity-against-demand model to 2035", "I6", "Air Access", "2027 H1", "Wesgro operating", "Early warning on the binding constraint"],
         ["Constitute Steerco with terms of reference and table the first escalation agenda", "I15, I17", "Wesgro CEO's office", "2027 H1", "Wesgro operating", "One forum and one route to national decisions"],
         ["Agree the data-sharing protocol with ACSA, SA Tourism, Stats SA and Cape Town Tourism", "I16", "Research", "2027 H1", "Wesgro operating", "The feeds the scorecard needs"],
         ["Run a bookability census of provincial product by district", "I3", "Research", "2027 H1", "Wesgro operating", "The baseline for the bookability indicator"],
         ["Request visitor counts and capacity from the five flagship sites", "I11", "Research", "2027 H1", "Wesgro operating", "The flagship capacity baseline"],
         ["Commission the tourism labour analysis behind the jobs ambition", "I18", "Research, with DEDAT", "2027 H1", "Wesgro and DEDAT operating", "A tested jobs target"],
         ["Package the Garden Route and Route 62 with a shuttle transfer sold inside the itinerary", "I8, I9", "Tourism", "2027 H2", "Wesgro operating; operators", "Car-free multi-day trips beyond the Metro"],
         ["Package the Southern Line as a visitor product with the City and PRASA", "I8", "Tourism", "2027 H2", "Wesgro operating; City", "A scenic rail route to Boulders and Simon's Town"],
         ["Choose two or three pilot communities and agree with municipalities and LTOs who funds a seller with a stake in each", "I12", "Tourism", "2027 H2", "Municipal and LTO budgets", "The first test of the inclusion model"],
         ["Give each pilot community one live booking route before any promotion", "I12, I3", "LTOs, with Tourism", "2028 H1", "Municipal and LTO budgets", "Community product that can be bought"],
     ], "boldFirstCol": False},
]
write("05_tactical.json", "4.5", "Tactical wins for the first 24 months", b45)

# ---------------------------------------------------------------- 4.6 Funding
FUND = {  # Wesgro operating, provincial or municipal, national and SOE, private
    "I1": "● - - ○", "I2": "● ● - ○", "I3": "● ● ○ ○", "I4": "● - - ○", "I5": "● - - ○", "I6": "● ● ○ ●",
    "I7": "● - ● ○", "I8": "○ ● ● ○", "I9": "● ● ○ ●", "I10": "○ ● - ○", "I11": "○ ○ ● ●", "I12": "○ ● ○ ○",
    "I13": "○ ● ○ ○", "I14": "● ● - ●", "I15": "● ● - -", "I16": "● ○ ○ ○", "I17": "● ● - -", "I18": "● ● ○ ○",
}
fund_rows = [[c, n] + FUND[c].split() for c, n, *_ in INIT]
count = {k: sum(1 for c in FUND if FUND[c].split()[i] == '●') for i, k in enumerate(["Wesgro operating budget", "Provincial and municipal budgets", "National programmes and SOEs", "Private capital"])}
b46 = [
    {"type": "pagebreak"},
    {"type": "h2", "text": "4.6 Funding and investment"},
    {"type": "lead", "text": "Most of the plan runs on budgets that already exist; the capital it needs sits with ACSA, PRASA, Transnet and private investors, and none of it has been costed yet."},
    {"type": "p", "text": "No deliverable costs any initiative. The Inception Report scoped an investment opportunity framework with return scoring, but no separate output was delivered (Inception Report, Nov 2025, p18, p20), and stakeholders describe Western Cape tourism funding as materially below peer destinations without giving a figure (Stakeholder Insights Report, Mar 2026, p25). This section therefore sets the funding route for each initiative and leaves the rand bands to be set with Wesgro Finance and DEDAT [cost band per initiative and phase: Wesgro Finance and DEDAT to set before Steerco signs off the plan]."},
    {"type": "table", "caption": "Thirteen initiatives draw mainly on Wesgro's operating budget, and four need private capital as a main source.",
     "source": "Letsema, from the initiative charters (section 4.3). ● main source; ○ supporting source; – none expected. Rand values are not estimated.",
     "columns": [{"header": "Code", "width": 0.6, "align": "left"}, {"header": "Initiative", "width": 3.2, "align": "left"}, {"header": "Wesgro operating", "width": 1.0, "align": "center"}, {"header": "Provincial and municipal", "width": 1.0, "align": "center"}, {"header": "National and SOE", "width": 1.0, "align": "center"}, {"header": "Private capital", "width": 1.0, "align": "center"}],
     "rows": fund_rows, "boldFirstCol": True},
    {"type": "figure", "id": "fig_4_funding", "caption": "Wesgro's operating budget is the main source for most initiatives, while private capital is the main source for the capital-heavy ones.",
     "source": "Letsema, count of initiatives by main funding source from the table above. An initiative can have more than one main source.",
     "chart": {"type": "hbar", "categories": list(count.keys()), "values": list(count.values()), "unit": ""}},
    {"type": "p", "text": "**Crowding in capital.** The rule for capital is the Inclusion Plan's: invest after demand is shown, and attach a maintenance and marketing covenant to any public asset (SME and Community Inclusion Plan, Sep 2026, p15, p31). Wesgro's investment promotion work builds the tourism pipeline from the Infrastructure Report's gap-closure tables, where every district lists tourism gaps with no committed capital (I14; Infrastructure Report, Jul 2026, p32 to p87). The air access fund draws public and private money on the Chilean model (I6; Global Benchmarking Report, Mar 2026, p28)."},
    {"type": "p", "text": "**What the SLA asks and what is still to do.** The SLA asks for return projections on infrastructure priorities (clause 1.1.8.3) [clause wording to be checked against the signed Annexure B]. Those need costed projects, and the only costed items in hand are the airport, rail and port programmes the province does not fund. The return case is therefore an output of I14 in Phase 1, built project by project as the pipeline forms."},
]
write("06_funding.json", "4.6", "Funding and investment", b46)

# ---------------------------------------------------------------- 4.7 Governance
gov_svg = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 760" width="1600" height="760" font-family="Raleway, Arial, sans-serif">'
    '<rect width="1600" height="760" fill="#ffffff"/>'
    # Board
    '<rect x="600" y="30" width="400" height="80" rx="8" fill="#5B6572"/>'
    '<text x="800" y="66" text-anchor="middle" font-size="26" font-weight="700" fill="#fff">Wesgro Board and Exco</text>'
    '<text x="800" y="96" text-anchor="middle" font-size="20" fill="#fff">Annual outlook; gate decisions</text>'
    # Steerco
    '<rect x="520" y="170" width="560" height="110" rx="8" fill="#0B3C5D"/>'
    '<text x="800" y="210" text-anchor="middle" font-size="28" font-weight="700" fill="#fff">Tourism Growth Steerco</text>'
    '<text x="800" y="242" text-anchor="middle" font-size="20" fill="#fff">Chair: Wesgro CEO. With DEDAT and Cape Town Tourism</text>'
    '<text x="800" y="268" text-anchor="middle" font-size="20" fill="#fff">Quarterly scorecard; escalation agenda</text>'
    # Programme office
    '<rect x="560" y="340" width="480" height="100" rx="8" fill="#1F7A8C"/>'
    '<text x="800" y="380" text-anchor="middle" font-size="26" font-weight="700" fill="#fff">Programme office in Wesgro</text>'
    '<text x="800" y="412" text-anchor="middle" font-size="20" fill="#fff">Build, operate, transfer; dashboard owner</text>'
    # Initiative leads
    '<rect x="420" y="500" width="760" height="100" rx="8" fill="#7A9E7E"/>'
    '<text x="800" y="540" text-anchor="middle" font-size="26" font-weight="700" fill="#fff">Initiative leads, I1 to I18</text>'
    '<text x="800" y="572" text-anchor="middle" font-size="20" fill="#fff">Wesgro units and partner co-leads; charters in section 4.3</text>'
    # side boxes
    '<rect x="40" y="170" width="380" height="110" rx="8" fill="#ffffff" stroke="#B23A48" stroke-width="3"/>'
    '<text x="230" y="210" text-anchor="middle" font-size="22" font-weight="700" fill="#B23A48">National escalation</text>'
    '<text x="230" y="240" text-anchor="middle" font-size="19" fill="#1C2431">Home Affairs, Transport, Treasury,</text>'
    '<text x="230" y="264" text-anchor="middle" font-size="19" fill="#1C2431">SAPS, ACSA, SA Tourism</text>'
    '<rect x="1180" y="170" width="380" height="110" rx="8" fill="#ffffff" stroke="#C98B2B" stroke-width="3"/>'
    '<text x="1370" y="210" text-anchor="middle" font-size="22" font-weight="700" fill="#C98B2B">Partners at the table</text>'
    '<text x="1370" y="240" text-anchor="middle" font-size="19" fill="#1C2431">City of Cape Town, districts,</text>'
    '<text x="1370" y="264" text-anchor="middle" font-size="19" fill="#1C2431">industry bodies, site operators</text>'
    '<rect x="1180" y="340" width="380" height="100" rx="8" fill="#ffffff" stroke="#1F7A8C" stroke-width="3"/>'
    '<text x="1370" y="380" text-anchor="middle" font-size="22" font-weight="700" fill="#1F7A8C">Wesgro Research</text>'
    '<text x="1370" y="410" text-anchor="middle" font-size="19" fill="#1C2431">Indicators, data protocol, evaluation</text>'
    # connectors
    '<line x1="800" y1="110" x2="800" y2="170" stroke="#5B6572" stroke-width="3"/>'
    '<line x1="800" y1="280" x2="800" y2="340" stroke="#5B6572" stroke-width="3"/>'
    '<line x1="800" y1="440" x2="800" y2="500" stroke="#5B6572" stroke-width="3"/>'
    '<line x1="420" y1="225" x2="520" y2="225" stroke="#B23A48" stroke-width="3"/>'
    '<line x1="1080" y1="225" x2="1180" y2="225" stroke="#C98B2B" stroke-width="3"/>'
    '<line x1="1040" y1="390" x2="1180" y2="390" stroke="#1F7A8C" stroke-width="3"/>'
    # cadence strip
    '<rect x="40" y="650" width="1520" height="80" rx="8" fill="#F3F6F9"/>'
    '<text x="800" y="684" text-anchor="middle" font-size="21" font-weight="700" fill="#0B3C5D">Quarterly: scorecard to Steerco   |   Annual: outlook to the Board and plan refresh   |   Gates: end 2028, 2030 review, end 2031, 2035</text>'
    '<text x="800" y="714" text-anchor="middle" font-size="19" fill="#5B6572">Each gate decides on the next phase against the Chapter 5 indicators</text>'
    '</svg>'
)
b47 = [
    {"type": "pagebreak"},
    {"type": "h2", "text": "4.7 Delivery governance"},
    {"type": "lead", "text": "One Steerco, one programme office and four fixed decision points keep eighteen initiatives and three tiers of government on one plan."},
    {"type": "figure", "id": "fig_4_governance", "caption": "Steerco sits between the Board and the initiative leads, with a route to national government on one side and the partners on the other.", "source": "Letsema, proposed delivery governance.", "svg": gov_svg},
    {"type": "p", "text": "**Steerco.** A Tourism Growth Steerco chaired at Wesgro CEO level, with DEDAT and Cape Town Tourism as standing members and the City of Cape Town, the district municipalities and the industry bodies at the table. It receives the quarterly scorecard, clears cross-initiative issues, holds the escalation agenda and recommends gate decisions to the Board. Stakeholders asked for this kind of alignment directly: mobility responsibilities alone are split across three tiers of government (Stakeholder Insights Report, Mar 2026, p23)."},
    {"type": "p", "text": "**Programme office.** A small office inside Wesgro runs the plan on a build, operate and transfer basis. It builds the charters, the dashboard and the reporting calendar in Phase 1, runs them through Phase 2 and hands them to the line units by the end of 2031. It owns the scorecard and the dashboard, and Wesgro Research owns the indicator definitions and the data protocol (I16)."},
    {"type": "p", "text": "**Cadence.** Initiative leads report monthly to the programme office, Steerco meets quarterly and the Board receives an annual outlook, which also anchors the Unlocking Tourism business outlook event. The plan is refreshed each year against the indicators and the gate decisions."},
    {"type": "table", "caption": "Four decision points test the plan against its indicators, and each one decides what the next phase funds.",
     "source": "Letsema, proposed gates; indicator codes from section 5.2.",
     "columns": [{"header": "Gate", "width": 1.2, "align": "left"}, {"header": "When", "width": 0.9, "align": "left"}, {"header": "What it tests", "width": 3.4, "align": "left"}, {"header": "What it decides", "width": 2.3, "align": "left"}],
     "rows": [
         ["Gate 1", "End 2028", "Seats on full routes held or added (T2-09, T2-10); bookability baseline published and moving (T2-04); pilots against thresholds (T2-17); data protocol live (T2-23)", "Move to Expand; scale or stop each pilot; confirm route cases for India and China"],
         ["Mid-term review", "2030", "Arrivals against the base path at the seat ceiling (T1-01); runway on its published dates; green-season share (T1-05)", "Re-sequence Phase 2 if the ceiling binds early or relief slips"],
         ["Gate 2", "End 2031", "Spend and spread (T1-03, T1-06); corridor readiness (T2-14); investment at financial close (T2-20)", "Commit Phase 3 funding; take direct route cases to carriers"],
         ["Terminal evaluation", "2035", "All Tier 1 indicators against the base and accelerated paths", "Close the plan and set the next one"],
     ], "boldFirstCol": True},
]
write("07_governance.json", "4.7", "Delivery governance", b47)

# ---------------------------------------------------------------- 4.8 Risks
b48 = [
    {"type": "pagebreak"},
    {"type": "h2", "text": "4.8 Risks and dependencies"},
    {"type": "lead", "text": "Six of the ten material risks sit outside Wesgro's control, so the mitigation for most of them is early warning and a route to the tier that can act."},
    {"type": "p", "text": "Likelihood and impact are Letsema's assessment on a three-point scale, from the evidence cited in each row. Steerco reviews the register each quarter and the owner reports on any risk rated high on both."},
    {"type": "table", "caption": "Ten risks could move the plan off its path, and the two rated high on both measures concern the airport and the national air and visa regime.",
     "source": "Letsema assessment. Evidence: Current State Diagnostic, Dec 2025 (Diag); Stakeholder Insights Report, Mar 2026 (SIR); Infrastructure Report, Jul 2026 (IR); SME and Community Inclusion Plan, Sep 2026 (SCIP); Inception Report, Nov 2025 (Inc).",
     "columns": [{"header": "Risk", "width": 2.2, "align": "left"}, {"header": "Evidence", "width": 1.3, "align": "left"}, {"header": "Likelihood", "width": 0.8, "align": "left"}, {"header": "Impact", "width": 0.7, "align": "left"}, {"header": "Mitigation", "width": 2.4, "align": "left"}, {"header": "Owner", "width": 1.0, "align": "left"}],
     "rows": [
         ["Runway relief at Cape Town International slips past about 2033", "IR p103, p109", "Medium", "High", "Quarterly milestone tracking; frequency and gauge on full routes; George as second gateway (I6)", "Air Access; ACSA"],
         ["Bilateral air agreements and the US carrier cap stay restrictive", "SIR p24; Inc p8", "High", "High", "Escalation agenda with stated asks (I17); route work inside existing rights (I6)", "Steerco; DEDAT"],
         ["Visa processing for China, India and African markets does not improve", "SIR p36, p45; Diag p34", "Medium", "High", "Escalation agenda; processing time tracked as T2-24 (I17)", "Steerco"],
         ["Safety incidents or perception deter visitors", "Diag p55; SCIP p27, p30", "Medium", "High", "Safety gates before any pilot launch (I12); escalation to SAPS (I17)", "Tourism; Steerco"],
         ["Climate events close sites and routes", "SCIP p24; SIR p33, p43", "High", "Medium", "Climate risk register; itineraries routed around closures (I13)", "Research; DEDAT"],
         ["Water and power supply fail in peak season", "Diag p38, p43; IR p31", "Medium", "Medium", "Escalation of utility risks; off-grid power at remote sites (I13, I17)", "DEDAT; site operators"],
         ["LTO funding collapses under Treasury Circular 131", "SIR p25, p39", "High", "Medium", "Stable funding agreements with a development mandate (I13)", "DEDAT; municipalities"],
         ["Data holders do not share data", "SIR p37; Diag p57", "Medium", "Medium", "Data-sharing protocol with each holder (I16)", "Research"],
         ["Cruise growth reverses as Red Sea reroutes end", "IR p112", "Medium", "Low", "Diversify lines and add Mossel Bay day stops (I7)", "Cruise Cape Town"],
         ["Skills shortages cap service quality", "SIR p43; Inc p8", "Medium", "Medium", "Labour analysis and skills plan (I18); quality charter (I10)", "Research; DEDAT"],
     ], "boldFirstCol": True},
]
write("08_risks.json", "4.8", "Risks and dependencies", b48)
print("chapter 4 sections written", count)
