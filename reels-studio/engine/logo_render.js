const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const [html, out] = process.argv.slice(2);
  const b = await chromium.launch();
  const url = 'file://' + path.join(__dirname, html);
  const p = await b.newPage({ viewport: { width: 1080, height: 1080 } });
  await p.goto(url + '?mode=pfp'); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(200);
  await p.screenshot({ path: path.join(out, 'profile_picture.png') });
  const q = await b.newPage({ viewport: { width: 1080, height: 760 }, deviceScaleFactor: 1 });
  await q.goto(url + '?mode=mock'); await q.evaluate(() => document.fonts.ready); await q.waitForTimeout(200);
  await q.screenshot({ path: path.join(out, 'instagram_preview.png') });
  await b.close();
})();
