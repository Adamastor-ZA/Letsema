"""usage: st_dump.py NAME SEC[,SEC...]  -> work/dump_NAME.txt and work/dups_NAME.txt"""
import sys
sys.path.insert(0, '/tmp/claude-0/-home-user-Letsema/98b96bfe-2843-55b4-9fb2-4f4083c56589/scratchpad/s16')
from stp import *
name, secs = sys.argv[1], set(sys.argv[2].split(','))
d = Doc(); store = load_store()
n = dump(d, store, secs, WORK + 'dump_%s.txt' % name)
# duplicates: sentences in these sections that also appear (exactly or nearly) in another section
def norm(s): return re.sub(r'\W+', ' ', s.lower()).strip()
def sh(n):
    w = n.split(); return {' '.join(w[i:i+5]) for i in range(len(w)-4)}
S_ = []
order = ['1.0','1.1','1.2','1.3','1.4','2.0','2.1','2.2','2.3','2.4','2.5','3.0','3.1','3.2','3.3','3.4','4.0','4.1','4.2','4.3','4.4','4.5','4.6','4.7','4.8','5.0','5.1','5.2','5.3','5.4','5.5','5.6','5.7','A0','A1','A2','A3','A4','A5','A6','A7','A8','A9']
for it in walk(d):
    if it['table'] or it['style'] not in ('Body', 'Lead', 'BoxBody') or it['sec'] not in order: continue
    for s in sents(cur(it, store)):
        if len(s.split()) >= 8: S_.append((it['sec'], it['pid'], s, sh(norm(s))))
idx = collections.defaultdict(set)
for i, x in enumerate(S_):
    for g in x[3]: idx[g].add(i)
out = []
for i, (sec, pid, s, g) in enumerate(S_):
    if sec not in secs or not g: continue
    c = collections.Counter()
    for x in g:
        for j in idx[x]:
            if j != i and S_[j][0] != sec: c[j] += 1
    for j, k in c.items():
        if k / len(g | S_[j][3]) >= 0.6:
            home = min(sec, S_[j][0], key=order.index)
            out.append('[%s] in %s: "%s"\n    also in %s [%s]. Home copy: %s. %s' % (pid, sec, s, S_[j][0], S_[j][1], home,
                       'KEEP yours.' if home == sec else 'Yours is the repeat: cut it or reduce it to the figure plus "(section %s)", in different words.' % home))
open(WORK + 'dups_%s.txt' % name, 'w').write('\n'.join(out) + '\n')
print(name, n, 'lines;', len(out), 'duplicate notes')
