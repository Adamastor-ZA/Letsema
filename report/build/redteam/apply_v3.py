"""Draft v3 content edits (Michael, 7 November 2026): short figure titles of three to six words, and a key-message
callout drawn inside each data chart where the chart needs one. The long v2 caption is kept in the log as the
message the callout condenses. Footnoting of citations is done at render time (helpers.js), not here, apart from the
one sentence in section 1.5 that describes the citation form.

Run once on the v2 content. Writes redteam/applied_v3.json.
"""
import json, glob, os

HERE = os.path.dirname(os.path.abspath(__file__))
C = os.path.join(HERE, '..', 'content')
FILES = {os.path.relpath(f, C): json.load(open(f)) for f in sorted(glob.glob(os.path.join(C, '*', '*.json')))}
LOG = []

# id: (title, callout or None). Callout coordinates are in the chart's own 1600-wide space; "band" adds a strip above.
FIG = {
    'fig_0_tree': ('The updated hypothesis tree', None),
    'fig_0_paths': ('Arrivals paths to 2035', {'text': 'Only the accelerated path clears 2.5m by 2035; the base path crosses the seat line before 2031.', 'x': 180, 'y': 80, 'w': 700}),
    'fig_ctia_arrivals_fy': ('Airport arrivals, FY15/16 to FY25/26', {'text': 'Arrivals passed the pre-pandemic peak in FY23/24 and reached 1.57m in FY25/26.', 'x': 180, 'y': 80, 'w': 640}),
    'fig_source_markets_2025': ('Overseas arrivals by market, 2025', {'text': 'Five markets supply 63% of overseas arrivals; the UK, Germany and the USA alone supply 52%.', 'x': 620, 'y': 450, 'w': 760}),
    'fig_spend_per_visitor_2024': ('Spend per visitor by market, 2024', {'text': "The USA spends R32,900 a visit, 3.9 times Zimbabwe's R8,500.", 'x': 640, 'y': 700, 'w': 760}),
    'fig_base_case_seat_ceiling': ('Base case against the seat line', {'text': "The base case crosses the model's 1.8m seat line in 2030, before runway relief in about 2033.", 'x': 180, 'y': 80, 'w': 700}),
    'fig_21_scenarios': ('Growth scenarios to 2035', {'text': 'The base case crosses the seat line in 2030; only the accelerated case reaches 2.5m by 2035.', 'x': 180, 'y': 80, 'w': 700}),
    'fig_21_groups': ('Base-case growth by market group', {'text': 'Hub and acceleration markets supply 382,402 of the 676,949 arrivals the base case adds.', 'x': 180, 'y': 110, 'w': 520}),
    'fig_22_loads': ('Route load factors to November 2025', {'text': 'Eleven of 27 routes ran above 80% load in the year to November 2025, and sixteen at 75% or more.', 'band': True}),
    'fig_22_months': ('International seats by month, 2025', {'text': "December carries 10.8% of the year's international seats; June carries 6.4%.", 'x': 180, 'y': 90, 'w': 700}),
    'fig_23_growth': ('Comparator growth, 2023 to 2024', {'text': "Chile and Singapore grew two to four times the world's 11%; Kenya, Valencia and New Zealand slightly faster.", 'x': 930, 'y': 330, 'w': 600}),
    'fig_24_tally': ('Themes raised by stakeholder organisations', {'text': 'Industry-government collaboration and data sharing each drew 15 of the 16 organisations.', 'x': 1100, 'y': 360, 'w': 460}),
    'fig_25_readiness': ('Readiness and accessibility by district', {'text': 'Both scores fall with each step away from the Cape Metro.', 'x': 960, 'y': 100, 'w': 580}),
    'fig_26_constraints': ('Binding constraints in 20 communities', {'text': 'Organisation binds in 11 of the 20 communities; distance binds in none.', 'x': 640, 'y': 690, 'w': 760}),
    'fig_3_fa02_months': ('Meetings, seats and visitors by month', {'text': 'Meetings peak from September to November, while seats and visitors climb out of the winter trough.', 'x': 180, 'y': 80, 'w': 640}),
    'fig_4_gantt': ('Initiative timeline, 2027 to 2035', {'text': 'Three initiatives start in implementation in 2027, eleven by 2028 and all eighteen by 2029.', 'band': True}),
    'fig_4_funding': ('Initiatives by main funding source', {'text': "Wesgro's operating budget is the main source for 13 initiatives, and private capital for the four capital-heavy ones.", 'x': 880, 'y': 500, 'w': 640}),
    'fig_4_governance': ('Delivery governance structure', None),
    'fig_5_chain': ('Results chain for the plan', None),
    'fig_5_paths': ('Arrivals paths and milestones to 2035', {'text': 'Only the accelerated path clears 2.5m by 2035; the base path crosses the seat line before 2031.', 'x': 180, 'y': 80, 'w': 700}),
    'fig_5_dashboard': ('Quarterly scorecard layout', None),
}

seen = set()
for f, d in FILES.items():
    for i, b in enumerate(d['blocks']):
        if b.get('type') != 'figure': continue
        fid = b['id']
        assert fid in FIG, fid
        title, call = FIG[fid]
        assert 3 <= len(title.split()) <= 6, title
        before = b['caption']
        b['caption'] = title
        if call:
            assert 'chart' in b, fid
            b['chart']['callout'] = call
        LOG.append({'id': fid, 'file': f, 'block': i, 'before': before, 'title': title, 'callout': call['text'] if call else None})
        seen.add(fid)
assert seen == set(FIG), set(FIG) - seen

# Section 1.5 describes the citation form; it now sits in footnotes.
f = 'ch1/05_how_to_read.json'
old = 'Every figure carries its source and page in the form (Demand-Side Analysis, Jun 2026, p21).'
new = 'Every figure carries its source and page in a footnote, in the form Demand-Side Analysis, Jun 2026, p21.'
hits = [b for b in FILES[f]['blocks'] if old in b.get('text', '')]
assert len(hits) == 1
hits[0]['text'] = hits[0]['text'].replace(old, new)
LOG.append({'id': 'citations', 'file': f, 'before': old, 'after': new})

for f, d in FILES.items():
    with open(os.path.join(C, f), 'w') as fh:
        json.dump(d, fh, indent=1, ensure_ascii=False); fh.write('\n')
json.dump(LOG, open(os.path.join(HERE, 'applied_v3.json'), 'w'), indent=1, ensure_ascii=False)
print(len(LOG), 'edits')
