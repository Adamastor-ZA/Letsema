export const meta = {
  name: 'wesgro-verify-content',
  description: 'Check every cited figure in a chapter\'s content files against the evidence extracts by targeted grep, fixing errors in place',
  phases: [{ title: 'Verify', detail: 'citation-by-citation grep check' }],
}

const EV = '/tmp/claude-0/-home-user-Letsema/4e1968e6-be48-539d-a4af-9019b21a7592/scratchpad/evidence'
const REPO = '/home/user/Letsema/report'
const dir = args && args.dir
if (!dir) throw new Error('args.dir required, e.g. ch1')
const files = (args && args.files) || null

const SCHEMA = {
  type: 'object',
  properties: {
    files_checked: { type: 'array', items: { type: 'string' } },
    citations_checked: { type: 'number' },
    corrections: { type: 'array', items: { type: 'object', properties: { file: { type: 'string' }, was: { type: 'string' }, now: { type: 'string' }, evidence: { type: 'string' } }, required: ['file', 'was', 'now', 'evidence'] } },
    unverifiable: { type: 'array', items: { type: 'string' } },
    verdict: { type: 'string', enum: ['reliable', 'reliable_after_corrections', 'unreliable'] },
  },
  required: ['files_checked', 'citations_checked', 'corrections', 'unverifiable', 'verdict'],
}

const DOCMAP = `Document name in a citation -> extract file: "Current State Diagnostic" -> ${EV}/diagnostic.md; "Inception Report" -> ${EV}/inception.md; "Market Assessment Report" -> ${EV}/market_assessment.md; "Demand-Side Analysis" -> ${EV}/demand_side.md; "MIDAS Aviation Market Assessment" -> ${EV}/midas.md (cited by section title, no pages); "Global Benchmarking Report" -> ${EV}/benchmark.md; "Stakeholder Insights Report" -> ${EV}/stakeholder.md; "Infrastructure Report" (Jul 2026) -> ${EV}/infrastructure_p1.md for pages 1 to 57 and ${EV}/infrastructure_p2.md for pages 58 to 114; "SME and Community Inclusion Plan" -> ${EV}/inclusion.md; "Skift Segmentation Analysis" -> ${EV}/segmentation.md; "Skift African Market Analysis" -> ${EV}/african_market.md; "Skift Digital and Search Insights" -> ${EV}/digital.md. Public sources (marked "public source") are checked against ${REPO}/evidence/jobs_research.md only.`

phase('Verify')
const v = await agent(`You are the figure checker for Chapter content of Wesgro's Unlocking Tourism final report. Content files: ${REPO}/build/content/${dir}/${files ? files.join(', ' + REPO + '/build/content/' + dir + '/') : '*.json'}. Each file is JSON with "blocks"; prose blocks carry citations in the form (Document, Mon YYYY, pNN) and figures.

${DOCMAP}

WORKING METHOD, which keeps your reading small. Do NOT read any extract file from top to bottom. For each citation in the content: (1) note every number, date, name or quotation the sentence (or table row or chart series) attaches to that citation; (2) run Grep on the mapped extract file for the page tag (for example "p25" or "(p25") and separately for the distinctive number or phrase, with a few lines of context; (3) judge whether the extract supports the value, the unit, the year, the basis (fiscal or calendar, province or Cape Town, overseas or international) and the page. Where a sentence says "computed from" or "derived", recompute from the extract's figures. For chart data series, check each value against the extract's table. Where a figure is marked as a public source, check it against jobs_research.md.

FIXES. Where the extract gives a different value, page or basis, correct the content in place with the Edit tool, keeping the JSON valid (escape quotes; no trailing commas). Where you cannot find support at all, replace the figure with a square-bracketed placeholder that states what is needed, and list it under unverifiable. Do not change wording beyond what the correction needs. Never delete a citation to avoid checking it.

Also check for terms the report bans outside quotations: ecosystem, unlocking (except the report title), formalisation, 80:20, private ownership, and any em dash. Fix them.

Return the structured result: files checked, number of citations checked, every correction with the evidence line that justified it, what remains unverifiable, and a verdict.`, { label: `verify:${dir}`, phase: 'Verify', schema: SCHEMA })
return v
