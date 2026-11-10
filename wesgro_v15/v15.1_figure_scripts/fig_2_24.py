import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figlib import *
# Figure 2.24. Resident share against spend share. Two panels: shares on one scale (left), rand a year (right).
H = 1800
fig, ax = canvas(H)
# ---- left panel: three shares on one scale
T(ax, 80, 140, 'Share of the province held or received by the 20 communities', S_AX, GREY)
x0, full = 640, 700                      # 18.4% is drawn 700 px long
rows = [('Residents', 18.4, '18.4%', CHAR), ('Employed residents', 15.4, '15.4%', CHAR), ('Foreign direct spend\nreceived', 0.04, '0.02% to 0.04%', CYAN)]
ys = [430, 760, 1090]; bh = 210
line(ax, x0, ys[0] - bh / 2 - 40, x0, ys[-1] + bh / 2 + 40, GRID, lw=2.8, z=1)
for (lab, v, txt, col), yc in zip(rows, ys):
    L = max(full * v / 18.4, 8)
    ll = lab.split('\n'); TL(ax, x0 - 32, yc - (len(ll) - 1) * S_AX * 0.65, ll, S_AX, INK, ha='right')
    rbox(ax, x0, yc - bh / 2, L, bh, col, r=14, z=3)
    T(ax, x0 + L + 24, yc - (30 if v < 1 else 0), txt, S_VAL, INK, True)
    if v < 1: T(ax, x0 + L + 24, yc + 30, 'too small to draw to scale', S_SMALL, GREY)
line(ax, 1600, 110, 1600, 1430, RULE, lw=2.8)
# ---- right panel: rand a year
T(ax, 1700, 140, 'Documented spend and two reference points, R million a year', S_AX, GREY)
yb, yt, vmax = 1260, 300, 600
gx0, gx1 = 1850, 3120
for v in (0, 200, 400, 600):
    y = yb - (yb - yt) * v / vmax
    line(ax, gx0, y, gx1, y, GRID, lw=2.8)
    T(ax, gx0 - 26, y, str(v), S_AX, GREY, ha='right')
bars = [(2090, 10, 'R4m to R10m', CYAN, ['Documented floor', '(drawn at R10m)']),
        (2500, 259, 'R259m', CHAR, ['1% of FY2025', 'foreign direct spend']),
        (2910, 547, 'R547m', CHAR, ['1% of the 2035', 'spend ambition'])]
bw = 260
for xc, v, txt, col, lab in bars:
    hgt = (yb - yt) * v / vmax
    rbox(ax, xc - bw / 2, yb - hgt, bw, hgt, col, r=14, z=3)
    T(ax, xc, yb - hgt - 40, txt, S_VAL, INK, True, ha='center')
    TL(ax, xc, yb + 62, lab, S_AX, GREY, ha='center')
callout(ax, 'The 20 communities hold 18.4% of residents yet receive 0.02% to 0.04% of foreign direct spend.', 80, 1540, maxw=2950)
save(fig, 'fig_2_24')
