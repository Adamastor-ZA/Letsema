"""Appendices built from the report's own data: A1 (hypothesis evaluation evidence), A7 (action register),
A8 (M&E toolkit register) and A9 (glossary and references). Writes content/appendices/01, 07, 08, 09.
A2 to A6 are drafted from the extracts by the appendix workflow."""
import csv, json, os, glob

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, '..', 'content', 'appendices')
CH3 = os.path.join(HERE, '..', 'content', 'ch3')
os.makedirs(OUT, exist_ok=True)


def write(name, sid, title, blocks):
    with open(os.path.join(OUT, name), 'w') as f:
        json.dump({"id": sid, "title": title, "blocks": blocks}, f, indent=1, ensure_ascii=False)
        f.write('\n')


TR = list(csv.DictReader(open(os.path.join(HERE, '..', '..', 'traceability.csv'))))

# ---------------------------------------------------------------- A1
READING = {
    "FA01": ("Supported; the segmentation is directional and leaves out the domestic and seven African markets", "Strong"),
    "FA02": ("Supported: 6.4% of 2025 international seat capacity; ICCA meetings 33 to 58 from 2022 to 2024", "Strong"),
    "FA03": ("The 70% is CapeNature's reservation mix only; no count of bookable products exists", "Adequate"),
    "FA04": ("The sum of two printed estimates, 71,000 and 30,000; the hub tables sum to 97,579", "Strong"),
    "FA05": ("Five mature long-haul routes above 80% load; no fare or yield data", "Adequate"),
    "FA06": ("Supported as spend per visitor; the printed averages do not reproduce from the totals", "Strong"),
    "FA07": ("MIDAS prints eleven routes above 80%; sixteen run at 75% or more", "Adequate"),
    "FA08": ("79 vessels (Diagnostic) against 83 calls (Infrastructure Report); the 250 plan is in no deliverable", "Adequate"),
    "FA09": ("Supported on the attractions and services basis; the transport basis gives 5.0 to 1.0", "Strong"),
    "FA10": ("Cold zones is the Infrastructure Report's own term; no count of idle assets", "Strong"),
    "FA11": ("Stated in words; no room or bed count", "Adequate"),
    "FA12": ("Stakeholder statements and queue times; no visitor counts or caps for any flagship", "Adequate"),
    "FA13": ("Supported; one page prints 18 shortlisted; the spend-tracing method is not described", "Strong"),
    "FA14": ("Supported by two organisations' statements and the Inclusion Plan's De Rust profile", "Adequate"),
    "FA15": ("An inference: a large capital pipeline exists and none of it reaches tourism product", "Adequate"),
    "FA16": ("Supported by the Diagnostic's tier table; no decision-rights map exists", "Adequate"),
    "FA17": ("A reconstructed count of organisations, not insight rows", "Strong"),
    "FA18": ("Platforms exist; no data-sharing protocol in progress is described", "Adequate"),
    "FA19": ("Holds for visas and air rights; safety programmes are provincial and basic services local", "Strong"),
    "FA20": ("Confirmed: no provincial tourism employment baseline in any deliverable", "Thin"),
}
REASON = {"FA02": "June holds 6.4% of seats; ICCA", "FA03": "Community product unbookable, 70% by phone, OTA gaps",
          "FA07": "16 of 27 routes above 80%, fares before seats", "FA08": "79 calls in 2024/25, plan to 250",
          "FA19": "Levers sit nationally", "FA20": "Jobs goal has no labour analysis"}
a1_rows = []
for r in TR:
    fa = r['fa_id']
    reading, strength = READING[fa]
    a1_rows.append([f"{int(fa[2:])} {r['focus_area']}", r['disposition'].replace('Moved from theme 2.1', 'Moved').replace('Flagged, untested', 'Flagged'),
                    REASON.get(fa, r['reason_one_line']), reading, strength])
a1_rows2 = [[f"{int(r['fa_id'][2:])}", r['december_origin'].replace('>>', '').strip() or 'None', r['workstream'], r['evidence_sections'], r['initiative_ids'], r['indicator_codes']] for r in TR]
b_a1 = [
    {"type": "h2", "text": "A1 Hypothesis evaluation evidence"},
    {"type": "lead", "text": "Every disposition traces to a December entry, a workstream and pages in the deliverables, and each one-line reason is set against what those pages print."},
    {"type": "p", "text": "The first table sets each focus area's one-line reason, as recorded at the 14 October 2026 review, against what the deliverables support. It rates the evidence on a four-point scale: strong, adequate, thin or none in hand. The second table traces each focus area back to its December entry and forward to its initiative and indicators. The full traceability file, with page references for every row, ships with this report as traceability.csv."},
    {"type": "table", "caption": "Two figures in the one-line reasons are not supported, sixteen routes above 80% and the plan to 250 cruise calls, and several others hold only with a qualifier.",
     "source": "One-line reasons as recorded at the 14 October 2026 review [Summary of Findings, 14 Oct 2026, pp15 to 16: deck page reference to be confirmed]; reading and strength from the evidence notes behind Chapter 3. Strong: the figure and finding are printed in two deliverables or in one with a full table. Adequate: supported, with a figure missing, different or from one source. Thin: side mentions only.",
     "columns": [{"header": "Focus area", "width": 2.2, "align": "left"}, {"header": "Disposition", "width": 0.9, "align": "left"}, {"header": "Reason as recorded", "width": 1.8, "align": "left"}, {"header": "What the evidence supports", "width": 2.4, "align": "left"}, {"header": "Strength", "width": 0.8, "align": "left"}],
     "rows": a1_rows, "boldFirstCol": True},
    {"type": "table", "caption": "Nineteen focus areas descend from a December entry, and each one leads to one initiative and one to three indicators.",
     "source": "traceability.csv (Appendix A1 file). December entries as printed in Current State Diagnostic, Dec 2025, p64. Workstream attribution is this report's, from the deliverables that carry the figures.",
     "columns": [{"header": "FA", "width": 0.4, "align": "left"}, {"header": "December entry", "width": 2.0, "align": "left"}, {"header": "Workstream", "width": 2.0, "align": "left"}, {"header": "Chapter 2", "width": 0.9, "align": "left"}, {"header": "Initiative", "width": 0.7, "align": "left"}, {"header": "Indicators", "width": 1.4, "align": "left"}],
     "rows": a1_rows2, "boldFirstCol": True},
]
write("01_a1_traceability.json", "A1", "Hypothesis evaluation evidence", b_a1)

# ---------------------------------------------------------------- A7 action register
FA2I = {r['fa_id']: r['initiative_ids'] for r in TR}
rows7 = []
for f in sorted(glob.glob(os.path.join(CH3, '*.json'))):
    d = json.load(open(f))
    fa = None
    for b in d['blocks']:
        if b['type'] == 'kicker':
            n = int(b['text'].rsplit('Focus area', 1)[1].strip())
            fa = f"FA{n:02d}"
        if b['type'] == 'grid' and fa:
            for who, action, lead in b['rows']:
                rows7.append([FA2I[fa], str(int(fa[2:])), who, action, lead])
order = lambda r: (int(r[0][1:]), int(r[1]))
rows7.sort(key=order)
b_a7 = [
    {"type": "pagebreak"},
    {"type": "h2", "text": "A7 Initiative charters and action register"},
    {"type": "lead", "text": f"The {len(rows7)} actions in Chapter 3 are listed here by initiative, so each lead can see every action the plan asks of it and of its partners."},
    {"type": "p", "text": "Section 4.3 carries the eighteen charters in full, so this appendix does not repeat them. It lists the actions from the Chapter 3 action tables in initiative order, with the tier that acts and the proposed lead and partners. The programme office loads this register into the toolkit as the Tier 3 work plan."},
    {"type": "table", "caption": "Every Chapter 3 action belongs to one initiative, and each initiative carries actions for Wesgro, its partners and, where the lever is national, an escalation.",
     "source": "Chapter 3 action tables; initiative mapping from the traceability table. Leads and partners are proposals for Steerco to confirm.",
     "columns": [{"header": "Initiative", "width": 0.7, "align": "left"}, {"header": "FA", "width": 0.4, "align": "left"}, {"header": "Who acts", "width": 0.8, "align": "left"}, {"header": "Action", "width": 4.2, "align": "left"}, {"header": "Lead and partners", "width": 1.8, "align": "left"}],
     "rows": rows7, "boldFirstCol": True},
]
write("07_a7_actions.json", "A7", "Initiative charters and action register", b_a7)

# ---------------------------------------------------------------- A8 M&E register
T2 = [
    ["T2-01", "Arrivals from the UK, Germany, USA and India", "SA Tourism; growth model", "Annual", "Research", "726,330 (2035, base; computed from MA p21, p22)"],
    ["T2-02", "ICCA association meetings in Cape Town", "ICCA", "Annual", "Convention Bureau", "Rising; level set at Gate 1"],
    ["T2-03", "May to September share of international seats", "ACSA; OAG", "Quarterly", "Air Access", "Rising"],
    ["T2-04", "Share of operators bookable online", "Bookability census", "Every two years", "Research", "Baseline in 2027; rising"],
    ["T2-05", "CapeNature reservations made online", "CapeNature", "Annual", "Research", "Rising"],
    ["T2-06", "India and China arrivals via hubs", "GDS bookings; growth model", "Annual", "Air Access", "India 165,260; China and Hong Kong 92,598 (2035, base, model)"],
    ["T2-07", "Spend per visitor, mature markets", "SA Tourism", "Annual", "Research", "Rising in real terms"],
    ["T2-08", "African arrivals and spend", "SA Tourism", "Annual", "Research", "Regional group 402,812 (2035, base)"],
    ["T2-09", "International seats and routes", "ACSA; OAG", "Quarterly", "Air Access", "From the capacity-against-demand model (I6)"],
    ["T2-10", "Routes above 80% load", "GDS bookings", "Annual", "Air Access", "Seats added on each full route"],
    ["T2-11", "Cruise calls and passengers", "Cruise Cape Town", "Each season", "Cruise Cape Town", "Held open until the 250-call plan is sourced"],
    ["T2-12", "Accessibility score by district", "Readiness re-score", "2029 and 2032", "Research", "Rising outside the Metro"],
    ["T2-13", "Corridor transfer products on sale", "I8 records", "Annual", "Tourism", "One per corridor by 2031 (proposed)"],
    ["T2-14", "Overall readiness by district", "Readiness re-score", "2029 and 2032", "Research", "Rising at each re-score"],
    ["T2-15", "Touring routes rated Ready", "Readiness re-score", "2029 and 2032", "Research", "Three of six by 2031; none below Developing (proposed)"],
    ["T2-16", "Peak queue at the Cableway", "Operator", "Annual", "Research", "Falling"],
    ["T2-17", "Communities with a live booking route", "Pilot records", "Quarterly", "Tourism", "Two or three pilots by 2028 (SCIP p32)"],
    ["T2-18", "LTOs with a funding agreement", "LTO survey", "Annual", "DEDAT", "Baseline in 2027; rising"],
    ["T2-19", "Weather losses at flagship sites", "Site operators", "Annual", "Research", "Tracked; no target"],
    ["T2-20", "Tourism projects at financial close", "I14 records", "Annual", "Wesgro investment promotion", "First projects by 2031"],
    ["T2-21", "Escalation items answered", "Steerco records", "Quarterly", "Wesgro CEO's office", "Each item answered within a year (proposed)"],
    ["T2-22", "Industry partners in the joint plan", "Steerco records", "Annual", "Wesgro CEO's office", "Plan agreed in 2027; partners rising"],
    ["T2-23", "Automated feeds in the dashboard", "Programme office", "Quarterly", "Research", "Arrivals, seats and cruise automated by 2028"],
    ["T2-24", "Visa processing time, priority markets", "Home Affairs; SA Tourism", "Annual", "Wesgro CEO's office", "Falling"],
    ["T2-25", "Tourism labour analysis published", "Research", "Once", "DEDAT, with Wesgro Research", "Published by the end of 2028"],
]
b_a8 = [
    {"type": "pagebreak"},
    {"type": "h2", "text": "A8 M&E toolkit"},
    {"type": "lead", "text": "The toolkit register adds the source, frequency, owner and target to each Tier 2 indicator in section 5.2."},
    {"type": "p", "text": "Targets come from the growth model where it prints them and from the Inclusion Plan where it sets a pilot count. Elsewhere the target is a direction or a milestone, marked proposed where it is this report's choice; Steerco fixes the levels at Gate 1 once the 2027 baselines exist. Tier 1 targets are in section 5.3 and Tier 3 outputs in the charters."},
    {"type": "table", "caption": "Each Tier 2 indicator has a source, a frequency, an owner and a target or direction for 2035.",
     "source": "Indicator register, section 5.2; Market Assessment Report, May 2026, p20 to p23 (model values, working analysis); SME and Community Inclusion Plan, Sep 2026, p32. T2-01 is the sum of the four printed market values (computed).",
     "columns": [{"header": "Code", "width": 0.6, "align": "left"}, {"header": "Indicator", "width": 2.0, "align": "left"}, {"header": "Source", "width": 1.3, "align": "left"}, {"header": "Frequency", "width": 0.9, "align": "left"}, {"header": "Owner", "width": 1.1, "align": "left"}, {"header": "Target or direction to 2035", "width": 2.0, "align": "left"}],
     "rows": T2, "boldFirstCol": True},
    {"type": "h3", "text": "Scorecard and dashboard templates"},
    {"type": "p", "text": "The quarterly scorecard carries one row per indicator: code, name, baseline and year, latest value and date, direction against the path, target, source and owner. The annual Board outlook adds the Tier 1 chart against both paths and the gate status. The dashboard data model lists each feed, its refresh frequency and the manual-entry form for indicators without a feed. The templates themselves are delivered with the Excel toolkit [M&E toolkit workbook: Letsema to deliver with the final report]."},
]
write("08_a8_toolkit.json", "A8", "M&E toolkit", b_a8)

# ---------------------------------------------------------------- A9 glossary and references
GLOSS = [
    ["Accelerated case", "The growth model's upside path: direct India and China routes secured with dedicated activation; 2,516,282 arrivals in 2035"],
    ["Base case", "The growth model's most likely path: Wesgro's current activity continues and hub carriers add capacity; 2,175,778 arrivals in 2035"],
    ["Cold zone", "The Infrastructure Report's term for an area with tourism assets but little or no tourism use"],
    ["Disposition", "What the evidence did to a December hypothesis: Validated, Refined, Reworded, New, Moved, Flagged or Withdrawn (section 1.5)"],
    ["Focus area", "One of the twenty entries on the October 2026 hypothesis tree, each with a Chapter 3 entry, an initiative and indicators"],
    ["Green season", "April to September, the months of lower overseas demand"],
    ["International arrivals", "On the growth model's basis, tourist arrivals; distinct from international passenger arrivals at Cape Town International, which ACSA reports"],
    ["Readiness", "The Infrastructure Report's score for how ready a district's assets are to receive visitors, beside attractiveness and accessibility"],
    ["Seat ceiling", "The 1.8 million inbound seats that current air access provides, as drawn in the Demand-Side Analysis"],
    ["Seller with a stake", "The Inclusion Plan's term for a local body that sells community product and keeps the revenue in the community"],
    ["Tier 1, 2 and 3", "Impact, outcome and output indicators (section 5.2)"],
]
REFS = [
    ["Inception Report", "Study team", "Nov 2025 (27 November 2025)", "Deliverable"],
    ["Current State Diagnostic, version 2", "Study team", "Dec 2025", "Deliverable"],
    ["Skift Digital and Search Insights memo", "Skift Advisory", "10 Dec 2025", "Working analysis"],
    ["Stakeholder Insights Report, phase 1", "Study team", "Mar 2026 (12 March 2026)", "Deliverable"],
    ["Skift Segmentation Analysis, version 2.0", "Skift Advisory", "Mar 2026 (12 March 2026)", "Working analysis"],
    ["Skift African Market Analysis, version 1", "Skift Advisory", "16 Mar 2026", "Working analysis"],
    ["Global Benchmarking Report", "Study team", "Mar 2026 (24 March 2026)", "Deliverable"],
    ["MIDAS Aviation Market Assessment, final draft", "MIDAS", "Mar 2026 (file 20 April 2026)", "Deliverable"],
    ["Market Assessment Report", "Study team", "May 2026", "Working analysis"],
    ["Demand-Side Analysis, final", "Study team", "Jun 2026 (file 1 October 2026)", "Deliverable"],
    ["Infrastructure Report, final", "Study team", "Jul 2026 (file 22 September 2026)", "Deliverable"],
    ["SME and Community Inclusion Plan", "Study team", "Sep 2026 (file 9 October 2026)", "Deliverable"],
    ["Unlocking Tourism Summary of Findings, working session", "Study team", "14 Oct 2026 (not in this evidence base)", "Deck"],
    ["Economic Value of Tourism in Cape Town for the 2024 year", "City of Cape Town (Futureneer Advisors)", "June 2025", "Public source"],
    ["Tourism Satellite Account release, as reported", "Statistics South Africa", "2026, provisional", "Public source"],
    ["Air access releases: jobs and spend per 100 international passengers", "Wesgro and Cape Town Air Access", "2023 to 2024", "Public source"],
    ["Presentation to the parliamentary committee", "Wesgro", "1 April 2026", "Public source"],
    ["Western Cape tourism is booming, but can locals afford to enjoy it?", "Hypertext", "April 2026", "Public source"],
    ["Service Level Agreement, Annexure B", "Wesgro and Letsema", "December 2025 (not in this evidence base)", "Contract"],
]
b_a9 = [
    {"type": "pagebreak"},
    {"type": "h2", "text": "A9 Glossary and references"},
    {"type": "lead", "text": "Eleven terms carry a specific meaning in this report, and nineteen documents support it, cited by the date on their covers."},
    {"type": "p", "text": "Abbreviations are listed in the front matter. Deliverables are cited with the date printed on the cover; where the file date differs, both are shown below. Working analyses rank below the deliverables, and public sources are used only where no deliverable carries the figure."},
    {"type": "table", "caption": "Eleven terms have a fixed meaning in this report.", "source": "Letsema, from Chapters 1 to 5.",
     "columns": [{"header": "Term", "width": 1.6, "align": "left"}, {"header": "Meaning in this report", "width": 6.2, "align": "left"}], "rows": GLOSS, "boldFirstCol": True},
    {"type": "table", "caption": "Twelve study documents, six public and reference sources and one deck not yet in hand support the report.", "source": "Letsema, document register. Study team: Letsema in partnership with Skift Advisory.",
     "columns": [{"header": "Document", "width": 3.2, "align": "left"}, {"header": "Author", "width": 1.8, "align": "left"}, {"header": "Date cited", "width": 1.8, "align": "left"}, {"header": "Status", "width": 1.0, "align": "left"}], "rows": REFS, "boldFirstCol": True},
]
write("09_a9_glossary.json", "A9", "Glossary and references", b_a9)
print("A1, A7, A8, A9 written;", len(rows7), "actions")
