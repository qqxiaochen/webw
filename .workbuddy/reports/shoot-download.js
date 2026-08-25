const { chromium } = require('playwright-core');
const path = require('path');

const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe';
const URL = 'file:///D:/Github/webw/download.html';
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

  await shoot('dl-desktop-light.png', { viewport: { width: 1440, height: 1200 }, colorScheme: 'light' });
  await shoot('dl-desktop-dark.png', { viewport: { width: 1440, height: 1200 }, colorScheme: 'dark' });
  await shoot('dl-mobile-light.png', { viewport: { width: 390, height: 844 }, colorScheme: 'light' });
  await shoot('dl-intro-light.png', { viewport: { width: 1440, height: 1200 }, colorScheme: 'light' }, async (p) => {
    await p.click('[data-intro="we"]');
    await p.waitForTimeout(600);
  });

  // 控制台错误收集
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 1200 }, colorScheme: 'light' });
  const page = await ctx.newPage();
  const errors = [];
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  page.on('pageerror', e => errors.push(String(e)));
  await page.goto(URL, { waitUntil: 'load' });
  await page.waitForTimeout(1000);
  await page.evaluate(() => window.scrollTo(0, 400));
  await page.waitForTimeout(500);
  await page.click('[data-intro="vn"]');
  await page.waitForTimeout(500);
  await page.keyboard.press('Escape');
  await page.waitForTimeout(300);
  await ctx.close();

  console.log(results.join('\n'));
  console.log('JS 错误:', errors.length === 0 ? '无' : errors.join(' | '));
  await browser.close();
})().catch(e => { console.error('FAIL:', e.message); process.exit(1); });
