'use strict';
// Pass-1 helper: find the printed page of every registered heading, figure and table caption in the converted PDF.
// Usage: node scan_pages.js report.pdf pagemap.json   (reads headings.json written by report.js pass 1)
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

const [,, pdf, outFile] = process.argv;
const here = __dirname;
const registry = JSON.parse(fs.readFileSync(path.join(here, 'headings.json'), 'utf8'));
const nPages = parseInt((execFileSync('pdfinfo', [pdf]).toString().match(/Pages:\s+(\d+)/) || [0, '0'])[1], 10);

const norm = (s) => s.replace(/\s+/g, ' ').replace(/[‘’]/g, "'").replace(/[“”]/g, '"').trim().toLowerCase();
// Each page is kept as its list of normalised lines; a heading or caption matches only a line that starts with it,
// so a heading's words inside a table or a sentence do not count.
const pages = [];
for (let p = 1; p <= nPages; p++) {
  const txt = execFileSync('pdftotext', ['-f', String(p), '-l', String(p), pdf, '-']).toString();
  pages.push(txt.split('\n').map(norm).filter(Boolean));
}
// A title can wrap (the chapter dividers set theirs large), so a line joined with the next two also counts.
const has = (lines, needle) => lines.some((l, i) => l.startsWith(needle) || (needle.length > 40 && l.length >= 20 && needle.startsWith(l))
  || (needle.length > l.length && needle.startsWith(l) && lines.slice(i, i + 3).join(' ').startsWith(needle)));

// Search in order, never moving backwards, starting after the front matter: the first page whose lines include the
// Abbreviations heading closes it (contents, figures and tables lists all come before it).
const abbrevIdx = pages.findIndex((lines) => lines.includes('abbreviations'));
const skip = abbrevIdx >= 0 ? abbrevIdx + 1 : (registry.skipPages || 0);
const map = {};
let cursor = Math.max(0, skip);
for (const item of registry.items) {
  const needle = norm(item.title).slice(0, 60);
  let found = null;
  for (let p = cursor; p < pages.length; p++) {
    if (has(pages[p], needle)) { found = p + 1; cursor = p; break; }
  }
  if (found == null) {
    // fall back to an unordered search after the contents pages
    for (let p = skip; p < pages.length; p++) if (has(pages[p], needle)) { found = p + 1; break; }
  }
  map[item.title] = found;
}
fs.writeFileSync(outFile, JSON.stringify({ nPages, map }, null, 1));
const missing = Object.entries(map).filter(([, v]) => v == null).map(([k]) => k);
console.log(`scanned ${nPages} pages, mapped ${Object.keys(map).length - missing.length}/${Object.keys(map).length} entries`);
if (missing.length) console.log('unmapped:', missing.slice(0, 20).join(' | '));
