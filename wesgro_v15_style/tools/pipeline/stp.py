"""Style-edit pipeline: store of new paragraph texts, dumps for editors, checks."""
import sys, re, json, os, collections
sys.path.insert(0, '/tmp/claude-0/-home-user-Letsema/98b96bfe-2843-55b4-9fb2-4f4083c56589/scratchpad/scripts')
from trk import *
WORK = '/tmp/claude-0/-home-user-Letsema/98b96bfe-2843-55b4-9fb2-4f4083c56589/scratchpad/wst/work/'
STORE = WORK + 'store.json'
PROSE = ('Body', 'Lead', 'BoxBody', 'TableMessage')
FRONT = ('Foreword', 'Contents', 'Figures', 'Tables', 'Abbreviations')

def load_store():
    return json.load(open(STORE)) if os.path.exists(STORE) else {}

def save_store(s):
    json.dump(s, open(STORE, 'w'), indent=0, ensure_ascii=False)

def seckey(s1, s2):
    if s1 == 'Executive summary': return 'ES'
    if s1 in FRONT: return 'FRONT'
    m = re.match(r'^(\d\.\d|A\d)', s2)
    if m: return m.group(1)
    return {'Context': '1.0', 'Analysis and insights': '2.0', 'Findings and recommendations': '3.0', 'Execution plan': '4.0',
            'Monitoring and evaluation framework': '5.0', 'Appendices': 'A0'}.get(s1, 'COVER')

def walk(doc):
    """yield dict(pid, p, style, sec, table(bool), tbl(el or None), cell(row,col))"""
    s1 = s2 = ''
    for el in doc.body:
        if el.tag == q('w:p'):
            st = pstyle(el); t = ptext(el).strip()
            if st in ('Heading1', 'Heading1Front'): s1 = t; s2 = ''
            elif st == 'Heading2': s2 = t
            yield dict(pid=el.get(q('w14:paraId')), p=el, style=st, sec=seckey(s1, s2), table=False, tbl=None, rc=None)
        elif el.tag == q('w:tbl'):
            for ri, tr in enumerate(el.findall(q('w:tr'))):
                for ci, tc in enumerate(tr.findall(q('w:tc'))):
                    for p in tc.iter(q('w:p')):
                        yield dict(pid=p.get(q('w14:paraId')), p=p, style=pstyle(p), sec=seckey(s1, s2), table=True, tbl=el, rc=(ri, ci))

def cur(item, store):
    return store.get(item['pid'], marked_plain(item['p']))

def dump(doc, store, secs, path):
    out = []; last_tbl = None; last_row = None
    for it in walk(doc):
        if it['sec'] not in secs: continue
        t = cur(it, store)
        if it['table']:
            if it['tbl'] is not last_tbl:
                out.append('<table>'); last_tbl = it['tbl']; last_row = None
            if it['rc'][0] != last_row:
                out.append('  row %d' % it['rc'][0]); last_row = it['rc'][0]
            if t.strip(): out.append('    [%s|%s] %s' % (it['pid'], it['style'] or 'cell', t))
        else:
            if last_tbl is not None: out.append('</table>'); last_tbl = None
            if not t.strip():
                kids = {c.tag.split('}')[1] for r in it['p'].findall(q('w:r')) for c in r}
                if 'drawing' in kids: out.append('[%s|IMAGE]' % it['pid'])
                continue
            out.append('[%s|%s] %s' % (it['pid'], it['style'] or 'plain', t))
    open(path, 'w').write('\n'.join(out) + '\n')
    return len(out)

NUM = re.compile(r'(?<![\w.])(?:R|US\$|NZ\$|S\$|A\$|\$|€|£)?\d[\d,]*(?:\.\d+)?%?')
def nums(s):
    s = re.sub(r'\[\^\d+\]', '', s)
    return collections.Counter(m.group(0).rstrip(',') for m in NUM.finditer(s))
WORDNUM = 'one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty thirty forty fifty sixty seventy eighty ninety hundred half third thirds quarter'.split()
def wnums(s):
    return collections.Counter(w for w in re.findall(r'[a-z]+', s.lower()) if w in WORDNUM)
BANNED = r'\b(ecosystem|unlock\w*|leverag\w*|delve\w*|navigat\w*|landscape|robust|seamless|tapestry|synerg\w+|paradigm|game-?changer|holistic|really|very|truly|extremely|deeply|incredibly|utili[sz]e\w*)\b|[—–]| we | our | We | Our '
def sents(t):
    t = re.sub(r'\[\^\d+\]', '', t)
    return [x for x in re.split(r'(?<=[.!?])\s+(?=[A-Z0-9])', t) if x.strip()]
