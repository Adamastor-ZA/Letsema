# Draft v4: Wesgro corporate identity

7 November 2026. Draft v3 rebuilt in the Wesgro CI, taken from Wesgro's cover and interleading slides (13 October 2026), with a darker and a lighter shade of Wesgro cyan added as Michael asked. The words, figures, footnotes, figure titles and callouts are those of v3.

## Palette

| Role | Colour | Use |
| --- | --- | --- |
| Charcoal | #4D4D4F | Cover, dividers and back cover; headings; table header rows; main chart series |
| Wesgro cyan | #00A3DA | Rules under titles and headings, header rule, callout bars, chart highlight |
| Dark cyan | #006E93 | Text-safe shade (5.8:1 on white): sub-headings, kickers, figure and table numbers, chart series |
| Light cyan | #80D1EC | Fills under dark text, chart series, Gantt design bars |
| Greys | #6D6E71, #A7A9AC, #E6E7E8, #F5F6F7 | Secondary text, minor series, rules, table banding and callout fills |
| Protea pink | #C8385F | The 1.8m seat line and other threshold lines only; taken from the cover image |

Cyan is never used for small text on white, because it falls below 4.5:1 contrast; the dark shade does that job. Text on any coloured box takes white or near-black, whichever meets 4.5:1. The scorecard's status dots keep green, amber and red, since they carry status.

## Type

Helvetica in the CI, set as Arial throughout: its metric twin, installed on every Windows machine, and the face the Wesgro slides use for body runs. Body 10pt (from 11pt EB Garamond); section headings 15pt bold charcoal over a cyan rule; sub-headings 11.5pt bold dark cyan.

## Pages

- **Cover**, after the cover slide: charcoal, the white Wesgro logo top left, the protea in the W, the title over a short cyan rule, and the Letsema and Skift credit as a small line.
- **Chapter dividers**, after the interleading slide: one each for the executive summary, Chapters 1 to 5 and the appendices. Charcoal ground, the Western Cape contour band, the chapter number and title in white over a cyan rule. The title is a real Heading 1, so the contents and bookmarks work.
- **Back cover**, after the closing slide: contour pattern, outlined protea W, "Contact us", hello@wesgro.co.za and the QR code from the slide.
- **Body pages**: white, with a cyan rule under the running header and "Wesgro | Letsema in partnership with Skift Advisory" in the footer. Tables take charcoal header rows with white text and light grey banding; summary boxes a cyan top rule.
- **Draft marking**: DRAFT FOR DISCUSSION stays on every page, in white on the charcoal pages. The cover keeps its circulation line.

Each chapter is now its own Word section, so a divider carries no running header or footer; page numbers run on through the report.

## Charts and diagrams

All 21 figures take the palette. Line charts run base in charcoal, accelerated in cyan and conservative in light cyan (labelled in dark cyan). The stacked chart, Gantt, hypothesis tree, results chain, governance diagram and scorecard use charcoal, the three cyans and the greys. The results chain now runs light to dark from inputs to impact.

## Other changes

- The document control status and the cover now read version 4 (both said version 1).
- The page scanner behind the contents pages now reads a title that wraps onto a second line, as the divider titles do.

## Checks

- Text against v3: the only changes are the cover lines, the document control version, the "Chapter 1" to "Chapter 5" divider labels and the back-cover contact lines.
- Contents: all 185 headings, figures and tables mapped to their pages.
- DRAFT FOR DISCUSSION on all 202 pages.
- 635 footnotes defined and referenced once each; every table row renders; `qa_structure.py` passes with zero issues.
- Pages: 202 (v3: 201). The seven dividers and the back cover add eight pages; Arial at 10pt runs slightly shorter than Garamond at 11pt.

## Open points

- Wesgro supplied only a white logo, so white pages carry no logo. A full-colour or charcoal version would go small in the footer.
- The QR code is copied from Wesgro's closing slide; its destination has not been checked.

The CI assets sit in `build/assets/ci/source`, and `build/assets/ci/compose.js` rebuilds the three page backgrounds from them.
