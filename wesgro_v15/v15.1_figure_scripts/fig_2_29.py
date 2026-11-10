import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figlib import *
# Figure 2.29. The inclusion response: three boxes in sequence, then the pilot sequence. Concept level only.
H = 1500
fig, ax = canvas(H)
# ---- three boxes in sequence
boxes = [('1', ['A functioning', 'selling capability']),
         ('2', ['A connection to demand', 'the node already has']),
         ('3', ['Launch gates for safety,', 'access and a viable', 'operating model'])]
bw, bh, gap, y0 = 900, 400, 170, 100
for i, (n, lines) in enumerate(boxes):
    x = 80 + i * (bw + gap)
    rbox(ax, x, y0, bw, bh, FILL, r=18, z=2)
    rect(ax, x, y0 + 18, 16, bh - 36, CYAN, z=3)
    ax.add_patch(Circle((x + 120, y0 + bh / 2), 56, facecolor=CYAN, edgecolor='none', zorder=4))
    T(ax, x + 120, y0 + bh / 2 + 2, n, S_HEAD, WHITE, True, ha='center')
    TL(ax, x + 220, y0 + bh / 2 - (len(lines) - 1) * S_HEAD * 0.65, lines, S_HEAD, INK, True)
    if i < 2: arrow(ax, x + bw + 34, y0 + bh / 2, x + bw + gap - 34, y0 + bh / 2, GREY, lw=7, head=40)
# ---- link down to the pilot
arrow(ax, 1600, y0 + bh + 40, 1600, 690, GREY, lw=7, head=40)
T(ax, 1650, (y0 + bh + 40 + 690) / 2 - 6, 'A pilot tests the model', S_AX, GREY)
# ---- the pilot sequence
py, ph = 710, 690
rbox(ax, 80, py, 3040, ph, WHITE, r=18, edge=GRID, lw=3.2, z=2)
T(ax, 150, py + 90, 'The pilot sequence', S_HEAD, INK, True)
steps = [['Run in two or three', 'of the six profiled', 'communities'], ['Test the model'], ['Measure results'], ['Scale only once', 'thresholds are met']]
sw, sh, sg, sy = 640, 250, 120, py + 180
for i, lines in enumerate(steps):
    x = 150 + i * (sw + sg); last = i == len(steps) - 1
    rbox(ax, x, sy, sw, sh, CYAN if last else CHAR, r=16, z=3)
    TL(ax, x + sw / 2, sy + sh / 2 - (len(lines) - 1) * S_VAL * 0.65, lines, S_VAL, WHITE, True, ha='center')
    if not last: arrow(ax, x + sw + 22, sy + sh / 2, x + sw + sg - 22, sy + sh / 2, GREY, lw=7, head=40)
ty = sy + sh + 60
rbox(ax, 150, ty, 2920, 130, FILL, r=14, z=3)
T(ax, 190, ty + 65, 'Thresholds are agreed before launch and cover bookings, local spend, delivery and safety.', S_AX, INK)
save(fig, 'fig_2_29')
