"""Figure 2.17. Cape Town International's site: a schematic coloured by status (Table 2.14 of v15).
Source page: Infrastructure Report, Jul 2026, p102 (src/pg/irB-36.png). Statuses are Table 2.14's."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figlib import *

H = 1800
fig, ax = canvas(H)
COL = {'Full': RED, 'Under strain': AMBER, 'A strength': GREEN}
TXT = {'Full': WHITE, 'Under strain': INK, 'A strength': WHITE}

# Table 2.14, v15: component -> status
STATUS = {
    'Runway and slots': 'Full',
    'Taxiways and aircraft stands': 'Under strain',
    'International terminal': 'Under strain',
    'Domestic arrivals hall': 'Full',
    'Domestic departures hall': 'Under strain',
    'Roads, drop-off and parking': 'Under strain',
    'Airline network and routes': 'A strength',
}


def comp(x, y, w, h, name, lines=None, align='center', pad=70):
    """A component box in its status colour with its name (bold) and its status word under it."""
    st = STATUS[name]
    rbox(ax, x, y, w, h, COL[st], r=22, z=3)
    lines = lines or [name]
    n = len(lines)
    total = n * S_HEAD * 1.22 + S_AX * 1.3
    y0 = y + h / 2 - total / 2 + S_HEAD * 0.61
    tx = x + w / 2 if align == 'center' else x + pad
    for i, l in enumerate(lines):
        T(ax, tx, y0 + i * S_HEAD * 1.22, l, S_HEAD, TXT[st], True, ha=align)
    T(ax, tx, y0 + (n - 1) * S_HEAD * 1.22 + S_HEAD * 0.61 + S_AX * 0.85, st, S_AX, TXT[st], False, ha=align)


# legend, top left
lx = 80
T(ax, lx, 92, 'Status', S_AX, GREY)
lx += tw('Status', S_AX) + 50
for st in ('Full', 'Under strain', 'A strength'):
    rbox(ax, lx, 92 - 22, 44, 44, COL[st], r=9)
    T(ax, lx + 62, 92, st, S_AX, INK)
    lx += 62 + tw(st, S_AX) + 80

# site boundary
BX0, BY0, BX1, BY1 = 80, 200, 2560, 1500
rbox(ax, BX0, BY0, BX1 - BX0, BY1 - BY0, None, r=30, edge=GREY, lw=4, z=1, ls=(0, (6, 4)))
T(ax, BX1, 152, 'Site boundary', S_SMALL, GREY, ha='right')

IX0, IX1 = BX0 + 70, BX1 - 70          # inner edges
IW = IX1 - IX0
# runway
RY, RH = 270, 200
comp(IX0, RY, IW, RH, 'Runway and slots', align='left')
cx0 = IX0 + 70 + tw('Runway and slots', S_HEAD, True) + 110
ax.plot([cx0, IX1 - 90], [RY + RH / 2, RY + RH / 2], color=WHITE, lw=7, ls=(0, (5, 4)), zorder=5)
for k in range(4):                      # threshold bars at the far end
    rect(ax, IX1 - 70, RY + 34 + k * 36, 34, 22, WHITE, z=5)
# taxiways and stands
AY, AH = RY + RH + 40, 190
comp(IX0, AY, IW, AH, 'Taxiways and aircraft stands', align='left')
# terminals
TY, TH = AY + AH + 40, 470
gap = 40
tw3 = (IW - 2 * gap) / 3
comp(IX0, TY, tw3, TH, 'International terminal', ['International', 'terminal'])
comp(IX0 + tw3 + gap, TY, tw3, TH, 'Domestic departures hall', ['Domestic', 'departures hall'])
comp(IX0 + 2 * (tw3 + gap), TY, tw3, TH, 'Domestic arrivals hall', ['Domestic', 'arrivals hall'])
# roads
OY = TY + TH + 40
OH = BY1 - 70 - OY
comp(IX0, OY, IW, OH, 'Roads, drop-off and parking', align='left')

# airline network: a tag beside the site, tied to the runway
GX, GW = 2650, 480
comp(GX, RY - 20, GW, RH + 40, 'Airline network and routes', ['Airline network', 'and routes'])
arrow(ax, GX - 12, RY + RH / 2, IX1 + 24, RY + RH / 2, GREY, lw=6, head=30, z=6)

# the squeeze: a bracket at the right of the site, from the runway side to the road side
sx = GX + 90
line(ax, sx, AY + 10, sx, OY - 10, GREY, lw=4, z=2)
arrow(ax, sx, AY + 80, sx, AY + 6, GREY, lw=4, head=26)
arrow(ax, sx, OY - 80, sx, OY - 6, GREY, lw=4, head=26)
line(ax, BX1 + 16, AY + 6, sx, AY + 6, GREY, lw=4, z=2)
line(ax, BX1 + 16, OY - 6, sx, OY - 6, GREY, lw=4, z=2)
T(ax, sx + 36, (AY + OY) / 2, 'Boxed in', S_AX, GREY)

callout(ax, 'The site is boxed in between the runway and the roads, so the fix has to move the runway itself.', 80, 1580, maxw=2800)
save(fig, 'fig_2_17')
