'use strict';
// Front matter: cover, document control, foreword placeholder, contents, figures, tables, abbreviations.
// Contents page numbers come from ctx.pagemap on pass 2 (see report.js and scan_pages.js).

// The draft version on the cover and in document control follows the output name (..._DRAFT_v7.docx reads version 7).
const OUT_ARG = process.argv[process.argv.indexOf('--out') + 1] || '';
const VERSION = (OUT_ARG.match(/_v(\d+)\.docx$/) || [null, '7'])[1];

const ABBREVIATIONS = [
  ['ACSA', 'Airports Company South Africa'],
  ['CAGR', 'Compound annual growth rate'],
  ['CTAA', 'Cape Town Air Access'],
  ['CTIA', 'Cape Town International Airport'],
  ['CTICC', 'Cape Town International Convention Centre'],
  ['CTT', 'Cape Town Tourism'],
  ['DEDAT', 'Department of Economic Development and Tourism, Western Cape Government'],
  ['DMO', 'Destination marketing organisation'],
  ['FTE', 'Full-time equivalent'],
  ['FY', 'Financial year (April to March)'],
  ['G4J', 'Growth for Jobs Strategy, Western Cape Government, 2023'],
  ['GCC', 'Gulf Cooperation Council'],
  ['GDPR', 'Gross domestic product by region'],
  ['GVA', 'Gross value added'],
  ['ICCA', 'International Congress and Convention Association'],
  ['LTO', 'Local tourism organisation'],
  ['M&E', 'Monitoring and evaluation'],
  ['Mero', 'Municipal Economic Review and Outlook'],
  ['MICE', 'Meetings, incentives, conferences and exhibitions'],
  ['OAG', 'Official Airline Guide (schedules and capacity data)'],
  ['OSM', 'OpenStreetMap'],
  ['OTA', 'Online travel agency'],
  ['Pero', 'Provincial Economic Review and Outlook'],
  ['RACI', 'Responsible, accountable, consulted, informed'],
  ['SAT', 'South African Tourism'],
  ['SLA', 'Service level agreement'],
  ['SMME', 'Small, medium and micro enterprise'],
  ['Stats SA', 'Statistics South Africa'],
  ['TSA', 'Tourism Satellite Account'],
  ['UIA', 'Union of International Associations'],
  ['VFR', 'Visiting friends and relatives'],
  ['WTTC', 'World Travel and Tourism Council'],
];

function build(ctx, H) {
  const { Paragraph, TextRun, AlignmentType } = H;
  const out = [];

  // Cover, after the Wesgro cover slide: charcoal ground, logo top left, the protea W, the title over a short cyan rule.
  const W = (t, o = {}) => new TextRun({ text: t, color: 'FFFFFF', font: H.FONT_HEAD, ...o });
  out.push(H.fullBleed('bg_cover.png'));
  out.push(new Paragraph({ spacing: { before: H.PT(470) * 10, after: 100 }, children: [W('FINAL RESEARCH REPORT', { size: H.PT(9), bold: true, characterSpacing: 40 })] }));
  out.push(new Paragraph({ spacing: { after: 200 }, indent: { right: 2600 }, border: { bottom: { style: H.docx.BorderStyle.SINGLE, size: 12, color: '00A3DA', space: 10 } },
    children: [W('Unlocking Tourism Growth', { size: H.PT(32), bold: true })] }));
  out.push(new Paragraph({ spacing: { after: 600 }, children: [W('A Strategy for the Western Cape to 2035', { size: H.PT(17) })] }));
  out.push(new Paragraph({ spacing: { after: 60 }, children: [W('Letsema in partnership with Skift Advisory', { size: H.PT(9.5) })] }));
  out.push(new Paragraph({ spacing: { after: 60 }, children: [W(`Draft for discussion  |  Version ${VERSION}  |  November 2026`, { size: H.PT(9.5) })] }));
  out.push(new Paragraph({ spacing: { before: 120, after: 60 }, children: [W('DRAFT FOR DISCUSSION. Not for circulation beyond the Wesgro project team.', { size: H.PT(8.5), bold: true })] }));
  out.push(H.pageBreak());

  // Document control
  out.push(H.h1NoBreak('Document control'));
  out.push(H.grid(
    [{ header: 'Item', width: 1 }, { header: 'Detail', width: 3 }],
    [
      ['Title', 'Unlocking Tourism Growth: A Strategy for the Western Cape to 2035. Final Research Report'],
      ['Client', 'Wesgro, the Western Cape Tourism, Trade and Investment Promotion Agency'],
      ['Authors', 'Letsema Consulting and Advisory in partnership with Skift Advisory'],
      ['Contract', 'Service Level Agreement, Annexure B, clause 1.1.14 (Final Research Report); clauses 1.1.4 and 1.1.10 (M&E toolkit)'],
      ['Status', `Draft for discussion, version ${VERSION}. Every page carries the draft marking until the Steerco review`],
      ['Audience', 'Unlocking Tourism Steerco, Wesgro Exco and Board; the written report launches at the Unlocking Tourism business outlook, February 2027'],
      ['Conventions', 'Figures carry a source and page in the form (Demand-Side Analysis, Jun 2026, p21). Square-bracketed text marks an open item. See section 1.5'],
    ],
  ));
  out.push(H.pageBreak());

  // Foreword placeholder
  out.push(H.h1NoBreak('Foreword'));
  out.push(H.body('[Foreword by the Chief Executive Officer of Wesgro, one page. To be drafted by Wesgro or ghost-written by Letsema for sign-off, SLA Annexure B clause 1.1.14.5.]'));
  out.push(H.pageBreak());

  // Contents
  out.push(H.h1NoBreak('Contents'));
  const tocEntries = ctx.headings.filter((h) => h.level <= 2).map((h) => ({ level: h.level, title: h.title, page: H.pageOf(ctx, h.title) }));
  out.push(...H.contentsList(tocEntries));
  out.push(H.pageBreak());

  // Figures and tables
  out.push(H.h1NoBreak('Figures'));
  out.push(...H.contentsList(ctx.figures.map((f) => ({ level: 2, title: `${f.num}. ${f.caption}`, page: H.pageOf(ctx, `${f.num}. ${f.caption}`) }))));
  out.push(H.spacer(10));
  out.push(H.h1NoBreak('Tables'));
  out.push(...H.contentsList(ctx.tables.map((t) => ({ level: 2, title: `${t.num}. ${t.caption}`, page: H.pageOf(ctx, `${t.num}. ${t.caption}`) }))));
  out.push(H.pageBreak());

  // Abbreviations
  out.push(H.h1NoBreak('Abbreviations'));
  out.push(H.grid([{ header: 'Abbreviation', width: 1 }, { header: 'Meaning', width: 3 }], ABBREVIATIONS, { zebra: true }));
  return out;
}

module.exports = { build, ABBREVIATIONS };
