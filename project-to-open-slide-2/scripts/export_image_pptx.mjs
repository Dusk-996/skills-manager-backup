#!/usr/bin/env node
import { createRequire } from 'node:module';
import { spawn, spawnSync } from 'node:child_process';
import fs from 'node:fs';
import net from 'node:net';
import path from 'node:path';
import process from 'node:process';

function arg(name) {
  const index = process.argv.indexOf(`--${name}`);
  return index >= 0 ? process.argv[index + 1] : undefined;
}

const target = path.resolve(arg('target') || '.');
const deck = arg('deck');
const output = path.resolve(arg('output') || path.join(target, 'exports', deck || 'deck', `${deck}.pptx`));
if (!deck) throw new Error('--deck is required');

const requireFromTarget = createRequire(path.join(target, 'package.json'));
const { chromium } = requireFromTarget('playwright-core');
const candidates = [
  process.env.CHROME_PATH,
  'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe',
  'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
].filter(Boolean);
const executablePath = candidates.find((candidate) => fs.existsSync(candidate));
if (!executablePath) throw new Error('未找到 Edge/Chrome，请设置 CHROME_PATH');

async function freePort() {
  return await new Promise((resolve, reject) => {
    const server = net.createServer();
    server.listen(0, '127.0.0.1', () => {
      const address = server.address();
      server.close(() => resolve(address.port));
    });
    server.on('error', reject);
  });
}

const port = await freePort();
const command = process.platform === 'win32' ? process.env.ComSpec : 'corepack';
const commandArgs = process.platform === 'win32'
  ? ['/d', '/s', '/c', 'corepack pnpm dev']
  : ['pnpm', 'dev'];
const child = spawn(command, commandArgs, {
  cwd: target,
  env: { ...process.env, OPEN_SLIDE_PORT: String(port) },
  windowsHide: true,
  stdio: ['ignore', 'pipe', 'pipe'],
});
let log = '';
child.stdout.on('data', (chunk) => { log += chunk.toString(); });
child.stderr.on('data', (chunk) => { log += chunk.toString(); });

let browser;
try {
  const base = `http://localhost:${port}`;
  for (let attempt = 0; attempt < 90; attempt += 1) {
    try {
      const response = await fetch(base);
      if (response.ok) break;
    } catch {}
    if (attempt === 89) throw new Error(`Open Slide 启动超时\n${log}`);
    await new Promise((resolve) => setTimeout(resolve, 1000));
  }
  browser = await chromium.launch({ executablePath, headless: true });
  const context = await browser.newContext({
    acceptDownloads: true,
    viewport: { width: 1920, height: 1080 },
  });
  const page = await context.newPage();
  await page.goto(`${base}/s/${encodeURIComponent(deck)}`, { waitUntil: 'networkidle' });
  const downloadPromise = page.waitForEvent('download', { timeout: 180000 });
  await page.getByRole('button', { name: /Download|下载/ }).click();
  await page.getByText(/Export as image PPTX|导出图片 PPTX/, { exact: true }).click();
  const download = await downloadPromise;
  fs.mkdirSync(path.dirname(output), { recursive: true });
  await download.saveAs(output);
  console.log(JSON.stringify({ ok: true, output, deck, port }));
} finally {
  if (browser) await browser.close();
  if (!child.killed) {
    if (process.platform === 'win32') {
      spawnSync('taskkill', ['/PID', String(child.pid), '/T', '/F'], {
        windowsHide: true,
        stdio: 'ignore',
      });
    } else {
      child.kill('SIGTERM');
    }
  }
  child.stdout.destroy();
  child.stderr.destroy();
}
process.exit(0);
