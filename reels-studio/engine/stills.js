// Transparent graphics stills at given times (for fast previews). Usage: node stills.js timeline.json outDir t1 t2 ...
const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path');
(async () => {
  const [tlPath, outDir, ...ts] = process.argv.slice(2);
  const tl = JSON.parse(fs.readFileSync(tlPath, 'utf8'));
  fs.mkdirSync(outDir, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.join(__dirname, 'stage.html'));
  await page.evaluate(async () => { await document.fonts.load('400 100px Anton'); await document.fonts.load('800 100px "Inter Tight"'); await document.fonts.load('italic 400 100px "Instrument Serif"'); await document.fonts.load('500 30px "JetBrains Mono"'); });
  await page.evaluate(tl => window.init(tl), tl);
  for (const t of ts.map(Number)) {
    await page.evaluate(t => window.renderAt(t), t);
    await page.screenshot({ path: path.join(outDir, `g_${t.toFixed(2)}.png`), omitBackground: true });
  }
  await browser.close();
})();
