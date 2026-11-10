import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figlib import *
# Addressable African markets: range bars, thousands of trips a year (lower, upper), ranked by upper estimate.
# Nigeria, Kenya and Ghana as v15 prints them; the other eight read from the vector bars on DSA p28 (axis 0 to 600).
data = [('Nigeria', 310, 510), ('Kenya', 240, 400), ('Zimbabwe', 180, 290), ('Botswana', 105, 175), ('Zambia', 95, 160),
        ('Mozambique', 65, 120), ('Tanzania', 65, 115), ('Ghana', 55, 100), ('Uganda', 30, 60), ('Ethiopia', 25, 50), ('Rwanda', 25, 50)]
PRI = ('Nigeria', 'Kenya', 'Ghana')
fig, ax = canvas(1800)
x0, x1, y0, y1 = 520, 2800, 70, 1480
px = (x1 - x0) / 600.0
for t in range(0, 601, 100):
    xx = x0 + t * px
    line(ax, xx, y0, xx, y1, GRID, 2.8)
    T(ax, xx, y1 + 58, format(t * 1000, ','), S_AX, GREY, ha='center')
n = len(data); slot = (y1 - y0) / n; bh = slot * 0.6
for i, (c, lo, hi) in enumerate(data):
    yc = y0 + slot * (i + 0.5)
    T(ax, x0 - 32, yc, c, S_AX, INK, ha='right')
    rbox(ax, x0 + lo * px, yc - bh / 2, (hi - lo) * px, bh, CYAN if c in PRI else CHAR, r=14, z=3)
    if c in PRI:
        T(ax, x0 + hi * px + 26, yc, '%s to %s' % (format(lo * 1000, ','), format(hi * 1000, ',')), S_VAL, INK, True, bbox=dict(facecolor=WHITE, edgecolor='none', pad=7))
callout(ax, 'Against those pools the visits are few: 7,256 Nigerian,\n10,152 Kenyan and 10,951 Ghanaian visitors.', 1380, 1150)
foot(ax, 'Modelled addressable adult leisure and business trips a year. Each bar spans the lower and upper estimate. Priority growth markets highlighted.')
save(fig, 'fig_2_12')
