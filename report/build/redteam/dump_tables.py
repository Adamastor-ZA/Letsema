"""Dump target tables with neighbouring blocks. Usage: python3 dump_tables.py 'file:caption' ..."""
import json, os, sys
C = os.path.join(os.path.dirname(__file__), '..', 'content')
def short(b):
    if b is None: return '-'
    t = b.get('type')
    if t in ('p', 'lead', 'note', 'h2', 'h3', 'h4', 'kicker'): return f'[{t}] {b["text"]}'
    if t in ('bullets', 'numbered'): return f'[{t}] ' + ' || '.join(b['items'])
    if t == 'table': return f'[table] {b["caption"]}'
    return f'[{t}] {b.get("caption", "")}'
for arg in sys.argv[1:]:
    f, cap = arg.split(':', 1)
    bl = json.load(open(os.path.join(C, f)))['blocks']
    i = [k for k, b in enumerate(bl) if b['type'] == 'table' and b['caption'] == cap][0]
    b = bl[i]
    print(f'##### {f} b{i} :: {cap}')
    print('PREV:', short(bl[i - 1]) if i else '-')
    print('MSG:', b.get('message')); print('SRC:', b.get('source'))
    print('COLS:', [c['header'] for c in b['columns']])
    for r in b['rows']: print('  -', ' | '.join(map(str, r)))
    print('NEXT:', short(bl[i + 1]) if i + 1 < len(bl) else '-'); print()
