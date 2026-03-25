/**
 * Differentiation System — Batch Apply
 * Updates all 9 remaining brand HTML files with unique
 * typeface, accent color, archetype, and motif per brand.
 *
 * Reference sources: St. Regis (Roos custom serif), Aman (earth tones, custom type),
 * Bvlgari (Futura + travertine #d0bca4), Binghatti (geometric + orange).
 */

import { readFileSync, writeFileSync } from 'fs';
import { resolve } from 'path';

const DIR = new URL('.', import.meta.url).pathname.replace(/^\/([A-Z]:)/, '$1');

const BRANDS = [
  {
    file: 'nidra-kala.html',
    // Keep Playfair Display (already distinct) — shift accent to moonstone blue-grey
    fontImport: "https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,300;0,400;1,300;1,400&family=Inter:wght@300;400;500&display=swap",
    cssVars: {
      '--accent':  '#7A9AAA',
      '--light':   '#EAE8F0',
      '--reserve': '#1A2030',
      '--serif':   "'Playfair Display', 'Georgia', serif",
    },
    toneWords: ['Nocturne', 'Moonstone', 'Lunar hush'],
    colorwayNote: 'Near-black ground, pale moonstone breath, steel blue as the single cool accent. The palette of rooms that hold the sky inside them.',
    motifClass: null, // Playfair already distinct
    archetype: 'The Nocturne — lunar intimacy, curated silence',
  },
  {
    file: 'shanti-vela.html',
    // Cormorant → EB Garamond. Gold → sage teal.
    fontImport: "https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;1,400;1,500&family=Inter:wght@300;400;500&display=swap",
    cssVars: {
      '--accent':  '#5A8870',
      '--light':   '#E4EDE8',
      '--reserve': '#1A2E28',
      '--serif':   "'EB Garamond', 'Georgia', serif",
    },
    toneWords: ['Stillness', 'Verdure', 'Sage clarity'],
    colorwayNote: 'Deep forest ground, eucalyptus light, sage teal as the single cool green. The palette of garden walls, morning dew, and botanical permanence.',
    archetype: 'The Garden — living botanical, green sanctuary',
  },
  {
    file: 'prana-grove.html',
    // Keep Cormorant Garamond — ONLY brand that keeps it. Shift amber to lichen moss.
    fontImport: "https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300;1,400&family=Inter:wght@300;400;500&display=swap",
    cssVars: {
      '--accent':  '#8A7A3A',
      '--light':   '#F0EBD8',
      '--reserve': '#1E2A14',
      '--serif':   "'Cormorant Garamond', 'Georgia', serif",
    },
    toneWords: ['Breath', 'Growth', 'Lichen'],
    colorwayNote: 'Forest black ground, warm linen light, lichen moss as the single muted accent. The palette of 40-year roots, morning rain, and the earth beneath the address.',
    archetype: 'The Forest — ancient roots, living material',
  },
  {
    file: 'akasha-zenith.html',
    // Cormorant → Montserrat (geometric, altitude). Gold → cerulean blue.
    fontImport: "https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,200;0,300;0,400;1,200;1,300&family=Inter:wght@300;400;500&display=swap",
    cssVars: {
      '--accent':  '#2A6AAA',
      '--light':   '#E4EAF4',
      '--reserve': '#1A2E4A',
      '--serif':   "'Montserrat', sans-serif",
    },
    toneWords: ['Altitude', 'Clarity', 'Cerulean'],
    colorwayNote: 'Night navy ground, cool ivory light, cerulean as the single pure-blue accent. The palette of clear altitude, polished steel, and the specific quality of sky above the cloud line.',
    archetype: 'The Apex — stratospheric position, altitude as identity',
  },
  {
    file: 'ambara-sol.html',
    // Playfair → Abril Fatface (editorial warmth, sunset drama). Amber → terracotta sunset.
    fontImport: "https://fonts.googleapis.com/css2?family=Abril+Fatface&family=Inter:wght@300;400;500&display=swap",
    cssVars: {
      '--accent':  '#C85A28',
      '--light':   '#F2E4D4',
      '--reserve': '#3A1808',
      '--serif':   "'Abril Fatface', 'Georgia', serif",
    },
    toneWords: ['Dusk', 'Warmth', 'Terracotta'],
    colorwayNote: 'Deep umber ground, warm sand light, terracotta sunset as the single warm-orange accent. The palette of Rajasthani stone at the end of a long day — decisive, elemental, complete.',
    archetype: 'The Golden Hour — solar ritual, dusk as daily ceremony',
  },
  {
    file: 'vihara-terra.html',
    // Cormorant → Lora (warm, bookish, heritage). Bronze → burnt Deccan red.
    fontImport: "https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,500;1,400;1,500&family=Inter:wght@300;400;500&display=swap",
    cssVars: {
      '--accent':  '#9A3A28',
      '--light':   '#F0E4D8',
      '--reserve': '#2A1810',
      '--serif':   "'Lora', 'Georgia', serif",
    },
    toneWords: ['Heritage', 'Earth', 'Deccan red'],
    colorwayNote: 'Deep terracotta ground, sun-bleached ivory light, burnt Deccan red as the single warm accent. The palette of Shahabad stone walls, handmade clay tile, and the warmth of the plateau at noon.',
    archetype: 'The Haveli — Deccan heritage, local material culture',
  },
  {
    file: 'mandapa-arch.html',
    // Cormorant → Raleway (geometric humanist, architectural). Copper patina → steel teal.
    fontImport: "https://fonts.googleapis.com/css2?family=Raleway:ital,wght@0,200;0,300;0,400;1,200;1,300&family=Inter:wght@300;400;500&display=swap",
    cssVars: {
      '--accent':  '#3A7A9A',
      '--light':   '#E0E8EC',
      '--reserve': '#1E3A4A',
      '--serif':   "'Raleway', sans-serif",
    },
    toneWords: ['Structure', 'Craft', 'Steel teal'],
    colorwayNote: 'Dark slate ground, cool stone light, steel teal as the single architectural accent. The palette of raw concrete, weathered copper, and the specific grey of Hyderabad granite under overcast sky.',
    archetype: 'The Blueprint — structure as luxury, craft at column-scale',
  },
  {
    file: 'svara-resonance.html',
    // Cormorant → Josefin Sans (geometric, cosmic frequency). Gold → violet indigo.
    fontImport: "https://fonts.googleapis.com/css2?family=Josefin+Sans:ital,wght@0,100;0,200;0,300;1,100;1,200;1,300&family=Inter:wght@300;400;500&display=swap",
    cssVars: {
      '--accent':  '#7848B8',
      '--light':   '#E8E0F4',
      '--reserve': '#2A1A48',
      '--serif':   "'Josefin Sans', sans-serif",
    },
    toneWords: ['Resonance', 'Cosmos', 'Violet'],
    colorwayNote: 'Deep indigo ground, pale cosmic light, violet as the single frequency accent. The palette of lapis lazuli, instrument strings in a silent room, and the sky 60 seconds before full dark.',
    archetype: 'The Frequency — cosmic vibration, 432Hz silence architecture',
  },
];

// Font import regex — handles both Cormorant and other multi-family imports
const FONT_LINK_RE = /<link href="https:\/\/fonts\.googleapis\.com\/css2\?[^"]*" rel="stylesheet">/;

// CSS variable regex
function replaceCSSVar(html, varName, newValue) {
  const re = new RegExp(`(${varName.replace('--', '--')}:\\s*)([^;]+)(;)`, 'g');
  return html.replace(re, `$1${newValue}$3`);
}

// Tone words replacement — find the three tone-word divs
function replaceToneWords(html, words) {
  let count = 0;
  return html.replace(/<div class="tone-word">([^<]+)<\/div>/g, (match) => {
    if (count < words.length) {
      const replacement = `<div class="tone-word">${words[count]}</div>`;
      count++;
      return replacement;
    }
    return match;
  });
}

// Colorway note (appears twice in template — concept slide + identity slide)
function replaceColorwayNote(html, note) {
  return html.replace(/<div class="colorway-note">[^<]*<\/div>/g,
    `<div class="colorway-note">${note}</div>`);
}

// Concept note (appears once on S03 concept slide)
function replaceConceptNote(html, note) {
  return html.replace(/<div class="concept-note">[^<]*<\/div>/g,
    `<div class="concept-note">${note}</div>`);
}

let updated = 0;
let errors = 0;

for (const brand of BRANDS) {
  const filePath = resolve(DIR, brand.file);
  try {
    let html = readFileSync(filePath, 'utf8');

    // 1. Font import
    html = html.replace(FONT_LINK_RE,
      `<link href="${brand.fontImport}" rel="stylesheet">`);

    // 2. CSS variables
    for (const [varName, value] of Object.entries(brand.cssVars)) {
      html = replaceCSSVar(html, varName, value);
    }

    // 3. Tone words
    html = replaceToneWords(html, brand.toneWords);

    // 4. Colorway note (both occurrences)
    html = replaceColorwayNote(html, brand.colorwayNote);

    // 5. Concept note on S03
    html = replaceConceptNote(html, brand.colorwayNote);

    // Write updated file
    writeFileSync(filePath, html, 'utf8');
    console.log(`✓ ${brand.file} → ${brand.archetype}`);
    updated++;
  } catch (err) {
    console.error(`✗ ${brand.file}: ${err.message}`);
    errors++;
  }
}

console.log(`\nDone: ${updated} updated, ${errors} errors.`);
console.log('Note: Sthāna (Mark) was already most distinct — no changes needed.');
