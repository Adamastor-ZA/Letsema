"""Checker for the v8 drafts (executive summary, section 1.1, Chapter 2 in four parts).

A draft is a JSON file in redteam/v8/drafts/ of the form
  {"module": "ch2/02_demand.json", "id": "2.2", "title": "Demand-side factors",
   "sources": [["ch2/01_demand.json", 13], ...],          # v7 blocks this draft absorbs in full (file relative to content/, index)
   "partial_sources": [["ch2/04_stakeholders.json", 9]],  # v7 blocks split across several drafts; checked jointly with --chapter2
   "relocations": [{"src": ["ch2/03_benchmarking.json", 7], "to": "held in Appendix A3 (Table A.10)", "reason": "..."}],
   "blocks": [... content blocks ..., {"type": "ref", "src": ["ch2/01_demand.json", 18]}]}
A "ref" block copies a v7 block verbatim (figures and tables are always carried this way).

Usage: python3 check_v8_draft.py DRAFT.json [DRAFT2.json ...] [--chapter2] [--strict-callouts]
Prints ERROR and WARN lines and a summary; exit code 1 if any ERROR.
  --chapter2         also check that every Chapter 2 v7 block is absorbed or relocated exactly once across the drafts given
  --strict-callouts  treat naming an interim deliverable in the text as an error (always on for exec and ch2 modules)
"""
import json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
C = os.path.join(HERE, '..', 'content')
V7 = {}


V7_COMMIT = os.environ.get('V7_COMMIT', 'a8ef7a0')  # the draft v7 commit: drafts are always checked against v7, wherever content/ stands
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))


def git_show(rel):
    out = subprocess.run(['git', '-C', REPO, 'show', f'{V7_COMMIT}:report/build/content/{rel}'], capture_output=True, text=True)
    if out.returncode: raise FileNotFoundError(rel)
    return json.loads(out.stdout)


def v7_files():
    out = subprocess.run(['git', '-C', REPO, 'ls-tree', '-r', '--name-only', V7_COMMIT, 'report/build/content/'], capture_output=True, text=True).stdout
    return [x[len('report/build/content/'):] for x in out.split() if x.endswith('.json')]


def v7(f):
    if f not in V7:
        V7[f] = git_show(f)['blocks']
    return V7[f]


ALL_V7_TEXT = None
PARTIAL, ALL_NEW, ALL_RELOC = {}, [], []

DOCS = ['Inception Report', 'Current State Diagnostic', 'Market Assessment Report', 'Demand-Side Analysis', 'MIDAS Aviation Market Assessment',
        'MIDAS', 'Global Benchmarking Report', 'Stakeholder Insights Report', 'Infrastructure Report', 'SME and Community Inclusion Plan',
        'Summary of Findings', 'Skift Segmentation', 'Skift Digital and Search Insights', 'Skift African Market Analysis', 'SLA Annexure B', 'Annexure B']
CALLOUT = re.compile(r"\b(" + '|'.join(re.escape(d) for d in DOCS) + r")\b|\b(the|this|that|each|both|two|June|May|March|July|September|December|October) (deck|decks)\b|\bdeck's\b|\bSkift's (survey|model|report|analysis)\b|\binterim deliverables?\b|\bthe (aviation|demand|benchmarking|stakeholder|infrastructure|inclusion) (report|deliverable|workstream|deck)\b", re.I)
MONTHS = r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{4}'
BANNED = re.compile(r'\b(unlock\w*|ecosystem\w*|leverag\w*|landscape\w*|navigat\w*|delve\w*|synerg\w*|tapestry|realm|game-changer|paradigm)\b', re.I)
INTENS = re.compile(r'\b(really|very|incredibly|absolutely|truly|deeply)\b', re.I)
OXF = re.compile(r',\s[^,.;:()\[\]]{1,60},\s(and|or)\s(?!then\b)', re.I)
TYPES = {'h2', 'h3', 'h4', 'lead', 'p', 'note', 'bullets', 'numbered', 'box', 'quote', 'ref', 'pagebreak', 'kicker', 'table', 'figure', 'grid', 'spacer'}


def nums(s):
    return {n for n in re.findall(r'\d+(?:[.,]\d+)*', s) if not (n.isdigit() and len(n) == 1)}


def block_text(b):
    parts = [b.get(k) or '' for k in ('text', 'title', 'caption', 'message', 'source', 'attribution')]
    parts += [x for x in (b.get('items') or []) if isinstance(x, str)] + [x for x in (b.get('paras') or []) if isinstance(x, str)]
    parts += [' '.join(map(str, r)) for r in (b.get('rows') or [])]
    if b.get('chart'): parts.append(json.dumps(b['chart'], ensure_ascii=False))
    return ' '.join(parts)


def prose(b):
    """The running text of a block that a reader reads as the report's own words (not figure or table furniture)."""
    if b['type'] in ('p', 'lead', 'note', 'quote', 'h2', 'h3', 'h4', 'kicker'): return [b.get('text', '')]
    if b['type'] in ('bullets', 'numbered'): return list(b.get('items', []))
    if b['type'] == 'box': return [b.get('title', '')] + list(b.get('paras', []))
    return []


def strip_cites(s):
    """Remove house-form citation parentheses (they become footnotes) and bracketed open items."""
    s = re.sub(r'\[[^\]]*\]', ' ', s)
    out, depth, buf = [], 0, []
    for ch in s:
        if ch == '(':
            depth += 1; buf.append(ch); continue
        if ch == ')' and depth:
            depth -= 1; buf.append(ch)
            if depth == 0:
                inner = ''.join(buf)
                if re.search(MONTHS, inner) or any(d in inner for d in DOCS) or re.fullmatch(r'\((pp?\s?\d[^)]*|"[^"]+"(, "[^"]+")*)\)', inner):
                    out.append(' ')
                else:
                    out.append(inner)
                buf = []
            continue
        (buf if depth else out).append(ch)
    return ''.join(out) + ''.join(buf)


def sentences(s):
    s = re.sub(r'\*\*', ' \n ', s)
    return [x.strip() for part in s.split('\n') for x in re.split(r'(?<=[.!?:;])\s+(?=[A-Z\[(])', part) if x.strip()]


def parens(s):
    out, depth, cur = [], 0, ''
    for ch in s:
        if ch == '(':
            depth += 1
            if depth == 1: cur = ''; continue
        if ch == ')' and depth:
            depth -= 1
            if depth == 0: out.append(cur); continue
        if depth: cur += ch
    return out


def check(path, errs, warns, chapter2_seen, strict):
    d = json.load(open(path))
    name = os.path.basename(path)
    E = lambda m: errs.append(f'{name}: {m}')
    W = lambda m: warns.append(f'{name}: {m}')
    for k in ('module', 'blocks', 'sources'):
        if k not in d: E(f'missing key {k}')
    mod = d.get('module', '')
    strict = strict or mod.startswith('ch2/') or mod.startswith('exec/')
    blocks = []
    for i, b in enumerate(d.get('blocks', [])):
        t = b.get('type')
        if t not in TYPES: E(f'block {i}: unknown type {t}'); continue
        if t == 'ref':
            f, j = b['src']
            chapter2_seen.setdefault(('REF', f, j), []).append(name)
            try: blocks.append(('ref', v7(f)[j]))
            except (IndexError, FileNotFoundError): E(f'block {i}: ref {b["src"]} does not resolve')
            continue
        if t in ('figure',): E(f'block {i}: figures must be carried as refs')
        if t in ('bullets', 'numbered') and not isinstance(b.get('items'), list): E(f'block {i}: {t} needs items')
        if t == 'box' and not isinstance(b.get('paras'), list): E(f'block {i}: box needs paras')
        if t in ('p', 'lead', 'note', 'h2', 'h3', 'h4', 'quote') and not b.get('text'): E(f'block {i}: {t} needs text')
        blocks.append(('new', b))
    if mod.startswith('ch2/') or mod.startswith('ch1/'):
        first_h2 = next((k for k, (_, b) in enumerate(blocks) if b.get('type') == 'h2'), None)
        intro_ok = mod == 'ch2/01_benchmarks.json' and first_h2 is not None and first_h2 <= 3 and all(blocks[k][1]['type'] in ('p', 'lead') for k in range(first_h2))
        if first_h2 != 0 and not intro_ok: E('first block must be the h2 section heading (only ch2/01 may open with up to three chapter-introduction paragraphs)')
    # style and call-outs on new prose only
    long_n = 0
    for kind, b in blocks:
        if kind != 'new': continue
        for s in prose(b):
            if '–' in s or '—' in s: E(f'dash in: {s[:90]}')
            for m in BANNED.finditer(s): E(f'banned word "{m.group(0)}" in: {s[:90]}')
            for m in INTENS.finditer(s): W(f'intensifier "{m.group(0)}" in: {s[:90]}')
            body = strip_cites(s)
            for m in CALLOUT.finditer(body):
                (E if strict else W)(f'names a deliverable in the text ("{m.group(0)}"): ...{body[max(0, m.start() - 60):m.end() + 40]}...')
            for m in OXF.finditer(body): W(f'possible Oxford comma: ...{body[max(0, m.start() - 30):m.end() + 10]}...')
            for sen in sentences(body):
                w = len(sen.split())
                if w > 35: E(f'sentence of {w} words: {sen[:120]}')
                elif w > 28: long_n += 1
            for p in parens(s):
                if any(dn in p for dn in DOCS) and not re.search(MONTHS, p) and 'Summary of Findings' not in p:
                    E(f'citation without a date: ({p[:80]})')
                if re.fullmatch(r'\s*(pp?\s?\d[^)]*|"[^"]+"(, "[^"]+")*)\s*', p):
                    E(f'short-form citation ({p}) : write it in full, e.g. (Demand-Side Analysis, Jun 2026, p22)')
    if long_n: W(f'{long_n} sentences of 29 to 35 words')
    # coverage
    src_text = ''
    for f, j in d.get('sources', []):
        try: src_text += ' ' + block_text(v7(f)[j])
        except (IndexError, FileNotFoundError): E(f'source {f}[{j}] does not resolve')
        chapter2_seen.setdefault((f, j), []).append(name)
    for f, j in d.get('partial_sources', []):
        chapter2_seen.setdefault((f, j), []).append(name + ' (partial)')
        PARTIAL.setdefault((f, j), True)
    reloc_text = ''
    for r in d.get('relocations', []):
        f, j = r['src']
        chapter2_seen.setdefault((f, j), []).append(name + ' (relocated)')
        reloc_text += ' ' + block_text(v7(f)[j]) if r.get('carries_all') else ''
        if not r.get('to') or not r.get('reason'): E(f'relocation {r["src"]} needs "to" and "reason"')
    new_text = ' '.join(block_text(b) for _, b in blocks)
    ALL_NEW.append(new_text); ALL_RELOC.append(reloc_text)
    missing = sorted(nums(src_text) - nums(new_text) - nums(reloc_text), key=lambda x: (len(x), x))
    if missing: E(f'{len(missing)} numbers from the absorbed sources are missing: {missing[:60]}')
    norm = lambda s: re.sub(r'\W+', ' ', s).strip().lower()
    open_src = {norm(x) for x in re.findall(r'\[([^\]]+)\]', src_text)}
    open_new = {norm(x) for x in re.findall(r'\[([^\]]+)\]', new_text)}
    for o in sorted(open_src - open_new): E(f'open item dropped: [{o[:120]}]')
    global ALL_V7_TEXT
    if ALL_V7_TEXT is None:
        ALL_V7_TEXT = ' '.join(block_text(b) for f in v7_files() for b in v7(f))
    invented = sorted(nums(' '.join(block_text(b) for k, b in blocks if k == 'new')) - nums(ALL_V7_TEXT), key=lambda x: (len(x), x))
    if invented: E(f'numbers that appear nowhere in the v7 report (check, or show the computation in the text): {invented[:40]}')
    words = sum(len(' '.join(prose(b)).split()) for k, b in blocks if k == 'new')
    return words


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    errs, warns, seen = [], [], {}
    total = 0
    for p in args:
        w = check(p, errs, warns, seen, '--strict-callouts' in sys.argv)
        print(f'{os.path.basename(p)}: {w} words of new prose')
        total += w
    if '--chapter2' in sys.argv:
        for f in sorted(x[len('ch2/'):] for x in v7_files() if x.startswith('ch2/')):
            for j, b in enumerate(v7('ch2/' + f)):
                if b['type'] in ('pagebreak', 'spacer'): continue
                hits = seen.get(('ch2/' + f, j), [])
                if not hits: errs.append(f'Chapter 2 coverage: ch2/{f}[{j}] ({b["type"]}: {block_text(b)[:70]}) is neither absorbed nor relocated')
                if b['type'] in ('figure', 'table'):
                    refs = seen.get(('REF', 'ch2/' + f, j), [])
                    moved = [h for h in hits if h.endswith('(relocated)')]
                    if len(refs) + len(moved) != 1: errs.append(f'Chapter 2 coverage: {b["type"]} ch2/{f}[{j}] "{b.get("caption")}" is carried {len(refs)} times as a ref and relocated {len(moved)} times (needs exactly one)')
    if PARTIAL:
        ptxt = ' '.join(block_text(v7(f)[j]) for f, j in PARTIAL)
        miss = sorted(nums(ptxt) - nums(' '.join(ALL_NEW)) - nums(' '.join(ALL_RELOC)), key=lambda x: (len(x), x))
        if miss: errs.append(f'partial sources: {len(miss)} numbers from blocks split across drafts appear in none of the drafts given: {miss[:60]}')
        opn = {re.sub(r'\W+', ' ', x).strip().lower() for x in re.findall(r'\[([^\]]+)\]', ptxt)}
        onew = {re.sub(r'\W+', ' ', x).strip().lower() for x in re.findall(r'\[([^\]]+)\]', ' '.join(ALL_NEW))}
        for o in sorted(opn - onew): errs.append(f'partial sources: open item in none of the drafts given: [{o[:120]}]')
    for w in warns: print('WARN ', w)
    for e in errs: print('ERROR', e)
    print(f'{len(errs)} errors, {len(warns)} warnings, {total} words of new prose')
    sys.exit(1 if errs else 0)


if __name__ == '__main__':
    main()
