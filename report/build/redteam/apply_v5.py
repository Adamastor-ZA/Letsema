"""Draft v5 content edits (Michael, 7 November 2026): table titles of three to six words.

Each table's v4 caption was a one-sentence message. The new title names the table; where the old sentence states a
finding, it moves word for word into a key-message callout above the table (the `message` field, rendered by
helpers.table). Descriptive tables (finding lists, registers, glossary, sources) take the title alone. The three
executive-summary pillar tables lose only their "Pillar N, name:" prefix in the callout, which the title now carries.

Run once on the v4 content. Writes redteam/applied_v5.json.
"""
import json, glob, os

HERE = os.path.dirname(os.path.abspath(__file__))
C = os.path.join(HERE, '..', 'content')
ORDER = [('exec', 'ES'), ('ch1', '1'), ('ch2', '2'), ('ch3', '3'), ('ch4', '4'), ('ch5', '5'), ('appendices', 'A')]
K, N = 'keep', None  # keep the old caption as the callout; no callout

T = {
    'ES.1': ('How the tree changed', K), 'ES.2': ('Pillar 1: Reshape demand', 'strip'), 'ES.3': ('Pillar 2: Transform supply', 'strip'),
    'ES.4': ('Pillar 3: Build enabling capability', 'strip'), 'ES.5': ('Actions for the first 24 months', K), 'ES.6': ('Impact indicators and targets', K),
    'ES.7': ('The main risks', K),
    '1.1': ('The four headline ambitions', K), '1.2': ('Arrivals figures in circulation', K), '1.3': ('Month of travel, 2024 and 2025', K),
    '1.4': ('District economy, assets and access', K), '1.5': ('The tourism system by tier', K), '1.6': ('December entries and October changes', K),
    '1.7': ('Interim deliverables and SLA clauses', N), '1.8': ('Chapter map and readers', N), '1.9': ('Disposition labels and counts', K),
    '2.1': ('Four traveller segments', K), '2.2': ('Demand findings for the tree', N), '2.3': ('Carrier launches since 2014', K),
    '2.4': ('Aviation findings for the tree', N), '2.5': ('Comparator growth and recovery', K), '2.6': ('Comparator lessons for the province', N),
    '2.7': ('Benchmark findings for the tree', N), '2.8': ('Stakeholder priority areas', N), '2.9': ('Attributed high-rated insights', K),
    '2.10': ('Stakeholder findings for the tree', N), '2.11': ('District strengths and weaknesses', K), '2.12': ('Touring route readiness', K),
    '2.13': ('Cruise ports and stance', K), '2.14': ('Remaining gaps by region', K), '2.15': ('Spatial findings for the tree', N),
    '2.16': ('Inclusion benchmark cases', K), '2.17': ('Community archetypes and responses', K), '2.18': ('The 20 shortlisted communities', K),
    '2.19': ('Inclusion findings for the tree', N),
    '3.1': ('Pillar 1 focus areas', K), '3.8': ('Pillar 2 focus areas', K), '3.15': ('Pillar 3 focus areas', K),
    '3.24': ('Growth paths and their interventions', K), '3.25': ('What moves in each phase', K),
    '4.1': ('Levels of the plan', K), '4.2': ('The eighteen initiatives', K), '4.3': ('Accountability by initiative and tier', K),
    '4.4': ('First-24-month actions and funding', K), '4.5': ('Funding routes by initiative', K), '4.6': ('Decision gates and reviews', K),
    '4.7': ('Risks and their mitigation', K),
    '5.1': ('Pillar 1 results chain', K), '5.2': ('Pillar 2 results chain', K), '5.3': ('Pillar 3 results chain', K),
    '5.4': ('Tier 1 impact indicators', N), '5.5': ('Tier 2 outcome indicators', K), '5.6': ('Tier 3 output indicators', N),
    '5.7': ('Tier 1 baselines and targets', K), '5.8': ('Data sources and holders', N), '5.9': ('Data gaps and owners', K),
    '5.10': ('Reporting calendar and cycles', N), '5.11': ('Evaluation questions by pillar', N), '5.12': ('The M&E toolkit files', N),
    'A.1': ('Reasons against the evidence', K), 'A.2': ('Traceability by focus area', N), 'A.3': ('Growth model scenario definitions', K),
    'A.4': ('Model end points by base year', K), 'A.5': ('Base case by market group', K), 'A.6': ('Acceleration and mature market paths', K),
    'A.7': ('Regional market paths', K), 'A.8': ('Base-case spend by group', K), 'A.9': ('Model printouts and limits', K),
    'A.10': ('Benchmark selection criteria', N), 'A.11': ('Comparator set, inception to final', K), 'A.12': ('Comparator growth, recovery and levers', K),
    'A.13': ('Comparator system types', K), 'A.14': ('Transferable levers by case', K), 'A.15': ('Asset database structure', N),
    'A.16': ('Readiness index weights', K), 'A.17': ('Dimension scores by district', K), 'A.18': ('Overall readiness by district', K),
    'A.19': ('Touring route scorecards', K), 'A.20': ('Asset counts by district', K), 'A.21': ('Community shortlist criteria', K),
    'A.22': ('Archetypes, responses and benchmarks', K), 'A.23': ('Shortlist readiness ratings', K), 'A.24': ('Community share of spend', K),
    'A.25': ('Inclusion cases and lessons', K), 'A.26': ('Insights by organisation', K), 'A.27': ('Later-phase engagement list', K),
    'A.28': ('Insights by tree element', K), 'A.29': ('Lines of enquiry by area', N), 'A.30': ('Chapter 3 action register', N),
    'A.31': ('Tier 2 indicator register', N), 'A.32': ('Glossary of terms', N), 'A.33': ('Documents and sources cited', N),
}

LOG, seen = [], set()
for d, lab in ORDER:
    n = 0
    for f in sorted(glob.glob(os.path.join(C, d, '*.json'))):
        data = json.load(open(f)); rel = os.path.relpath(f, C); changed = False
        for i, b in enumerate(data['blocks']):
            if b['type'] != 'table': continue
            n += 1; num = f'{lab}.{n}'
            old = b['caption']
            if num in T:
                title, msg = T[num]
            else:  # Chapter 3 evidence tables, one per focus area
                fa = int(os.path.basename(f)[5:7]) if os.path.basename(f)[3:5] == 'fa' else None
                assert lab == '3' and fa, (num, rel)
                title, msg = f'Evidence for focus area {fa}', K
            assert 3 <= len(title.split()) <= 6, (num, title)
            if msg == K: msg = old
            elif msg == 'strip':
                rest = old.split(': ', 1)[1]; msg = rest[0].upper() + rest[1:]
            b['caption'] = title
            if msg: b['message'] = msg
            LOG.append({'table': num, 'file': rel, 'block': i, 'before': old, 'title': title, 'message': msg})
            seen.add(num); changed = True
        if changed:
            with open(f, 'w') as fh:
                json.dump(data, fh, indent=1, ensure_ascii=False); fh.write('\n')
assert set(T) <= seen, set(T) - seen
json.dump(LOG, open(os.path.join(HERE, 'applied_v5.json'), 'w'), indent=1, ensure_ascii=False)
print(len(LOG), 'tables;', sum(1 for e in LOG if e['message']), 'with a key-message callout')
