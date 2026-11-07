"""Print blocks: python3 show.py file idx[-idx2] ..."""
import json, sys, os
C = os.path.join(os.path.dirname(__file__), '..', 'content')
args = sys.argv[1:]
f = args[0]
d = json.load(open(os.path.join(C, f)))
for a in args[1:]:
    lo, _, hi = a.partition('-')
    for i in range(int(lo), int(hi or lo) + 1):
        print(i, json.dumps(d['blocks'][i], ensure_ascii=False)); print()
