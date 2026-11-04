'use strict';
// Chart templates that return SVG strings for content figures. Drafting agents pass data; style stays consistent.
// Types: lineChart, barChart (vertical, grouped), hbarChart (horizontal), stackedBarChart.
// All charts: 1600 x 900 viewBox, Raleway, palette aligned with helpers.js. Values are formatted with fmt().

const PAL = ['#0B3C5D', '#1F7A8C', '#7A9E7E', '#C98B2B', '#8C5E8A', '#B23A48', '#5B6572'];
const INK = '#1C2431', GREY = '#5B6572', GRID = '#C9D1DA';
const W = 1600, HGT = 900;
const FONT = 'Raleway, Arial, sans-serif';

function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
let DEC = false; // set per chart: when any value in a small-number series has decimals, print one decimal throughout
function fmt(v, unit) {
  if (v == null || Number.isNaN(v)) return '';
  const a = Math.abs(v);
  let s;
  if (unit === '%') s = DEC ? `${(Math.round(v * 10) / 10).toFixed(1)}%` : `${Math.round(v * 10) / 10}%`;
  else if (DEC && a < 100) s = (Math.round(v * 10) / 10).toFixed(1);
  else if (a >= 1e6) s = `${(v / 1e6).toFixed(a >= 1e7 ? 1 : 2)}m`;
  else if (a >= 1e4) s = `${Math.round(v / 1e3)}k`;
  else if (a >= 1e3) s = Math.round(v).toLocaleString('en-GB');
  else s = Number.isInteger(v) ? String(v) : String(Math.round(v * 10) / 10);
  return unit && unit !== '%' ? `${unit}${s}` : s;
}
function niceTicks(min, max, n = 4) {
  const span = max - min || 1;
  const raw = span / n;
  const mag = Math.pow(10, Math.floor(Math.log10(raw)));
  const steps = [1, 2, 2.5, 5, 10];
  const step = steps.map((s) => s * mag).find((s) => s >= raw) || 10 * mag;
  const lo = Math.floor(min / step) * step;
  const hi = Math.ceil(max / step) * step;
  const ticks = [];
  for (let t = lo; t <= hi + 1e-9; t += step) ticks.push(Math.round(t * 1e6) / 1e6);
  return { lo, hi, ticks };
}
function frame(title, subtitle) {
  let s = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${HGT}" width="${W}" height="${HGT}" font-family="${FONT}"><rect width="${W}" height="${HGT}" fill="#ffffff"/>`;
  if (title) s += `<text x="40" y="52" font-size="30" font-weight="700" fill="${INK}">${esc(title)}</text>`;
  if (subtitle) s += `<text x="40" y="88" font-size="22" fill="${GREY}">${esc(subtitle)}</text>`;
  return s;
}
function legend(series, x, y) {
  let s = ''; let cx = x;
  series.forEach((sr, i) => {
    s += `<rect x="${cx}" y="${y - 16}" width="22" height="22" rx="3" fill="${sr.color || PAL[i % PAL.length]}"/>`;
    s += `<text x="${cx + 32}" y="${y + 2}" font-size="22" fill="${INK}">${esc(sr.name)}</text>`;
    cx += 32 + sr.name.length * 12.5 + 40;
  });
  return s;
}

// lineChart({ title, subtitle, categories: ['2025',...], series: [{name, values, color}], unit, yMin, refLines: [{value, label, color}], labelLast: true })
function lineChart(o) {
  const L = 150, R = 300, T = o.title ? 130 : 60, B = 110;
  const pw = W - L - R, ph = HGT - T - B;
  const all = o.series.flatMap((s) => s.values).concat((o.refLines || []).map((r) => r.value)).filter((v) => v != null);
  const { lo, hi, ticks } = niceTicks(o.yMin != null ? o.yMin : Math.min(...all), Math.max(...all));
  const y = (v) => T + ph - ((v - lo) / (hi - lo)) * ph;
  const n = o.categories.length;
  const x = (i) => L + (n === 1 ? pw / 2 : (i / (n - 1)) * pw);
  let s = frame(o.title, o.subtitle);
  for (const t of ticks) s += `<line x1="${L}" y1="${y(t)}" x2="${L + pw}" y2="${y(t)}" stroke="${GRID}" stroke-width="1"/><text x="${L - 14}" y="${y(t) + 8}" text-anchor="end" font-size="22" fill="${GREY}">${fmt(t, o.unit)}</text>`;
  o.categories.forEach((c, i) => { s += `<text x="${x(i)}" y="${T + ph + 44}" text-anchor="middle" font-size="22" fill="${GREY}">${esc(c)}</text>`; });
  for (const r of o.refLines || []) {
    s += `<line x1="${L}" y1="${y(r.value)}" x2="${L + pw}" y2="${y(r.value)}" stroke="${r.color || '#B23A48'}" stroke-width="3" stroke-dasharray="12 9"/>`;
    s += `<text x="${L + 12}" y="${y(r.value) - 12}" font-size="22" font-weight="700" fill="${r.color || '#B23A48'}">${esc(r.label || '')}</text>`;
  }
  o.series.forEach((sr, si) => {
    const col = sr.color || PAL[si % PAL.length];
    const pts = sr.values.map((v, i) => (v == null ? null : `${x(i)},${y(v)}`)).filter(Boolean).join(' ');
    s += `<polyline fill="none" stroke="${col}" stroke-width="5" stroke-linejoin="round" stroke-linecap="round" points="${pts}"/>`;
    sr.values.forEach((v, i) => { if (v != null) s += `<circle cx="${x(i)}" cy="${y(v)}" r="7" fill="${col}"/>`; });
    const lastIdx = sr.values.length - 1;
    if (o.labelLast !== false && sr.values[lastIdx] != null) s += `<text x="${L + pw + 14}" y="${y(sr.values[lastIdx]) + 8}" font-size="22" font-weight="700" fill="${col}">${esc(sr.name)} ${fmt(sr.values[lastIdx], o.unit)}</text>`;
  });
  if (o.labelLast === false) s += legend(o.series, L, T - 20);
  if (o.footnote) s += `<text x="40" y="${HGT - 20}" font-size="18" fill="${GREY}">${esc(o.footnote)}</text>`;
  return s + '</svg>';
}

// barChart({ title, subtitle, categories, series: [{name, values, color}], unit, showValues: true })
function barChart(o) {
  const L = 150, R = 60, T = o.title ? 150 : 80, B = 110;
  const pw = W - L - R, ph = HGT - T - B;
  const all = o.series.flatMap((s) => s.values).filter((v) => v != null);
  const { lo, hi, ticks } = niceTicks(Math.min(0, ...all), Math.max(...all));
  const y = (v) => T + ph - ((v - lo) / (hi - lo)) * ph;
  const n = o.categories.length, k = o.series.length;
  const slot = pw / n, gap = slot * 0.25, bw = (slot - gap) / k;
  let s = frame(o.title, o.subtitle);
  for (const t of ticks) s += `<line x1="${L}" y1="${y(t)}" x2="${L + pw}" y2="${y(t)}" stroke="${GRID}" stroke-width="1"/><text x="${L - 14}" y="${y(t) + 8}" text-anchor="end" font-size="22" fill="${GREY}">${fmt(t, o.unit)}</text>`;
  o.categories.forEach((c, i) => {
    const cx = L + i * slot + slot / 2;
    const words = String(c).split(' ');
    const lines = words.length > 2 && String(c).length > 14 ? [words.slice(0, Math.ceil(words.length / 2)).join(' '), words.slice(Math.ceil(words.length / 2)).join(' ')] : [String(c)];
    lines.forEach((ln, li) => { s += `<text x="${cx}" y="${T + ph + 40 + li * 26}" text-anchor="middle" font-size="21" fill="${GREY}">${esc(ln)}</text>`; });
    o.series.forEach((sr, si) => {
      const v = sr.values[i]; if (v == null) return;
      const col = sr.color || PAL[si % PAL.length];
      const x0 = L + i * slot + gap / 2 + si * bw;
      const top = Math.min(y(v), y(0)), h = Math.abs(y(0) - y(v));
      s += `<rect x="${x0}" y="${top}" width="${bw - 4}" height="${h}" fill="${col}" rx="2"/>`;
      if (o.showValues !== false) s += `<text x="${x0 + (bw - 4) / 2}" y="${top - 10}" text-anchor="middle" font-size="20" font-weight="700" fill="${INK}">${fmt(v, o.unit)}</text>`;
    });
  });
  if (k > 1) s += legend(o.series, L, T - 30);
  if (o.footnote) s += `<text x="40" y="${HGT - 20}" font-size="18" fill="${GREY}">${esc(o.footnote)}</text>`;
  return s + '</svg>';
}

// hbarChart({ title, subtitle, categories, values, unit, color, highlight: [indices] })
function hbarChart(o) {
  const n = o.categories.length;
  const T = o.title ? 130 : 60, B = 50;
  const L = 40 + Math.min(420, Math.max(...o.categories.map((c) => String(c).length)) * 13), R = 180;
  const pw = W - L - R, ph = HGT - T - B;
  const rowH = ph / n, bh = Math.min(rowH * 0.66, 60);
  const max = Math.max(...o.values.filter((v) => v != null));
  const x = (v) => L + (v / max) * pw;
  let s = frame(o.title, o.subtitle);
  o.categories.forEach((c, i) => {
    const v = o.values[i]; const cy = T + i * rowH + rowH / 2;
    const col = (o.highlight || []).includes(i) ? (o.highlightColor || PAL[1]) : (o.color || PAL[0]);
    s += `<text x="${L - 16}" y="${cy + 8}" text-anchor="end" font-size="22" fill="${INK}">${esc(c)}</text>`;
    if (v != null) {
      s += `<rect x="${L}" y="${cy - bh / 2}" width="${Math.max(2, x(v) - L)}" height="${bh}" fill="${col}" rx="3"/>`;
      s += `<text x="${x(v) + 12}" y="${cy + 8}" font-size="22" font-weight="700" fill="${INK}">${fmt(v, o.unit)}</text>`;
    }
  });
  if (o.footnote) s += `<text x="40" y="${HGT - 14}" font-size="18" fill="${GREY}">${esc(o.footnote)}</text>`;
  return s + '</svg>';
}

// stackedBarChart({ title, subtitle, categories, series: [{name, values}], unit, totals: true })
function stackedBarChart(o) {
  const L = 150, R = 60, T = o.title ? 170 : 100, B = 110;
  const pw = W - L - R, ph = HGT - T - B;
  const n = o.categories.length;
  const sums = o.categories.map((_, i) => o.series.reduce((a, s) => a + (s.values[i] || 0), 0));
  const { lo, hi, ticks } = niceTicks(0, Math.max(...sums));
  const y = (v) => T + ph - ((v - lo) / (hi - lo)) * ph;
  const slot = pw / n, bw = slot * 0.6;
  let s = frame(o.title, o.subtitle);
  for (const t of ticks) s += `<line x1="${L}" y1="${y(t)}" x2="${L + pw}" y2="${y(t)}" stroke="${GRID}" stroke-width="1"/><text x="${L - 14}" y="${y(t) + 8}" text-anchor="end" font-size="22" fill="${GREY}">${fmt(t, o.unit)}</text>`;
  o.categories.forEach((c, i) => {
    const x0 = L + i * slot + (slot - bw) / 2; let acc = 0;
    o.series.forEach((sr, si) => {
      const v = sr.values[i] || 0; if (!v) return;
      const col = sr.color || PAL[si % PAL.length];
      s += `<rect x="${x0}" y="${y(acc + v)}" width="${bw}" height="${y(acc) - y(acc + v)}" fill="${col}"/>`;
      if ((y(acc) - y(acc + v)) > 26 && o.segmentValues !== false) s += `<text x="${x0 + bw / 2}" y="${(y(acc) + y(acc + v)) / 2 + 7}" text-anchor="middle" font-size="19" fill="#ffffff">${fmt(v, o.unit)}</text>`;
      acc += v;
    });
    if (o.totals !== false) s += `<text x="${x0 + bw / 2}" y="${y(acc) - 10}" text-anchor="middle" font-size="21" font-weight="700" fill="${INK}">${fmt(acc, o.unit)}</text>`;
    s += `<text x="${x0 + bw / 2}" y="${T + ph + 40}" text-anchor="middle" font-size="22" fill="${GREY}">${esc(c)}</text>`;
  });
  s += legend(o.series, L, T - 40);
  if (o.footnote) s += `<text x="40" y="${HGT - 20}" font-size="18" fill="${GREY}">${esc(o.footnote)}</text>`;
  return s + '</svg>';
}

// ganttChart({ title, phases: [{name, from, to}], years: [2027..2035], rows: [{code, name, cells: {2027:'D'|'I'|'', ...}}] })
// D = design (light), I = implement (dark). One row per initiative; years as columns.
function ganttChart(o) {
  const years = o.years;
  const rowH = 44, headH = o.title ? 150 : 90, L = 520, R = 40;
  const H = headH + o.rows.length * rowH + 60;
  const pw = W - L - R, cw = pw / years.length;
  let s = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" font-family="${FONT}"><rect width="${W}" height="${H}" fill="#ffffff"/>`;
  if (o.title) s += `<text x="40" y="52" font-size="30" font-weight="700" fill="${INK}">${esc(o.title)}</text>`;
  if (o.subtitle) s += `<text x="40" y="88" font-size="22" fill="${GREY}">${esc(o.subtitle)}</text>`;
  // phase bands
  (o.phases || []).forEach((ph, i) => {
    const i0 = years.indexOf(ph.from), i1 = years.indexOf(ph.to);
    if (i0 < 0 || i1 < 0) return;
    const x0 = L + i0 * cw, x1 = L + (i1 + 1) * cw;
    s += `<rect x="${x0}" y="${headH - 50}" width="${x1 - x0}" height="${H - headH + 50 - 60}" fill="${i % 2 ? '#F3F6F9' : '#FFFFFF'}"/>`;
    s += `<text x="${(x0 + x1) / 2}" y="${headH - 58}" text-anchor="middle" font-size="21" font-weight="700" fill="${PAL[0]}">${esc(ph.name)}</text>`;
  });
  years.forEach((y, i) => { s += `<text x="${L + i * cw + cw / 2}" y="${headH - 22}" text-anchor="middle" font-size="20" fill="${GREY}">${esc(y)}</text>`; });
  o.rows.forEach((r, ri) => {
    const y = headH + ri * rowH;
    s += `<line x1="40" y1="${y + rowH}" x2="${W - R}" y2="${y + rowH}" stroke="${GRID}" stroke-width="1"/>`;
    s += `<text x="40" y="${y + rowH / 2 + 7}" font-size="19" font-weight="700" fill="${INK}">${esc(r.code)}</text>`;
    s += `<text x="110" y="${y + rowH / 2 + 7}" font-size="19" fill="${INK}">${esc(String(r.name).slice(0, 42))}</text>`;
    years.forEach((yr, i) => {
      const c = (r.cells || {})[yr];
      if (!c) return;
      const fill = c === 'I' ? PAL[0] : (c === 'D' ? '#9DBBD0' : '#DCE6EE');
      s += `<rect x="${L + i * cw + 3}" y="${y + 9}" width="${cw - 6}" height="${rowH - 18}" rx="3" fill="${fill}"/>`;
    });
  });
  const ly = H - 26;
  s += `<rect x="${L}" y="${ly - 16}" width="22" height="18" rx="3" fill="#9DBBD0"/><text x="${L + 30}" y="${ly}" font-size="19" fill="${INK}">Design</text>`;
  s += `<rect x="${L + 140}" y="${ly - 16}" width="22" height="18" rx="3" fill="${PAL[0]}"/><text x="${L + 170}" y="${ly}" font-size="19" fill="${INK}">Implement</text>`;
  return s + '</svg>';
}

// treeChart({ goal, pillars: [{name, objective, themes: [{name, areas: [{code, name, disposition}]}]}] })
// The hypothesis tree as a figure: three pillar columns, themes stacked, focus areas listed with disposition tags.
function treeChart(o) {
  const cols = o.pillars.length;
  const colW = (W - 80) / cols, gap = 24;
  const FS = 21, LH = 26, WRAP = 27;
  const DISP = { Validated: '#7A9E7E', Refined: '#1F7A8C', Reworded: '#C98B2B', New: '#0B3C5D', Moved: '#8C5E8A', Flagged: '#B23A48', Withdrawn: '#5B6572' };
  // height: tallest pillar column
  const colH = o.pillars.map((p) => p.themes.reduce((acc, t) => acc + 52 + t.areas.reduce((a2, ar) => a2 + 44 + (wrap(ar.name, WRAP).length) * LH + 8, 0) + 10, 0));
  const H = 250 + Math.max(...colH) + 20;
  let s = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" font-family="${FONT}"><rect width="${W}" height="${H}" fill="#ffffff"/>`;
  s += `<rect x="40" y="20" width="${W - 80}" height="64" rx="6" fill="${PAL[0]}"/><text x="${W / 2}" y="62" text-anchor="middle" font-size="28" font-weight="700" fill="#ffffff">${esc(o.goal)}</text>`;
  o.pillars.forEach((p, pi) => {
    const x = 40 + pi * colW + gap / 2, w = colW - gap;
    s += `<rect x="${x}" y="104" width="${w}" height="100" rx="6" fill="${PAL[1]}"/>`;
    s += `<text x="${x + w / 2}" y="144" text-anchor="middle" font-size="27" font-weight="700" fill="#ffffff">${esc(p.name)}</text>`;
    s += `<text x="${x + w / 2}" y="180" text-anchor="middle" font-size="20" fill="#ffffff">${esc(p.objective || '')}</text>`;
    let y = 222;
    p.themes.forEach((t) => {
      s += `<rect x="${x}" y="${y}" width="${w}" height="42" rx="4" fill="${C_HEAD()}"/><text x="${x + 12}" y="${y + 29}" font-size="21" font-weight="700" fill="${PAL[0]}">${esc(t.name)}</text>`;
      y += 52;
      t.areas.forEach((a) => {
        const lines = wrap(a.name, WRAP);
        const h = 44 + lines.length * LH;
        s += `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="4" fill="#ffffff" stroke="${GRID}"/>`;
        s += `<text x="${x + 12}" y="${y + 30}" font-size="${FS}" font-weight="700" fill="${INK}">${esc(a.code)}</text>`;
        lines.forEach((ln, li) => { s += `<text x="${x + 52}" y="${y + 30 + li * LH}" font-size="${FS}" fill="${INK}">${esc(ln)}</text>`; });
        if (a.disposition) {
          const dw = a.disposition.length * 11 + 22;
          s += `<rect x="${x + 52}" y="${y + h - 34}" width="${dw}" height="26" rx="13" fill="${DISP[a.disposition] || GREY}"/><text x="${x + 52 + dw / 2}" y="${y + h - 15}" text-anchor="middle" font-size="16" font-weight="700" fill="#ffffff">${esc(a.disposition)}</text>`;
        }
        y += h + 8;
      });
      y += 10;
    });
  });
  return s + '</svg>';
}
function C_HEAD() { return '#DCE6EE'; }
function wrap(text, n) {
  const words = String(text).split(' '); const lines = []; let cur = '';
  for (const w of words) { if ((cur + ' ' + w).trim().length > n) { lines.push(cur.trim()); cur = w; } else cur += ' ' + w; }
  if (cur.trim()) lines.push(cur.trim());
  return lines;
}

// Resolve a figure block that carries { chart: { type, ...options } } into its SVG string.
function svgFor(chart) {
  const vals = [].concat(chart.values || [], ...((chart.series || []).map((x) => x.values || []))).filter((v) => typeof v === 'number');
  DEC = vals.length > 0 && vals.every((v) => Math.abs(v) < 100) && vals.some((v) => !Number.isInteger(v));
  const fns = { line: lineChart, bar: barChart, hbar: hbarChart, stacked: stackedBarChart, gantt: ganttChart, tree: treeChart };
  const fn = fns[chart.type];
  if (!fn) throw new Error(`unknown chart type ${chart.type}`);
  return fn(chart);
}

module.exports = { lineChart, barChart, hbarChart, stackedBarChart, ganttChart, treeChart, svgFor, PAL };
