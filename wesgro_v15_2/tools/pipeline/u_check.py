"""Check a comma-pass edits file.  usage: u_check.py work/commas_NAME.json SEC[,SEC...]"""
import sys, difflib
sys.path.insert(0, '/tmp/claude-0/-home-user-Letsema/98b96bfe-2843-55b4-9fb2-4f4083c56589/scratchpad/s16')
from stp import *
path, secs = sys.argv[1], set(sys.argv[2].split(','))
E = json.load(open(path)); d = Doc(); store = load_store()
items = {it['pid']: it for it in walk(d)}
PAT = re.compile(r', (and|or)\b')
rew = E.get('rewrites', {}); exc = E.get('exceptions', {})
err, warn = [], []
for k in E:
    if k not in ('rewrites', 'exceptions', 'log'): err.append('unknown key %s' % k)
def words(t): return re.findall(r"[A-Za-z0-9%$'’.\-/]+", re.sub(r'\[\^\d+\]|\*\*', ' ', t).lower())
need = 0
for pid, it in items.items():
    if it['sec'] not in secs or it['style'].startswith(('TOC', 'Heading')): continue
    old = cur(it, store)
    n = len(PAT.findall(old))
    if n:
        need += 1
        if pid not in rew and pid not in exc: err.append('%s still has ", and" or ", or" and is not in rewrites or exceptions: %s' % (pid, old[:70]))
for pid, new in rew.items():
    if pid not in items: err.append('unknown pid %s' % pid); continue
    it = items[pid]
    if it['sec'] not in secs: err.append('%s is outside your sections' % pid); continue
    old = cur(it, store)
    if PAT.search(new) and pid not in exc: err.append('%s still contains ", and" or ", or": %s' % (pid, PAT.search(new).group(0) + new[PAT.search(new).end():][:40]))
    if nums(old) != nums(new): err.append('%s numbers differ: lost %s added %s' % (pid, list((nums(old) - nums(new)).elements()), list((nums(new) - nums(old)).elements())))
    if re.findall(r'\[\^\d+\]', old) != re.findall(r'\[\^\d+\]', new): err.append('%s footnote markers changed' % pid)
    if re.findall(r'\[\[QUERY[^\]]*\]\]', old) != re.findall(r'\[\[QUERY[^\]]*\]\]', new): err.append('%s query placeholder changed' % pid)
    if old.count('**') != new.count('**'): err.append('%s bold markers changed' % pid)
    if re.search(r'[—–]', new): err.append('%s contains a dash' % pid)
    if re.search(r'(^|[.!?] )And ', new): err.append('%s has a sentence starting with "And"' % pid)
    ow, nw = words(old), words(new)
    sm = difflib.SequenceMatcher(None, ow, nw, autojunk=False)
    added = sum(j2 - j1 for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag in ('insert', 'replace'))
    removed = sum(i2 - i1 for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag in ('delete', 'replace'))
    sites = max(1, len(PAT.findall(old)))
    if not PAT.search(old): warn.append('%s had no ", and" to fix; remove it from rewrites unless it is needed' % pid)
    if added > 6 * sites or removed > 6 * sites: err.append('%s changes too much (%d words added, %d removed for %d site(s)); change only the comma construction' % (pid, added, removed, sites))
    elif added > 3 * sites or removed > 3 * sites: warn.append('%s: %d words added, %d removed for %d site(s); check it is minimal' % (pid, added, removed, sites))
    if it['style'] in PROSE:
        oldmax = max([len(s.split()) for s in sents(old)] or [0])
        for s in sents(new):
            if len(s.split()) > 35 and len(s.split()) > oldmax: err.append('%s sentence of %d words: %s' % (pid, len(s.split()), s[:60]))
    if new.strip() == old.strip(): warn.append('%s identical to current text' % pid)
for pid in exc:
    if pid in items and not PAT.search(cur(items[pid], store)) : warn.append('%s exception not needed' % pid)
print('%d paragraphs need a fix; %d rewrites, %d exceptions' % (need, len(rew), len(exc)))
for w in warn[:60]: print('WARN', w)
for e in err[:80]: print('ERROR', e)
print('RESULT:', 'FAIL (%d errors)' % len(err) if err else 'OK')
sys.exit(1 if err else 0)
