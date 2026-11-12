// Usage: node cover.js cover.json out.png   (cover.json: {bg, tag, lines[], number, label, brand, titleSize?, numSize?, numTop?})
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
(async () => {
  const c = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.join(__dirname, 'cover.html'));
  await page.evaluate(async () => { await document.fonts.load('400 100px Anton'); await document.fonts.load('500 30px "JetBrains Mono"'); });
  await page.evaluate(c => window.renderCover(c), c);
  await page.waitForTimeout(150);
  await page.screenshot({ path: process.argv[3], type: 'png' });
  await browser.close();
  console.log('cover ->', process.argv[3]);
})();
