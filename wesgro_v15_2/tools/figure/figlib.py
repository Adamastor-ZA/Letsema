"""Shared style for the v15.1 report figures. Pixel coordinates: x 0..3200 left to right, y 0..H top to bottom.
Usage:
    from figlib import *
    fig, ax = canvas(1800)            # 3200 x 1800 px, white
    hbars(...), T(...), rbox(...), callout(...)
    save(fig, 'fig_2_04')             # writes fig/fig_2_04.png (full size) and fig/fig_2_04_s.png (one third size preview)
Never put a chart title, logo or slide title in the image. One callout per chart."""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, Polygon, FancyArrowPatch, Wedge, Arc, Ellipse
from matplotlib import font_manager as fm
from PIL import Image, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'fig')
REG = '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'
BLD = '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'
fm.fontManager.addfont(REG); fm.fontManager.addfont(BLD)
plt.rcParams['font.family'] = 'Liberation Sans'
W = 3200
DPI = 100
PX = 72.0 / DPI                       # font size in points for a size given in pixels
# colours (report palette)
CYAN, CHAR, LCYAN, DCYAN = '#00A3DA', '#4D4D4F', '#80D1EC', '#006E93'
INK, GREY, GRID, FILL, RULE = '#2B2B2D', '#6D6E71', '#DBDCDD', '#F5F6F7', '#E6E7E8'
PINK = '#C8305A'                      # only for a limit, date or target marker (dashed)
GREEN, AMBER, RED = '#4C9F70', '#E9A23B', '#C8443F'   # status colours, only where a rating is called for
WHITE = '#FFFFFF'
# type sizes in pixels on the 3200 px canvas (match the existing figures)
S_AX = 42      # axis and category labels, body labels (regular)
S_VAL = 44     # value labels at bar ends, series labels (bold)
S_CAL = 48     # callout sentence (bold)
S_SMALL = 36   # footnote line inside an image, minor annotations
S_HEAD = 52    # a card or box heading (bold)

def canvas(h=1800):
    fig = plt.figure(figsize=(W / DPI, h / DPI), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(h, 0); ax.axis('off')
    fig._h = h
    return fig, ax

def tw(s, size=S_AX, bold=False):
    """Rendered width of s in pixels."""
    return ImageFont.truetype(BLD if bold else REG, int(size)).getlength(s)

def wrap(s, maxw, size=S_AX, bold=False):
    """Greedy word wrap to a pixel width; returns a list of lines."""
    out = []
    for para in str(s).split('\n'):
        line = ''
        for w in para.split():
            t = (line + ' ' + w).strip()
            if tw(t, size, bold) <= maxw or not line: line = t
            else: out.append(line); line = w
        out.append(line)
    return out

def T(ax, x, y, s, size=S_AX, color=INK, bold=False, ha='left', va='center', z=10, **kw):
    """One line of text at pixel (x, y)."""
    return ax.text(x, y, s, fontsize=size * PX, color=color, fontweight='bold' if bold else 'normal', ha=ha, va=va, zorder=z, **kw)

def TL(ax, x, y, lines, size=S_AX, color=INK, bold=False, ha='left', lh=1.3, z=10):
    """Several lines; y is the centre of the first line. Returns y of the line after the last."""
    if isinstance(lines, str): lines = lines.split('\n')
    for i, l in enumerate(lines): T(ax, x, y + i * size * lh, l, size, color, bold, ha, 'center', z)
    return y + len(lines) * size * lh

def rbox(ax, x, y, w, h, fill=FILL, r=14, edge=None, lw=0, z=2, ls='-'):
    """Rounded rectangle with top-left corner (x, y)."""
    r = max(0, min(r, w / 3, h / 3))
    p = FancyBboxPatch((x + r, y + r), w - 2 * r, h - 2 * r, boxstyle='round,pad=%f,rounding_size=%f' % (r, r), linewidth=lw, edgecolor=edge or 'none', facecolor=fill if fill else 'none', zorder=z, linestyle=ls)
    ax.add_patch(p); return p

def rect(ax, x, y, w, h, fill, z=2):
    p = Rectangle((x, y), w, h, linewidth=0, facecolor=fill, zorder=z); ax.add_patch(p); return p

def line(ax, x0, y0, x1, y1, color=GRID, lw=2.8, ls='-', z=1):
    return ax.plot([x0, x1], [y0, y1], color=color, lw=lw, ls=ls, zorder=z, solid_capstyle='round')

def dashed(ax, x0, y0, x1, y1, color=PINK, lw=5.5, z=3):
    """The crimson dashed marker (limit, date or target only)."""
    return ax.plot([x0, x1], [y0, y1], color=color, lw=lw, ls=(0, (4, 3)), zorder=z)

def arrow(ax, x0, y0, x1, y1, color=GREY, lw=5, head=28, z=4):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle='-|>,head_length=%f,head_width=%f' % (head / 10, head / 16), mutation_scale=10, linewidth=lw, color=color, zorder=z, shrinkA=0, shrinkB=0))

def callout(ax, text, x, y, w=None, size=S_CAL, maxw=1500):
    """Pale grey box with a cyan left rule and one bold sentence. (x, y) is the top-left corner.
    text may hold '\\n'; otherwise it is wrapped to maxw. Returns (width, height)."""
    lines = text.split('\n') if '\n' in text else wrap(text, maxw, size, True)
    lh = size * 1.3; h = lh * len(lines) + 62
    if w is None: w = max(tw(l, size, True) for l in lines) + 52 + 60
    rbox(ax, x, y, w, h, FILL, r=12, z=20)
    rect(ax, x, y, 16, h, CYAN, z=21)
    for j, l in enumerate(lines): T(ax, x + 52, y + 31 + lh * (j + 0.5), l, size, CHAR, True, z=22)
    return w, h

def hbars(ax, cats, vals, x0, y0, y1, xmax_px, colors=None, fmt=lambda v: str(v), vmax=None, label_gap=32, bar_frac=0.66, size=S_AX):
    """Horizontal bars as in the existing figures: category label right-aligned at x0 - label_gap, bar from x0,
    bold value label at the bar end. Rows fill y0..y1. xmax_px is the pixel length of the largest bar."""
    n = len(cats); slot = (y1 - y0) / n; bh = slot * bar_frac; vmax = vmax or max(vals)
    for i, (c, v) in enumerate(zip(cats, vals)):
        yc = y0 + slot * (i + 0.5); L = xmax_px * v / vmax
        T(ax, x0 - label_gap, yc, c, size, INK, ha='right')
        rbox(ax, x0, yc - bh / 2, max(L, 6), bh, (colors[i] if colors else CHAR), r=14, z=3)
        T(ax, x0 + L + 24, yc, fmt(v), S_VAL, INK, True)

def foot(ax, s, h=None, x=80):
    """Small grey line at the bottom left of the image (use sparingly; the Note under the caption carries caveats)."""
    T(ax, x, (h or ax.figure._h) - 52, s, S_SMALL, GREY)

def save(fig, name):
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, name + '.png')
    fig.savefig(p, dpi=DPI, facecolor='white'); plt.close(fig)
    im = Image.open(p).convert('RGB'); assert im.size[0] == W, im.size
    im.resize((W // 3, im.size[1] // 3)).save(os.path.join(OUT, name + '_s.png'))
    print('saved', p, im.size); return p
