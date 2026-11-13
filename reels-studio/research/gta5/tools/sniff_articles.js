// Usage: node sniff_articles.js out.json url1 url2 ...
// Visits public Newswire article pages; keeps the title and every image URL the page loads, shows, or lists in its own data.
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const [out, ...urls] = process.argv.slice(2);
  const proxy = process.env.HTTPS_PROXY || process.env.https_proxy;
  const browser = await chromium.launch(proxy ? { proxy: { server: proxy } } : {});
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const res = {};
  for (const url of urls) {
    const page = await ctx.newPage(); const imgs = new Set();
    page.on('response', async r => {
      const u = r.url();
      if (/\.(jpg|jpeg|png|webp)(\?|$)/i.test(u) && /rockstargames/.test(u)) imgs.add(u);
      if (u.includes('graph.rockstargames.com')) { try { const t = await r.text(); for (const m of t.matchAll(/https?:\\?\/\\?\/[^"\s]+?\.(?:jpg|jpeg|png|webp)/gi)) imgs.add(m[0].replace(/\\\//g, '/')); } catch (e) {} }
    });
    try { await page.goto(url, { waitUntil: 'networkidle', timeout: 50000 }); } catch (e) {}
    for (let i = 0; i < 10; i++) { await page.mouse.wheel(0, 1600); await page.waitForTimeout(500); }
    await page.waitForTimeout(1500);
    const dom = await page.evaluate(() => [...document.querySelectorAll('img, source, a')].flatMap(e => [e.currentSrc, e.src, e.href, ...(e.srcset || '').split(',').map(s => s.trim().split(' ')[0])]).filter(Boolean));
    dom.filter(u => /\.(jpg|jpeg|png|webp)(\?|$)/i.test(u)).forEach(u => imgs.add(u));
    const title = await page.title();
    res[url] = { title, final: page.url(), imgs: [...imgs] };
    console.log(title, '|', imgs.size, 'images');
    await page.close();
  }
  fs.writeFileSync(out, JSON.stringify(res, null, 1));
  await browser.close();
})();
