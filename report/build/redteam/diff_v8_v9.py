"""Content-level check of draft v9 against draft v8, outside the modules the drafts rewrote.

Every module that no draft replaced must equal its v8 form block for block, except blocks named by a sweep edit in
v9/drafts/sweep.json, the executive summary's pillar tables and tree figure (edited by apply_v9.py), and blocks whose only
change is a logged table or figure renumbering. Blocks a sweep edit deletes or replaces may shift later indices, so blocks
are aligned with difflib before comparing.
Usage: python3 diff_v8_v9.py <v8 content dir> <v9 content dir>
"""
import difflib, glob, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
LOG = json.load(open(os.path.join(HERE, 'applied_v9.json')))
SWEEP = json.load(open(os.path.join(HERE, 'v9', 'drafts', 'sweep.json')))['edits']
DRAFTED = {e['file'] for e in LOG if e['kind'] == 'module rewritten'}
TARGET = {(e['module'], e['index']) for e in SWEEP}
RENUM = [(e['file'], e['before'], e['after']) for e in LOG if e['kind'] == 'renumbered reference']


def load(d):
    return {os.path.relpath(f, d): json.load(open(f))['blocks'] for f in sorted(glob.glob(os.path.join(d, '*', '*.json')))}


def main(d8, d9):
    v8, v9 = load(d8), load(d9)
    bad, same, edited = [], 0, 0
    for f in sorted(v8):
        if f in DRAFTED: continue
        a, b = v8[f], v9[f]
        if a == b: same += 1; continue
        edited += 1
        ja = [json.dumps(x, sort_keys=True, ensure_ascii=False) for x in a]
        jb = [json.dumps(x, sort_keys=True, ensure_ascii=False) for x in b]
        for op, i1, i2, j1, j2 in difflib.SequenceMatcher(a=ja, b=jb, autojunk=False).get_opcodes():
            if op == 'equal': continue
            for i in range(i1, i2):
                x = a[i]
                if (f, i) in TARGET: continue
                if f == 'exec/01_summary.json' and (x.get('id') == 'fig_0_tree' or re.match(r'Pillar \d: ', x.get('caption') or '')): continue
                # a block changed only by renumbering
                s = json.dumps(x, ensure_ascii=False)
                for ff, bef, aft in RENUM:
                    if ff == f: s = s.replace(json.dumps(bef, ensure_ascii=False)[1:-1], json.dumps(aft, ensure_ascii=False)[1:-1])
                if json.dumps(json.loads(s), sort_keys=True, ensure_ascii=False) in jb[j1:j2]: continue
                bad.append((f, i, x['type'], json.dumps(x, ensure_ascii=False)[:150]))
    print(f'{same} untouched modules identical to v8; {edited} modules changed; {len(bad)} changed blocks not named by a sweep edit or a logged change')
    for x in bad: print('UNEXPLAINED:', x)
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
