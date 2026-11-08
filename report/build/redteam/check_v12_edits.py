"""Checker for a v12 edit file (redteam/v12/edits/<stream>.json).

Checks the new text each edit introduces: house style (dashes, banned words, intensifiers, sentences over 35 words outside
citations, possible Oxford commas as warnings); no interim deliverable named in the text of the summary, Chapter 2 or Chapter 3;
no factbase named anywhere; no reference to an earlier tree; no table or figure cited by number; every citation parses into a
footnote (run through the renderer's own parser); and every number in the new text appears in the v11 report, the evidence
extracts or the three factbase texts, unless the edit lists it under "computed".
Usage: python3 check_v12_edits.py <edits.json> [--modules m1,m2,...]   (--modules: the modules this stream owns)
"""
import glob, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.join(HERE, '..')
sys.path.insert(0, HERE)
from check_v9_draft import BANNED, INTENS, OXF, CALLOUT, VERSIONING, strip_cites, sentences, block_text, nums  # noqa: E402

FB = '/tmp/claude-0/-home-user-Letsema/4e1968e6-be48-539d-a4af-9019b21a7592/scratchpad/factbases/txt'
ALLOWED = ' '.join(open(f).read() for f in glob.glob(os.path.join(FB, '*.txt')))
ALLOWED += ' '.join(open(f).read() for f in glob.glob(os.path.join(B, '..', 'evidence', '**', '*.md'), recursive=True))
ALLOWED += ' '.join(json.dumps(json.load(open(f)), ensure_ascii=False) for f in glob.glob(os.path.join(B, 'content', '*', '*.json')))
ALLOWED_N = nums(ALLOWED)


def new_texts(e):
    """(field, text) pairs of reader-facing text the edit introduces."""
    out = []
    if e['op'] == 'replace_text': out.append(('repl', e['repl']))
    if e['op'] == 'set':
        for k, v in e['fields'].items():
            if isinstance(v, str): out.append((k, v))
            elif k == 'rows': out += [('cell', str(c)) for r in v for c in r]
    if e['op'] == 'add_rows': out += [('cell', str(c)) for r in e['rows'] for c in r]
    for b in e.get('blocks', []) or []:
        if b.get('type') == 'ref': continue
        for k in ('text', 'title', 'caption', 'message', 'source'):
            if isinstance(b.get(k), str): out.append((b['type'] + ':' + k, b[k]))
        out += [(b['type'] + ':item', x) for x in (b.get('items') or []) + (b.get('paras') or []) if isinstance(x, str)]
        out += [(b['type'] + ':cell', str(c)) for r in (b.get('rows') or []) for c in r]
    return out


def main():
    path = sys.argv[1]
    own = None
    if '--modules' in sys.argv: own = set(sys.argv[sys.argv.index('--modules') + 1].split(','))
    d = json.load(open(path)); errs, warns = [], []
    prose_for_parse = []
    for k, e in enumerate(d['edits']):
        where = f"edit {k} ({e.get('module')}[{e.get('index')}] {e.get('op')})"
        if own and e.get('module') not in own: errs.append(f'{where}: module not owned by this stream')
        if not e.get('reason'): errs.append(f'{where}: no reason')
        strict = str(e.get('module', '')).startswith(('exec/', 'ch2/', 'ch3/'))
        computed = set(map(str, e.get('computed', [])))
        for field, t in new_texts(e):
            is_prose = not field.endswith('cell') and not field.endswith('source') and not field.endswith('caption')
            if '–' in t or '—' in t: errs.append(f'{where}: dash in {field}: {t[:80]}')
            for m in BANNED.finditer(t): errs.append(f'{where}: banned word "{m.group(0)}"')
            for m in INTENS.finditer(t): warns.append(f'{where}: intensifier "{m.group(0)}"')
            if re.search(r'factbase', t, re.I): errs.append(f'{where}: names a factbase')
            body = strip_cites(t)
            for m in VERSIONING.finditer(body): errs.append(f'{where}: earlier tree or disposition: "{m.group(0)}"')
            if strict and is_prose:
                for m in CALLOUT.finditer(body): errs.append(f'{where}: names an interim deliverable in the text: "{m.group(0)}"')
            if re.search(r'\b(?:Tables?|Figures?) (?:ES|A|\d)\.\d', body): errs.append(f'{where}: cites a table or figure by number')
            for m in OXF.finditer(body): warns.append(f'{where}: possible Oxford comma: ...{body[max(0, m.start() - 30):m.end() + 10]}')
            if is_prose:
                for s in sentences(body):
                    if len(s.split()) > 35: errs.append(f'{where}: sentence of {len(s.split())} words: {s[:100]}')
                prose_for_parse.append((where, t))
            miss = sorted(nums(t) - ALLOWED_N - computed, key=lambda x: (len(x), x))
            if miss: errs.append(f'{where}: numbers found in neither the report, the extracts nor the factbases (list them under "computed" if you computed them): {miss}')
    # citations must parse into footnotes: run the renderer's own parser
    if prose_for_parse:
        js = ("const H=require(%s);const xs=JSON.parse(require('fs').readFileSync(0,'utf8'));"
              "const out=xs.map(([w,t])=>{const segs=H.citeSplit(t,true);const s=segs.filter(x=>typeof x==='string').join('');"
              "const bad=(s.match(/\\([^()]*\\b(?:19|20)\\d\\d\\b[^()]*\\)/g)||[]);return [w,bad];}).filter(x=>x[1].length);"
              "console.log(JSON.stringify(out));") % json.dumps(os.path.join(B, 'helpers.js'))
        r = subprocess.run(['node', '-e', js], input=json.dumps(prose_for_parse), capture_output=True, text=True, cwd=B)
        if r.returncode: errs.append('citation parse failed to run: ' + r.stderr[:300])
        else:
            for w, bad in json.loads(r.stdout or '[]'): errs.append(f'{w}: parenthesis with a year that does not parse as a citation: {bad}')
    for w in warns: print('WARN ', w)
    for e in errs: print('ERROR', e)
    print(f'{len(d["edits"])} edits; {len(errs)} errors, {len(warns)} warnings')
    sys.exit(1 if errs else 0)


if __name__ == '__main__':
    main()
