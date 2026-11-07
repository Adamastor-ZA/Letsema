"""Paragraph-level diff of draft v1 against draft v2 (the "change nothing else" test).

Reads every paragraph (body text and table cells) from the two .docx files, aligns them with difflib and maps each
changed paragraph to an edit in redteam/applied.json. Anything that maps to no edit is printed as UNEXPLAINED.
Contents and list-of-tables lines whose only change is a page number are counted separately.
Usage: python3 diff_v1_v2.py v1.docx v2.docx > report.txt
"""
import difflib, json, os, re, sys, zipfile

sys.path.insert(0, os.path.dirname(__file__))
from pages import norm  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def paras(docx):
    xml = zipfile.ZipFile(docx).read('word/document.xml').decode('utf8')
    out = []
    for p in re.findall(r'<w:p[ >].*?</w:p>', xml, re.S):
        t = ''.join(re.findall(r'<w:t(?: [^>]*)?>([^<]*)</w:t>', p))
        t = t.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&apos;', "'")
        if t.strip(): out.append(norm(t))
    return out


def parts(s):
    """Split a logged before/after value into its pieces (joined rows, joined paragraphs, JSON block lists)."""
    out = []
    if s.startswith('[') or s.startswith('{'):
        try:
            def walk(x):
                if isinstance(x, str): out.append(x)
                elif isinstance(x, list): [walk(y) for y in x]
                elif isinstance(x, dict): [walk(v) for k, v in x.items() if k != 'type']
            walk(json.loads(s)); return [norm(x) for x in out if x.strip()]
        except ValueError: pass
    return [norm(x) for x in re.split(r' \|\| | \| | / ', s) if x.strip()]


def hit(piece, para, other):
    if len(piece) <= 40: return piece == para or (len(piece) >= 12 and piece in para and piece not in other)
    w = piece.split(' ')
    for sn in (piece, ' '.join(w[:7]), ' '.join(w[-7:])):
        if sn in para and sn not in other: return True
    return False


def main():
    global log
    log = json.load(open(os.path.join(HERE, 'applied.json')))['log']
    v1, v2 = paras(sys.argv[1]), paras(sys.argv[2])
    sm = difflib.SequenceMatcher(a=v1, b=v2, autojunk=False)
    pagenum = re.compile(r'(\.{2,}|\s)\d{1,3}$')
    changed, unexplained, toc = [], [], 0


    def explain(old, new):
        ids = set()
        for e in log:
            if any(hit(pc, new, old) for pc in parts(e['after'])) or any(hit(pc, old, new) for pc in parts(e['before'])): ids.add(e['id'])
        return sorted(ids)


    for op, a0, a1, b0, b1 in sm.get_opcodes():
        if op == 'equal': continue
        olds, news = v1[a0:a1], v2[b0:b1]
        pairs = list(zip(olds, news)) + [(o, '') for o in olds[len(news):]] + [('', n) for n in news[len(olds):]]
        for old, new in pairs:
            if old and new and pagenum.sub('', old) == pagenum.sub('', new): toc += 1; continue
            ids = explain(old, new)
            if not ids:
                # a contents or list line whose caption text changed under an edit, with or without a new page number
                o2, n2 = pagenum.sub('', old), pagenum.sub('', new)
                ids = explain(o2, n2)
            rec = {'op': op, 'v1': old, 'v2': new, 'ids': ids}
            (changed if ids else unexplained).append(rec)

    print(f'v1 paragraphs {len(v1)}, v2 paragraphs {len(v2)}')
    print(f'changed paragraphs mapped to a change ID: {len(changed)}')
    print(f'contents or list lines with only a new page number: {toc}')
    print(f'UNEXPLAINED: {len(unexplained)}')
    for r in unexplained:
        print('---', r['op']); print('  v1:', r['v1'][:300]); print('  v2:', r['v2'][:300])
    json.dump({'changed': changed, 'unexplained': unexplained, 'toc_only': toc}, open(os.path.join(HERE, 'diff_v1_v2.json'), 'w'), indent=1, ensure_ascii=False)


if __name__ == '__main__':
    main()
