'use strict';
// Shared styles, numbering and element helpers for the Unlocking Tourism Growth final report.
// Run with NODE_PATH=$(npm root -g) so the globally installed docx package resolves.

const fs = require('fs');
const path = require('path');
const docx = require('docx');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, AlignmentType,
  Header, Footer, PageNumber, ImageRun, BorderStyle, ShadingType, HeadingLevel, LevelFormat,
  VerticalAlign, TableLayoutType, PageBreak, Bookmark, InternalHyperlink, TabStopType, LineRuleType,
} = docx;
// LibreOffice treats w:line without w:lineRule as a fixed height, which collapses inline images; always state the rule.
const AUTO = LineRuleType.AUTO;

// ---------- Typography and palette ----------
const FONT_TITLE = 'EB Garamond';   // brand: titles
const FONT_HEAD = 'Raleway';        // brand: descriptors, headings, kickers, tables
const FONT_BODY = 'EB Garamond';    // body prose
const PT = (n) => Math.round(n * 2); // points to half-points

// Neutral palette pending Wesgro brand colours (open item).
const C = {
  ink: '1C2431',
  navy: '0B3C5D',
  teal: '1F7A8C',
  grey: '5B6572',
  mid: 'C9D1DA',
  light: 'EEF2F6',
  head: 'DCE6EE',
  highlight: 'FFF3B0',
  white: 'FFFFFF',
};

// A4 with 2.2 cm margins; text width 16.6 cm.
const PAGE = { width: 11906, height: 16838, margin: 1247 }; // DXA
const TEXT_WIDTH_DXA = PAGE.width - 2 * PAGE.margin;        // 9412
const CM_TO_DXA = 567;
const TEXT_WIDTH_CM = TEXT_WIDTH_DXA / CM_TO_DXA;           // 16.6

// ---------- Inline markup ----------
// **bold**, *italic*, and [placeholder] rendered with a yellow highlight so open items stay visible.
function runs(text, base = {}) {
  if (Array.isArray(text)) return text.flatMap((t) => (typeof t === 'string' ? runs(t, base) : [t]));
  if (typeof text !== 'string') return [text];
  const out = [];
  const re = /(\*\*[^*]+\*\*|\*[^*]+\*|\[[^\]\n]+\])/g;
  let last = 0; let m;
  while ((m = re.exec(text)) !== null) {
    if (m.index > last) out.push(new TextRun({ ...base, text: text.slice(last, m.index) }));
    const tok = m[0];
    if (tok.startsWith('**')) out.push(new TextRun({ ...base, text: tok.slice(2, -2), bold: true }));
    else if (tok.startsWith('*')) out.push(new TextRun({ ...base, text: tok.slice(1, -1), italics: true }));
    else out.push(new TextRun({ ...base, text: tok, highlight: 'yellow' }));
    last = m.index + tok.length;
  }
  if (last < text.length) out.push(new TextRun({ ...base, text: text.slice(last) }));
  return out;
}

// ---------- Paragraph helpers ----------
const body = (text, opts = {}) => new Paragraph({ style: 'Body', children: runs(text), ...opts });
const lead = (text, opts = {}) => new Paragraph({ style: 'Lead', children: runs(text), ...opts });
const note = (text, opts = {}) => new Paragraph({ style: 'Note', children: runs(text), ...opts });
const kicker = (text, brk = false) => new Paragraph({ style: 'Kicker', pageBreakBefore: brk, children: [new TextRun({ text: text.toUpperCase() })] });
const h1 = (text, id) => new Paragraph({ heading: HeadingLevel.HEADING_1, pageBreakBefore: true, children: id ? [new Bookmark({ id, children: [new TextRun(text)] })] : [new TextRun(text)] });
const h1NoBreak = (text, id) => new Paragraph({ heading: HeadingLevel.HEADING_1, children: id ? [new Bookmark({ id, children: [new TextRun(text)] })] : [new TextRun(text)] });
const h2 = (text, id, brk = false) => new Paragraph({ heading: HeadingLevel.HEADING_2, pageBreakBefore: brk, children: id ? [new Bookmark({ id, children: [new TextRun(text)] })] : [new TextRun(text)] });
const h3 = (text, id, brk = false) => new Paragraph({ heading: HeadingLevel.HEADING_3, pageBreakBefore: brk, children: id ? [new Bookmark({ id, children: [new TextRun(text)] })] : [new TextRun(text)] });
const h4 = (text) => new Paragraph({ heading: HeadingLevel.HEADING_4, children: [new TextRun(text)] });
const pageBreak = () => new Paragraph({ children: [new PageBreak()] });
const spacer = (pt = 6) => { const p = new Paragraph({ spacing: { before: 0, after: PT(pt) * 10 }, children: [new TextRun('')] }); p._spacer = true; return p; };

// Numbered and bulleted lists. Each call to numbered() restarts at 1 through a fresh instance.
let listInstance = 0;
function numbered(items, reference = 'n_policy') {
  listInstance += 1;
  const inst = listInstance;
  return items.map((t) => new Paragraph({ style: 'ListText', numbering: { reference, level: 0, instance: inst }, children: runs(t) }));
}
function bullets(items) {
  return items.map((t) => new Paragraph({ style: 'ListText', numbering: { reference: 'bullets', level: 0 }, children: runs(t) }));
}

// Citation in the house form: (Demand-Side Analysis, Jun 2026, p21)
const cite = (doc, date, page) => `(${doc}, ${date}${page ? ', ' + page : ''})`;

// ---------- Counters and registries for figures and tables ----------
function makeContext() {
  return { chapter: '0', fig: 0, tab: 0, figures: [], tables: [], headings: [], pass: 1, pagemap: {} };
}
function setChapter(ctx, label) { ctx.chapter = String(label); ctx.fig = 0; ctx.tab = 0; }

// Heading helpers bound to a context so the contents pages can be built from the registry.
function headings(ctx) {
  const reg = (level, title) => { ctx.headings.push({ level, title }); return title; };
  return {
    h1: (t, id) => h1(reg(1, t), id),
    h1NoBreak: (t, id) => h1NoBreak(reg(1, t), id),
    h2: (t, id, brk) => h2(reg(2, t), id, brk),
    h3: (t, id, brk) => h3(reg(3, t), id, brk),
    h4,
  };
}
const pageOf = (ctx, title) => (ctx.pagemap && ctx.pagemap[title] != null ? ctx.pagemap[title] : null);

// ---------- Tables ----------
const thinBorder = { style: BorderStyle.SINGLE, size: 4, color: C.mid };
const noBorder = { style: BorderStyle.NONE, size: 0, color: C.white };
const cellMargins = { top: 60, bottom: 60, left: 90, right: 90 };

function cellText(content, { head = false, align = AlignmentType.LEFT, bold = false } = {}) {
  const style = head ? 'TableHead' : 'TableText';
  if (Array.isArray(content) && content.length && content[0] instanceof Paragraph) return content;
  const lines = String(content == null ? '' : content).split('\n');
  return lines.map((line) => new Paragraph({ style, alignment: align, children: runs(line, bold ? { bold: true } : {}) }));
}

// columns: [{ header, width (fraction of text width or cm), align }]
// rows: array of arrays of strings (or Paragraph arrays)
function table(ctx, { caption, source, columns, rows, fontSize, headShade = C.head, zebra = true, boldFirstCol = false, keepTogether = false }) {
  const widths = normaliseWidths(columns.map((c) => c.width));
  const colDxa = widths.map((w) => Math.round(w * TEXT_WIDTH_DXA));
  ctx.tab += 1;
  const num = `Table ${ctx.chapter}.${ctx.tab}`;
  ctx.tables.push({ num, caption });
  const headerRow = new TableRow({
    tableHeader: true, cantSplit: true,
    children: columns.map((c, i) => new TableCell({
      width: { size: colDxa[i], type: WidthType.DXA }, margins: cellMargins,
      shading: { type: ShadingType.CLEAR, fill: headShade, color: 'auto' }, verticalAlign: VerticalAlign.BOTTOM,
      children: cellText(c.header, { head: true, align: c.align || AlignmentType.LEFT }),
    })),
  });
  const bodyRows = rows.map((r, ri) => new TableRow({
    cantSplit: true,
    children: r.map((cell, i) => new TableCell({
      width: { size: colDxa[i], type: WidthType.DXA }, margins: cellMargins,
      shading: zebra && ri % 2 === 1 ? { type: ShadingType.CLEAR, fill: C.light, color: 'auto' } : undefined,
      children: cellText(cell, { align: columns[i].align || AlignmentType.LEFT, bold: boldFirstCol && i === 0 }),
    })),
  }));
  const t = new Table({
    width: { size: TEXT_WIDTH_DXA, type: WidthType.DXA }, columnWidths: colDxa, layout: TableLayoutType.FIXED,
    borders: { top: thinBorder, bottom: thinBorder, left: noBorder, right: noBorder, insideHorizontal: thinBorder, insideVertical: noBorder },
    rows: [headerRow, ...bodyRows],
  });
  const out = [new Paragraph({ style: 'Caption', keepNext: true, children: [new TextRun({ text: `${num}. `, bold: true }), ...runs(caption)] }), t];
  if (source) out.push(new Paragraph({ style: 'Source', children: runs(`Source: ${source}`) }));
  else out.push(spacer(4));
  return out;
}

function normaliseWidths(ws) {
  const vals = ws.map((w) => (w == null ? 1 : w));
  const sum = vals.reduce((a, b) => a + b, 0);
  return vals.map((w) => w / sum);
}

// A plain (unnumbered, uncaptioned) grid, for front-matter lists and charters.
function grid(columns, rows, { headShade = C.head, zebra = false } = {}) {
  const widths = normaliseWidths(columns.map((c) => c.width));
  const colDxa = widths.map((w) => Math.round(w * TEXT_WIDTH_DXA));
  const headerRow = new TableRow({ tableHeader: true, cantSplit: true, children: columns.map((c, i) => new TableCell({ width: { size: colDxa[i], type: WidthType.DXA }, margins: cellMargins, shading: { type: ShadingType.CLEAR, fill: headShade, color: 'auto' }, children: cellText(c.header, { head: true, align: c.align }) })) });
  const bodyRows = rows.map((r, ri) => new TableRow({ cantSplit: true, children: r.map((cell, i) => new TableCell({ width: { size: colDxa[i], type: WidthType.DXA }, margins: cellMargins, shading: zebra && ri % 2 === 1 ? { type: ShadingType.CLEAR, fill: C.light, color: 'auto' } : undefined, children: cellText(cell, { align: columns[i].align }) })) }));
  return new Table({ width: { size: TEXT_WIDTH_DXA, type: WidthType.DXA }, columnWidths: colDxa, layout: TableLayoutType.FIXED, borders: { top: thinBorder, bottom: thinBorder, left: noBorder, right: noBorder, insideHorizontal: thinBorder, insideVertical: noBorder }, rows: [headerRow, ...bodyRows] });
}

// Shaded call-out box (for example "What this means for the tree").
function box(title, paragraphs, { fill = C.light } = {}) {
  const children = [];
  if (title) children.push(new Paragraph({ style: 'BoxTitle', children: [new TextRun(title)] }));
  for (const p of paragraphs) children.push(typeof p === 'string' ? new Paragraph({ style: 'BoxBody', children: runs(p) }) : p);
  const t = new Table({
    width: { size: TEXT_WIDTH_DXA, type: WidthType.DXA }, columnWidths: [TEXT_WIDTH_DXA], layout: TableLayoutType.FIXED,
    borders: { top: { style: BorderStyle.SINGLE, size: 12, color: C.teal }, bottom: noBorder, left: noBorder, right: noBorder, insideHorizontal: noBorder, insideVertical: noBorder },
    rows: [new TableRow({ cantSplit: true, children: [new TableCell({ width: { size: TEXT_WIDTH_DXA, type: WidthType.DXA }, margins: { top: 140, bottom: 140, left: 200, right: 200 }, shading: { type: ShadingType.CLEAR, fill, color: 'auto' }, children })] })],
  });
  return [t, spacer(6)];
}

// ---------- Figures ----------
function pngSize(buf) {
  if (buf.length < 24 || buf.toString('ascii', 1, 4) !== 'PNG') return null;
  return { w: buf.readUInt32BE(16), h: buf.readUInt32BE(20) };
}
function figure(ctx, { file, caption, source, widthCm = TEXT_WIDTH_CM }) {
  ctx.fig += 1;
  const num = `Figure ${ctx.chapter}.${ctx.fig}`;
  ctx.figures.push({ num, caption });
  const out = [];
  if (file && fs.existsSync(file)) {
    const data = fs.readFileSync(file);
    const sz = pngSize(data) || { w: 1600, h: 900 };
    const wPx = Math.round((widthCm / 2.54) * 96);
    const hPx = Math.round(wPx * (sz.h / sz.w));
    out.push(new Paragraph({ keepNext: true, alignment: AlignmentType.CENTER, spacing: { before: 120, after: 60, line: 240, lineRule: AUTO }, children: [new ImageRun({ type: 'png', data, transformation: { width: wPx, height: hPx } })] }));
  } else {
    out.push(new Paragraph({ keepNext: true, alignment: AlignmentType.CENTER, spacing: { before: 120, after: 60, line: 240, lineRule: AUTO }, children: [new TextRun({ text: `[Figure to be rendered: ${file ? path.basename(file) : 'no file'}]`, highlight: 'yellow', font: FONT_HEAD, size: PT(9) })] }));
  }
  out.push(new Paragraph({ style: 'Caption', children: [new TextRun({ text: `${num}. `, bold: true }), ...runs(caption)] }));
  if (source) out.push(new Paragraph({ style: 'Source', children: runs(`Source: ${source}`) }));
  return out;
}

// ---------- Front-matter contents built from a scanned page map (two-pass build) ----------
function contentsList(entries) {
  // entries: [{ level: 1|2, title, page }]
  return entries.map((e) => new Paragraph({
    style: e.level === 1 ? 'TocL1' : 'TocL2',
    tabStops: [{ type: TabStopType.RIGHT, position: TEXT_WIDTH_DXA, leader: 'dot' }],
    children: [new TextRun(e.title), new TextRun({ text: `\t${e.page == null ? '' : e.page}` })],
  }));
}

// ---------- Document assembly ----------
function styles() {
  const base = { font: FONT_BODY, size: PT(11), color: C.ink };
  return {
    default: { document: { run: base, paragraph: { spacing: { line: 276, lineRule: AUTO, after: 120 } } } },
    paragraphStyles: [
      { id: 'Body', name: 'Body', basedOn: 'Normal', next: 'Body', quickFormat: true, run: base, paragraph: { spacing: { line: 276, lineRule: AUTO, after: 140 }, alignment: AlignmentType.LEFT } },
      { id: 'Lead', name: 'Lead', basedOn: 'Body', next: 'Body', run: { ...base, size: PT(12), color: C.navy }, paragraph: { spacing: { line: 276, lineRule: AUTO, after: 160 } } },
      { id: 'Note', name: 'Note', basedOn: 'Body', next: 'Body', run: { ...base, size: PT(9.5), color: C.grey }, paragraph: { spacing: { after: 100 } } },
      { id: 'Kicker', name: 'Kicker', basedOn: 'Normal', next: 'Body', run: { font: FONT_HEAD, size: PT(8.5), bold: true, color: C.teal, characterSpacing: 30 }, paragraph: { spacing: { before: 240, after: 40 }, keepNext: true } },
      { id: 'ListText', name: 'List Text', basedOn: 'Body', next: 'ListText', run: base, paragraph: { spacing: { after: 80 } } },
      { id: 'Caption', name: 'Caption', basedOn: 'Normal', next: 'Body', run: { font: FONT_HEAD, size: PT(9), color: C.ink }, paragraph: { spacing: { before: 160, after: 80 }, keepNext: true } },
      { id: 'Source', name: 'Source', basedOn: 'Normal', next: 'Body', run: { font: FONT_HEAD, size: PT(7.5), color: C.grey }, paragraph: { spacing: { before: 60, after: 200 } } },
      { id: 'TableText', name: 'Table Text', basedOn: 'Normal', next: 'TableText', run: { font: FONT_HEAD, size: PT(8.5), color: C.ink }, paragraph: { spacing: { before: 0, after: 0, line: 240, lineRule: AUTO } } },
      { id: 'TableHead', name: 'Table Head', basedOn: 'TableText', next: 'TableText', run: { font: FONT_HEAD, size: PT(8.5), bold: true, color: C.navy }, paragraph: { spacing: { before: 0, after: 0, line: 240, lineRule: AUTO } } },
      { id: 'BoxTitle', name: 'Box Title', basedOn: 'Normal', next: 'BoxBody', run: { font: FONT_HEAD, size: PT(10), bold: true, color: C.navy }, paragraph: { spacing: { after: 80 } } },
      { id: 'BoxBody', name: 'Box Body', basedOn: 'Normal', next: 'BoxBody', run: { ...base, size: PT(10) }, paragraph: { spacing: { after: 80, line: 264, lineRule: AUTO } } },
      { id: 'Quote', name: 'Quote', basedOn: 'Body', next: 'Body', run: { ...base, italics: true, color: C.grey }, paragraph: { indent: { left: 567, right: 567 }, spacing: { after: 140 } } },
      { id: 'TocL1', name: 'TOC L1', basedOn: 'Normal', next: 'TocL1', run: { font: FONT_HEAD, size: PT(10), bold: true, color: C.ink }, paragraph: { spacing: { before: 100, after: 40 } } },
      { id: 'TocL2', name: 'TOC L2', basedOn: 'Normal', next: 'TocL2', run: { font: FONT_BODY, size: PT(10.5), color: C.ink }, paragraph: { indent: { left: 400 }, spacing: { after: 30 } } },
      { id: 'CoverTitle', name: 'Cover Title', basedOn: 'Normal', run: { font: FONT_TITLE, size: PT(34), bold: true, color: C.navy }, paragraph: { spacing: { before: 2400, after: 200 } } },
      { id: 'CoverSub', name: 'Cover Sub', basedOn: 'Normal', run: { font: FONT_HEAD, size: PT(14), bold: true, color: C.teal }, paragraph: { spacing: { after: 600 } } },
      { id: 'CoverMeta', name: 'Cover Meta', basedOn: 'Normal', run: { font: FONT_HEAD, size: PT(10.5), color: C.grey }, paragraph: { spacing: { after: 80 } } },
      { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Body', quickFormat: true, run: { font: FONT_TITLE, size: PT(24), bold: true, color: C.navy }, paragraph: { spacing: { before: 0, after: 360 }, keepNext: true, outlineLevel: 0 } },
      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Body', quickFormat: true, run: { font: FONT_HEAD, size: PT(14), bold: true, color: C.navy }, paragraph: { spacing: { before: 360, after: 160 }, keepNext: true, outlineLevel: 1 } },
      { id: 'Heading3', name: 'Heading 3', basedOn: 'Normal', next: 'Body', quickFormat: true, run: { font: FONT_HEAD, size: PT(11.5), bold: true, color: C.teal }, paragraph: { spacing: { before: 280, after: 120 }, keepNext: true, outlineLevel: 2 } },
      { id: 'Heading4', name: 'Heading 4', basedOn: 'Normal', next: 'Body', quickFormat: true, run: { font: FONT_HEAD, size: PT(10), bold: true, color: C.ink }, paragraph: { spacing: { before: 200, after: 80 }, keepNext: true, outlineLevel: 3 } },
    ],
  };
}

function numberingConfig() {
  const decimal = (ref) => ({ reference: ref, levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.START, style: { paragraph: { indent: { left: 567, hanging: 360 } } } }] });
  return {
    config: [
      decimal('n_policy'),
      decimal('n_90'),
      decimal('n_steps'),
      { reference: 'bullets', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.START, style: { paragraph: { indent: { left: 567, hanging: 300 } } } }] },
    ],
  };
}

function headerFooter(shortTitle, draft) {
  const header = new Header({ children: [new Paragraph({
    tabStops: [{ type: TabStopType.RIGHT, position: TEXT_WIDTH_DXA }],
    children: [new TextRun({ text: shortTitle, font: FONT_HEAD, size: PT(7.5), color: C.grey }), new TextRun({ text: `\t${draft ? 'DRAFT FOR DISCUSSION' : ''}`, font: FONT_HEAD, size: PT(7.5), bold: true, color: C.teal })],
  })] });
  const footer = new Footer({ children: [new Paragraph({
    tabStops: [{ type: TabStopType.RIGHT, position: TEXT_WIDTH_DXA }],
    children: [new TextRun({ text: 'Letsema in partnership with Skift Advisory, for Wesgro', font: FONT_HEAD, size: PT(7.5), color: C.grey }), new TextRun({ children: ['\t', PageNumber.CURRENT], font: FONT_HEAD, size: PT(8), color: C.ink })],
  })] });
  return { header, footer };
}

// sections: [{ children, landscape?, firstPageBlank? }]
function buildDocument({ sections, shortTitle, draft = true, title, creator = 'Letsema in partnership with Skift Advisory' }) {
  const { header, footer } = headerFooter(shortTitle, draft);
  return new Document({
    creator, title, description: 'Final research report',
    styles: styles(), numbering: numberingConfig(),
    features: { updateFields: false },
    sections: sections.map((s, i) => ({
      properties: {
        page: { size: { width: PAGE.width, height: PAGE.height }, margin: { top: PAGE.margin, bottom: PAGE.margin, left: PAGE.margin, right: PAGE.margin, header: 600, footer: 600 } },
        titlePage: !!s.firstPageBlank,
        pageNumberStart: s.pageNumberStart,
      },
      headers: s.firstPageBlank ? { default: header, first: new Header({ children: [new Paragraph('')] }) } : { default: header },
      footers: s.firstPageBlank ? { default: footer, first: new Footer({ children: [new Paragraph('')] }) } : { default: footer },
      children: s.children,
    })),
  });
}

async function save(doc, outPath) {
  const buf = await Packer.toBuffer(doc);
  fs.mkdirSync(path.dirname(outPath), { recursive: true });
  fs.writeFileSync(outPath, buf);
  return outPath;
}

module.exports = {
  docx, C, PT, FONT_TITLE, FONT_HEAD, FONT_BODY, TEXT_WIDTH_CM, TEXT_WIDTH_DXA,
  runs, body, lead, note, kicker, h1, h1NoBreak, h2, h3, h4, pageBreak, spacer, numbered, bullets, cite,
  makeContext, setChapter, headings, pageOf, table, grid, box, figure, contentsList, buildDocument, save,
  Paragraph, TextRun, AlignmentType,
};
