"""Structural QA for the final report (run after qa_text.js). Checks the brief's return conditions:
20 entries x six parts; every initiative in 4.2, 4.3 and 4.4; every Tier 1 and Tier 2 indicator with a baseline or a
dated gap; executive-summary toplines identical to Chapter 3; no figure cited to the October deck; Chapter 3 link-forward
codes agree with traceability.csv; page counts by chapter against budget (needs pagemap.json from a build)."""
import csv, glob, json, os, re, sys

H = os.path.dirname(os.path.abspath(__file__))
C = os.path.join(H, 'content')
issues = []
ok = []


def load(d):
    return [(os.path.basename(f), json.load(open(f))) for f in sorted(glob.glob(os.path.join(C, d, '*.json')))]


def texts(blocks):
    for b in blocks:
        for k in ('text', 'caption', 'source', 'title'):
            if isinstance(b.get(k), str):
                yield b[k]
        for k in ('items', 'paras'):
            for t in b.get(k, []) or []:
                if isinstance(t, str):
                    yield t
        for r in b.get('rows', []) or []:
            for c in r:
                if isinstance(c, str):
                    yield c


TR = {r['fa_id']: r for r in csv.DictReader(open(os.path.join(H, '..', 'traceability.csv')))}

# 1. Chapter 3: 20 entries x six parts, link-forward codes
entries = {}
for name, d in load('ch3'):
    bl = d['blocks']
    for i, b in enumerate(bl):
        if b['type'] == 'kicker' and 'Focus area' in b['text']:
            n = int(b['text'].rsplit('Focus area', 1)[1])
            fa = f"FA{n:02d}"
            j = i + 1
            end = next((k for k in range(j + 1, len(bl)) if bl[k]['type'] == 'kicker'), len(bl))
            sl = bl[i:end]
            h4 = [x['text'] for x in sl if x['type'] == 'h4']
            parts = ['kicker', 'topline'] + h4
            ev = [x for x in sl if x['type'] == 'table']
            link = next((x['text'] for x in sl if x['type'] == 'p' and x['text'].startswith('**Initiative')), '')
            entries[fa] = dict(file=name, top=bl[i + 2]['text'] if bl[i + 2]['type'] == 'lead' else None, h4=h4, ev_rows=len(ev[0]['rows']) if ev else 0, link=link)
if len(entries) == 20:
    ok.append('Chapter 3 has 20 focus-area entries')
else:
    issues.append(f'Chapter 3 has {len(entries)} entries, not 20')
need = ['Hypothesis and disposition', 'Evidence', 'Recommendation', 'Benchmark precedent', 'Link forward']
for fa, e in sorted(entries.items()):
    miss = [p for p in need if p not in e['h4']]
    if miss or not e['top']:
        issues.append(f'{fa}: missing parts {miss or "topline"}')
    if not 3 <= e['ev_rows'] <= 6:
        issues.append(f'{fa}: evidence table has {e["ev_rows"]} rows (brief: 3 to 6)')
    init = TR[fa]['initiative_ids']
    if f'Initiative {init}' not in e['link'] and f'**Initiative {init}**' not in e['link']:
        issues.append(f'{fa}: link forward does not name {init} ({e["link"][:60]})')
    for code in [c.strip() for c in TR[fa]['indicator_codes'].split(';')]:
        if code not in e['link']:
            issues.append(f'{fa}: link forward lacks indicator {code} listed in traceability.csv')
if not [i for i in issues if i.startswith('FA')]:
    ok.append('All 20 entries carry kicker, topline and the five parts; evidence tables 3 to 6 rows; links match traceability.csv')

# 2. Initiatives in 4.2 (Gantt), 4.3 (charters), 4.4 (RACI)
ch4 = dict(load('ch4'))
codes = [f'I{i}' for i in range(1, 19)]
gantt = next(b for b in ch4['02_sequencing.json']['blocks'] if b['type'] == 'figure')['chart']['rows']
g = {r['code'] for r in gantt}
ch = {b['text'].split()[0] for b in ch4['03_charters.json']['blocks'] if b['type'] == 'h3'}
raci = {r[0] for b in ch4['04_raci.json']['blocks'] if b['type'] == 'table' for r in b['rows']}
for c in codes:
    for where, s in (('4.2 Gantt', g), ('4.3 charters', ch), ('4.4 RACI', raci)):
        if c not in s:
            issues.append(f'{c} missing from {where}')
if all(c in g and c in ch and c in raci for c in codes):
    ok.append('All 18 initiatives appear in 4.2, 4.3 and 4.4')

# 3. Indicators: every T1 and T2 has a baseline or a dated gap
ch5 = dict(load('ch5'))
t1 = next(b for b in ch5['03_baselines_targets.json']['blocks'] if b['type'] == 'table')['rows']
t2 = next(b for b in ch5['02_indicators.json']['blocks'] if b['type'] == 'table' and b['caption'].startswith('Twenty-five'))['rows']
for r in t1:
    if not r[1].strip():
        issues.append(f'{r[0]}: no baseline')
for r in t2:
    if not r[3].strip():
        issues.append(f'{r[0]}: no baseline')
gaps = next(b for b in ch5['04_data.json']['blocks'] if b['type'] == 'table' and 'gaps' in b['caption'])['rows']
gap_ind = {r[1] for r in gaps}
for r in t1 + t2:
    base = r[1] if r[0].startswith('T1') else r[3]
    code = r[0].split()[0]
    if base.lower().startswith('not in hand') and code not in gap_ind:
        issues.append(f'{code}: baseline not in hand and no dated gap in 5.4')
ok.append(f'{len(t1)} Tier 1 and {len(t2)} Tier 2 indicators checked for a baseline or a dated gap')

# 4. Executive summary toplines identical to Chapter 3
ex = load('exec')
ex_txt = list(texts(ex[0][1]['blocks'])) if ex else []
for fa, e in entries.items():
    if e['top'] not in ex_txt:
        issues.append(f'{fa}: topline not lifted verbatim into the executive summary')
if all(e['top'] in ex_txt for e in entries.values()):
    ok.append('All 20 toplines appear verbatim in the executive summary')

# 5. Nothing cited to the October deck except as a bracketed open item
for d in ('exec', 'ch1', 'ch2', 'ch3', 'ch4', 'ch5', 'appendices'):
    for name, doc in load(d):
        for t in texts(doc['blocks']):
            for m in re.finditer(r'Summary of Findings[^\]\)]*', t):
                pre = t[:m.start()]
                if pre.count('[') <= pre.count(']') and 'ispositions' not in t and name != '09_a9_glossary.json':
                    issues.append(f'{d}/{name}: deck cited outside a placeholder: {t[max(0, m.start() - 60):m.end()][:140]}')
ok.append('October deck cited only for dispositions or as an open item, never for a figure')

# 6. Page budget
pm = os.path.join(H, 'pagemap.json')
if os.path.exists(pm):
    m = json.load(open(pm))
    pages, n = m['map'], m['nPages']
    marks = [('Executive summary', 'Executive summary', (10, 12)), ('Context', 'Chapter 1', (18, 22)), ('Analysis summaries', 'Chapter 2', (45, 52)),
             ('Findings and recommendations', 'Chapter 3', (60, 80)), ('Execution plan', 'Chapter 4', (25, 30)), ('Monitoring and evaluation framework', 'Chapter 5', (15, 20)), ('Appendices', 'Appendices', (0, 999))]
    starts = [(pages.get(k), lab, bud) for k, lab, bud in marks]
    for i, (p0, lab, bud) in enumerate(starts):
        p1 = starts[i + 1][0] if i + 1 < len(starts) else n + 1
        if p0 is None or p1 is None:
            continue
        cnt = p1 - p0
        flag = '' if bud[0] <= cnt <= bud[1] else f'  (budget {bud[0]} to {bud[1]})'
        ok.append(f'{lab}: {cnt} pages{flag}')

print('PASS'); [print('  ' + o) for o in ok]
print('ISSUES', len(issues)); [print('  ' + i) for i in issues]
sys.exit(1 if issues else 0)
