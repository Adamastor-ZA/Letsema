'use strict';
// Front matter: cover, document control, foreword placeholder, contents, figures, tables, abbreviations.
// Contents page numbers come from ctx.pagemap on pass 2 (see report.js and scan_pages.js).

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

  // Cover
  out.push(new Paragraph({ style: 'CoverMeta', spacing: { before: 400 }, children: [new TextRun('Letsema in partnership with Skift Advisory, for Wesgro')] }));
  out.push(new Paragraph({ style: 'CoverTitle', children: [new TextRun('Unlocking Tourism Growth')] }));
  out.push(new Paragraph({ style: 'CoverSub', children: [new TextRun('A Strategy for the Western Cape to 2035')] }));
  out.push(new Paragraph({ style: 'CoverMeta', children: [new TextRun('Final Research Report')] }));
  out.push(new Paragraph({ style: 'CoverMeta', children: [new TextRun('Draft for discussion, version 1, November 2026')] }));
  out.push(new Paragraph({ style: 'CoverMeta', children: [new TextRun({ text: 'DRAFT FOR DISCUSSION. Not for circulation beyond the Wesgro project team.', bold: true })] }));
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
      ['Status', 'Draft for discussion, version 1. Every page carries the draft marking until the Steerco review'],
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
