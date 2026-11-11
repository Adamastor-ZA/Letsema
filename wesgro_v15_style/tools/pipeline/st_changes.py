"""List every change in the build against the original, by section. -> work/changes_<part>.txt"""
import sys, difflib
sys.path.insert(0, '/tmp/claude-0/-home-user-Letsema/98b96bfe-2843-55b4-9fb2-4f4083c56589/scratchpad/scripts')
from stp import *
WST = '/tmp/claude-0/-home-user-Letsema/98b96bfe-2843-55b4-9fb2-4f4083c56589/scratchpad/wst/'
o = Doc(WST + 'unpacked'); b = Doc(WST + 'build')
def acc(p):
    return ''.join(('[^%s]' % r.find(q('w:footnoteReference')).get(q('w:id'))) if r.find(q('w:footnoteReference')) is not None else rtext(r)
                   for r in p.iter(q('w:r')) if r.getparent().tag != q('w:del'))
def orig(p):
    return ''.join(('[^%s]' % r.find(q('w:footnoteReference')).get(q('w:id'))) if r.find(q('w:footnoteReference')) is not None else rtext(r) for r in p.iter(q('w:r')))
def deleted(p): return p.find('w:pPr/w:rPr/w:del', NS) is not None
def inserted(p): return p.find('w:pPr/w:rPr/w:ins', NS) is not None
O = {it['pid']: it for it in walk(o)}
parts = collections.defaultdict(list); counts = collections.Counter()
def part(sec):
    if sec in ('ES', 'FRONT', 'COVER') or sec.startswith('1'): return '1_front_ES_ch1'
    if sec.startswith('2'): return '2_ch2'
    if sec.startswith('3'): return '3_ch3'
    return '4_ch4_ch5_appendices'
def inline(a, c):
    a, c = a.split(), c.split(); out = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, c, autojunk=False).get_opcodes():
        if tag == 'equal': out.append(' '.join(a[i1:i2]))
        else:
            if i2 > i1: out.append('[-' + ' '.join(a[i1:i2]) + '-]')
            if j2 > j1: out.append('{+' + ' '.join(c[j1:j2]) + '+}')
    return ' '.join(out)
for it in walk(b):
    pid, p = it['pid'], it['p']; sec = it['sec']; pt = part(sec)
    if it['style'].startswith('TOC'): continue
    new = acc(p)
    if pid in O and not inserted(p):
        old = orig(O[pid]['p'])
        if deleted(p) and not new.strip():
            if old.strip(): parts[pt].append('DELETED [%s|%s|%s] %s' % (sec, it['style'], pid, old)); counts['deleted'] += 1
        elif old != new:
            parts[pt].append('CHANGED [%s|%s|%s] %s' % (sec, it['style'], pid, inline(old, new))); counts['changed'] += 1
    else:
        if new.strip(): parts[pt].append('INSERTED [%s|%s] %s' % (sec, it['style'], new)); counts['inserted'] += 1
for k, v in parts.items():
    open(WORK + 'changes_%s.txt' % k, 'w').write('\n\n'.join(v) + '\n')
    print(k, len(v), 'entries', sum(len(x.split()) for x in v), 'words')
print(dict(counts))
