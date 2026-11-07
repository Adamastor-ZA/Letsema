"""Draft v4 content edits: Wesgro CI colours in the content modules.

The renderer carries the CI (charts.js palette, helpers.js styles, cover, dividers and back cover). This script sets
the colours the content modules hold themselves: the series colours of five line charts and the three hand-drawn
diagrams (results chain, governance, scorecard). Diagram text on a coloured box takes white or near-black, whichever
meets 4.5:1 contrast on the new fill. The scorecard's status dots keep green, amber and red, since they carry status.

Run once on the v3 content. Writes redteam/applied_v4.json.
"""
import json, glob, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
C = os.path.join(HERE, '..', 'content')
FILES = {os.path.relpath(f, C): json.load(open(f)) for f in sorted(glob.glob(os.path.join(C, '*', '*.json')))}
LOG = []

CHAR, CYAN, DCYAN, LCYAN = '#4D4D4F', '#00A3DA', '#006E93', '#80D1EC'
GREY, LGREY, RULE, FILL, GRID, INK, PINK = '#6D6E71', '#A7A9AC', '#E6E7E8', '#F5F6F7', '#D9DADB', '#2B2B2D', '#C8385F'


def text_on(hex_):
    def lin(i):
        v = int(hex_[1 + 2 * i:3 + 2 * i], 16) / 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    L = 0.2126 * lin(0) + 0.7152 * lin(1) + 0.0722 * lin(2)
    return '#ffffff' if 1.05 / (L + 0.05) >= 4.5 else '#1E1E20'


def block(fid):
    hits = [(f, b) for f, d in FILES.items() for b in d['blocks'] if b.get('id') == fid]
    assert len(hits) == 1, fid
    return hits[0]


# 1. Line chart series.
SERIES = {'Accelerated': CYAN, 'Base': CHAR, 'Conservative': LCYAN, 'Seats': CHAR, 'Visitors': DCYAN, 'Meetings': CYAN}
for fid in ('fig_0_paths', 'fig_21_scenarios', 'fig_5_paths', 'fig_3_fa02_months'):
    f, b = block(fid)
    for sr in b['chart']['series']:
        old = sr.get('color'); sr['color'] = SERIES[sr['name']]
        LOG.append({'figure': fid, 'file': f, 'series': sr['name'], 'before': old, 'after': sr['color']})


# 2. Diagrams. Boxes are rects with a fill; text that follows a box takes the contrast colour of the box's new fill.
def recolour(svg, box, stroke, text, other, dot=None):
    out, cur = [], None
    for tok in re.split(r'(<[^>]+>)', svg):
        if not tok.startswith('<') or tok.startswith('</'):
            out.append(tok); continue
        tag = re.match(r'<(\w+)', tok).group(1)
        fill = re.search(r'fill="(#[0-9A-Fa-f]{3,6})"', tok)
        if tag == 'rect' and fill:
            old = fill.group(1).upper()
            w = re.search(r'width="(\d+)"', tok)
            if dot and w and int(w.group(1)) <= 30 and old in dot:
                tok = tok.replace(fill.group(0), f'fill="{dot[old]}"')
            elif old in box:
                tok = tok.replace(fill.group(0), f'fill="{box[old]}"'); cur = box[old]
            elif old in ('#FFFFFF', '#FFF', '#F3F6F9'):
                if old == '#F3F6F9': tok = tok.replace(fill.group(0), f'fill="{FILL}"')
                cur = None
        elif tag == 'text' and fill:
            old = fill.group(1).upper()
            if old in ('#FFF', '#FFFFFF') and cur: tok = tok.replace(fill.group(0), f'fill="{text_on(cur)}"')
            elif old in text: tok = tok.replace(fill.group(0), f'fill="{text[old]}"')
        elif fill and fill.group(1).upper() in other:
            tok = tok.replace(fill.group(0), f'fill="{other[fill.group(1).upper()]}"')
        st = re.search(r'stroke="(#[0-9A-Fa-f]{6})"', tok)
        if st and st.group(1).upper() in stroke:
            tok = tok.replace(st.group(0), f'stroke="{stroke[st.group(1).upper()]}"')
        out.append(tok)
    return ''.join(out)


DIAGRAMS = {
    # Results chain: light to dark, inputs to impact.
    'fig_5_chain': dict(box={'#5B6572': RULE, '#1F7A8C': LCYAN, '#7A9E7E': CYAN, '#C98B2B': DCYAN, '#0B3C5D': CHAR},
                        stroke={'#5B6572': LGREY}, text={'#1C2431': INK}, other={'#5B6572': LGREY}),
    # Governance: charcoal for the Board and Steerco tiers, the cyan family for delivery and partners.
    'fig_4_governance': dict(box={'#5B6572': GREY, '#0B3C5D': CHAR, '#1F7A8C': DCYAN, '#7A9E7E': LCYAN},
                             stroke={'#B23A48': DCYAN, '#C98B2B': CYAN, '#1F7A8C': LCYAN, '#5B6572': GREY},
                             text={'#B23A48': DCYAN, '#C98B2B': DCYAN, '#1F7A8C': DCYAN, '#0B3C5D': CHAR, '#5B6572': GREY, '#1C2431': INK}, other={}),
    # Scorecard: charcoal header, CI greys; the status dots stay green, amber and red.
    'fig_5_dashboard': dict(box={'#0B3C5D': CHAR}, stroke={'#C9D1DA': GRID, '#0B3C5D': CHAR, '#7A9E7E': DCYAN},
                            text={'#0B3C5D': CHAR, '#1C2431': INK, '#5B6572': GREY}, other={},
                            dot={'#7A9E7E': '#2E9E6B', '#C98B2B': '#E5A823', '#B23A48': PINK}),
}
for fid, maps in DIAGRAMS.items():
    f, b = block(fid)
    before = b['svg']
    b['svg'] = recolour(before, **maps)
    left = sorted(set(h.upper() for h in re.findall(r'#[0-9A-Fa-f]{6}\b', b['svg'])) & {'#0B3C5D', '#1F7A8C', '#7A9E7E', '#C98B2B', '#B23A48', '#5B6572', '#1C2431', '#F3F6F9', '#C9D1DA'})
    LOG.append({'figure': fid, 'file': f, 'changed_tokens': sum(1 for a, c in zip(re.split(r'(<[^>]+>)', before), re.split(r'(<[^>]+>)', b['svg'])) if a != c), 'old_colours_left': left})

for f, d in FILES.items():
    with open(os.path.join(C, f), 'w') as fh:
        json.dump(d, fh, indent=1, ensure_ascii=False); fh.write('\n')
json.dump(LOG, open(os.path.join(HERE, 'applied_v4.json'), 'w'), indent=1, ensure_ascii=False)
for e in LOG: print(e)
