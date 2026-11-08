"""Draft v11 content edits (Michael, 8 November 2026): fewer, shorter footnotes.

The footnote form itself changes in the renderer (helpers.js, FN_MODE now defaults to para,short,tight,es0): one footnote per
paragraph with repeated sources folded, study documents cited by short title without their dates, closer footnote lines,
and no footnotes in the executive summary. This script changes only the text that describes the citation form:
section 1.5's conventions paragraph, Appendix A9's note on how documents are cited (plus a key to the short titles), and
the executive summary's closing note. The document control row is in front_matter.js.
Run once on the v10 content. Writes redteam/applied_v11.json.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
C = os.path.join(HERE, '..', 'content')
LOG = []


def load(f): return json.load(open(os.path.join(C, f)))


def save(f, d):
    with open(os.path.join(C, f), 'w') as fh:
        json.dump(d, fh, indent=1, ensure_ascii=False); fh.write('\n')


def edit(f, find, repl, why):
    d = load(f); s = json.dumps(d, ensure_ascii=False)
    a, b = json.dumps(find, ensure_ascii=False)[1:-1], json.dumps(repl, ensure_ascii=False)[1:-1]
    assert s.count(a) == 1, (f, find[:60], s.count(a))
    save(f, json.loads(s.replace(a, b)))
    LOG.append({'file': f, 'before': find, 'after': repl, 'reason': why})


edit('ch1/05_how_to_read.json',
     'Every figure carries its source and page in a footnote, in the form Demand-Side Analysis, Jun 2026, p21. The date is the cover date and the page',
     'Sources sit in footnotes, one per paragraph, in the order the paragraph uses them. Each study document is cited by a short title and page, in the form Demand-Side Analysis, p21; Appendix A9 gives each full title and cover date. The executive summary carries no footnotes, because the chapters source its figures. The page',
     'the footnote form changed: one per paragraph, short titles, no footnotes in the summary')

edit('appendices/09_a9_glossary.json',
     'Deliverables are cited with the date printed on the cover; where the file date differs, both are shown below.',
     'Footnotes cite each deliverable by a short title, keyed below; the table gives its full title and the date printed on its cover, and where the file date differs, both are shown.',
     'deliverables are now cited in footnotes by short title, without the date')

d = load('appendices/09_a9_glossary.json')
i = next(k for k, b in enumerate(d['blocks']) if b['type'] == 'note' and 'SLA clause numbers in the last column' in b.get('text', ''))
key = ('Short titles used in the footnotes: Inception Report; Diagnostic (Current State Diagnostic); Digital Insights (Skift Digital and Search '
       'Insights memo); Stakeholder Insights (Stakeholder Insights Report); Segmentation (Skift Segmentation Analysis); African Markets (Skift '
       'African Market Analysis); Benchmarking (Global Benchmarking Report); MIDAS (MIDAS Aviation Market Assessment); Market Assessment '
       '(Market Assessment Report); Demand-Side Analysis; Infrastructure Report; Inclusion Plan (SME and Community Inclusion Plan). Public '
       'sources are cited by full title and date.')
d['blocks'].insert(i + 1, {'type': 'note', 'text': key})
save('appendices/09_a9_glossary.json', d)
LOG.append({'file': 'appendices/09_a9_glossary.json', 'before': '', 'after': key, 'reason': 'key to the short titles the footnotes use'})

edit('exec/01_summary.json',
     'Each is marked in square brackets where it occurs and listed with an owner in the accompanying open-items register.',
     'Each is marked in square brackets where it occurs and listed with an owner in the accompanying open-items register. The chapters that follow give the source of every figure in this summary.',
     'the summary carries no footnotes; its figures are sourced in the chapters')

json.dump(LOG, open(os.path.join(HERE, 'applied_v11.json'), 'w'), indent=1, ensure_ascii=False)
print(len(LOG), 'edits')
