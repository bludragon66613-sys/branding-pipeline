/**
 * inject-and-export.mjs
 * 1. Injects Freepik images as base64 into all 15 execution decks
 * 2. Generates PDFs via Chrome headless
 * 3. Sends each PDF to the Real Estate Branding Telegram group
 *
 * Image placement per deck (8 slides):
 *   S1 cover   → cover.jpg  (dark overlay, bg behind text)
 *   S4 villas  → outdoor.jpg (dark overlay)
 *   S5-left    → interior.jpg (accent-color overlay, feature panel)
 *   S8 close   → cover.jpg again (dark overlay)
 */

import fs from 'fs';
import path from 'path';
import https from 'https';
import { execSync, exec } from 'child_process';
import { fileURLToPath } from 'url';
import { promisify } from 'util';

const execAsync = promisify(exec);
const __dirname = path.dirname(fileURLToPath(import.meta.url));

const EXEC_DIR   = path.join(__dirname, 'projects', 'virama', 'execution');
const IMG_DIR    = path.join(EXEC_DIR, 'brand-images');
const OUT_DIR    = path.join(EXEC_DIR, 'updated');
const BOT_TOKEN  = '8573892946:AAFzDV6eDwiOr_Azj-eKOODV9UD-Fpf-LD4';
const CHAT_ID    = '-1003461219121';
const CHROME     = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';

const BRANDS = [
  { id: 'aurum',   name: 'Aurum',   tagline: 'The art of the junction' },
  { id: 'croft',   name: 'Croft',   tagline: 'Private Land. Personal Standard.' },
  { id: 'grantha', name: 'Grantha', tagline: 'Every room is a chapter' },
  { id: 'kohl',    name: 'Kohl',    tagline: 'Drawn from This Ground' },
  { id: 'norr',    name: 'Norr',    tagline: 'The body knows what the mind forgets' },
  { id: 'oikos',   name: 'Oikos',   tagline: 'The Whole World Within One Gate' },
  { id: 'palomar', name: 'Palomar', tagline: 'Colour is the first architecture' },
  { id: 'revel',   name: 'Revel',   tagline: 'Architecture as Spectacle' },
  { id: 'roji',    name: 'Roji',    tagline: 'The Walk Home Is Part of the Home' },
  { id: 'serac',   name: 'Sérac',   tagline: 'Where the air runs out of things to say' },
  { id: 'silaj',   name: 'Silāj',   tagline: 'To Descend Is to Arrive' },
  { id: 'tessera', name: 'Tessera', tagline: 'Each piece. The whole.' },
  { id: 'therme',  name: 'Therme',  tagline: 'Built From What It Stands On' },
  { id: 'verano',  name: 'Verano',  tagline: 'The Unhurried Life of the Estate' },
  { id: 'zenith',  name: 'Zénith',  tagline: 'The Pinnacle Is Not a Place. It Is a Practice.' },
];

// ─── Image helpers ─────────────────────────────────────────────────────────

function toBase64(imgPath) {
  if (!fs.existsSync(imgPath)) return null;
  return 'data:image/jpeg;base64,' + fs.readFileSync(imgPath).toString('base64');
}

/** Inject background image into a CSS class selector in <style> block */
function injectBgCss(html, cssClass, b64, opacity, blendMode = 'normal') {
  // Insert after the class opening brace
  const overlayStyle = `
  /* ── injected image ── */
  .${cssClass} {
    background-image: url('${b64}');
    background-size: cover;
    background-position: center;
    background-blend-mode: ${blendMode};
  }`;
  // Append before closing </style>
  return html.replace('</style>', overlayStyle + '\n</style>');
}

/**
 * Injects an absolutely-positioned image div + overlay into a slide element.
 * Works by inserting HTML immediately after the opening tag of the slide div.
 */
function injectImgDiv(html, slideClass, b64, overlayColor, overlayOpacity) {
  const imgDiv = `
    <div style="position:absolute;inset:0;z-index:0;pointer-events:none;">
      <img src="${b64}" style="width:100%;height:100%;object-fit:cover;display:block;" />
      <div style="position:absolute;inset:0;background:${overlayColor};opacity:${overlayOpacity};"></div>
    </div>`;
  // Find the opening div tag for this class and insert after it
  const regex = new RegExp(`(<div[^>]*class="[^"]*\\b${slideClass}\\b[^"]*"[^>]*>)`);
  return html.replace(regex, `$1${imgDiv}`);
}

// ─── Telegram ─────────────────────────────────────────────────────────────

function sendTelegramFile(filePath, caption) {
  return new Promise((resolve, reject) => {
    const boundary = `BOUND${Date.now()}`;
    const fileContent = fs.readFileSync(filePath);
    const filename = path.basename(filePath);
    const body = Buffer.concat([
      Buffer.from(`--${boundary}\r\nContent-Disposition: form-data; name="chat_id"\r\n\r\n${CHAT_ID}\r\n`),
      Buffer.from(`--${boundary}\r\nContent-Disposition: form-data; name="caption"\r\n\r\n${caption}\r\n`),
      Buffer.from(`--${boundary}\r\nContent-Disposition: form-data; name="document"; filename="${filename}"\r\nContent-Type: application/pdf\r\n\r\n`),
      fileContent,
      Buffer.from(`\r\n--${boundary}--\r\n`),
    ]);
    const u = new URL(`https://api.telegram.org/bot${BOT_TOKEN}/sendDocument`);
    const req = https.request({
      hostname: u.hostname, path: u.pathname, method: 'POST',
      headers: { 'Content-Type': `multipart/form-data; boundary=${boundary}`, 'Content-Length': body.length },
    }, res => {
      let d = '';
      res.on('data', c => (d += c));
      res.on('end', () => {
        const json = JSON.parse(d);
        if (json.ok) resolve(json);
        else reject(new Error(json.description));
      });
    });
    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

function sendTelegramMsg(text) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify({ chat_id: CHAT_ID, text, parse_mode: 'Markdown' });
    const req = https.request({
      hostname: 'api.telegram.org',
      path: `/bot${BOT_TOKEN}/sendMessage`,
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(body) },
    }, res => {
      let d = '';
      res.on('data', c => (d += c));
      res.on('end', () => resolve(JSON.parse(d)));
    });
    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

const sleep = ms => new Promise(r => setTimeout(r, ms));

// ─── Core: inject images into HTML ────────────────────────────────────────

function buildUpdatedHtml(brandId, originalHtml) {
  const coverB64    = toBase64(path.join(IMG_DIR, `${brandId}-cover.jpg`));
  const interiorB64 = toBase64(path.join(IMG_DIR, `${brandId}-interior.jpg`));
  const outdoorB64  = toBase64(path.join(IMG_DIR, `${brandId}-outdoor.jpg`));

  let html = originalHtml;

  // Add position:relative to page class so absolute children work
  html = html.replace(
    '.page {',
    '.page {\n    position: relative;'
  );

  // S1 — Cover: cover.jpg as full background with deep dark overlay
  if (coverB64) {
    html = injectImgDiv(html, 's1', coverB64, '#000000', 0.62);
    // Ensure text is above overlay
    html = html.replace(
      '.s1-left-bar {',
      '.s1-left-bar { position:relative; z-index:1;'
    );
    html = html.replace(
      '.s1-main {',
      '.s1-main { position:relative; z-index:1;'
    );
    html = html.replace(
      '.s1-right-column {',
      '.s1-right-column { position:relative; z-index:1;'
    );
  }

  // S4 — Villas: outdoor.jpg as bg with dark overlay (walnut tones)
  if (outdoorB64) {
    html = injectImgDiv(html, 's4', outdoorB64, '#1a1005', 0.72);
    html = html.replace(
      '.s4-top {',
      '.s4-top { position:relative; z-index:1;'
    );
    html = html.replace(
      '.s4-grid {',
      '.s4-grid { position:relative; z-index:1;'
    );
  }

  // S5-left panel: interior.jpg as bg with accent-color overlay
  // Extract the accent/primary color from CSS vars for overlay tint
  const accentMatch = html.match(/--(?:accent|gold|primary|teal|moss|blue|terracotta|magenta|jade|brass|champagne|lichen|thermal|adriatic|bronze|deep-gold|sultan-jade|golconda|spruce|aegean|volcanic|forest|stepwell|byzantine|stone|navy):\s*(#[0-9a-fA-F]{3,6})/);
  const accentColor = accentMatch ? accentMatch[1] : '#1a1a1a';

  if (interiorB64) {
    html = injectImgDiv(html, 's5-left', interiorB64, accentColor, 0.68);
    // Make children above overlay
    html = html.replace(
      '.s5-feature-label {',
      '.s5-feature-label { position:relative; z-index:1;'
    );
    html = html.replace(
      '.s5-feature-title {',
      '.s5-feature-title { position:relative; z-index:1;'
    );
    html = html.replace(
      '.s5-feature-body {',
      '.s5-feature-body { position:relative; z-index:1;'
    );
  }

  // S8 — Close: outdoor.jpg as bg with very dark overlay
  if (outdoorB64) {
    html = injectImgDiv(html, 's8', outdoorB64, '#000000', 0.70);
    html = html.replace(
      '.s8-label {',
      '.s8-label { position:relative; z-index:1;'
    );
    html = html.replace(
      '.s8-brand {',
      '.s8-brand { position:relative; z-index:1;'
    );
    html = html.replace(
      '.s8-tagline {',
      '.s8-tagline { position:relative; z-index:1;'
    );
    html = html.replace(
      '.s8-rule {',
      '.s8-rule { position:relative; z-index:1;'
    );
  }

  // S2-left dark panel: cover.jpg at low opacity for texture
  if (coverB64) {
    html = injectImgDiv(html, 's2-left', coverB64, '#0d0d0d', 0.78);
    html = html.replace(
      '.s2-year {',
      '.s2-year { z-index:1;'
    );
    html = html.replace(
      '.s2-location-label {',
      '.s2-location-label { position:relative; z-index:1;'
    );
    html = html.replace(
      '.s2-headline {',
      '.s2-headline { position:relative; z-index:1;'
    );
    html = html.replace(
      '.s2-body {',
      '.s2-body { position:relative; z-index:1;'
    );
  }

  return html;
}

// ─── PDF generation via Chrome headless ───────────────────────────────────

async function generatePdf(htmlPath, pdfPath) {
  const cmd = `"${CHROME}" --headless=new --disable-gpu --no-sandbox --print-to-pdf="${pdfPath}" --print-to-pdf-no-header --no-pdf-header-footer "file:///${htmlPath.replace(/\\/g, '/')}"`;
  await execAsync(cmd, { timeout: 60000 });
}

// ─── Main ─────────────────────────────────────────────────────────────────

async function main() {
  fs.mkdirSync(OUT_DIR, { recursive: true });

  await sendTelegramMsg(`🏗 *Virama — Updated Brand Decks*\n\nInjecting imagery into all 15 brand presentations and regenerating PDFs. Sending each one now...`);

  let sent = 0;

  for (const brand of BRANDS) {
    const srcHtml = path.join(EXEC_DIR, `deck_${brand.id}.html`);
    if (!fs.existsSync(srcHtml)) {
      console.log(`⚠ skipping ${brand.id} — HTML not found`);
      continue;
    }

    console.log(`\n── ${brand.name}`);

    // 1. Read + inject
    const original = fs.readFileSync(srcHtml, 'utf8');
    const updated  = buildUpdatedHtml(brand.id, original);

    const updatedHtml = path.join(OUT_DIR, `deck_${brand.id}.html`);
    const updatedPdf  = path.join(OUT_DIR, `deck_${brand.id}.pdf`);
    fs.writeFileSync(updatedHtml, updated, 'utf8');
    console.log(`  ✓ HTML injected`);

    // 2. Generate PDF
    try {
      await generatePdf(updatedHtml, updatedPdf);
      const size = fs.statSync(updatedPdf).size;
      console.log(`  ✓ PDF generated (${(size / 1024 / 1024).toFixed(1)}MB)`);
    } catch (e) {
      console.error(`  ✗ PDF failed: ${e.message}`);
      continue;
    }

    // 3. Send to Telegram
    try {
      await sendTelegramFile(updatedPdf, `*${brand.name}*\n_${brand.tagline}_\n\nVirama brand deck — with imagery`);
      console.log(`  ✓ sent to Telegram`);
      sent++;
    } catch (e) {
      console.error(`  ✗ Telegram send failed: ${e.message}`);
    }

    await sleep(2000); // avoid rate limiting
  }

  await sendTelegramMsg(`✅ *Done!* ${sent}/15 brand decks delivered.\n\nAll PDFs also saved to \`execution/updated/\``);
  console.log(`\n✅ Complete — ${sent}/15 PDFs sent.`);
}

main().catch(e => { console.error('Fatal:', e); process.exit(1); });
