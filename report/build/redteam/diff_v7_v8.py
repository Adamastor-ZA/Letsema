"""Content-level check of draft v8 against draft v7.

The rewritten modules (executive summary, section 1.1, Chapter 2) are checked draft by draft with check_v8_draft.py.
This script checks everything else: every module outside the rewrite must equal its v7 form once the logged edits in
applied_v8.json are applied (text edits, renumbered references, the traceability column, appended blocks). It also checks
that every open item in the v7 executive summary, section 1.1 and Chapter 2 survives word for word somewhere in v8.
Usage: python3 diff_v7_v8.py <v7 content dir> <v8 content dir>
"""
import glob, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
LOG = json.load(open(os.path.join(HERE, 'applied_v8.json')))
REWRITTEN = {e['file'] for e in LOG if e['kind'] in ('module rewritten', 'module created', 'module removed')}


def load(d):
    return {os.path.relpath(f, d): json.load(open(f)) for f in sorted(glob.glob(os.path.join(d, '*', '*.json')))}


def main(d7, d8):
    v7, v8 = load(d7), load(d8)
    bad, same, edited = [], 0, 0
    for f in sorted(set(v7) | set(v8)):
        if f in REWRITTEN: continue
        if f not in v7 or f not in v8: bad.append((f, 'module added or removed without a log entry')); continue
        s = json.dumps(v7[f]['blocks'], ensure_ascii=False)
        for e in LOG:
            if e.get('file') == f and e['kind'] in ('text edit', 'renumbered reference'):
                s = s.replace(json.dumps(e['before'], ensure_ascii=False)[1:-1], json.dumps(e['after'], ensure_ascii=False)[1:-1], 1)
        exp = json.loads(s)
        for e in LOG:
            if e.get('file') == f and e['kind'] == 'traceability':
                t = next(b for b in exp if b['type'] == 'table' and b['caption'] == 'Traceability by focus area')
                k = [c['header'] for c in t['columns']].index('Chapter 2')
                r = next(r for r in t['rows'] if int(re.match(r'\D*(\d+)', r[0]).group(1)) == e['fa'])
                assert r[k] == e['before']; r[k] = e['after']
        got = v8[f]['blocks']
        n_app = sum(e['blocks'] for e in LOG if e['kind'] == 'blocks appended' and e['file'] == f)
        if n_app:
            if got[:len(got) - n_app] != exp: bad.append((f, 'blocks before the appended ones differ'))
            edited += 1; continue
        if got == exp:
            if v7[f]['blocks'] == got: same += 1
            else: edited += 1
        else:
            for i, (a, b) in enumerate(zip(exp, got)):
                if a != b: bad.append((f, i, json.dumps(a, ensure_ascii=False)[:160], json.dumps(b, ensure_ascii=False)[:160]))
            if len(exp) != len(got): bad.append((f, 'block count', len(exp), len(got)))
    # open items
    def strings(x):
        if isinstance(x, str): yield x
        elif isinstance(x, list):
            for y in x: yield from strings(y)
        elif isinstance(x, dict):
            for k, y in x.items():
                if k not in ('chart', 'svg'): yield from strings(y)
    txt = lambda mods: '\n'.join(strings(list(mods.values())))
    old = {k: v for k, v in v7.items() if k.startswith(('exec/', 'ch2/')) or k == 'ch1/01_mandate.json'}
    norm = lambda s: re.sub(r'\W+', ' ', s).strip().lower()
    items = {norm(x) for x in re.findall(r'\[([^\]]+)\]', txt(old))}
    have = {norm(x) for x in re.findall(r'\[([^\]]+)\]', txt(v8))}
    lost = sorted(items - have)
    print(f'{same} modules unchanged; {edited} changed only by logged edits; {len(bad)} unexplained differences')
    for x in bad: print('UNEXPLAINED:', x)
    print(f'open items in the v7 summary, section 1.1 and Chapter 2: {len(items)}; not found word for word in v8: {len(lost)}')
    for x in lost: print('  LOST:', x[:160])
    sys.exit(1 if bad or lost else 0)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
