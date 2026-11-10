import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figlib import *
# Figure 2.14. Three layers of tourism supply: the weakest-layer logic only (Table 2.13 carries questions and categories).
# Placed at two-thirds width, so type is drawn 1.5 times the usual size to read at the same size as the other figures.
K = 1.5
H = 1560
fig, ax = canvas(H)
cx, cy = 300, 1470
clip = Rectangle((60, 0), 3100, cy, transform=ax.transData)
BANDS = [(1080, GRID), (780, CHAR), (470, CYAN)]
for r, col in BANDS:
    c = Circle((cx, cy), r, facecolor=col, edgecolor=WHITE, linewidth=8, zorder=2)
    ax.add_patch(c); c.set_clip_path(clip)
T(ax, 110, cy - 900, 'Enabling', 70, INK, True); T(ax, 110, cy - 815, 'infrastructure', 70, INK, True)
T(ax, 110, cy - 600, 'Services', 70, WHITE, True)
T(ax, 110, cy - 240, 'Attractions', 70, WHITE, True)
CX0, CW = 1470, 1650
callout(ax, 'The weakest layer limits how a\ndestination performs.', CX0, 70, w=CW, size=int(S_CAL * K))
CH = 330
rows = [
    (530, 1010, GRID, 'Enabling infrastructure', 'Poor access keeps visitors away'),
    (900, 900, CHAR, 'Services', 'Weak services shorten the\nstay and cut spend'),
    (1270, 720, CYAN, 'Attractions', 'Services and infrastructure without\nattractions draw too little demand'),
]
SV, SS = 62, 52
for yc, dx, col, layer, reading in rows:
    line(ax, dx, yc, CX0, yc, WHITE, lw=12, z=5)
    line(ax, dx, yc, CX0, yc, GREY, lw=4.5, z=6)
    ax.add_patch(Circle((dx, yc), 24, facecolor=WHITE, edgecolor=GREY, linewidth=4.5, zorder=7))
    rbox(ax, CX0, yc - CH / 2, CW, CH, WHITE, r=18, edge=GRID, lw=4.5, z=8)
    lines = reading.split('\n')
    block = SS * 1.3 + 20 + len(lines) * SV * 1.3
    y0 = yc - block / 2 + SS * 0.65
    rbox(ax, CX0 + 60, y0 - 24, 48, 48, col, r=10, edge=(GREY if col == GRID else None), lw=(3 if col == GRID else 0), z=9)
    T(ax, CX0 + 132, y0, layer, SS, GREY)
    for l in lines: assert tw(l, SV, True) < CW - 120, l
    TL(ax, CX0 + 60, y0 + SS * 0.65 + 20 + SV * 0.65, lines, SV, INK, True)
save(fig, 'fig_2_14')
