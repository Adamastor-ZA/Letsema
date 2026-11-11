import sys
sys.path.insert(0, '/tmp/claude-0/-home-user-Letsema/98b96bfe-2843-55b4-9fb2-4f4083c56589/scratchpad/scripts')
from stp import *
d = Doc(); store = {}
log = collections.Counter()
def sub(pat, rep, t, name, flags=0):
    n = len(re.findall(pat, t, flags))
    if n: log[name] += n
    return re.sub(pat, rep, t, flags=flags)
for it in walk(d):
    if it['sec'] in ('FRONT', 'COVER'): continue
    st = it['style']; t0 = marked_plain(it['p']); t = t0
    if not t.strip() or st.startswith('Heading') or st.startswith('TOC'): continue
    prose = st in PROSE
    # all text
    t = sub(r'\btoward\b', 'towards', t, 'toward')
    t = sub(r'\b([Bb])ase path\b', r'\1ase case', t, 'base path')
    t = sub(r'\b([Aa])ccelerated path\b', r'\1ccelerated case', t, 'accelerated path')
    t = sub(r'\b([Cc])onservative (path|floor)\b', r'\1onservative case', t, 'conservative path')
    t = sub(r'\b([Dd])irect foreign spend\b', lambda m: ('F' if m.group(1) == 'D' else 'f') + 'oreign direct spend', t, 'direct foreign spend')
    t = sub(r'\bthree spheres\b', 'three tiers', t, 'three spheres')
    t = sub(r'\bTurkiye\b', 'Turkey', t, 'Turkiye')
    t = sub(r'(\d)km\b', r'\1 km', t, 'km spacing')
    t = sub(r'\bPero\b', 'PERO', t, 'Pero')
    t = sub(r'\bCovid-era\b', 'pandemic-era', t, 'Covid')
    t = sub(r'\b(?:Covid|COVID)\b(?!-)', 'COVID-19', t, 'Covid')
    t = sub(r'\b(\d(?:\.\d+)?)M\b', r'\1 million', t, '1.8M')
    if st not in ('Caption', 'Source', 'Note'):
        t = sub(r'\bthe Province\b', 'the Western Cape Government', t, 'the Province')
    if prose:
        t = sub(r'((?:R|US\$|NZ\$|S\$|A\$|€)\d[\d,]*(?:\.\d+)?)bn\b', r'\1 billion', t, 'bn')
        t = sub(r'((?:R|US\$|NZ\$|S\$|A\$|€)\d[\d,]*(?:\.\d+)?)m\b', r'\1 million', t, 'money m')
        t = sub(r'(?<![\w$.,])(\d+\.\d+)m\b', r'\1 million', t, 'count m')
        t = sub(r'\bCTIA\b', 'Cape Town International', t, 'CTIA')
        t = sub(r'\blocal tourism (bodies|offices)\b', 'LTOs', t, 'local tourism bodies')
        t = sub(r'\blocal tourism (body|office)\b', 'LTO', t, 'local tourism bodies')
        t = sub(r'\bSCIP\b', 'Inclusion Plan', t, 'SCIP')
        t = sub(r'\bthe Winelands\b', 'the Cape Winelands', t, 'the Winelands')
        t = sub(r'\b11 of (the )?27\b', r'eleven of \g<1>27', t, 'eleven of 27')
        t = sub(r'(?<=[a-z,;:] )Objective (?=\d)', 'objective ', t, 'Objective N')
    if t != t0: store[it['pid']] = t
# Table 5.1 initiative names -> canonical
canon = {'I1 Segment-led activation and yield': 'I1 Segment-led activation and yield in mature markets', 'I2 Green-season events calendar': 'I2 Green-season events and business-events calendar',
 'I3 Findable province': 'I3 Findable province programme', 'I5 Regional Africa': 'I5 Regional Africa programme', 'I6 Route development and seat retention': 'I6 Route development and seat retention through Cape Town Air Access',
 'I10 Visitor experience and quality': 'I10 Visitor experience and quality standards', 'I15 Steerco and three-tier alignment': 'I15 Tourism Growth Steerco and three-tier alignment',
 'I16 Data sharing, intelligence and economic measures': 'I16 Data sharing, visitor intelligence and economic measures', 'I17 Access and safety escalation': 'I17 Access and safety escalation agenda',
 'I18 Labour analysis and skills plan': 'I18 Tourism labour analysis and skills plan'}
for it in walk(d):
    if it['table'] and it['sec'] == '5.1':
        t = store.get(it['pid'], marked_plain(it['p'])); bare = t.replace('*', '').strip()
        if bare in canon:
            store[it['pid']] = t.replace(bare, canon[bare]); log['Table 5.1 names'] += 1
save_store(store)
print(len(store), 'paragraphs changed'); print(dict(log))
