'use strict';
// Text QA over content JSON: banned words, em and en dashes, Oxford commas (heuristic), long sentences,
// placeholders, US spellings, and the six-part template for Chapter 3 focus-area entries.
// Usage: node qa_text.js [content dir ...]   (default: all chapter content directories)
const fs = require('fs');
const path = require('path');
const { loadDir } = require('./content_render');

const dirs = process.argv.slice(2).length ? process.argv.slice(2) : ['exec', 'ch1', 'ch2', 'ch3', 'ch4', 'ch5', 'appendices'].map((d) => path.join(__dirname, 'content', d));

const BANNED = [
  { re: /\becosystems?\b/i, label: 'ecosystem' },
  { re: /\bunlocking\b/i, label: 'unlocking (title only)' },
  { re: /\bformali[sz]ation\b/i, label: 'formalisation' },
  { re: /80\s*[:/]\s*20/, label: '80:20' },
  { re: /\bprivate ownership\b/i, label: 'private ownership' },
  { re: /—/, label: 'em dash' },
  { re: /\s–\s/, label: 'spaced en dash' },
  { re: /\bleverag(e|ing|es)\b/i, label: 'leverage' },
  { re: /\bdelve/i, label: 'delve' },
  { re: /\bsynerg/i, label: 'synergy' },
  { re: /\bnavigat(e|ing)\b/i, label: 'navigate' },
  { re: /\bgame-?changer/i, label: 'game-changer' },
  { re: /\brobust\b/i, label: 'robust' },
  { re: /\bjourney\b/i, label: 'journey (check: traveller journeys are allowed)' },
  { re: /\b(really|very|incredibly|absolutely|truly|deeply)\b/i, label: 'intensifier' },
  { re: /\b(organization|prioritize|behavior|center|program\b|traveler|labor|color|optimize|analyze|realize|recognize|favor)/, label: 'US spelling' },
];
const OXFORD = /\b\w+,\s+\w+(\s+\w+)?,\s+(and|or)\s+\w+/i; // "a, b, and c"
const WORDS = (s) => s.trim().split(/\s+/).filter(Boolean).length;

const TEMPLATE_PARTS = ['Hypothesis and disposition', 'Evidence', 'Recommendation', 'Benchmark precedent', 'Link forward'];

let issues = 0;
function flag(file, kind, text) { issues += 1; console.log(`${file}: ${kind}: ${String(text).slice(0, 160)}`); }

for (const dir of dirs) {
  if (!fs.existsSync(dir)) continue;
  for (const section of loadDir(dir)) {
    const file = `${path.basename(dir)}/${section.__file}`;
    const strings = [];
    const push = (s, where) => { if (typeof s === 'string') strings.push({ s, where }); };
    (section.blocks || []).forEach((b, i) => {
      push(b.text, `block ${i} ${b.type}`); push(b.caption, `block ${i} caption`);
      (b.items || []).forEach((t) => push(t, `block ${i} item`));
      (b.paras || []).forEach((t) => push(t, `block ${i} box`));
      (b.rows || []).forEach((r) => r.forEach((c) => push(c, `block ${i} cell`)));
    });
    for (const { s, where } of strings) {
      for (const b of BANNED) if (b.re.test(s) && !(b.label.startsWith('unlocking') && /Unlocking Tourism/.test(s))) flag(file, `${b.label} (${where})`, s);
      if (OXFORD.test(s)) flag(file, `possible Oxford comma (${where})`, s.match(OXFORD)[0]);
      if (/\[[^\]]+\]/.test(s)) flag(file, `placeholder (${where})`, s.match(/\[[^\]]+\]/)[0]);
      // Count sentence length without parenthetical citations or bracketed placeholders; a closing bold marker ends a label.
      const plain = s.replace(/\([^()]*\b(19|20)\d\d\b[^()]*\)/g, '').replace(/\[[^\]]*\]/g, '').replace(/\.\*\*/g, '.');
      if (where.includes('cell')) continue;
      for (const sent of plain.split(/(?<=[.!?])\s+/)) if (WORDS(sent) > 35) flag(file, `long sentence ${WORDS(sent)} words (${where})`, sent);
    }
    // Chapter 3 template: each h3 entry (focus area) must have the kicker and the five h4 parts.
    if (/ch3/.test(dir)) {
      const blocks = section.blocks || [];
      // Theme headings ("3.1.1 Traveller, brand and proposition") are h3 too but carry a section number; skip them.
      const entries = blocks.map((b, i) => ({ b, i })).filter(({ b }) => b.type === 'h3' && !/^\d+\.\d+\.\d+\s/.test(b.text));
      entries.forEach(({ i }, k) => {
        const end = k + 1 < entries.length ? entries[k + 1].i : blocks.length;
        const slice = blocks.slice(i, end);
        const h4s = slice.filter((b) => b.type === 'h4').map((b) => b.text);
        const missing = TEMPLATE_PARTS.filter((p) => !h4s.some((h) => h.toLowerCase().startsWith(p.toLowerCase())));
        if (!(blocks[i - 1] && blocks[i - 1].type === 'kicker')) flag(file, 'focus area without kicker', blocks[i].text);
        if (!(slice[1] && slice[1].type === 'lead')) flag(file, 'focus area without topline lead', blocks[i].text);
        if (missing.length) flag(file, `focus area missing parts: ${missing.join('; ')}`, blocks[i].text);
      });
    }
  }
}
console.log(`${issues} issue(s)`);
process.exit(issues ? 1 : 0);
