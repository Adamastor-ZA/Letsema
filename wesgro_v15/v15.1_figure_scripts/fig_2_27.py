"""Figure 2.27. Safety and service readiness in the 20 communities: a 20 x 6 heatmap.
Ratings: SME and Community Inclusion Plan, Sep 2026, p27 (src/scip/scip.txt, page 27; src/pg/scip-27.png).
Rows follow Table 2.21 of v15; names follow Table A.22. The script checks the safety perception column against
Table A.22 in d0.txt and the column counts against the note under Table A.22 before it draws."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figlib import *

COLS = ['Safety perception', 'Extortion', 'Energy supply', 'Water and sanitation', 'Coach access', 'Service delivery']
# rows in the order of Table 2.21, named as Table A.22 spells them
GROUPS = [
    ('Cape Metro', ['Langa', 'Khayelitsha', 'Gugulethu', 'Mitchells Plain', 'Atlantis']),
    ('Cape Winelands', ['Kayamandi', 'Mbekweni', 'Nkqubela']),
    ('Overberg', ['Genadendal', 'Zwelihle', 'Kassiesbaai']),
    ('Garden Route', ['Knysna northern townships', 'Thembalethu', 'De Rust']),
    ('West Coast', ['Laingville', 'Doringbaai', 'Elands Bay']),
    ('Central Karoo', ['Laingsburg (Bergsig)', 'Kwa-Mandlenkosi', 'Prince Albert North']),
]
SLIDE_NAME = {'Knysna northern townships': 'Knysna north'}      # the slide's shorter label for the same community

# ---- read the slide (p27) --------------------------------------------------------------------------------
page = open(os.path.join(HERE, 'src', 'scip', 'scip.txt'), encoding='utf-8', errors='replace').read().split('\f')[26]
assert 'SAFETY, EXTORTION AND THE ENABLING ENVIRONMENT' in page
RATING = {}
for _, names in GROUPS:
    for n in names:
        sn = SLIDE_NAME.get(n, n)
        row = [l for l in page.split('\n') if l.strip().startswith(sn + '  ')]
        assert len(row) == 1, (n, row)
        cells = re.findall(r'\b(Ready|Developing|Gap)\b', row[0][len(row[0]) - len(row[0].lstrip()) + len(sn):])[:6]
        assert len(cells) == 6, (n, cells)
        RATING[n] = cells

# ---- checks against v15 (d0.txt) ---------------------------------------------------------------------------
d0 = open(os.path.join(HERE, 'd0.txt'), encoding='utf-8').read().split('\n')
i0 = next(i for i, l in enumerate(d0) if 'Caption| Table A.22.' in l)
A22 = {}
for l in d0[i0:i0 + 40]:
    m = re.match(r'\s+r\d+: (.*)', l)
    if not m: continue
    c = [re.sub(r'^[0-9A-F]{8}:', '', x.strip()).replace('**', '') for x in m.group(1).split(' || ')]
    if len(c) == 7 and c[5] in ('Ready', 'Developing', 'Gap') and '(count)' not in c[0]:
        A22[c[0]] = c[5]
assert len(A22) == 20 and set(A22) == set(RATING), sorted(set(A22) ^ set(RATING))
diff = [(n, RATING[n][0], A22[n]) for n in RATING if RATING[n][0] != A22[n]]
print('safety perception, slide p27 against Table A.22: %d differences %s' % (len(diff), diff))
for n in RATING: RATING[n][0] = A22[n]                      # Table A.22 governs
count = lambda j, r: sum(1 for n in RATING if RATING[n][j] == r)
tally = [[count(j, r) for r in ('Ready', 'Developing', 'Gap')] for j in range(6)]
print('Ready, Developing, Gap by column:', dict(zip(COLS, tally)))
assert tally[0] == [2, 9, 9], tally[0]                      # Table A.22 count rows; text: nine safety-perception gaps
# note under Table A.22: extortion 10, 5, 5; energy 6, 14, 0; water and sanitation 1, 14, 5; coach 0, 20, 0; service 1, 14, 5
assert tally[1:] == [[10, 5, 5], [6, 14, 0], [1, 14, 5], [0, 20, 0], [1, 14, 5]], tally
# Table 2.21 order
i1 = next(i for i, l in enumerate(d0) if 'Caption| Table 2.21.' in l)
order = []
for l in d0[i1:i1 + 30]:
    m = re.match(r'\s+r\d+: (.*)', l)
    if m:
        c = [re.sub(r'^[0-9A-F]{8}:', '', x.strip()) for x in m.group(1).split(' || ')]
        if c[0] != 'Region': order.append((c[0], c[1]))
assert order == [(g, n) for g, names in GROUPS for n in names], order
print('row order equals Table 2.21; names equal Table A.22')

# ---- draw ------------------------------------------------------------------------------------------------
H = 2400
fig, ax = canvas(H)
COL = {'Ready': GREEN, 'Developing': AMBER, 'Gap': RED}
TXT = {'Ready': WHITE, 'Developing': INK, 'Gap': WHITE}
XR, XC, XG, XE = 80, 470, 1050, 3120            # region, community, first cell, right edge
GAP = 12
CW = (XE - XG - 5 * GAP) / 6
PITCH, CH, GG = 82, 70, 22

# legend
lx = XR
for r in ('Ready', 'Developing', 'Gap'):
    rbox(ax, lx, 80 - 22, 44, 44, COL[r], r=9)
    T(ax, lx + 62, 80, r, S_AX, INK)
    lx += 62 + tw(r, S_AX) + 80

# header
HY = 222
T(ax, XR, HY, 'Region', S_AX, CHAR, True)
T(ax, XC, HY, 'Community', S_AX, CHAR, True)
for j, c in enumerate(COLS):
    ls = wrap(c, CW - 20, S_AX, True)
    xc = XG + j * (CW + GAP) + CW / 2
    for k, l in enumerate(ls):
        T(ax, xc, HY - (len(ls) - 1) * S_AX * 0.62 + k * S_AX * 1.24, l, S_AX, CHAR, True, ha='center')
line(ax, XR, 290, XE, 290, CHAR, lw=3)

y = 312
for gi, (g, names) in enumerate(GROUPS):
    if gi:
        line(ax, XR, y + GG / 2 - 6, XE, y + GG / 2 - 6, GRID, lw=2.8)
        y += GG
    T(ax, XR, y + PITCH / 2, g, S_AX, CHAR, True)
    for n in names:
        yc = y + PITCH / 2
        T(ax, XC, yc, n, S_AX, INK)
        for j, r in enumerate(RATING[n]):
            x = XG + j * (CW + GAP)
            rbox(ax, x, yc - CH / 2, CW, CH, COL[r], r=12, z=3)
            T(ax, x + CW / 2, yc, r, 40, TXT[r], True, ha='center')
        y += PITCH
line(ax, XR, y + 4, XE, y + 4, CHAR, lw=3)

# gap count per column
yc = y + 4 + 58
T(ax, XR, yc, 'Communities rated Gap', S_AX, CHAR, True)
for j in range(6):
    T(ax, XG + j * (CW + GAP) + CW / 2, yc, '%d of 20' % tally[j][2], S_VAL, INK, True, ha='center')

callout(ax, 'Nine of the 20 communities record a safety-perception gap and five record extortion.', XR, yc + 96, maxw=2800)
save(fig, 'fig_2_27')
