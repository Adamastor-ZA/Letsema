"""Tracked-change engine: rewrite paragraphs as w:ins / w:del at word level.

Marked text syntax (new text): **bold**, [^n] footnote reference, \t tab. Comment range markers and
bookmarks are never part of the text; they are carried through in place.
"""
import copy, re, sys, difflib
from lxml import etree
sys.path.insert(0, '/tmp/claude-0/-home-user-Letsema/98b96bfe-2843-55b4-9fb2-4f4083c56589/scratchpad/s16')
from dxst import *

AUTHOR = 'Claude (update pass)'
DATE = '2026-11-11T12:00:00Z'
TOK = re.compile(r"\[\^\d+\]|\t|\s+|[\w$%]+(?:[.,'’/\-:][\w%]+)*|.", re.S)
BOLD_STYLES = ('Body', 'Lead', 'TableText', 'BoxBody', '')
INVIS = ('commentRangeStart', 'commentRangeEnd', 'bookmarkStart', 'bookmarkEnd', 'proofErr')


class Trk:
    def __init__(self, doc, start=20000):
        self.doc = doc
        self.n = start
        self.stats = {'paras': 0, 'ins': 0, 'del': 0, 'new_paras': 0, 'del_paras': 0}

    def mark(self, el):
        self.n += 1
        el.set(q('w:id'), str(self.n)); el.set(q('w:author'), AUTHOR); el.set(q('w:date'), DATE)
        return el

    def E(self, tag):
        return self.mark(etree.Element(q(tag)))

    # ---------- atoms
    def atoms(self, p):
        """-> (tokens, trailing_invisibles). token = dict(key, text, rpr, opaque(el or None), bold, pre=[invisible els])."""
        toks, pend = [], []
        bold_style = pstyle(p) in BOLD_STYLES
        for ch in p:
            tag = ch.tag.split('}')[1]
            if tag == 'pPr':
                continue
            if tag in INVIS:
                pend.append(ch); continue
            if tag != 'r':
                raise ValueError('unexpected child %s in %s' % (tag, p.get(q('w14:paraId'))))
            rpr = ch.find(q('w:rPr'))
            if ch.find(q('w:commentReference')) is not None:
                pend.append(ch); continue
            bold = bold_style and rpr is not None and rpr.find(q('w:b')) is not None
            kids = [c for c in ch if c.tag != q('w:rPr')]
            for c in kids:
                ct = c.tag.split('}')[1]
                if ct == 't':
                    for m in TOK.finditer(c.text or ''):
                        toks.append(dict(key=(m.group(0), bold and not m.group(0).isspace()), text=m.group(0), rpr=rpr, opaque=None, pre=pend, run=ch)); pend = []
                elif ct == 'tab':
                    toks.append(dict(key=('\t', False), text='\t', rpr=rpr, opaque=None, pre=pend, run=ch)); pend = []
                elif ct == 'footnoteReference':
                    toks.append(dict(key=('[^%s]' % c.get(q('w:id')), False), text=None, rpr=rpr, opaque=c, pre=pend, run=ch)); pend = []
                else:
                    # fields, drawings and breaks are carried through in place, never diffed
                    r2 = etree.Element(q('w:r'))
                    if rpr is not None:
                        r2.append(copy.deepcopy(rpr))
                    r2.append(copy.deepcopy(c))
                    pend.append(r2)
        return toks, pend

    @staticmethod
    def parse_new(s, bold_style):
        """marked string -> list of (text, bold)"""
        out = []
        parts = re.split(r'(\*\*.+?\*\*)', s, flags=re.S) if bold_style else [s]
        for part in parts:
            if not part:
                continue
            b = bold_style and part.startswith('**') and part.endswith('**') and len(part) > 4
            if b:
                part = part[2:-2]
            for m in TOK.finditer(part):
                t = m.group(0)
                out.append((t, False if t.startswith('[^') or t.isspace() else b))
        return out

    # ---------- run builders
    def _run(self, text, rpr, deleted=False):
        r = etree.Element(q('w:r'))
        if rpr is not None:
            r.append(copy.deepcopy(rpr))
        if text == '\t':
            etree.SubElement(r, q('w:tab'))
            return r
        t = etree.SubElement(r, q('w:delText') if deleted else q('w:t'))
        t.text = text
        t.set(XML_SPACE, 'preserve')
        return r

    def _opaque_run(self, tok, deleted=False):
        r = etree.Element(q('w:r'))
        if tok['rpr'] is not None:
            r.append(copy.deepcopy(tok['rpr']))
        r.append(copy.deepcopy(tok['opaque']))
        return r

    def _emit_old(self, toks, deleted):
        """group consecutive tokens of the same original run into runs"""
        out, buf, cur = [], [], None
        def flush():
            nonlocal buf, cur
            if buf:
                out.append(self._run(''.join(buf), cur['rpr'], deleted)); buf = []
        for t in toks:
            if t['opaque'] is not None or t['text'] == '\t':
                flush()
                out.append(self._opaque_run(t) if t['opaque'] is not None else self._run('\t', t['rpr'], deleted))
                cur = None
                continue
            if cur is not None and t['run'] is not cur['run']:
                flush()
            cur = t; buf.append(t['text'])
        flush()
        return out

    def _bold_rpr(self, rpr):
        rp = copy.deepcopy(rpr) if rpr is not None else etree.Element(q('w:rPr'))
        if rp.find(q('w:b')) is None:
            r = mkrun('x', rp if len(rp) else None, bold=True)
            return r.find(q('w:rPr'))
        return rp

    def _plain_rpr(self, rpr):
        if rpr is None:
            return None
        rp = copy.deepcopy(rpr)
        for t in ('w:b', 'w:bCs'):
            for e in rp.findall(q(t)):
                rp.remove(e)
        return rp if len(rp) else None

    def _fn_clone(self, fid):
        src = self.doc.fn(fid)
        new = copy.deepcopy(src)
        ids = [int(f.get(q('w:id'))) for f in self.doc.fnroot.findall(q('w:footnote'))]
        nid = max(ids) + 1
        new.set(q('w:id'), str(nid))
        for p in new.iter(q('w:p')):
            p.set(q('w14:paraId'), self.doc.new_pid())
        for p in new.iter(q('w:p')):
            runs = [c for c in p if c.tag == q('w:r')]
            if runs:
                ins = self.E('w:ins')
                p.insert(list(p).index(runs[0]), ins)
                for r in runs:
                    ins.append(r)
        self.doc.fnroot.append(new)
        self.stats['fn_clones'] = self.stats.get('fn_clones', 0) + 1
        return nid

    def _emit_new(self, items, p, neighbour_rpr, bold_style, fn_like):
        """items: [(text, bold)] -> runs for inside w:ins"""
        out, buf, curb = [], [], None
        base = body_rpr(p) if bold_style else neighbour_rpr
        def flush():
            nonlocal buf
            if buf:
                rp = base
                if bold_style:
                    rp = self._bold_rpr(base) if curb else self._plain_rpr(base)
                out.append(self._run(''.join(buf), rp)); buf = []
        for text, b in items:
            if text.startswith('[^') and text.endswith(']'):
                flush()
                fid = text[2:-1]
                nid = self._fn_clone(fid)
                r = etree.Element(q('w:r'))
                rp = etree.SubElement(r, q('w:rPr'))
                if fn_like is not None and fn_like.find(q('w:rPr')) is not None:
                    r.remove(rp); r.append(copy.deepcopy(fn_like.find(q('w:rPr'))))
                else:
                    etree.SubElement(rp, q('w:rStyle')).set(q('w:val'), 'FootnoteReference')
                etree.SubElement(r, q('w:footnoteReference')).set(q('w:id'), str(nid))
                out.append(r); continue
            if text == '\t':
                flush(); out.append(self._run('\t', base)); continue
            if curb is not None and b != curb:
                flush()
            curb = b; buf.append(text)
        flush()
        return out

    # ---------- paragraph rewrite
    def rewrite(self, p, new_marked):
        new_marked = re.sub(r'\{c\d+>|<c\d+\}', '', new_marked)
        bold_style = pstyle(p) in BOLD_STYLES
        old, trail = self.atoms(p)
        new = self.parse_new(new_marked, bold_style)
        a = [t['key'] for t in old]
        b = [(t, bb) for t, bb in new]
        if a == b:
            return False
        sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
        ops = [list(o) for o in sm.get_opcodes()]
        # smooth: short equal spans between two changes become part of the change
        def small(i1, i2):
            seg = a[i1:i2]
            if any(k[0].startswith('[^') or k[0].startswith('<') or k[0] == '\t' for k in seg):
                return False
            words = [k for k in seg if not k[0].isspace()]
            return len(words) <= 1 and len(seg) <= 3
        changed = True
        while changed:
            changed = False
            for i in range(1, len(ops) - 1):
                if ops[i][0] == 'equal' and ops[i-1][0] != 'equal' and ops[i+1][0] != 'equal' and small(ops[i][1], ops[i][2]):
                    merged = ['replace', ops[i-1][1], ops[i+1][2], ops[i-1][3], ops[i+1][4]]
                    ops[i-1:i+2] = [merged]; changed = True; break
        fn_like = next((t['run'] for t in old if t['opaque'] is not None and t['key'][0].startswith('[^')), None)
        if fn_like is None:
            fn_like = self._any_fn_run()
        children = []
        for tag, i1, i2, j1, j2 in ops:
            if tag == 'equal':
                grp = []
                for t in old[i1:i2]:
                    if t['pre']:
                        children.extend(self._emit_old(grp, False)); grp = []
                        children.extend(t['pre'])
                    grp.append(t)
                children.extend(self._emit_old(grp, False))
                continue
            if i2 > i1:
                for t in old[i1:i2]:
                    children.extend(t['pre'])
                d = self.E('w:del')
                for r in self._emit_old(old[i1:i2], True):
                    d.append(r)
                children.append(d); self.stats['del'] += 1
            if j2 > j1:
                nb = old[i1]['rpr'] if i2 > i1 else (old[i1-1]['rpr'] if i1 > 0 else (old[i1]['rpr'] if i1 < len(old) else None))
                ins = self.E('w:ins')
                for r in self._emit_new(b[j1:j2], p, nb, bold_style, fn_like):
                    ins.append(r)
                children.append(ins); self.stats['ins'] += 1
        children.extend(trail)
        for c in list(p):
            if c.tag != q('w:pPr'):
                p.remove(c)
        for c in children:
            p.append(c)
        self.stats['paras'] += 1
        return True

    def _any_fn_run(self):
        if not hasattr(self, '_fnr'):
            self._fnr = None
            for r in self.doc.body.iter(q('w:r')):
                if r.find(q('w:footnoteReference')) is not None:
                    self._fnr = r; break
        return self._fnr

    # ---------- paragraph marks
    def _mark_ppr(self, p, kind):
        ppr = p.find(q('w:pPr'))
        if ppr is None:
            ppr = etree.Element(q('w:pPr')); p.insert(0, ppr)
        rpr = ppr.find(q('w:rPr'))
        if rpr is None:
            rpr = etree.Element(q('w:rPr'))
            # rPr precedes sectPr and pPrChange
            pos = len(ppr)
            for i, c in enumerate(ppr):
                if c.tag in (q('w:sectPr'), q('w:pPrChange')):
                    pos = i; break
            ppr.insert(pos, rpr)
        for e in rpr.findall(q('w:ins')) + rpr.findall(q('w:del')):
            rpr.remove(e)
        rpr.insert(0, self.E('w:' + kind))

    def delete_para(self, p):
        """Delete the whole paragraph (content and mark)."""
        old, trail = self.atoms(p)
        children = []
        if old:
            for t in old:
                children.extend(t['pre'])
            d = self.E('w:del')
            for r in self._emit_old(old, True):
                d.append(r)
            children.append(d)
        children.extend(trail)
        for c in list(p):
            if c.tag != q('w:pPr'):
                p.remove(c)
        for c in children:
            p.append(c)
        self._mark_ppr(p, 'del')
        self.stats['del_paras'] += 1

    def new_para(self, like, marked, style=None):
        """New tracked paragraph with pPr copied from `like` (optionally restyled)."""
        p = etree.Element(q('w:p'))
        p.set(q('w14:paraId'), self.doc.new_pid()); p.set(q('w14:textId'), '77777777')
        ppr = like.find(q('w:pPr'))
        if ppr is not None:
            ppr = copy.deepcopy(ppr)
            for t in ('w:sectPr', 'w:pageBreakBefore', 'w:rPr'):
                for e in ppr.findall(q(t)):
                    ppr.remove(e)
            p.append(ppr)
        if style:
            ps = p.find('w:pPr/w:pStyle', NS)
            if ps is None:
                if p.find(q('w:pPr')) is None:
                    p.insert(0, etree.Element(q('w:pPr')))
                ps = etree.Element(q('w:pStyle')); p.find(q('w:pPr')).insert(0, ps)
            ps.set(q('w:val'), style)
        bold_style = pstyle(p) in BOLD_STYLES
        items = self.parse_new(marked, bold_style)
        if items:
            ins = self.E('w:ins')
            base = body_rpr(like)
            # _emit_new uses body_rpr(p) for bold styles; p has no runs yet, so pass like
            for r in self._emit_new(items, like, base, bold_style, self._any_fn_run()):
                ins.append(r)
            p.append(ins)
        self._mark_ppr(p, 'ins')
        self.stats['new_paras'] += 1
        return p

    # ---------- tables
    def delete_table(self, tbl):
        for tr in tbl.findall(q('w:tr')):
            trpr = tr.find(q('w:trPr'))
            if trpr is None:
                trpr = etree.Element(q('w:trPr'))
                pos = 0
                for i, c in enumerate(tr):
                    if c.tag in (q('w:tblPrEx'),):
                        pos = i + 1
                tr.insert(pos, trpr)
            trpr.append(self.E('w:del'))
            for p in tr.iter(q('w:p')):
                self.delete_para(p)

    def insert_table_copy(self, tbl):
        """Deep copy of tbl in its ORIGINAL state, marked as inserted. Call before delete_table."""
        new = copy.deepcopy(tbl)
        for tr in new.findall(q('w:tr')):
            trpr = tr.find(q('w:trPr'))
            if trpr is None:
                trpr = etree.Element(q('w:trPr'))
                pos = 0
                for i, c in enumerate(tr):
                    if c.tag in (q('w:tblPrEx'),):
                        pos = i + 1
                tr.insert(pos, trpr)
            trpr.append(self.E('w:ins'))
            for p in tr.iter(q('w:p')):
                p.set(q('w14:paraId'), self.doc.new_pid())
                runs = [c for c in p if c.tag == q('w:r')]
                if runs:
                    ins = self.E('w:ins')
                    p.insert(list(p).index(runs[0]), ins)
                    for r in runs:
                        ins.append(r)
                for c in list(p):
                    if c.tag.split('}')[1] in INVIS:
                        p.remove(c)
                for r in list(p.iter(q('w:r'))):
                    if r.find(q('w:commentReference')) is not None:
                        r.getparent().remove(r)
                self._mark_ppr(p, 'ins')
        return new

    def copy_para_inserted(self, p):
        """Copy of a paragraph (original state) as an inserted paragraph, e.g. a moved caption."""
        new = copy.deepcopy(p)
        new.set(q('w14:paraId'), self.doc.new_pid())
        for c in list(new):
            if c.tag.split('}')[1] in INVIS or (c.tag == q('w:r') and c.find(q('w:commentReference')) is not None):
                new.remove(c)
        runs = [c for c in new if c.tag == q('w:r')]
        if runs:
            ins = self.E('w:ins')
            new.insert(list(new).index(runs[0]), ins)
            for r in runs:
                ins.append(r)
        self._mark_ppr(new, 'ins')
        self.stats['new_paras'] += 1
        return new


def marked_plain(p):
    """Current text of p in the engine's syntax (no comment markers)."""
    out = []
    bold_style = pstyle(p) in BOLD_STYLES
    for ch in p:
        if ch.tag != q('w:r'):
            continue
        fr = ch.find(q('w:footnoteReference'))
        if fr is not None:
            out.append('[^%s]' % fr.get(q('w:id'))); continue
        t = rtext(ch)
        if not t:
            continue
        rpr = ch.find(q('w:rPr'))
        if bold_style and rpr is not None and rpr.find(q('w:b')) is not None:
            # keep surrounding whitespace outside the markers
            m = re.match(r'^(\s*)(.*?)(\s*)$', t, re.S)
            t = m.group(1) + ('**' + m.group(2) + '**' if m.group(2) else '') + m.group(3)
        out.append(t)
    s = ''.join(out)
    return re.sub(r'\*\*\*\*', '', s)
