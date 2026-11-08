"""Draft v8 content edits (Michael, 7 November 2026).

1. The executive summary is rewritten as a story (draft redteam/v8/drafts/es.json).
2. Section 1.1 keeps the mandate, objective, ambitions, metrics and alignment up front, with the data reconciliation
   held to a short closing note (draft s11.json). The arrivals-bases table moves to the end of Appendix A2.
3. Chapter 2 becomes "Analysis and insights", a discussion in four parts: 2.1 global benchmarks and their lessons,
   2.2 demand-side factors, 2.3 supply-side factors and 2.4 the enabling environment (drafts ch2_1 to ch2_4). The
   interim deliverables move out of the text into the footnotes. The six v7 modules are replaced by four.
4. Knock-on edits: the Chapter 1 sentences that describe Chapter 2, cross-references into Chapter 2, the Chapter 2
   column of the Appendix A1 traceability table and traceability.csv, the chapter title in ch2_analysis.js and the
   QA scripts that look it up.

The drafts carry v7 figures and tables as {"type": "ref", "src": [file, index]} blocks, resolved here to the v7 block
verbatim. Run once on the v7 content. Writes redteam/applied_v8.json.
"""
import copy, csv, glob, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.join(HERE, '..')
C = os.path.join(B, 'content')
D = os.path.join(HERE, 'v8', 'drafts')
V7 = {os.path.relpath(f, C): json.load(open(f)) for f in sorted(glob.glob(os.path.join(C, '*', '*.json')))}
OUT = copy.deepcopy(V7)
LOG = []
CH2_TITLE = 'Analysis and insights'


def resolve(blocks):
    out = []
    for b in blocks:
        if b.get('type') == 'ref':
            f, j = b['src']
            out.append(copy.deepcopy(V7[f]['blocks'][j]))
        else:
            out.append(b)
    return out


def edit(f, find, repl, n=1):
    hits = [b for b in OUT[f]['blocks'] if find in json.dumps(b, ensure_ascii=False)]
    total = sum(json.dumps(b, ensure_ascii=False).count(find) for b in hits)
    assert total == n, (f, find[:70], total)
    for b in hits:
        new = json.loads(json.dumps(b, ensure_ascii=False).replace(find, repl))
        b.clear(); b.update(new)
    LOG.append({'kind': 'text edit', 'file': f, 'before': find, 'after': repl})


# ------------------------------------------------------------------------------------------------ 1 to 3. Drafts
DRAFTS = [('es.json', 'exec/01_summary.json'), ('s11.json', 'ch1/01_mandate.json'), ('ch2_1.json', 'ch2/01_benchmarks.json'),
          ('ch2_2.json', 'ch2/02_demand.json'), ('ch2_3.json', 'ch2/03_supply.json'), ('ch2_4.json', 'ch2/04_enabling.json')]
for name, mod in DRAFTS:
    d = json.load(open(os.path.join(D, name)))
    assert d['module'] == mod, (name, d['module'])
    blocks = resolve(d['blocks'])
    before = OUT.get(mod)
    OUT[mod] = {'id': d.get('id', before and before.get('id')), 'title': d.get('title', before and before.get('title')), 'blocks': blocks}
    LOG.append({'kind': 'module rewritten' if before else 'module created', 'file': mod, 'draft': name,
                'sources': d.get('sources', []) + d.get('partial_sources', []), 'relocations': d.get('relocations', [])})
    extra = d.get('appendix_blocks')
    if extra:
        tgt = extra['module']
        OUT[tgt]['blocks'].extend(resolve(extra['blocks']))
        LOG.append({'kind': 'blocks appended', 'file': tgt, 'from_draft': name, 'blocks': len(extra['blocks'])})

NEW_CH2 = [m for _, m in DRAFTS if m.startswith('ch2/')]
for f in [k for k in OUT if k.startswith('ch2/') and k not in NEW_CH2]:
    del OUT[f]
    LOG.append({'kind': 'module removed', 'file': f})


# ------------------------------------------------------------------------------------------------ 4. Knock-on edits
def section_of(pred):
    """The new Chapter 2 section whose module holds a block matching pred."""
    hits = [OUT[m]['id'] for m in NEW_CH2 if any(pred(b) for b in OUT[m]['blocks'])]
    assert len(hits) >= 1, 'no section matches'
    return hits[0]


has = lambda s: (lambda b: s in json.dumps(b, ensure_ascii=False))
cap = lambda c: (lambda b: b.get('caption') == c)

edit('ch1/04_approach.json', re.search(r'Chapter 2 summarises them:[^"]*?folded into 2\.1 and 2\.5\.', json.dumps(V7['ch1/04_approach.json'], ensure_ascii=False)).group(0),
     'Chapter 2 draws them together as one body of analysis in four parts: the global benchmarks and their lessons (2.1), demand (2.2), supply (2.3) and the enabling environment (2.4). The Inception Report frames 1.1 and 1.4, and the Current State Diagnostic frames 1.2.')
edit('ch1/05_how_to_read.json', 'Chapter 2 summarises what each interim deliverable asked, did and found, with the evidence that survived into the hypothesis tree.',
     'Chapter 2 sets out what the analysis found, in four parts: the global benchmarks and their lessons, demand, supply and the enabling environment.')
edit('ch1/05_how_to_read.json', 'and each section closes with a box naming the focus areas it supports', 'and each part closes with a box naming the focus areas it supports')
edit('appendices/03_a3_benchmark.json', 'Kenya 14.6% (section 2.2)', f"Kenya 14.6% (section {section_of(has('14.6%'))})")
edit('appendices/05_a5_inclusion.json', "section 2.6 prints each community's archetype", f"section {section_of(cap('The 20 shortlisted communities'))} prints each community's archetype")
edit('ch3/31_fa13.json', 'first allocated to Kliptown (section 2.6)', f"first allocated to Kliptown (section {section_of(has('R436'))})")
edit('ch5/03_baselines_targets.json', 'Base path by group, section 2.1', f"Base path by group, section {section_of(cap('Base-case growth by market group'))}")

edit('ch1/05_how_to_read.json', 'The executive summary gives the case in short: the growth case to 2035, the constraints that cap it, the twenty focus areas by pillar, the first 24 months and the headline indicators.',
     "The executive summary tells the case in short: where the province stands, what caps growth and what 2.5 million arrivals would take. It then sets out the three shifts and the twenty focus areas, the first 24 months, the headline indicators, the main risks and the Board's decisions.")


# Table and figure numbers cited in modules the drafts did not rewrite: the moved and removed tables renumber everything after
# them, so each cited number is mapped through its caption from the v7 numbering to the v8 numbering.
def numbering(mods):
    out = {'table': {}, 'figure': {}}
    for dname, lab in [('exec', 'ES'), ('ch1', '1'), ('ch2', '2'), ('ch3', '3'), ('ch4', '4'), ('ch5', '5'), ('appendices', 'A')]:
        n = {'table': 0, 'figure': 0}
        for f in sorted(k for k in mods if k.startswith(dname + '/')):
            for b in mods[f]['blocks']:
                if b['type'] in n:
                    n[b['type']] += 1; out[b['type']][f'{lab}.{n[b["type"]]}'] = b['caption']
    return out


N7, N8 = numbering(V7), numbering(OUT)
INV8 = {k: {c: num for num, c in v.items()} for k, v in N8.items()}
XREF = re.compile(r'\b(Tables?|Figures?) ((?:ES|A|\d)\.\d+(?:(?:, | and | to )(?:ES|A|\d)\.\d+)*)')


def renum(f, s):
    def one(m):
        kind = 'table' if m.group(1).startswith('Table') else 'figure'
        def tok(t):
            new = INV8[kind][N7[kind][t.group(0)]]
            return new
        return m.group(1) + ' ' + re.sub(r'(?:ES|A|\d)\.\d+', tok, m.group(2))
    t = XREF.sub(one, s)
    if t != s: LOG.append({'kind': 'renumbered reference', 'file': f, 'before': s, 'after': t})
    return t


def walk(f, x):
    if isinstance(x, str): return renum(f, x)
    if isinstance(x, list): return [walk(f, y) for y in x]
    if isinstance(x, dict): return {k: (walk(f, v) if k not in ('chart', 'svg', 'id') else v) for k, v in x.items()}
    return x


drafted = {m for _, m in DRAFTS}
for f in OUT:
    if f not in drafted:
        OUT[f]['blocks'] = walk(f, OUT[f]['blocks'])
for f in drafted:
    for b in OUT[f]['blocks']:
        for t in [b.get('text', '')] + list(b.get('items', []) or []) + list(b.get('paras', []) or []):
            for m in XREF.finditer(t or ''):
                print('NOTE: drafted module cites a number:', f, m.group(0))

# Chapter 2 column of the traceability table and traceability.csv: the new sections whose closing box names the focus area,
# the pillar's own section first; Chapter 1 references are kept as they were.
PILLAR_SEC = lambda n: '2.2' if n <= 6 else '2.3' if n <= 12 else '2.4'
boxes = {}
for m in NEW_CH2:
    for b in OUT[m]['blocks']:
        if b['type'] == 'box':
            for p in b.get('paras', []):
                for n in re.findall(r'FA(\d\d)', p):
                    boxes.setdefault(int(n), set()).add(OUT[m]['id'])
for n in range(1, 21):
    assert n in boxes, f'FA{n:02d} is named in no Chapter 2 box'


def new_col(n, old):
    secs = sorted(boxes[n], key=lambda s: (s != PILLAR_SEC(n), s))
    keep = [x.strip() for x in old.split(';') if x.strip().startswith('1.')]
    return '; '.join(secs + keep)


a1 = 'appendices/01_a1_traceability.json'
t = next(b for b in OUT[a1]['blocks'] if b['type'] == 'table' and b['caption'] == 'Traceability by focus area')
k = [c['header'] for c in t['columns']].index('Chapter 2')
for r in t['rows']:
    n = int(re.match(r'\D*(\d+)', r[0]).group(1))
    old = r[k]; r[k] = new_col(n, old)
    LOG.append({'kind': 'traceability', 'file': a1, 'fa': n, 'before': old, 'after': r[k]})
TCSV = os.path.join(B, '..', 'traceability.csv')
rows = list(csv.DictReader(open(TCSV)))
fields = list(rows[0].keys())
for r in rows:
    n = int(r['fa_id'][2:]); old = r['evidence_sections']; r['evidence_sections'] = new_col(n, old)
    LOG.append({'kind': 'traceability.csv', 'fa': n, 'before': old, 'after': r['evidence_sections']})

# ------------------------------------------------------------------------------------------------ Checks and write
# No module may still point at a Chapter 2 section that no longer exists.
for f, d in OUT.items():
    s = json.dumps(d, ensure_ascii=False)
    for m in re.finditer(r'[Ss]ections? 2\.([5-9])\b', s):
        raise AssertionError(f'{f}: stale reference to section 2.{m.group(1)}: {s[max(0, m.start() - 80):m.end() + 20]}')
for f in [k for k in V7 if k.startswith('ch2/') and k not in OUT]:
    os.remove(os.path.join(C, f))
for f, d in OUT.items():
    with open(os.path.join(C, f), 'w') as fh:
        json.dump(d, fh, indent=1, ensure_ascii=False); fh.write('\n')
with open(TCSV, 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=fields); w.writeheader(); w.writerows(rows)
for p, a, b in [(os.path.join(B, 'ch2_analysis.js'), "title: 'Analysis summaries'", f"title: '{CH2_TITLE}'"),
                (os.path.join(B, 'smoke_test.js'), "H.h1('Analysis summaries', 'ch2')", f"H.h1('{CH2_TITLE}', 'ch2')"),
                (os.path.join(B, 'qa_structure.py'), "('Analysis summaries', 'Chapter 2', (45, 52))", f"('{CH2_TITLE}', 'Chapter 2', (45, 52))")]:
    s = open(p).read(); assert s.count(a) == 1, (p, a); open(p, 'w').write(s.replace(a, b))
    LOG.append({'kind': 'chapter title', 'file': os.path.relpath(p, B), 'before': a, 'after': b})
json.dump(LOG, open(os.path.join(HERE, 'applied_v8.json'), 'w'), indent=1, ensure_ascii=False)
print(len(LOG), 'log entries;', 'modules now:', sorted(k for k in OUT if k.startswith(('exec/', 'ch1/01', 'ch2/'))))
