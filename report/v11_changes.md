# Draft v11: fewer, shorter footnotes

8 November 2026. The recommended footnote changes, at Michael's request. The words of the report are unchanged, apart from the four passages that describe how sources are cited.

| | v10 | v11 |
| --- | --- | --- |
| Pages | 210 | 200 |
| Footnotes | 845 | 394 |
| Footnote space, whole report | 11.2 page-equivalents | 4.9 |
| Footnote space on a page that has footnotes | 8% on average, 26% at most | 4% on average, 11% at most |

Footnote space is measured from the first footnote number on each page down to the footer, as a share of the text area.

## What changed

- **One footnote per paragraph.** A paragraph's sources sit in a single footnote at its end, in the order the paragraph uses them. A document cited more than once is named once, followed by all its pages, for example "Infrastructure Report, p88 to p90, p30; MIDAS, 'Seasonality'". Notes on a source stay with it.
- **Short titles, no dates.** Each study document is cited by a short title and page: Diagnostic, Benchmarking, Stakeholder Insights, Market Assessment, Inclusion Plan, MIDAS, and so on. Each exists in one version, so the date added nothing. A new note under the documents table in Appendix A9 keys each short title to its full title, and the table already gives the cover dates. Public sources keep their full titles and dates.
- **Closer footnote lines,** with the gap between notes removed.
- **No footnotes in the executive summary.** Its closing note now says the chapters give the source of every figure in it.
- **The citation conventions** in section 1.5, Appendix A9 and the document control table now describe this form.

The renderer makes these changes when it turns citations into footnotes, so the content keeps its full citations. Setting `FN_MODE` to an empty string rebuilds the v10 form.

## Checks

- **Nothing lost:** every source-and-page pair in v10's 797 footnotes outside the summary appears in the matching v11 footnote, under its short title. No footnote repeats a page.
- **Build:** 394 footnotes, each defined and referenced once, none empty. No citation-like parenthesis is left in the text, and every table row renders. 145 of 145 contents entries are mapped. `qa_structure.py` passes with zero issues, with all 20 findings word for word in the summary. DRAFT FOR DISCUSSION is on all 200 pages.
- **Changes:** the content changes are the four logged edits in `redteam/apply_v11.py`. The code changes are the default footnote form in `helpers.js` and the conventions row in `front_matter.js`.

## Possible next step

Chapter 3 often cites in its text a figure that its evidence table already sources. Dropping those citations would remove perhaps another hundred footnotes. That needs an editorial pass, not a switch.
