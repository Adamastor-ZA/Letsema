"""QA for draft v3: footnotes in place of inline citations, and short figure titles.
Usage: python3 qa_v3.py ../outputs/Unlocking_Tourism_Growth_Final_Report_DRAFT_v3.docx"""
import re, sys, zipfile

z = zipfile.ZipFile(sys.argv[1])
doc = z.read('word/document.xml').decode('utf8')
fns = z.read('word/footnotes.xml').decode('utf8') if 'word/footnotes.xml' in z.namelist() else ''
text = lambda x: re.sub(r'\s+', ' ', ''.join(re.findall(r'<w:t(?: [^>]*)?>([^<]*)</w:t>', x))).replace('&amp;', '&').strip()

notes = [(m.group(1), text(m.group(2))) for m in re.finditer(r'<w:footnote [^>]*w:id="(\d+)"[^>]*>(.*?)</w:footnote>', fns, re.S) if int(m.group(1)) > 0]
refs = re.findall(r'<w:footnoteReference w:id="(\d+)"/>', doc)
print(f'footnotes defined {len(notes)}, referenced in the text {len(refs)}, distinct {len(set(refs))}')
bad = [n for n in notes if not n[1] or not n[1].endswith('.')]
print('footnotes empty or without a closing full stop:', len(bad), bad[:5])

PROSE = {'Body', 'Lead', 'Note', 'ListText', 'BoxBody', 'Quote'}
MON = r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)'
CITE = re.compile(rf'\([^()]*(?:,\s(?:\d{{1,2}}\s)?{MON}[a-z]*\s20\d\d|\bp\d+\b)[^()]*\)')
left = []
for p in re.findall(r'<w:p[ >].*?</w:p>', doc, re.S):
    st = re.search(r'<w:pStyle w:val="([^"]+)"', p)
    if not st or st.group(1) not in PROSE: continue
    t = text(p)
    for m in CITE.finditer(re.sub(r'\[[^\]]*\]', '', t)): left.append((st.group(1), m.group(0), t[:120]))
print('citation-like parentheses left in prose:', len(left))
for l in left: print('  ', l)

caps = [text(p) for p in re.findall(r'<w:p[ >].*?</w:p>', doc, re.S) if '<w:pStyle w:val="Caption"/>' in p]
figs = [c for c in caps if c.startswith('Figure ')]
long_ = [c for c in figs if not 3 <= len(re.sub(r'^Figure [A-Z0-9]+\.\d+\.\s*', '', c).split()) <= 6]
print(f'figure captions {len(figs)}, outside 3 to 6 words: {len(long_)}', long_)
for c in figs: print('  ', c)
