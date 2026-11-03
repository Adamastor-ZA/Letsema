export const meta = {
  name: 'wesgro-reconcile',
  description: 'Reconcile structure-doc figures against verified extracts, reconstruct the tree, and build a fact sheet per focus area',
  phases: [
    { title: 'Reconcile', detail: 'figures cited by structure.md tested against the deliverables; tree reconstruction' },
    { title: 'Fact sheets', detail: 'one evidence pack per theme, covering its focus areas' },
    { title: 'Audit', detail: 'adversarial check of every fact sheet against the extracts' },
  ],
}

const IN = '/tmp/claude-0/-home-user-Letsema/4e1968e6-be48-539d-a4af-9019b21a7592/scratchpad/inputs'
const EV = '/tmp/claude-0/-home-user-Letsema/4e1968e6-be48-539d-a4af-9019b21a7592/scratchpad/evidence'
const REPO = '/home/user/Letsema/report'

const EXTRACTS = ["demand_side", "market_assessment", "diagnostic", "midas", "benchmark", "inclusion", "segmentation", "african_market", "digital", "inception", "stakeholder", "infrastructure_p1", "infrastructure_p2"]
  .map((id) => `${EV}/${id}.md`)

const CITE_RULES = `Citation and precedence rules for the final report. Every figure carries a source and page in the form (Demand-Side Analysis, Jun 2026, p21), citing the date printed on the cover: Current State Diagnostic, Dec 2025; Inception Report, Nov 2025; Stakeholder Insights Report, Mar 2026; Global Benchmarking Report, Mar 2026; MIDAS Aviation Market Assessment, Mar 2026 (cite by section title, no page numbers); Market Assessment Report, May 2026; Demand-Side Analysis, Jun 2026; Infrastructure Report, Jun 2026; SME and Community Inclusion Plan, Oct 2026 (file dated 9 October); Skift memos by title and date (cite by section). Page numbers are PDF page indices because none of the decks print page numbers. Hierarchy: interim deliverables first, then working analyses (Market Assessment, Skift memos), then Wesgro and government data cited through a deliverable, then benchmark and reference reports, then public sources. The deliverable wins over the deck and over structure.md; conflicts are logged, never silently resolved. The final Infrastructure Report (cover file dated 22 September 2026, 114 slides) is extracted in two files, infrastructure_p1.md (pages 1 to 57) and infrastructure_p2.md (pages 58 to 114); the June 2026 draft extract at infrastructure_draft_jun2026.md is superseded and may be cited only for a figure the final report dropped, labelled as the June draft. Confirmed decisions: the growth case runs from the Market Assessment's 2025 base of 1,498,829 to 2,175,778 (base) and 2,516,282 (accelerated) in 2035 with the structure doc's market-group increments; 1.44m FY24/25 stays the recovery baseline; the comparator set is the Benchmarking Report's six; initiatives are numbered I1 onwards; phases are Activate 2027 to 2028, Expand 2029 to 2031, Sustain 2032 to 2035.`

const FOCUS_AREAS = `The 20 focus areas of the updated (14 October 2026) hypothesis tree, with dispositions and one-line reasons from structure.md:
FA01 Respond to growth segment traveller preferences (Validated). FA02 Create green-season demand with MICE and events (Reworded: June holds 6.4% of seats; ICCA). FA03 Make the whole province findable and bookable (Reworded: community product unbookable, 70% by phone, OTA gaps). FA04 Convert India and China hub traffic (Reworded: 101,000 journeys via hubs a year). FA05 Increase yield in mature markets (Validated: full routes). FA06 Build a regional foundation (Africa) (Validated: regional loads, Nigeria R31,000 and Ghana R27,700 a visit).
FA07 Win direct routes and add seats on full routes (Reworded: 16 of 27 routes above 80%, fares before seats). FA08 Grow cruise calls and ports (New: 79 calls in 2024/25, plan to 250). FA09 Accelerate tourism-enabling internal mobility (Validated: access decay 4.7 to 1.0). FA10 Support diversified route and product development (Validated: idle assets, cold zones). FA11 Align visitor experience in-destination (Validated: mid-scale gap). FA12 Balance impact on nature-based attractions (Validated: flagship limits).
FA13 Embed local destination bodies for community inclusion (Refined: seller with a stake, 20 communities, R259m at 1%). FA14 Manage climate risk and sustainable tourism (Reworded: LTOs unfunded, Meiringspoort flood). FA15 Crowd in capital with targeted investment strategies (Validated: no pipeline). FA16 Align institutional stakeholders across all three tiers (Reworded: air rights and visas sit nationally). FA17 Strengthen industry and government collaboration (Validated: 15 of 16 organisations). FA18 Expedite tourism-enabling policy and data sharing (Validated: already underway). FA19 Lead removal of infrastructure, visa and safety deficits (Moved from theme 2.1). FA20 Develop workforce and service skills (Flagged, untested: jobs goal has no labour analysis).`

const THEMES = [
  { key: 't11', name: 'Theme 1.1 Traveller, brand and proposition', fas: ['FA01', 'FA02', 'FA03'] },
  { key: 't12', name: 'Theme 1.2 Source market growth and diversification', fas: ['FA04', 'FA05', 'FA06'] },
  { key: 't21', name: 'Theme 2.1 Accessibility, connectivity and infrastructure', fas: ['FA07', 'FA08', 'FA09'] },
  { key: 't22', name: 'Theme 2.2 Product and destination capacity', fas: ['FA10', 'FA11', 'FA12'] },
  { key: 't31', name: 'Theme 3.1 Investment, inclusion and sustainability', fas: ['FA13', 'FA14', 'FA15'] },
  { key: 't32', name: 'Theme 3.2 Governance and leadership', fas: ['FA16', 'FA17', 'FA18', 'FA19', 'FA20'] },
]

const RECON_SCHEMA = {
  type: 'object',
  properties: {
    output_file: { type: 'string' },
    n_items: { type: 'number' },
    high_severity: { type: 'array', items: { type: 'string' } },
    not_in_hand: { type: 'array', items: { type: 'string' } },
  },
  required: ['output_file', 'n_items', 'high_severity', 'not_in_hand'],
}
const TREE_SCHEMA = {
  type: 'object',
  properties: {
    output_file: { type: 'string' },
    changes: { type: 'array', items: { type: 'string' } },
    needs_deck: { type: 'array', items: { type: 'string' } },
    evidence_strength: { type: 'array', items: { type: 'object', properties: { fa: { type: 'string' }, strength: { type: 'string', enum: ['strong', 'adequate', 'thin', 'none_in_hand'] }, note: { type: 'string' } }, required: ['fa', 'strength', 'note'] } },
  },
  required: ['output_file', 'changes', 'needs_deck', 'evidence_strength'],
}
const SHEET_SCHEMA = {
  type: 'object',
  properties: {
    output_file: { type: 'string' },
    fas_covered: { type: 'array', items: { type: 'string' } },
    rows_per_fa: { type: 'array', items: { type: 'object', properties: { fa: { type: 'string' }, rows: { type: 'number' }, strength: { type: 'string' } }, required: ['fa', 'rows', 'strength'] } },
    placeholders_needed: { type: 'array', items: { type: 'string' } },
  },
  required: ['output_file', 'fas_covered', 'rows_per_fa', 'placeholders_needed'],
}
const AUDIT_SCHEMA = {
  type: 'object',
  properties: {
    rows_checked: { type: 'number' },
    corrections: { type: 'array', items: { type: 'object', properties: { fa: { type: 'string' }, was: { type: 'string' }, now: { type: 'string' } }, required: ['fa', 'was', 'now'] } },
    removed: { type: 'array', items: { type: 'string' } },
    verdict: { type: 'string', enum: ['reliable', 'reliable_after_corrections', 'unreliable'] },
  },
  required: ['rows_checked', 'corrections', 'removed', 'verdict'],
}

phase('Reconcile')
const [recon, tree] = await parallel([
  () => agent(`You reconcile figures for the final report of Wesgro's Unlocking Tourism study. Read ${IN}/structure.md in full (the agreed report structure; it cites many figures). Read the brief's expectations in ${REPO}/plan.md sections 3 and 6. Then read every verified evidence extract in full: ${EXTRACTS.join(', ')} (each ends with a Verification section listing corrections; trust the corrected text).

${CITE_RULES}

Produce ${REPO}/discrepancies.md with two parts. Part A, a reconciliation table of every figure structure.md or plan.md cites (arrivals 1.44m FY24/25 and 1.16m FY19/20; 63% five-market share; 65% October to March; 72.5% Metro GDPR; one airline to Asia against ten to Africa; 2.18m and 2.52m; 1.8m seat ceiling in 2030; market-group increments +179k/+207k/+110k/+176k/+5k; spend per visitor USA R32,900 to Zimbabwe R8,500; 16 of 27 routes above 80% and 76.0%; June 6.4%; 17 routes added; 101,000 hub journeys; comparator growth rates and mechanisms including Melbourne ~5.3% and the 5 to 35% range; theme counts across 16 organisations; readiness 4.7 to 1.0; 93 of 107; 18.4%; 0.02 to 0.04%; R4m to R10m; R259m at 1%; 11 of 20 and 9 of 20; 79 cruise calls and the 250 plan; Nigeria R31,000 and Ghana R27,700; ICCA 33 to 58; 3 to 5% global norm; 2.8m, 2.5m, 5.7m and the G4J 3 million ambitions; 300k jobs; phase durations; comparator set evolution; deliverable cover dates against the brief's dates; and every other figure you find). Columns: figure as cited; where cited; what the deliverable says; deliverable and page; status (confirmed, confirmed by working analysis only, differs, not in hand); value the report will use; note. Part B, a numbered log of discrepancies in the house format: topic, value A with source and page, value B with source and page, the value used and why, severity (high, medium, low). Include the internal inconsistencies the verifiers found inside single documents (for example 63% and 61% on one slide; 29 and 27 routes; 14 and 17 new routes; 30,000 against a hub table summing to 29,015; Phase 4 at 7 and 6 months). Record values exactly. Never resolve by averaging. Return the structured summary.`, { label: 'reconcile:figures', phase: 'Reconcile', schema: RECON_SCHEMA }),

  () => agent(`You reconstruct the hypothesis tree for the final report of Wesgro's Unlocking Tourism study. The 14 October 2026 summary deck that carries the updated tree (its pages 15 and 16) is not available. Read in full: ${IN}/structure.md (Chapter 3 table); the tree transcriptions inside ${EV}/market_assessment.md (p3), ${EV}/diagnostic.md (p64), ${EV}/demand_side.md (p4), ${EV}/benchmark.md (p62), ${EV}/stakeholder.md (p7) and ${EV}/infrastructure_p1.md (p2); and the Findings and Expected-figure sections of every extract: ${EXTRACTS.join(', ')}.

${FOCUS_AREAS}

Write ${REPO}/evidence/tree.md with: (1) the December 2025 tree verbatim, noting the wording variants between documents (for example the governance entry reads "(Wesgro, DEDAT, CTT)" in the Diagnostic and "(local, provincial and national)" later; the seasonality entry reads "Develop the Seasonality and Spread Proposition" in the Diagnostic and "Develop seasonality, spread and Mega events proposition" later) with document and page for each variant; (2) the October 2026 tree of 20 focus areas with pillar, theme, disposition, the one-line reason, the December entry each descends from, and the workstream that drove the change; (3) the numbered list of changes from December to October (the brief speaks of eight; derive what the documents support and say where the count is uncertain); (4) for each of the 20, the evidence in hand by document and page and a strength rating (strong, adequate, thin, none_in_hand), naming any figure in the one-line reason that no deliverable in hand supports (for example "16 of 27 routes above 80%", "70% by phone", "plan to 250", "15 of 16 organisations", "4.7 to 1.0"); (5) facts only the deck can settle. Then update ${REPO}/traceability.csv: fill the evidence_sections and evidence_deliverables columns from what you found and set status to "evidence_mapped"; keep every other column as it is and keep the CSV valid (quote fields containing commas). Return the structured summary.`, { label: 'reconcile:tree', phase: 'Reconcile', schema: TREE_SCHEMA }),
])

phase('Fact sheets')
log('Building one evidence pack per theme')
const sheets = await pipeline(
  THEMES,
  (t) => agent(`You build the evidence pack for ${t.name} of the final report of Wesgro's Unlocking Tourism study, covering focus areas ${t.fas.join(', ')}. Read in full: ${REPO}/evidence/tree.md (dispositions, origins, evidence map), ${REPO}/discrepancies.md (values the report will use), and every verified extract: ${EXTRACTS.join(', ')}. The extracts are the only evidence you may use; the Verification section at the end of each lists corrections and omissions that override the body.

${CITE_RULES}

${FOCUS_AREAS}

Write ${REPO}/evidence/factsheet_${t.key}.md. For each focus area in this theme, in order, give: (a) the focus area name, disposition, one-line reason, December origin and workstream, copied from tree.md; (b) an evidence table of 6 to 12 rows, each row one finding with its exact figure, unit, year and basis, the document, the page, and the Chapter 2 section it will sit in; mark any figure from a working analysis or public source as such; (c) the figures in the one-line reason that no document in hand supports, written as placeholders in square brackets with what is needed; (d) the benchmark precedent available for it (document, page, two-sentence content) or "none in the Benchmarking Report"; (e) stakeholder evidence for it (organisation, insight, impact rating, page) from the Stakeholder Insights extract; (f) what the deliverables recommend for it (the deliverable's own "what we need to do" or response lines, with page), split into what Wesgro can do, what partners must do, and what sits nationally; (g) data points that could serve as its Chapter 5 indicator with the baseline value, year and source. Record values exactly as the extracts give them; do not round, infer or combine. Return the structured summary.`, { label: `sheet:${t.key}`, phase: 'Fact sheets', schema: SHEET_SCHEMA }),
  (sheet, t) => sheet ? agent(`You audit the evidence pack ${sheet.output_file} for ${t.name} (focus areas ${t.fas.join(', ')}) against the verified extracts: ${EXTRACTS.join(', ')}. For every row in every evidence table and every figure in parts (c) to (g): find it in the named extract at the named page and check value, unit, year, basis, document and page. Assume each row is wrong until the extract proves it right. Fix errors in place with the Edit tool; delete any row you cannot trace to an extract and list it under removed; add a "## Audit" section at the end listing what you changed. Check also that nothing is cited to the 14 October deck or to structure.md as if it were a deliverable, and that every placeholder in square brackets states what is needed. Return the structured result.`, { label: `audit:${t.key}`, phase: 'Audit', schema: AUDIT_SCHEMA }).then((a) => ({ theme: t.key, sheet, audit: a })) : null,
)

return { reconciliation: recon, tree, sheets: sheets.filter(Boolean) }
