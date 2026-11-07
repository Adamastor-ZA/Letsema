"""Content-level diff of draft v6 against draft v7 (the "change nothing else" test for the table review).

The renderer did not change between v6 and v7, so every difference in the report comes from the content modules.
This script aligns the v6 and v7 blocks of each module and maps every changed block to an entry in applied_v7.json.
Tables kept in both versions are compared cell by cell, so an added column or a width change is all that may differ.
Usage: python3 diff_v6_v7.py <v6 content dir> <v7 content dir>
"""
import difflib, glob, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
LOG = json.load(open(os.path.join(HERE, 'applied_v7.json')))['log']
TABLES = {e['table'] for e in LOG if e['table']} | {c for e in LOG for c in e.get('captions', [])}
EDITS = [e for e in LOG if e['action'] in ('text edit', 'renumbered reference')]
AFTER = ' '.join(e['after'] for e in LOG if e['action'] == 'narrative')
for e in LOG:  # the narrative 'after' is logged before the sentence splits
    if e['group'] == 'sentence split': AFTER = AFTER.replace(e['before'], e['after'])


def load(d):
    return {os.path.relpath(f, d): json.load(open(f))['blocks'] for f in sorted(glob.glob(os.path.join(d, '*', '*.json')))}


def text(b):
    return ' '.join([b.get('text', ''), ' '.join(b.get('items', []) if isinstance(b.get('items'), list) else []), b.get('source', '')])


def explained_old(b):
    if b['type'] == 'table': return b['caption'] in TABLES
    return any(e['before'] in text(b) for e in EDITS)


def explained_new(b):
    if b['type'] == 'table': return b['caption'] in TABLES
    t = b.get('text', '')
    if t and t in AFTER: return True
    return any(e['after'] in text(b) for e in EDITS)


def same_table(f, a, b):
    """Kept tables: same caption, message, source and cells, apart from logged edits, added columns and widths."""
    s = json.dumps(a, ensure_ascii=False)
    for e in EDITS:
        if e['file'] == f: s = s.replace(e['before'], e['after'])
    a = json.loads(s)
    ha, hb = [c['header'] for c in a['columns']], [c['header'] for c in b['columns']]
    if not set(ha) <= set(hb): return 'columns dropped'
    if len(hb) > len(ha) and not any(e['table'] == b['caption'] and 'column' in e['action'] for e in LOG): return 'unlogged column'
    keep = [hb.index(h) for h in ha]
    if a['rows'] != [[r[i] for i in keep] for r in b['rows']]: return 'cells changed'
    for k in ('caption', 'message', 'source'):
        if a.get(k) != b.get(k) and not any(e['table'] == b['caption'] and b.get(k, '') in e['after'] and a.get(k, '') in e['before'] for e in LOG):
            return k + ' changed'
    return None


def main(d6, d7):
    v6, v7 = load(d6), load(d7)
    assert set(v6) == set(v7)
    bad, n_old, n_new, kept, edited = [], 0, 0, 0, 0
    for f in v6:
        a, b = v6[f], v7[f]
        ja, jb = [json.dumps(x, sort_keys=True, ensure_ascii=False) for x in a], [json.dumps(x, sort_keys=True, ensure_ascii=False) for x in b]
        for op, i1, i2, j1, j2 in difflib.SequenceMatcher(a=ja, b=jb, autojunk=False).get_opcodes():
            if op == 'equal': continue
            olds, news = a[i1:i2], b[j1:j2]
            # A table present on both sides with the same caption is a kept table: compare it cell by cell.
            for x in list(olds):
                y = next((y for y in news if y['type'] == 'table' and x['type'] == 'table' and y['caption'] == x['caption']), None)
                if y is not None:
                    kept += 1
                    why = same_table(f, x, y)
                    if why: bad.append((f, 'kept table: ' + why, x['caption']))
                    olds.remove(x); news.remove(y)
            # An edited paragraph must become its v7 form exactly once the logged edits are applied to it.
            for x in [x for x in olds if x['type'] != 'table']:
                s = json.dumps(x, ensure_ascii=False)
                for e in EDITS:
                    if e['file'] == f: s = s.replace(e['before'], e['after'])
                y = next((y for y in news if json.dumps(y, ensure_ascii=False) == s), None)
                if y is not None:
                    edited += 1; olds.remove(x); news.remove(y)
            for x in olds:
                n_old += 1
                if not explained_old(x): bad.append((f, 'removed', x['type'], (x.get('caption') or text(x))[:160]))
            for y in news:
                n_new += 1
                if not explained_new(y): bad.append((f, 'added', y['type'], (y.get('caption') or text(y))[:160]))
    print(f'{edited} paragraphs edited exactly as logged; {kept} kept tables compared cell by cell; {n_old} v6 blocks removed, {n_new} v7 blocks added')
    for x in bad: print('UNEXPLAINED:', x)
    print('UNEXPLAINED', len(bad))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
