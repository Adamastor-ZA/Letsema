export const meta = {
  name: 'wesgro-draft-ch3',
  description: 'Draft one Chapter 3 unit (a focus-area entry, a pillar introduction or the integrated case) with an adversarial review',
  phases: [
    { title: 'Draft', detail: 'writer' },
    { title: 'Review', detail: 'fact, template and style check with fixes in place' },
  ],
}

const IN = '/tmp/claude-0/-home-user-Letsema/4e1968e6-be48-539d-a4af-9019b21a7592/scratchpad/inputs'
const EV = '/tmp/claude-0/-home-user-Letsema/4e1968e6-be48-539d-a4af-9019b21a7592/scratchpad/evidence'
const REPO = '/home/user/Letsema/report'
const CONTENT = `${REPO}/build/content/ch3`
const STYLE = '/root/.claude/skills/synced/1d797b75-a9af-4564-9806-faaa7d08ed42_a0274f8f-f6a5-4577-8bab-dba35eb89302/michael-writing-style/SKILL.md'

const EXTRACTS = {
  demand_side: 'Demand-Side Analysis, Jun 2026', market_assessment: 'Market Assessment Report, May 2026', diagnostic: 'Current State Diagnostic, Dec 2025',
  midas: 'MIDAS Aviation Market Assessment, Mar 2026 (cite by section title)', benchmark: 'Global Benchmarking Report, Mar 2026', inclusion: 'SME and Community Inclusion Plan, Oct 2026',
  segmentation: 'Skift Segmentation Analysis, Mar 2026 (cite by section)', african_market: 'Skift African Market Analysis memo, Mar 2026 (cite by section)', digital: 'Skift Digital and Search Insights memo, Dec 2025 (cite by section)',
  inception: 'Inception Report, Nov 2025', stakeholder: 'Stakeholder Insights Report, Mar 2026', infrastructure_p1: 'Infrastructure Report, Jul 2026 (final, file dated 22 Sep 2026; pages 1 to 57)', infrastructure_p2: 'Infrastructure Report, Jul 2026 (final, file dated 22 Sep 2026; pages 58 to 114)',
}
const extractList = Object.entries(EXTRACTS).map(([k, v]) => `${EV}/${k}.md (${v})`).join('; ')

const FA = {
  FA01: { pillar: 1, theme: '3.1.1 Traveller, brand and proposition', name: 'Respond to growth segment traveller preferences', sheet: 't11', file: '11_fa01.json' },
  FA02: { pillar: 1, theme: '3.1.1 Traveller, brand and proposition', name: 'Create green-season demand with MICE and events', sheet: 't11', file: '12_fa02.json' },
  FA03: { pillar: 1, theme: '3.1.1 Traveller, brand and proposition', name: 'Make the whole province findable and bookable', sheet: 't11', file: '13_fa03.json' },
  FA04: { pillar: 1, theme: '3.1.2 Source market growth and diversification', name: 'Convert India and China hub traffic', sheet: 't12', file: '14_fa04.json' },
  FA05: { pillar: 1, theme: '3.1.2 Source market growth and diversification', name: 'Increase yield in mature markets', sheet: 't12', file: '15_fa05.json' },
  FA06: { pillar: 1, theme: '3.1.2 Source market growth and diversification', name: 'Build a regional foundation (Africa)', sheet: 't12', file: '16_fa06.json' },
  FA07: { pillar: 2, theme: '3.2.1 Accessibility, connectivity and infrastructure', name: 'Win direct routes and add seats on full routes', sheet: 't21', file: '21_fa07.json' },
  FA08: { pillar: 2, theme: '3.2.1 Accessibility, connectivity and infrastructure', name: 'Grow cruise calls and ports', sheet: 't21', file: '22_fa08.json' },
  FA09: { pillar: 2, theme: '3.2.1 Accessibility, connectivity and infrastructure', name: 'Accelerate tourism-enabling internal mobility', sheet: 't21', file: '23_fa09.json' },
  FA10: { pillar: 2, theme: '3.2.2 Product and destination capacity', name: 'Support diversified route and product development', sheet: 't22', file: '24_fa10.json' },
  FA11: { pillar: 2, theme: '3.2.2 Product and destination capacity', name: 'Align visitor experience in-destination', sheet: 't22', file: '25_fa11.json' },
  FA12: { pillar: 2, theme: '3.2.2 Product and destination capacity', name: 'Balance impact on nature-based attractions', sheet: 't22', file: '26_fa12.json' },
  FA13: { pillar: 3, theme: '3.3.1 Investment, inclusion and sustainability', name: 'Embed local destination bodies for community inclusion', sheet: 't31', file: '31_fa13.json' },
  FA14: { pillar: 3, theme: '3.3.1 Investment, inclusion and sustainability', name: 'Manage climate risk and sustainable tourism', sheet: 't31', file: '32_fa14.json' },
  FA15: { pillar: 3, theme: '3.3.1 Investment, inclusion and sustainability', name: 'Crowd in capital with targeted investment strategies', sheet: 't31', file: '33_fa15.json' },
  FA16: { pillar: 3, theme: '3.3.2 Governance and leadership', name: 'Align institutional stakeholders across all three tiers', sheet: 't32', file: '34_fa16.json' },
  FA17: { pillar: 3, theme: '3.3.2 Governance and leadership', name: 'Strengthen industry and government collaboration', sheet: 't32', file: '35_fa17.json' },
  FA18: { pillar: 3, theme: '3.3.2 Governance and leadership', name: 'Expedite tourism-enabling policy and data sharing', sheet: 't32', file: '36_fa18.json' },
  FA19: { pillar: 3, theme: '3.3.2 Governance and leadership', name: 'Lead removal of infrastructure, visa and safety deficits', sheet: 't32', file: '37_fa19.json' },
  FA20: { pillar: 3, theme: '3.3.2 Governance and leadership', name: 'Develop workforce and service skills', sheet: 't32', file: '38_fa20.json' },
}
const PILLARS = {
  1: { h2: '3.1 Pillar 1: Reshape Demand', file: '10_pillar1.json', intro: 'Break through market, seasonality and spread ceilings. Themes 3.1.1 Traveller, brand and proposition (FA01 to FA03) and 3.1.2 Source market growth and diversification (FA04 to FA06).' },
  2: { h2: '3.2 Pillar 2: Transform Supply', file: '20_pillar2.json', intro: 'Remove mobility, infrastructure and product constraints. Themes 3.2.1 Accessibility, connectivity and infrastructure (FA07 to FA09) and 3.2.2 Product and destination capacity (FA10 to FA12).' },
  3: { h2: '3.3 Pillar 3: Build Enabling Capability', file: '30_pillar3.json', intro: 'An inclusive, well-governed system. Themes 3.3.1 Investment, inclusion and sustainability (FA13 to FA15) and 3.3.2 Governance and leadership (FA16 to FA20), which also holds the deficits entry moved from theme 2.1 and the flagged workforce entry.' },
}

const COMMON = `You are drafting part of Chapter 3, Findings and recommendations, of the final research report of Wesgro's Unlocking Tourism study: "Unlocking Tourism Growth: A Strategy for the Western Cape to 2035", by Letsema in partnership with Skift Advisory. The report is the contractual Final Research Report under SLA Annexure B clause 1.1.14, goes to Steerco, Exco and the Board, and launches in February 2027. Write for a Board member who has not read the interim deliverables and a programme owner who will run the plan for eight years. Chapter 3 follows the updated hypothesis tree exactly: three pillars, six themes, 20 focus areas.

The argument that runs through every chapter: Western Cape tourism growth is supply-constrained, not demand-constrained. The destination has recovered (1.44m international arrivals at Cape Town International in FY24/25 against 1.16m in FY19/20) and the next step of growth, to 2.5m, is capped by air seats, bookability, internal mobility and institutional alignment. Cape Town is the functional axle of the system, where international visitors arrive and disperse; never frame Route 62 or any other route as the axle. Say "doubling" only when quoting the original mandate; the strategy's language is growth to 2.5m. The confirmed growth case: 2025 base 1,498,829 arrivals (Market Assessment Report, May 2026, p19) to 2,175,778 base and 2,516,282 accelerated in 2035; the base case passes the 1.8m inbound seat ceiling at the 2030 year point.

READ FIRST, in full: the writing rules at ${STYLE}; the Chapter 3 part of ${IN}/structure.md; the confirmed decisions in ${REPO}/plan.md section 3; the discrepancy log ${REPO}/discrepancies.md (use the "value the report will use" column); the tree record ${REPO}/evidence/tree.md; the traceability table ${REPO}/traceability.csv (initiative and indicator codes per focus area). Then the fact sheet for your theme and the extracts it cites, in full (each extract ends with a Verification section whose corrections override the body): ${extractList}. The extracts and fact sheets are the ONLY sources of figures. Never draft from memory, never from the 14 October deck (not in hand), never from structure.md as if it were evidence.

EVIDENCE RULES. Every figure carries a source and page in the form (Demand-Side Analysis, Jun 2026, p21), with the cover dates in the extract list; page numbers are PDF page indices; MIDAS and the Skift memos are cited by section title. Where inputs disagree, use the value discrepancies.md says the report uses. Where the structure's one-line reason names a figure no input supports (for example "16 of 27 routes above 80%", "70% by phone", "plan to 250", "15 of 16 organisations", "4.7 to 1.0"), use the supported figure from the fact sheet and, where none exists, a square-bracketed placeholder stating what is needed. Do not invent figures, owners, costs or dates. Precedent lines may draw on a destination outside the comparator set only from a public source, labelled as such.

WRITING RULES. UK English. No em dashes, no en dashes in prose, no Oxford comma. Topic sentence first in every paragraph. Strong verbs, lean prose, declarative register, confident where the evidence supports it. Sentences under 25 words where the content allows and never over 35. Paragraphs of three sentences or fewer. Inline enumeration rather than bullets for arguments. Tables for tabular content. Every table and figure has a numbered caption written as a declarative sentence and a source line. Banned: ecosystem, unlocking (except the report title), formalisation, 80:20, private ownership, leverage, delve, synergy, navigate, robust, game-changer, intensifiers (really, very, incredibly, truly, deeply). No filler, no "this section will", no recap paragraphs. Headings are short noun phrases. Public-agency frame: Wesgro's mandate and the provincial sphere; national levers named as national and escalated, not assumed.

OUTPUT FORMAT. Write ONE JSON file at the path given below, shaped {"id": "...", "title": "...", "blocks": [ ... ]}. Block types: {"type":"kicker","text"} (rendered in small caps, carries the theme reference); {"type":"h2","text"}, {"type":"h3","text"}, {"type":"h4","text"}; {"type":"lead","text"} (one declarative sentence); {"type":"p","text"} (inline **bold** and *italic*; square-bracketed text renders as a highlighted placeholder); {"type":"numbered","items"}; {"type":"bullets","items"}; {"type":"table","caption","source","columns":[{"header","width","align"}],"rows":[[...]],"boldFirstCol":true}; {"type":"box","title","paras"}; {"type":"figure","id":"fig_<unique>","caption","source","chart":{...}} with chart one of {"type":"line","categories","series":[{"name","values"}],"unit","yMin","refLines":[{"value","label"}]}, {"type":"bar","categories","series","unit"}, {"type":"hbar","categories","values","unit","highlight":[i]}, {"type":"stacked","categories","series","unit"}; {"type":"quote","text","attribution"}. Table and figure numbers are assigned automatically; refer to them by subject, never by number, and keep "Figure" and "Table" out of captions. Keep JSON valid. Write nothing except the JSON file and your final summary.`

const FA_TEMPLATE = (code, f) => `YOUR UNIT: focus area ${code}, "${f.name}", theme ${f.theme}. Output path: ${CONTENT}/${f.file}. Fact sheet: ${REPO}/evidence/factsheet_${f.sheet}.md (its section for ${code} carries the disposition record, evidence rows, precedent, stakeholder evidence, the deliverables' own recommendations and indicator candidates; audit notes at its end override the body).

Length: 2 to 4 pages, target 3 (about 1,000 words of prose plus one evidence table and, where the data earns it, one figure).

THE SIX-PART TEMPLATE, in this exact order and with these exact headings:
1. {"type":"kicker","text":"${f.theme}"} then {"type":"h3","text":"${f.name}"} then one {"type":"lead"}: a single declarative topline sentence that the executive summary will lift verbatim. It must state the finding and the direction of the recommendation in one breath, carry one anchoring figure, and be under 30 words.
2. {"type":"h4","text":"Hypothesis and disposition"}: a two-column table (columns "Item" and "Record"; rows: December 2025 hypothesis as worded on the December tree; Disposition (Validated, Refined, Reworded, New, Withdrawn, Flagged or Moved); Reason in one line with its figure and source; Workstream that drove it) followed by one short paragraph on what the evidence changed.
3. {"type":"h4","text":"Evidence"}: a table of three to six findings (columns "Finding", "Figure", "Source"), each finding a declarative sentence, each source in the citation form with page, drawn from the fact sheet; then one to three paragraphs that argue from the table to the recommendation, naming the Chapter 2 section the reader can go to. An optional figure drawn from extract data.
4. {"type":"h4","text":"Recommendation"}: three paragraphs, each opening with a bold label: **What Wesgro does.** (within its mandate and units: Cape Town Air Access, Cruise Cape Town, Convention Bureau, Destination Marketing, Research, Tourism); **What Wesgro asks partners to do.** (DEDAT, City of Cape Town and Cape Town Tourism, districts and LTOs, ACSA, industry bodies); **What sits outside the province and is escalated.** (national levers such as bilateral air service agreements, visas, Home Affairs, ports; name the route of escalation). Recommendations must follow from the evidence table and from what the deliverables themselves recommend; no new programmes the inputs do not support. Keep inclusion material (FA13) at concept level: a seller with a stake, a safe way in, demand pulled from the adjacent node; no roles or funding (Chapter 4), no Wesgro-funded hub, no trade-mission incentives.
5. {"type":"h4","text":"Benchmark precedent"}: two sentences from the Benchmarking Report with page, or one sentence saying no comparator case speaks to it and naming the nearest.
6. {"type":"h4","text":"Link forward"}: one paragraph naming the Chapter 4 initiative code(s) and the Chapter 5 indicator code(s) from traceability.csv for ${code}, with the indicator's baseline value and source where the fact sheet gives one. If the codes are empty in the table, write [initiative code to be assigned] and [indicator code to be assigned].

Special instructions. FA20 is Flagged and untested: write it as a recommendation to commission the labour analysis, not as a finding; its evidence table holds what the inputs do say about skills and the absence of a labour baseline (see ${REPO}/evidence/jobs_research.md for the public figures found, cited as public sources). FA19 is the entry moved from theme 2.1: say so in the disposition record and keep the recommendation to escalation. FA08 is New: the cruise evidence sits in the Diagnostic p37, the Infrastructure Report p110 to p112 and the Stakeholder report (Mossel Bay); the "plan to 250" calls figure is unsupported and becomes a placeholder.`

const PILLAR_TEMPLATE = (n, p) => `YOUR UNIT: the one-page introduction to Pillar ${n}. Output path: ${CONTENT}/${p.file}. Blocks: {"type":"h2","text":"${p.h2}"}, one lead, then two or three paragraphs (about 350 words) that state the ceiling this pillar breaks (${p.intro}), the two themes and the sequence in which the focus areas work together, and one table listing the pillar's focus areas (columns "Focus area", "Disposition", "What changed", "Chapter 4 initiatives") filled from ${REPO}/evidence/tree.md and ${REPO}/traceability.csv. No evidence table, no figure. Do not pre-empt the toplines of the entries.`

const INTEGRATED_TEMPLATE = `YOUR UNIT: section 3.4, The integrated case. Output path: ${CONTENT}/40_integrated.json. Three pages. Blocks: {"type":"h2","text":"3.4 The integrated case"}, one lead, then: how the three pillars combine into the 2.52m accelerated case (what the Market Assessment and Demand-Side Analysis say drives the step from base to accelerated: confirmed new direct airlift, above-baseline activation in India, China, the USA and the GCC, hub carriers adding Cape Town capacity, Japan and South Korea introduced; Market Assessment Report, May 2026, p18 to p19; Demand-Side Analysis, Jun 2026, p19 to p20); the seat ceiling in 2030 as the binding constraint (base case 1,802,929 at the 2030 year point against 1.8m; the airport capacity findings in the Infrastructure Report, Jul 2026, p101 to p103 and p109, with the fix dates); what happens to the base case if the supply moves slip (the conservative case 1,822,634 and the deliverables' own words that volume reverts to base without confirmed routes); one figure of the three paths against the seat ceiling (line chart from the Market Assessment p19 to p20 year points; the accelerated and conservative paths have only 2025 and 2035 end points, so plot them as two-point lines and say so in the caption); and a closing page on sequencing: air access and bookability move first because every other lever runs through them, which bridges into Chapter 4 (name the Phase 1 emphasis: air access, bookability, green-season events and the inclusion pilots). End on a short, hard sentence; no recap.`

const DRAFT_SCHEMA = { type: 'object', properties: { file: { type: 'string' }, words: { type: 'number' }, tables: { type: 'number' }, figures: { type: 'number' }, topline: { type: 'string' }, placeholders: { type: 'array', items: { type: 'string' } }, notes: { type: 'string' } }, required: ['file', 'words', 'tables', 'figures', 'topline', 'placeholders', 'notes'] }
const REVIEW_SCHEMA = { type: 'object', properties: { file: { type: 'string' }, figures_checked: { type: 'number' }, fact_corrections: { type: 'array', items: { type: 'object', properties: { was: { type: 'string' }, now: { type: 'string' }, source: { type: 'string' } }, required: ['was', 'now', 'source'] } }, style_fixes: { type: 'number' }, template_issues_fixed: { type: 'array', items: { type: 'string' } }, remaining_placeholders: { type: 'array', items: { type: 'string' } }, topline_after: { type: 'string' }, words_after: { type: 'number' }, verdict: { type: 'string', enum: ['ready', 'ready_after_fixes', 'needs_rewrite'] } }, required: ['file', 'figures_checked', 'fact_corrections', 'style_fixes', 'template_issues_fixed', 'remaining_placeholders', 'topline_after', 'words_after', 'verdict'] }

const mode = (args && args.mode) || 'fa'
let unitLabel, unitPrompt, outFile, isFA = false
if (mode === 'fa') {
  const code = args.fa; const f = FA[code]
  if (!f) throw new Error('unknown focus area ' + code)
  unitLabel = code; unitPrompt = FA_TEMPLATE(code, f); outFile = `${CONTENT}/${f.file}`; isFA = true
} else if (mode === 'pillar') {
  const p = PILLARS[args.pillar]
  if (!p) throw new Error('unknown pillar')
  unitLabel = `pillar${args.pillar}`; unitPrompt = PILLAR_TEMPLATE(args.pillar, p); outFile = `${CONTENT}/${p.file}`
} else if (mode === 'integrated') {
  unitLabel = '3.4'; unitPrompt = INTEGRATED_TEMPLATE; outFile = `${CONTENT}/40_integrated.json`
} else throw new Error('unknown mode')

phase('Draft')
log(`Drafting ${unitLabel}`)
const d = await agent(`${COMMON}\n\n${unitPrompt}\n\nWhen done, return the structured summary (prose word count, tables, figures, the topline sentence verbatim, every placeholder left and why).`, { label: `draft:${unitLabel}`, phase: 'Draft', schema: DRAFT_SCHEMA })
if (!d) return { unit: unitLabel, failed: 'draft returned null' }

phase('Review')
const r = await agent(`You are the adversarial reviewer of a drafted unit of Chapter 3 of the Wesgro final report: ${unitLabel}, at ${outFile}. The writer reported ${d.words} words, ${d.tables} tables, ${d.figures} figures and the topline "${d.topline}".

Read first: the writing rules at ${STYLE}; ${REPO}/plan.md section 3; ${REPO}/discrepancies.md; ${REPO}/evidence/tree.md; ${REPO}/traceability.csv; the unit brief below. Then read the draft JSON in full and the fact sheet and extracts it cites: ${extractList}.

Check and FIX IN PLACE with the Edit tool, keeping the JSON valid:
1. Facts. For every figure, date, count, name and quotation: find it in the cited extract at the cited page. Wrong value, page, document or basis, or an uncited figure: fix it or replace it with a square-bracketed placeholder. Any figure only the 14 October deck or structure.md carries becomes a placeholder. Verify chart data against the extract. Check the disposition record against tree.md and the December wording against the December tree transcription.
2. Writing rules. UK English; no em or en dashes; no Oxford commas; no banned words; sentences under 35 words; paragraphs of three sentences or fewer; topic sentence first; no filler or recap; headings are short noun phrases; captions declarative with a source line. Rewrite offending sentences in the house voice. The lead must be one declarative sentence under 30 words that the executive summary can lift verbatim.
3. Template. ${isFA ? 'Six parts in order with the exact h4 headings "Hypothesis and disposition", "Evidence", "Recommendation", "Benchmark precedent", "Link forward"; the kicker precedes the h3; the lead follows the h3; the recommendation has the three bold labels; the Link forward codes match traceability.csv; the evidence table has three to six rows with figures and page-referenced sources. Length 2 to 4 pages (900 to 1,800 words of prose plus tables).' : 'The unit matches its brief in structure and length.'}
4. Argument. The unit serves the carried argument (supply-constrained growth, Cape Town the axle, growth to 2.5m) without repeating it verbatim; recommendations follow from the evidence and from the deliverables' own recommendations; national levers are escalated, not assumed; inclusion material stays at concept level with no banned terms.

UNIT BRIEF: ${unitPrompt}

Return the structured result.`, { label: `review:${unitLabel}`, phase: 'Review', schema: REVIEW_SCHEMA })

return { unit: unitLabel, file: outFile, draft: { words: d.words, tables: d.tables, figures: d.figures, topline: d.topline, placeholders: d.placeholders }, review: r }
