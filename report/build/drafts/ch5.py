"""FIRST-DRAFT GENERATOR ONLY. After the figure check (4 Nov 2026) the JSON files in content/ are the source of record; do not re-run this script.
Chapter 5 Monitoring and evaluation framework. Writes content/ch5/01 to 07.
Targets: printed model values where they exist; computed values are labelled (constant-rate path between printed
end points; geometric mean between printed year points). Jobs: Wesgro ratio of 2 jobs per 100 international
passengers (jobs_research.md, public source), applied to the arrivals path. No other target level is invented:
where no deliverable supports a level, the target is a direction or a milestone, marked proposed."""
import json, os

OUT = os.path.join(os.path.dirname(__file__), '..', 'content', 'ch5')
os.makedirs(OUT, exist_ok=True)


def write(name, sid, title, blocks):
    with open(os.path.join(OUT, name), 'w') as f:
        json.dump({"id": sid, "title": title, "blocks": blocks}, f, indent=1, ensure_ascii=False)
        f.write('\n')


# ---------------------------------------------------------------- 5.1 Results chain
chain_svg = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 560" width="1600" height="560" font-family="Raleway, Arial, sans-serif">'
    '<rect width="1600" height="560" fill="#ffffff"/>'
)
cols = [("Inputs", "#5B6572", ["Wesgro budget and units", "Partner budgets", "Data from SA Tourism,", "ACSA, Stats SA, OTAs"]),
        ("Activities", "#1F7A8C", ["18 initiatives,", "I1 to I18", "82 actions by tier", "(Chapter 3)"]),
        ("Outputs", "#7A9E7E", ["36 Tier 3 indicators", "Calendar published,", "fund constituted,", "routes bookable"]),
        ("Outcomes", "#C98B2B", ["25 Tier 2 indicators", "Seats, readiness,", "bookability, hub", "arrivals, pilots"]),
        ("Impact", "#0B3C5D", ["7 Tier 1 indicators", "Arrivals, spend, jobs,", "green season, spread,", "community spend"])]
x = 40
for i, (t, c, lines) in enumerate(cols):
    chain_svg += f'<rect x="{x}" y="60" width="270" height="360" rx="10" fill="{c}"/>'
    chain_svg += f'<text x="{x + 135}" y="112" text-anchor="middle" font-size="30" font-weight="700" fill="#fff">{t}</text>'
    for k, ln in enumerate(lines):
        chain_svg += f'<text x="{x + 135}" y="{180 + k * 40}" text-anchor="middle" font-size="22" fill="#fff">{ln}</text>'
    if i < 4:
        chain_svg += f'<polygon points="{x + 278},230 {x + 304},240 {x + 278},250" fill="#5B6572"/>'
        chain_svg += f'<line x1="{x + 272}" y1="240" x2="{x + 284}" y2="240" stroke="#5B6572" stroke-width="4"/>'
    x += 312
chain_svg += ('<rect x="40" y="460" width="1520" height="70" rx="8" fill="#F3F6F9"/>'
              '<text x="800" y="503" text-anchor="middle" font-size="22" fill="#1C2431">Wesgro controls the first three columns; outcomes and impact also depend on airlines, national government and the wider economy</text></svg>')

LOGIC = {
    1: [["I1 Segment-led activation and yield", "T3-01, T3-02 segment targets set; spend moved to conversion", "T2-01 segment home-market arrivals; T2-07 mature-market spend per visitor", "T1-01, T1-02, T1-03"],
        ["I2 Green-season events calendar", "T3-03, T3-04 calendar published; green-season bids", "T2-02 ICCA meetings; T2-03 May to September seat share", "T1-05"],
        ["I3 Bookable province", "T3-05, T3-06 census published; operators onboarded", "T2-04 operators bookable online; T2-05 CapeNature online share", "T1-06"],
        ["I4 India and China hub conversion", "T3-07, T3-08 carrier agreements; route cases", "T2-06 India and China hub arrivals", "T1-01, T1-02"],
        ["I5 Regional Africa", "T3-09, T3-10 activation run; capacity cases", "T2-08 African arrivals and spend", "T1-02, T1-03"]],
    2: [["I6 Route development and seat retention", "T3-11, T3-12 fund constituted; runway reports", "T2-09 seats and routes; T2-10 routes above 80% load", "T1-01"],
        ["I7 Cruise growth through product", "T3-13, T3-14 excursions listed; lines engaged", "T2-11 cruise calls and passengers", "T1-03"],
        ["I8 Corridor mobility", "T3-15, T3-16 Southern Line product; shuttles bookable", "T2-12 accessibility; T2-13 corridor transfer products", "T1-06"],
        ["I9 Corridor product development", "T3-17, T3-18 itineraries listed; assets activated", "T2-14 readiness by district", "T1-06"],
        ["I10 Visitor experience and quality", "T3-19, T3-20 charter adopted; businesses certified", "T2-15 routes rated Ready", "T1-03"],
        ["I11 Flagship site demand management", "T3-21, T3-22 baseline published; flow tools in place", "T2-16 peak Cableway queue", "T1-06"]],
    3: [["I12 Community inclusion pilots", "T3-23, T3-24 pilots selected; tests held", "T2-17 communities with a live booking route", "T1-07"],
        ["I13 Climate resilience and LTO funding", "T3-25, T3-26 risk register; funding model", "T2-18 LTOs funded; T2-19 weather losses", "T1-06"],
        ["I14 Tourism investment pipeline", "T3-27, T3-28 cases prepared; investor engagements", "T2-20 projects at financial close", "T1-03, T1-04"],
        ["I15 Steerco and three-tier alignment", "T3-29, T3-30 quarterly Steerco; joint industry plan", "T2-21 escalations resolved; T2-22 partners in the joint plan", "All"],
        ["I16 Data protocol and intelligence", "T3-31, T3-32 agreements signed; dashboard live", "T2-23 data feeds in the dashboard", "All"],
        ["I17 Access and safety escalation", "T3-33, T3-34 agenda tabled; responses logged", "T2-24 visa processing time", "T1-01, T1-02"],
        ["I18 Labour analysis and skills plan", "T3-35, T3-36 analysis published; skills plan adopted", "T2-25 labour analysis published", "T1-04"]],
}
LOGIC_COLS = [{"header": "Initiative (activity)", "width": 2.0, "align": "left"}, {"header": "Outputs (Tier 3)", "width": 2.2, "align": "left"},
              {"header": "Outcomes (Tier 2)", "width": 2.4, "align": "left"}, {"header": "Impact (Tier 1)", "width": 1.2, "align": "left"}]
b51 = [
    {"type": "h2", "text": "5.1 Results chain"},
    {"type": "lead", "text": "Every initiative is measured at three levels: what it produces, what changes because of it and what that adds to the 2035 case."},
    {"type": "p", "text": "The framework is the written form of the M&E toolkit the SLA requires (clauses 1.1.4 and 1.1.10). It sets indicators, baselines and targets for arrivals, spend, jobs, airlift, cruise and SMME inclusion, with the tools to track them [clause wording to be checked against the signed Annexure B]. The Inception Report adds geographic spread and asks for definitions, sources, frequency, owners and governance for each indicator (Inception Report, Nov 2025, p22)."},
    {"type": "figure", "id": "fig_5_chain", "caption": "Initiatives produce outputs Wesgro controls, which move outcomes Wesgro shares with partners, which add up to the 2035 impact.", "source": "Letsema, results chain for the plan.", "svg": chain_svg},
    {"type": "p", "text": "The three tables below give the chain for each pillar. Tier 3 output indicators come from the initiative charters, Tier 2 outcome indicators from the focus areas and Tier 1 impact indicators from the growth case."},
    {"type": "table", "caption": "Pillar 1 initiatives move arrivals, market mix, spend and the green-season share.", "source": "Initiative charters (section 4.3); indicator register (section 5.2).", "columns": LOGIC_COLS, "rows": LOGIC[1], "boldFirstCol": True},
    {"type": "table", "caption": "Pillar 2 initiatives move seats, cruise volumes and the share of visitors and spend outside the Metro.", "source": "Initiative charters (section 4.3); indicator register (section 5.2).", "columns": LOGIC_COLS, "rows": LOGIC[2], "boldFirstCol": True},
    {"type": "table", "caption": "Pillar 3 initiatives move community spend and jobs, and supply the governance and data every other indicator relies on.", "source": "Initiative charters (section 4.3); indicator register (section 5.2).", "columns": LOGIC_COLS, "rows": LOGIC[3], "boldFirstCol": True},
]
write("01_results_chain.json", "5.1", "Results chain", b51)

# ---------------------------------------------------------------- 5.2 Indicator set
T1 = [
    ["T1-01", "International arrivals", "Arrivals, growth-model basis; quarterly proxy: international passenger arrivals at CTIA", "SA Tourism; ACSA", "Annual; quarterly proxy", "Research"],
    ["T1-02", "Arrivals by market group", "Arrivals in the mature, hub, regional, acceleration and strategic groups", "SA Tourism", "Annual", "Research"],
    ["T1-03", "Direct foreign spend", "Foreign direct spend in the Western Cape, rand", "SA Tourism", "Annual; quarterly shares", "Research"],
    ["T1-04", "Tourism jobs", "Jobs supported by international air arrivals, on Wesgro's ratio, until the labour analysis sets a provincial measure", "Wesgro ratio; Stats SA TSA", "Annual", "Research"],
    ["T1-05", "Green-season share", "Share of overseas visitor travel in April to September", "SA Tourism; Wesgro visitor tracking", "Annual", "Research"],
    ["T1-06", "Share outside the Metro", "Share of arrivals and of spend recorded outside the Cape Metro", "SA Tourism provincial data; data protocol", "Annual", "Research"],
    ["T1-07", "Community share of foreign direct spend", "Spend traced to businesses trading inside the 20 shortlisted communities, as a share of foreign direct spend", "Pilot records; SA Tourism", "Annual", "Tourism; Research"],
]
T2 = [
    ["T2-01", "Arrivals from the four largest segment home markets (UK, Germany, USA, India)", "1", "503,277 (2025, computed)", "MA p21, p22"],
    ["T2-02", "ICCA association meetings in Cape Town", "2", "58 (2024)", "DSA p37"],
    ["T2-03", "May to September share of international seats at CTIA", "2", "34.0% (2025, computed)", "MIDAS"],
    ["T2-04", "Share of operators bookable online, by district", "3", "Not in hand; about 40% or more of smaller operators lack online booking", "IR p32"],
    ["T2-05", "CapeNature reservations made online", "3", "About 70% through the call centre", "SIR p42"],
    ["T2-06", "India and China arrivals via hubs", "4", "India 71,000; China 29,600 (2025)", "MIDAS"],
    ["T2-07", "Spend per visitor, mature markets", "5", "USA R32,900; UK R26,500; Germany R25,600 (2024)", "DSA p14"],
    ["T2-08", "African arrivals and spend", "6", "323,971 arrivals (2024); R4.2bn spend (2025)", "DSA p27, p29"],
    ["T2-09", "International seats and routes at CTIA", "7", "3,816,797 seats on 27 tabled routes (year to Nov 2025); 29 routes (2026)", "MIDAS"],
    ["T2-10", "Routes above 80% load", "7", "11 of 27 (year to Nov 2025)", "MIDAS"],
    ["T2-11", "Cruise calls and passengers", "8", "79 vessels; 127,178 passengers (2024/25)", "Diag p37"],
    ["T2-12", "Accessibility score by district", "9", "Metro 4.7 to Central Karoo 1.0 (2026)", "IR p88"],
    ["T2-13", "Corridor transfer products on sale", "9", "No inter-town tourism shuttle on the Garden Route", "IR p90"],
    ["T2-14", "Overall readiness by district", "10", "Metro 4.5; Garden Route and Winelands 3.4; Overberg 2.7; West Coast 2.5; Central Karoo 1.9", "IR p28 to p85"],
    ["T2-15", "Touring routes rated Ready", "11", "1 of 6 (2026)", "IR p30"],
    ["T2-16", "Peak queue at the Cableway", "12", "Up to three hours up and two down", "SIR p36"],
    ["T2-17", "Communities with a live booking route", "13", "0 of 19 profiled rate Ready on bookability", "SCIP p28"],
    ["T2-18", "LTOs with a funding agreement", "14", "Not in hand", "SIR p25"],
    ["T2-19", "Weather losses at flagship sites", "14", "Robben Island roughly R16m a year", "SIR p33"],
    ["T2-20", "Tourism projects at financial close", "15", "None; tourism gaps carry no committed capital", "IR p32 to p87"],
    ["T2-21", "Escalation items answered by the national tier", "16", "No agenda tabled yet", "This plan"],
    ["T2-22", "Industry partners signed up to the joint plan", "17", "No joint plan; 15 of 16 organisations raised collaboration", "SIR p20 to p46"],
    ["T2-23", "Automated data feeds in the dashboard", "18", "None; no dashboard", "This plan"],
    ["T2-24", "Visa processing time, priority markets", "19", "Not in hand", "SIR p36, p45"],
    ["T2-25", "Tourism labour analysis published", "20", "Not commissioned", "Inc p4"],
]
T3 = [
    ["T3-01, T3-02", "I1", "Segment targets in Wesgro's annual plan; share of market budget in trade-led conversion"],
    ["T3-03, T3-04", "I2", "Green-season calendar published; bids submitted for May to September events"],
    ["T3-05, T3-06", "I3", "Bookability census published; operators onboarded to online booking"],
    ["T3-07, T3-08", "I4", "Joint marketing agreements with hub carriers; India and China route cases prepared"],
    ["T3-09, T3-10", "I5", "Activation programmes run in Nigeria and Kenya; regional capacity cases made"],
    ["T3-11, T3-12", "I6", "Air access fund constituted; quarterly runway milestone reports issued"],
    ["T3-13, T3-14", "I7", "Excursion packages listed; lines engaged on expedition and home-porting"],
    ["T3-15, T3-16", "I8", "Southern Line visitor product launched; corridor shuttle products bookable"],
    ["T3-17, T3-18", "I9", "Multi-day itineraries listed per route; cold-zone assets activated"],
    ["T3-19, T3-20", "I10", "Quality charter adopted; businesses certified"],
    ["T3-21, T3-22", "I11", "Flagship baseline published; flow-management tools in place"],
    ["T3-23, T3-24", "I12", "Pilot communities selected; fixed-date tests held"],
    ["T3-25, T3-26", "I13", "Climate risk register published; LTO funding model agreed"],
    ["T3-27, T3-28", "I14", "Investment cases prepared; investor engagements held"],
    ["T3-29, T3-30", "I15", "Steerco meetings held each quarter; joint industry plan agreed"],
    ["T3-31, T3-32", "I16", "Data-sharing agreements signed; dashboard live"],
    ["T3-33, T3-34", "I17", "Escalation agenda tabled; responses logged"],
    ["T3-35, T3-36", "I18", "Labour analysis published; skills plan adopted"],
]
b52 = [
    {"type": "pagebreak"},
    {"type": "h2", "text": "5.2 Indicator set"},
    {"type": "lead", "text": "Seven impact indicators, twenty-five outcome indicators and thirty-six output indicators measure the plan, each with a definition, a source, an owner and a frequency."},
    {"type": "p", "text": "Tier 1 measures the 2035 case and is reported to the Board. Tier 2 measures the focus areas, one or two each, and is reported to Steerco each quarter where the source allows. Tier 3 measures the initiatives' own outputs and is reported by the leads to the programme office each month. The full register, with targets, sits in the toolkit (section 5.7)."},
    {"type": "table", "caption": "Seven Tier 1 indicators measure arrivals, market mix, spend, jobs, season, spread and community spend.",
     "source": "Letsema, indicator register; SLA clauses 1.1.4 and 1.1.10; Inception Report, Nov 2025, p22. Baselines and targets in section 5.3.",
     "columns": [{"header": "Code", "width": 0.6, "align": "left"}, {"header": "Indicator", "width": 1.5, "align": "left"}, {"header": "Definition", "width": 2.8, "align": "left"}, {"header": "Source", "width": 1.4, "align": "left"}, {"header": "Frequency", "width": 1.0, "align": "left"}, {"header": "Owner", "width": 0.8, "align": "left"}],
     "rows": T1, "boldFirstCol": True},
    {"type": "table", "caption": "Twenty-five Tier 2 indicators give each focus area one or two outcome measures, and seven of them have no baseline yet.",
     "source": "Chapter 3 evidence tables. MA: Market Assessment Report, May 2026. DSA: Demand-Side Analysis, Jun 2026. IR: Infrastructure Report, Jul 2026. SIR: Stakeholder Insights Report, Mar 2026. SCIP: SME and Community Inclusion Plan, Sep 2026. Diag: Current State Diagnostic, Dec 2025. Inc: Inception Report, Nov 2025. MIDAS: MIDAS Aviation Market Assessment, Mar 2026. Computed values are sums or shares of printed figures.",
     "columns": [{"header": "Code", "width": 0.6, "align": "left"}, {"header": "Indicator", "width": 2.6, "align": "left"}, {"header": "Focus area", "width": 0.7, "align": "center"}, {"header": "Baseline", "width": 2.6, "align": "left"}, {"header": "Source", "width": 1.3, "align": "left"}],
     "rows": T2, "boldFirstCol": True},
    {"type": "table", "caption": "Thirty-six Tier 3 output indicators, two per initiative, track what each lead delivers.",
     "source": "Initiative charters, section 4.3. Each output has a baseline of zero at the start of 2027.",
     "columns": [{"header": "Codes", "width": 1.2, "align": "left"}, {"header": "Initiative", "width": 0.8, "align": "left"}, {"header": "Outputs", "width": 5.8, "align": "left"}],
     "rows": T3, "boldFirstCol": True},
]
write("02_indicators.json", "5.2", "Indicator set", b52)

# ---------------------------------------------------------------- 5.3 Baselines and targets
b53 = [
    {"type": "pagebreak"},
    {"type": "h2", "text": "5.3 Baselines and targets"},
    {"type": "lead", "text": "The arrivals targets come straight from the growth model, the jobs targets from a stated ratio, and the other Tier 1 targets wait for baselines that do not yet exist."},
    {"type": "p", "text": "Baselines are fixed at calendar 2025 for the growth-model indicators and at FY2024/25 for the airport series, the recovery baseline used in Chapter 1. Targets follow two paths: the base case, which assumes Wesgro's current activity continues with hub carriers adding capacity, and the accelerated case, which adds direct India and China routes and dedicated activation (Demand-Side Analysis, Jun 2026, p19). The model prints the base case for 2028, 2030, 2032, 2034 and 2035, and the other paths for 2035 only. The 2031 base value and the accelerated milestones are computed and marked as such."},
    {"type": "figure", "id": "fig_5_paths", "caption": "Only the accelerated path clears 2.5 million arrivals in 2035, and the base path passes the 1.8m seat ceiling before 2031.",
     "source": "Market Assessment Report, May 2026, p19 (2025 base); Demand-Side Analysis, Jun 2026, p20, p21 (2028 and 2035 points; 1.8m ceiling). The 2031 base value is the geometric mean of the printed 2030 and 2032 points; the accelerated and conservative milestones are computed at a constant rate between the printed 2025 and 2035 values.",
     "chart": {"type": "line", "categories": ["2025", "2028", "2031", "2035"],
               "series": [{"name": "Accelerated", "values": [1498829, 1750871, 2045297, 2516282], "color": "#1F7A8C"},
                          {"name": "Base", "values": [1498829, 1673855, 1871637, 2175778], "color": "#0B3C5D"},
                          {"name": "Conservative", "values": [1498829, 1589411, 1685468, 1822634], "color": "#7A9E7E"}],
               "unit": "", "yMin": 1400000, "refLines": [{"value": 1800000, "label": "1.8m inbound seat ceiling"}],
               "footnote": "Milestone years only; the intervals are three, three and four years."}},
    {"type": "table", "caption": "Arrivals and jobs carry targets on both paths; spend carries the working analysis's base path; the other Tier 1 indicators carry dated baselines first.",
     "source": "T1-01: Market Assessment Report, May 2026, p19; Demand-Side Analysis, Jun 2026, p20, p21 (computed values marked *). T1-03: Demand-Side Analysis, Jun 2026, p11 (baseline); Market Assessment Report, May 2026, p24 (modelled base path, working analysis). T1-04: Wesgro's ratio of two jobs per 100 international passengers, applied to T1-01 (computed; public source, see the note below). T1-05: Demand-Side Analysis, Jun 2026, p12; Current State Diagnostic, Dec 2025, p32. T1-07: SME and Community Inclusion Plan, Sep 2026, p5.",
     "columns": [{"header": "Indicator", "width": 1.5, "align": "left"}, {"header": "Baseline", "width": 1.6, "align": "left"}, {"header": "2028 base / accelerated", "width": 1.5, "align": "left"}, {"header": "2031 base / accelerated", "width": 1.5, "align": "left"}, {"header": "2035 base / accelerated", "width": 1.6, "align": "left"}],
     "rows": [
         ["T1-01 International arrivals", "1,498,829 (2025); CTIA 1.44m (FY24/25)", "1,673,855 / 1,750,871*", "1,871,637* / 2,045,297*", "2,175,778 / 2,516,282"],
         ["T1-02 Arrivals by market group", "Mature 587,287; hubs 427,803; regional 292,514; acceleration 182,815 (2025)", "Base path by group, section 2.1", "2030: 670,350; 523,523; 343,096; 255,159", "766,067; 634,387; 402,812; 358,633 (base); accelerated not split"],
         ["T1-03 Direct foreign spend", "R25.9bn (FY2025)", "Not printed", "R33.7bn in 2030 (base, modelled)", "R40.6bn (base, modelled); accelerated not modelled"],
         ["T1-04 Tourism jobs (ratio)", "About 30,000 jobs supported (2025)", "33,500 / 35,000*", "37,400 / 40,900*", "43,500 / 50,300*"],
         ["T1-05 Green-season share", "About 35% (2025, provisional; 38.1% normalised); 39% (2024)", "Level set at Gate 1", "Rising", "Rising"],
         ["T1-06 Share outside the Metro", "Not in hand; baseline due in 2027 from the data protocol", "Baseline set", "Rising", "Rising"],
         ["T1-07 Community share of spend", "0.02% to 0.04%; R4m to R10m a year (floor)", "Pilots measured", "Level set after the pilots", "1% (R259m at FY2025 spend) as the reference point"],
     ], "boldFirstCol": True},
    {"type": "p", "text": "**Arrivals.** The model's 2025 base and the airport series measure different things: tourist arrivals on the model's basis, and international passenger arrivals at Cape Town International. The airport series is the quarterly proxy because ACSA publishes it, and it stood at 1.44m in FY24/25 and 1.57m in FY25/26 (Demand-Side Analysis, Jun 2026, p11). Both are reported, each against its own history."},
    {"type": "p", "text": "**Jobs.** No deliverable carries a provincial tourism employment baseline, and the Pero tourism table could not be retrieved [provincial tourism employment baseline: Wesgro Research to supply from the Pero 2025 or the Stats SA provincial TSA]. The Tier 1 measure is therefore jobs supported by international air arrivals, on Wesgro's own rule of thumb of two jobs for every 100 international passengers, which counts direct, indirect and induced jobs (public source: Wesgro and Cape Town Air Access releases, 2023 to 2024) [methodology note for the ratio: Cape Town Air Access to supply]. Applied to the arrivals paths, it gives about 30,000 jobs in 2025 and adds about 13,500 on the base path and 20,300 on the accelerated path by 2035. It is a ratio-based projection, not a labour-market measure."},
    {"type": "p", "text": "The ratio does not reach the 300,000 tourism-linked jobs in the Inception Report's ambition, because it counts only jobs linked to international air arrivals (Inception Report, Nov 2025, p4). The report restates the 300,000 as a total-sector figure for the labour analysis to test (I18). For context, public sources put direct tourism employment at 106,707 in Cape Town in 2024 (City of Cape Town, Economic Value of Tourism, 2025) and 953,981 nationally in 2024 (Stats SA Tourism Satellite Account, provisional, as reported in 2026)."},
    {"type": "p", "text": "**Green season.** Plan decision 6 sets the October to March share at about 65% for 2025, provisional, which puts the green season at about 35%. The 2025 month table sums to 104.9%, and once normalised it gives 61.9% and 38.1%, in line with the printed 61% and 39% for 2024 (Demand-Side Analysis, Jun 2026, p12; Current State Diagnostic, Dec 2025, p32). The report recommends the normalised figure as the baseline [Michael to confirm: switch the T1-05 baseline to 38.1%]."},
    {"type": "p", "text": "**Spread and community spend.** No deliverable prints district visitor spend, so the share outside the Metro has no baseline until the data protocol delivers one (I16). The community share starts from the Inclusion Plan's traced floor; its 1% is a reference point the plan prints, not a target any party has adopted (SME and Community Inclusion Plan, Sep 2026, p5)."},
]
write("03_baselines_targets.json", "5.3", "Baselines and targets", b53)

# ---------------------------------------------------------------- 5.4 Data sources and gaps
b54 = [
    {"type": "pagebreak"},
    {"type": "h2", "text": "5.4 Data sources and gaps"},
    {"type": "lead", "text": "Arrivals, seats and cruise volumes can be tracked from existing feeds; spread, bookability, jobs and community spend cannot until new data is built or shared."},
    {"type": "p", "text": "Stakeholders put data among the top barriers: no approved methodology exists for provincial tourism GDP and jobs (Stakeholder Insights Report, Mar 2026, p37), and no one holds a single view of visitor behaviour (Current State Diagnostic, Dec 2025, p56, p57). The data-sharing protocol under focus area 18 (I16) is the route to closing the gaps below."},
    {"type": "table", "caption": "Five sources cover most of the indicators, and each has a named holder the protocol must reach.",
     "source": "Letsema, from the indicator register; data holders as listed in Current State Diagnostic, Dec 2025, p56, p57.",
     "columns": [{"header": "Source", "width": 1.6, "align": "left"}, {"header": "Holder", "width": 1.4, "align": "left"}, {"header": "Indicators", "width": 2.0, "align": "left"}, {"header": "Frequency", "width": 1.0, "align": "left"}, {"header": "Status", "width": 1.8, "align": "left"}],
     "rows": [
         ["Departure survey and performance reports", "SA Tourism", "T1-01 to T1-03, T1-05, T2-07, T2-08", "Quarterly and annual", "Published; provincial cuts on request"],
         ["Passenger statistics and schedules", "ACSA; OAG", "T1-01 proxy, T2-03, T2-09", "Monthly", "Available; automated feed possible"],
         ["GDS bookings by route", "MIDAS or a data vendor", "T2-06, T2-10", "Annual", "Repeat commission needed"],
         ["Cruise season economic contribution", "Cruise Cape Town; StratEcon", "T2-11", "Each season", "Received by Wesgro; study not in this evidence base"],
         ["Infrastructure readiness scores", "Wesgro; Letsema method", "T2-12, T2-14, T2-15", "Every three years", "Re-score in 2029 and 2032"],
         ["Operator, site and pilot records", "LTOs; CapeNature; site operators; pilots", "T2-04, T2-05, T2-16, T2-17, T2-19", "Annual", "New collection under the protocol"],
     ], "boldFirstCol": True},
    {"type": "table", "caption": "Eleven data gaps stand between the plan and a full baseline, and each has a proposed owner and date.",
     "source": "Letsema, from the placeholders in Chapters 3 and 5; owners and dates proposed for Steerco to confirm.",
     "columns": [{"header": "Gap", "width": 3.0, "align": "left"}, {"header": "Indicator", "width": 0.9, "align": "left"}, {"header": "Proposed owner", "width": 1.6, "align": "left"}, {"header": "Proposed date", "width": 1.0, "align": "left"}, {"header": "Route", "width": 1.3, "align": "left"}],
     "rows": [
         ["District-level visitor arrivals and spend", "T1-06", "Research", "End 2027", "SA Tourism cut; protocol"],
         ["Provincial tourism employment baseline", "T1-04", "Research", "Mid 2027", "Pero; Stats SA provincial TSA"],
         ["Methodology for two jobs per 100 passengers", "T1-04", "Air Access", "Mid 2027", "Cape Town Air Access note"],
         ["Count of bookable products by district", "T2-04", "Research", "End 2027", "Bookability census (I3)"],
         ["Visitor counts and capacity at five flagship sites", "T2-16", "Research", "End 2027", "Request to operators (I11)"],
         ["Meetings, incentives and exhibitions volumes", "T2-02", "Convention Bureau", "End 2028", "Venue and DMC returns"],
         ["LTOs and their municipal funding", "T2-18", "DEDAT", "End 2027", "LTO survey"],
         ["Visa processing times by market", "T2-24", "Wesgro CEO's office", "End 2027", "Request to Home Affairs (I17)"],
         ["Nigeria and Ghana in the growth model", "T1-02", "Research", "Mid 2027", "Model update"],
         ["Source and definition of the 250 cruise-call plan", "T2-11", "Cruise Cape Town", "Mid 2027", "Cruise Cape Town"],
         ["Mid-scale accommodation stock by district", "T2-15", "Research", "End 2028", "Supply database or audit"],
     ], "boldFirstCol": True},
]
write("04_data.json", "5.4", "Data sources and gaps", b54)

# ---------------------------------------------------------------- 5.5 Tracking mechanism
dash_svg = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 820" width="1600" height="820" font-family="Raleway, Arial, sans-serif">'
    '<rect width="1600" height="820" fill="#ffffff"/>'
    '<rect x="30" y="20" width="1540" height="70" rx="8" fill="#0B3C5D"/>'
    '<text x="60" y="65" font-size="28" font-weight="700" fill="#fff">Tourism Growth Scorecard</text>'
    '<text x="1540" y="65" text-anchor="end" font-size="22" fill="#fff">Quarter | Phase | Gate status</text>'
)
tiles = ["Arrivals", "Market mix", "Spend", "Jobs", "Green season", "Outside Metro", "Community spend"]
for i, t in enumerate(tiles):
    x = 30 + i * 222
    dash_svg += f'<rect x="{x}" y="110" width="210" height="150" rx="8" fill="#F3F6F9" stroke="#C9D1DA"/>'
    dash_svg += f'<text x="{x + 105}" y="150" text-anchor="middle" font-size="21" font-weight="700" fill="#0B3C5D">{t}</text>'
    dash_svg += f'<text x="{x + 105}" y="200" text-anchor="middle" font-size="20" fill="#1C2431">Actual against</text>'
    dash_svg += f'<text x="{x + 105}" y="228" text-anchor="middle" font-size="20" fill="#1C2431">base and accelerated</text>'
dash_svg += ('<rect x="30" y="285" width="760" height="300" rx="8" fill="#ffffff" stroke="#C9D1DA"/>'
             '<text x="60" y="325" font-size="22" font-weight="700" fill="#0B3C5D">Seats and arrivals by month</text>'
             '<polyline points="70,540 160,500 250,470 340,520 430,560 520,555 610,500 700,430 760,410" fill="none" stroke="#0B3C5D" stroke-width="5"/>'
             '<polyline points="70,520 160,490 250,480 340,530 430,550 520,560 610,520 700,450 760,430" fill="none" stroke="#7A9E7E" stroke-width="5"/>'
             '<text x="60" y="575" font-size="18" fill="#5B6572">Automated feed: ACSA and OAG</text>'
             '<rect x="810" y="285" width="760" height="300" rx="8" fill="#ffffff" stroke="#C9D1DA"/>'
             '<text x="840" y="325" font-size="22" font-weight="700" fill="#0B3C5D">Initiative status, I1 to I18</text>')
for r in range(6):
    for c in range(3):
        col = ['#7A9E7E', '#C98B2B', '#7A9E7E', '#B23A48', '#7A9E7E', '#7A9E7E'][(r + c) % 6]
        x = 840 + c * 240; y = 350 + r * 36
        dash_svg += f'<rect x="{x}" y="{y}" width="24" height="24" rx="12" fill="{col}"/><text x="{x + 36}" y="{y + 19}" font-size="18" fill="#1C2431">I{r * 3 + c + 1}</text>'
dash_svg += ('<text x="840" y="575" font-size="18" fill="#5B6572">Manual entry by leads each month</text>'
             '<rect x="30" y="605" width="1540" height="190" rx="8" fill="#ffffff" stroke="#C9D1DA"/>'
             '<text x="60" y="645" font-size="22" font-weight="700" fill="#0B3C5D">Outcome indicators by pillar (Tier 2) and the escalation agenda</text>'
             '<text x="60" y="690" font-size="20" fill="#1C2431">Pillar 1: T2-01 to T2-08     Pillar 2: T2-09 to T2-16     Pillar 3: T2-17 to T2-25</text>'
             '<text x="60" y="730" font-size="20" fill="#1C2431">Each row: baseline, latest value, direction, target, source, last updated</text>'
             '<text x="60" y="770" font-size="18" fill="#5B6572">Escalation items: asked, of whom, date, response</text></svg>')
b55 = [
    {"type": "pagebreak"},
    {"type": "h2", "text": "5.5 Tracking mechanism"},
    {"type": "lead", "text": "A quarterly scorecard to Steerco, an annual outlook to the Board and a live dashboard where the sources allow it."},
    {"type": "p", "text": "Four principles run the tracking. Automate before collecting by hand: arrivals, seats and cruise volumes come from feeds that already exist. Name one owner for the dashboard (the programme office) and one for the definitions (Wesgro Research). Report every indicator against its own baseline and both paths. Refresh the register each year at the plan review."},
    {"type": "figure", "id": "fig_5_dashboard", "caption": "The scorecard puts the seven impact indicators on one line, then seats and arrivals by month, initiative status and the outcome indicators by pillar.", "source": "Letsema, dashboard concept. Illustrative layout; no values shown.", "svg": dash_svg},
    {"type": "table", "caption": "Monthly, quarterly and annual reporting run on a fixed calendar tied to Steerco and the Board.",
     "source": "Letsema, proposed reporting calendar.",
     "columns": [{"header": "Cycle", "width": 1.2, "align": "left"}, {"header": "What is reported", "width": 3.2, "align": "left"}, {"header": "From and to", "width": 2.0, "align": "left"}, {"header": "Format", "width": 1.4, "align": "left"}],
     "rows": [
         ["Monthly", "Tier 3 outputs and initiative status; seats and arrivals feeds", "Leads to the programme office", "Dashboard update"],
         ["Quarterly", "Tier 2 outcomes where available; risks rated high; escalation responses", "Programme office to Steerco", "Scorecard"],
         ["Annual", "Tier 1 impact against both paths; plan refresh; gate status", "Steerco to the Board; public at the business outlook event", "Outlook report"],
         ["At gates", "Gate tests in section 4.7", "Steerco to the Board", "Gate paper"],
     ], "boldFirstCol": True},
]
write("05_tracking.json", "5.5", "Tracking mechanism", b55)

# ---------------------------------------------------------------- 5.6 Evaluation
b56 = [
    {"type": "pagebreak"},
    {"type": "h2", "text": "5.6 Evaluation and learning"},
    {"type": "lead", "text": "Two evaluations bracket the plan: a mid-term review in 2030, when the seat ceiling binds, and a terminal evaluation in 2035."},
    {"type": "p", "text": "The mid-term review tests whether the plan is on its path and whether the path still holds. It falls in 2030 because that is when the base case reaches the 1.8 million seat ceiling (Demand-Side Analysis, Jun 2026, p21) and two years before relief at Cape Town International (Infrastructure Report, Jul 2026, p103). The terminal evaluation in 2035 measures the result against both paths and sets up the next plan. Both should be run by a party independent of the programme office."},
    {"type": "table", "caption": "Each pillar carries two evaluation questions, one on results and one on the assumptions behind them.",
     "source": "Letsema, proposed evaluation questions.",
     "columns": [{"header": "Pillar", "width": 1.4, "align": "left"}, {"header": "Did it work?", "width": 3.2, "align": "left"}, {"header": "Does the logic still hold?", "width": 3.2, "align": "left"}],
     "rows": [
         ["1 Reshape demand", "Did arrivals, spend per visitor and the green-season share move with the activation, and in which markets and segments?", "Is conversion still the constraint, or has access overtaken it in the growth markets?"],
         ["2 Transform supply", "Did seats, readiness and bookability rise outside the Metro, and did visitors follow?", "Did the airport relief arrive on time, and did the second gateways carry the load meanwhile?"],
         ["3 Build enabling capability", "Did the pilots meet their thresholds, and did community spend rise?", "Did the national asks get answers, and did the data protocol deliver the baselines?"],
     ], "boldFirstCol": True},
    {"type": "p", "text": "**Pilots before capital.** The inclusion pilots are evaluated before any capital is committed, on the Inclusion Plan's own measures: bookings, visitors and locally retained revenue (SME and Community Inclusion Plan, Sep 2026, p33). A pilot scales only when it meets the thresholds agreed before launch (p32). The same rule applies to any product or asset investment under I9 and I14: test demand, then invest."},
    {"type": "p", "text": "**Learning into the plan.** Findings from each review, gate and pilot go into the annual plan refresh under section 4.7, so the charters, targets and sequence change with the evidence rather than at the end of the plan."},
]
write("06_evaluation.json", "5.6", "Evaluation and learning", b56)

# ---------------------------------------------------------------- 5.7 Toolkit
b57 = [
    {"type": "h2", "text": "5.7 Toolkit handover"},
    {"type": "lead", "text": "The M&E toolkit turns this chapter into four working files that Wesgro Research owns from handover."},
    {"type": "table", "caption": "Four files make up the toolkit, and each has one owner in Wesgro.",
     "source": "Letsema; SLA clauses 1.1.10.2 and 1.1.15.3 [clause wording to be checked against the signed Annexure B].",
     "columns": [{"header": "File", "width": 1.6, "align": "left"}, {"header": "Contents", "width": 4.4, "align": "left"}, {"header": "Owner", "width": 1.8, "align": "left"}],
     "rows": [
         ["Indicator register", "All 68 indicators with definition, unit, source, frequency, owner, baseline and target by year and path", "Research"],
         ["Baseline workbook", "The baseline values with page references to the deliverables, and the computed values with their method", "Research"],
         ["Scorecard template", "The quarterly Steerco scorecard and the annual Board outlook", "Programme office"],
         ["Dashboard data model", "Feeds, refresh frequency and manual-entry forms for the dashboard in section 5.5", "Programme office"],
     ], "boldFirstCol": True},
    {"type": "p", "text": "Handover runs through knowledge-transfer sessions with Wesgro Research and the programme office, as the SLA requires (clause 1.1.15). The Excel toolkit itself is outside this report and is listed as an open item [M&E toolkit workbook: Letsema to deliver with the final report]."},
]
write("07_toolkit.json", "5.7", "Toolkit handover", b57)
print("chapter 5 written")
