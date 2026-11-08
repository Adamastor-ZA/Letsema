"""Draft v9 content edits (Michael, 8 November 2026).

1. Chapter 3: each focus-area entry becomes a discussion of the topic, the challenge or opportunity and why the proposed course
   of action can yield results. The parts are The challenge (or The opportunity), What the evidence shows, The course of
   action, Why it can work and Link forward; "Hypothesis and disposition" goes (drafts in redteam/v9/drafts/ch3/).
2. Only the current hypothesis tree is referenced anywhere in the report: the December 2025 tree, the October review and the
   disposition labels go from the executive summary, Chapters 1 to 3 and the appendices (sweep.json, plus the pillar tables'
   Disposition column and the tree figure's disposition labels, which this script drops).
3. Section 2.1 becomes more substantive, with more on how the benchmarks were chosen (draft ch2_1.json).

Drafts carry v8 blocks as {"type": "ref", "src": [module, index]}. Sweep edits name v8 blocks by module and index:
  {"module", "index", "op": "replace", "blocks": [...]}        replace the block with new blocks (refs allowed)
  {"module", "index", "op": "delete"}                          remove the block
  {"module", "index", "op": "replace_text", "find", "repl"}   exact text replacement inside the block (all string fields)
  {"module", "index", "op": "drop_columns", "columns": [...]}  drop table or grid columns by header
  {"module", "index", "op": "drop_rows", "first_cells": [...]} drop table rows by their first cell
  {"module", "index", "op": "set", "fields": {...}}            set block fields such as message, source or caption
Every edit carries a "reason".
Usage: python3 apply_v9.py [--dry-run]. Run once on the v8 content; writes redteam/applied_v9.json.
"""
import copy, glob, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.join(HERE, '..')
C = os.path.join(B, 'content')
D = os.path.join(HERE, 'v9', 'drafts')
DRY = '--dry-run' in sys.argv
sys.path.insert(0, HERE)
from check_v9_draft import VERSIONING, block_text, strip_cites  # noqa: E402

V8 = {os.path.relpath(f, C): json.load(open(f)) for f in sorted(glob.glob(os.path.join(C, '*', '*.json')))}
assert 'ch2/01_benchmarks.json' in V8 and 'ch2/01_demand.json' not in V8, 'content/ must hold draft v8'
OUT = copy.deepcopy(V8)
LOG = []


def resolve(blocks):
    return [copy.deepcopy(V8[b['src'][0]]['blocks'][b['src'][1]]) if b.get('type') == 'ref' else b for b in blocks]


# ------------------------------------------------------------------------------------------------ 1 and 3. Module drafts
drafts = sorted(glob.glob(os.path.join(D, 'ch3', '*.json'))) + [p for p in [os.path.join(D, 'ch2_1.json')] if os.path.exists(p)]
for p in drafts:
    d = json.load(open(p))
    mod = d['module']
    assert mod in V8, mod
    OUT[mod] = {'id': d.get('id', V8[mod].get('id')), 'title': d.get('title', V8[mod].get('title')), 'blocks': resolve(d['blocks'])}
    LOG.append({'kind': 'module rewritten', 'file': mod, 'draft': os.path.relpath(p, HERE),
                'sources': d.get('sources', []) + d.get('partial_sources', []), 'relocations': d.get('relocations', [])})
    extra = d.get('appendix_blocks')
    if extra:
        OUT[extra['module']]['blocks'].extend(resolve(extra['blocks']))
        LOG.append({'kind': 'blocks appended', 'file': extra['module'], 'from_draft': os.path.relpath(p, HERE), 'blocks': len(extra['blocks'])})
DRAFTED = {e['file'] for e in LOG if e['kind'] == 'module rewritten'}

# ------------------------------------------------------------------------------------------------ 2. Sweep edits
SW = os.path.join(D, 'sweep.json')
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

# The executive summary's pillar tables lose their Disposition column; the tree figure loses its disposition labels.
ES = 'exec/01_summary.json'
for b in OUT[ES]['blocks']:
    if b['type'] == 'table' and re.match(r'Pillar \d: ', b['caption']) and any(c['header'] == 'Disposition' for c in b['columns']):
        k = [c['header'] for c in b['columns']].index('Disposition')
        w = b['columns'][k]['width']
        del b['columns'][k]
        for r in b['rows']: del r[k]
        j = [c['header'] for c in b['columns']].index('What the evidence shows and what follows')
        b['columns'][j]['width'] = round(b['columns'][j]['width'] + w, 2)
        b['source'] = b['source'].replace('; dispositions as recorded at the 14 October 2026 review', '')
        LOG.append({'kind': 'pillar table', 'file': ES, 'caption': b['caption'], 'change': 'Disposition column dropped'})
    if b['type'] == 'figure' and b.get('id') == 'fig_0_tree':
        for p in b['chart']['pillars']:
            for t in p['themes']:
                for a in t['areas']: a.pop('disposition', None)
        b['caption'] = 'The hypothesis tree'
        b['source'] = 'Letsema; Appendix A1 traces each focus area to its evidence.'
        LOG.append({'kind': 'tree figure', 'file': ES, 'change': 'disposition labels dropped; caption and source restated'})


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
left = []
for f, d in OUT.items():
    for i, b in enumerate(d['blocks']):
        t = block_text(b) if b['type'] != 'figure' else ' '.join([b.get('caption', ''), b.get('source', ''), json.dumps(b.get('chart', {}).get('pillars', ''))])
        for m in VERSIONING.finditer(strip_cites(t)):
            left.append((f, i, b['type'], m.group(0), strip_cites(t)[max(0, m.start() - 70):m.end() + 50]))
print(f'{len(drafts)} drafts, {len(sweep)} sweep edits, {len(LOG)} log entries; references to an earlier tree or a disposition left: {len(left)}')
for x in left: print('  LEFT:', x)
if DRY:
    print('dry run: nothing written'); sys.exit(0)
assert not left, 'references to an earlier tree remain'
for f, d in OUT.items():
    with open(os.path.join(C, f), 'w') as fh:
        json.dump(d, fh, indent=1, ensure_ascii=False); fh.write('\n')
json.dump(LOG, open(os.path.join(HERE, 'applied_v9.json'), 'w'), indent=1, ensure_ascii=False)
print('written')
