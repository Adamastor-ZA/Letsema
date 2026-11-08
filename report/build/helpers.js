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
  FootnoteReferenceRun, HorizontalPositionRelativeFrom, VerticalPositionRelativeFrom, TextWrappingType,
} = docx;
// LibreOffice treats w:line without w:lineRule as a fixed height, which collapses inline images; always state the rule.
const AUTO = LineRuleType.AUTO;

// ---------- Typography and palette ----------
// Wesgro CI: Helvetica, set here as Arial, its metric twin and the face the Wesgro template uses for body runs.
const FONT_TITLE = 'Arial';
const FONT_HEAD = 'Arial';
const FONT_BODY = 'Arial';
const PT = (n) => Math.round(n * 2); // points to half-points

// Wesgro CI (cover and interleading slides, 13 Oct 2026): charcoal #4D4D4F ground, cyan #00A3DA rule, white type.
// navy and teal keep their names so every style that used them now takes charcoal and cyan.
const C = {
  ink: '2B2B2D',
  navy: '4D4D4F',
  teal: '00A3DA',
  grey: '6D6E71',
  mid: 'C8C9CB',
  light: 'F5F6F7',
  head: '4D4D4F',
  dcyan: '006E93', // darker Wesgro cyan: safe for text on white (5.8:1)
  lcyan: '80D1EC', // lighter Wesgro cyan: fills and chart series
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

// ---------- Citations as footnotes ----------
// Body text keeps its citations in the house form, (Demand-Side Analysis, Jun 2026, p21), in the content modules.
// At render time each citation becomes a numbered footnote: the parenthesis leaves the text, the reference mark
// follows any punctuation that closed the citation, and short forms such as (p22) or ("Seasonality") are written out
// in full from the last source cited in the same section. Cross-references and data notes, such as (section 4.3),
// (I6) or (computed), stay inline. Captions, source lines and table cells are not touched.
const FOOTNOTES = {};
const FOOTNOTE_TEXT = []; // plain text of each footnote, for QA
let footnoteId = 0;
const citeState = { last: null, lastSect: null };
const resetCites = () => { citeState.last = null; citeState.lastSect = null; };
const MON = '(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*';
const RE_FULL = new RegExp(`^[A-Z][^;]*?,\\s(?:\\d{1,2}\\s)?${MON}\\s\\d{4}\\b`);
const RE_DOC = new RegExp(`^(.*?,\\s(?:\\d{1,2}\\s)?${MON}\\s\\d{4})`);
const RE_NAMED = /^(?:Wesgro Research, Western Cape Tourism Performance|City of Cape Town|Stats SA|Sernatur|UN Tourism|World Tourism Barometer|ACSA|Minister of Transport|George Herald|Western Cape Government|Singapore Tourism Board|Hypertext|Travel News)\b.*\b(?:19|20)\d{2}\b|^SLA Annexure B\b/;
const PG = 'pp?\\d+(?:\\s(?:to|and)\\spp?\\d+)?';
const RE_PAGE = new RegExp(`^(?:computed from\\s)?${PG}(?:,\\s(?:${PG}|computed|counted))*$`);
const RE_SECT = /^"[^"]+"(?:,\s"[^"]+")*$/;
const RE_MOD = /^(?:(?:sum\s)?computed|public sources?|counted)$/;
const RE_STUDY = /^(?:Inception Report|Current State Diagnostic|Stakeholder Insights Report|Global Benchmarking Report|MIDAS Aviation Market Assessment|Market Assessment Report|Demand-Side Analysis|Infrastructure Report|SME and Community Inclusion Plan|Summary of Findings|Skift)\b/;

function citeKind(part, prevFull) {
  if (RE_FULL.test(part) || RE_NAMED.test(part)) return 'full';
  if (RE_PAGE.test(part)) return 'page';
  if (RE_SECT.test(part)) return 'sect';
  if (RE_MOD.test(part)) return 'mod';
  if (prevFull && /^[A-Z][A-Za-z ]{2,40}$/.test(part) && part.split(' ').length <= 4) return 'sect';
  return 'other';
}

// Parse the inside of one parenthesis. Returns null if it is not a citation, else { note, inline }.
function parseCitation(inner) {
  const parts = inner.split(';').map((x) => x.trim());
  const kinds = []; let prevFull = false;
  for (const p of parts) { const k = citeKind(p, prevFull); kinds.push(k); prevFull = k === 'full'; }
  if (!kinds.some((k) => k === 'full' || k === 'page' || k === 'sect')) return null;
  let { last, lastSect } = citeState;
  const fn = [], inl = [];
  for (let i = 0; i < parts.length; i++) {
    const p = parts[i], k = kinds[i];
    if (k === 'full') {
      fn.push(p);
      const m = p.match(RE_DOC);
      // Short forms (p22) and ("Seasonality") only ever refer to the study documents, so public sources do not reset them.
      if (m && RE_STUDY.test(m[1])) { last = m[1]; if (!/^,\s+pp?\d/.test(p.slice(m[1].length))) lastSect = m[1]; }
    } else if (k === 'page') {
      if (!last) return null;
      const m = p.match(/^computed from\s(.*)$/);
      // a second location in the source the same citation has just named is written without repeating the source
      if (!m && fn.length && fn[fn.length - 1].startsWith(`${last},`)) fn.push(p);
      else fn.push(m ? `computed from ${last}, ${m[1]}` : `${last}, ${p}`);
    } else if (k === 'sect') {
      const src = lastSect || last;
      if (!src) return null;
      fn.push(fn.length && fn[fn.length - 1].startsWith(`${src},`) ? p : `${src}, ${p}`);
    } else if (k === 'mod') {
      if (fn.length) fn[fn.length - 1] += `, ${p}`; else fn.push(p);
    } else if (fn.length && /^[a-z]/.test(p) && p.split(' ').length >= 4) {
      fn[fn.length - 1] += `; ${p}`; // a note on the source, such as what a count covers
    } else inl.push(p);
  }
  citeState.last = last; citeState.lastSect = lastSect;
  const note = fn.join('; ');
  return { note: note.charAt(0).toUpperCase() + note.slice(1) + (/[.!?]$/.test(note) ? '' : '.'), inline: inl.length ? inl.join('; ') : null };
}

// Footnote trimming options, chosen with FN_MODE (comma-separated): 'nodate' drops the dates of the study documents, which A9
// lists once; 'short' also shortens their titles; 'para' gives each paragraph one footnote, folding repeats of a source;
// 'tight' closes up the footnote lines; 'es0' leaves the executive summary without footnotes.
// Draft v11 adopted para, short, tight and es0; set FN_MODE to another list (or to an empty string for one note per citation).
const FN_MODE = new Set((process.env.FN_MODE ?? 'para,short,tight,es0').split(',').filter(Boolean));
const SHORT_TITLES = [['Inception Report', 'Inception Report'], ['Current State Diagnostic', 'Diagnostic'], ['Stakeholder Insights Report', 'Stakeholder Insights'],
  ['Global Benchmarking Report', 'Benchmarking'], ['MIDAS Aviation Market Assessment', 'MIDAS'], ['Market Assessment Report', 'Market Assessment'],
  ['Demand-Side Analysis', 'Demand-Side Analysis'], ['Infrastructure Report', 'Infrastructure Report'], ['SME and Community Inclusion Plan', 'Inclusion Plan'],
  ['Skift Segmentation Analysis', 'Segmentation'], ['Skift Digital and Search Insights', 'Digital Insights'], ['Skift African Market Analysis', 'African Markets']];
const STUDY_NAMES = SHORT_TITLES.map(([f]) => f).concat(['Summary of Findings']);
const DATE_AFTER = new RegExp(`(${STUDY_NAMES.map((n) => n.replace(/[-]/g, '\\-')).join('|')}), (?:\\d{1,2} )?(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \\d{4}`, 'g');
function trimNote(text) {
  let t = text;
  if (FN_MODE.has('nodate') || FN_MODE.has('short')) t = t.replace(DATE_AFTER, '$1');
  if (FN_MODE.has('short')) for (const [f, sh] of SHORT_TITLES) t = t.split(f).join(sh);
  return t;
}
// Fold a list of footnote notes into one: parts naming the same source as an earlier part keep only their locators.
function foldNotes(notes) {
  const parts = notes.flatMap((n) => n.replace(/\.$/, '').split('; '));
  const out = []; const bySrc = new Map();
  for (const p of parts) {
    const m = p.match(/^(.*?)(, (?:pp?\d|"|computed|p\d).*)$/);
    if (m && bySrc.has(m[1])) {
      // add only the locators this source does not already carry (each page or section once)
      const k = bySrc.get(m[1]); const have = new Set(out[k].slice(m[1].length + 2).split(', '));
      for (const loc of m[2].slice(2).split(', ')) if (!have.has(loc)) { out[k] += `, ${loc}`; have.add(loc); }
      continue;
    }
    if (m) bySrc.set(m[1], out.length);
    if (!out.includes(p)) out.push(p);
  }
  const t = out.join('; ');
  return t.charAt(0).toUpperCase() + t.slice(1) + '.';
}
const citeMode = { module: '' };
function addFootnote(text) {
  text = trimNote(text);
  footnoteId += 1;
  FOOTNOTES[footnoteId] = { children: [new Paragraph({ style: 'FootnoteText', children: runs(` ${text}`) })] };
  FOOTNOTE_TEXT.push(text);
  return footnoteId;
}

// Split text into strings and footnote ids. Parentheses inside [open items] are left alone.
function citeSplit(text, collect = false) {
  const skip = [];
  for (const m of text.matchAll(/\[[^\]\n]+\]/g)) skip.push([m.index, m.index + m[0].length]);
  const inSkip = (i) => skip.some(([a, b]) => i >= a && i < b);
  const out = []; let pos = 0, depth = 0, start = -1;
  for (let i = 0; i < text.length; i++) {
    const ch = text[i];
    if (ch === '(' && !inSkip(i)) { if (depth === 0) start = i; depth += 1; }
    else if (ch === ')' && depth > 0 && !inSkip(i)) {
      depth -= 1;
      if (depth === 0) {
        const c = parseCitation(text.slice(start + 1, i));
        if (!c) continue;
        let before = text.slice(pos, start);
        before = c.inline ? `${before}(${c.inline})` : before.replace(/\s+$/, '');
        let next = i + 1;
        if ('.,;:'.includes(text[next] || '')) { before += text[next]; next += 1; }
        out.push(before, collect ? { note: c.note } : { fn: addFootnote(c.note) });
        pos = next; i = next - 1;
      }
    }
  }
  out.push(text.slice(pos));
  return out.filter((x) => x !== '');
}

// Citation in the house form, for code that builds text: (Demand-Side Analysis, Jun 2026, p21)
const cite = (doc, date, page) => `(${doc}, ${date}${page ? ', ' + page : ''})`;

// runs() with citations moved to footnotes.
function noteRuns(text, base = {}) {
  if (typeof text !== 'string') return runs(text, base);
  const es0 = FN_MODE.has('es0') && citeMode.module.startsWith('exec/');
  if (FN_MODE.has('para') || es0) {
    const segs = citeSplit(text, true);
    const notes = segs.filter((x) => typeof x !== 'string').map((x) => x.note);
    const textRuns = segs.filter((x) => typeof x === 'string').flatMap((x) => runs(x, base));
    if (!notes.length || es0) return textRuns;
    return [...textRuns, new FootnoteReferenceRun(addFootnote(foldNotes(notes)))];
  }
  return citeSplit(text).flatMap((seg) => (typeof seg === 'string' ? runs(seg, base) : [new FootnoteReferenceRun(seg.fn)]));
}

// ---------- Paragraph helpers ----------
const body = (text, opts = {}) => new Paragraph({ style: 'Body', children: noteRuns(text), ...opts });
const lead = (text, opts = {}) => new Paragraph({ style: 'Lead', children: noteRuns(text), ...opts });
const note = (text, opts = {}) => new Paragraph({ style: 'Note', children: noteRuns(text), ...opts });
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
// cont = true carries the numbering on from the previous list (a list split by an intervening paragraph).
function numbered(items, reference = 'n_policy', cont = false) {
  if (!cont) listInstance += 1;
  const inst = listInstance;
  return items.map((t) => new Paragraph({ style: 'ListText', numbering: { reference, level: 0, instance: inst }, children: noteRuns(t) }));
}
function bullets(items) {
  return items.map((t) => new Paragraph({ style: 'ListText', numbering: { reference: 'bullets', level: 0 }, children: noteRuns(t) }));
}


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

function cellText(content, { head = false, align = AlignmentType.LEFT, bold = false, keepNext = false } = {}) {
  const style = head ? 'TableHead' : 'TableText';
  if (Array.isArray(content) && content.length && content[0] instanceof Paragraph) return content;
  const lines = String(content == null ? '' : content).split('\n');
  return lines.map((line) => new Paragraph({ style, alignment: align, keepNext, children: runs(line, bold ? { bold: true } : {}) }));
}

// columns: [{ header, width (fraction of text width or cm), align }]
// rows: array of arrays of strings (or Paragraph arrays)
function table(ctx, { caption, source, columns, rows, fontSize, headShade = C.head, zebra = true, boldFirstCol = false, keepTogether = false, message = null }) {
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
      // keepNext holds the header row with the first body row: a header left alone at a page foot made LibreOffice drop
      // the rows that follow it (Table 5.2 in draft v1).
      children: cellText(c.header, { head: true, align: c.align || AlignmentType.LEFT, keepNext: true }),
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
  const out = [new Paragraph({ style: 'Caption', keepNext: true, children: [new TextRun({ text: `${num}. `, bold: true, color: C.dcyan }), ...runs(caption)] })];
  // Key message, set like the chart callouts: grey fill, cyan rule on the left, bold charcoal.
  if (message) out.push(new Paragraph({ style: 'TableMessage', keepNext: true, children: runs(message) }));
  out.push(t);
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
  for (const p of paragraphs) children.push(typeof p === 'string' ? new Paragraph({ style: 'BoxBody', children: noteRuns(p) }) : p);
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
  out.push(new Paragraph({ style: 'Caption', children: [new TextRun({ text: `${num}. `, bold: true, color: C.dcyan }), ...runs(caption)] }));
  if (source) out.push(new Paragraph({ style: 'Source', children: runs(`Source: ${source}`) }));
  return out;
}

// ---------- Wesgro CI pages: full-bleed backgrounds, chapter dividers ----------
const CI = path.join(__dirname, 'assets', 'ci');
// A paragraph carrying one page-sized image behind the text, anchored to the page corner.
function fullBleed(file) {
  const data = fs.readFileSync(path.join(CI, file));
  return new Paragraph({ spacing: { before: 0, after: 0, line: 240, lineRule: AUTO }, children: [new ImageRun({
    type: 'png', data, transformation: { width: 794, height: 1123 },
    floating: { horizontalPosition: { relative: HorizontalPositionRelativeFrom.PAGE, offset: 0 }, verticalPosition: { relative: VerticalPositionRelativeFrom.PAGE, offset: 0 },
      behindDocument: true, allowOverlap: true, lockAnchor: true, wrap: { type: TextWrappingType.NONE } },
  })] });
}
// Chapter divider, after the Wesgro interleading slide: charcoal, the Western Cape contour band, a white title over a
// short cyan rule. The title is a real Heading 1, so the contents and bookmarks still work.
function divider(hd, { label, title, bookmark }) {
  const white = (t, o = {}) => new TextRun({ text: t, color: C.white, font: FONT_HEAD, ...o });
  const out = [fullBleed('bg_divider_alt.png')];
  out.push(new Paragraph({ spacing: { before: PT(150) * 10, after: 120 }, children: [white(label || ' ', { size: PT(14) })] }));
  const h = hd.h1NoBreak(title, bookmark);
  out.push(new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 0, after: 240 }, indent: { right: 2000 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: C.teal, space: 10 } },
    children: [bookmark ? new Bookmark({ id: bookmark, children: [white(title, { size: PT(36), bold: true })] }) : white(title, { size: PT(36), bold: true })] }));
  return { out, registered: h };
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
  const base = { font: FONT_BODY, size: PT(10), color: C.ink };
  return {
    default: { document: { run: base, paragraph: { spacing: { line: 276, lineRule: AUTO, after: 120 } } } },
    paragraphStyles: [
      { id: 'Body', name: 'Body', basedOn: 'Normal', next: 'Body', quickFormat: true, run: base, paragraph: { spacing: { line: 300, lineRule: AUTO, after: 140 }, alignment: AlignmentType.LEFT } },
      { id: 'Lead', name: 'Lead', basedOn: 'Body', next: 'Body', run: { ...base, size: PT(11.5), color: C.navy }, paragraph: { spacing: { line: 300, lineRule: AUTO, after: 160 } } },
      { id: 'Note', name: 'Note', basedOn: 'Body', next: 'Body', run: { ...base, size: PT(9.5), color: C.grey }, paragraph: { spacing: { after: 100 } } },
      { id: 'Kicker', name: 'Kicker', basedOn: 'Normal', next: 'Body', run: { font: FONT_HEAD, size: PT(8), bold: true, color: C.dcyan, characterSpacing: 30 }, paragraph: { spacing: { before: 240, after: 40 }, keepNext: true } },
      { id: 'ListText', name: 'List Text', basedOn: 'Body', next: 'ListText', run: base, paragraph: { spacing: { after: 80 } } },
      { id: 'Caption', name: 'Caption', basedOn: 'Normal', next: 'Body', run: { font: FONT_HEAD, size: PT(9), color: C.ink }, paragraph: { spacing: { before: 160, after: 80 }, keepNext: true } },
      { id: 'Source', name: 'Source', basedOn: 'Normal', next: 'Body', run: { font: FONT_HEAD, size: PT(7.5), color: C.grey }, paragraph: { spacing: { before: 60, after: 200 } } },
      { id: 'TableText', name: 'Table Text', basedOn: 'Normal', next: 'TableText', run: { font: FONT_HEAD, size: PT(8.5), color: C.ink }, paragraph: { spacing: { before: 0, after: 0, line: 240, lineRule: AUTO } } },
      { id: 'TableHead', name: 'Table Head', basedOn: 'TableText', next: 'TableText', run: { font: FONT_HEAD, size: PT(8.5), bold: true, color: C.white }, paragraph: { spacing: { before: 0, after: 0, line: 240, lineRule: AUTO } } },
      { id: 'BoxTitle', name: 'Box Title', basedOn: 'Normal', next: 'BoxBody', run: { font: FONT_HEAD, size: PT(10), bold: true, color: C.navy }, paragraph: { spacing: { after: 80 } } },
      { id: 'BoxBody', name: 'Box Body', basedOn: 'Normal', next: 'BoxBody', run: { ...base, size: PT(10) }, paragraph: { spacing: { after: 80, line: 264, lineRule: AUTO } } },
      { id: 'TableMessage', name: 'Table Message', basedOn: 'Normal', next: 'Body', run: { font: FONT_HEAD, size: PT(9), bold: true, color: C.navy },
        paragraph: { spacing: { before: 0, after: 120, line: 264, lineRule: AUTO }, indent: { left: 160, right: 120 }, keepNext: true,
          shading: { type: ShadingType.CLEAR, fill: C.light, color: 'auto' }, border: { left: { style: BorderStyle.SINGLE, size: 36, color: C.teal, space: 8 }, top: { style: BorderStyle.SINGLE, size: 4, color: C.light, space: 4 }, bottom: { style: BorderStyle.SINGLE, size: 4, color: C.light, space: 4 } } } },
      { id: 'FootnoteText', name: 'footnote text', basedOn: 'Normal', next: 'FootnoteText', run: { font: FONT_HEAD, size: PT(7.5), color: C.grey }, paragraph: { spacing: FN_MODE.has('tight') ? { before: 0, after: 0, line: 200, lineRule: AUTO } : { before: 0, after: 20, line: 220, lineRule: AUTO } } },
      { id: 'Quote', name: 'Quote', basedOn: 'Body', next: 'Body', run: { ...base, italics: true, color: C.grey }, paragraph: { indent: { left: 567, right: 567 }, spacing: { after: 140 } } },
      { id: 'TocL1', name: 'TOC L1', basedOn: 'Normal', next: 'TocL1', run: { font: FONT_HEAD, size: PT(10), bold: true, color: C.ink }, paragraph: { spacing: { before: 100, after: 40 } } },
      { id: 'TocL2', name: 'TOC L2', basedOn: 'Normal', next: 'TocL2', run: { font: FONT_BODY, size: PT(10.5), color: C.ink }, paragraph: { indent: { left: 400 }, spacing: { after: 30 } } },
      { id: 'CoverTitle', name: 'Cover Title', basedOn: 'Normal', run: { font: FONT_TITLE, size: PT(34), bold: true, color: C.navy }, paragraph: { spacing: { before: 2400, after: 200 } } },
      { id: 'CoverSub', name: 'Cover Sub', basedOn: 'Normal', run: { font: FONT_HEAD, size: PT(14), bold: true, color: C.teal }, paragraph: { spacing: { after: 600 } } },
      { id: 'CoverMeta', name: 'Cover Meta', basedOn: 'Normal', run: { font: FONT_HEAD, size: PT(10.5), color: C.grey }, paragraph: { spacing: { after: 80 } } },
      { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Body', quickFormat: true, run: { font: FONT_TITLE, size: PT(22), bold: true, color: C.navy }, paragraph: { spacing: { before: 0, after: 360 }, keepNext: true, outlineLevel: 0 } },
      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Body', quickFormat: true, run: { font: FONT_HEAD, size: PT(15), bold: true, color: C.navy }, paragraph: { spacing: { before: 360, after: 200 }, keepNext: true, outlineLevel: 1, border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: C.teal, space: 6 } } } },
      { id: 'Heading3', name: 'Heading 3', basedOn: 'Normal', next: 'Body', quickFormat: true, run: { font: FONT_HEAD, size: PT(11.5), bold: true, color: C.dcyan }, paragraph: { spacing: { before: 280, after: 120 }, keepNext: true, outlineLevel: 2 } },
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
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: C.teal, space: 4 } },
    children: [new TextRun({ text: shortTitle, font: FONT_HEAD, size: PT(7.5), color: C.grey }), new TextRun({ text: `\t${draft ? 'DRAFT FOR DISCUSSION' : ''}`, font: FONT_HEAD, size: PT(7.5), bold: true, color: C.navy })],
  })] });
  const footer = new Footer({ children: [new Paragraph({
    tabStops: [{ type: TabStopType.RIGHT, position: TEXT_WIDTH_DXA }],
    children: [new TextRun({ text: 'Wesgro  |  Letsema in partnership with Skift Advisory', font: FONT_HEAD, size: PT(7.5), color: C.grey }), new TextRun({ children: ['\t', PageNumber.CURRENT], font: FONT_HEAD, size: PT(8), bold: true, color: C.navy })],
  })] });
  return { header, footer };
}

// sections: [{ children, landscape?, firstPageBlank? }]
function buildDocument({ sections, shortTitle, draft = true, title, creator = 'Letsema in partnership with Skift Advisory' }) {
  const { header, footer } = headerFooter(shortTitle, draft);
  return new Document({
    creator, title, description: 'Final research report',
    styles: styles(), numbering: numberingConfig(), footnotes: FOOTNOTES,
    features: { updateFields: false },
    sections: sections.map((s, i) => ({
      properties: {
        page: { size: { width: PAGE.width, height: PAGE.height }, margin: { top: PAGE.margin, bottom: PAGE.margin, left: PAGE.margin, right: PAGE.margin, header: 600, footer: 600 } },
        titlePage: !!s.firstPageBlank,
        pageNumberStart: s.pageNumberStart,
      },
      // The first page of these sections is a charcoal CI page (cover, divider, back cover): the draft marking stays, in white.
      headers: s.firstPageBlank ? { default: header, first: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: draft ? 'DRAFT FOR DISCUSSION' : '', font: FONT_HEAD, size: PT(7.5), bold: true, color: C.white })] })] }) } : { default: header },
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
  fullBleed, divider, runs, noteRuns, resetCites, citeMode, FN_MODE, body, lead, note, kicker, h1, h1NoBreak, h2, h3, h4, pageBreak, spacer, numbered, bullets, cite, citeSplit, FOOTNOTE_TEXT,
  makeContext, setChapter, headings, pageOf, table, grid, box, figure, contentsList, buildDocument, save,
  Paragraph, TextRun, AlignmentType,
};
