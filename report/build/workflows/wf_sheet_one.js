export const meta = {
  name: 'wesgro-factsheet-one',
  description: 'Build and audit the evidence pack for one theme of the hypothesis tree',
  phases: [
    { title: 'Fact sheet', detail: 'evidence pack for the theme\'s focus areas' },
    { title: 'Audit', detail: 'adversarial check of every row against the extracts' },
  ],
}

const EV = '/tmp/claude-0/-home-user-Letsema/4e1968e6-be48-539d-a4af-9019b21a7592/scratchpad/evidence'
const REPO = '/home/user/Letsema/report'
const EXTRACTS = ['demand_side', 'market_assessment', 'diagnostic', 'midas', 'benchmark', 'inclusion', 'segmentation', 'african_market', 'digital', 'inception', 'stakeholder', 'infrastructure_p1', 'infrastructure_p2'].map((id) => `${EV}/${id}.md`)

const CITE_RULES = `Citation and precedence rules for the final report. Every figure carries a source and page in the form (Demand-Side Analysis, Jun 2026, p21), citing the date printed on the cover: Current State Diagnostic, Dec 2025; Inception Report, Nov 2025; Stakeholder Insights Report, Mar 2026; Global Benchmarking Report, Mar 2026; MIDAS Aviation Market Assessment, Mar 2026 (cite by section title, no page numbers); Market Assessment Report, May 2026; Demand-Side Analysis, Jun 2026; Infrastructure Report, Jul 2026 (final, file dated 22 September 2026, extracted in two files for pages 1 to 57 and 58 to 114; the June 2026 draft extract at ${EV}/infrastructure_draft_jun2026.md is superseded and may be cited only for a figure the final dropped, labelled as the June draft); SME and Community Inclusion Plan, Oct 2026; Skift memos by title and date (cite by section). Page numbers are PDF page indices because none of the decks print page numbers. Hierarchy: interim deliverables first, then working analyses (Market Assessment, Skift memos), then Wesgro and government data cited through a deliverable, then benchmark and reference reports, then public sources. The deliverable wins over the deck and over structure.md; conflicts are logged in ${REPO}/discrepancies.md, never silently resolved. Confirmed decisions: the growth case runs from the Market Assessment's 2025 base of 1,498,829 to 2,175,778 (base) and 2,516,282 (accelerated) in 2035 with the structure doc's market-group increments; 1.44m FY24/25 stays the recovery baseline; the comparator set is the Benchmarking Report's six; initiatives are numbered I1 onwards; phases are Activate 2027 to 2028, Expand 2029 to 2031, Sustain 2032 to 2035.`

const FOCUS_AREAS = `The 20 focus areas of the updated (14 October 2026) hypothesis tree, with dispositions and one-line reasons from structure.md:
FA01 Respond to growth segment traveller preferences (Validated). FA02 Create green-season demand with MICE and events (Reworded: June holds 6.4% of seats; ICCA). FA03 Make the whole province findable and bookable (Reworded: community product unbookable, 70% by phone, OTA gaps). FA04 Convert India and China hub traffic (Reworded: 101,000 journeys via hubs a year). FA05 Increase yield in mature markets (Validated: full routes). FA06 Build a regional foundation (Africa) (Validated: regional loads, Nigeria R31,000 and Ghana R27,700 a visit).
FA07 Win direct routes and add seats on full routes (Reworded: 16 of 27 routes above 80%, fares before seats). FA08 Grow cruise calls and ports (New: 79 calls in 2024/25, plan to 250). FA09 Accelerate tourism-enabling internal mobility (Validated: access decay 4.7 to 1.0). FA10 Support diversified route and product development (Validated: idle assets, cold zones). FA11 Align visitor experience in-destination (Validated: mid-scale gap). FA12 Balance impact on nature-based attractions (Validated: flagship limits).
FA13 Embed local destination bodies for community inclusion (Refined: seller with a stake, 20 communities, R259m at 1%). FA14 Manage climate risk and sustainable tourism (Reworded: LTOs unfunded, Meiringspoort flood). FA15 Crowd in capital with targeted investment strategies (Validated: no pipeline). FA16 Align institutional stakeholders across all three tiers (Reworded: air rights and visas sit nationally). FA17 Strengthen industry and government collaboration (Validated: 15 of 16 organisations). FA18 Expedite tourism-enabling policy and data sharing (Validated: already underway). FA19 Lead removal of infrastructure, visa and safety deficits (Moved from theme 2.1). FA20 Develop workforce and service skills (Flagged, untested: jobs goal has no labour analysis).`

const THEMES = {
  t11: { name: 'Theme 1.1 Traveller, brand and proposition', fas: ['FA01', 'FA02', 'FA03'] },
  t12: { name: 'Theme 1.2 Source market growth and diversification', fas: ['FA04', 'FA05', 'FA06'] },
  t21: { name: 'Theme 2.1 Accessibility, connectivity and infrastructure', fas: ['FA07', 'FA08', 'FA09'] },
  t22: { name: 'Theme 2.2 Product and destination capacity', fas: ['FA10', 'FA11', 'FA12'] },
  t31: { name: 'Theme 3.1 Investment, inclusion and sustainability', fas: ['FA13', 'FA14', 'FA15'] },
  t32: { name: 'Theme 3.2 Governance and leadership', fas: ['FA16', 'FA17', 'FA18', 'FA19', 'FA20'] },
}

const SHEET_SCHEMA = { type: 'object', properties: { output_file: { type: 'string' }, fas_covered: { type: 'array', items: { type: 'string' } }, rows_per_fa: { type: 'array', items: { type: 'object', properties: { fa: { type: 'string' }, rows: { type: 'number' }, strength: { type: 'string' } }, required: ['fa', 'rows', 'strength'] } }, placeholders_needed: { type: 'array', items: { type: 'string' } } }, required: ['output_file', 'fas_covered', 'rows_per_fa', 'placeholders_needed'] }
const AUDIT_SCHEMA = { type: 'object', properties: { rows_checked: { type: 'number' }, corrections: { type: 'array', items: { type: 'object', properties: { fa: { type: 'string' }, was: { type: 'string' }, now: { type: 'string' } }, required: ['fa', 'was', 'now'] } }, removed: { type: 'array', items: { type: 'string' } }, verdict: { type: 'string', enum: ['reliable', 'reliable_after_corrections', 'unreliable'] } }, required: ['rows_checked', 'corrections', 'removed', 'verdict'] }

const key = args && args.theme
const t = THEMES[key]
if (!t) throw new Error('unknown theme ' + key)

phase('Fact sheet')
log(`Evidence pack for ${t.name}`)
const sheet = await agent(`You build the evidence pack for ${t.name} of the final report of Wesgro's Unlocking Tourism study, covering focus areas ${t.fas.join(', ')}. Read in full: ${REPO}/evidence/tree.md (dispositions, origins, the evidence map in its section 4 and the deck-only facts in section 5), ${REPO}/discrepancies.md (values the report will use), and every verified extract: ${EXTRACTS.join(', ')}. The extracts are the only evidence you may use; the Verification section at the end of each lists corrections and omissions that override the body.

${CITE_RULES}

${FOCUS_AREAS}

Write ${REPO}/evidence/factsheet_${key}.md. For each focus area in this theme, in order, give: (a) the focus area name, disposition, one-line reason, December origin and workstream, copied from tree.md; (b) an evidence table of 6 to 12 rows, each row one finding with its exact figure, unit, year and basis, the document, the page, and the Chapter 2 section it will sit in; mark any figure from a working analysis or public source as such; (c) the figures in the one-line reason that no document in hand supports, written as placeholders in square brackets with what is needed, and the supported figure that replaces each (for example eleven of 27 routes above 80% in place of sixteen); (d) the benchmark precedent available for it (document, page, two-sentence content) or "none in the Benchmarking Report" with the nearest case; (e) stakeholder evidence for it (organisation, insight, impact rating, page) from the Stakeholder Insights extract; (f) what the deliverables recommend for it (the deliverable's own "what we need to do", "strategic implication" or response lines, with page), split into what Wesgro can do, what partners must do, and what sits nationally; (g) data points that could serve as its Chapter 5 indicator with the baseline value, year and source; (h) for the theme as a whole, the candidate Chapter 4 initiatives the deliverables themselves point to (name, the focus areas it serves, the deliverable and page), so the portfolio can be assembled from evidence rather than invented. Record values exactly as the extracts give them; do not round, infer or combine. Return the structured summary.`, { label: `sheet:${key}`, phase: 'Fact sheet', schema: SHEET_SCHEMA })
if (!sheet) return { theme: key, failed: 'sheet returned null' }

phase('Audit')
const audit = await agent(`You audit the evidence pack ${sheet.output_file} for ${t.name} (focus areas ${t.fas.join(', ')}) against the verified extracts: ${EXTRACTS.join(', ')}. For every row in every evidence table and every figure in parts (c) to (h): find it in the named extract at the named page and check value, unit, year, basis, document and page. Assume each row is wrong until the extract proves it right. Fix errors in place with the Edit tool; delete any row you cannot trace to an extract and list it under removed; add a "## Audit" section at the end listing what you changed. Check also that nothing is cited to the 14 October deck or to structure.md as if it were a deliverable, that every placeholder in square brackets states what is needed, and that the citation dates follow the rules: ${CITE_RULES.slice(0, 900)}. Return the structured result.`, { label: `audit:${key}`, phase: 'Audit', schema: AUDIT_SCHEMA })

return { theme: key, sheet, audit }
