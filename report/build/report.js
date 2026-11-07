'use strict';
// Assembler for the Unlocking Tourism Growth final report.
// Usage: NODE_PATH=$(npm root -g) node report.js --out ../outputs/Report.docx --pass 1|2 [--pagemap pagemap.json]
const fs = require('fs');
const path = require('path');
const H = require('./helpers');

function arg(name, dflt) { const i = process.argv.indexOf(name); return i > -1 ? process.argv[i + 1] : dflt; }
const outPath = arg('--out', path.join(__dirname, '..', 'outputs', 'Unlocking_Tourism_Growth_Final_Report_DRAFT_v1.docx'));
const pass = parseInt(arg('--pass', '1'), 10);
const pagemapPath = arg('--pagemap', null);
const only = arg('--only', null); // comma-separated module names for partial renders (e.g. ch1_context,ch2_analysis)

const TITLE = 'Unlocking Tourism Growth: A Strategy for the Western Cape to 2035';
const SHORT = 'Unlocking Tourism Growth: A Strategy for the Western Cape to 2035';

// Content modules in document order. Each exports build(ctx, H) -> array of docx elements.
const MODULES = ['front_matter', 'exec_summary', 'ch1_context', 'ch2_analysis', 'ch3_findings', 'ch4_execution', 'ch5_me', 'appendices'];

function load(name) {
  const p = path.join(__dirname, `${name}.js`);
  if (!fs.existsSync(p)) return null;
  return require(p);
}

async function main() {
  const ctx = H.makeContext();
  ctx.pass = pass;
  ctx.pagemap = pagemapPath && fs.existsSync(pagemapPath) ? JSON.parse(fs.readFileSync(pagemapPath, 'utf8')).map : {};
  ctx.title = TITLE;
  const wanted = only ? only.split(',') : MODULES;

  // Two-stage build: content modules first so the registries are full, then front matter (which reads them).
  const built = {};
  for (const name of wanted) {
    if (name === 'front_matter') continue;
    const mod = load(name);
    if (!mod) { console.log(`skip ${name} (no module yet)`); continue; }
    built[name] = mod.build(ctx, H);
    console.log(`built ${name}: ${built[name].length} elements`);
  }
  const sections = [];
  if (wanted.includes('front_matter')) {
    const fm = load('front_matter');
    if (fm) sections.push({ children: fm.build(ctx, H), firstPageBlank: true });
  }
  // One section per chapter, so the divider (its first page) carries no header or footer; numbering runs on.
  for (const name of wanted) if (built[name]) sections.push({ children: built[name], firstPageBlank: true });
  // Back cover, after the Wesgro closing slide.
  const W = (t, o = {}) => new H.TextRun({ text: t, color: 'FFFFFF', font: H.FONT_HEAD, ...o });
  sections.push({ firstPageBlank: true, children: [H.fullBleed('bg_back.png'),
    new H.Paragraph({ spacing: { before: H.PT(330) * 10, after: 120 }, indent: { right: 5200 }, border: { bottom: { style: H.docx.BorderStyle.SINGLE, size: 12, color: '00A3DA', space: 10 } }, children: [W('Contact us', { size: H.PT(26), bold: true })] }),
    new H.Paragraph({ spacing: { after: 60 }, children: [W('hello@wesgro.co.za', { size: H.PT(12) })] }),
  ] });
  if (!sections.length) throw new Error('nothing to build');

  // Registry for the page scanner (pass 1) and the contents pages (pass 2).
  fs.writeFileSync(path.join(__dirname, 'headings.json'), JSON.stringify({
    skipPages: 6,
    items: [
      ...ctx.headings.filter((h) => h.level <= 2).map((h) => ({ kind: 'heading', title: h.title })),
      ...ctx.figures.map((f) => ({ kind: 'figure', title: `${f.num}. ${f.caption}` })),
      ...ctx.tables.map((t) => ({ kind: 'table', title: `${t.num}. ${t.caption}` })),
    ],
  }, null, 1));

  const doc = H.buildDocument({ sections, shortTitle: SHORT, title: TITLE, draft: true });
  await H.save(doc, outPath);
  console.log(`pass ${pass}: wrote ${outPath}`);
}
main().catch((e) => { console.error(e); process.exit(1); });
