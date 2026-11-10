import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figlib import *
import math
# Three airports: timing (x), impact (y, indicative) and scale (bubble area, indicative). Labels carry v15's values
# (section "Secondary gateways and airfields" and "Runway and terminal capacity"). Layout after Infrastructure Report p109.
H = 1800
fig, ax = canvas(H)
XL, XR, YT, YB = 430, 3040, 110, 1440
def X(yr): return XL + (yr - 2026) * (XR - XL) / 9.0
def Y(imp): return YB - imp * (YB - YT)
for yr in range(2026, 2036):
    if yr > 2026: line(ax, X(yr), YT, X(yr), YB, GRID, 2.8)
    T(ax, X(yr), YB + 58, str(yr), S_AX, GREY, ha='center')
line(ax, XL, YT, XL, YB, GREY, 3.2, z=2); line(ax, XL, YB, XR, YB, GREY, 3.2, z=2)
T(ax, (XL + XR) / 2, YB + 140, 'Timing of new capacity', S_AX, INK, ha='center')
T(ax, XL - 36, YT + 30, 'Higher', S_AX, GREY, ha='right')
T(ax, XL - 36, YB - 30, 'Lower', S_AX, GREY, ha='right')
T(ax, XL - 110, (YT + YB) / 2, 'Impact', S_AX, INK, ha='center', rotation=90)
K = 75.0                                  # radius in px = K * sqrt(million passengers a year)
def label(x, y, name, lines, ha='left'):
    """Bold name and regular lines on one white backing block, so gridlines do not run through the text."""
    w = max([tw(name, S_VAL, True)] + [tw(l, S_AX) for l in lines]) + 36
    h = 62 + len(lines) * S_AX * 1.3 + 16
    rbox(ax, (x - 18) if ha == 'left' else (x - w / 2), y - 36, w, h, WHITE, r=10, z=5)
    T(ax, x, y, name, S_VAL, INK, True, ha=ha)
    for k, l in enumerate(lines): T(ax, x, y + 62 + k * S_AX * 1.3, l, S_AX, INK, ha=ha)
# Cape Winelands: scenario, drawn dashed (first passengers targeted for 2028; terminal designed for 5.2 million)
xw, yw, rw = X(2028), Y(0.66), K * math.sqrt(5.2)
ax.add_patch(Circle((xw, yw), rw, facecolor=FILL, edgecolor=CHAR, linewidth=6, linestyle=(0, (3.2, 2.4)), zorder=4))
label(xw + rw + 44, yw - 96, 'Cape Winelands (scenario)', ['First passengers targeted for 2028', 'R8bn first phase', 'Terminal designed for 5.2 million'])
# George: about 2 million by 2028 or 2029
xg, yg, rg = X(2028.5), Y(0.17), K * math.sqrt(2.0)
ax.add_patch(Circle((xg, yg), rg, facecolor=CHAR, edgecolor='none', zorder=4))
label(xg + rg + 44, yg - 124, 'George', ['911,000 passengers in 2025', 'R310m expansion to about 2 million', 'by 2028 or 2029', 'Domestic only'])
# Cape Town International: about 11.1 million passengers in 2025; runway relief about 2033
xc, yc, rc = X(2033), Y(0.74), K * math.sqrt(11.1)
ax.add_patch(Circle((xc, yc), rc, facecolor=CYAN, edgecolor='none', zorder=4))
label(xc, yc + rc + 70, 'Cape Town International', ['About 11.1 million passengers in 2025', 'Runway relief about 2033'], ha='center')
callout(ax, 'The certain fix comes last,\nand the earliest large option\nis the least certain.', 2130, 1070)
foot(ax, 'Bubble area: about 2 million, 5.2 million and 11.1 million passengers a year. Dashed outline: a scenario, not committed capacity.')
save(fig, 'fig_2_19')
