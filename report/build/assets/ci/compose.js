// Compose A4 page backgrounds from the Wesgro CI assets (charcoal ground, contour pattern, protea W, logo, QR).
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const A = path.join(__dirname, 'source');
const b64 = (f) => `data:image/${f.endsWith('.svg') ? 'svg+xml' : 'png'};base64,${fs.readFileSync(path.join(A, f)).toString('base64')}`;
const page = (inner) => `<!doctype html><html><head><style>
  html,body{margin:0;padding:0} .pg{position:relative;width:210mm;height:297mm;background:#4D4D4F;overflow:hidden}
  img{position:absolute;display:block}</style></head><body><div class="pg">${inner}</div></body></html>`;
const PAGES = {
  cover: page(`<img src="${b64('logo_white.png')}" style="left:20mm;top:18mm;width:58mm">
               <img src="${b64('w_protea_crop.png')}" style="left:84mm;top:52mm;width:104mm">`),
  divider: page(`<img src="${b64('contours.svg')}" style="left:50%;top:0;height:297mm;transform:translateX(-46%)">`),
  divider_alt: page(`<img src="${b64('contours.svg')}" style="left:-75mm;top:95mm;width:360mm;-webkit-mask-image:linear-gradient(to bottom,transparent 0,#000 18%,#000 82%,transparent 100%)">`),
  back: page(`<img src="${b64('contours.svg')}" style="left:50%;top:0;height:297mm;transform:translateX(-46%)">
              <img src="${b64('logo_white.png')}" style="left:20mm;top:18mm;width:58mm">
              <img src="${b64('w_outline_protea.png')}" style="left:118mm;top:178mm;width:72mm">
              <img src="${b64('qr_crop.png')}" style="left:20mm;top:226mm;width:24mm">
              <div style="position:absolute;left:20mm;top:253mm;color:#fff;font:15px Arial,Helvetica,sans-serif">Learn more</div>`),
};
(async () => {
  const b = await chromium.launch();
  for (const [name, html] of Object.entries(PAGES)) {
    const p = await b.newPage({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 2.0833 });
    await p.setContent(html, { waitUntil: 'load' }); await p.waitForTimeout(200);
    await p.screenshot({ path: path.join(__dirname, `bg_${name}.png`), clip: { x: 0, y: 0, width: 794, height: 1123 } });
    await p.close(); console.log('wrote', name);
  }
  await b.close();
})();
