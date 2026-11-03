'use strict';
// Render SVG files to PNG through the pre-installed Chromium (no plotting library in the sandbox).
// Usage: NODE_PATH=$(npm root -g) node render_svg.js in.svg out.png [scale]
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

async function renderOne(browser, svgPath, pngPath, scale) {
  const svg = fs.readFileSync(svgPath, 'utf8');
  const m = svg.match(/viewBox="0 0 (\d+(?:\.\d+)?) (\d+(?:\.\d+)?)"/) || svg.match(/width="(\d+)(?:px)?"\s+height="(\d+)(?:px)?"/);
  const w = m ? Math.ceil(parseFloat(m[1])) : 1200;
  const h = m ? Math.ceil(parseFloat(m[2])) : 700;
  const page = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: scale });
  const html = `<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;padding:0;background:#fff}svg{display:block}</style></head><body>${svg}</body></html>`;
  await page.setContent(html, { waitUntil: 'load' });
  await page.waitForTimeout(150); // let fonts settle
  await page.screenshot({ path: pngPath, clip: { x: 0, y: 0, width: w, height: h }, omitBackground: false });
  await page.close();
}

async function main() {
  const [,, input, output, scaleArg] = process.argv;
  const scale = scaleArg ? parseFloat(scaleArg) : 2;
  const browser = await chromium.launch();
  try {
    if (fs.statSync(input).isDirectory()) {
      fs.mkdirSync(output, { recursive: true });
      for (const f of fs.readdirSync(input).filter((x) => x.endsWith('.svg'))) {
        await renderOne(browser, path.join(input, f), path.join(output, f.replace(/\.svg$/, '.png')), scale);
        console.log('rendered', f);
      }
    } else {
      await renderOne(browser, input, output, scale);
      console.log('rendered', output);
    }
  } finally {
    await browser.close();
  }
}
main().catch((e) => { console.error(e); process.exit(1); });
