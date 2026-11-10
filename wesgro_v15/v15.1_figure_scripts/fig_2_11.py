import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figlib import *
# Path to purchase in three growth markets: 3 x 4 matrix. Cell wording follows v15 ("China: discovery, booking and access",
# "India: discovery, booking and access", "The Middle East: source and gateway"). The Gulf in-destination cell is the one
# cell v15 does not cover; it is taken from Demand-Side Analysis p49. **...** marks platform names (set bold).
COLS = ['Inspiration', 'Consideration', 'Booking', 'In destination']
ROWS = [
 ('China', [
  '**Douyin** leads discovery on short video. **Xiaohongshu** supplies peer validation. Travel creators shape aspiration.',
  'Reviews on **Trip.com** act as the credibility filter. Package prices on **Qunar** set how a destination compares.',
  '**Trip.com**, **Qunar** and **Fliggy** dominate outbound booking, often as flight and hotel packages, with peaks around the main holidays.',
  'Visitors look for Mandarin-speaking guides or translation, clear signage, **Alipay** and **WeChat Pay** and structured itineraries.']),
 ('India', [
  '**Instagram**, **YouTube** and the advice of family and friends.',
  'Research on **Google** into visas, costs, weather and safety. Packages compared on **MakeMyTrip**.',
  '**MakeMyTrip**, **Booking.com** and **Expedia**, often as bundled packages for multi-destination trips.',
  '**Google Maps**, **WhatsApp** and **TripAdvisor** carry directions, contact with operators and activity booking.']),
 ('Gulf', [
  'Visual social media: **TikTok**, **Instagram**, **YouTube** and, in Saudi Arabia and the UAE, **Snapchat**.',
  '**Google** searches for visas, safety, halal options and family-friendly stays. Fares compared on **Skyscanner**. Reviews checked on **TripAdvisor**.',
  '**Almosafer**, **Wego** and **Cleartrip** take bookings through Arabic interfaces. Much travel is still arranged through private advisors, concierge agencies and offline agents.',
  '**Google Maps** and **Google Translate** for navigation, halal dining and prayer facilities. **WhatsApp** for contact with guides. Luxury shopping and dining, often led by concierge services.']),
]
SZ = S_AX; LH = SZ * 1.34
def words(s):
    """Split marked-up text into words; each word is a list of (fragment, bold)."""
    out, cur, bold, i, buf = [], [], False, 0, ''
    def flush():
        nonlocal buf
        if buf: cur.append((buf, bold)); buf = ''
    while i < len(s):
        if s.startswith('**', i): flush(); bold = not bold; i += 2; continue
        ch = s[i]; i += 1
        if ch == ' ':
            flush()
            if cur: out.append((cur, bold)); cur = []      # bold here = whether the following space sits inside a bold run
        else: buf += ch
    flush()
    if cur: out.append((cur, False))
    return out
def ww(word): return sum(tw(f, SZ, b) for f, b in word)
def rwrap(s, maxw):
    lines, line_, wline = [], [], 0.0
    for word, sp_bold in words(s):
        w = ww(word); sp = tw(' ', SZ, False)
        if line_ and wline + sp + w > maxw: lines.append(line_); line_, wline = [], 0.0
        if line_: wline += sp
        line_.append((word, wline)); wline += w
    if line_: lines.append(line_)
    return lines
def rdraw(ax, x, y, lines):
    for j, ln in enumerate(lines):
        for word, off in ln:
            xx = x + off
            for f, b in word:
                T(ax, xx, y + j * LH, f, SZ, INK, b); xx += tw(f, SZ, b)
ML, MR, RH, GAP = 70, 70, 250, 34
CW = (W - ML - MR - RH - 4 * GAP) / 4.0
PADX, PADY = 34, 40
HH = 124                                   # header height
wrapped = [[rwrap(c, CW - 2 * PADX) for c in cells] for _, cells in ROWS]
nl = [max(len(c) for c in row) for row in wrapped]
rh = [n * LH + 2 * PADY for n in nl]
TOP = 70
Hc = int(TOP + HH + sum(rh) + 3 * GAP + 70)
print('lines per row', nl, 'needed height', Hc)
H = int((Hc + 3 * 36 + 19) // 20 * 20)       # modest height: the rows need little more than their text
extra = (H - Hc) / 3.0                     # spread spare height evenly over the rows
rh = [r + extra for r in rh]
fig, ax = canvas(H)
cx = [ML + RH + GAP + k * (CW + GAP) for k in range(4)]
for k, c in enumerate(COLS):
    rbox(ax, cx[k], TOP, CW, HH, CHAR, r=16)
    T(ax, cx[k] + CW / 2, TOP + HH / 2, c, S_HEAD, WHITE, True, ha='center')
    if k < 3:                              # small arrow in the gap: the stages run left to right
        xa = cx[k] + CW + GAP / 2
        ax.add_patch(Polygon([(xa - 9, TOP + HH / 2 - 20), (xa + 11, TOP + HH / 2), (xa - 9, TOP + HH / 2 + 20)], closed=True, facecolor=GREY, edgecolor='none', zorder=5))
y = TOP + HH + GAP
for (name, cells), row, h in zip(ROWS, wrapped, rh):
    rbox(ax, ML, y, RH, h, CYAN, r=16)
    T(ax, ML + RH / 2, y + h / 2, name, S_HEAD, WHITE, True, ha='center')
    for k, lines in enumerate(row):
        rbox(ax, cx[k], y, CW, h, FILL, r=16)
        rdraw(ax, cx[k] + PADX, y + PADY + extra / 2 + LH / 2, lines)
    y += h + GAP
save(fig, 'fig_2_11')
