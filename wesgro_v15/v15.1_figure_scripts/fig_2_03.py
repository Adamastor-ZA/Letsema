import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figlib import *
import math
# Figure 2.3. Three components of a growth system: the triangle, and the six comparators tagged with the
# system type exactly as Table 2.2 of the report prints it. Source page (Global Benchmarking Report) not available.
H = 1580
fig, ax = canvas(H)
A, B, C = (880, 190), (370, 1230), (1390, 1230)          # top, bottom left, bottom right
ax.add_patch(Polygon([A, B, C], closed=True, facecolor=FILL, edgecolor='none', zorder=1))
def edge(p, q, t0, t1):
    (x0, y0), (x1, y1) = p, q
    a = (x0 + (x1 - x0) * t0, y0 + (y1 - y0) * t0); b = (x0 + (x1 - x0) * t1, y0 + (y1 - y0) * t1)
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle='<|-|>,head_length=4.4,head_width=2.6', mutation_scale=10, linewidth=9, color=CYAN, zorder=3, shrinkA=0, shrinkB=0))
edge(A, B, 0.15, 0.82); edge(A, C, 0.15, 0.82); edge(B, C, 0.31, 0.69)
nodes = [(A, ['Institutional coordination'], 760, 150), (B, ['Strategic marketing', 'and promotion'], 580, 210), (C, ['Accessibility and', 'connectivity'], 580, 210)]
for (x, y), lines, w, h in nodes:
    rbox(ax, x - w / 2, y - h / 2, w, h, CHAR, r=22, z=5)
    TL(ax, x, y - (len(lines) - 1) * S_HEAD * 0.65 + 2, lines, S_HEAD, WHITE, True, ha='center')
gx, gy = 880, 840
TL(ax, gx, gy - 40, ['Sustained growth'], S_HEAD, INK, True, ha='center')
TL(ax, gx, gy + 40, ['three reinforcing', 'components'], S_AX, GREY, ha='center')
# ---- comparators and system types (Table 2.2, order and wording as printed)
rows = [('Chile', 'Connectivity-led'), ('Singapore', 'Orchestrated experience'), ('Kenya', 'Product-led'),
        ('Valencia', 'Governance-led'), ('New Zealand', 'Value-led'), ('Melbourne and Victoria', 'Events-led')]
lx, rx = 1900, 3120
T(ax, lx, 155, 'Comparator', S_AX, GREY); T(ax, rx, 155, 'System type', S_AX, GREY, ha='right')
y0, slot = 230, 180
for i, (name, typ) in enumerate(rows):
    y = y0 + i * slot
    line(ax, lx, y, rx, y, GRID, lw=2.8)
    T(ax, lx, y + slot / 2, name, S_VAL, INK, True)
    pw = tw(typ, S_VAL, True) + 80
    rbox(ax, rx - pw, y + slot / 2 - 52, pw, 104, LCYAN, r=34, z=3)
    T(ax, rx - pw / 2, y + slot / 2 + 2, typ, S_VAL, INK, True, ha='center')
line(ax, lx, y0 + 6 * slot, rx, y0 + 6 * slot, GRID, lw=2.8)
TL(ax, lx, y0 + 6 * slot + 80, ['All six align coordination, marketing and access, but each', 'builds its system around a different anchor.'], S_AX, GREY)
save(fig, 'fig_2_03')
