"""Write report/change_log.md and report/reconciliation_log.md from redteam/applied.json, with v1 and v2 pages."""
import json, os, re, sys
from collections import OrderedDict

sys.path.insert(0, os.path.dirname(__file__))
from pages import load, page_of, norm  # noqa: E402
from diff_v1_v2 import parts  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
REPORT = os.path.join(HERE, '..', '..')
A = json.load(open(os.path.join(HERE, 'applied.json')))
LOG = A['log']
V1, V2 = load(os.path.join(REPORT, 'qa', 'v1_raw.txt')), load(os.path.join(REPORT, 'qa', 'v2_raw.txt'))


def pages(text, P):
    best = []
    for pc in sorted(parts(text), key=len, reverse=True)[:3] if text else []:
        best = page_of(pc, P)
        if best: break
    if not best: return ''
    if len(best) > 4: return ', '.join(map(str, best[:4])) + ' and more'
    return ', '.join(map(str, best))


def short(s, n=170):
    if s.startswith('[{') or s.startswith('{"'): s = ' / '.join(parts(s))
    s = norm(s).replace('|', '/')
    return s if len(s) <= n else s[:n - 50].rstrip() + ' ... ' + s[-45:].lstrip()


def cell(s):
    return s.replace('|', '/').replace('\n', ' ')


ORDER = ['C1.1', 'C1.2', 'C1.3', 'C2', 'C3', 'C4.1', 'C4.2', 'C4.3', 'C5', 'C6.1', 'C6.2', 'C6.3', 'C6.4',
         'M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9', 'M10', 'M11', 'M12', 'M13'] + [f'P{i}' for i in range(1, 21)] + ['Sources']

STATUS = {k: 'Done' for k in ORDER}
STATUS.update({'M1': 'Skipped', 'C6.3': 'Done (closed by C6.1)', 'P6': 'Done (closed by C6.1)', 'P8': 'Done (closed by C1.3)',
               'P10': 'Done (closed by C6.4)', 'P14': 'Done (closed by C5)', 'P13': 'Blocked', 'C2': 'Done, one find adjusted for the D1 skip',
               'C6.1': 'Done, decision 1 kept for the D1 skip', 'M13': 'Done, one sentence omitted for the D1 skip'})

NOTES = {
    'C1.1': 'Every find in the table applied at the count listed, plus the chart label in all four charts. The p25 find ("before the base case reaches the seat ceiling") also sits inside the p115 title and the p118 sentence, which the brief names separately; those two longer finds were applied first, so the p25 find then matched once. The glossary term keeps its alphabetical place. Two further seat-line hits from the sweep were changed (marked Sweep); the remaining "ceiling" hits are listed under Sweeps.',
    'C1.2': 'Both inserts made: the caveat paragraph after the Figure 1.4 source note (now holding the P2 note) and before "The routes that exist are full.", and the sentence in A2.',
    'C1.3': 'All six places changed. The planning date stays about 2033 (D3). The risk rows "Runway relief at Cape Town International slips past about 2033" (Tables ES.7 and 4.7) are left as instructed.',
    'C2': 'All rows applied. The p13 thesis line is handled under M13. At p22 the thesis clause is replaced but "growth to 2.5 million arrivals" is kept instead of "between 2.2 million and 2.5 million", because D1 is on the skip line and the brief says to keep every goal statement as it is.',
    'C3': 'All six items done. The C3.1 paragraph sits directly after the Table 1.2 source note. One comma was removed from the brief\'s text ("returning residents, or OAG" became "returning residents or OAG") under rule 7, no Oxford comma.',
    'C4.1': 'All rows applied. The p30 find spans two paragraphs in the source: the replacement closes the first paragraph and the second keeps its 2024 sentence. Table 1.3\'s source note now says the 2025 shares are normalised to 100% for the October to March share. Table 2.2\'s source key gains "Diag", which its new source cell uses (Consequential). p28 is unchanged.',
    'C4.2': 'All three cells and the source note changed; the Spend paragraph is inserted directly after "Arrivals." in section 5.3. The brief\'s Table 5.6 is Table 5.7 in the report.',
    'C4.3': 'All rows applied (D4: T1-04 kept, baseline and path removed). The brief\'s Table 5.6 is Table 5.7 and its "Table 5.8" methodology row sits in Table 5.9; the row is deleted and the provincial employment row kept. Consequential: Table 5.4 T1-04 source, Table 5.9 title count, Table 1.1 jobs row, the ES.6 and 5.7 titles and the 5.3 topline, each of which said jobs carry a ratio or targets.',
    'C5': 'All known instances applied; the sweep terms found no further passage that met the rule. Passages that may meet it but match no sweep term are left and listed under Seen, not changed (items 2 to 5). The two caveats the brief keeps (Nigeria and Ghana spend averages; readiness accessibility basis) stay as single lines. SLA Annexure B and the 14 October deck are not in the build\'s input folders, so their open items are left as they are. Every removed passage, with its v1 page, is in reconciliation_log.md.',
    'C6.1': 'List replaced with the Board decisions (1 to 5) and the recommendations (6 and 7), numbered on through the split. Decision 1 keeps its v1 wording ("Adopt growth to 2.5 million arrivals by 2035 as the plan\'s goal, with the base and accelerated paths as its targets.") because D1 is on the skip line. No cross-reference to an old decision number exists; the new M11 risk row cites Decision 3 on the new numbering. The paragraph "Several items remain open..." is kept.',
    'C6.2': 'Both titles changed. Table 4.4\'s rows are unchanged.',
    'C6.3': 'Decision 3 now reads "first-24-month"; this also closes P6.',
    'C6.4': 'All rows applied (D2). The I15 charter does not describe the chair, so its Partners cell is unchanged (its Dependencies cell is listed under Seen, not changed). Consequential: the Figure 4.3 label is longer than the box at 20px, so that one label is set at 17px; nothing else in the diagram moved.',
    'M1': 'Skipped: D1 is on Michael\'s skip line. p26 and the Figure ES.1 header are unchanged. Goal statements naming 2.5 million are kept (see Sweeps).',
    'M2': 'All rows applied, including the Figure 2.5 bars and the reference bar. Consequential: the p35 range end (4% to 35% became 4% to 40%), the Kenya bar label (no longer a range midpoint) and the Figure 2.5 source note. The open item sits directly after the Table 2.5 source note. Table A.12 keeps its printed values.',
    'M3': 'Qualifiers added in the three entries; no label, count, table or tree graphic changed. Table 1.9 sits in section 1.5 (pp40 to 41 in v1), so "What the evidence argued against." follows it there, as a bold run-in like the report\'s other run-ins.',
    'M4': 'Topline changed in both places (Chapter 3 and Table ES.2, which carries the Pillar 1 toplines) and both row labels changed.',
    'M5': 'Both open items added.',
    'M6': 'Open item replaced. Supply_Infrastructure.xlsx is not in the build\'s input folders, so the 50,332 count could not be tested; no count or share is restated.',
    'M7': 'All rows applied. The Baseline column of Table 5.5 confirms the seven without a baseline are T2-04, T2-18, T2-20, T2-21, T2-23, T2-24 and T2-25. The new line points to Table 5.9, the table with the dated gaps (the brief calls it Table 5.8). The find "T2-10 routes above 80% load" also matched Table 5.2 (p147), which the brief does not list; renamed there to match (Consequential).',
    'M8': 'All rows applied. The 0.02% to 0.04% figures in the Chapter 2 and 3 bodies and Appendix A5 are left, as instructed.',
    'M9': 'All rows applied. The p103 find also matched its verbatim copy in Appendix A7 (p186); applied to both, because A7 reproduces the Chapter 3 actions word for word and the brief pairs the two pages for every other A7 action it changes (M9 row 1, C6.4, P16, P17). Revert the A7 row if you want the strict count rule.',
    'M10': 'All rows applied (D9). p157 ("did the second gateways carry the load meanwhile?") is left as it is.',
    'M11': 'Four rows added after the existing ten. Check of the existing rows: six sit outside Wesgro\'s control, read as risks whose remedy sits with another body (runway with ACSA; air agreements, visas and LTO funding with national government; safety with SAPS; water and power with utilities); the other four are mitigated through Wesgro\'s own programmes. Six confirmed, so the lead reads ten of fourteen. Consequential: the Table 4.7 title count and its source key (DSA). No other risk count exists; Table ES.7 is unchanged. **Michael to review the four new ratings (likelihood and impact), which are Letsema\'s assessment.**',
    'M12': 'All rows applied; both toplines match.',
    'M13': 'ES opening replaced by the three paragraphs, except the sentence "The base path is the plan\'s target and the accelerated path its stretch.", omitted because D1 is on the skip line. The doubling mandate stays in section 1.1. Tone rows applied; the FA16 topline matches in both places.',
    'P1': 'Rows I6 to I11 existed in the source. The cause was rendering: the table\'s header row fell alone at the foot of v1 p147, and LibreOffice then dropped the rows after it. Fix in helpers.js: the header row is kept with the first body row. A row check over every table in v1 found Table 5.2 the only one affected; in v2 every row of every table is in the PDF text.',
    'P2': 'The Figure 1.4 note now ends the figure\'s source line, wording kept.',
    'P3': 'charts.js lineChart gains a timeAxis option that places each year point at its calendar distance (2025 to 2035); points, labels, colours and y-axis unchanged. The ES.2 and 5.2 spacing note is removed.',
    'P4': 'The labels were cut in the chart data itself, not only by the renderer. Full names restored from the section 4.3 charter titles, and ganttChart wraps a long name to two lines (rows grow from 44 to 54px).',
    'P5': 'Both items moved, wording kept. Section 1.5 has no open-items list, so they close section 1.5 as bracketed items.',
    'P7': 'Table A.4 prints +323,805 and the sentence about the misprint is removed (logged in reconciliation_log.md under C5). The rest of that note is unchanged (see Seen, not changed).',
    'P9': 'p34 sentence inserted. At p48 the paragraph has no separate source note, so "Other study documents count new routes from 2014 on a different basis." takes the place of the deleted C5 sentence.',
    'P13': 'Investigated, not changed. No forced page break sits after Figure 2.1. The space is left by the next figure (Figure 2.2), which is too tall for the rest of the page and moves whole, because its image is kept with its caption and source. Removing that setting would split a figure from its caption, and the brief rules out moving content. In v2 the same gap falls on p45, and p44 now ends about a third empty because Figure 2.1 moved down. Options for Michael: allow Figure 2.2 at a smaller width, or let a paragraph move ahead of it.',
    'P18': 'All ten occurrences changed: the first body mention (p58, with the date), p60 and the eight others.',
    'P19': 'Paragraph, Table 1.2 row (figure, source, open item) and the Table 1.2 source list changed. The Hypertext row stays in the A9 sources table (M11 cites it). The 106,707 Cape Town jobs figure is unchanged.',
    'Sources': 'Nine rows added after the existing public sources, before the SLA row; the brief\'s "Type" is the table\'s Status column. Table A.33 title now counts fifteen public and reference sources and the A9 lead twenty-eight documents.',
}

by = OrderedDict((k, []) for k in ORDER)
for e in LOG:
    by.setdefault(e['id'], []).append(e)


CONTENT = os.path.join(HERE, '..', 'content')
_cache = {}


def context(e):
    """Caption or heading text of the block an edit sits in, for edits too short to find on their own (cells, chart labels)."""
    f = e['file'].split(' and ')[0].split(', ')[0]
    if f not in _cache:
        try: _cache[f] = json.load(open(os.path.join(CONTENT, f)))
        except (OSError, ValueError): _cache[f] = None
    d = _cache[f]
    if not d: return ''
    m = re.search(r'\.blocks\[(\d+)\]', e['path'])
    cands = [b for b in d['blocks'] if e['after'] and e['after'] in json.dumps(b, ensure_ascii=False)]
    b = cands[0] if len(cands) == 1 else (d['blocks'][int(m.group(1))] if m and int(m.group(1)) < len(d['blocks']) else None)
    return (b or {}).get('caption') or (b or {}).get('text') or ''


OVERRIDE = {'P3': ('18, 34, 44, 152', '18, 34, 45, 154'), 'P4': ('118', '119'), 'P2': ('34', '34')}


def v1_context(ctx):
    for x in LOG:
        if x['after'] and len(x['after']) > 12 and x['after'] in ctx: ctx = ctx.replace(x['after'], x['before'])
    return ctx


def edit_row(e):
    ctx = context(e)
    multi = lambda x: not x or ',' in x or 'more' in x
    v1 = pages(e['before'], V1) if e['before'] else 'new'
    if e['before'] and multi(v1): v1 = pages(v1_context(ctx), V1) or v1
    v2 = pages(e['after'], V2) if e['after'] else 'removed'
    if e['after'] and multi(v2): v2 = pages(ctx, V2) or v2
    if e['id'] in OVERRIDE and e['path'] != '.blocks[3].svg': v1, v2 = OVERRIDE[e['id']]
    if e['path'].endswith('.chart') or e['path'] == '.blocks[3].svg': v1, v2 = ('54', '55') if e['id'] == 'M2' else ('144', '145')
    return f"| {v1 or '?'} | {v2 or '?'} | {cell(short(e['before'])) or '(insert)'} | {cell(short(e['after'])) or '(deleted)'} |"


out = ['# Change log: draft v1 to draft v2', '',
       '7 November 2026. Internal working record for Michael. Brief: "apply the red-team changes to Unlocking Tourism Growth, draft v1 to v2". Skip line: D1. Decisions D2 to D9 at their defaults.', '',
       'Source edited: the content modules in `report/build/content/` (the JSON files the renderer reads), through one script, `report/build/redteam/apply_v2.py`, which holds every find string, its expected count and its replacement. The build lives at `report/build/` (not `/home/claude/build/`); the PDF comes from the project\'s `build.sh`, which converts with LibreOffice directly (there is no `soffice.py`). Renderer changes: `helpers.js` (P1 table header; numbered lists that carry on, for C6.1), `content_render.js` (passes that option) and `charts.js` (P3 time axis; P4 two-line Gantt labels).', '',
       f'Result: {len(LOG)} logged edits. Every find matched the count the brief lists, or the extra match is explained below (C1.1, M7, M9). v1 has 191 pages and v2 193. Page numbers below are PDF pages, which equal the printed footer numbers.', '',
       '## Summary by change ID', '', '| ID | Status | v2 pages | Note |', '| --- | --- | --- | --- |']
for k in ORDER:
    es = by.get(k, [])
    pg = sorted({int(p) for e in es for p in re.findall(r'\d+', (pages(e['after'], V2) or pages(context(e), V2)) if e['after'] else '')})
    pgs = ', '.join(map(str, pg[:12])) + (' and more' if len(pg) > 12 else '') if pg else ''
    pgs = {'P1': '150', 'P3': '18, 34, 45, 154', 'C6.3': '21', 'P6': '21', 'P8': '30, 35, 52', 'P10': '145', 'P14': '43, 49, 54, 58, 63, 67, 172, 183'}.get(k, pgs)
    out.append(f"| {k} | {STATUS[k]} | {pgs} | {cell(NOTES.get(k, '').split('. ')[0])} |")

out += ['', '## Detail by change ID', '']
for k in ORDER:
    es = [e for e in by.get(k, []) if e['kind'] != 'Consequential']
    out += [f'### {k}: {STATUS[k]}', '']
    if NOTES.get(k): out += [NOTES[k], '']
    if es:
        out += ['| v1 page | v2 page | Before | After |', '| --- | --- | --- | --- |']
        out += [edit_row(e) + (f" {e['kind']}" if e['kind'] == 'Sweep' else '') for e in es]
        out += ['']

out += ['## Consequential edits', '', 'Each was forced by a named change and is logged under its parent ID.', '',
        '| Parent | v1 page | v2 page | Before | After | Why |', '| --- | --- | --- | --- | --- | --- |']
for e in LOG:
    if e['kind'] == 'Consequential':
        r = edit_row(e).strip('|').split(' | ')
        out.append(f"| {e['id']} | " + ' | '.join(x.strip() for x in r) + f" | {cell(e['note'])} |")

out += ['', '## Sweeps', '',
        'Pages in this section and the next are v2 pages.', '', '**C1.1, "ceiling".** After the table, 15 hits remain in the content modules. None refers to the seat line outside a quotation:', '',
        '- Quotations kept verbatim: "a hard ceiling at 1.8 million inbound seats" (2.1, p46) and the A2 quotation of both decks (p167).',
        '- Water: the "hard ceiling" water scarcity sets on visitor load (1.2, p32, a quotation; 3.3.2, p111).',
        '- The airport or runway, not the seat line: "Cape Town International itself is now the physical ceiling" (p30), "they set the ceiling the airlines fly into" (p49), Table 2.4 row "Airport is the ceiling" (p53) and the Pillar 2 topline "Supply sets the ceiling on the growth case" (p85).',
        '- The model\'s lever names as the deck prints them: "the airlift ceiling" (p43) and "an airlift capacity ceiling" (p164); "Source-market growth sets the ceiling" (p164) is a different ceiling.',
        '- Other meanings: "market, seasonality and spread ceilings" (Pillar 1 objective, p71), "a capacity ceiling" for a community site (A5, p180), and the internal figure id `fig_base_case_seat_ceiling`, which never prints.',
        '- Changed under the rule (Sweep rows above): "the case stops at the ceiling" (3.4) and "when the ceiling binds" (4.2).', '',
        '**C4.1, "65%".** All ten "65%" strings in v1 meant the October to March share, and all ten are changed (C4.1 detail). The only "65%" in v2 is "65% to 72% load" in the new C2 text (p18). The Doha 65.2% load factor (p79) and p28\'s 61% are untouched.', '',
        '**C4.3, jobs.** "two jobs", "ratio-based" and "30,000 jobs": no hits left. The India and China "about 30,000" traveller figures are untouched. Four mentions of the jobs ratio remain outside the brief\'s terms (see Seen, not changed).', '',
        '**C5.** Every sweep term was searched. Hits outside the known instances: "typo" (a false match on "typology", p67) and "do not reproduce" in the FA6 source note and Table A.1, both the Nigeria and Ghana caveat the brief keeps. "Plan decision", "Michael", "agreed structure", "agreed report structure", "house style", "misprint", "appear nowhere", "do not follow the stated weights", "reconciliation", "discrepanc", "logs the" and "this report logs" have no hits left.', '',
        '**M1 (skipped), "goal" near 2.5 million.** Three statements name 2.5 million as the goal and are kept: decision 1 (ES, p20), section 1.1 ("it is the goal the report carries", p23) and the Table 1.1 row "Growth to 2.5 million" (p23). Two other "goal" hits concern jobs (FA20 and A1).', '',
        '**C6.1, decision numbers.** No "Decision N" cross-reference existed in v1. The one in v2 is the new M11 row, which cites Decision 3 on the new numbering.', '',
        '**M11, risk counts.** No "ten risks" or "ten material risks" outside 4.8; the Table 4.7 title count is updated (Consequential).', '',
        '## Seen, not changed', '',
        'Noticed while working; not named in the brief, so left exactly as they are.', '',
        '1. Table 1.3 row label "2025 (provisional)" (p30): the row\'s October to March cell is now the normalised 62%.',
        '2. Section 1.5, "The five-market share, printed as both 63% and 61% on one slide, is one case ... Nothing is averaged and nothing is reconciled silently." (p42), and Table 2.2 "top five 63% (61% in the slide text)" (p48): both report the slide conflict C5 removed at p28, but neither matches a sweep term.',
        '3. Section 1.5, "Four cover dates differ from their file dates ..." (p41): the same point as the 1.4 sentence C5 deleted.',
        '4. Internal-record wording outside the sweep terms: "the difference is logged" (1.4, p38) and "No document in hand records why, and the change is logged." (2.3, p54).',
        '5. A2 note on the June deck\'s printed CAGRs against its end points (p165): an erratum left after the P7 sentence was removed.',
        '6. Table 3.9 source note: "76.0% is the printed network total and the 27 rows sum to 75.0%" (p86).',
        '7. Table 2.7 row "Growth above the norm is designed" (p57): the new cell cites the world 11% and the corrected Chile and Singapore figures, but its Pages cell still reads "p7, p8, p9".',
        '8. The jobs ratio outside the C4.3 terms: the FA20 action and its A7 copy ("obtain the method note for the jobs-per-passenger ratio", pp114, 189), two I18 charter rows ("the method note for the jobs ratio obtained"; "the jobs indicator moved from the ratio to a provincial measure", p139), and the A9 source "Air access releases: jobs and spend per 100 international passengers" (p193), which no passage now cites.',
        '9. Section 5.3 opens its second jobs paragraph with "The report restates the 300,000 ..." (p155) now that the sentence that introduced the 300,000 is removed under C4.3.',
        '10. D2 against older wording: the I15 charter Dependencies "DEDAT and Cape Town Tourism as standing members" (p136), section 4.4 "DEDAT is a standing member of Steerco" (p141) and the FA16 recommendation "A Tourism Growth Steerco at Wesgro CEO level, with DEDAT and Cape Town Tourism" (p106).',
        '11. D9 against older wording: Table 3.9 row label "Second gateways" (p86) and the I6 charter Expand row "growth at George" (p127).',
        '12. Table 3.1 cell for FA2, "international meetings cluster from May to November" (p71), close to the topline M4 rewrote.',
        '13. A6 source note "The deck does not print the number 16." (p181).',
        '14. Table 4.7\'s narrow columns break "Likelihood" and "Medium" mid-word (pp147 to 148), as in v1.',
        '15. The Pillar 2 topline "Supply sets the ceiling on the growth case." (p85) keeps the supply-first thesis that C2 narrowed elsewhere.',
        '16. `report/open_items.md` and `report/discrepancies.md` are outside the report and were not updated for v2: open item 3 (the deck\'s basis for 16) left the report under C5, and v2 adds new open items (C1.2, C3, C4.2, M2, M5, M6, M7, M8, M9, M12, P15).',
        '']
open(os.path.join(REPORT, 'change_log.md'), 'w').write('\n'.join(out))

# Reconciliation log: every erratum or internal note removed under C5 (with P7 and the C4.1 paragraph that held "Plan decision 6").
rec = ['# Reconciliation log (internal, not for Wesgro)', '',
       '7 November 2026. Every erratum, misprint, reconciliation or internal-workings note taken out of the report under C5 (decision D6), with its v1 page, the wording removed and the line that replaced it, if any. The reconciliation table and discrepancy log behind these notes stay in `report/discrepancies.md`.', '',
       '| # | v1 page | Removed wording | Replaced by |', '| --- | --- | --- | --- |']
n = 0
for e in LOG:
    if e['id'] in ('C5', 'P7') or (e['id'] == 'C4.1' and 'Plan decision 6' in e['before']):
        n += 1
        before = norm(e['before'])
        pg = pages(e['before'], V1)
        if not pg or ',' in pg or 'more' in pg: pg = pages(v1_context(context(e)), V1) or pg
        rec.append(f"| {n} | {pg or '?'} | {cell(before)} | {cell(norm(e['after'])) or '(deleted)'} |")
rec += ['', 'Kept on purpose as single-line caveats, because later changes rely on them: the Nigeria and Ghana spend averages (FA6 source note, Table A.1 and the FA6 evidence row) and the readiness accessibility basis (Table 1.4 source note).', '']
open(os.path.join(REPORT, 'reconciliation_log.md'), 'w').write('\n'.join(rec))
print('wrote change_log.md and reconciliation_log.md;', n, 'reconciliation rows')
