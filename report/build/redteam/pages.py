"""Page lookup in a pdftotext -raw extract: which printed page carries a snippet of text."""
import re

_strip = re.compile(r'\*\*|\*(?=\S)|(?<=\S)\*')


def norm(s):
    s = _strip.sub('', s)
    s = s.replace('­', '').replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')
    return re.sub(r'\s+', ' ', s).strip()


def load(path):
    pages = open(path).read().split('\f')
    return [norm(p.replace('-\n', '-')) for p in pages]


def chunks(text):
    t = norm(text)
    if not t: return []
    out = [t]
    w = t.split(' ')
    for n in (14, 9, 6):
        if len(w) > n:
            out += [' '.join(w[:n]), ' '.join(w[-n:]), ' '.join(w[len(w) // 2 - n // 2: len(w) // 2 + n - n // 2])]
    return out


def page_of(text, pages, first_body=13):
    """Return sorted printed page numbers (1-based PDF pages) where the text, or a distinctive chunk of it, occurs.
    Body pages are searched first; front-matter lists (contents, figures, tables) only if nothing else matches."""
    for c in chunks(text):
        if len(c) < 18: continue
        hits = [i + 1 for i, p in enumerate(pages) if c in p]
        body = [h for h in hits if h >= first_body]
        if body: return body
        if hits: return hits
    return []
