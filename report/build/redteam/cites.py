"""List every parenthetical in body text (p, lead, note, quote, bullets, numbered, box paras) for citation analysis."""
import json, glob, os, re, collections
C = os.path.join(os.path.dirname(__file__), '..', 'content')
def texts(b):
    t = b.get('type')
    if t in ('p', 'lead', 'note', 'quote') and b.get('text'): yield b['text']
    if t in ('bullets', 'numbered'): yield from b['items']
    if t == 'box': yield from b.get('paras', [])
def parens(s):
    out, depth, start = [], 0, None
    for i, ch in enumerate(s):
        if ch == '(':
            if depth == 0: start = i
            depth += 1
        elif ch == ')' and depth:
            depth -= 1
            if depth == 0: out.append(s[start + 1:i])
    return out
allp = []
for f in sorted(glob.glob(os.path.join(C, '*', '*.json'))):
    for b in json.load(open(f))['blocks']:
        for s in texts(b): allp += parens(s)
print(len(allp), 'parentheticals')
for p in allp: print(p)
