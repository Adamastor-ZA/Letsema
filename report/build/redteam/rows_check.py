"""Check every table/grid row renders: the first words of each row's first two cells must appear in the PDF text.
Usage: python3 rows_check.py qa/vN_raw.txt"""
import json, glob, os, re, sys
C = os.path.join(os.path.dirname(__file__), '..', 'content')
txt = open(sys.argv[1]).read()
norm = lambda s: re.sub(r'\s+', ' ', re.sub(r'[*\[\]]', '', s)).strip()
T = norm(txt.replace('-\n', '-'))
miss = []
for f in sorted(glob.glob(os.path.join(C, '*', '*.json'))):
    d = json.load(open(f))
    for bi, b in enumerate(d['blocks']):
        if b.get('type') not in ('table', 'grid'): continue
        for ri, r in enumerate(b['rows']):
            ok = True
            for cell in r[:3]:
                w = norm(str(cell)).split(' ')[:8]
                if not w or not w[0]: continue
                if ' '.join(w) not in T: ok = False
            if not ok: miss.append((os.path.relpath(f, C), bi, ri, str(r[0])[:50]))
for m in miss: print(*m)
print(len(miss), 'rows not found')
