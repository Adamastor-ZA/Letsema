"""Figure 2.25. The 107 long-listed communities and the tourism corridors: the map raster embedded on
SME and Community Inclusion Plan p16 (src/scip/img-001.png, 1571 x 1129), scaled up, Cape Metro inset kept.
The raster's small legend is removed (the coast and the 'Mossel Bay' label it covered are restored) and a
larger legend is redrawn in the report style with colours sampled from the raster."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figlib import *
from PIL import ImageDraw
import numpy as np

H = 2400
SRC = os.path.join(HERE, 'src', 'scip', 'img-001.png')
raw = Image.open(SRC).convert('RGB')
a = np.asarray(raw).astype(int)
hexc = lambda v: '#%02X%02X%02X' % tuple(int(x) for x in v)

# colours sampled from the raster's own legend markers and marks
REGIONS = [('Cape Metro', hexc(a[991, 874])), ('Cape Winelands', hexc(a[1017, 874])), ('Overberg', hexc(a[1043, 874])),
       ('Garden Route', hexc(a[1069, 874])), ('West Coast', hexc(a[1095, 874])), ('Central Karoo', hexc(a[991, 1090]))]
C_STAR, C_CORR = hexc(a[1017, 1090]), hexc(a[1043, 1090])
ring = a[1055:1085, 1065:1095].reshape(-1, 3)
C_RING = hexc(ring[ring.sum(1).argmin()])
C_LAND, C_COAST, C_LABEL = hexc(a[700, 500]), '#8C8C8C', '#595959'
print(REGIONS, C_STAR, C_CORR, C_RING, C_LAND)

# 1. remove the raster's legend box (x 846..1394, y 950..1113) and restore what it covered
LB = (845, 949, 1396, 1115)
SS = 4
px0, py0 = LB[0], LB[1]
pw, ph = LB[2] - LB[0], LB[3] - LB[1]
patch = Image.new('RGB', (pw * SS, ph * SS), 'white')
d = ImageDraw.Draw(patch)
# coast traced from the de-blended legend corner (native pixel coordinates)
COAST = [(845, 990.8), (855.5, 989.7), (863, 987.5), (873, 985.5), (883, 982.7), (890.5, 978.7), (895, 975.6), (893, 972.5),
         (898, 970), (901.7, 968), (895.5, 965.6), (894, 962), (896, 957.5), (900.5, 953.7), (903.5, 949)]
q = [((x - px0) * SS, (y - py0) * SS) for x, y in COAST]
d.polygon([(0, 0)] + [((COAST[-1][0] - px0) * SS, 0)] + q[::-1], fill=C_LAND)
d.line(q, fill=C_COAST, width=int(1.6 * SS), joint='curve')
patch = patch.resize((pw, ph), Image.LANCZOS)
raw.paste(patch, (px0, py0))
# the place label the legend half covered, in the raster's own label size (10 pt at 100 dpi) and grey
ImageDraw.Draw(raw).text((953, 961), 'Mossel Bay', font=ImageFont.truetype(REG, 14), fill=C_LABEL, anchor='ls')

# 2. scale up
SC = 2.0
big = raw.resize((int(raw.size[0] * SC), int(raw.size[1] * SC)), Image.LANCZOS)
fig, ax = canvas(H)
X0, Y0 = (W - big.size[0]) // 2, (H - big.size[1]) // 2
ax.imshow(np.asarray(big), extent=(X0, X0 + big.size[0], Y0 + big.size[1], Y0), interpolation='nearest', zorder=1, aspect='auto')
ax.set_xlim(0, W); ax.set_ylim(H, 0)
N = lambda x, y: (X0 + x * SC, Y0 + y * SC)          # native raster pixel -> canvas pixel

# 3. legend, in the empty area north of the province (native x 330..1050, y 0..300 is blank)
lx, ly = N(352, 46)
pitch = 70
T(ax, lx, ly, 'Region', S_VAL, CHAR, True)
for i, (name, col) in enumerate(REGIONS):
    yc = ly + 86 + i * pitch
    ax.add_patch(Circle((lx + 22, yc), 22, facecolor=col, edgecolor='none', zorder=5))
    T(ax, lx + 70, yc, name, S_AX, INK)
kx = lx + 470
T(ax, kx, ly, 'Key', S_VAL, CHAR, True)
yc = ly + 86
ax.plot([kx + 30], [yc - 2], marker='*', markersize=58 * PX, markerfacecolor=C_STAR, markeredgecolor=INK, markeredgewidth=2.2, zorder=5)
T(ax, kx + 86, yc, 'Tourism node (35)', S_AX, INK)
yc += pitch
ax.plot([kx, kx + 60], [yc, yc], color=C_CORR, lw=9, zorder=5, solid_capstyle='round')
T(ax, kx + 86, yc, 'Corridor: N2, R62 and the Winelands roads', S_AX, INK)
yc += pitch
ax.add_patch(Circle((kx + 30, yc), 21, facecolor='none', edgecolor=C_RING, linewidth=4.5, zorder=5))
T(ax, kx + 86, yc, 'Shortlisted community (20), labelled', S_AX, INK)
yc += pitch
for r, dx in ((8, 8), (13, 27), (19, 53)):
    ax.add_patch(Circle((kx + dx, yc), r, facecolor=GREY, edgecolor='none', alpha=0.55, zorder=5))
T(ax, kx + 86, yc, 'Bubble size shows 2011 population', S_AX, INK)

# 4. callout, in the open water south-east of the coast
cx, cy = N(905, 1010)
callout(ax, '93 of the 107 lie within 45 minutes of one of 35\ntourism nodes or three corridors.', cx, cy)
save(fig, 'fig_2_25')
