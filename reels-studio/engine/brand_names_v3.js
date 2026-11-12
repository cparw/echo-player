const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const out = process.argv[2];
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1200 }, deviceScaleFactor: 2 });
  const url = 'file://' + path.join(__dirname, 'brand_names_v3.html');
  await p.goto(url); await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(300);
  await p.screenshot({ path: path.join(out, 'names_sheet.jpg'), fullPage: true, type: 'jpeg', quality: 90 });
  const n = await p.evaluate(() => window.NAMES_COUNT);
  const q = await b.newPage({ viewport: { width: 1080, height: 1080 }, deviceScaleFactor: 1 });
  for (let i = 0; i < n; i++) {
    await q.goto(url + '?solo=' + i); await q.evaluate(() => document.fonts.ready); await q.waitForTimeout(150);
    await q.screenshot({ path: path.join(out, `avatar_${String(i + 1).padStart(2, '0')}.png`) });
  }
  await b.close();
})();
