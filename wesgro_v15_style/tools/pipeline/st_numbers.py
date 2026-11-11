import sys, re, json, csv
from collections import defaultdict, OrderedDict
sys.path.insert(0, '/tmp/claude-0/-home-user-Letsema/98b96bfe-2843-55b4-9fb2-4f4083c56589/scratchpad/scripts')
from dxst import *
OUT = '/home/user/Letsema/wesgro_v15_style/output/'
d = Doc(); kids = list(d.body)
# walk body: track H1/H2 section; yield (section, kind, text, footnote text)
sec1 = sec2 = ''
units = []
def fn_of(p): return '; '.join(d.fn_text(i).strip() for i in fn_ids(p))
for el in kids:
    if el.tag == q('w:p'):
        st = pstyle(el); t = ptext(el).strip()
        if st in ('Heading1', 'Heading1Front'): sec1 = t; sec2 = ''; continue
        if st == 'Heading2': sec2 = t; continue
        if st in ('TOCL1', 'TOCL2', 'Heading3', 'Heading4', 'Kicker') or not t: continue
        units.append((sec1, sec2, 'text' if st in ('Body', 'Lead', 'BoxBody', 'Note') else st.lower(), t, fn_of(el)))
    elif el.tag == q('w:tbl'):
        for tr in el.findall(q('w:tr')):
            row = ' | '.join(' '.join(ptext(p).strip() for p in tc.findall(q('w:p'))) for tc in tr.findall(q('w:tc')))
            if row.strip(): units.append((sec1, sec2, 'table', row, ''))
FRONT = ('Foreword', 'Contents', 'Figures', 'Tables', 'Abbreviations')
units = [u for u in units if u[0] not in FRONT]
NUM = re.compile(r'(?<![\w.,/-])(?P<pre>about |over |under |almost |nearly |more than |fewer than |roughly |some )?(?P<cur>R|US\$|A\$|NZ\$|S\$|\$|£|€)?(?P<num>\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+\.\d+|\d+)(?P<suf>%| ?bn\b| billion\b| ?m\b| million\b|M\b| ?km\b| ?m\b| nights\b| days\b| minutes\b| percentage points\b)?')
def canon(m):
    num = float(m.group('num').replace(',', '')); suf = (m.group('suf') or '').strip(); cur = m.group('cur') or ''
    mult = {'bn': 1e9, 'billion': 1e9, 'm': 1e6, 'million': 1e6, 'M': 1e6}.get(suf, 1)
    unit = cur + ('%' if suf == '%' else (' ' + suf if suf in ('km', 'nights', 'days', 'minutes', 'percentage points') else ''))
    if suf == 'm' and not cur and num > 50 and '.' not in m.group('num'): mult = 1; unit = ' m (length)'
    v = num * mult
    return (unit.strip() or 'count'), v
found = defaultdict(list)
for s1, s2, kind, t, fn in units:
    for m in NUM.finditer(t):
        raw = m.group(0).strip(); suf = (m.group('suf') or '').strip(); cur = m.group('cur') or ''
        numtxt = m.group('num')
        nxt = t[m.end():m.end() + 14]; prv = t[max(0, m.start() - 14):m.start()]
        if not cur and not suf:
            v = float(numtxt.replace(',', ''))
            if ',' not in numtxt and '.' not in numtxt and v < 100: continue          # small bare integers
            if ',' not in numtxt and 1990 <= v <= 2040: continue                      # years
            if re.search(r'(p|slide|section|Table|Figure|clause|I|T\d-|objective|Objective|FY|Circular No\.|Gazette|Phase|Tier|Goal|No\.)\s?$', prv): continue
            if re.match(r'^(/\d\d)', nxt): continue
        if re.search(r'\bp$|p\d*$', prv.strip()) and not cur and not suf: continue
        unit, v = canon(m)
        found[(unit, round(v, 6))].append((s1, s2, kind, raw, t, fn, m.start()))
rows = []
def period(t, pos):
    seg = t[max(0, pos - 160):pos + 160]
    ys = re.findall(r'\b(?:FY\d{2,4}/\d{2}|FY\d{4}|20\d\d/\d\d|(?:19|20)\d\d(?: to (?:19|20)\d\d)?)\b', seg)
    return '; '.join(OrderedDict.fromkeys(ys))[:60]
n = 0
for (unit, v), occ in sorted(found.items(), key=lambda kv: (-len(set((o[0], o[1]) for o in kv[1])), kv[0][0], kv[0][1])):
    secs = OrderedDict.fromkeys(('%s %s' % (o[0][:14], o[1].split(' ')[0] if o[1] else '')).strip() for o in occ)
    places = set((o[0], o[1]) for o in occ)
    forms = OrderedDict.fromkeys(o[3] for o in occ)
    big = unit != 'count' or v >= 1000
    if len(places) < 2 or not big: continue
    if unit == '%' and v in (100.0,) : continue
    n += 1
    first = occ[0]; ctx = first[4][max(0, first[6] - 70):first[6] + 90].replace('\n', ' ')
    srcs = OrderedDict.fromkeys(o[5] for o in occ if o[5])
    rows.append(['A%03d' % n, ' / '.join(forms), ('%g' % v) if v < 1e15 else str(v), unit, period(first[4], first[6]), ' || '.join(list(srcs)[:2])[:300],
                 '%d places: %s' % (len(occ), '; '.join(list(secs)[:12])), ('FORMAT VARIANTS (%d). ' % len(forms) if len(set(f.lstrip('about over under almost nearly more than fewer roughly some ') for f in forms)) > 1 else '') + 'Context: …' + ctx + '…'])
json.dump(rows, open('numbers_auto.json', 'w'))
print('distinct values', len(found), 'auto register rows', len(rows))
print(sum(1 for r in rows if r[7].startswith('FORMAT')), 'with format variants')
for r in rows[:12]: print(r[0], '|', r[1][:60], '|', r[3], '|', r[6][:90])
