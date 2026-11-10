"""Figure 2.20. Three cruise ports: a coastline schematic with a status card for each port.
Source page: Infrastructure Report, Jul 2026, p111 (src/pg/irB-45.png). Every status line is v15's
(section 2.4, "Cruise circuit and shore capacity"). The coastline is a hand-drawn schematic, not a basemap."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figlib import *

H = 1800
fig, ax = canvas(H)

# schematic projection: approximate longitude and latitude to pixels
def P(lon, lat):
    return 420 + (lon - 17.0) * 400, 70 + (-32.0 - lat) * 470

# approximate coastline, north-west to east (lon, lat)
COAST = [(18.30, -31.60), (18.33, -32.10), (18.28, -32.45), (18.10, -32.70), (17.87, -32.80), (17.90, -33.00),
         (18.05, -33.10), (18.18, -33.40), (18.42, -33.72), (18.44, -33.90), (18.33, -34.02), (18.38, -34.25),
         (18.48, -34.36), (18.50, -34.12), (18.72, -34.08), (18.83, -34.20), (18.82, -34.38), (19.10, -34.40),
         (19.28, -34.44), (19.33, -34.62), (19.65, -34.75), (20.00, -34.83), (20.45, -34.50), (20.85, -34.42),
         (21.40, -34.40), (21.80, -34.38), (22.10, -34.20), (22.25, -34.08), (22.60, -34.03), (23.05, -34.10),
         (23.40, -34.08), (23.75, -34.02), (24.10, -34.05)]
def smooth(q, n=2):
    """Chaikin corner cutting, so the schematic coast reads as one soft line."""
    for _ in range(n):
        o = [q[0]]
        for a, b in zip(q[:-1], q[1:]):
            o += [(0.75 * a[0] + 0.25 * b[0], 0.75 * a[1] + 0.25 * b[1]), (0.25 * a[0] + 0.75 * b[0], 0.25 * a[1] + 0.75 * b[1])]
        q = o + [q[-1]]
    return q

pts = smooth([P(*c) for c in COAST])
land = pts + [(W + 40, pts[-1][1]), (W + 40, -40), (pts[0][0], -40)]
ax.add_patch(Polygon(land, closed=True, facecolor=FILL, edgecolor='none', zorder=1))
ax.plot([p[0] for p in pts], [p[1] for p in pts], color=GRID, lw=7, zorder=2, solid_joinstyle='round', solid_capstyle='round')

SAL, CPT, MOS = P(17.93, -33.02), P(18.43, -33.91), P(22.14, -34.18)

# the two itineraries, offshore, dashed
def route(ll, label, lx, ly, ha='left'):
    q = [P(*c) for c in ll]
    q = smooth(q[:-1]) + [q[-1]]
    ax.plot([p[0] for p in q[:-1]], [p[1] for p in q[:-1]], color=DCYAN, lw=5, ls=(0, (4, 3)), zorder=3)
    arrow(ax, q[-2][0], q[-2][1], q[-1][0], q[-1][1], DCYAN, lw=5, head=30, z=3)
    T(ax, lx, ly, label, S_AX, DCYAN, ha=ha)

route([(18.30, -33.93), (18.02, -33.75), (17.62, -33.05), (17.50, -32.60), (17.50, -32.42), (17.50, -32.22)],
      'West coast itinerary', 110, 250)
route([(18.30, -33.98), (18.15, -34.20), (18.40, -34.55), (19.30, -34.85), (20.05, -35.02), (21.10, -34.70),
       (22.05, -34.36), (22.60, -34.30), (23.55, -34.32), (23.80, -34.32)],
      'East coast itinerary', P(23.80, -34.32)[0], P(23.80, -34.32)[1] + 66, ha='right')

# ports
def port(p, home=False):
    r = 34 if home else 26
    ax.add_patch(Circle(p, r + 9, facecolor=WHITE, edgecolor='none', zorder=6))
    ax.add_patch(Circle(p, r, facecolor=CYAN if home else CHAR, edgecolor='none', zorder=7))

port(SAL); port(CPT, True); port(MOS)

# status cards, on the land side
def card(x, y, w, name, tag, lines, home=False, anchor=None):
    lh = S_AX * 1.42
    h = 56 + S_HEAD + 30 + lh * len(lines) + 34
    rbox(ax, x, y, w, h, WHITE, r=18, edge=CYAN if home else GRID, lw=5 if home else 4, z=8)
    T(ax, x + 48, y + 56 + S_HEAD / 2 - 6, name, S_HEAD, CHAR, True, z=10)
    tx = x + 48 + tw(name, S_HEAD, True) + 34
    tgw = tw(tag, S_SMALL, True) + 44
    rbox(ax, tx, y + 56 + S_HEAD / 2 - 6 - 30, tgw, 60, CYAN if home else CHAR, r=30, z=9)
    T(ax, tx + tgw / 2, y + 56 + S_HEAD / 2 - 6, tag, S_SMALL, WHITE, True, ha='center', z=10)
    y0 = y + 56 + S_HEAD + 30 + lh / 2
    for i, l in enumerate(lines):
        if not l.startswith('  '):
            ax.add_patch(Circle((x + 60, y0 + i * lh), 8, facecolor=CYAN if home else GREY, edgecolor='none', zorder=10))
        T(ax, x + 92, y0 + i * lh, l.strip(), S_AX, INK, z=10)
    if anchor:
        (px, py), (cx, cy) = anchor
        line(ax, px, py, cx, cy, CYAN if home else CHAR, lw=4, z=5)
    return h

sal_lines = ['3 trial calls into an ore terminal', 'No cruise berth or passenger facility']
cpt_lines = ['One equipped berth', '150 or more calls a season', 'Ships up to 300m', 'South-Easter delays and no shore power']
mos_lines = ['21 calls and about 13,000 passengers', 'R22m passenger facility opened', '  in November 2025',
             'Ships anchor and tender', 'Small and mid-sized ships only']

def cw(lines):
    return 92 + max(tw(l.strip(), S_AX) for l in lines) + 56

card(1010, 330, cw(sal_lines), 'Saldanha Bay', 'West coast', sal_lines, anchor=(SAL, (1010, 470)))
card(1150, 700, cw(cpt_lines), 'Cape Town', 'Homeport', cpt_lines, home=True, anchor=(CPT, (1150, 880)))
mw = cw(mos_lines)
card(MOS[0] - mw / 2 + 120, 490, mw, 'Mossel Bay', 'East coast', mos_lines, anchor=(MOS, (MOS[0], 950)))

callout(ax, 'Protect Cape Town, back Mossel Bay now and watch Saldanha Bay.', 1370, 1590, maxw=2000)
foot(ax, 'Schematic, not to scale.')
save(fig, 'fig_2_20')
