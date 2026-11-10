import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figlib import *
# Figure 2.5. Four traveller segments: typographic cards. All content from Table 2.4 of the report.
H = 1800
fig, ax = canvas(H)
S_HERO = 132
segs = [  # name, travellers, share %, what drives them, priority markets, named for regions and green season
    ('Curious\nExplorers', '30m', 31, 'Cultural immersion, learning and authentic connection', 'UK, USA', True),
    ('Creative\nConnectors', '25m', 26, 'Design, food and urban creativity', 'India', False),
    ('Discerning\nConnoisseurs', '19m', 20, 'Exclusivity, refinement and access', 'China, UAE', False),
    ('Reflective\nAdventurers', '23m', 23, 'Renewal and connection with nature', 'Germany', True),
]
cw, gap, y0, ch, hh, b = 730, 40, 90, 1400, 240, 5
for i, (name, n, pct, drives, mkts, mark) in enumerate(segs):
    x = 80 + i * (cw + gap); col = CYAN if mark else CHAR; px = x + 50; iw = cw - 100
    rbox(ax, x, y0, cw, ch, col, r=20, z=2)
    rbox(ax, x + b, y0 + hh, cw - 2 * b, ch - hh - b, WHITE, r=16, z=3)
    rect(ax, x + b, y0 + hh, cw - 2 * b, 40, WHITE, z=3)
    TL(ax, px, y0 + hh / 2 - S_HEAD * 0.65 + 2, name, S_HEAD, WHITE, True, z=5)
    y = y0 + hh + 130
    T(ax, px, y, n, S_HERO, INK, True)
    TL(ax, px + tw(n, S_HERO, True) + 30, y - 12, ['addressable', 'travellers'], S_AX, GREY, lh=1.2)
    y += 120
    rbox(ax, px, y, iw, 26, RULE, r=13, z=4)
    rbox(ax, px, y, iw * pct / 100, 26, col, r=13, z=5)
    T(ax, px, y + 78, '%d%% of the four segments' % pct, S_AX, INK)
    y += 170
    line(ax, px, y, px + iw, y, GRID, lw=2.8, z=4)
    T(ax, px, y + 70, 'What drives them', S_SMALL, GREY)
    TL(ax, px, y + 136, wrap(drives, iw, S_AX), S_AX, INK)
    y += 310
    line(ax, px, y, px + iw, y, GRID, lw=2.8, z=4)
    T(ax, px, y + 70, 'Priority markets', S_SMALL, GREY)
    T(ax, px, y + 140, mkts, S_VAL, INK, True)
    if mark:
        by = y0 + ch - 170
        rbox(ax, px, by, iw, 120, LCYAN, r=16, z=4)
        TL(ax, px + 32, by + 60 - S_SMALL * 0.65, ['For the regions and', 'the green season'], S_SMALL, INK, True)
callout(ax, 'The four segments hold about 97 million interested travellers.', 80, 1560)
save(fig, 'fig_2_05')
