import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figlib import *
import numpy as np
from mapdata_2_10 import LAND, WATER
# India and China reach Cape Town through hubs: schematic flow map. Volumes and headline figures as v15 prints them
# ("Path to purchase by market"; "China: discovery, booking and access"; "India: discovery, booking and access").
# Coastlines are hand-drawn and approximate (mapdata_2_10.py); routes are drawn as curves for legibility, not as flight paths.
H = 2000
fig, ax = canvas(H)
S, LON0, LAT0 = 24.0, -6.0, 42.0
def P(lon, lat): return np.array([(lon - LON0) * S, (LAT0 - lat) * S])
for poly in LAND: ax.add_patch(Polygon([P(*q) for q in poly], closed=True, facecolor=RULE, edgecolor=RULE, linewidth=1.5, joinstyle='round', zorder=1))
for poly in WATER: ax.add_patch(Polygon([P(*q) for q in poly], closed=True, facecolor=WHITE, edgecolor='none', zorder=1.1))
CPT, JNB, ADD, DOH, DXB, SIN = P(18.4, -33.9), P(28.2, -26.1), P(38.8, 9.0), P(51.5, 25.3), P(55.3, 25.25), P(103.9, 1.35)
IND = {'Addis Ababa': 30184, 'Dubai': 28621, 'Doha': 8660, 'Johannesburg': 1099}
CHN = {'Dubai': 8593, 'Addis Ababa': 6853, 'Singapore': 6728, 'Doha': 5398, 'Johannesburg': 1443}
assert sum(IND.values()) == 68564 and sum(CHN.values()) == 29015
PXK = 1.0                                   # line weight: px per 1,000 travellers
def wd(v): return max(4.0, v / 1000.0 * PXK)
zc = [3.0]
def bez(p0, c, p2, n=90):
    t = np.linspace(0, 1, n)[:, None]
    return (1 - t) ** 2 * np.array(p0) + 2 * t * (1 - t) * np.array(c) + t ** 2 * np.array(p2)
def offs(pts, d):
    g = np.gradient(pts, axis=0); nrm = np.stack([-g[:, 1], g[:, 0]], axis=1); nrm /= np.linalg.norm(nrm, axis=1)[:, None]
    return pts + nrm * d
def stroke(pts, w, col, casing=True):
    zc[0] += 0.01
    if casing: ax.plot(pts[:, 0], pts[:, 1], color=WHITE, lw=(w + 12) * 0.72, zorder=zc[0], solid_capstyle='butt', solid_joinstyle='round')
    zc[0] += 0.01
    ax.plot(pts[:, 0], pts[:, 1], color=col, lw=w * 0.72, zorder=zc[0], solid_capstyle='butt', solid_joinstyle='round')
def leg(pts, vi, vc):
    """Hub to Cape Town: India (cyan) and China (charcoal) side by side."""
    wi, wc = (wd(vi) if vi else 0), (wd(vc) if vc else 0)
    zc[0] += 0.01
    ax.plot(pts[:, 0], pts[:, 1], color=WHITE, lw=(wi + wc + 12) * 0.72, zorder=zc[0], solid_capstyle='butt')
    if wi: stroke(offs(pts, -wc / 2.0), wi, CYAN, False)
    if wc: stroke(offs(pts, wi / 2.0), wc, CHAR, False)
# origin boxes
IB = (1950, 470, 350, 204); CB = (2650, 150, 350, 204)
# 1 hub to Cape Town legs
leg(bez(SIN, (1500, 1900), CPT), 0, CHN['Singapore'])
leg(bez(JNB, (JNB + CPT) / 2, CPT), IND['Johannesburg'], CHN['Johannesburg'])
leg(bez(DXB, (DXB + CPT) / 2 + np.array([40, 20]), CPT), IND['Dubai'], CHN['Dubai'])
leg(bez(DOH, (DOH + CPT) / 2, CPT), IND['Doha'], CHN['Doha'])
leg(bez(ADD, (ADD + CPT) / 2 + np.array([-30, -10]), CPT), IND['Addis Ababa'], CHN['Addis Ababa'])
# 2 origin to hub
stroke(bez((CB[0] + 50, CB[1] + CB[3]), (2360, 1010), ADD), wd(CHN['Addis Ababa']), CHAR)
stroke(bez((IB[0], IB[1] + IB[3] - 24), (1550, 760), ADD), wd(IND['Addis Ababa']), CYAN)
stroke(bez((CB[0] + 110, CB[1] + CB[3]), (2400, 1500), JNB), wd(CHN['Johannesburg']), CHAR)
stroke(bez((IB[0] + 20, IB[1] + IB[3]), (1560, 1560), JNB), wd(IND['Johannesburg']), CYAN)
stroke(bez((CB[0] + 200, CB[1] + CB[3]), (2700, 650), SIN), wd(CHN['Singapore']), CHAR)
stroke(bez((CB[0], CB[1] + 120), (2000, 330), DXB), wd(CHN['Dubai']), CHAR)
stroke(bez((IB[0], IB[1] + 30), (1700, 250), DXB), wd(IND['Dubai']), CYAN)
stroke(bez((IB[0] + 40, IB[1]), (1600, 150), DOH), wd(IND['Doha']), CYAN)
stroke(bez((CB[0], CB[1] + 70), (1560, 60), DOH), wd(CHN['Doha']), CHAR)
# origin boxes on top of the line starts
for (x, y, w, h), col, name, big in ((IB, CYAN, 'India', 'about 71,000'), (CB, CHAR, 'China', 'about 30,000')):
    rbox(ax, x, y, w, h, col, r=16, z=8)
    T(ax, x + w / 2, y + 50, name, S_HEAD, WHITE, True, ha='center')
    T(ax, x + w / 2, y + 112, big, S_AX, WHITE, ha='center')
    T(ax, x + w / 2, y + 164, 'travellers a year', S_AX, WHITE, ha='center')
# hub nodes and cards
def card(node, x, y, name, anchor=None):
    rows = [(CYAN, 'India', IND[name])] if name in IND else []
    rows += [(CHAR, 'China', CHN[name])] if name in CHN else []
    w = max(tw(name, S_VAL, True), max(34 + tw('%s %s' % (o, format(v, ',')), S_VAL, True) for _, o, v in rows)) + 56
    h = 70 + 56 * len(rows) + 22
    if anchor is not None: line(ax, node[0], node[1], anchor[0], anchor[1], GREY, 2.6, z=8.5)
    rbox(ax, x, y, w, h, WHITE, r=14, edge=GRID, lw=2.6, z=9)
    T(ax, x + 28, y + 48, name, S_VAL, INK, True)
    for k, (col, o, v) in enumerate(rows):
        yy = y + 70 + 56 * k + 30
        ax.add_patch(Circle((x + 28 + 12, yy), 12, facecolor=col, edgecolor='none', zorder=10))
        T(ax, x + 28 + 34, yy, o, S_AX, INK)
        T(ax, x + 28 + 34 + tw(o + ' ', S_AX), yy, format(v, ','), S_VAL, INK, True)
    return w, h
for n in (JNB, ADD, DOH, DXB, SIN): ax.add_patch(Circle(n, 21, facecolor=WHITE, edgecolor=INK, linewidth=4.5, zorder=8.8))
card(DOH, 1010, 205, 'Doha', (1340, 330))
card(DXB, 1520, 450, 'Dubai', (1530, 455))
card(ADD, 700, 640, 'Addis Ababa', (1030, 760))
card(JNB, 1010, 1240, 'Johannesburg', (1020, 1420))
card(SIN, 2700, 900, 'Singapore', (2710, 960))
# Cape Town
ax.add_patch(Circle(CPT, 44, facecolor=INK, edgecolor=WHITE, linewidth=5, zorder=8.8))
T(ax, CPT[0] - 70, CPT[1] + 6, 'Cape Town', S_HEAD, INK, True, ha='right')
callout(ax, 'Addis Ababa and Dubai carry 81% of Indian\ntravellers, and no direct service links either\ncountry to Cape Town.', 1930, 1570)
foot(ax, 'Schematic map. Line weight shows travellers a year through each hub.')
save(fig, 'fig_2_10')
