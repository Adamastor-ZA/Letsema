"""Case-insensitive grep over content JSON strings with context. Usage: python3 grep.py pattern [pattern ...]"""
import json, glob, os, re, sys
C = os.path.join(os.path.dirname(__file__), '..', 'content')
def strings(x, path):
    if isinstance(x, str): yield path, x
    elif isinstance(x, list):
        for i, y in enumerate(x): yield from strings(y, f'{path}[{i}]')
    elif isinstance(x, dict):
        for k, v in x.items():
            if k == 'svg': continue
            yield from strings(v, f'{path}.{k}')
for pat in sys.argv[1:]:
    rx = re.compile(pat, re.I); n = 0
    out = []
    for f in sorted(glob.glob(os.path.join(C, '*', '*.json'))):
        d = json.load(open(f))
        for p, s in strings(d, ''):
            for m in rx.finditer(s):
                n += 1
                a, b = max(0, m.start() - 70), min(len(s), m.end() + 70)
                out.append(f'   {os.path.relpath(f, C)} {p[:28]}: ...{s[a:b]}...')
    print(f'== {pat}: {n}'); print('\n'.join(out))
