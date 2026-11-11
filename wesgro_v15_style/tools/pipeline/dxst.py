"""Core helpers for editing the unpacked docx in place (lxml, no pretty-printing)."""
import copy, random, re, sys
from lxml import etree

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
W14 = 'http://schemas.microsoft.com/office/word/2010/wordml'
NS = {'w': W, 'w14': W14,
      'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
      'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
XML_SPACE = '{http://www.w3.org/XML/1998/namespace}space'
ROOT = '/tmp/claude-0/-home-user-Letsema/98b96bfe-2843-55b4-9fb2-4f4083c56589/scratchpad/wst/unpacked'


def q(tag):
    p, t = tag.split(':')
    return '{%s}%s' % (NS[p], t)


class Doc:
    def __init__(self, root=ROOT):
        self.root = root
        self.dpath = root + '/word/document.xml'
        self.fpath = root + '/word/footnotes.xml'
        parser = etree.XMLParser(remove_blank_text=False)
        self.dtree = etree.parse(self.dpath, parser)
        self.ftree = etree.parse(self.fpath, parser)
        self.body = self.dtree.getroot().find(q('w:body'))
        self.fnroot = self.ftree.getroot()
        self._ids = set(self.dtree.getroot().xpath('//@w14:paraId', namespaces=NS))
        self._ids |= set(self.fnroot.xpath('//@w14:paraId', namespaces=NS))

    def save(self):
        self.dtree.write(self.dpath, xml_declaration=True, encoding='UTF-8', standalone=True)
        self.ftree.write(self.fpath, xml_declaration=True, encoding='UTF-8', standalone=True)

    # ---------- ids
    def new_pid(self):
        while True:
            v = '%08X' % random.randint(0x10000000, 0x7FFFFFFE)
            if v not in self._ids:
                self._ids.add(v)
                return v

    # ---------- lookup
    def P(self, pid):
        r = self.dtree.getroot().xpath('//w:p[@w14:paraId="%s"]' % pid, namespaces=NS)
        if len(r) != 1:
            raise KeyError('paraId %s matched %d' % (pid, len(r)))
        return r[0]

    def allp(self):
        return self.body.iter(q('w:p'))

    def find(self, needle, style=None, body_only=False):
        out = []
        it = self.body.findall(q('w:p')) if body_only else self.allp()
        for p in it:
            if style and pstyle(p) != style:
                continue
            if needle in ptext(p):
                out.append(p)
        return out

    def one(self, needle, style=None):
        r = self.find(needle, style)
        if len(r) != 1:
            raise KeyError('%r matched %d paragraphs' % (needle, len(r)))
        return r[0]

    def starts(self, needle, style=None):
        r = [p for p in self.allp() if ptext(p).startswith(needle) and (not style or pstyle(p) == style)]
        if len(r) != 1:
            raise KeyError('%r start-matched %d paragraphs' % (needle, len(r)))
        return r[0]

    # ---------- footnotes
    def fn(self, fid):
        r = self.fnroot.xpath('w:footnote[@w:id="%s"]' % fid, namespaces=NS)
        if len(r) != 1:
            raise KeyError('footnote %s matched %d' % (fid, len(r)))
        return r[0]

    def fn_text(self, fid):
        return ''.join(self.fn(fid).itertext()).strip()

    def fn_delete(self, fid):
        f = self.fn(fid)
        f.getparent().remove(f)

    def fn_set(self, fid, text):
        """Replace footnote text, keeping the footnoteRef run and the first text run's rPr."""
        f = self.fn(fid)
        p = f.find(q('w:p'))
        runs = p.findall(q('w:r'))
        ref = [r for r in runs if r.find(q('w:footnoteRef')) is not None]
        txt = [r for r in runs if r.find(q('w:t')) is not None]
        rpr = None
        for r in txt:
            if r.find(q('w:rPr')) is not None:
                rpr = copy.deepcopy(r.find(q('w:rPr')))
            break
        for r in runs:
            if r not in ref:
                p.remove(r)
        for extra in f.findall(q('w:p'))[1:]:
            f.remove(extra)
        p.append(mkrun(' ' + text.strip(), rpr))

    def fn_new(self, text, like=None):
        ids = [int(x) for x in self.fnroot.xpath('w:footnote/@w:id', namespaces=NS)]
        nid = max(ids) + 1
        if like is None:
            like = [i for i in ids if i > 0][0]
        f = copy.deepcopy(self.fn(like))
        f.set(q('w:id'), str(nid))
        for p in f.iter(q('w:p')):
            if p.get(q('w14:paraId')):
                p.set(q('w14:paraId'), self.new_pid())
        self.fnroot.append(f)
        self.fn_set(nid, text)
        return nid

    def fn_ref_run(self, fid, like=None):
        """A footnoteReference run; copy rPr from an existing reference run."""
        if like is None:
            like = self.body.xpath('.//w:r[w:footnoteReference]', namespaces=NS)[0]
        r = copy.deepcopy(like)
        r.find(q('w:footnoteReference')).set(q('w:id'), str(fid))
        return r


# ---------- text helpers
def pstyle(p):
    s = p.find('w:pPr/w:pStyle', NS)
    return s.get(q('w:val')) if s is not None else ''


def rtext(r):
    out = []
    for c in r:
        if c.tag == q('w:t'):
            out.append(c.text or '')
        elif c.tag == q('w:tab'):
            out.append('\t')
        elif c.tag in (q('w:br'), q('w:cr')):
            out.append('\n')
        elif c.tag == q('w:noBreakHyphen'):
            out.append('-')
    return ''.join(out)


def ptext(p):
    return ''.join(rtext(r) for r in p.iter(q('w:r')))


def is_hl(r):
    return r.find('w:rPr/w:highlight', NS) is not None


def pmarked(p):
    """Text with markers: [^n] footnotes, {cN> <cN} comment ranges, <<..>> highlight, **bold**."""
    out = []
    for el in p.iter():
        if el.tag == q('w:commentRangeStart'):
            out.append('{c%s>' % el.get(q('w:id')))
        elif el.tag == q('w:commentRangeEnd'):
            out.append('<c%s}' % el.get(q('w:id')))
        elif el.tag == q('w:r'):
            fr = el.find(q('w:footnoteReference'))
            if fr is not None:
                out.append('[^%s]' % fr.get(q('w:id')))
                continue
            if el.find(q('w:drawing')) is not None:
                out.append('<IMG %s>' % ','.join(el.xpath('.//a:blip/@r:embed', namespaces=NS)))
            if el.find(q('w:br')) is not None and el.find(q('w:br')).get(q('w:type')) == 'page':
                out.append('<PAGEBREAK>')
            t = rtext(el)
            if not t:
                continue
            if is_hl(el):
                t = '<<' + t + '>>'
            elif el.find('w:rPr/w:b', NS) is not None and pstyle(p) in ('Body', 'Lead', 'TableText', ''):
                t = '**' + t + '**'
            elif el.find('w:rPr/w:i', NS) is not None:
                t = '_' + t + '_'
            out.append(t)
    return ''.join(out)


def mkrun(text, rpr=None, bold=False, italic=False, highlight=False):
    r = etree.Element(q('w:r'))
    if rpr is not None:
        rp = copy.deepcopy(rpr)
    else:
        rp = None
    if bold or italic or highlight:
        if rp is None:
            rp = etree.Element(q('w:rPr'))
        # schema order: rStyle, rFonts, b, bCs, i, iCs, ..., color, ..., sz, szCs, highlight, ...
        def ins(tag, before):
            if rp.find(q(tag)) is not None:
                return
            el = etree.Element(q(tag))
            for i, c in enumerate(rp):
                if c.tag.split('}')[1] in before:
                    rp.insert(i, el)
                    return el
            rp.append(el)
            return el
        after_b = ['i', 'iCs', 'caps', 'smallCaps', 'strike', 'dstrike', 'outline', 'shadow', 'emboss', 'imprint',
                   'noProof', 'snapToGrid', 'vanish', 'webHidden', 'color', 'spacing', 'w', 'kern', 'position', 'sz',
                   'szCs', 'highlight', 'u', 'effect', 'bdr', 'shd', 'fitText', 'vertAlign', 'rtl', 'cs', 'em', 'lang']
        if bold:
            ins('w:b', ['bCs'] + after_b)
            ins('w:bCs', after_b)
        if italic:
            ins('w:i', after_b[1:])
            ins('w:iCs', after_b[2:])
        if highlight:
            h = ins('w:highlight', after_b[after_b.index('u'):])
            if h is not None:
                h.set(q('w:val'), 'yellow')
    if rp is not None and len(rp):
        r.append(rp)
    t = etree.SubElement(r, q('w:t'))
    t.text = text
    t.set(XML_SPACE, 'preserve')
    return r


def body_rpr(p):
    """rPr of the first plain (non-bold, non-highlight, non-footnote) text run, or None."""
    cand = None
    for r in p.findall(q('w:r')):
        if r.find(q('w:t')) is None:
            continue
        rp = r.find(q('w:rPr'))
        if rp is None:
            return None
        if rp.find(q('w:highlight')) is None and rp.find(q('w:b')) is None and rp.find(q('w:i')) is None:
            return rp
        if cand is None:
            cand = rp
    if cand is not None:
        rp = copy.deepcopy(cand)
        for t in ('w:highlight', 'w:b', 'w:bCs', 'w:i', 'w:iCs'):
            for e in rp.findall(q(t)):
                rp.remove(e)
        return rp if len(rp) else None
    return None


SEG = re.compile(r'(\*\*.+?\*\*|<<.+?>>|__.+?__)', re.S)


def parse_segments(s):
    """'**bold** text <<open item>> __italic__' -> [(text, kind)]"""
    out = []
    for part in SEG.split(s):
        if not part:
            continue
        if part.startswith('**') and part.endswith('**'):
            out.append((part[2:-2], 'b'))
        elif part.startswith('<<') and part.endswith('>>'):
            out.append((part[2:-2], 'h'))
        elif part.startswith('__') and part.endswith('__'):
            out.append((part[2:-2], 'i'))
        else:
            out.append((part, ''))
    return out


def rewrite_paragraph(p, segments, keep_fn=True, fn_runs=None, keep_comments=True):
    """Replace the text of p.

    segments: a marked string or list of (text, kind) with kind in '', 'b', 'h', 'i'.
    Keeps pPr; builds runs from the existing body-text rPr; keeps footnote reference runs at the
    end (in order); keeps comment range markers (start at the front, end + reference at the back).
    fn_runs: explicit list of footnote reference runs to place at the end instead of the existing ones.
    """
    if isinstance(segments, str):
        segments = parse_segments(segments)
    rpr = body_rpr(p)
    cstart = p.findall(q('w:commentRangeStart')) if keep_comments else []
    cend = p.findall(q('w:commentRangeEnd')) if keep_comments else []
    cref = [r for r in p.findall(q('w:r')) if r.find(q('w:commentReference')) is not None] if keep_comments else []
    fns = [r for r in p.iter(q('w:r')) if r.find(q('w:footnoteReference')) is not None] if keep_fn else []
    if fn_runs is not None:
        fns = fn_runs
    for c in list(p):
        if c.tag != q('w:pPr'):
            p.remove(c)
    for c in cstart:
        p.append(c)
    for text, kind in segments:
        p.append(mkrun(text, rpr, bold=(kind == 'b'), highlight=(kind == 'h'), italic=(kind == 'i')))
    for r in fns:
        p.append(r)
    # each commentRangeEnd is followed by its reference run
    for e in cend:
        p.append(e)
        cid = e.get(q('w:id'))
        for r in cref:
            if r.find(q('w:commentReference')).get(q('w:id')) == cid:
                p.append(r)
    for r in cref:
        if r.getparent() is None:
            p.append(r)
    return p


def clone_para(doc, like, segments, style=None):
    """New paragraph copying pPr (and body rPr) from `like`, with new text. No footnotes/comments carried."""
    p = etree.Element(q('w:p'))
    p.set(q('w14:paraId'), doc.new_pid())
    p.set(q('w14:textId'), '77777777')
    ppr = like.find(q('w:pPr'))
    if ppr is not None:
        ppr = copy.deepcopy(ppr)
        for e in ppr.findall(q('w:sectPr')):
            ppr.remove(e)
        for e in ppr.findall(q('w:pageBreakBefore')):
            ppr.remove(e)
        p.append(ppr)
    rpr = body_rpr(like)
    if isinstance(segments, str):
        segments = parse_segments(segments)
    for text, kind in segments:
        p.append(mkrun(text, rpr, bold=(kind == 'b'), highlight=(kind == 'h'), italic=(kind == 'i')))
    return p


def has_sect(p):
    return p.find('w:pPr/w:sectPr', NS) is not None


def fn_ids(el):
    return [x for x in el.xpath('.//w:footnoteReference/@w:id', namespaces=NS)]


def delete_block(doc, el, drop_fn=True):
    """Delete a body-level paragraph or table, and its footnotes."""
    if el.tag == q('w:p') and has_sect(el):
        raise ValueError('refusing to delete sectPr paragraph: ' + ptext(el)[:60])
    if el.xpath('.//w:commentRangeStart|.//w:commentRangeEnd|.//w:commentReference', namespaces=NS):
        raise ValueError('block carries comment markers: ' + ptext(el)[:60] if el.tag == q('w:p') else 'table w/ comment')
    if drop_fn:
        for fid in fn_ids(el):
            doc.fn_delete(fid)
    el.getparent().remove(el)


def strip_comment(doc, cid):
    """Remove all markers for comment cid from document.xml."""
    n = 0
    for tag in ('w:commentRangeStart', 'w:commentRangeEnd'):
        for e in doc.body.xpath('.//%s[@w:id="%s"]' % (tag, cid), namespaces=NS):
            e.getparent().remove(e)
            n += 1
    for e in doc.body.xpath('.//w:r[w:commentReference[@w:id="%s"]]' % cid, namespaces=NS):
        e.getparent().remove(e)
        n += 1
    return n


def dump(doc, path):
    lines = []
    for i, el in enumerate(doc.body):
        if el.tag == q('w:p'):
            flags = ''
            if el.find('w:pPr/w:pageBreakBefore', NS) is not None:
                flags += 'B'
            if has_sect(el):
                flags += 'S'
            lines.append('%d|%s|%s%s| %s' % (i, el.get(q('w14:paraId')), pstyle(el), ('/' + flags) if flags else '', pmarked(el)))
        elif el.tag == q('w:tbl'):
            rows = el.findall(q('w:tr'))
            lines.append('%d|TABLE %d rows' % (i, len(rows)))
            for ri, tr in enumerate(rows):
                cells = []
                for tc in tr.findall(q('w:tc')):
                    cells.append(' ¶ '.join('%s:%s' % (pp.get(q('w14:paraId')), pmarked(pp)) for pp in tc.findall(q('w:p'))))
                lines.append('   r%d: ' % ri + ' || '.join(cells))
        else:
            lines.append('%d|%s' % (i, el.tag.split('}')[1]))
    open(path, 'w').write('\n'.join(lines) + '\n')
    return len(lines)


if __name__ == '__main__':
    d = Doc(sys.argv[2] if len(sys.argv) > 2 else ROOT)
    print(dump(d, sys.argv[1]))


# ---------- added helpers
def body_range(doc, start_pid, end_pid):
    a = doc.P(start_pid); b = doc.P(end_pid)
    kids = list(doc.body)
    i, j = kids.index(a), kids.index(b)
    assert i <= j
    return kids[i:j + 1]


def insert_after(ref, *els):
    par = ref.getparent()
    idx = par.index(ref)
    for k, e in enumerate(els):
        par.insert(idx + 1 + k, e)


def insert_before(ref, *els):
    par = ref.getparent()
    idx = par.index(ref)
    for k, e in enumerate(els):
        par.insert(idx + k, e)


def note(msg):
    open('/tmp/claude-0/-home-user-Letsema/98b96bfe-2843-55b4-9fb2-4f4083c56589/scratchpad/wst/notes.md', 'a').write(msg.rstrip() + '\n')


def cell_set(doc, pid, segments):
    """Rewrite a table-cell paragraph by paraId."""
    return rewrite_paragraph(doc.P(pid), segments)


def replace_in_para(p, old, new, count=1):
    """Replace text inside a single run of p (after run merging). Raises if not found in one run."""
    n = 0
    for r in p.iter(q('w:r')):
        for t in r.findall(q('w:t')):
            if t.text and old in t.text:
                t.text = t.text.replace(old, new, count if count else -1)
                t.set(XML_SPACE, 'preserve')
                n += 1
                if count and n >= count:
                    return n
    if n == 0:
        raise KeyError('%r not found in a single run of: %s' % (old, ptext(p)[:80]))
    return n


def caption_set(p, label=None, title=None):
    """Caption paragraphs: first text run is the bold coloured label ('Table 1.1. '), the rest the title."""
    runs = [r for r in p.findall(q('w:r')) if r.find(q('w:t')) is not None]
    if label is not None:
        runs[0].find(q('w:t')).text = label
        runs[0].find(q('w:t')).set(XML_SPACE, 'preserve')
    if title is not None:
        runs[1].find(q('w:t')).text = title
        for r in runs[2:]:
            p.remove(r)


def mk_caption(doc, like, label, title, keep_next=True):
    p = copy.deepcopy(like)
    p.set(q('w14:paraId'), doc.new_pid())
    for e in p.xpath('.//w:commentRangeStart|.//w:commentRangeEnd|.//w:r[w:commentReference]|.//w:r[w:footnoteReference]', namespaces=NS):
        e.getparent().remove(e)
    caption_set(p, label, title)
    return p


def mk_styled(doc, style, segments, keep_next=False, rpr_xml=None):
    """New paragraph with a given pStyle and plain runs."""
    p = etree.Element(q('w:p'))
    p.set(q('w14:paraId'), doc.new_pid()); p.set(q('w14:textId'), '77777777')
    ppr = etree.SubElement(p, q('w:pPr'))
    ps = etree.SubElement(ppr, q('w:pStyle')); ps.set(q('w:val'), style)
    if keep_next:
        etree.SubElement(ppr, q('w:keepNext'))
    if isinstance(segments, str):
        segments = parse_segments(segments)
    for text, kind in segments:
        p.append(mkrun(text, None, bold=(kind == 'b'), highlight=(kind == 'h'), italic=(kind == 'i')))
    return p


def reanchor(doc, cid, p_start, p_end=None):
    """Move comment cid so it spans p_start..p_end (whole paragraphs)."""
    cid = str(cid)
    refs = doc.body.xpath('.//w:r[w:commentReference[@w:id="%s"]]' % cid, namespaces=NS)
    ref = copy.deepcopy(refs[0]) if refs else None
    if ref is None:
        ref = etree.fromstring('<w:r xmlns:w="%s"><w:rPr><w:rStyle w:val="CommentReference"/></w:rPr><w:commentReference w:id="%s"/></w:r>' % (W, cid))
    strip_comment(doc, cid)
    p_end = p_end if p_end is not None else p_start
    s = etree.Element(q('w:commentRangeStart')); s.set(q('w:id'), cid)
    ppr = p_start.find(q('w:pPr'))
    if ppr is not None:
        ppr.addnext(s)
    else:
        p_start.insert(0, s)
    e = etree.Element(q('w:commentRangeEnd')); e.set(q('w:id'), cid)
    p_end.append(e); p_end.append(ref)


def fn_attach(doc, p, text, like_id=None):
    """Create a new footnote and append its reference run to p."""
    nid = doc.fn_new(text, like=like_id)
    p.append(doc.fn_ref_run(nid))
    return nid


TBLPR = ('<w:tblPr><w:tblW w:w="9412" w:type="dxa"/><w:tblBorders><w:top w:val="single" w:sz="4" w:space="0" w:color="C8C9CB"/>'
         '<w:left w:val="none" w:sz="0" w:space="0" w:color="FFFFFF"/><w:bottom w:val="single" w:sz="4" w:space="0" w:color="C8C9CB"/>'
         '<w:right w:val="none" w:sz="0" w:space="0" w:color="FFFFFF"/><w:insideH w:val="single" w:sz="4" w:space="0" w:color="C8C9CB"/>'
         '<w:insideV w:val="none" w:sz="0" w:space="0" w:color="FFFFFF"/></w:tblBorders><w:tblLayout w:type="fixed"/>'
         '<w:tblCellMar><w:left w:w="10" w:type="dxa"/><w:right w:w="10" w:type="dxa"/></w:tblCellMar>'
         '<w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0" w:firstColumn="1" w:lastColumn="0" w:noHBand="0" w:noVBand="1"/></w:tblPr>')
TCMAR = '<w:tcMar><w:top w:w="60" w:type="dxa"/><w:left w:w="90" w:type="dxa"/><w:bottom w:w="60" w:type="dxa"/><w:right w:w="90" w:type="dxa"/></w:tcMar>'
TBLPREX = '<w:tblPrEx><w:tblCellMar><w:top w:w="0" w:type="dxa"/><w:bottom w:w="0" w:type="dxa"/></w:tblCellMar></w:tblPrEx>'


def xesc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def _cellp(doc, text, style, bold=False, keep_next=False):
    """One or more paragraphs for a cell; text may contain \\n for paragraph breaks and ** for bold."""
    out = []
    for line in text.split('\n'):
        runs = ''
        for seg, kind in parse_segments(line):
            rpr = '<w:rPr><w:b/><w:bCs/></w:rPr>' if (bold or kind == 'b') else ('<w:rPr><w:highlight w:val="yellow"/></w:rPr>' if kind == 'h' else '')
            runs += '<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r>' % (rpr, xesc(seg))
        out.append('<w:p w14:paraId="%s" w14:textId="77777777"><w:pPr><w:pStyle w:val="%s"/>%s</w:pPr>%s</w:p>'
                   % (doc.new_pid(), style, '<w:keepNext/>' if keep_next else '', runs))
    return ''.join(out)


def mk_table(doc, widths, header, rows, bold_first=True):
    """Report-style table: dark header row, zebra body rows, TableHead/TableText styles."""
    assert sum(widths) == 9412, sum(widths)
    x = ['<w:tbl xmlns:w="%s" xmlns:w14="%s">' % (W, W14), TBLPR, '<w:tblGrid>']
    x += ['<w:gridCol w:w="%d"/>' % w for w in widths]
    x.append('</w:tblGrid>')
    x.append('<w:tr>%s<w:trPr><w:cantSplit/><w:tblHeader/></w:trPr>' % TBLPREX)
    for w, h in zip(widths, header):
        x.append('<w:tc><w:tcPr><w:tcW w:w="%d" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="4D4D4F"/>%s<w:vAlign w:val="bottom"/></w:tcPr>%s</w:tc>'
                 % (w, TCMAR, _cellp(doc, h, 'TableHead', keep_next=True)))
    x.append('</w:tr>')
    for i, row in enumerate(rows, 1):
        shd = '<w:shd w:val="clear" w:color="auto" w:fill="F5F6F7"/>' if i % 2 == 0 else ''
        x.append('<w:tr>%s<w:trPr><w:cantSplit/></w:trPr>' % TBLPREX)
        for j, (w, c) in enumerate(zip(widths, row)):
            x.append('<w:tc><w:tcPr><w:tcW w:w="%d" w:type="dxa"/>%s%s</w:tcPr>%s</w:tc>'
                     % (w, shd, TCMAR, _cellp(doc, c, 'TableText', bold=(bold_first and j == 0))))
        x.append('</w:tr>')
    x.append('</w:tbl>')
    return etree.fromstring(''.join(x))


# ---------- figure tables (native Word tables standing in for diagrams)
def fig_table(doc, grid, rows, font_sz=17):
    """grid: list of column widths (sum 9412). rows: list of rows; a row is 'arrow' or a list of cells.
    cell = dict(span=int, fill=hex|None, lines=[(text, style)], align='left'|'center') with style a string of
    flags: b bold, i italic, w white, s small-caps-free uppercase label."""
    assert sum(grid) == 9412, sum(grid)
    B = '<w:{0} w:val="single" w:sz="4" w:space="0" w:color="C8C9CB"/>'
    x = ['<w:tbl xmlns:w="%s" xmlns:w14="%s"><w:tblPr><w:tblW w:w="9412" w:type="dxa"/><w:jc w:val="center"/><w:tblBorders>' % (W, W14)]
    x += [B.format(s) for s in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV')]
    x.append('</w:tblBorders><w:tblLayout w:type="fixed"/><w:tblCellMar><w:left w:w="10" w:type="dxa"/><w:right w:w="10" w:type="dxa"/></w:tblCellMar>'
             '<w:tblLook w:val="04A0" w:firstRow="0" w:lastRow="0" w:firstColumn="0" w:lastColumn="0" w:noHBand="1" w:noVBand="1"/></w:tblPr><w:tblGrid>')
    x += ['<w:gridCol w:w="%d"/>' % w for w in grid]
    x.append('</w:tblGrid>')
    n = len(rows)
    for ri, row in enumerate(rows):
        kn = '<w:keepNext/>' if ri < n - 1 else ''
        if row == 'arrow':
            x.append('<w:tr><w:trPr><w:cantSplit/><w:trHeight w:val="200" w:hRule="atLeast"/></w:trPr><w:tc><w:tcPr><w:tcW w:w="9412" w:type="dxa"/><w:gridSpan w:val="%d"/>'
                     '<w:tcBorders><w:left w:val="nil"/><w:right w:val="nil"/></w:tcBorders><w:vAlign w:val="center"/></w:tcPr>'
                     '<w:p w14:paraId="%s" w14:textId="77777777"><w:pPr><w:pStyle w:val="TableText"/>%s<w:spacing w:before="0" w:after="0" w:line="200" w:lineRule="exact"/><w:jc w:val="center"/></w:pPr>'
                     '<w:r><w:rPr><w:color w:val="4D4D4F"/><w:sz w:val="16"/><w:szCs w:val="16"/></w:rPr><w:t>↓</w:t></w:r></w:p></w:tc></w:tr>' % (len(grid), doc.new_pid(), kn))
            continue
        x.append('<w:tr><w:trPr><w:cantSplit/></w:trPr>')
        gi = 0
        for c in row:
            span = c.get('span', 1)
            w = sum(grid[gi:gi + span]); gi += span
            fill = c.get('fill')
            shd = '<w:shd w:val="clear" w:color="auto" w:fill="%s"/>' % fill if fill else ''
            gs = '<w:gridSpan w:val="%d"/>' % span if span > 1 else ''
            x.append('<w:tc><w:tcPr><w:tcW w:w="%d" w:type="dxa"/>%s%s%s<w:vAlign w:val="center"/></w:tcPr>' % (w, gs, shd, TCMAR))
            lines = c.get('lines') or [('', '')]
            for text, st in lines:
                rp = ''
                if 'b' in st: rp += '<w:b/><w:bCs/>'
                if 'i' in st: rp += '<w:i/><w:iCs/>'
                if 'w' in st: rp += '<w:color w:val="FFFFFF"/>'
                rp += '<w:sz w:val="%d"/><w:szCs w:val="%d"/>' % (font_sz, font_sz)
                jc = '<w:jc w:val="center"/>' if c.get('align') == 'center' else ''
                x.append('<w:p w14:paraId="%s" w14:textId="77777777"><w:pPr><w:pStyle w:val="TableText"/>%s<w:spacing w:before="0" w:after="20"/>%s</w:pPr>'
                         '<w:r><w:rPr>%s</w:rPr><w:t xml:space="preserve">%s</w:t></w:r></w:p>' % (doc.new_pid(), kn, jc, rp, xesc(text)))
            x.append('</w:tc>')
        assert gi == len(grid), (gi, row)
        x.append('</w:tr>')
    x.append('</w:tbl>')
    return etree.fromstring(''.join(x))


def tr_of(p):
    a = p
    while a is not None and a.tag != q('w:tr'):
        a = a.getparent()
    return a


def restripe(tbl, fill='F5F6F7'):
    """Zebra: data row i (1-based) shaded when even."""
    for i, tr in enumerate(tbl.findall(q('w:tr'))):
        if i == 0:
            continue
        for tc in tr.findall(q('w:tc')):
            tcpr = tc.find(q('w:tcPr'))
            shd = tcpr.find(q('w:shd'))
            if i % 2 == 0:
                if shd is None:
                    shd = etree.Element(q('w:shd'))
                    # shd goes after tcW/gridSpan/vMerge/tcBorders and before noWrap/tcMar
                    idx = 0
                    for k, c in enumerate(tcpr):
                        if c.tag.split('}')[1] in ('tcW', 'gridSpan', 'vMerge', 'hMerge', 'tcBorders'):
                            idx = k + 1
                    tcpr.insert(idx, shd)
                shd.set(q('w:val'), 'clear'); shd.set(q('w:color'), 'auto'); shd.set(q('w:fill'), fill)
            elif shd is not None:
                tcpr.remove(shd)


def clone_row(doc, tr, texts):
    """Copy a table row; set each cell to one paragraph with the given marked text (first para's format kept)."""
    new = copy.deepcopy(tr)
    if new.get(q('w14:paraId')):
        new.set(q('w14:paraId'), doc.new_pid())
    for e in new.xpath('.//w:commentRangeStart|.//w:commentRangeEnd|.//w:r[w:commentReference]|.//w:r[w:footnoteReference]', namespaces=NS):
        e.getparent().remove(e)
    cells = new.findall(q('w:tc'))
    assert len(cells) == len(texts), (len(cells), len(texts))
    for tc, t in zip(cells, texts):
        ps = tc.findall(q('w:p'))
        for extra in ps[1:]:
            tc.remove(extra)
        p = ps[0]
        p.set(q('w14:paraId'), doc.new_pid())
        bold = p.find('w:r/w:rPr/w:b', NS) is not None
        for c in list(p):
            if c.tag != q('w:pPr'):
                p.remove(c)
        for seg, kind in parse_segments(t):
            p.append(mkrun(seg, None, bold=(bold or kind == 'b'), highlight=(kind == 'h')))
    return new


def tbl_of(p):
    a = p
    while a is not None and a.tag != q('w:tbl'):
        a = a.getparent()
    return a


def replace_all(doc, old, new, footnotes=False, skip_styles=()):
    """Replace text within single runs across the whole document. Returns list of (paraId, context)."""
    hits = []
    roots = [doc.body] + ([doc.fnroot] if footnotes else [])
    for root in roots:
        for p in root.iter(q('w:p')):
            if pstyle(p) in skip_styles:
                continue
            for t in p.iter(q('w:t')):
                if t.text and old in t.text:
                    t.text = t.text.replace(old, new)
                    t.set(XML_SPACE, 'preserve')
                    hits.append(p.get(q('w14:paraId')))
    return hits


def fig_cell_runs(text, st, font_sz):
    """Runs for a figure-table line; '**x**' inside text makes that part bold."""
    out = ''
    for seg, kind in parse_segments(text):
        rp = ''
        if 'b' in st or kind == 'b': rp += '<w:b/><w:bCs/>'
        if 'i' in st: rp += '<w:i/><w:iCs/>'
        if 'w' in st: rp += '<w:color w:val="FFFFFF"/>'
        rp += '<w:sz w:val="%d"/><w:szCs w:val="%d"/>' % (font_sz, font_sz)
        out += '<w:r><w:rPr>%s</w:rPr><w:t xml:space="preserve">%s</w:t></w:r>' % (rp, xesc(seg))
    return out


# ---------- v14 helpers
def add_after(doc, ref, texts, like=None):
    """Insert new Body paragraphs (no footnotes) after `ref` (paragraph element). Returns the new paragraphs."""
    like = like if like is not None else ref
    ps = [clone_para(doc, like, t) for t in texts]
    insert_after(ref, *ps)
    return ps


def add_before(doc, ref, texts, like):
    ps = [clone_para(doc, like, t) for t in texts]
    insert_before(ref, *ps)
    return ps


def ptxt(doc, pid):
    return ptext(doc.P(pid))


def para_fn(doc, pid):
    f = fn_ids(doc.P(pid))
    return (f[0], doc.fn_text(f[0])) if f else None


A7_HEAD = '7D07E0C7'
RLOG = []


def rlog(obj, init, decision, what, why):
    """Record a re-evaluation decision for the change log."""
    RLOG.append((obj, init, decision, what, why))
    note('  - REEVAL | obj %s | %s | %s | %s | because: %s' % (obj, init, decision, what, why))


def ev_row(doc, after_pid, cells):
    """Add an evidence-table row after the row holding paragraph after_pid."""
    tr = tr_of(doc.P(after_pid)); new = clone_row(doc, tr, cells); tr.addnext(new); restripe(tbl_of(new.find(q('w:tc')).find(q('w:p')))); return new


def _a7_row(doc, action_text):
    t = tbl_of(doc.P(A7_HEAD))
    hits = [tr for tr in t.findall(q('w:tr')) if ptext(tr.findall(q('w:tc'))[3].find(q('w:p'))).strip() == action_text.strip()]
    if len(hits) != 1:
        raise KeyError('A7 rows matching %r: %d' % (action_text[:60], len(hits)))
    return hits[0]


def wa_add(doc, after_action_pid, who, action, lead, init, obj, a7_after_text=None):
    """Add a who-acts row after the row holding after_action_pid and the matching A7 row."""
    anchor = doc.P(after_action_pid); tr = tr_of(anchor)
    a7 = _a7_row(doc, a7_after_text if a7_after_text else ptext(anchor))
    new = clone_row(doc, tr, [who, action, lead]); tr.addnext(new); restripe(tbl_of(anchor))
    n7 = clone_row(doc, a7, [init, str(obj), who, action, lead]); a7.addnext(n7); restripe(tbl_of(doc.P(A7_HEAD)))
    return new


def wa_change(doc, action_pid, new_action=None, new_lead=None, new_who=None):
    p = doc.P(action_pid); tr = tr_of(p); a7 = _a7_row(doc, ptext(p))
    cells = tr.findall(q('w:tc')); a7c = a7.findall(q('w:tc'))
    if new_action is not None:
        rewrite_paragraph(p, new_action); rewrite_paragraph(a7c[3].find(q('w:p')), new_action)
    if new_lead is not None:
        rewrite_paragraph(cells[2].find(q('w:p')), new_lead); rewrite_paragraph(a7c[4].find(q('w:p')), new_lead)
    if new_who is not None:
        rewrite_paragraph(cells[0].find(q('w:p')), new_who); rewrite_paragraph(a7c[2].find(q('w:p')), new_who)


def wa_drop(doc, action_pid):
    p = doc.P(action_pid); tr = tr_of(p); a7 = _a7_row(doc, ptext(p)); t = tbl_of(p)
    tr.getparent().remove(tr); a7.getparent().remove(a7); restripe(t); restripe(tbl_of(doc.P(A7_HEAD)))


def cell_app(doc, pid, extra):
    p = doc.P(pid); rewrite_paragraph(p, pmarked_plain(p).rstrip() + extra)


def pmarked_plain(p):
    """Marked text of a paragraph without footnote/comment/image markers (keeps ** and << >>)."""
    out = []
    for r in p.findall(q('w:r')):
        if r.find(q('w:footnoteReference')) is not None or r.find(q('w:commentReference')) is not None:
            continue
        t = rtext(r)
        if not t:
            continue
        if is_hl(r):
            t = '<<' + t + '>>'
        elif r.find('w:rPr/w:b', NS) is not None and pstyle(p) in ('Body', 'Lead', 'TableText', ''):
            t = '**' + t + '**'
        out.append(t)
    return ''.join(out)
