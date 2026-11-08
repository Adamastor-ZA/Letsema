"""Draft v10 content edits (Michael, 8 November 2026).

1. The executive summary loses its section on the decisions asked of the Board.
2. The report no longer calls the work a strategy: it is a research project that develops an action plan. Every reference to
   the work as a strategy is reworded ("this report", "the research", "the action plan"); references to other bodies'
   strategies (Growth for Jobs, Wesgro's strategy statements, the comparators' strategies), the "Strategic growth" market
   group, focus area 15's title and the quoted study objective stay. The subtitle changes in report.js and front_matter.js.

Edits name v9 blocks by module and index, in redteam/v10/edits.json, with the operations apply_v9.py takes for its sweep
(replace, delete, replace_text, drop_columns, drop_rows, set), each with a reason.
Usage: python3 apply_v10.py [--dry-run]. Run once on the v9 content; writes redteam/applied_v10.json.
"""
import copy, glob, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.join(HERE, '..')
C = os.path.join(B, 'content')
DRY = '--dry-run' in sys.argv
sys.path.insert(0, HERE)
from check_v9_draft import block_text, strip_cites  # noqa: E402

V8 = {os.path.relpath(f, C): json.load(open(f)) for f in sorted(glob.glob(os.path.join(C, '*', '*.json')))}  # the v9 content (name kept for the shared code)
assert any(b.get('text') == 'Why it can work' for b in V8['ch3/14_fa04.json']['blocks']), 'content/ must hold draft v9'
OUT = copy.deepcopy(V8)
LOG = []
DRAFTED = set()


def resolve(blocks):
    return [copy.deepcopy(V8[b['src'][0]]['blocks'][b['src'][1]]) if b.get('type') == 'ref' else b for b in blocks]


# ------------------------------------------------------------------------------------------------ Edits
SW = os.path.join(HERE, 'v10', 'edits.json')
sweep = json.load(open(SW))['edits'] if os.path.exists(SW) else []
for e in sweep:
    assert e['module'] not in DRAFTED, f"sweep edits a drafted module: {e['module']}"
    assert e.get('reason'), e


def strings_replace(x, find, repl):
    if isinstance(x, str): return x.replace(find, repl)
    if isinstance(x, list): return [strings_replace(y, find, repl) for y in x]
    if isinstance(x, dict): return {k: (strings_replace(v, find, repl) if k not in ('svg',) else v) for k, v in x.items()}
    return x


by_mod = {}
for e in sweep: by_mod.setdefault(e['module'], []).append(e)
for mod, edits in by_mod.items():
    bl = OUT[mod]['blocks']
    # in-place edits first (indices stay valid), then structural edits from the bottom up
    for e in [x for x in edits if x['op'] in ('replace_text', 'drop_columns', 'drop_rows', 'set')]:
        b = bl[e['index']]
        if e['op'] == 'replace_text':
            n = json.dumps(b, ensure_ascii=False).count(json.dumps(e['find'], ensure_ascii=False)[1:-1])
            assert n >= 1, (mod, e['index'], e['find'][:80])
            bl[e['index']] = strings_replace(b, e['find'], e['repl'])
        elif e['op'] == 'drop_columns':
            hs = [c['header'] for c in b['columns']]
            keep = [i for i, h in enumerate(hs) if h not in e['columns']]
            assert len(keep) == len(hs) - len(e['columns']), (mod, e['index'], hs, e['columns'])
            freed = sum(b['columns'][i]['width'] for i in range(len(hs)) if i not in keep)
            b['columns'] = [b['columns'][i] for i in keep]
            widest = max(range(len(b['columns'])), key=lambda i: b['columns'][i]['width'])
            b['columns'][widest]['width'] = round(b['columns'][widest]['width'] + freed, 2)
            b['rows'] = [[r[i] for i in keep] for r in b['rows']]
        elif e['op'] == 'drop_rows':
            before = len(b['rows'])
            b['rows'] = [r for r in b['rows'] if r[0] not in e['first_cells']]
            assert before - len(b['rows']) == len(e['first_cells']), (mod, e['index'], e['first_cells'])
        elif e['op'] == 'set':
            b.update(e['fields'])
        LOG.append({'kind': 'sweep ' + e['op'], 'file': mod, 'index': e['index'], 'reason': e['reason'],
                    'detail': {k: v for k, v in e.items() if k not in ('module', 'index', 'op', 'reason')}})
    for e in sorted([x for x in edits if x['op'] in ('replace', 'delete')], key=lambda x: -x['index']):
        old = bl[e['index']]
        bl[e['index']:e['index'] + 1] = resolve(e['blocks']) if e['op'] == 'replace' else []
        LOG.append({'kind': 'sweep ' + e['op'], 'file': mod, 'index': e['index'], 'reason': e['reason'], 'before': block_text(old)[:4000],
                    'after': ' '.join(block_text(x) for x in resolve(e.get('blocks', [])))[:4000]})

# ------------------------------------------------------------------------------------------------ Renumbered references
def numbering(mods):
    out = {'table': {}, 'figure': {}}
    for dname, lab in [('exec', 'ES'), ('ch1', '1'), ('ch2', '2'), ('ch3', '3'), ('ch4', '4'), ('ch5', '5'), ('appendices', 'A')]:
        n = {'table': 0, 'figure': 0}
        for f in sorted(k for k in mods if k.startswith(dname + '/')):
            for b in mods[f]['blocks']:
                if b['type'] in n:
                    n[b['type']] += 1; out[b['type']][f'{lab}.{n[b["type"]]}'] = b['caption']
    return out


N8, N9 = numbering(V8), numbering(OUT)
INV9 = {k: {c: num for num, c in v.items()} for k, v in N9.items()}
XREF = re.compile(r'\b(Tables?|Figures?) ((?:ES|A|\d)\.\d+(?:(?:, | and | to )(?:ES|A|\d)\.\d+)*)')


def renum(f, s):
    def one(m):
        kind = 'table' if m.group(1).startswith('Table') else 'figure'
        return m.group(1) + ' ' + re.sub(r'(?:ES|A|\d)\.\d+', lambda t: INV9[kind][N8[kind][t.group(0)]], m.group(2))
    t = XREF.sub(one, s)
    if t != s: LOG.append({'kind': 'renumbered reference', 'file': f, 'before': s, 'after': t})
    return t


def walk(f, x):
    if isinstance(x, str): return renum(f, x)
    if isinstance(x, list): return [walk(f, y) for y in x]
    if isinstance(x, dict): return {k: (walk(f, v) if k not in ('chart', 'svg', 'id') else v) for k, v in x.items()}
    return x


for f in OUT:
    if f not in DRAFTED:
        OUT[f]['blocks'] = walk(f, OUT[f]['blocks'])

# ------------------------------------------------------------------------------------------------ Checks and write
# The work is never called a strategy, and the executive summary no longer asks the Board for decisions.
WORK = re.compile(r"\b(?:this|the|our|a|its) (?:tourism )?strateg(?:y|y's|ies)\b|\bstrategy's\b|\bfor the strategy\b|\bstrategic (?:case|narrative|plan)\b", re.I)
KEEP = re.compile(r"Growth for Jobs Strategy|G4J|Wesgro's (?:own )?strategy|investment strategies|Strategic growth|evidence-based tourism strategy that will double|Hub Strategy|Brand Strategy|gateway strategy|campaign strategy|calendar strategy|route strategy|marketing strategy|one strategy|national strategy|tourism board's strategy")
left = []
for f, d in OUT.items():
    for i, b in enumerate(d['blocks']):
        if b['type'] == 'figure': continue
        t = strip_cites(block_text(b))
        for m in WORK.finditer(t):
            ctx = t[max(0, m.start() - 80):m.end() + 60]
            if not KEEP.search(ctx): left.append((f, i, b['type'], m.group(0), ctx))
es = json.dumps(OUT['exec/01_summary.json'], ensure_ascii=False)
for k in ('asked to decide', 'Five decisions', 'Board next decides', 'The Wesgro Board decides'):
    if k in es: left.append(('exec/01_summary.json', None, 'decisions', k, ''))
print(f'{len(sweep)} edits, {len(LOG)} log entries; references left: {len(left)}')
for x in left: print('  LEFT:', x)
if DRY:
    print('dry run: nothing written'); sys.exit(0)
assert not left, 'references remain'
for f, d in OUT.items():
    with open(os.path.join(C, f), 'w') as fh:
        json.dump(d, fh, indent=1, ensure_ascii=False); fh.write('\n')
json.dump(LOG, open(os.path.join(HERE, 'applied_v10.json'), 'w'), indent=1, ensure_ascii=False)
print('written')
