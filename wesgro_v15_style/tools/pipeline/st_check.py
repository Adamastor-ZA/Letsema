"""Check an editor's edits file.  usage: st_check.py edits_NAME.json SEC[,SEC...]"""
import sys
sys.path.insert(0, '/tmp/claude-0/-home-user-Letsema/98b96bfe-2843-55b4-9fb2-4f4083c56589/scratchpad/scripts')
from stp import *
path, secs = sys.argv[1], set(sys.argv[2].split(','))
E = json.load(open(path))
d = Doc(); store = load_store()
items = {it['pid']: it for it in walk(d)}
err, warn = [], []
rew = E.get('rewrites', {}); ins = E.get('inserts', []); dels = E.get('deletes', [])
for k in E:
    if k not in ('rewrites', 'inserts', 'deletes', 'queries', 'log', 'number_notes'): err.append('unknown key %s' % k)
after = collections.defaultdict(list)
for i in ins:
    if not {'after', 'style', 'text'} <= set(i): err.append('insert needs after, style, text: %s' % str(i)[:80]); continue
    after[i['after']].append(i)
    if i['after'] not in items: err.append('insert after unknown pid %s' % i['after'])
    elif items[i['after']]['sec'] not in secs: err.append('insert outside your sections: after %s' % i['after'])
    if i['style'] not in ('Body', 'BoxBody'): err.append('insert style must be Body or BoxBody: %s' % i['style'])
def text_checks(pid, t, style):
    for m in re.finditer(BANNED, ' ' + t + ' '):
        err.append('%s banned word or dash: %r' % (pid, m.group(0).strip()))
    if ' ' in t: err.append('%s contains a non-breaking space' % pid)
    if style in PROSE:
        for s in sents(t):
            n = len(s.split())
            if n > 35: err.append('%s sentence of %d words: %s...' % (pid, n, s[:70]))
        if re.search(r',\s(?:[\w\'-]+\s){0,3}[\w\'-]+,\s(and|or)\s', t): warn.append('%s possible Oxford comma' % pid)
        if t.count('**') % 2: err.append('%s unbalanced ** markers' % pid)
    if re.search(r'\{c\d+>|<c\d+\}|<<|>>', t): err.append('%s contains comment or highlight markers; remove them' % pid)
fn_old, fn_new = collections.Counter(), collections.Counter()
touched = set(rew) | set(dels) | set(after)
for pid in touched:
    if pid not in items: err.append('unknown pid %s' % pid); continue
    it = items[pid]
    if it['sec'] not in secs: err.append('%s is in section %s, outside your sections' % (pid, it['sec'])); continue
    old = cur(it, store)
    if pid in rew and pid in dels: err.append('%s both rewritten and deleted' % pid)
    if pid in rew and it['style'].startswith('Heading'): err.append('%s is a heading; headings must not change' % pid)
    new_parts = []
    if pid in rew: new_parts.append(rew[pid]); text_checks(pid, rew[pid], it['style'])
    elif pid not in dels: new_parts.append(old)
    for i in after.get(pid, []): new_parts.append(i['text']); text_checks('insert after ' + pid, i['text'], i['style'])
    new = ' '.join(new_parts)
    fo = collections.Counter(re.findall(r'\[\^\d+\]', old)); fn = collections.Counter(re.findall(r'\[\^\d+\]', new))
    fn_old += fo; fn_new += fn
    if pid in rew and rew[pid].strip() == old.strip(): warn.append('%s rewrite is identical to the current text; remove it' % pid)
    if pid not in dels:
        no, nn = nums(old), nums(new)
        if no != nn:
            lost = list((no - nn).elements()); added = list((nn - no).elements())
            note = E.get('number_notes', {}).get(pid)
            (warn if note else err).append('%s numbers differ: lost %s added %s%s' % (pid, lost, added, ' [note: %s]' % note if note else ' (add a number_notes entry explaining, or fix)'))
        wo, wn = wnums(old), wnums(new)
        if wo != wn and not E.get('number_notes', {}).get(pid):
            warn.append('%s number words differ: lost %s added %s' % (pid, list((wo - wn).elements()), list((wn - wo).elements())))
    else:
        warn.append('%s deleted: %s' % (pid, old[:90]))
if fn_old != fn_new:
    err.append('footnote markers differ overall: lost %s, added or duplicated %s' % (list((fn_old - fn_new).elements()), list((fn_new - fn_old).elements())))
for qy in E.get('queries', []):
    if not {'pid', 'issue'} <= set(qy): err.append('query needs pid and issue')
print('%d rewrites, %d inserts, %d deletes, %d queries' % (len(rew), len(ins), len(dels), len(E.get('queries', []))))
for w in warn: print('WARN', w)
for e in err: print('ERROR', e)
print('RESULT:', 'FAIL (%d errors)' % len(err) if err else 'OK')
sys.exit(1 if err else 0)
