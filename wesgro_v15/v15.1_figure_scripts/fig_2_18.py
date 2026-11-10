import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figlib import *
# Airport relief against 2035. Every date and value follows v15 (section "Runway and terminal capacity", Table 2.14).
# Only the bar start of the two terminal projects (2027.3 on the axis) is read from the Infrastructure Report p103.
H = 1700
fig, ax = canvas(H)
X26, X35 = 1050, 3000
def X(yr): return X26 + (yr - 2026) * (X35 - X26) / 9.0
GT, GB = 160, 1330                       # gridline top and bottom
for yr in range(2026, 2035):
    line(ax, X(yr), GT, X(yr), GB, GRID, 2.8)
    T(ax, X(yr), 100, str(yr), S_AX, GREY, ha='center')
dashed(ax, X(2035), GT - 20, X(2035), GB + 20)
T(ax, X(2035), 100, '2035', S_VAL, PINK, True, ha='center')
BH = 116
BB = dict(facecolor=WHITE, edgecolor='none', pad=10)   # white backing so gridlines do not run through text
def bar(y, a, b, col, label):
    rbox(ax, X(a), y - BH / 2, X(b) - X(a), BH, col, r=16, z=3)
    T(ax, X(b) - 30, y, label, S_VAL, WHITE, True, ha='right', z=6)
def left(y, name, lines):
    T(ax, 80, y - (len(lines) * 0.5) * S_AX * 1.3, name, S_VAL, INK, True)
    TL(ax, 80, y - (len(lines) * 0.5) * S_AX * 1.3 + 62, lines, S_AX, GREY)
# 1 Realigned runway
y1 = 450
bar(y1, 2027.0, 2033.0, CYAN, 'Done about 2033')
left(y1, 'Realigned runway', ['About R6.39bn'])
xd = X(2026 + 11.5 / 12)                 # December 2026
ax.add_patch(Circle((xd, y1 - BH / 2 - 86), 19, facecolor=CHAR, edgecolor='none', zorder=6))
T(ax, xd + 40, y1 - BH / 2 - 86, 'Contractor appointment planned for December 2026', S_AX, INK, bbox=BB)
ya = y1 + BH / 2 + 82                    # first text line of the upside labels
for xm, head, sub, ha in ((X(2029 + 11.5 / 12), 'Upside: December 2029', ['ACSA latest schedule,', 'subject to contract award'], 'right'),
                          (X(2031.0), 'Upside: 2031', ['ACSA, May 2025'], 'left')):
    line(ax, xm, y1, xm, ya - 2, CHAR, 3.2, z=5)
    ax.add_patch(Circle((xm, y1), 21, facecolor=WHITE, edgecolor=CHAR, linewidth=4.5, zorder=7))
    dx = -26 if ha == 'right' else 26
    bw = max([tw(head, S_VAL, True)] + [tw(l, S_AX) for l in sub]) + 28
    rbox(ax, (xm + dx - bw + 14) if ha == 'right' else (xm + dx - 14), ya - 34, bw, 60 + len(sub) * S_AX * 1.3 + 14, WHITE, r=10, z=2.5)
    T(ax, xm + dx, ya, head, S_VAL, INK, True, ha=ha)
    for k, l in enumerate(sub): T(ax, xm + dx, ya + 60 + k * S_AX * 1.3, l, S_AX, GREY, ha=ha)
# 2 International terminal upgrade
y2 = 870
bar(y2, 2027.3, 2032.0, CHAR, 'Done about 2032')
left(y2, 'International terminal upgrade', ['R863m'])
# 3 New domestic arrivals and departures (one project)
y3 = 1170
bar(y3, 2027.3, 2034.0, CHAR, 'Done about 2034')
left(y3, 'New domestic arrivals and departures', ['R2.39bn arrivals works and R500m', 'departures expansion from April 2027'])
callout(ax, 'The risk is timing, not scope, with relief landing between about 2032 and 2034.', X26, 1440, maxw=2400)
save(fig, 'fig_2_18')
