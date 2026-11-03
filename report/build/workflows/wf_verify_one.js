export const meta = {
  name: 'wesgro-verify-one',
  description: 'Adversarially verify an existing evidence extract against its source document',
  phases: [{ title: 'Verify', detail: 'figure-by-figure check against the source' }],
}

const IN = '/tmp/claude-0/-home-user-Letsema/4e1968e6-be48-539d-a4af-9019b21a7592/scratchpad/inputs'
const UP = '/root/.claude/uploads/4e1968e6-be48-539d-a4af-9019b21a7592'
const OUT = '/tmp/claude-0/-home-user-Letsema/4e1968e6-be48-539d-a4af-9019b21a7592/scratchpad/evidence'

const REGISTRY = {
  demand_side: { name: 'Demand-Side Analysis (cover June 2026)', text: `${IN}/Demand_Side_Final_01.10.txt`, src: `${UP}/ba362155-Wesgro_Demand-Side_Analysis_Final_01.10.pdf`, kind: 'pdf' },
  market_assessment: { name: 'Market Assessment Report (May 2026)', text: `${IN}/Market_Assessment_May2026.txt`, src: `${UP}/eddf3a01-Doubling_Toursim_Market_Assessment_Report_May_2026.pdf`, kind: 'pdf' },
  diagnostic: { name: 'Current State Diagnostic v2 (December 2025)', text: `${IN}/Diagnostic_v2.txt`, src: `${UP}/01a126c7-Wesgro_Diagnostic_Report_v2.pdf`, kind: 'pdf' },
  midas: { name: 'MIDAS Aviation Market Assessment (March 2026, file 20.04.26)', text: `${IN}/MIDAS_Aviation_20.04.26.md`, src: `${UP}/a6e8ddc6-Final_Draft_Report_-_MIDAS_outputs_20.04.26.docx`, kind: 'docx' },
  benchmark: { name: 'Global Benchmarking Report (March 2026)', text: `${IN}/Global_Benchmark_24.03.26.txt`, src: `${UP}/5e431ff8-Global_Benchmark_Report_24.03.2026_1.pdf`, kind: 'pdf' },
  inclusion: { name: 'SME and Community Inclusion Plan (file dated 9 October 2026)', text: `${IN}/SMME_Inclusion_09.10.26.txt`, src: `${UP}/c1d1e45b-SMME_Inclusion_Strategy_09102026.pdf`, kind: 'pdf' },
  segmentation: { name: 'Skift Segmentation Analysis v2.0 (12 March 2026)', text: `${IN}/20260312_Wesgro_Segmentation_Analysis_Skift_v2.0.md`, src: `${UP}/c02ff95d-20260312_Wesgro_Segmentation_Analysis_Skift_v2.0.docx`, kind: 'docx' },
  african_market: { name: 'Skift African Market Analysis memo v1 (16 March 2026)', text: `${IN}/20260316_Wesgro_African_Market_Analysis_Skift_Memo_v1.md`, src: `${UP}/e26989e8-20260316_Wesgro_African_Market_Analysis_Skift_Memo_v1.docx`, kind: 'docx' },
  inception: { name: 'Inception Report (27 November 2025)', text: `${IN}/Inception_27.11.25.txt`, src: `${UP}/88aa3ba3-Wesgro_Doubling_Tourism_Inception_Report_27.11.25_.pdf`, kind: 'pdf' },
  stakeholder: { name: 'Stakeholder Insights Report (12 March 2026)', text: `${IN}/Stakeholder_Insights_12.03.26.txt`, src: `${UP}/8f89358f-Wesgro_Stakeholder_Insights_Report_20260312_1.pdf`, kind: 'pdf' },
  infrastructure: { name: 'Infrastructure Report (June 2026 draft)', text: `${IN}/Infrastructure_Report.txt`, src: `${UP}/b3fec3ef-Unlocking_Tourism_Growth_Supply_Side.pdf`, kind: 'pdf' },
}

const VERIFY_SCHEMA = {
  type: 'object',
  properties: {
    doc_id: { type: 'string' },
    figures_checked: { type: 'number' },
    corrections: { type: 'array', items: { type: 'object', properties: { location: { type: 'string' }, was: { type: 'string' }, now: { type: 'string' }, reason: { type: 'string' } }, required: ['location', 'was', 'now', 'reason'] } },
    unverifiable: { type: 'array', items: { type: 'string' } },
    missed_material: { type: 'array', items: { type: 'string' } },
    high_value_facts: { type: 'array', items: { type: 'string' }, description: 'up to 12 facts from this document the final report must carry, each with page' },
    verdict: { type: 'string', enum: ['reliable', 'reliable_after_corrections', 'unreliable'] },
  },
  required: ['doc_id', 'figures_checked', 'corrections', 'unverifiable', 'missed_material', 'high_value_facts', 'verdict'],
}

const id = args && args.id
const d = REGISTRY[id]
if (!d) throw new Error('unknown doc id ' + id)
const file = `${OUT}/${id}.md`

const prompt = `You are an adversarial checker for the evidence base of Wesgro's Unlocking Tourism final report. A colleague extracted evidence from ${d.name} into ${file}. Source: ${d.src} (${d.kind}); text layer at ${d.text}. ${d.kind === 'pdf' ? 'Render the whole source once if the folder ' + OUT + '/pages/' + id + '/ is empty: `mkdir -p ' + OUT + '/pages/' + id + ' && pdftoppm -r 60 -png "' + d.src + '" ' + OUT + '/pages/' + id + '/p`, then Read the PNG of each page you check (several per turn).' : 'Embedded images: `mkdir -p ' + OUT + '/media/' + id + ' && cd ' + OUT + '/media/' + id + ' && unzip -o -q "' + d.src + '" "word/media/*"`, then Read those that carry figures.'}

Your job is to find errors, not to confirm. Read the extract in full. For every figure, count, date, quotation and page reference in it: locate it in the source and check value, unit, year, base (fiscal or calendar, province or Cape Town, overseas or international), wording and page. Assume the extract is wrong until the source proves it right. Then read the source end to end once and list important findings or figures the extract omitted, especially anything the final report needs: growth case and seat ceiling, market groups, seasonality, route loads, readiness scores by district, the community shortlist and spend figures, comparator growth rates and institutional mechanisms, employment figures, stakeholder quotes with attribution, and any hypothesis tree.

Fix every error directly in ${file} with the Edit tool (never rewrite the file wholesale; never delete evidence). Add material omissions as new numbered findings or table rows in the right section. Append a section "## Verification" at the end listing what you changed and what you could not verify. Then return the structured result; count figures_checked honestly and list up to 12 high-value facts with pages.`

phase('Verify')
log(`Verifying ${id}`)
const v = await agent(prompt, { label: `verify:${id}`, phase: 'Verify', schema: VERIFY_SCHEMA })
return v ? { doc: id, file, verdict: v.verdict, figures_checked: v.figures_checked, corrections: v.corrections, unverifiable: v.unverifiable, missed: v.missed_material, high_value_facts: v.high_value_facts } : { doc: id, failed: 'verify returned null' }
