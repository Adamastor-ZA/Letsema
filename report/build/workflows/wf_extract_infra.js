export const meta = {
  name: 'wesgro-extract-infrastructure-final',
  description: 'Extract and verify the final Infrastructure Report (114 slides) in two page ranges',
  phases: [
    { title: 'Extract', detail: 'two readers, pages 1 to 57 and 58 to 114' },
    { title: 'Verify', detail: 'adversarial check of each half against the source' },
  ],
}

const IN = '/tmp/claude-0/-home-user-Letsema/4e1968e6-be48-539d-a4af-9019b21a7592/scratchpad/inputs'
const OUT = '/tmp/claude-0/-home-user-Letsema/4e1968e6-be48-539d-a4af-9019b21a7592/scratchpad/evidence'
const SRC = '/root/.claude/uploads/4e1968e6-be48-539d-a4af-9019b21a7592/0ce97143-Unlocking_Tourism_Growth_Infrastructure_Report__20260922.pdf'
const NAME = 'Infrastructure Report, final (Unlocking Tourism Research Initiative, file dated 22 September 2026; 114 slides)'

const PARTS = [
  { id: 'infrastructure_p1', from: 1, to: 57, text: `${IN}/Infra_Final_part1_p1-57.txt`,
    scope: 'Pages 1 to 57: cover and tree recap (p2), the Transform Supply framing (p3 to p5 executive summary), objectives and the three-layer supply system (p7 to p10), methodology, the four phases, the evaluation framework, key assumptions and the route readiness scorecard method (p11 to p19), the regional overview (p20 to p21), the Cape Metro (asset base ~20,281 assets, spatial maps, Cape Peninsula route, analysis summary, ~R30bn pipeline and gap closure, p22 to p32), the Garden Route (asset base, maps, route pages, second engine, George Airport expansion by 2028, p33 to p43), the Cape Winelands (asset base ~7,730, maps, route, R8bn airport, p44 to p54) and the West Coast opening pages (asset base 4,752, p55 to p57).' },
  { id: 'infrastructure_p2', from: 58, to: 114, text: `${IN}/Infra_Final_part2_p58-114.txt`,
    scope: 'Pages 58 to 114: the West Coast maps, routes, asset base and pipeline (p58 to p65), the Overberg (asset base 6,176, maps, Whale Coast route, pipeline, p66 to p76), the Central Karoo and Route 62 (asset base 1,518, maps, routes, pipeline, p77 to p87), the comparative regional analysis of attractions, services and transport including the statement that infrastructure falls away with distance from Cape Town (p88 to p90), the province-wide asset mapping (p91 to p99), rail (p100), the air access assessments of Cape Town International (binding dependency, two of seven parts full, planned fixes and dates, p101 to p103, p109), George Airport (R310m terminal expansion doubling capacity by 2028, p104 to p105), the Cape Winelands airport (p106 to p107), secondary airports (p108), the cruise terminal (~40% seasonal berth use, p110), Mossel Bay and Saldanha Bay cruise potential (p111), the port investment conclusion (p112) and the key messages slide (p114).' },
]

const FOCUS_AREAS = `The 20 focus areas of the updated (14 October 2026) hypothesis tree: FA01 Respond to growth segment traveller preferences; FA02 Create green-season demand with MICE and events; FA03 Make the whole province findable and bookable; FA04 Convert India and China hub traffic; FA05 Increase yield in mature markets; FA06 Build a regional foundation (Africa); FA07 Win direct routes and add seats on full routes; FA08 Grow cruise calls and ports; FA09 Accelerate tourism-enabling internal mobility; FA10 Support diversified route and product development; FA11 Align visitor experience in-destination; FA12 Balance impact on nature-based attractions; FA13 Embed local destination bodies for community inclusion; FA14 Manage climate risk and sustainable tourism; FA15 Crowd in capital with targeted investment strategies; FA16 Align institutional stakeholders across all three tiers; FA17 Strengthen industry and government collaboration; FA18 Expedite tourism-enabling policy and data sharing; FA19 Lead removal of infrastructure, visa and safety deficits; FA20 Develop workforce and service skills.`

const EXPECTED = `Figures the final report expects from this document (structure.md and the brief): readiness scores by district and category; accessibility decaying from 4.7 to 1.0 with distance from the Metro; six touring routes with their readiness scorecards; the primary cluster, secondary corridors and cold zones; the key gap per region; the mid-scale bed gap; car-only access beyond the Metro and Garden Route; idle assets; flagship attraction limits (Table Mountain, Robben Island, Cape Point, Boulders); the Meiringspoort flood and other climate events; the taxonomy and scoring rubric; the supply dataset limits (no geography below district; post-May expansion records are placeholders); asset counts per district and province; investment pipelines and their rand values and dates; airport capacity figures, constraints and fix dates for Cape Town International, George and Cape Winelands; cruise berth utilisation, calls and the port investment conclusion; rail status.`

const EXTRACT_SCHEMA = {
  type: 'object',
  properties: {
    part_id: { type: 'string' }, cover_date: { type: 'string' }, page_numbering_note: { type: 'string' },
    sections: { type: 'array', items: { type: 'object', properties: { title: { type: 'string' }, pages: { type: 'string' } }, required: ['title', 'pages'] } },
    n_findings: { type: 'number' },
    expected_figures_check: { type: 'array', items: { type: 'object', properties: { expected: { type: 'string' }, status: { type: 'string', enum: ['found_exact', 'found_different', 'not_found', 'outside_my_pages'] }, found_value: { type: 'string' }, page: { type: 'string' }, note: { type: 'string' } }, required: ['expected', 'status', 'found_value', 'page', 'note'] } },
    banned_terms: { type: 'array', items: { type: 'string' } },
    gaps: { type: 'array', items: { type: 'string' } },
    extract_file: { type: 'string' },
  },
  required: ['part_id', 'cover_date', 'page_numbering_note', 'sections', 'n_findings', 'expected_figures_check', 'banned_terms', 'gaps', 'extract_file'],
}
const VERIFY_SCHEMA = {
  type: 'object',
  properties: {
    part_id: { type: 'string' }, figures_checked: { type: 'number' },
    corrections: { type: 'array', items: { type: 'object', properties: { location: { type: 'string' }, was: { type: 'string' }, now: { type: 'string' }, reason: { type: 'string' } }, required: ['location', 'was', 'now', 'reason'] } },
    unverifiable: { type: 'array', items: { type: 'string' } },
    missed_material: { type: 'array', items: { type: 'string' } },
    high_value_facts: { type: 'array', items: { type: 'string' } },
    verdict: { type: 'string', enum: ['reliable', 'reliable_after_corrections', 'unreliable'] },
  },
  required: ['part_id', 'figures_checked', 'corrections', 'unverifiable', 'missed_material', 'high_value_facts', 'verdict'],
}

function extractPrompt(p) {
  return `You are building the evidence base for the final report of Wesgro's Unlocking Tourism study (Letsema with Skift Advisory). Your document: ${NAME}. You cover PDF pages ${p.from} to ${p.to} only; a colleague covers the rest.

Files: text layer for your pages, with "===== PDF PAGE n =====" markers, at ${p.text}; the original PDF at ${SRC} (landscape slides, 114 pages). Render your pages once up front: \`mkdir -p ${OUT}/pages/infrastructure_final && pdftoppm -r 60 -png -f ${p.from} -l ${p.to} "${SRC}" ${OUT}/pages/infrastructure_final/p\` (files p-001.png onwards, numbered by PDF page). Then Read the PNG of every page that carries a chart, table, map, scorecard or diagram whose figures you will cite; several per turn. Maps and scorecards hold most of the figures in this deck, so read them; where a value is read off a chart or colour scale rather than printed, write "read from chart".

Your scope: ${p.scope}

${EXPECTED}

${FOCUS_AREAS}

Deliver two things.
1. Write a markdown evidence extract to ${OUT}/${p.id}.md with these sections: Document (cover title, date, version, status, page count, page-numbering note, the pages you cover); Structure (section list with page ranges for your pages); Findings (numbered, 30 to 50 items; each a declarative sentence followed by the supporting figures, each figure with its page in the form (p12), and the focus area numbers it supports); Key tables (transcribe in full every scorecard, readiness table, asset-count table, pipeline table with rand values and dates, airport capacity table and cruise table in your pages, with page); Definitions and method (taxonomy, scoring rubric, assumptions, data sources the document cites, dataset limits); Expected-figure check (every item in the expected list: found exact, found different, not found, or outside my pages, with page); Banned-term occurrences (ecosystem, unlocking, formalisation, 80:20, private ownership) with page; Gaps (what the final report needs from these pages that they do not carry).
2. Return the structured summary.

Rules. No page numbers are printed on the slides, so cite the PDF page index. Never round a figure the source states precisely. Where the document shows two values for the same quantity, record both with pages. Quote slide titles verbatim where they carry the finding. Do not editorialise.`
}

function verifyPrompt(p, ex) {
  return `You are an adversarial checker. A colleague extracted evidence from ${NAME}, PDF pages ${p.from} to ${p.to}, into ${ex.extract_file}. Source PDF: ${SRC}; text layer for these pages at ${p.text}; rendered pages in ${OUT}/pages/infrastructure_final/ (p-NNN.png by PDF page; render any missing one with pdftoppm -r 60 -png -f N -l N).

Your job is to find errors, not to confirm. For every figure, count, rand value, date, score and page reference in the extract: locate it in the source at the cited page and check value, unit, year, scope (province, district, route, node) and page. Assume the extract is wrong until the source proves it right. Then read all pages ${p.from} to ${p.to} once and list important findings or figures the extract omitted, especially readiness scores, asset counts, pipeline values and dates, airport and cruise capacity figures, route scorecards and the comparative statements about distance from Cape Town.

Fix every error directly in ${ex.extract_file} with the Edit tool (never rewrite wholesale; never delete evidence), add material omissions as new numbered findings or table rows, append a "## Verification" section listing what you changed and could not verify, and return the structured result with up to 12 high-value facts with pages. Count figures_checked honestly.`
}

phase('Extract')
log('Two readers on the final Infrastructure Report')
const results = await pipeline(
  PARTS,
  (p) => agent(extractPrompt(p), { label: `extract:${p.id}`, phase: 'Extract', schema: EXTRACT_SCHEMA }),
  (ex, p) => ex ? agent(verifyPrompt(p, ex), { label: `verify:${p.id}`, phase: 'Verify', schema: VERIFY_SCHEMA }).then((v) => ({ part: p.id, extract: ex, verification: v })) : { part: p.id, failed: 'extract returned null' },
)
return results
