"""Accept all tracked changes in the build tree -> wst/acc (proper row and paragraph removal)."""
import sys, shutil
sys.path.insert(0, '/tmp/claude-0/-home-user-Letsema/98b96bfe-2843-55b4-9fb2-4f4083c56589/scratchpad/scripts')
from dxst import *
WST = '/tmp/claude-0/-home-user-Letsema/98b96bfe-2843-55b4-9fb2-4f4083c56589/scratchpad/wst/'
shutil.rmtree(WST + 'acc', ignore_errors=True); shutil.copytree(WST + 'build', WST + 'acc')
d = Doc(WST + 'acc')
for root in (d.body, d.fnroot):
    for tr in list(root.iter(q('w:tr'))):
        if tr.find('w:trPr/w:del', NS) is not None: tr.getparent().remove(tr)
    for tbl in list(root.iter(q('w:tbl'))):
        if not tbl.findall(q('w:tr')): tbl.getparent().remove(tbl)
    for p in list(root.iter(q('w:p'))):
        if p.find('w:pPr/w:rPr/w:del', NS) is not None:
            live = [r for r in p.iter(q('w:r')) if r.getparent().tag != q('w:del') and (rtext(r).strip() or r.find(q('w:drawing')) is not None)]
            if not live and p.find('w:pPr/w:sectPr', NS) is None and p.getparent().tag != q('w:tc'):
                p.getparent().remove(p); continue
            if not live and p.getparent().tag == q('w:tc') and len(p.getparent().findall(q('w:p'))) > 1:
                p.getparent().remove(p); continue
    for e in list(root.iter(q('w:del'))):
        if e.getparent() is not None and e.getparent().tag in (q('w:p'),): e.getparent().remove(e)
        elif e.getparent() is not None: e.getparent().remove(e)
    for e in list(root.iter(q('w:ins'))):
        par = e.getparent()
        if par.tag in (q('w:rPr'), q('w:trPr')): par.remove(e); continue
        i = list(par).index(e)
        for c in list(e): par.insert(i, c); i += 1
        par.remove(e)
refs = {r.get(q('w:id')) for r in d.body.iter(q('w:footnoteReference'))}
for f in list(d.fnroot.findall(q('w:footnote'))):
    if f.get(q('w:type')) is None and f.get(q('w:id')) not in refs: d.fnroot.remove(f)
d.save()
print('accepted')
