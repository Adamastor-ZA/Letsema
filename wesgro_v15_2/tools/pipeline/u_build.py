"""Update pass: apply the twelve comments as tracked changes.  usage: u_build.py [pages.json]"""
import sys, shutil, glob
sys.path.insert(0, '/tmp/claude-0/-home-user-Letsema/98b96bfe-2843-55b4-9fb2-4f4083c56589/scratchpad/s16')
from stp import *
W16 = '/tmp/claude-0/-home-user-Letsema/98b96bfe-2843-55b4-9fb2-4f4083c56589/scratchpad/w16/'
BUILD = W16 + 'build'
pages = json.load(open(sys.argv[1])) if len(sys.argv) > 1 else None
shutil.rmtree(BUILD, ignore_errors=True); shutil.copytree(W16 + 'unpacked', BUILD)
import random; random.seed(11)
d = Doc(BUILD); T = Trk(d)
store = load_store(); logs = {}; exceptions = {}
items = {it['pid']: it for it in walk(d)}
for f in sorted(glob.glob(WORK + 'commas_[A-G].json')):
    E = json.load(open(f)); name = f[-6]
    store.update(E.get('rewrites', {})); exceptions.update(E.get('exceptions', {})); logs[name] = E.get('log', [])
ov = WORK + 'overrides.json'
if os.path.exists(ov):
    O = json.load(open(ov)); store.update(O.get('rewrites', {}))
    for pid in O.get('drop', []): store.pop(pid, None)
    for pid, pat, rep in O.get('subs', []):
        t0 = store.get(pid, marked_plain(d.P(pid))); t1 = re.sub(pat, rep, t0)
        if t1 == t0: print('SUB MISS', pid, pat)
        store[pid] = t1
json.dump(logs, open(WORK + 'agent_logs.json', 'w'), indent=1, ensure_ascii=False)
json.dump(exceptions, open(WORK + 'agent_exceptions.json', 'w'), indent=1, ensure_ascii=False)
def curtext(pid): return store.get(pid, marked_plain(d.P(pid)))

# ---------- A7 action register follows the Chapter 3 action cells
def cells(tbl, col):
    out = []
    for r in tbl.findall(q('w:tr'))[1:]:
        tcs = r.findall(q('w:tc'))
        if len(tcs) > col: out.append(tcs[col].findall(q('w:p')))
    return out
amap = {}; a7 = []
for tbl in d.body.iter(q('w:tbl')):
    rows = tbl.findall(q('w:tr')); head = [ptext(tc).strip() for tc in rows[0].findall(q('w:tc'))]
    if head[:2] == ['Who acts', 'Action']:
        for ps in cells(tbl, 1):
            for p in ps:
                pid = p.get(q('w14:paraId'))
                if pid in store and store[pid] != marked_plain(p): amap[marked_plain(p).strip()] = store[pid].strip()
    elif 'Action' in head and len(rows) > 100:
        a7 = [p for ps in cells(tbl, head.index('Action')) for p in ps]
n7 = 0
for p in a7:
    t = marked_plain(p).strip()
    if t in amap: store[p.get(q('w14:paraId'))] = amap[t]; n7 += 1
left7 = [p.get(q('w14:paraId')) for p in a7 if re.search(r', (and|or)\b', curtext(p.get(q('w14:paraId'))))]
print('A7 cells aligned', n7, 'A7 cells still with a comma construction', len(left7), left7[:5])

# ---------- C12 and C13: "How to read this report" moves to the front matter
S13 = ['48D56842', '3E0D8225', '27469AF0', '54A5FF22', '78BFCD65']
t13 = {k: curtext(k) for k in S13}
for k in S13: store.pop(k, None)
lead13 = 'The report is built so that a stakeholder can read the summary and any one objective on its own. The programme office can run the plan from Chapters 3 to 5.'
anchor = d.P('2298786B')                      # the paragraph that ends the front-matter section
front = [T.copy_para_inserted(d.P('5B5F83F1')),
         T.new_para(d.P('7A559CB3'), 'How to read this report'),
         T.new_para(d.P('3E0D8225'), lead13),
         T.new_para(d.P('27469AF0'), t13['27469AF0']),
         T.new_para(d.P('54A5FF22'), t13['54A5FF22']),
         T.new_para(d.P('78BFCD65'), t13['78BFCD65'])]
insert_before(anchor, *front)

# ---------- C11: mechanistic sections removed
C11 = ['78D36AF1', '283897F3', '20A30906', '5A30EE6B']
for k in C11: store.pop(k, None)

# ---------- C10: steering committees and working groups (details not yet supplied)
c10 = T.new_para(d.P('36E52EAE'), 'Steering committee meetings and Board tourism working groups ran throughout the project. [[QUERY C10: dates and number of these meetings and the membership of each body, to be supplied]]')
insert_after(d.P('36E52EAE'), c10)

# ---------- C4: Figure ES.2 as a diagram
shutil.copy(W16 + 'figs/fig/fig_es_2.png', BUILD + '/word/media/image_es2.png')
rp = BUILD + '/word/_rels/document.xml.rels'; rx = open(rp).read()
assert 'rIdES2' not in rx
rx = rx.replace('</Relationships>', '<Relationship Id="rIdES2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/image_es2.png"/></Relationships>')
open(rp, 'w').write(rx)
src = copy.deepcopy(d.P('2D228581'))          # Figure ES.1's image paragraph
WP = '{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}'; A = '{http://schemas.openxmlformats.org/drawingml/2006/main}'
R = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}'
ext = src.find('.//' + WP + 'extent'); cx = int(ext.get('cx')); cy = int(round(cx * 2076 / 3200.0))
ext.set('cy', str(cy))
for e in src.iter(A + 'ext'):
    if e.get('cx') == str(cx): e.set('cy', str(cy))
for b in src.iter(A + 'blip'): b.set(R + 'embed', 'rIdES2')
for dp in src.iter(WP + 'docPr'):
    dp.set('id', '9201'); dp.set('name', 'Figure ES.2'); dp.set('descr', 'Diagram of the three strategic goals, six themes and twenty objectives')
cap2 = d.P('3177D7C8'); tbl2 = cap2.getnext()
while tbl2.tag != q('w:tbl'): tbl2 = tbl2.getnext()
insert_before(cap2, T.copy_para_inserted(src))
for p in tbl2.iter(q('w:p')): store.pop(p.get(q('w14:paraId')), None)
T.delete_table(tbl2)

# ---------- rewrites and deletions
miss = 0
for pid, text in store.items():
    try: p = d.P(pid)
    except KeyError: miss += 1; print('MISSING PID', pid); continue
    T.rewrite(p, text)
for k in S13 + C11: T.delete_para(d.P(k))

# ---------- footnotes (C7)
FN = [(r'\(SA Tourism departure survey\), and Destination', '(SA Tourism departure survey) and Destination'), (r'Mar 2026, and January to December 2023', 'Mar 2026 and January to December 2023'),
      (r'61% in its text, and 63% is', '61% in its text; 63% is'), (r'reported for FY2024, and the spend path', 'reported for FY2024; the spend path'),
      (r'sum to 29,015, and the aviation', 'sum to 29,015; the aviation'), (r'is not printed, and they differ', 'is not printed and they differ'),
      (r'Garden Route, p147, and Central Karoo', 'Garden Route, p147; Central Karoo'), (r'municipal plans, and need rests', 'municipal plans; need rests'),
      (r'"Seasonality", and Demand-Side', '"Seasonality" and Demand-Side'), (r'no source line, and the plan pools', 'no source line; the plan pools'),
      (r'two-way seats, or 1,908,399 each way, in the year', 'two-way seats (1,908,399 each way) in the year'),
      (r'gap 1,216,601, or 63\.7%', 'gap 1,216,601 (63.7%)'), (r'gap 811,324, or 42\.5%', 'gap 811,324 (42.5%)')]
nf = 0
for fp in d.fnroot.iter(q('w:p')):
    t0 = marked_plain(fp); t1 = t0
    for a, b in FN: t1 = re.sub(a, b, t1)
    if t1 != t0: T.rewrite(fp, t1); nf += 1
left_fn = [marked_plain(fp)[:80] for fp in d.fnroot.iter(q('w:p')) if re.search(r', (and|or)\b', ''.join(rtext(r) for r in fp.iter(q('w:r')) if r.getparent().tag != q('w:del')))]
print('footnotes fixed', nf, 'left', left_fn)

# ---------- contents and lists
def acc_text(p):
    if p.find('w:pPr/w:rPr/w:del', NS) is not None and not [r for r in p.iter(q('w:r')) if r.getparent().tag != q('w:del') and rtext(r).strip()]: return None
    return ''.join(rtext(r) for r in p.iter(q('w:r')) if r.getparent().tag != q('w:del'))
heads, figs, tabs = [], [], []; body = False
for el in d.body:
    ps = [el] if el.tag == q('w:p') else list(el.iter(q('w:p')))
    for p in ps:
        st = pstyle(p); t = acc_text(p)
        if not t or not t.strip(): continue
        t = t.strip()
        if st == 'Heading1Front' and t == 'How to read this report': heads.append((1, t)); continue
        if st == 'Heading1' and t == 'Executive summary': body = True
        if not body: continue
        if st == 'Heading1': heads.append((1, t))
        elif st == 'Heading2': heads.append((2, t))
        elif st == 'Caption' and t.startswith('Figure'): figs.append(t)
        elif st == 'Caption' and t.startswith('Table'): tabs.append(t)
json.dump({'toc': heads, 'figs': figs, 'tabs': tabs}, open(WORK + 'toc_entries.json', 'w'))
def sync(h_text, desired, keyf, styles):
    h = [p for p in d.body.findall(q('w:p')) if pstyle(p) == 'Heading1Front' and ptext(p).strip() == h_text][0]
    ent = []; n = h.getnext()
    while n is not None and pstyle(n) in styles: ent.append(n); n = n.getnext()
    def title(s): return re.sub(r'^((Figure|Table) [A-Z0-9.]+\.|\d\.\d)\s*', '', s.split('\t')[0]).strip()
    old = [(e, ptext(e)) for e in ent]; used = set(); anchor = h; new = 0
    om = {}
    for e, s in old: om.setdefault(title(s), []).append((e, s))
    first_l1 = next(e for e, s in old if pstyle(e) == 'TOCL1') if h_text == 'Contents' else None
    for label in desired:
        cand = [x for x in om.get(title(label), []) if id(x[0]) not in used]
        page = (pages or {}).get(keyf(label))
        if cand:
            e, s = cand[0]; used.add(id(e)); T.rewrite(e, label + '\t' + (page or s.split('\t')[-1])); anchor = e
        else:
            like = first_l1 if (h_text == 'Contents' and label == 'How to read this report') else old[min(len(old) - 1, 6)][0]
            ne = T.new_para(like, label + '\t' + (page or '0')); insert_after(anchor, ne); anchor = ne; new += 1
    for e, s in old:
        if id(e) not in used: T.delete_para(e)
    return new
sync('Contents', [t for l, t in heads], lambda s: 'H|' + s, ('TOCL1', 'TOCL2'))
sync('Figures', figs, lambda s: 'C|' + s, ('TOCL2',))
sync('Tables', tabs, lambda s: 'C|' + s, ('TOCL2',))

def order_footnotes(d):
    pos = {}
    for i, r in enumerate(d.body.iter(q('w:footnoteReference'))): pos.setdefault(r.get(q('w:id')), i)
    fns = d.fnroot.findall(q('w:footnote'))
    special = [f for f in fns if f.get(q('w:type')) is not None]
    normal = sorted([f for f in fns if f.get(q('w:type')) is None], key=lambda f: pos.get(f.get(q('w:id')), 10**9))
    for f in fns: d.fnroot.remove(f)
    for f in special + normal: d.fnroot.append(f)
    newid = {f.get(q('w:id')): str(i) for i, f in enumerate(normal, 1)}
    for f in normal: f.set(q('w:id'), newid[f.get(q('w:id'))])
    for r in d.body.iter(q('w:footnoteReference')): r.set(q('w:id'), newid[r.get(q('w:id'))])
order_footnotes(d)
d.save()
print('missing', miss, T.stats, 'heads', len(heads), 'figs', len(figs), 'tabs', len(tabs))
