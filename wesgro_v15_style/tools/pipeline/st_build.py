"""Assemble the edited report as tracked changes.  usage: st_build.py [pages.json]"""
import sys, shutil, glob, subprocess
sys.path.insert(0, '/tmp/claude-0/-home-user-Letsema/98b96bfe-2843-55b4-9fb2-4f4083c56589/scratchpad/scripts')
from stp import *
from es_spec import ES, Q
WST = '/tmp/claude-0/-home-user-Letsema/98b96bfe-2843-55b4-9fb2-4f4083c56589/scratchpad/wst/'
BUILD = WST + 'build'
pages = json.load(open(sys.argv[1])) if len(sys.argv) > 1 else None
shutil.rmtree(BUILD, ignore_errors=True); shutil.copytree(WST + 'unpacked', BUILD)
import random; random.seed(7)
d = Doc(BUILD); T = Trk(d)
store = load_store(); inserts = []; deletes = []; queries = []; logs = {}
for f in sorted(glob.glob(WORK + 'edits_*.json')):
    E = json.load(open(f)); name = f.split('edits_')[1][:-5]
    store.update(E.get('rewrites', {})); inserts += E.get('inserts', []); deletes += E.get('deletes', [])
    for qy in E.get('queries', []): qy['from'] = name; queries.append(qy)
    logs[name] = E.get('log', [])
ov = WORK + 'overrides.json'   # lead editor's corrections to agent edits: {"rewrites": {...}, "drop": [pids]}
if os.path.exists(ov):
    O = json.load(open(ov)); store.update(O.get('rewrites', {}))
    for pid in O.get('drop', []): store.pop(pid, None)
json.dump(queries, open(WORK + 'agent_queries.json', 'w'), indent=1, ensure_ascii=False)
json.dump(logs, open(WORK + 'agent_logs.json', 'w'), indent=1, ensure_ascii=False)
items = {it['pid']: it for it in walk(d)}
def curtext(pid): return store.get(pid, marked_plain(d.P(pid)))

# ---------- late mechanical fixes the first pass missed
for it in walk(d):
    if it['style'] in PROSE and it['sec'] not in ('FRONT', 'COVER'):
        t0 = curtext(it['pid']); t1 = re.sub(r'\bThe Winelands\b', 'The Cape Winelands', t0)
        if t1 != t0: store[it['pid']] = t1

for pid in (json.load(open(ov)).get('unsplit', []) if os.path.exists(ov) else []):
    parts = [i for i in inserts if i['after'] == pid]
    store[pid] = ' '.join([curtext(pid)] + [i['text'] for i in parts])
    inserts = [i for i in inserts if i['after'] != pid]
for pid, pat, rep in (json.load(open(ov)).get('subs', []) if os.path.exists(ov) else []):
    t0 = curtext(pid); t1 = re.sub(pat, rep, t0)
    if t1 == t0: print('SUB MISS', pid, pat)
    store[pid] = t1
# source keys keep "SCIP"; nothing to do there

# ---------- placeholders for open queries (one each, at the first place the issue bites)
def placeholder(pid, pat, ph):
    t = curtext(pid); m = re.search(pat, t)
    if not m: print('PLACEHOLDER MISS', pid, ph); return
    e = re.search(r'[.!?](?:\[\^\d+\])*(?=\s|$)', t[m.end():])
    pos = m.end() + (e.start() if e else len(t) - m.end())
    store[pid] = t[:pos] + ' ' + ph + t[pos:]
def first(pat, secs, styles=('Body', 'Lead')):
    for it in walk(d):
        if it['sec'] in secs and it['style'] in styles and not it['table'] and re.search(pat, curtext(it['pid'])): return it['pid']
P_ = [(r'Department of Economic Development(?! and Tourism)', ('2.3', '2.4', '2.5'), '[[QUERY Q13: is this DEDAT?]]'),
      (r'growth markets', ('2.3',), '[[QUERY Q4: which markets are the growth markets?]]'),
      (r'\bGCC\b', ('3.4',), '[[QUERY Q6: Gulf, Middle East or GCC?]]'),
      (r'1\.4 million arrive', ('2.1',), '[[QUERY Q11: 1.4 million arrivals where, and in which year?]]'),
      (r'\bwinter\b', ('2.3',), '[[QUERY Q16: which months?]]'),
      (r'\bSMMEs?\b', ('2.5',), '[[QUERY Q17: SME or SMME?]]'),
      (r'FY2025', ('1.2', '2.3'), '[[QUERY Q7: is FY2025 the same year as FY24/25?]]'),
      (r'1,498,829', ('1.1', '2.3'), '[[QUERY Q10: what does the 1,498,829 count?]]'),
      (r'[Tt]he province should', ('2.2',), '[[QUERY Q5: who acts here: Wesgro, DEDAT or the Western Cape Government?]]'),
      (r'funders already sit in the partnership', ('4.6',), '[[QUERY Q15: partnership or unit?]]'),
      (r'LTOs?\b', ('3.3',), '[[QUERY Q14: are local destination bodies the LTOs?]]')]
for pat, secs, ph in P_:
    pid = first(pat, secs)
    if pid: placeholder(pid, pat, ph)
    else: print('PLACEHOLDER: no paragraph for', ph)

# ---------- executive summary ops
es_new = []; es_del = []
for op in ES:
    if op[0] == 'rw': store[op[1]] = op[2]
    elif op[0] == 'rep': es_del.append(op[1]); es_new.append((op[1], op[1], op[2])); store.pop(op[1], None)
    elif op[0] == 'del': es_del.append(op[1]); store.pop(op[1], None)
    elif op[0] == 'new': es_new.append((op[1], op[2], op[3]))
# figure captions that carry the old scenario word
store['1B80DC9E'] = store.get('1B80DC9E', marked_plain(d.P('1B80DC9E')))
for it in walk(d):
    if it['style'] == 'Caption' and 'paths' in marked_plain(it['p']):
        store[it['pid']] = marked_plain(it['p']).replace('Arrivals paths and milestones', 'Arrivals by case and milestones').replace('Arrivals paths to 2035', 'Arrivals by case to 2035')
store.pop('1B80DC9E', None)

# ---------- central question (1.1) and closing answer (3.4)
extra_new = [('732A8E88', '32E7390F', 'This report answers one question: ' + Q),
             ('294EAF01', '294EAF01', 'This answers the question the report began with (section 1.1). Conversion comes first, and seats pace growth at the peak. The base case holds if current marketing continues and the hub carriers keep adding capacity. The target also needs direct India and China routes, dedicated activation and national escalation. Without confirmed routes, growth reverts to the base case.')]

# ---------- table numbers
def tmap(k):
    k = int(k); return k + 1 if k <= 7 else (k + 2 if k <= 13 else k + 3)
def renum(t):
    def grp(m):
        return m.group(1) + re.sub(r'3\.(\d+)', lambda x: '3.%d' % tmap(x.group(1)), m.group(2))
    t = re.sub(r'(Tables? )(3\.\d+(?:(?:, | and | to )3\.\d+)*)', grp, t)
    return t.replace('Table ES.5', 'Table ES.1')
moved_src = {'69417BDB': ('10397D18', '2ADAA706', 'Table 3.1.'), '4AA2F9E4': ('695972EC', None, 'Table 3.9.'), '2733F456': ('0F314656', None, 'Table 3.16.')}
skip = set(es_del) | set(moved_src) | {v[0] for v in moved_src.values()} | {'1AFA7412'}
for it in list(walk(d)):
    if it['sec'] in ('FRONT', 'COVER') or it['pid'] in skip: continue
    t = store.get(it['pid'], marked_plain(it['p']))
    if 'Table' in t:
        n = renum(t)
        if n != t: store[it['pid']] = n
for fp in d.fnroot.iter(q('w:p')):
    t = marked_plain(fp)
    if 'Table' in t and renum(t) != t: T.rewrite(fp, renum(t))

# ---------- moved tables (copies made before anything is rewritten)
def next_tbl(p):
    n = p.getnext()
    while n is not None and n.tag != q('w:tbl'): n = n.getnext()
    return n
def lead_after(h2text):
    hit = False
    for el in d.body:
        if el.tag == q('w:p') and pstyle(el) == 'Heading2' and ptext(el).strip().startswith(h2text): hit = True
        elif hit and el.tag == q('w:p') and pstyle(el) == 'Lead': return el
dest = {'69417BDB': lead_after('3.1 '), '4AA2F9E4': lead_after('3.2 '), '2733F456': lead_after('3.3 ')}
spacer = d.P('60881121')
todo_del = []
for cap_pid, (msg_pid, _, label) in moved_src.items():
    cap = d.P(cap_pid); msg = d.P(msg_pid); tbl = next_tbl(msg)
    ctbl = copy.deepcopy(tbl)
    for p in ctbl.iter(q('w:p')):
        pid = p.get(q('w14:paraId'))
        if pid in store and store[pid] != marked_plain(p): rewrite_paragraph(p, store[pid].replace('__', ''))
    ccap = copy.deepcopy(cap)
    for r in ccap.findall(q('w:r')):
        for tt in r.findall(q('w:t')):
            if tt.text and tt.text.strip().startswith('Table ES.'): tt.text = label + (' ' if tt.text.endswith(' ') else '')
    new = [T.copy_para_inserted(ccap), T.copy_para_inserted(msg), T.insert_table_copy(ctbl), T.copy_para_inserted(spacer)]
    insert_after(dest[cap_pid], *new)
    todo_del.append((cap, msg, tbl))
    for p in tbl.iter(q('w:p')): store.pop(p.get(q('w14:paraId')), None)
for cap, msg, tbl in todo_del:
    T.delete_para(cap); T.delete_para(msg); T.delete_table(tbl)
for pid in ('60881121', '5441FEFB'): T.delete_para(d.P(pid))
cap4 = d.P('1AFA7412'); t4 = next_tbl(cap4)
for p in t4.iter(q('w:p')): store.pop(p.get(q('w14:paraId')), None)
T.delete_para(cap4); T.delete_table(t4)

# ---------- rewrites, inserts, deletes
for pid in es_del + deletes: store.pop(pid, None)
miss = 0
for pid, text in store.items():
    try: p = d.P(pid)
    except KeyError: miss += 1; print('MISSING PID', pid); continue
    T.rewrite(p, text)
last = {}
def body_like(pid):
    p = d.P(pid)
    if pstyle(p) in ('Body', 'BoxBody'): return p
    sec = items[pid]['sec']
    return next(x['p'] for x in walk(d) if x['sec'] == sec and x['style'] == 'Body' and not x['table'])
for after, like, text in [(i['after'], i['after'], i['text']) for i in inserts] + es_new + extra_new:
    ref = last.get(after, d.P(after))
    np_ = T.new_para(body_like(like), text)
    insert_after(ref, np_)
    last[after] = np_
for pid in es_del + deletes: T.delete_para(d.P(pid))

# ---------- glossary order (production checklist): two rows moved, as tracked row delete and insert
def move_row(cell_pid, after_cell_pid):
    tr = tr_of(d.P(cell_pid)); dst = tr_of(d.P(after_cell_pid))
    new = copy.deepcopy(tr)
    trpr = new.find(q('w:trPr'))
    if trpr is None:
        trpr = etree.Element(q('w:trPr')); new.insert(0, trpr)
    trpr.append(T.E('w:ins'))
    for p in new.iter(q('w:p')):
        p.set(q('w14:paraId'), d.new_pid())
        for c in list(p):
            if c.tag.split('}')[1] in INVIS or (c.tag == q('w:r') and c.find(q('w:commentReference')) is not None): p.remove(c)
        runs = [c for c in p if c.tag == q('w:r')]
        if runs:
            ins = T.E('w:ins'); p.insert(list(p).index(runs[0]), ins)
            for r in runs: ins.append(r)
        T._mark_ppr(p, 'ins')
    dst.addnext(new)
    trpr = tr.find(q('w:trPr'))
    if trpr is None:
        trpr = etree.Element(q('w:trPr')); tr.insert(0, trpr)
    trpr.append(T.E('w:del'))
    for p in tr.iter(q('w:p')): T.delete_para(p)
    return tbl_of(d.P(after_cell_pid))
g = move_row('65EB7685', '5D471DA9'); move_row('2BE9B924', '218E7951')
live = [tr for tr in g.findall(q('w:tr')) if tr.find('w:trPr/w:del', NS) is None]
def shade_of(tr):
    s = tr.find('.//w:tcPr/w:shd', NS); return s.get(q('w:fill')) if s is not None else None
pattern = [shade_of(tr) for tr in g.findall(q('w:tr')) if True][1:3]
for i, tr in enumerate(live[1:]):
    want = pattern[i % 2]
    for tcpr in tr.iter(q('w:tcPr')):
        s = tcpr.find(q('w:shd'))
        if want is None:
            if s is not None: tcpr.remove(s)
        else:
            if s is None:
                s = etree.Element(q('w:shd')); idx = 0
                for k, c in enumerate(tcpr):
                    if c.tag.split('}')[1] in ('tcW', 'gridSpan', 'vMerge', 'hMerge', 'tcBorders'): idx = k + 1
                tcpr.insert(idx, s); s.set(q('w:val'), 'clear'); s.set(q('w:color'), 'auto')
            s.set(q('w:fill'), want)

# ---------- contents and lists
def acc_text(p):
    if p.find('w:pPr/w:rPr/w:del', NS) is not None and not [r for r in p.iter(q('w:r')) if r.getparent().tag != q('w:del') and rtext(r).strip()]: return None
    return ''.join(rtext(r) for r in p.iter(q('w:r')) if r.getparent().tag != q('w:del'))
heads, figs, tabs = [], [], []
front = True
for el in d.body:
    ps = [el] if el.tag == q('w:p') else list(el.iter(q('w:p')))
    for p in ps:
        st = pstyle(p); t = acc_text(p)
        if st == 'Heading1' and t and t.strip() == 'Executive summary': front = False
        if front or not t or not t.strip(): continue
        t = t.strip()
        if st == 'Heading1': heads.append((1, t))
        elif st == 'Heading2': heads.append((2, t))
        elif st == 'Caption' and t.startswith('Figure'): figs.append(t)
        elif st == 'Caption' and t.startswith('Table'): tabs.append(t)
json.dump({'toc': heads, 'figs': figs, 'tabs': tabs}, open(WORK + 'toc_entries.json', 'w'))
def sync(h_text, desired, keyf, styles):
    h = [p for p in d.body.findall(q('w:p')) if pstyle(p) == 'Heading1Front' and ptext(p).strip() == h_text][0]
    ent = []; n = h.getnext()
    while n is not None and pstyle(n) in styles: ent.append(n); n = n.getnext()
    def title(s): return re.sub(r'^(Figure|Table) [A-Z0-9.]+\.\s*', '', s.split('\t')[0]).strip()
    old = [(e, ptext(e)) for e in ent]
    used = set(); anchor = h; res = 0
    oldmap = {}
    for e, s in old:
        oldmap.setdefault(title(s), []).append((e, s))
    for des in desired:
        label, pg = des
        cand = [x for x in oldmap.get(title(label), []) if id(x[0]) not in used]
        moved = cand and cand[0][1].startswith('Table ES.') and label.startswith('Table 3.')
        page = (pages or {}).get(keyf(label))
        if cand and not moved:
            e, s = cand[0]; used.add(id(e))
            T.rewrite(e, label + '\t' + (page or s.split('\t')[-1])); anchor = e
        else:
            like = old[min(len(old) - 1, 6)][0]
            ne = T.new_para(like, label + '\t' + (page or '0'))
            insert_after(anchor, ne); anchor = ne; res += 1
    for e, s in old:
        if id(e) not in used: T.delete_para(e)
    return res
lvl_style = {1: 'TOCL1', 2: 'TOCL2'}
sync('Contents', [(t, None) for l, t in heads], lambda s: 'H|' + s, ('TOCL1', 'TOCL2'))
sync('Figures', [(t, None) for t in figs], lambda s: 'C|' + s, ('TOCL2',))
sync('Tables', [(t, None) for t in tabs], lambda s: 'C|' + s, ('TOCL2',))

# ---------- Figure ES.1 callout wording (image text; cannot be tracked)
from PIL import Image, ImageDraw, ImageFont
ip = BUILD + '/word/media/image3.png'
im = Image.open(ip).convert('RGB'); dr = ImageDraw.Draw(im)
fill = im.getpixel((1000, 200)); ink = (77, 77, 79)
dr.rectangle([380, 165, 1735, 340], fill=fill)
f = ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf', 46)
dr.text((412, 192), 'Only the accelerated case reaches 2.5m by 2035; the', font=f, fill=ink)
dr.text((412, 254), 'base case reaches about 2.2m.', font=f, fill=ink)
im.save(ip, optimize=True)

d.save()
print('missing', miss, T.stats, 'figs', len(figs), 'tabs', len(tabs), 'heads', len(heads))
