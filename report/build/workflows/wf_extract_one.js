export const meta = {
  name: 'wesgro-extract-one',
  description: 'Extract and adversarially verify page-referenced evidence from one Wesgro deliverable',
  phases: [
    { title: 'Extract', detail: 'full read, page-referenced findings' },
    { title: 'Verify', detail: 'adversarial figure-by-figure check against the source' },
  ],
}

const IN = '/tmp/claude-0/-home-user-Letsema/4e1968e6-be48-539d-a4af-9019b21a7592/scratchpad/inputs'
const UP = '/root/.claude/uploads/4e1968e6-be48-539d-a4af-9019b21a7592'
const OUT = '/tmp/claude-0/-home-user-Letsema/4e1968e6-be48-539d-a4af-9019b21a7592/scratchpad/evidence'

const REGISTRY = {
  demand_side: { name: 'Demand-Side Analysis (final; cover June 2026; file dated 01.10)', text: `${IN}/Demand_Side_Final_01.10.txt`, src: `${UP}/ba362155-Wesgro_Demand-Side_Analysis_Final_01.10.pdf`, kind: 'pdf', pages: 57,
    use: 'Chapter 2.1, 3.1 (all six demand focus areas), 3.4 integrated case, Chapter 5 targets. Expected: four-driver growth model; scenarios (conservative 1,822,634, base 2,175,778, accelerated 2,516,282 in 2035); the 1.8m inbound seat ceiling and the year the base case reaches it; the base-case year points 2024, 2028, 2030, 2032, 2034, 2035 by market group (Mature, Regional, Hubs, Acceleration, Strategic) transcribed in full; spend per visitor by market; spend projections by group; the four segments; India and China route-to-market (71,000 and 30,000 hub journeys); 63% or 61% five-market share; monthly shares and their total; MICE and ICCA figures; African markets table (Nigeria R31,000, Ghana R27,700). Record that the base year here is 2024 (1,445,031) and transcribe every year point exactly.' },
  market_assessment: { name: 'Market Assessment Report (May 2026)', text: `${IN}/Market_Assessment_May2026.txt`, src: `${UP}/eddf3a01-Doubling_Toursim_Market_Assessment_Report_May_2026.pdf`, kind: 'pdf', pages: 61,
    use: 'Predecessor of the Demand-Side Analysis. The final report will use THIS document\'s 2025 base of 1,498,829 and its market-group year points (2025 to 2035) for the growth case, so transcribe the base-case chart values for every year and group exactly, plus the scenario table (2035 projections, absolute growth, CAGR). Record every point where it differs from the Demand-Side Final (base year, increments, seasonality 61% vs 65%, top-5 61% vs 63%). Page 3 prints the December 2025 hypothesis tree: transcribe it exactly (three pillars, six themes, 18 focus areas).' },
  diagnostic: { name: 'Current State Diagnostic v2 (December 2025)', text: `${IN}/Diagnostic_v2.txt`, src: `${UP}/01a126c7-Wesgro_Diagnostic_Report_v2.pdf`, kind: 'pdf', pages: 68,
    use: 'Chapter 1.2 baseline (arrivals FY15/16 to FY24/25, spend, length of stay, source-market trend, 72.5% Metro GDPR and the other district GDPR shares, one airline to Asia against ten to Africa, stakeholder map, cruise vessels, passengers, direct jobs and GDP contribution by season, rail and utility constraints), folded into 2.1 (concentration, seasonality, segments) and 2.5 (Metro concentration, regional profiles). Any tourism EMPLOYMENT figure for the Western Cape (jobs, employment share, Employment Absorption page) must be transcribed exactly with its source, because the jobs indicator depends on it. Transcribe the December hypothesis tree printed near the end exactly, including the governance entry wording "(Wesgro, DEDAT, CTT)".' },
  midas: { name: 'MIDAS Aviation Market Assessment (final draft, file dated 20.04.26)', text: `${IN}/MIDAS_Aviation_20.04.26.md`, src: `${UP}/a6e8ddc6-Final_Draft_Report_-_MIDAS_outputs_20.04.26.docx`, kind: 'docx', pages: null,
    use: 'Chapter 2.2 and 3.2.1. Expected: one airline to Asia against ten to Africa; 16 of 27 routes above 80% load and a 76.0% network figure (the text mentions 29 international destinations and individual route loads such as Newark 88.5%, Heathrow and Frankfurt 83%: establish what the 16 of 27 and 76.0% refer to, or report them as not found); June share of seats (expected 6.4%); routes added 2015 to 2025 (expected 17); connecting shares above 80% on Emirates; fares-before-seats behaviour; regional route loads; India, China, Australia and Saudi opportunities; new airport developments (Winelands). The docx has no page numbers: cite by numbered section heading and figure or table, and say so. Extract the 21 embedded images (unzip word/media) and view those that carry figures.' },
  benchmark: { name: 'Global Benchmarking Report (24 March 2026)', text: `${IN}/Global_Benchmark_24.03.26.txt`, src: `${UP}/5e431ff8-Global_Benchmark_Report_24.03.2026_1.pdf`, kind: 'pdf', pages: 64,
    use: 'Chapter 2.3, precedent lines in Chapter 3, Chapter 4.6 funding gap. The case set is Chile, Melbourne and Victoria, Valencia, Singapore, Kenya and New Zealand. Expected: the 30-destination screen and 12 criteria; growth rates per case (Chile ~35%, Kenya 12.8 to 14.6%, Singapore ~19%, New Zealand ~12%, Melbourne ~5.3%, Valencia 13 to 14%) with the period each covers; recovery percentages; institutional mechanisms per case (Chile ~US$900m Nuevo Pudahuel concession and open skies; New Zealand 16,000+ route-accountable bookings; Melbourne 5,000 rooms and the events model; Valencia SICTED; Singapore STB coordination; Kenya Nairobi hub and reforms); the 3 to 5% global growth norm (p7) and the 5 to 35% range; the structured framework applied per case; transferable lessons listed per case. Transcribe the summary comparison table in full.' },
  inclusion: { name: 'SME and Community Inclusion Plan (file dated 9 October 2026)', text: `${IN}/SMME_Inclusion_09.10.26.txt`, src: `${UP}/c1d1e45b-SMME_Inclusion_Strategy_09102026.pdf`, kind: 'pdf', pages: 58,
    use: 'Chapter 2.6, 3.3.1 (community inclusion at concept level), Chapter 4 inclusion pilots, Chapter 5 community-share indicator, Appendix A5. Expected: 107-community long-list (2.81 million people), 93 within 45 minutes of a node or corridor, five shortlisting criteria with weights, the 20 shortlist with region, archetype, composite score, minutes to node, population and unemployment (transcribe the whole table), four archetypes with long-list and shortlist counts, 18.4% of residents and 15.4% of [what], 0.02 to 0.04% of foreign visitor spend, R4m to R10m a year, R259m at 1% capture, 11 of 20 held back by organisation and 9 by safety perception (find the constraint tally), the one binding constraint per community, the six pathway types, the four-step order (seller with a stake, safe and workable visit, local product, exposure), the response by archetype, pilot candidates, benchmark cards, data sources (OSM Geofabrik 16 Sep 2026, Census 2011 sub-places, SAPS 2025/26, OSRM). Also record every occurrence of formalisation, 80:20, private ownership and "hub" (the final report may not propose a Wesgro-funded hub).' },
  segmentation: { name: 'Skift Segmentation Analysis v2.0 (12 March 2026)', text: `${IN}/20260312_Wesgro_Segmentation_Analysis_Skift_v2.0.md`, src: `${UP}/c02ff95d-20260312_Wesgro_Segmentation_Analysis_Skift_v2.0.docx`, kind: 'docx', pages: null,
    use: 'Working analysis behind the four segments in 2.1 and 3.1.1: segment definitions, sizes, incidence by market, demographics, booking channels, fit with the Western Cape. Cite by section heading. Secondary evidence: used only where the Demand-Side Analysis does not carry the figure.' },
  african_market: { name: 'Skift African Market Analysis memo v1 (16 March 2026)', text: `${IN}/20260316_Wesgro_African_Market_Analysis_Skift_Memo_v1.md`, src: `${UP}/e26989e8-20260316_Wesgro_African_Market_Analysis_Skift_Memo_v1.docx`, kind: 'docx', pages: null,
    use: 'Working analysis behind Build a regional foundation (Africa): addressable trips by market (Nigeria 310k to 510k, Kenya 240k to 400k, Ghana 55k to 100k), spend per visitor, traveller profiles, counter-seasonality, air links. Cite by section heading.' },
  digital: { name: 'Skift Digital and Search Insights memo (10 December 2025)', text: `${IN}/20251210_Wesgro_Digital_Analysis_Skift_Memo.md`, src: `${UP}/0a49bab5-20251210_Wesgro_Digital_Analysis_Skift_Memo.docx`, kind: 'docx', pages: null,
    use: 'Working analysis behind Make the whole province findable and bookable and the Chapter 5 tracking mechanism (quarterly digital tracking, BI dashboard, primary brand research). Cite by section heading. Short document: 15 findings are enough.' },
  inception: { name: 'Doubling Tourism Research Initiative Inception Report (27 November 2025)', text: `${IN}/Inception_27.11.25.txt`, src: `${UP}/88aa3ba3-Wesgro_Doubling_Tourism_Inception_Report_27.11.25_.pdf`, kind: 'pdf', pages: 37,
    use: 'Chapter 1.1 (objective: double international arrivals by 2035; 2.8m visitors, 300k tourism-linked jobs, 10k SMMEs, 2x airlift and cruise; Wesgro mission, vision, eight strategy statements, six outcome metrics), 1.4 (four phases with durations, deliverables per phase, session calendar, governance), Chapter 2 "what was asked" lines (phase descriptions per workstream), 4.4 stakeholder map (internal units and external stakeholders), Chapter 5 (M&E indicator list on the phase 4 plan: arrivals, spend, jobs, SMME inclusion, geographic spread, airlift, cruise volumes; definitions, sources, frequency, owners, governance), benchmarking screen (30 destinations ranked with scores and reasons, the six selected), data received list, stakeholder challenges and opportunities. Transcribe the deliverable list, the phase durations, the 30-destination screen table and the outcome metrics exactly. Record every SLA clause number it references, if any.' },
  stakeholder: { name: 'Stakeholder Insights Report (12 March 2026, phase 1)', text: `${IN}/Stakeholder_Insights_12.03.26.txt`, src: `${UP}/8f89358f-Wesgro_Stakeholder_Insights_Report_20260312_1.pdf`, kind: 'pdf', pages: 47,
    use: 'Chapter 2.4, 3.3.2 (focus areas 16 to 19), 3.3.1 (climate, LTO funding), 4.8 risk register, 5.4 data gaps, Appendix A6. Expected: the organisations engaged (count them; the brief says 16), the four engagement phases, the theme tally by hypothesis-tree element (the brief says collaboration 15, policy and data 15, route and product 11, path to purchase 11: find or reconstruct the tally from the appendix tables), the priority focus areas for further engagement, and the detailed insights tables (pillar, theme, insight, impact rating) which must be transcribed in full with the organisation each table belongs to. Quotes verbatim. Note which organisation raised each of: bilateral air agreements and open skies, eVisa, safety perception, climate events such as Meiringspoort, load-shedding and water, LTO funding and Treasury Circular 131, data access, CTIA capacity, cruise berth capacity, skills.' },
  infrastructure: { name: 'Infrastructure Report (spatial and infrastructure readiness)', text: `${IN}/Infrastructure_Report.txt`, src: `${UP}/INFRA_PLACEHOLDER.pdf`, kind: 'pdf', pages: null,
    use: 'Chapter 2.5, 3.2.1 (internal mobility), 3.2.2 (all three product focus areas), 3.3.1 (climate), Chapter 5 readiness indicators, Appendix A4. Expected: readiness scores by district and category; accessibility decay from 4.7 to 1.0; six touring routes; primary cluster, secondary corridors and cold zones; key gap per region; mid-scale bed gap; car-only access beyond the Metro and Garden Route; taxonomy and scoring rubric; the dataset limits (no geography below district; post-May expansion records are placeholders).' },
}

const EXTRACT_SCHEMA = {
  type: 'object',
  properties: {
    doc_id: { type: 'string' },
    cover_title: { type: 'string' },
    cover_date: { type: 'string' },
    page_numbering_note: { type: 'string' },
    sections: { type: 'array', items: { type: 'object', properties: { title: { type: 'string' }, pages: { type: 'string' } }, required: ['title', 'pages'] } },
    headline_findings: { type: 'array', items: { type: 'object', properties: {
      finding: { type: 'string' },
      figures: { type: 'array', items: { type: 'object', properties: { value: { type: 'string' }, page: { type: 'string' } }, required: ['value', 'page'] } },
      focus_areas: { type: 'array', items: { type: 'string' } },
      report_use: { type: 'string' },
    }, required: ['finding', 'figures', 'focus_areas', 'report_use'] } },
    expected_figures_check: { type: 'array', items: { type: 'object', properties: {
      expected: { type: 'string' }, status: { type: 'string', enum: ['found_exact', 'found_different', 'not_found'] }, found_value: { type: 'string' }, page: { type: 'string' }, note: { type: 'string' },
    }, required: ['expected', 'status', 'found_value', 'page', 'note'] } },
    banned_terms: { type: 'array', items: { type: 'string' } },
    tree_transcription: { type: 'string' },
    gaps: { type: 'array', items: { type: 'string' } },
    extract_file: { type: 'string' },
  },
  required: ['doc_id', 'cover_title', 'cover_date', 'page_numbering_note', 'sections', 'headline_findings', 'expected_figures_check', 'banned_terms', 'tree_transcription', 'gaps', 'extract_file'],
}

const VERIFY_SCHEMA = {
  type: 'object',
  properties: {
    doc_id: { type: 'string' },
    figures_checked: { type: 'number' },
    corrections: { type: 'array', items: { type: 'object', properties: { location: { type: 'string' }, was: { type: 'string' }, now: { type: 'string' }, reason: { type: 'string' } }, required: ['location', 'was', 'now', 'reason'] } },
    unverifiable: { type: 'array', items: { type: 'string' } },
    missed_material: { type: 'array', items: { type: 'string' } },
    verdict: { type: 'string', enum: ['reliable', 'reliable_after_corrections', 'unreliable'] },
  },
  required: ['doc_id', 'figures_checked', 'corrections', 'unverifiable', 'missed_material', 'verdict'],
}

const FOCUS_AREAS = `The 20 focus areas of the updated (14 October 2026) hypothesis tree, by pillar and theme:
Pillar 1 Reshape Demand. Theme 1.1 Traveller, brand and proposition: (1) Respond to growth segment traveller preferences; (2) Create green-season demand with MICE and events; (3) Make the whole province findable and bookable. Theme 1.2 Source market growth and diversification: (4) Convert India and China hub traffic; (5) Increase yield in mature markets; (6) Build a regional foundation (Africa).
Pillar 2 Transform Supply. Theme 2.1 Accessibility, connectivity and infrastructure: (7) Win direct routes and add seats on full routes; (8) Grow cruise calls and ports; (9) Accelerate tourism-enabling internal mobility. Theme 2.2 Product and destination capacity: (10) Support diversified route and product development; (11) Align visitor experience in-destination; (12) Balance impact on nature-based attractions.
Pillar 3 Build Enabling Capability. Theme 3.1 Investment, inclusion and sustainability: (13) Embed local destination bodies for community inclusion; (14) Manage climate risk and sustainable tourism; (15) Crowd in capital with targeted investment strategies. Theme 3.2 Governance and leadership: (16) Align institutional stakeholders across all three tiers; (17) Strengthen industry and government collaboration; (18) Expedite tourism-enabling policy and data sharing; (19) Lead removal of infrastructure, visa and safety deficits; (20) Develop workforce and service skills.`

const id = args && args.id
const d = Object.assign({}, REGISTRY[id] || {}, (args && args.override) || {})
if (!d.name) throw new Error('unknown doc id ' + id)
const partial = args && args.partial

function renderNote() {
  if (d.kind === 'pdf') return `The text layer of a slide deck garbles charts and tables. Render the WHOLE document once, up front: \`mkdir -p ${OUT}/pages/${id} && pdftoppm -r 60 -png "${d.src}" ${OUT}/pages/${id}/p\` (this produces p-01.png, p-02.png and so on, or p-1.png for short decks). Then Read the PNG of every page that carries a chart, table or diagram whose figures you will cite. Read several pages per turn to move quickly. Do not skip pages with numbers you cite.`
  return `For the docx, extract embedded images once: \`mkdir -p ${OUT}/media/${id} && cd ${OUT}/media/${id} && unzip -o -q "${d.src}" "word/media/*"\` and Read any image that carries figures you need. Several per turn is fine.`
}

function extractPrompt() {
  return `You are building the evidence base for the final report of Wesgro's Unlocking Tourism study (Letsema with Skift Advisory). Your document: ${d.name}.

Files: text extraction at ${d.text}; original at ${d.src} (${d.kind}${d.pages ? ', ' + d.pages + ' PDF pages, landscape slide format' : ''}).
${partial ? 'A previous reader wrote a partial extract at ' + partial + ' before being cut off. Read it, keep what is right, complete and correct it, and overwrite the file rather than starting from nothing. ' : ''}Read the WHOLE text extraction first. ${renderNote()}
How the final report will use this document: ${d.use}

${FOCUS_AREAS}

Deliver two things.
1. Write a markdown evidence extract to ${OUT}/${id}.md with these sections: Document (cover title, date, version, status, page count, page-numbering note); Structure (section list with page ranges); Findings (numbered, 20 to 40 items, 15 for a short memo; each a declarative sentence followed by the supporting figures, each figure with its page in the form (p12), and the focus area numbers it supports); Key tables (transcribe in full every table or chart series the report will need, with page); Definitions and method (base year, fiscal or calendar conventions, scope limits, the sources the document itself cites such as Stats SA, ACSA, OAG, SAT, Mero, StratEcon, Census, OSM); Expected-figure check (every figure named in the "how the final report will use this document" paragraph: found exact, found different or not found, with page); Banned-term occurrences (ecosystem, unlocking, formalisation, 80:20, private ownership) with page; Tree transcription if the document prints a hypothesis tree; Gaps (what the final report needs from this document that it does not carry).
2. Return the structured summary.

Rules. Cite the page number printed on the slide if one exists and state how it relates to the PDF index in page_numbering_note; if none is printed, cite the PDF page index and say so. Never round a figure the source states precisely. Never infer a figure from a chart without writing "read from chart". Where the document shows two values for the same quantity, record both with pages. Quotes verbatim with the organisation as given. Do not editorialise; the extract is evidence, not argument.`
}

function verifyPrompt(ex) {
  return `You are an adversarial checker. A colleague extracted evidence from ${d.name} into ${ex.extract_file}. Source: ${d.src} (${d.kind}); text layer at ${d.text}. ${d.kind === 'pdf' ? 'Rendered pages should exist in ' + OUT + '/pages/' + id + '/ (p-NN.png); if not, render the whole document with pdftoppm -r 60 -png into that folder.' : 'Embedded images are under ' + OUT + '/media/' + id + '/word/media/.'}

Your job is to find errors, not to confirm. For every figure, count, date and quotation in the extract: locate it in the source at the cited page and check value, unit, year, base (fiscal or calendar, province or Cape Town, overseas or international), wording and page. Assume the extract is wrong until the source proves it right. Then read the source end to end once and list important findings or figures the extract omitted, especially anything the final report needs for the growth case, market groups, seasonality, route loads, readiness scores, the community shortlist and spend figures, comparator growth rates and mechanisms, employment figures, and the hypothesis tree.

Fix every error directly in ${ex.extract_file} with the Edit tool (do not rewrite the file wholesale), add any material omission as new numbered findings or table rows in the right section, append a section "Verification" at the end listing what you changed and what you could not verify, then return the structured result. Count figures_checked honestly.`
}

phase('Extract')
log(`Extracting ${d.name}`)
const ex = await agent(extractPrompt(), { label: `extract:${id}`, phase: 'Extract', schema: EXTRACT_SCHEMA })
if (!ex) return { doc: id, failed: 'extract returned null' }

phase('Verify')
log(`Verifying ${id}`)
const v = await agent(verifyPrompt(ex), { label: `verify:${id}`, phase: 'Verify', schema: VERIFY_SCHEMA })

return {
  doc: id, file: ex.extract_file, cover_title: ex.cover_title, cover_date: ex.cover_date, page_note: ex.page_numbering_note,
  sections: ex.sections, n_findings: ex.headline_findings.length,
  expected: ex.expected_figures_check, banned: ex.banned_terms, tree: ex.tree_transcription ? ex.tree_transcription.slice(0, 1500) : '', gaps: ex.gaps,
  verification: v ? { verdict: v.verdict, figures_checked: v.figures_checked, corrections: v.corrections, unverifiable: v.unverifiable, missed: v.missed_material } : 'verify returned null',
}
