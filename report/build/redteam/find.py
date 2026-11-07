"""Count occurrences of find strings across all content JSON strings. Usage: python3 find.py 'text' ['text' ...]"""
import json, glob, os, sys
C = os.path.join(os.path.dirname(__file__), '..', 'content')
def strings(x, path):
    if isinstance(x, str): yield path, x
    elif isinstance(x, list):
        for i, y in enumerate(x): yield from strings(y, f'{path}[{i}]')
    elif isinstance(x, dict):
        for k, v in x.items(): yield from strings(v, f'{path}.{k}')
def hits(needle):
    out = []
    for f in sorted(glob.glob(os.path.join(C, '*', '*.json'))):
        d = json.load(open(f))
        for p, s in strings(d, ''):
            n = s.count(needle)
            if n: out.append((os.path.relpath(f, C), p, n))
    return out
if __name__ == '__main__':
    for a in sys.argv[1:]:
        h = hits(a); tot = sum(x[2] for x in h)
        print(f'{tot}x  {a[:90]}'); [print('     ', x[0], x[1][:60]) for x in h]
