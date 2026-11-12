// node brand_shot.js <html> <out.png> <query> <width> <height> [scale]
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const [html, out, query, w, h, s] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: +w, height: +h }, deviceScaleFactor: +(s || 1) });
  await p.goto('file://' + path.join(__dirname, html) + '?' + query);
  await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(250);
  await p.screenshot({ path: out });
  await b.close();
})();
