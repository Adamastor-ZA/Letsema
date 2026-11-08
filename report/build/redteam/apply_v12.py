"""Draft v12 content edits (Michael, 8 November 2026): the three Western Cape factbases used to enrich the report.

Michael's rule: "No need to reference these docs, just use." Factbase facts enter the report directly, cited to the original
document the factbase names (never to the factbase), under the treatments in redteam/v12/decisions.md. Scope is option (b) of
report/factbase_assessment.md: close open items, fix conflicts, targeted enrichment of the summary and Chapters 1 to 5 and
the appendices.

Edits sit in redteam/v12/edits/<stream>.json as {"edits": [...]}, each naming a v11 block by module and index:
  replace (blocks; refs to v11 blocks allowed), delete, insert_after (blocks), replace_text (find, repl), set (fields),
  add_rows (rows appended to a table or grid), drop_rows (first_cells), drop_columns (columns).
Each edit carries a "reason". Usage: python3 apply_v12.py [--dry-run]. Run once on the v11 content; writes applied_v12.json.
"""
import copy, glob, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
C = os.path.join(HERE, '..', 'content')
DRY = '--dry-run' in sys.argv
sys.path.insert(0, HERE)
from check_v9_draft import VERSIONING, block_text, strip_cites  # noqa: E402

BASE = {os.path.relpath(f, C): json.load(open(f)) for f in sorted(glob.glob(os.path.join(C, '*', '*.json')))}
assert 'one per paragraph' in json.dumps(BASE['ch1/05_how_to_read.json']), 'content/ must hold draft v11'
assert not any('Strategic Plan 2025/26' in json.dumps(d) for d in BASE.values()), 'v12 already applied'
OUT = copy.deepcopy(BASE)
LOG = []


def resolve(blocks):
    return [copy.deepcopy(BASE[b['src'][0]]['blocks'][b['src'][1]]) if b.get('type') == 'ref' else b for b in blocks]


def strings_replace(x, find, repl):
    if isinstance(x, str): return x.replace(find, repl)
    if isinstance(x, list): return [strings_replace(y, find, repl) for y in x]
    if isinstance(x, dict): return {k: (strings_replace(v, find, repl) if k not in ('svg',) else v) for k, v in x.items()}
    return x


edits = []
for p in sorted(glob.glob(os.path.join(HERE, 'v12', 'edits', '*.json'))):
    for e in json.load(open(p))['edits']:
        e['_stream'] = os.path.basename(p)[:-5]; edits.append(e)
by_mod = {}
for e in edits:
    assert e.get('reason') and e['module'] in BASE and 0 <= e['index'] < len(BASE[e['module']]['blocks']), (e.get('module'), e.get('index'))
    by_mod.setdefault(e['module'], []).append(e)
for mod, es in by_mod.items():
    owners = {e['_stream'] for e in es}
    assert len(owners) == 1, f'{mod} is edited by more than one stream: {owners}'
    bl = OUT[mod]['blocks']
    for e in [x for x in es if x['op'] in ('replace_text', 'set', 'add_rows', 'drop_rows', 'drop_columns')]:
        b = bl[e['index']]
        if e['op'] == 'replace_text':
            n = json.dumps(b, ensure_ascii=False).count(json.dumps(e['find'], ensure_ascii=False)[1:-1])
            assert n >= 1, (mod, e['index'], e['find'][:80])
            bl[e['index']] = strings_replace(b, e['find'], e['repl'])
        elif e['op'] == 'set':
            b.update(e['fields'])
        elif e['op'] == 'add_rows':
            assert all(len(r) == len(b['columns']) for r in e['rows']), (mod, e['index'], 'row width')
            b['rows'].extend(e['rows'])
        elif e['op'] == 'drop_rows':
            before = len(b['rows']); b['rows'] = [r for r in b['rows'] if r[0] not in e['first_cells']]
            assert before - len(b['rows']) == len(e['first_cells']), (mod, e['index'], e['first_cells'])
        elif e['op'] == 'drop_columns':
            keep = [i for i, c in enumerate(b['columns']) if c['header'] not in e['columns']]
            b['columns'] = [b['columns'][i] for i in keep]; b['rows'] = [[r[i] for i in keep] for r in b['rows']]
        LOG.append({'stream': e['_stream'], 'kind': e['op'], 'file': mod, 'index': e['index'], 'reason': e['reason'],
                    'detail': {k: v for k, v in e.items() if k not in ('module', 'index', 'op', 'reason', '_stream')}})
    structural = [x for x in es if x['op'] in ('replace', 'delete', 'insert_after')]
    idx = [x['index'] for x in structural]
    assert len(idx) == len(set(idx)), f'{mod}: two structural edits on one block'
    for e in sorted(structural, key=lambda x: -x['index']):
        i = e['index']; old = bl[i]
        if e['op'] == 'insert_after': bl[i + 1:i + 1] = resolve(e['blocks'])
        elif e['op'] == 'replace': bl[i:i + 1] = resolve(e['blocks'])
        else: bl[i:i + 1] = []
        LOG.append({'stream': e['_stream'], 'kind': e['op'], 'file': mod, 'index': i, 'reason': e['reason'], 'before': block_text(old)[:3000],
                    'after': ' '.join(block_text(x) for x in resolve(e.get('blocks', [])))[:6000]})


# Table and figure numbers cited in the text follow their captions to the new numbering.
def numbering(mods):
    out = {'table': {}, 'figure': {}}
    for dname, lab in [('exec', 'ES'), ('ch1', '1'), ('ch2', '2'), ('ch3', '3'), ('ch4', '4'), ('ch5', '5'), ('appendices', 'A')]:
        n = {'table': 0, 'figure': 0}
        for f in sorted(k for k in mods if k.startswith(dname + '/')):
            for b in mods[f]['blocks']:
                if b['type'] in n:
                    n[b['type']] += 1; out[b['type']][f'{lab}.{n[b["type"]]}'] = b['caption']
    return out


N0, N1 = numbering(BASE), numbering(OUT)
INV = {k: {c: num for num, c in v.items()} for k, v in N1.items()}
XREF = re.compile(r'\b(Tables?|Figures?) ((?:ES|A|\d)\.\d+(?:(?:, | and | to )(?:ES|A|\d)\.\d+)*)')


def renum(f, s):
    def one(m):
        kind = 'table' if m.group(1).startswith('Table') else 'figure'
        return m.group(1) + ' ' + re.sub(r'(?:ES|A|\d)\.\d+', lambda t: INV[kind][N0[kind][t.group(0)]], m.group(2))
    t = XREF.sub(one, s)
    if t != s: LOG.append({'kind': 'renumbered reference', 'file': f, 'before': s, 'after': t})
    return t


def walk(f, x):
    if isinstance(x, str): return renum(f, x)
    if isinstance(x, list): return [walk(f, y) for y in x]
    if isinstance(x, dict): return {k: (walk(f, v) if k not in ('chart', 'svg', 'id') else v) for k, v in x.items()}
    return x


for f in OUT: OUT[f]['blocks'] = walk(f, OUT[f]['blocks'])

# ------------------------------------------------------------------------------------------------ Checks and write
WORK = re.compile(r"\b(?:this|the|our|a|its) (?:tourism )?strateg(?:y|y's)\b(?! (?:statements?|that will double))|\bstrategy's\b|\bfor the strategy\b", re.I)
KEEP = re.compile(r"Growth for Jobs Strategy|G4J|Wesgro's (?:own |five-year )?strateg|investment strategies|Strategic growth|evidence-based tourism strategy|Hub Strategy|Brand Strategy|gateway strategy|calendar strategy|route strategy|marketing strategy|one strategy|coordinated strategy|joint strategy|Tourism Transport Strategy|aviation strategy|national strategy|tourism board's strategy|City's strategy|province's strategy")
left = []
for f, d in OUT.items():
    for i, b in enumerate(d['blocks']):
        if b['type'] == 'figure': continue
        t = strip_cites(block_text(b))
        for m in VERSIONING.finditer(t): left.append((f, i, 'earlier tree', m.group(0)))
        for m in WORK.finditer(t):
            if not KEEP.search(t[max(0, m.start() - 80):m.end() + 60]): left.append((f, i, 'work as strategy', t[max(0, m.start() - 60):m.end() + 40]))
        if re.search(r'factbase', block_text(b), re.I): left.append((f, i, 'factbase named', ''))
print(f'{len(edits)} edits from {len({e["_stream"] for e in edits})} streams, {len(LOG)} log entries; problems: {len(left)}')
for x in left: print('  LEFT:', x)
if DRY:
    print('dry run: nothing written'); sys.exit(0)
assert not left, 'problems remain'
for f, d in OUT.items():
    with open(os.path.join(C, f), 'w') as fh:
        json.dump(d, fh, indent=1, ensure_ascii=False); fh.write('\n')
json.dump(LOG, open(os.path.join(HERE, 'applied_v12.json'), 'w'), indent=1, ensure_ascii=False)
print('written')
