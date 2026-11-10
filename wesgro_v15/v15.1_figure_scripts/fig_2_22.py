"""Figure 2.22. Tourism attractions across the province: the map raster embedded on Infrastructure Report p92
(src/pg/ir92img-003.png, 1233 x 942), scaled up, with the eight-category legend rebuilt beside it.
Legend colours are sampled from the dots on the raster; the two categories with no distinguishable dots on the
raster (adventure and outdoor, marinas and waterfront) take the colour of the deck's own key on p92."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figlib import *
import numpy as np
import matplotlib.colors as mc

H = 2000
SRC = os.path.join(HERE, 'src', 'pg', 'ir92img-003.png')
PAGE = os.path.join(HERE, 'src', 'pg', 'irB-26.png')

raw = Image.open(SRC).convert('RGB')
raw = raw.crop((2, 2, raw.size[0] - 2, raw.size[1] - 2))          # drop the 2 px screenshot edge
SC = 2.0
big = raw.resize((int(raw.size[0] * SC), int(raw.size[1] * SC)), Image.LANCZOS)

# sample the dot colours from the raster: median of the most saturated pixels in each hue band
a = np.asarray(raw).astype(float)
hsv = mc.rgb_to_hsv(a / 255.0)
Hh, Ss, Vv = hsv[..., 0] * 360, hsv[..., 1], hsv[..., 2]
vivid = (Ss > 0.6) & (Vv > 0.6)


def sample(lo, hi):
    m = vivid & ((Hh >= lo) & (Hh <= hi) if lo < hi else (Hh >= lo) | (Hh <= hi))
    px = a[m]; s = (Ss * Vv)[m]
    top = px[s >= np.percentile(s, 60)]
    return '#%02X%02X%02X' % tuple(int(round(v)) for v in np.median(top, 0)), int(m.sum())


def key_colour(y):
    """Colour of a key dot on the page render of p92 (2000 px wide), used where the raster shows no such dots."""
    pg = np.asarray(Image.open(PAGE).convert('RGB')).astype(float)
    return '#%02X%02X%02X' % tuple(int(round(v)) for v in np.median(pg[y - 4:y + 5, 1513:1522].reshape(-1, 3), 0))


CATS = [
    ('Cultural and heritage', sample(20, 35)[0]),
    ('Botanical gardens', sample(100, 150)[0]),
    ('Adventure and outdoor', key_colour(533)),
    ('Marinas and waterfront', key_colour(612)),
    ('Wine and agri-tourism', sample(170, 190)[0]),
    ('Night entertainment', sample(285, 310)[0]),
    ('Natural landscapes', sample(50, 65)[0]),
    ('National parks', sample(350, 10)[0]),
]
for c in CATS: print(c)

fig, ax = canvas(H)
X0, Y0 = 40, (H - big.size[1]) // 2
im = ax.imshow(np.asarray(big), extent=(X0, X0 + big.size[0], Y0 + big.size[1], Y0), interpolation='nearest', zorder=1, aspect='auto')
ax.set_xlim(0, W); ax.set_ylim(H, 0)
clip = FancyBboxPatch((X0 + 26, Y0 + 26), big.size[0] - 52, big.size[1] - 52, boxstyle='round,pad=26,rounding_size=26', transform=ax.transData, facecolor='none', edgecolor='none')
ax.add_patch(clip); im.set_clip_path(clip)
rbox(ax, X0, Y0, big.size[0], big.size[1], None, r=26, edge=GRID, lw=3, z=2)

# legend
LX = X0 + big.size[0] + 66
T(ax, LX, Y0 + 40, 'Attraction type', S_VAL, CHAR, True)
pitch = 88
for i, (name, col) in enumerate(CATS):
    yc = Y0 + 150 + i * pitch
    ax.add_patch(Circle((LX + 24, yc), 24, facecolor=col, edgecolor=CHAR, linewidth=2.5, zorder=5))
    T(ax, LX + 76, yc, name, S_AX, INK)

# callout: the finding the page states and v15 repeats in "Province-wide asset maps"
ctext = 'Attractions cluster\nalong three corridors,\nand variety falls off\nbeyond them.'
ch_ = S_CAL * 1.3 * 4 + 62
callout(ax, ctext, LX, Y0 + big.size[1] - ch_, w=W - 40 - LX)
save(fig, 'fig_2_22')
