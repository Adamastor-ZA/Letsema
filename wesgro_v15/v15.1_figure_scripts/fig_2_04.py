import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figlib import *
fig, ax = canvas(1800)
cats = ['Kenya', 'Egypt', 'Western Cape', 'Morocco', 'Rest of South Africa', 'Namibia']
vals = [1460, 970, 890, 630, 500, 250]
cols = [CYAN if c == 'Western Cape' else CHAR for c in cats]
hbars(ax, cats, vals, x0=640, y0=120, y1=1620, xmax_px=2150, colors=cols, fmt=lambda v: 'US$%s' % format(v, ','))
callout(ax, 'Egypt and Morocco draw 15.7m and 17.4m arrivals against the\nprovince\'s 1.4m, yet earn less per arrival than Kenya.', 1560, 1300)
foot(ax, 'Spend per international arrival, US$, 2024. Western Cape highlighted.')
save(fig, 'fig_2_04')
