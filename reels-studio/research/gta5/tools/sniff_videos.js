// Usage: node sniff_videos.js out.json id1 id2 ...
// Visits each public video page https://www.rockstargames.com/videos/<id> and keeps the video data the page's own player loads.
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const [out, ...ids] = process.argv.slice(2);
  const proxy = process.env.HTTPS_PROXY || process.env.https_proxy;
  const browser = await chromium.launch(proxy ? { proxy: { server: proxy } } : {});
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const res = {};
  for (const id of ids) {
    const page = await ctx.newPage();
    page.on('response', async r => {
      if (r.url().includes('GET_VIDEO_DATA')) { try { const d = JSON.parse(await r.text()); const v = d.data && d.data.video; if (v && v.id === id) res[id] = v; } catch (e) {} }
    });
    try { await page.goto('https://www.rockstargames.com/videos/' + id, { waitUntil: 'networkidle', timeout: 45000 }); } catch (e) {}
    await page.waitForTimeout(1500);
    const v = res[id];
    console.log(id, v ? `${v.title} | ${v.createdFormatted} | ytOnly=${v.youtubeOnly} | agegated=${v.agegated} | ${(v.files || []).map(f => f.resolution).join(',')}` : 'NO DATA');
    await page.close();
  }
  fs.writeFileSync(out, JSON.stringify(res, null, 1));
  await browser.close();
})();
