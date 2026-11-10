import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figlib import *
# Figure 2.2. Three effects of tourism levers: a three-tier funnel, one line of example levers per tier.
# Terms, definitions and levers from Table A.12 of the report and its source line. Source page not available.
H = 1560
fig, ax = canvas(H)
cxm, wt, wb = 630, 1100, 520               # funnel centre x, top width, bottom width
yt, yb, g = 100, 1380, 46                  # funnel top, bottom, gap between tiers
th = (yb - yt - 2 * g) / 3
def wid(y): return wt + (wb - wt) * (y - yt) / (yb - yt)
tiers = [
    (CHAR, ['Structural demand', 'creation'], 'Expands total addressable demand',
     'Kenya, conservation-led wildlife product; Melbourne and Victoria, event-led demand'),
    (DCYAN, ['Demand activation', 'and acceleration'], 'Converts latent or constrained demand',
     'Chile, gateway-led air concentration; Kenya, Nairobi-led gateway diversification'),
    (CYAN, ['System and product', 'yield optimisation'], 'Raises value per traveller without increasing arrivals',
     'Valencia, institutionalised quality governance; New Zealand, demand-led route development'),
]
tx = 1380; tw_max = 3120 - tx
for i, (col, name, effect, ex) in enumerate(tiers):
    y0 = yt + i * (th + g); y1 = y0 + th; ym = (y0 + y1) / 2
    pts = [(cxm - wid(y0) / 2, y0), (cxm + wid(y0) / 2, y0), (cxm + wid(y1) / 2, y1), (cxm - wid(y1) / 2, y1)]
    ax.add_patch(Polygon(pts, closed=True, facecolor=col, edgecolor=col, linewidth=22, joinstyle='round', zorder=2))
    TL(ax, cxm, ym - (len(name) - 1) * S_HEAD * 0.65 + 2, name, S_HEAD, WHITE, True, ha='center')
    xe = cxm + wid(ym) / 2 + 11
    line(ax, xe + 22, ym, tx - 46, ym, GREY, lw=3.2, z=3)
    ax.add_patch(Circle((xe + 22, ym), 15, facecolor=WHITE, edgecolor=GREY, linewidth=3.2, zorder=4))
    exl = wrap(ex, tw_max, S_AX)
    block = S_HEAD * 1.3 + 22 + len(exl) * S_AX * 1.3
    ya = ym - block / 2 + S_HEAD * 0.65
    T(ax, tx, ya, effect, S_HEAD, INK, True)
    TL(ax, tx, ya + S_HEAD * 0.65 + 22 + S_AX * 0.65, exl, S_AX, INK)
foot(ax, 'The line under each effect gives example levers from the six comparator cases.')
save(fig, 'fig_2_02')
