"""Classify a parenthetical as a citation and split it into the footnote text and any inline remainder.
Shared logic, mirrored in helpers.js (footnoteCitations). Used here to test the rules on the content."""
import re
MON = r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*'
FULL = re.compile(rf'^[A-Z][^;]*?,\s(?:\d{{1,2}}\s)?{MON}\s\d{{4}}\b')
FULL_YEAR = re.compile(r'^(?:City of Cape Town|Stats SA|Wesgro|Sernatur|Skift|UN Tourism|World Tourism Barometer|ACSA|Minister of Transport|George Herald|Western Cape Government|Singapore Tourism Board|Hypertext|Travel News)\b')
PAGE = re.compile(r'^pp?\d+(?:\s(?:to|and)\spp?\d+)?(?:,\s(?:pp?\d+(?:\s(?:to|and)\spp?\d+)?|computed))*$')
SECT = re.compile(r'^"[^"]+"(?:,\s"[^"]+")*$')
MOD = re.compile(r'^(?:computed|public source)$')
def classify(part, prev_full):
    p = part.strip()
    if FULL.match(p) or FULL_YEAR.match(p): return 'full'
    if PAGE.match(p): return 'page'
    if SECT.match(p): return 'sect'
    if MOD.match(p): return 'mod'
    if prev_full and re.match(r'^[A-Z][A-Za-z ]{2,40}$', p) and len(p.split()) <= 4: return 'sect'
    return 'other'
def doc_of(full):
    """'Demand-Side Analysis, Jun 2026, p21' -> 'Demand-Side Analysis, Jun 2026'"""
    m = re.match(rf'^(.*?,\s(?:\d{{1,2}}\s)?{MON}\s\d{{4}})', full)
    return m.group(1) if m else None
def parse(inner, last):
    """Return (footnote_text or None, inline_remainder or None, new_last)."""
    parts = [x.strip() for x in inner.split(';')]
    kinds = []; prev_full = False
    for p in parts:
        k = classify(p, prev_full); kinds.append(k); prev_full = k == 'full'
    if not any(k in ('full', 'page', 'sect') for k in kinds): return None, None, last
    fn, inl = [], []
    for p, k in zip(parts, kinds):
        if k == 'full':
            fn.append(p); d = doc_of(p); last = d or last
        elif k in ('page', 'sect'):
            if not last: return None, None, last
            fn.append(f'{last}, {p}')
        elif k == 'mod':
            if fn: fn[-1] += f', {p}'
            else: fn.append(p.capitalize())
        else: inl.append(p)
    return '; '.join(fn), ('; '.join(inl) if inl else None), last
