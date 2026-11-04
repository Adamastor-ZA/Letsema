'use strict';
// Renders content-block JSON (written by drafting agents) into docx elements through helpers.js.
// A content file is { "id": "2.1", "title": "...", "blocks": [ ... ] }. Block types:
//   h2 | h3 | h4 | kicker | lead | p | note | quote   -> { type, text, attribution? }
//   numbered | bullets                               -> { type, items: [..], ref? }
//   table   -> { type, caption, source, columns: [{header, width, align}], rows: [[..]], boldFirstCol? }
//   box     -> { type, title, paras: [..] }
//   grid    -> { type, columns, rows } (unnumbered table, no caption: Chapter 3 action tables)
//   figure  -> { type, id, caption, source, widthCm?, svg? (inline SVG string) | file? (png under assets/png) }
//   pagebreak
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

const ASSETS = path.join(__dirname, 'assets');

function ensureFigure(block) {
  const pngDir = path.join(ASSETS, 'png');
  const svgDir = path.join(ASSETS, 'svg');
  fs.mkdirSync(pngDir, { recursive: true }); fs.mkdirSync(svgDir, { recursive: true });
  if (block.file) return path.isAbsolute(block.file) ? block.file : path.join(pngDir, block.file);
  if (block.chart && !block.svg) block.svg = require('./charts').svgFor(block.chart);
  if (!block.svg || !block.id) return null;
  const svgPath = path.join(svgDir, `${block.id}.svg`);
  const pngPath = path.join(pngDir, `${block.id}.png`);
  const current = fs.existsSync(svgPath) ? fs.readFileSync(svgPath, 'utf8') : null;
  if (current !== block.svg) fs.writeFileSync(svgPath, block.svg);
  const stale = !fs.existsSync(pngPath) || current !== block.svg;
  if (stale) {
    try {
      execFileSync('node', [path.join(__dirname, 'render_svg.js'), svgPath, pngPath, '2'], { stdio: 'pipe', env: { ...process.env, NODE_PATH: process.env.NODE_PATH || execFileSync('npm', ['root', '-g']).toString().trim() } });
    } catch (e) {
      console.error(`figure ${block.id}: render failed: ${e.message.split('\n')[0]}`);
      return null;
    }
  }
  return pngPath;
}

function render(ctx, H, blocks, heads) {
  const out = [];
  const hd = heads || H.headings(ctx);
  for (const b of blocks) {
    switch (b.type) {
      case 'h2': out.push(hd.h2(b.text, b.id)); break;
      case 'h3': out.push(hd.h3(b.text, b.id)); break;
      case 'h4': out.push(hd.h4(b.text)); break;
      case 'kicker': out.push(H.kicker(b.text)); break;
      case 'lead': out.push(H.lead(b.text)); break;
      case 'p': out.push(H.body(b.text)); break;
      case 'note': out.push(H.note(b.text)); break;
      case 'quote': out.push(new H.Paragraph({ style: 'Quote', children: H.runs(b.attribution ? `${b.text} (${b.attribution})` : b.text) })); break;
      case 'numbered': out.push(...H.numbered(b.items, b.ref || 'n_policy')); break;
      case 'bullets': out.push(...H.bullets(b.items)); break;
      case 'table': out.push(...H.table(ctx, { caption: b.caption, source: b.source, columns: b.columns, rows: b.rows, boldFirstCol: !!b.boldFirstCol, zebra: b.zebra !== false })); break;
      case 'box': out.push(...H.box(b.title, b.paras || [])); break;
      case 'grid': out.push(H.grid(b.columns, b.rows, { zebra: b.zebra !== false }), H.spacer(6)); break;
      case 'figure': out.push(...H.figure(ctx, { file: ensureFigure(b), caption: b.caption, source: b.source, widthCm: b.widthCm })); break;
      case 'pagebreak': out.push(H.pageBreak()); break;
      case 'spacer': out.push(H.spacer(b.pt || 6)); break;
      default: throw new Error(`unknown block type ${b.type}`);
    }
  }
  return out;
}

// Load every *.json in a content directory in filename order.
function loadDir(dir) {
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir).filter((f) => f.endsWith('.json')).sort().map((f) => {
    const data = JSON.parse(fs.readFileSync(path.join(dir, f), 'utf8'));
    data.__file = f;
    return data;
  });
}

// Factory for a chapter module: an H1 followed by every content file's blocks.
function makeChapter({ chapter, title, dir, bookmark }) {
  return {
    build(ctx, H) {
      H.setChapter(ctx, chapter);
      const hd = H.headings(ctx);
      const out = [hd.h1(title, bookmark)];
      for (const section of loadDir(dir)) {
        if (section.lead_title) out.push(hd.h2(section.lead_title));
        out.push(...render(ctx, H, section.blocks || [], hd));
      }
      return out;
    },
  };
}

// Plain-text dump of a content directory for QA scripts (banned words, sentence length, placeholders).
function textOf(dir) {
  const parts = [];
  for (const s of loadDir(dir)) for (const b of s.blocks || []) {
    if (b.text) parts.push(b.text);
    if (b.items) parts.push(...b.items);
    if (b.caption) parts.push(b.caption);
    if (b.paras) parts.push(...b.paras);
    if (b.rows) for (const r of b.rows) parts.push(...r.map(String));
    if (b.columns) parts.push(...b.columns.map((c) => c.header));
  }
  return parts.join('\n');
}

module.exports = { render, loadDir, makeChapter, textOf, ensureFigure };
