"""inline word diff of agent rewrites. usage: st_diff.py NAME [pid ...]"""
import sys, difflib
sys.path.insert(0, '/tmp/claude-0/-home-user-Letsema/98b96bfe-2843-55b4-9fb2-4f4083c56589/scratchpad/scripts')
from stp import *
d = Doc(); store = load_store(); E = json.load(open(WORK + 'edits_%s.json' % sys.argv[1]))
pids = sys.argv[2:] or list(E['rewrites'])
for pid in pids:
    old = store.get(pid, marked_plain(d.P(pid))).split(); new = E['rewrites'][pid].split()
    out = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, old, new, autojunk=False).get_opcodes():
        if tag == 'equal':
            seg = old[i1:i2]; out.append(' '.join(seg) if len(seg) <= 10 else ' '.join(seg[:5]) + ' … ' + ' '.join(seg[-5:]))
        else:
            if i2 > i1: out.append('[-' + ' '.join(old[i1:i2]) + '-]')
            if j2 > j1: out.append('{+' + ' '.join(new[j1:j2]) + '+}')
    print(pid, ' '.join(out)); print()
