import sys, re, json, csv
sys.path.insert(0, '/tmp/claude-0/-home-user-Letsema/98b96bfe-2843-55b4-9fb2-4f4083c56589/scratchpad/scripts')
from dxst import *
OUT = '/home/user/Letsema/wesgro_v15_style/output/'
d = Doc(); kids = list(d.body)
def words_of(el):
    return sum(len(ptext(p).split()) for p in ([el] if el.tag == q('w:p') else el.iter(q('w:p'))))
# ---- headings with level and word counts
heads = []
for i, el in enumerate(kids):
    if el.tag == q('w:p') and pstyle(el) in ('Heading1', 'Heading1Front', 'Heading2', 'Heading3', 'Heading4'):
        heads.append([i, pstyle(el), ptext(el).strip(), 0])
for j, h in enumerate(heads):
    lvl = {'Heading1': 1, 'Heading1Front': 1, 'Heading2': 2, 'Heading3': 3, 'Heading4': 4}[h[1]]
    end = len(kids)
    for k in heads[j + 1:]:
        l2 = {'Heading1': 1, 'Heading1Front': 1, 'Heading2': 2, 'Heading3': 3, 'Heading4': 4}[k[1]]
        if l2 <= lvl: end = k[0]; break
    h[3] = sum(words_of(e) for e in kids[h[0] + 1:end] if not (e.tag == q('w:p') and pstyle(e) in ('TOCL1', 'TOCL2')))
    h.append(lvl)
lines = ['# Structure map (v15.1)', '', '## Headings', '', '| Level | Heading | Words beneath (tables included) |', '|---|---|---|']
for i, st, t, w, lvl in heads:
    if lvl <= 3: lines.append('| %d | %s%s | %s |' % (lvl, '&nbsp;&nbsp;' * (lvl - 1), t, format(w, ',')))
h4 = [h for h in heads if h[4] == 4]
lines += ['', 'Level 4 headings: %d (the five recurring parts of each objective, the comparator and district subheads).' % len(h4)]
# ---- figures and tables against their list entries
def front_list(name):
    h = [p for p in kids if p.tag == q('w:p') and pstyle(p) == 'Heading1Front' and ptext(p).strip() == name][0]
    out = []; n = h.getnext()
    while n is not None and n.tag == q('w:p') and pstyle(n) in ('TOCL1', 'TOCL2'):
        out.append(re.sub(r'\s+', ' ', ptext(n).rsplit('\t', 1)[0]).strip() if '\t' in ptext(n) else re.sub(r'\s*\d+$', '', re.sub(r'\s+', ' ', ptext(n))).strip()); n = n.getnext()
    return out
caps = [re.sub(r'\s+', ' ', ptext(p)).strip() for p in kids if p.tag == q('w:p') and pstyle(p) == 'Caption' and ptext(p).strip()]
figs = [c for c in caps if c.startswith('Figure')]; tabs = [c for c in caps if c.startswith('Table')]
lf, lt = front_list('Figures'), front_list('Tables')
def clean(x): return re.sub(r'\d+$', '', x).strip()
pass
lines += ['', '## Figures and tables', '', 'Figures: %d captions, %d list entries, word-for-word match: %s.' % (len(figs), len(lf), figs == lf),
          'Tables: %d captions, %d list entries, word-for-word match: %s.' % (len(tabs), len(lt), tabs == lt), '']
lines += ['| Caption |', '|---|'] + ['| %s |' % c for c in caps]
open(OUT + 'structure_map.md', 'w').write('\n'.join(lines) + '\n')
print('headings', len(heads), 'figs', len(figs), figs == lf, 'tabs', len(tabs), tabs == lt)
for i, st, t, w, lvl in heads:
    if lvl <= 2: print(lvl, t, w)
