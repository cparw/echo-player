// Usage: node render.js timeline.json out.mov [startSec] [endSec] [stillsDir]
// Renders the transparent motion graphics layer frame by frame and pipes PNGs into ffmpeg (PNG in MOV keeps alpha).
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

(async () => {
  const [tlPath, out, s0, s1, stills] = process.argv.slice(2);
  const tl = JSON.parse(fs.readFileSync(tlPath, 'utf8'));
  const fps = tl.fps || 30;
  const start = s0 ? parseFloat(s0) : 0;
  const end = s1 ? parseFloat(s1) : tl.duration;
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.join(__dirname, 'stage.html'));
  await page.evaluate(async () => { await document.fonts.load('400 100px Anton'); await document.fonts.load('800 100px "Inter Tight"'); await document.fonts.load('italic 400 100px "Instrument Serif"'); await document.fonts.load('500 30px "JetBrains Mono"'); });
  await page.evaluate(tl => window.init(tl), tl);

  if (stills) {
    fs.mkdirSync(stills, { recursive: true });
    for (const t of tl.stills || []) {
      await page.evaluate(t => window.renderAt(t), t);
      await page.screenshot({ path: path.join(stills, `still_${String(t).replace('.', '_')}.png`), omitBackground: false });
    }
    await browser.close();
    return;
  }

  const n = Math.round((end - start) * fps);
  const ff = spawn('ffmpeg', ['-y', '-v', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'png', '-i', '-', '-c:v', 'png', '-pix_fmt', 'rgba', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  const t0 = Date.now();
  for (let i = 0; i < n; i++) {
    const t = start + i / fps;
    await page.evaluate(t => window.renderAt(t), t);
    const buf = await page.screenshot({ type: 'png', omitBackground: true });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (i % 150 === 0) console.log(`frame ${i}/${n} (${((Date.now() - t0) / 1000).toFixed(0)}s)`);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await browser.close();
  console.log(`done ${n} frames in ${((Date.now() - t0) / 1000).toFixed(0)}s -> ${out}`);
})();
