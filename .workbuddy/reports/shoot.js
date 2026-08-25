const { chromium } = require('playwright-core');
const path = require('path');

const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe';
const URL = 'file:///D:/Github/webw/index.html';
const OUT = 'D:/Github/webw/.workbuddy/reports/shots';

(async () => {
  const browser = await chromium.launch({
    executablePath: EDGE,
    headless: true,
    args: ['--headless=new', '--no-sandbox', '--disable-gpu']
  });
  const results = [];

  async function shoot(name, opts, action) {
    const ctx = await browser.newContext(opts);
    const page = await ctx.newPage();
    await page.goto(URL, { waitUntil: 'load' });
    await page.waitForTimeout(900);
    if (action) await action(page);
    await page.waitForTimeout(500);
    const file = path.join(OUT, name);
    await page.screenshot({ path: file });
    results.push(name + ' OK');
    await ctx.close();
  }

  await shoot('desktop-light.png', { viewport: { width: 1440, height: 900 }, colorScheme: 'light' });
  await shoot('desktop-dark.png', { viewport: { width: 1440, height: 900 }, colorScheme: 'dark' });
  await shoot('mobile-light.png', { viewport: { width: 390, height: 844 }, colorScheme: 'light' });
  await shoot('modal-light.png', { viewport: { width: 1440, height: 900 }, colorScheme: 'light' }, async (p) => {
    await p.click('#tosOpen');
    await p.waitForTimeout(600);
  });

  // Hover 状态：验证按钮扫光 + 卡片玻璃高亮
  await shoot('hover-fx.png', { viewport: { width: 1440, height: 900 }, colorScheme: 'light' }, async (p) => {
    await p.evaluate(() => window.scrollTo(0, 880));
    await p.waitForTimeout(700);
    await p.hover('.feat');
    await p.waitForTimeout(500);
  });

  // 控制台错误收集
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, colorScheme: 'light' });
  const page = await ctx.newPage();
  const errors = [];
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  page.on('pageerror', e => errors.push(String(e)));
  await page.goto(URL, { waitUntil: 'load' });
  await page.waitForTimeout(1200);
  await page.evaluate(() => window.scrollTo(0, 400));
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(OUT, 'desktop-scrolled.png') });
  await ctx.close();

  console.log(results.join('\n'));
  console.log('JS 错误:', errors.length === 0 ? '无' : errors.join(' | '));
  await browser.close();
})().catch(e => { console.error('FAIL:', e.message); process.exit(1); });
