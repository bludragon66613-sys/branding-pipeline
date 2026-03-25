/**
 * fetch-brand-images.mjs
 * Searches Freepik stock library for images matching each Virama execution brand.
 * 3 images per brand → sends to "Real Estate Branding" Telegram group.
 */

import https from 'https';
import http from 'http';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const FREEPIK_KEY = 'FPSX18731460d46dcdeef7d0dab5f2542e71';
const BOT_TOKEN   = '8573892946:AAFzDV6eDwiOr_Azj-eKOODV9UD-Fpf-LD4';
const CHAT_ID     = '-1003461219121'; // Real Estate Branding group
const OUTPUT_DIR  = path.join(__dirname, 'projects', 'virama', 'execution', 'brand-images');

// 15 brands × 3 images = 45 images
const BRANDS = [
  {
    id: 'aurum',
    name: 'Aurum',
    tagline: 'The art of the junction',
    palette: 'gold + dark ink + travertine',
    searches: [
      { slot: 'cover',    term: 'luxury villa gold warm candlelight exterior dusk architecture' },
      { slot: 'interior', term: 'luxury interior gold warm wood dark panelling jewellery boutique feel' },
      { slot: 'outdoor',  term: 'luxury pool gold travertine warm evening light estate' },
    ],
  },
  {
    id: 'croft',
    name: 'Croft',
    tagline: 'Private Land. Personal Standard.',
    palette: 'flint + weld green + brick red',
    searches: [
      { slot: 'cover',    term: 'english countryside estate manor private luxury exterior green' },
      { slot: 'interior', term: 'luxury country home interior dark green traditional fireplace' },
      { slot: 'outdoor',  term: 'private estate garden green field luxury home landscape' },
    ],
  },
  {
    id: 'grantha',
    name: 'Grantha',
    tagline: 'Every room is a chapter',
    palette: 'mahogany + parchment + rosewood',
    searches: [
      { slot: 'cover',    term: 'luxury villa dark mahogany library literary warm exterior' },
      { slot: 'interior', term: 'luxury home library dark wood bookshelves reading room parchment' },
      { slot: 'outdoor',  term: 'luxury heritage villa garden courtyard warm evening' },
    ],
  },
  {
    id: 'kohl',
    name: 'Kohl',
    tagline: 'Drawn from This Ground',
    palette: 'antimony black + sultan jade + Golconda gold',
    searches: [
      { slot: 'cover',    term: 'luxury dark villa black jade accents Hyderabad architecture opulent' },
      { slot: 'interior', term: 'opulent dark interior black jade gold indian luxury palace' },
      { slot: 'outdoor',  term: 'luxury pool dark stone jade green garden india evening' },
    ],
  },
  {
    id: 'norr',
    name: 'Norr',
    tagline: 'The body knows what the mind forgets',
    palette: 'spruce green + moss + birch white',
    searches: [
      { slot: 'cover',    term: 'scandinavian luxury villa forest pine green minimal architecture' },
      { slot: 'interior', term: 'nordic spa luxury interior birch wood light minimal serene' },
      { slot: 'outdoor',  term: 'luxury sauna forest pool nordic nature green exterior' },
    ],
  },
  {
    id: 'oikos',
    name: 'Oikos',
    tagline: 'The Whole World Within One Gate',
    palette: 'aegean blue + terracotta + olive',
    searches: [
      { slot: 'cover',    term: 'greek luxury villa aegean blue sea view terracotta architecture' },
      { slot: 'interior', term: 'mediterranean luxury interior blue white terracotta olive greek' },
      { slot: 'outdoor',  term: 'infinity pool aegean sea blue mediterranean luxury villa' },
    ],
  },
  {
    id: 'palomar',
    name: 'Palomar',
    tagline: 'Colour is the first architecture',
    palette: 'magenta + volcanic black + adobe',
    searches: [
      { slot: 'cover',    term: 'bold colourful luxury architecture villa vibrant pink magenta exterior' },
      { slot: 'interior', term: 'luxury interior bold colour vibrant art deco living room' },
      { slot: 'outdoor',  term: 'luxury pool bold colourful modern architecture vivid exterior' },
    ],
  },
  {
    id: 'revel',
    name: 'Revel',
    tagline: 'Architecture as Spectacle',
    palette: 'obsidian black + bronze + crystal',
    searches: [
      { slot: 'cover',    term: 'dramatic luxury villa obsidian black bronze night architecture spectacular' },
      { slot: 'interior', term: 'dramatic luxury interior crystal chandelier bronze obsidian dark glamour' },
      { slot: 'outdoor',  term: 'dramatic night pool obsidian black bronze lighting luxury villa' },
    ],
  },
  {
    id: 'roji',
    name: 'Roji',
    tagline: 'The Walk Home Is Part of the Home',
    palette: 'charcoal + roji moss + cedar + washi',
    searches: [
      { slot: 'cover',    term: 'japanese luxury villa zen garden path stone moss architecture' },
      { slot: 'interior', term: 'japanese luxury interior washi cedar wood minimal zen serene' },
      { slot: 'outdoor',  term: 'japanese zen garden path stones moss water luxury home' },
    ],
  },
  {
    id: 'serac',
    name: 'Sérac',
    tagline: 'Where the air runs out of things to say',
    palette: 'forest green + lichen + dew white',
    searches: [
      { slot: 'cover',    term: 'mountain luxury villa forest alpine architecture misty green exterior' },
      { slot: 'interior', term: 'mountain retreat luxury interior wood stone panoramic view nature' },
      { slot: 'outdoor',  term: 'alpine luxury pool mountain view forest misty landscape' },
    ],
  },
  {
    id: 'silaj',
    name: 'Silāj',
    tagline: 'To Descend Is to Arrive',
    palette: 'stepwell teal + sandstone + earth',
    searches: [
      { slot: 'cover',    term: 'heritage stepwell architecture teal sandstone india luxury villa' },
      { slot: 'interior', term: 'heritage indian interior stepwell teal sandstone luxury traditional' },
      { slot: 'outdoor',  term: 'heritage courtyard pool stepwell teal architecture india stone' },
    ],
  },
  {
    id: 'tessera',
    name: 'Tessera',
    tagline: 'Each piece. The whole.',
    palette: 'byzantine blue + gold + ivory + crimson',
    searches: [
      { slot: 'cover',    term: 'byzantine mosaic luxury villa gold blue architecture mediterranean' },
      { slot: 'interior', term: 'luxury interior mosaic gold byzantine crimson opulent mediterranean' },
      { slot: 'outdoor',  term: 'mediterranean luxury pool mosaic gold tile blue water villa' },
    ],
  },
  {
    id: 'therme',
    name: 'Therme',
    tagline: 'Built From What It Stands On',
    palette: 'stone + thermal blue + travertine',
    searches: [
      { slot: 'cover',    term: 'luxury spa villa stone travertine thermal architecture natural mineral' },
      { slot: 'interior', term: 'luxury thermal spa interior stone mineral pool travertine serene' },
      { slot: 'outdoor',  term: 'thermal spa pool luxury stone travertine natural steaming water' },
    ],
  },
  {
    id: 'verano',
    name: 'Verano',
    tagline: 'The Unhurried Life of the Estate',
    palette: 'terracotta + adriatic blue + linen',
    searches: [
      { slot: 'cover',    term: 'spanish iberian luxury estate terracotta warm sunshine exterior villa' },
      { slot: 'interior', term: 'mediterranean luxury interior terracotta linen warm sunlight estate' },
      { slot: 'outdoor',  term: 'spanish estate pool terracotta adriatic blue garden luxury sunshine' },
    ],
  },
  {
    id: 'zenith',
    name: 'Zénith',
    tagline: 'The Pinnacle Is Not a Place. It Is a Practice.',
    palette: 'deep navy + champagne gold + ivory',
    searches: [
      { slot: 'cover',    term: 'luxury penthouse villa navy champagne gold elevated high architecture' },
      { slot: 'interior', term: 'luxury interior navy deep blue champagne gold ivory elegant' },
      { slot: 'outdoor',  term: 'rooftop infinity pool navy luxury penthouse champagne high rise' },
    ],
  },
];

// ─── Helpers ─────────────────────────────────────────────────────────────────

function get(url, headers = {}) {
  return new Promise((resolve, reject) => {
    const mod = url.startsWith('https') ? https : http;
    let data = '';
    const req = mod.get(url, { headers }, res => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        return get(res.headers.location, headers).then(resolve).catch(reject);
      }
      res.on('data', c => (data += c));
      res.on('end', () => resolve({ status: res.statusCode, body: data }));
    });
    req.on('error', reject);
    req.setTimeout(30000, () => { req.destroy(); reject(new Error('timeout')); });
  });
}

function downloadFile(url, dest) {
  return new Promise((resolve, reject) => {
    const mod = url.startsWith('https') ? https : http;
    const file = fs.createWriteStream(dest);
    const req = mod.get(url, res => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        file.close();
        try { fs.unlinkSync(dest); } catch {}
        return downloadFile(res.headers.location, dest).then(resolve).catch(reject);
      }
      res.pipe(file);
      file.on('finish', () => file.close(resolve));
    });
    req.on('error', e => { try { fs.unlinkSync(dest); } catch {} reject(e); });
    req.setTimeout(60000, () => { req.destroy(); reject(new Error('download timeout')); });
  });
}

function postJson(url, data) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify(data);
    const u = new URL(url);
    const req = https.request({
      hostname: u.hostname, path: u.pathname + u.search, method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(body) },
    }, res => {
      let d = '';
      res.on('data', c => (d += c));
      res.on('end', () => resolve({ status: res.statusCode, body: d }));
    });
    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

function sendPhoto(filePath, caption) {
  return new Promise((resolve, reject) => {
    const boundary = `--BOUNDARY${Date.now()}`;
    const fileContent = fs.readFileSync(filePath);
    const filename = path.basename(filePath);
    const body = Buffer.concat([
      Buffer.from(`--${boundary}\r\nContent-Disposition: form-data; name="chat_id"\r\n\r\n${CHAT_ID}\r\n`),
      Buffer.from(`--${boundary}\r\nContent-Disposition: form-data; name="caption"\r\n\r\n${caption}\r\n`),
      Buffer.from(`--${boundary}\r\nContent-Disposition: form-data; name="photo"; filename="${filename}"\r\nContent-Type: image/jpeg\r\n\r\n`),
      fileContent,
      Buffer.from(`\r\n--${boundary}--\r\n`),
    ]);
    const u = new URL(`https://api.telegram.org/bot${BOT_TOKEN}/sendPhoto`);
    const req = https.request({
      hostname: u.hostname, path: u.pathname, method: 'POST',
      headers: { 'Content-Type': `multipart/form-data; boundary=${boundary}`, 'Content-Length': body.length },
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

// ─── Freepik ──────────────────────────────────────────────────────────────────

async function searchFreepik(term) {
  const url = `https://api.freepik.com/v1/resources?term=${encodeURIComponent(term)}&filters%5Bcontent_type%5D%5Bphoto%5D=1&filters%5Blicense%5D%5Bfreemium%5D=1&limit=8&order=relevance`;
  const res = await get(url, { 'x-freepik-api-key': FREEPIK_KEY, 'Accept-Language': 'en-US' });
  if (res.status !== 200) throw new Error(`Search failed: ${res.status}`);
  const json = JSON.parse(res.body);
  for (const item of (json.data || [])) {
    const imgUrl = item.image?.source?.url;
    // Only landscape orientation for deck images
    if (imgUrl && item.image?.orientation === 'horizontal') {
      return { id: item.id, title: item.title, url: imgUrl };
    }
  }
  // Fall back to any orientation
  const first = (json.data || [])[0];
  if (first?.image?.source?.url) return { id: first.id, title: first.title, url: first.image.source.url };
  return null;
}

// ─── Main ─────────────────────────────────────────────────────────────────────

async function main() {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
  console.log(`Output: ${OUTPUT_DIR}\n`);

  // Announce
  await postJson(`https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`, {
    chat_id: CHAT_ID, parse_mode: 'Markdown',
    text: `🏡 *Virama — Brand Image Pack*\n\nFetching Freepik stock photos for all 15 brands.\n3 images each: cover · interior · outdoor\nSending now...`,
  });

  let totalSent = 0;

  for (const brand of BRANDS) {
    console.log(`\n── ${brand.name} (${brand.palette})`);

    // Brand header message
    await postJson(`https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`, {
      chat_id: CHAT_ID, parse_mode: 'Markdown',
      text: `*${brand.name}* — _${brand.tagline}_\n${brand.palette}`,
    });
    await sleep(300);

    for (const search of brand.searches) {
      process.stdout.write(`  [${search.slot}] `);

      let result;
      try {
        result = await searchFreepik(search.term);
      } catch (e) {
        console.log(`search error: ${e.message}`);
        await sleep(2000);
        continue;
      }

      if (!result) {
        console.log('no results');
        continue;
      }

      console.log(`"${result.title.slice(0, 55)}"...`);

      const filepath = path.join(OUTPUT_DIR, `${brand.id}-${search.slot}.jpg`);
      try {
        await downloadFile(result.url, filepath);
      } catch (e) {
        console.log(`download failed: ${e.message}`);
        await sleep(1000);
        continue;
      }

      const caption = `${brand.name} — ${search.slot}\n${brand.palette}\n\n"${result.title}"`;
      try {
        const res = await sendPhoto(filepath, caption);
        if (res.ok) {
          console.log(`  ✓ sent`);
          totalSent++;
        } else {
          console.log(`  Telegram error: ${res.description}`);
        }
      } catch (e) {
        console.log(`  send error: ${e.message}`);
      }

      await sleep(600);
    }

    await sleep(1200);
  }

  await postJson(`https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`, {
    chat_id: CHAT_ID, parse_mode: 'Markdown',
    text: `✅ *Done!* ${totalSent}/45 images delivered across 15 Virama brands.\n\nFiles saved to \`execution/brand-images/\``,
  });

  console.log(`\n✅ Complete — ${totalSent}/45 images sent. Saved to: ${OUTPUT_DIR}`);
}

main().catch(e => { console.error('Fatal:', e); process.exit(1); });
