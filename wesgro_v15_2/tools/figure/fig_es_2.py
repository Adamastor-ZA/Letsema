"""Figure ES.2. Strategic goals and objectives: the earlier tree structure, current wording."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figlib import *
TITLE = 'Accelerating tourism growth: towards 2.5 million international arrivals by 2035'
GOALS = [
 ('1 Reshape demand', 'More segments, markets, months and places',
  [('1.1 Traveller, brand and proposition', [(1, 'Respond to growth segment traveller preferences'), (2, 'Create green-season demand with MICE and events'), (3, 'Make the whole province findable and bookable')]),
   ('1.2 Source market growth', [(4, 'Convert India and China hub traffic'), (5, 'Increase yield in mature markets'), (6, 'Build a regional foundation (Africa)')])]),
 ('2 Transform supply', 'Seats, reach, product and experience',
  [('2.1 Access and infrastructure', [(7, 'Win direct routes and add seats on full routes'), (8, 'Grow cruise calls and ports'), (9, 'Accelerate tourism-enabling internal mobility')]),
   ('2.2 Product and capacity', [(10, 'Support diversified route and product development'), (11, 'Align visitor experience in-destination'), (12, 'Balance impact on nature-based attractions')])]),
 ('3 Build enabling capability', 'Inclusion, capital, governance and data',
  [('3.1 Inclusion and sustainability', [(13, 'Embed local destination bodies for community inclusion'), (14, 'Embed sustainable tourism and manage climate risk'), (15, 'Crowd in capital with targeted investment strategies')]),
   ('3.2 Governance and leadership', [(16, 'Align institutional stakeholders across all three tiers'), (17, 'Strengthen industry and government collaboration'), (18, 'Expedite tourism-enabling policy and data sharing'), (19, 'Lead removal of infrastructure, visa and safety deficits'), (20, 'Develop workforce and service skills')])]),
]
M = 80; GAP = 48; CW = (W - 2 * M - 2 * GAP) / 3
S_OBJ = 47; LH = 60; PAD = 26; NUMW = 104
def layout():
    cols = []
    for g in GOALS:
        y = 0; items = []
        for theme, objs in g[2]:
            items.append(('theme', theme, y, 84)); y += 84 + 20
            for n, t in objs:
                lines = wrap(t, CW - NUMW - 2 * PAD, S_OBJ)
                h = max(96, 2 * PAD + LH * len(lines))
                items.append(('obj', (n, lines), y, h)); y += h + 16
            y += 20
        cols.append((items, y))
    return cols
cols = layout()
top_title = 40; h_title = 128; top_goal = top_title + h_title + 40; h_goal = 200; top_body = top_goal + h_goal + 36
H = int(top_body + max(c[1] for c in cols) + 30)
fig, ax = canvas(H)
rbox(ax, M - 24, top_title, W - 2 * (M - 24), h_title, fill=CHAR, r=16)
T(ax, W / 2, top_title + h_title / 2, TITLE, size=56, color=WHITE, bold=True, ha='center')
for i, g in enumerate(GOALS):
    x = M + i * (CW + GAP)
    rbox(ax, x, top_goal, CW, h_goal, fill=DCYAN, r=16)
    T(ax, x + CW / 2, top_goal + 74, g[0], size=56, color=WHITE, bold=True, ha='center')
    T(ax, x + CW / 2, top_goal + 146, g[1], size=44, color=WHITE, ha='center')
    for kind, val, y, h in cols[i][0]:
        yy = top_body + y
        if kind == 'theme':
            rbox(ax, x, yy, CW, h, fill='#E6E7E8', r=10)
            T(ax, x + PAD, yy + h / 2, val, size=46, color=CHAR, bold=True)
        else:
            n, lines = val
            rbox(ax, x, yy, CW, h, fill=WHITE, r=10, edge='#C9CACC', lw=2.2)
            T(ax, x + PAD, yy + PAD + LH / 2, str(n), size=S_OBJ, color=INK, bold=True)
            for k, ln in enumerate(lines):
                T(ax, x + PAD + NUMW, yy + PAD + LH / 2 + k * LH, ln, size=S_OBJ, color=INK)
save(fig, 'fig_es_2')
