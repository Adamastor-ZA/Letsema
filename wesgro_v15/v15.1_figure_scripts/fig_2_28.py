"""Figure 2.28. The archetype matrix: the scatter raster embedded on SME and Community Inclusion Plan p17
(src/scip/img-003.png, 1650 x 990), scaled up, with the four quadrant labels in v15's wording and counts.
What is done to the raster, all in its native pixels before scaling:
  - the plot interior is cut out (frame, axis text and legend are redrawn in the report style);
  - the raster's own four quadrant captions (old wording) are painted out; under the top-left caption the two
    bubbles it crossed are repainted from their fitted circles;
  - two dotted reference lines with red text (town comparisons the slide itself masks, not in v15) are painted out;
  - 33 blank rows are added below the zero row, inside the frame, so the lower labels clear every bubble.
No data point is moved or hidden."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figlib import *
from PIL import ImageDraw
import numpy as np

H = 2000
SRC = os.path.join(HERE, 'src', 'scip', 'img-003.png')
raw = Image.open(SRC).convert('RGB')
a = np.asarray(raw).astype(int).copy()
hexc = lambda v: '#%02X%02X%02X' % tuple(int(round(x)) for x in v)
med = lambda x, y: np.median(a[y - 2:y + 3, x - 2:x + 3].reshape(-1, 3), 0)

# bubble colours sampled at clean bubble centres (before any edit)
REGIONS = [('Cape Metro', hexc(med(134, 376))), ('Cape Winelands', hexc(med(134, 416))), ('Overberg', hexc(med(317, 386))),
           ('Garden Route', hexc(med(1120, 434))), ('West Coast', hexc(med(1003, 580))), ('Central Karoo', hexc(med(949, 580)))]
print(REGIONS)
FX0, FX1, FY0, FY1 = 93, 1531, 24, 861          # plot interior in the raster (frame lines sit just outside)
XT = [(316.5, '2'), (558.5, '5'), (741.5, '10'), (924.5, '20'), (1138.5, '45'), (1321.5, '90'), (1503.5, '180')]
YT = [(81.5, '100'), (235.5, '30'), (372.5, '10'), (512.5, '3'), (690.5, '1'), (800.5, '0')]
VX, HYL = 1138.5, 701.5                         # the 45-minute line and the line between 0 and 1 attraction

# 1. dotted reference lines and their red text (rows 93..147)
sat = a.max(-1) - a.min(-1)
band = np.zeros(a.shape[:2], bool); band[93:148, FX0:FX1] = True
reddish = band & (a[..., 0] - np.maximum(a[..., 1], a[..., 2]) > 10)
dash_cols = np.zeros_like(band); dash_cols[:, 1136:1142] = True
for y, x in zip(*np.nonzero(reddish & dash_cols)):      # where a dotted line crossed the dashed 45-minute line
    a[y, x] = a[y - 11, x]                              # the dash pattern repeats every 11 rows
a[reddish & ~dash_cols] = 255
keep = np.zeros_like(band); keep[:, 1136:1142] = True; keep[:106, 618:681] = True     # dashed line; Mitchells Plain bubble
blue = (a[..., 2] - a[..., 0] > 15) & (a.sum(-1) < 600)                                                 # any bubble or label pixel
assert (blue[84:148, FX0:FX1] & ~keep[84:148, FX0:FX1]).sum() == 0                     # only compression fringe is wiped
wipe = np.zeros_like(band); wipe[84:148, FX0:FX1] = True
a[wipe & ~keep] = 255
pink = np.zeros_like(band); pink[96:106, 618:681] = True                                  # fringe of the dotted line under the bubble
a[pink & ((a[..., 0] - a[..., 2] > 3) | (a.sum(-1) > 700))] = 255

# 2. the raster's own quadrant captions (with an 8 px margin for compression fringe)
for (x0, y0, x1, y1) in [(157, 338, 464, 372), (1152, 338, 1480, 372), (FX0, 817, 1136, FY1), (1142, 817, FX1, FY1)]:
    assert (sat[y0:y1, x0:x1] > 30).sum() == 0, (x0, y0)
    a[y0:y1, x0:x1] = 255
# top-left caption start (x 116..156) crossed an Overberg dot and a Cape Metro bubble: repaint those from fitted circles
SS = 8
bx0, by0, bx1, by1 = 112, 336, 158, 368
syn = Image.new('RGB', ((bx1 - bx0) * SS, (by1 - by0) * SS), 'white')
d = ImageDraw.Draw(syn)
def disc(cx, cy, r, col):
    d.ellipse([(cx - r - bx0) * SS, (cy - r - by0) * SS, (cx + r - bx0) * SS, (cy + r - by0) * SS], fill=col)
disc(134.5, 350.3, 6.9, tuple(int(v) for v in med(317, 386)))        # Overberg dot (centre and radius fitted)
disc(134.46, 373.33, 17.6, (255, 255, 255))                          # the white rim matplotlib draws round a bubble
disc(134.46, 373.33, 17.08, (131, 145, 171))                         # Cape Metro bubble (fitted: r 17.08)
syn = np.asarray(syn.resize((bx1 - bx0, by1 - by0), Image.LANCZOS)).astype(int)
a[338:367, bx0:bx1] = syn[338 - by0:367 - by0]
clean = Image.fromarray(a.astype(np.uint8))

# 3. interior, with 33 blank rows (three dash periods) added at the bottom
EXT = 33
inner = clean.crop((FX0, FY0, FX1, FY1))
iw, ih = inner.size
ext = Image.new('RGB', (iw, ih + EXT), 'white')
ext.paste(inner, (0, 0))
ext.paste(inner.crop((0, ih - EXT, iw, ih)), (0, ih))
chk = np.asarray(ext).astype(int)
assert ((chk[ih - EXT:].max(-1) - chk[ih - EXT:].min(-1)) > 30).sum() == 0      # the copied rows hold no data
SC = 2.0
big = ext.resize((int(iw * SC), int((ih + EXT) * SC)), Image.LANCZOS)

fig, ax = canvas(H)
X0, Y0 = 236, 36
PW, PH = big.size
ax.imshow(np.asarray(big), extent=(X0, X0 + PW, Y0 + PH, Y0), interpolation='nearest', zorder=1, aspect='auto')
ax.set_xlim(0, W); ax.set_ylim(H, 0)
NX = lambda x: X0 + (x - FX0) * SC
NY = lambda y: Y0 + (y - FY0) * SC
# frame and ticks
ax.add_patch(Rectangle((X0, Y0), PW, PH, facecolor='none', edgecolor=GRID, linewidth=3.5, zorder=4))
for x, s in XT:
    line(ax, NX(x), Y0 + PH, NX(x), Y0 + PH + 14, GREY, lw=3, z=4)
    T(ax, NX(x), Y0 + PH + 46, s, S_AX, GREY, ha='center')
for y, s in YT:
    line(ax, X0 - 14, NY(y), X0, NY(y), GREY, lw=3, z=4)
    T(ax, X0 - 26, NY(y), s, S_AX, GREY, ha='right')
T(ax, X0 + PW / 2, Y0 + PH + 112, 'Minutes by road to the nearest tourism node or corridor (log scale, free-flow estimate)', S_AX, INK, ha='center')
T(ax, 62, Y0 + PH / 2, 'Mapped attractions inside the boundary (OpenStreetMap)', S_AX, INK, ha='center', rotation=90)

# quadrant labels, v15 wording and counts
def qlabel(x, y, name, counts):
    T(ax, x, y, name, S_VAL, CHAR, True, z=12)
    T(ax, x, y + 56, counts, S_AX, INK, z=12)

xl, xr = X0 + 44, NX(VX) + 40
yt, yb = Y0 + 62, Y0 + PH - 62 - 56
qlabel(xl, yt, 'Near a node, assets underused', '49 long-listed, 11 shortlisted')
qlabel(xr, yt, 'Remote, assets underused', '7 long-listed, 2 shortlisted')
qlabel(xl, yb, 'Near a node, nothing inside', '43 long-listed, 6 shortlisted')
qlabel(xr, yb, 'Remote, nothing inside', '8 long-listed, 1 shortlisted')

# callout, in the clear area right of Mitchells Plain (raster x 790..1125, y 30..235 holds no bubble or label)
big_a = np.asarray(big).astype(int)
cx, cy, cw = NX(812), NY(38), 610
ctext = 'The largest group,\n49 of the 107, sits\nnear a node and has\nsomething worth\nvisiting.'
ch = S_CAL * 1.3 * 5 + 62
sub = big_a[int(cy - Y0) - 10:int(cy - Y0 + ch) + 10, int(cx - X0) - 10:int(cx - X0 + cw) + 10]
assert (np.abs(sub - 255).sum(-1) > 60).sum() == 0, 'callout would cover marks'
callout(ax, ctext, cx, cy, w=cw)

# check that the quadrant labels sit on blank raster
for (x, y, s1, s2) in [(xl, yt, 'Near a node, assets underused', '49 long-listed, 11 shortlisted'), (xr, yt, 'Remote, assets underused', '7 long-listed, 2 shortlisted'),
                       (xl, yb, 'Near a node, nothing inside', '43 long-listed, 6 shortlisted'), (xr, yb, 'Remote, nothing inside', '8 long-listed, 1 shortlisted')]:
    wd = max(tw(s1, S_VAL, True), tw(s2, S_AX))
    sub = big_a[int(y - Y0 - 30):int(y - Y0 + 56 + 28), int(x - X0 - 8):int(x - X0 + wd + 8)]
    assert (np.abs(sub - 255).sum(-1) > 60).sum() == 0, ('label over marks', s1)
    assert x + wd < X0 + PW - 10

# legend
ly = Y0 + PH + 184
items = [(n, c) for n, c in REGIONS]
tot = sum(44 + 22 + tw(n, S_AX) for n, _ in items) + 70 * (len(items) - 1)
lx = X0 + PW / 2 - tot / 2
for n, c in items:
    ax.add_patch(Circle((lx + 22, ly), 22, facecolor=c, edgecolor='none', zorder=5))
    T(ax, lx + 66, ly, n, S_AX, INK)
    lx += 66 + tw(n, S_AX) + 70
save(fig, 'fig_2_28')
