"""
Virāma by SSquare — Brand Deck PDF Builder
Generates a self-contained HTML file with embedded images (base64)
Open in Chrome → Print → Save as PDF (A3 Landscape, no margins, background graphics ON)
"""

import base64, os, pathlib

IMG_DIR = pathlib.Path(r"C:\Users\Rohan\virama-site\images")

def b64(filename):
    path = IMG_DIR / filename
    if not path.exists():
        return ""
    ext = path.suffix.lower().lstrip(".")
    mime = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png"}.get(ext, "image/png")
    data = base64.b64encode(path.read_bytes()).decode()
    return f"data:{mime};base64,{data}"

imgs = {
    "hero":     b64("hero.png"),
    "pool":     b64("pool.png"),
    "interior": b64("interior.png"),
    "garden":   b64("garden.png"),
    "entrance": b64("entrance.png"),
    "aerial":   b64("aerial.png"),
    "v7":       b64("virama7.jpg"),
    "v8":       b64("virama8.png"),
    "v9":       b64("virama9.png"),
}

HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Virāma by SSquare — Brand Deck</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400;1,500&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
<style>
/* ─── RESET ──────────────────────────────────────── */
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

/* ─── PRINT CONFIG ───────────────────────────────── */
@page {{
  size: A3 landscape;
  margin: 0;
}}
@media print {{
  body {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
  .page {{ page-break-after: always; page-break-inside: avoid; }}
  .page:last-child {{ page-break-after: auto; }}
}}

/* ─── TOKENS ─────────────────────────────────────── */
:root {{
  --stone:    #2C2825;
  --basalt:   #1A1A18;
  --white:    #F5F1EC;
  --gold:     #C9A96E;
  --sand:     #E8DDD0;
  --green:    #3D4A3A;
  --stone-60: rgba(44,40,37,0.6);
  --white-60: rgba(245,241,236,0.6);
  --white-80: rgba(245,241,236,0.8);

  --serif: 'Cormorant Garamond', Georgia, serif;
  --sans:  'Inter', system-ui, sans-serif;

  /* A3 landscape = 420×297mm */
  --W: 420mm;
  --H: 297mm;
}}

/* ─── BASE PAGE ──────────────────────────────────── */
body {{ background: #111; }}

.page {{
  position: relative;
  width: var(--W);
  height: var(--H);
  overflow: hidden;
  display: block;
  margin: 0 auto 2mm;
}}

/* ─── FULL BLEED IMAGE ───────────────────────────── */
.bg {{
  position: absolute;
  inset: 0;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}}
.overlay-dark  {{ position:absolute;inset:0;background:linear-gradient(160deg,rgba(26,26,24,0.72)0%,rgba(26,26,24,0.42)55%,rgba(26,26,24,0.78)100%); }}
.overlay-left  {{ position:absolute;inset:0;background:linear-gradient(to right,rgba(26,26,24,0.92)0%,rgba(26,26,24,0.72)42%,transparent 100%); }}
.overlay-bottom{{ position:absolute;inset:0;background:linear-gradient(to top,rgba(26,26,24,0.95)0%,rgba(26,26,24,0.55)45%,transparent 100%); }}
.overlay-right {{ position:absolute;inset:0;background:linear-gradient(to left,rgba(26,26,24,0.9)0%,rgba(26,26,24,0.6)40%,transparent 100%); }}

/* ─── HAIRLINE ───────────────────────────────────── */
.rule {{
  display: block;
  width: 60mm;
  height: 0.3pt;
  background: var(--gold);
  margin: 3mm 0;
}}
.rule-short {{ width: 32mm; }}
.rule-full  {{ width: 100%; }}
.rule-white {{ background: rgba(245,241,236,0.35); }}

/* ─── TYPE UTILITIES ─────────────────────────────── */
.eyebrow {{
  font-family: var(--sans);
  font-size: 6.5pt;
  font-weight: 400;
  letter-spacing: 0.28em;
  text-transform: uppercase;
  color: var(--gold);
}}
.headline {{
  font-family: var(--serif);
  font-weight: 300;
  font-style: italic;
  color: var(--white);
  line-height: 1.15;
}}
.headline-dark {{ color: var(--stone); }}
.headline-gold {{ color: var(--gold); }}
.body-copy {{
  font-family: var(--serif);
  font-weight: 400;
  font-size: 10.5pt;
  line-height: 1.75;
  color: var(--white-80);
  letter-spacing: 0.015em;
}}
.body-dark {{ color: var(--stone-60); }}
.label {{
  font-family: var(--sans);
  font-size: 6pt;
  font-weight: 400;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: rgba(201,169,110,0.75);
}}
.label-dark {{ color: rgba(44,40,37,0.5); }}
.stat-num {{
  font-family: var(--serif);
  font-weight: 300;
  color: var(--stone);
  letter-spacing: -0.01em;
}}
.tagline-quote {{
  font-family: var(--serif);
  font-style: italic;
  font-weight: 300;
  color: var(--gold);
}}

/* ─── LAYOUT HELPERS ─────────────────────────────── */
.pad {{ padding: 18mm 20mm; }}
.pad-sm {{ padding: 14mm 16mm; }}
.col-left {{ position:absolute; left:18mm; top:0; bottom:0; width:130mm; display:flex; flex-direction:column; justify-content:center; }}
.col-right {{ position:absolute; right:18mm; top:0; bottom:0; width:130mm; display:flex; flex-direction:column; justify-content:center; text-align:right; }}
.bottom-left {{ position:absolute; left:18mm; bottom:16mm; }}
.bottom-right {{ position:absolute; right:18mm; bottom:16mm; text-align:right; }}
.top-left {{ position:absolute; left:18mm; top:16mm; }}
.center-block {{ position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; }}

/* ─── FACT CARDS ──────────────────────────────────── */
.fact-row {{
  display:flex;
  gap:4mm;
  margin-top: 8mm;
}}
.fact-card {{
  flex:1;
  background: var(--basalt);
  padding: 8mm 6mm;
  display:flex;
  flex-direction:column;
  align-items:center;
  gap: 3mm;
  text-align:center;
}}
.fact-num {{
  font-family: var(--serif);
  font-size: 32pt;
  font-weight: 300;
  color: var(--gold);
  line-height:1;
}}
.fact-label {{
  font-family: var(--sans);
  font-size: 6pt;
  letter-spacing:0.2em;
  text-transform:uppercase;
  color: rgba(245,241,236,0.5);
  line-height:1.4;
}}

/* ─── AMENITY GRID ────────────────────────────────── */
.amenity-grid {{
  position:absolute;
  right:0; top:0; bottom:0;
  width:190mm;
  display:grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 1fr 1fr 1fr;
  gap: 1.5mm;
}}
.amenity-cell {{
  background-size:cover;
  background-position:center;
  position:relative;
  overflow:hidden;
}}
.amenity-cell::after {{
  content:'';
  position:absolute;
  inset:0;
  background:linear-gradient(to top,rgba(26,26,24,0.75)0%,transparent 55%);
}}
.amenity-name {{
  position:absolute;
  bottom:4mm;
  left:5mm;
  z-index:2;
  font-family:var(--sans);
  font-size:6pt;
  letter-spacing:0.2em;
  text-transform:uppercase;
  color:var(--white-80);
}}

/* ─── GALLERY SPREAD ──────────────────────────────── */
.gallery-grid {{
  position:absolute;
  inset:0;
  display:grid;
  grid-template-columns: 2fr 1fr 1fr;
  grid-template-rows: 1fr 1fr;
  gap: 1.5mm;
}}
.gallery-cell {{ background-size:cover; background-position:center; }}
.gallery-cell.tall {{ grid-row: span 2; }}

/* ─── STATS TRIPTYCH ──────────────────────────────── */
.triptych {{
  display:flex;
  justify-content:center;
  gap: 20mm;
  margin-top: 12mm;
}}
.triptych-item {{
  display:flex;
  flex-direction:column;
  align-items:center;
  gap:2mm;
}}

/* ─── DIFF LIST ───────────────────────────────────── */
.diff-list {{
  list-style:none;
  margin-top:6mm;
  display:flex;
  flex-direction:column;
  gap:4mm;
}}
.diff-list li {{
  display:flex;
  align-items:flex-start;
  gap:4mm;
  font-family:var(--serif);
  font-size:10pt;
  color:var(--stone);
  line-height:1.55;
}}
.diff-list li::before {{
  content:'';
  display:block;
  flex-shrink:0;
  width:0.3pt;
  height:14mm;
  background:var(--gold);
  margin-top:1mm;
}}

/* ─── CHAPTER NUMBER ──────────────────────────────── */
.ch-num {{
  font-family:var(--serif);
  font-size:120pt;
  font-weight:300;
  color:rgba(201,169,110,0.08);
  line-height:1;
  position:absolute;
  right:16mm;
  bottom:-8mm;
  pointer-events:none;
}}

/* ─── CONTACT ROW ─────────────────────────────────── */
.contact-row {{
  display:flex;
  gap: 14mm;
  margin-top: 8mm;
}}
.contact-item {{
  display:flex;
  flex-direction:column;
  gap:1.5mm;
}}

</style>
</head>
<body>

<!-- ═══════════════════════════════════════════════════════════
     PAGE 01 — COVER
════════════════════════════════════════════════════════════ -->
<div class="page">
  <div class="bg" style="background-image:url('{imgs["hero"]}')"></div>
  <div class="overlay-dark"></div>
  <div class="center-block">
    <span class="eyebrow" style="margin-bottom:5mm;letter-spacing:0.4em;">A SSquare Development</span>
    <div class="rule" style="width:48mm;margin:0 auto 5mm;"></div>
    <h1 class="headline" style="font-size:88pt;letter-spacing:0.04em;color:var(--white);margin-bottom:3mm;">Virāma</h1>
    <p style="font-family:var(--serif);font-size:20pt;color:rgba(245,241,236,0.55);letter-spacing:0.25em;font-weight:300;margin-bottom:7mm;">विराम</p>
    <div class="rule" style="width:48mm;margin:0 auto 7mm;"></div>
    <p class="eyebrow" style="letter-spacing:0.35em;color:rgba(201,169,110,0.7);">Twelve Private Villas &nbsp;·&nbsp; Jubilee Hills &nbsp;·&nbsp; Hyderabad</p>
  </div>
  <div class="bottom-right">
    <p class="eyebrow" style="color:rgba(245,241,236,0.3);">Come Home to Quiet.</p>
  </div>
</div>

<!-- ═══════════════════════════════════════════════════════════
     PAGE 02 — THE PAUSE (Philosophy)
════════════════════════════════════════════════════════════ -->
<div class="page" style="background:var(--white);">
  <div class="col-left" style="left:22mm;width:115mm;">
    <span class="eyebrow label-dark" style="margin-bottom:5mm;">Virāma &nbsp;·&nbsp; विराम</span>
    <div class="rule" style="background:var(--gold);"></div>
    <h2 class="headline headline-dark" style="font-size:38pt;margin-top:5mm;margin-bottom:8mm;">The word does not<br>mean stop.<br><em style="color:var(--stone);">It means the breath between.</em></h2>
    <p class="body-copy body-dark" style="font-size:11pt;">In Sanskrit, virāma is the pause that gives a phrase its meaning. Not silence as absence — silence as presence.</p>
    <p class="body-copy body-dark" style="font-size:11pt;margin-top:4mm;">We named this place after that idea. Twelve homes built not around what fills them, but around what they let go of.</p>
    <div class="rule rule-short" style="margin-top:10mm;"></div>
    <p class="tagline-quote" style="font-size:16pt;margin-top:3mm;">"Come Home to Quiet."</p>
  </div>
  <!-- right image -->
  <div style="position:absolute;right:0;top:0;bottom:0;width:185mm;">
    <div class="bg" style="background-image:url('{imgs["v9"]}');inset:0;position:absolute;"></div>
    <div style="position:absolute;inset:0;background:linear-gradient(to right,rgba(245,241,236,1)0%,rgba(245,241,236,0.3)30%,transparent 55%);"></div>
  </div>
</div>

<!-- ═══════════════════════════════════════════════════════════
     PAGE 03 — SSQUARE 35 YEARS
════════════════════════════════════════════════════════════ -->
<div class="page" style="background:var(--white);">
  <div style="position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;padding:0 22mm;">
    <span class="eyebrow label-dark" style="margin-bottom:5mm;">The Developer</span>
    <div class="rule" style="background:var(--gold);margin-bottom:6mm;"></div>
    <h2 class="headline headline-dark" style="font-size:42pt;max-width:280mm;margin-bottom:8mm;">Thirty-five years of building<br>things that last.</h2>
    <p class="body-copy body-dark" style="max-width:200mm;font-size:11pt;">SSquare was founded in 1991. Since then, we have developed over ten million square feet of premium commercial real estate across Hyderabad. We have never built for volume. We have built to a standard.</p>
    <p class="body-copy body-dark" style="max-width:200mm;font-size:11pt;margin-top:4mm;">Virāma is our first residential work — and it will be our definitive one.</p>

    <div class="triptych" style="justify-content:flex-start;gap:24mm;margin-top:14mm;">
      <div class="triptych-item" style="align-items:flex-start;">
        <span class="stat-num" style="font-size:52pt;">35</span>
        <div class="rule rule-short" style="margin:0;width:24mm;"></div>
        <span class="label label-dark" style="margin-top:2mm;">Years in Hyderabad</span>
      </div>
      <div class="triptych-item" style="align-items:flex-start;">
        <span class="stat-num" style="font-size:52pt;">10M+</span>
        <div class="rule rule-short" style="margin:0;width:24mm;"></div>
        <span class="label label-dark" style="margin-top:2mm;">Sq ft delivered</span>
      </div>
      <div class="triptych-item" style="align-items:flex-start;">
        <span class="stat-num" style="font-size:52pt;">1</span>
        <div class="rule rule-short" style="margin:0;width:24mm;"></div>
        <span class="label label-dark" style="margin-top:2mm;">Residential debut</span>
      </div>
    </div>

    <div class="rule" style="margin-top:14mm;width:90mm;"></div>
    <p class="tagline-quote" style="font-size:15pt;margin-top:4mm;">"The Standard, Privately Held."</p>
  </div>
  <div class="ch-num">03</div>
</div>

<!-- ═══════════════════════════════════════════════════════════
     PAGE 04 — THE ESTATE (Key Facts)
════════════════════════════════════════════════════════════ -->
<div class="page" style="background:var(--sand);">
  <div style="position:absolute;left:22mm;top:0;bottom:0;width:165mm;display:flex;flex-direction:column;justify-content:center;">
    <span class="eyebrow label-dark" style="margin-bottom:5mm;">The Estate</span>
    <div class="rule" style="margin-bottom:6mm;"></div>
    <h2 class="headline headline-dark" style="font-size:52pt;line-height:1.05;margin-bottom:8mm;">Twelve.<br>No more.</h2>
    <p class="body-copy body-dark" style="font-size:11pt;max-width:140mm;">A gated estate of twelve private villas. Each home has its own pool, its own forecourt, its own silence. The Green Circuit — a continuous landscape corridor — connects them without crowding them. This is not a development. It is a private enclave.</p>

    <div class="fact-row" style="margin-top:10mm;">
      <div class="fact-card">
        <span class="fact-num">12</span>
        <span class="fact-label">Private Villas</span>
      </div>
      <div class="fact-card">
        <span class="fact-num">1</span>
        <span class="fact-label">Gate · One Entry</span>
      </div>
      <div class="fact-card">
        <span class="fact-num" style="font-size:24pt;">400m</span>
        <span class="fact-label">The Green Circuit</span>
      </div>
      <div class="fact-card">
        <span class="fact-num" style="font-size:18pt;">Rs 13–20 Cr</span>
        <span class="fact-label">Price Range</span>
      </div>
    </div>
  </div>
  <!-- right aerial image -->
  <div style="position:absolute;right:0;top:0;bottom:0;width:175mm;">
    <div class="bg" style="background-image:url('{imgs["aerial"]}');"></div>
    <div style="position:absolute;inset:0;background:linear-gradient(to right,var(--sand)0%,rgba(232,221,208,0.4)22%,transparent 45%);"></div>
  </div>
  <div class="ch-num" style="color:rgba(44,40,37,0.05);">04</div>
</div>

<!-- ═══════════════════════════════════════════════════════════
     PAGE 05 — ARCHITECTURE LANGUAGE
════════════════════════════════════════════════════════════ -->
<div class="page">
  <div class="bg" style="background-image:url('{imgs["entrance"]}')"></div>
  <div class="overlay-right"></div>
  <div class="col-right" style="right:20mm;width:140mm;">
    <span class="eyebrow" style="margin-bottom:5mm;text-align:right;">Architecture</span>
    <div class="rule rule-short" style="margin-left:auto;margin-bottom:6mm;"></div>
    <h2 class="headline" style="font-size:38pt;text-align:right;margin-bottom:8mm;">Stone, glass, and<br>the discipline<br>of restraint.</h2>
    <p class="body-copy" style="text-align:right;font-size:10.5pt;">Single storey. Honed limestone walls. Dark basalt at the base. A cantilevered roof that extends the interior into the landscape. Floor-to-ceiling glazing that disappears at dusk.</p>
    <p class="body-copy" style="text-align:right;font-size:10.5pt;margin-top:4mm;">A teak pivot door that announces arrival without announcing itself. Every material chosen for how it weathers.</p>

    <div style="margin-top:9mm;text-align:right;">
      <div style="display:inline-flex;gap:6mm;flex-wrap:wrap;justify-content:flex-end;">
        {"".join(f'<span style="font-family:var(--sans);font-size:6pt;letter-spacing:0.18em;text-transform:uppercase;color:var(--gold);border:0.3pt solid rgba(201,169,110,0.4);padding:2mm 3.5mm;">{m}</span>' for m in ["Honed Limestone","Dark Basalt","Teak Pivot Door","Cantilevered Roof","Floor-to-Ceiling Glazing"])}
      </div>
    </div>
  </div>
</div>

<!-- ═══════════════════════════════════════════════════════════
     PAGE 06 — THE VILLA (Interior)
════════════════════════════════════════════════════════════ -->
<div class="page">
  <div class="bg" style="background-image:url('{imgs["interior"]}')"></div>
  <div class="overlay-bottom"></div>
  <div class="bottom-left" style="bottom:18mm;max-width:220mm;">
    <span class="eyebrow" style="margin-bottom:4mm;">The Villa</span>
    <div class="rule rule-short" style="margin-bottom:5mm;"></div>
    <h2 class="headline" style="font-size:42pt;margin-bottom:6mm;">A home that knows<br>when to step back.</h2>
    <p class="body-copy" style="font-size:10.5pt;max-width:180mm;">The living spaces open fully to the outdoors. Bedrooms face the pool. The kitchen faces the garden. The roof is a horizontal plane that makes the sky feel deliberately framed. Living here is an act of attention.</p>
  </div>
</div>

<!-- ═══════════════════════════════════════════════════════════
     PAGE 07 — PRIVATE POOL
════════════════════════════════════════════════════════════ -->
<div class="page">
  <div class="bg" style="background-image:url('{imgs["pool"]}')"></div>
  <div class="overlay-dark" style="background:linear-gradient(160deg,rgba(26,26,24,0.6)0%,rgba(26,26,24,0.25)50%,rgba(26,26,24,0.75)100%);"></div>
  <div class="bottom-left" style="bottom:20mm;">
    <span class="eyebrow" style="margin-bottom:5mm;">Private Pool</span>
    <div class="rule" style="width:40mm;margin-bottom:5mm;"></div>
    <h2 class="headline" style="font-size:64pt;letter-spacing:0.02em;line-height:1.05;">Yours.<br>Only yours.</h2>
  </div>
  <div class="bottom-right" style="bottom:20mm;max-width:150mm;">
    <p class="body-copy" style="text-align:right;font-size:10.5pt;">Each villa at Virāma holds its own body of water — a private infinity pool set flush with the landscape. Not a shared amenity accessed by schedule. Yours, always, at any hour, in complete silence.</p>
  </div>
</div>

<!-- ═══════════════════════════════════════════════════════════
     PAGE 08 — THE GREEN CIRCUIT
════════════════════════════════════════════════════════════ -->
<div class="page">
  <div class="bg" style="background-image:url('{imgs["garden"]}')"></div>
  <div style="position:absolute;inset:0;background:linear-gradient(160deg,rgba(61,74,58,0.82)0%,rgba(26,26,24,0.55)55%,rgba(26,26,24,0.7)100%);"></div>
  <div class="col-left" style="left:22mm;width:155mm;">
    <span class="eyebrow" style="margin-bottom:5mm;">The Green Circuit</span>
    <div class="rule" style="margin-bottom:6mm;"></div>
    <h2 class="headline" style="font-size:40pt;margin-bottom:8mm;">Native trees.<br>Continuous ground.<br>No fences between.</h2>
    <p class="body-copy" style="font-size:10.5pt;max-width:135mm;">The Green Circuit is a 400-metre landscaped loop linking all twelve villas through the estate's living fabric — through grove, courtyard, garden, and back. Named at the outset of the master plan. Treated as infrastructure, not afterthought.</p>
    <p class="body-copy" style="font-size:10.5pt;max-width:135mm;margin-top:4mm;">You are not separated from your neighbours by walls. <em>You are separated by garden.</em></p>
  </div>
</div>

<!-- ═══════════════════════════════════════════════════════════
     PAGE 09 — ARRIVAL
════════════════════════════════════════════════════════════ -->
<div class="page" style="background:var(--basalt);">
  <!-- left image -->
  <div style="position:absolute;left:0;top:0;bottom:0;width:190mm;">
    <div class="bg" style="background-image:url('{imgs["v7"]}');"></div>
    <div style="position:absolute;inset:0;background:linear-gradient(to left,var(--basalt)0%,rgba(26,26,24,0.4)35%,transparent 60%);"></div>
  </div>
  <div class="col-right" style="right:20mm;width:145mm;">
    <span class="eyebrow" style="text-align:right;margin-bottom:5mm;">Arrival</span>
    <div class="rule rule-short" style="margin-left:auto;margin-bottom:6mm;"></div>
    <h2 class="headline" style="font-size:38pt;text-align:right;margin-bottom:8mm;">The door is the first<br>thing you understand.</h2>
    <p class="body-copy" style="text-align:right;font-size:10.5pt;">A teak pivot door, floor-to-ceiling, set in a deep limestone reveal. The forecourt is quiet — no waterfalls, no statement planting. Basalt stepping stones across pale gravel.</p>
    <p class="body-copy" style="text-align:right;font-size:10.5pt;margin-top:4mm;font-style:italic;">You are not announced. You simply come home.</p>
  </div>
</div>

<!-- ═══════════════════════════════════════════════════════════
     PAGE 10 — GALLERY SPREAD (all 9 images)
════════════════════════════════════════════════════════════ -->
<div class="page">
  <div class="gallery-grid">
    <div class="gallery-cell tall" style="background-image:url('{imgs["hero"]}');background-size:cover;background-position:center;"></div>
    <div class="gallery-cell" style="background-image:url('{imgs["pool"]}');background-size:cover;background-position:center;"></div>
    <div class="gallery-cell" style="background-image:url('{imgs["interior"]}');background-size:cover;background-position:center;"></div>
    <div class="gallery-cell" style="background-image:url('{imgs["garden"]}');background-size:cover;background-position:center;"></div>
    <div class="gallery-cell" style="background-image:url('{imgs["entrance"]}');background-size:cover;background-position:center;"></div>
  </div>
  <div style="position:absolute;inset:0;background:linear-gradient(to bottom,rgba(26,26,24,0.4)0%,transparent 25%,transparent 70%,rgba(26,26,24,0.6)100%);pointer-events:none;"></div>
  <div class="top-left" style="top:14mm;">
    <span class="eyebrow" style="letter-spacing:0.35em;">The Address</span>
  </div>
  <div class="bottom-left" style="bottom:14mm;">
    <p class="headline" style="font-size:28pt;">Visual Record</p>
  </div>
</div>

<!-- ═══════════════════════════════════════════════════════════
     PAGE 11 — GALLERY SPREAD 2 (remaining images)
════════════════════════════════════════════════════════════ -->
<div class="page">
  <div style="position:absolute;inset:0;display:grid;grid-template-columns:2fr 1fr 1fr;grid-template-rows:1fr 1fr;gap:1.5mm;">
    <div style="grid-row:span 2;background-image:url('{imgs["v8"]}');background-size:cover;background-position:center;"></div>
    <div style="background-image:url('{imgs["v9"]}');background-size:cover;background-position:center;"></div>
    <div style="background-image:url('{imgs["aerial"]}');background-size:cover;background-position:center;"></div>
    <div style="background-image:url('{imgs["v7"]}');background-size:cover;background-position:center;"></div>
    <div style="background-image:url('{imgs["garden"]}');background-size:cover;background-position:center;"></div>
  </div>
  <div style="position:absolute;inset:0;background:linear-gradient(to bottom,rgba(26,26,24,0.45)0%,transparent 20%,transparent 75%,rgba(26,26,24,0.55)100%);pointer-events:none;"></div>
  <div class="bottom-right" style="bottom:14mm;">
    <span class="eyebrow" style="color:rgba(245,241,236,0.4);">Prashashan Nagar · Jubilee Hills</span>
  </div>
</div>

<!-- ═══════════════════════════════════════════════════════════
     PAGE 12 — AMENITIES
════════════════════════════════════════════════════════════ -->
<div class="page" style="background:var(--basalt);">
  <!-- Left copy -->
  <div style="position:absolute;left:22mm;top:0;bottom:0;width:140mm;display:flex;flex-direction:column;justify-content:center;">
    <span class="eyebrow" style="margin-bottom:5mm;">The Amenities</span>
    <div class="rule" style="margin-bottom:6mm;"></div>
    <h2 class="headline" style="font-size:36pt;margin-bottom:9mm;">Where silence<br>becomes structure.</h2>
    <div style="display:flex;flex-direction:column;gap:5mm;">
      {"".join(f'''<div style="display:flex;flex-direction:column;gap:1.5mm;">
        <span style="font-family:var(--serif);font-size:10pt;color:var(--gold);font-style:italic;">{name}</span>
        <span class="body-copy" style="font-size:9.5pt;">{desc}</span>
      </div>''' for name, desc in [
        ("The Still Water", "A private infinity pool with each villa. Yours alone, at any hour."),
        ("The Root System", "Mature trees, gravel paths, an unbroken chain of shade."),
        ("The Green Circuit", "A 400m landscaped loop connecting all twelve villas."),
        ("The Gathering Stone", "One pavilion. Open on three sides. A long table, good light."),
        ("The Quiet Body", "A wellness courtyard — enclosed basalt, open to garden."),
        ("The First Breath", "An arrival forecourt designed to shed the outside world."),
      ])}
    </div>
  </div>
  <!-- Right amenity grid -->
  <div class="amenity-grid">
    <div class="amenity-cell" style="background-image:url('{imgs["pool"]}');">
      <span class="amenity-name">Private Pool</span>
    </div>
    <div class="amenity-cell" style="background-image:url('{imgs["interior"]}');">
      <span class="amenity-name">The Villa</span>
    </div>
    <div class="amenity-cell" style="background-image:url('{imgs["aerial"]}');">
      <span class="amenity-name">The Estate</span>
    </div>
    <div class="amenity-cell" style="background-image:url('{imgs["garden"]}');">
      <span class="amenity-name">The Green Circuit</span>
    </div>
    <div class="amenity-cell" style="background-image:url('{imgs["entrance"]}');">
      <span class="amenity-name">Arrival</span>
    </div>
    <div class="amenity-cell" style="background-image:url('{imgs["v8"]}');">
      <span class="amenity-name">The Pavilion</span>
    </div>
  </div>
</div>

<!-- ═══════════════════════════════════════════════════════════
     PAGE 13 — DIFFERENTIATION
════════════════════════════════════════════════════════════ -->
<div class="page" style="background:var(--white);">
  <div style="position:absolute;inset:0;padding:16mm 22mm;display:flex;flex-direction:column;justify-content:center;">
    <span class="eyebrow label-dark" style="margin-bottom:5mm;">Why Virāma</span>
    <div class="rule" style="margin-bottom:8mm;"></div>
    <h2 class="headline headline-dark" style="font-size:36pt;max-width:250mm;margin-bottom:10mm;">What sets it apart<br>from every other<br>Jubilee Hills address.</h2>
    <ul class="diff-list">
      <li>The only gated villa estate in Jubilee Hills where no two homes share a wall, a view, or a pool. Privacy is the fundamental unit of the plan.</li>
      <li>SSquare has delivered 10M+ sq ft without ever entering the residential market. Virāma is the singular exception — which means twelve families acquire something never replicated.</li>
      <li>Every villa sits on a single storey — not as constraint but conviction. Horizontal living means the landscape is always in frame, the sky always present.</li>
      <li>The estate carries no commercial tenancy, no retail podium, no hotel-style lobby. What passes through the gate belongs here. Everyone else does not.</li>
      <li>The architecture references Aman Amanyara and Amangiri — not what has been built in Hyderabad before. The result is a project that does not compete with its neighbours because it is not in the same conversation.</li>
    </ul>
  </div>
  <div class="ch-num" style="color:rgba(44,40,37,0.04);">13</div>
</div>

<!-- ═══════════════════════════════════════════════════════════
     PAGE 14 — LOCATION
════════════════════════════════════════════════════════════ -->
<div class="page" style="background:var(--basalt);">
  <div class="bg" style="background-image:url('{imgs["v9"]}');opacity:0.22;"></div>
  <div style="position:absolute;inset:0;background:rgba(26,26,24,0.65);"></div>
  <div style="position:absolute;left:22mm;top:0;bottom:0;width:155mm;display:flex;flex-direction:column;justify-content:center;">
    <span class="eyebrow" style="margin-bottom:5mm;">The Location</span>
    <div class="rule" style="margin-bottom:6mm;"></div>
    <h2 class="headline" style="font-size:38pt;margin-bottom:8mm;">Where Hyderabad's hills<br>meet their quietest road.</h2>
    <p class="body-copy" style="font-size:10.5pt;max-width:140mm;margin-bottom:8mm;">Prashashan Nagar — known locally as Malibu. No through traffic. A deep canopy. The particular calm of a place that has never needed to prove itself.</p>

    <div style="display:flex;flex-direction:column;gap:3.5mm;">
      {"".join(f'<div style="display:flex;align-items:baseline;gap:5mm;"><span style="font-family:var(--serif);font-size:18pt;font-style:italic;color:var(--gold);min-width:18mm;">{t}</span><span style="font-family:var(--sans);font-size:7.5pt;letter-spacing:0.15em;text-transform:uppercase;color:rgba(245,241,236,0.65);">{d}</span></div>' for t, d in [("4 min","Jubilee Hills Club"),("8 min","Banjara Hills Road No. 12"),("10 min","KBR National Park"),("10 min","HITECH City Corridor"),("18 min","Financial District")])}
    </div>
  </div>
  <div style="position:absolute;right:20mm;top:0;bottom:0;width:145mm;display:flex;flex-direction:column;justify-content:center;gap:4mm;">
    <div style="border:0.3pt solid rgba(201,169,110,0.3);padding:9mm;background:rgba(26,26,24,0.6);">
      <p class="eyebrow" style="margin-bottom:3mm;">Neighbourhood Profile</p>
      {"".join(f'<p class="body-copy" style="font-size:9.5pt;margin-bottom:2mm;">· {note}</p>' for note in ["No through traffic · Dead-end residential street","Mature rain tree and neem canopy throughout","Established UHNI residential pocket since 1980s","Five minutes from Film Nagar · Ten from HITECH City","Locally known as 'Malibu' — a neighbourhood that needs no introduction"])}
    </div>
  </div>
</div>

<!-- ═══════════════════════════════════════════════════════════
     PAGE 15 — BRAND VOICE + COPY
════════════════════════════════════════════════════════════ -->
<div class="page" style="background:var(--sand);">
  <div style="position:absolute;inset:0;padding:16mm 22mm;display:flex;gap:16mm;">
    <!-- Left: voice rules -->
    <div style="flex:1;display:flex;flex-direction:column;justify-content:center;">
      <span class="eyebrow label-dark" style="margin-bottom:5mm;">Brand Voice</span>
      <div class="rule" style="margin-bottom:6mm;"></div>
      <h2 class="headline headline-dark" style="font-size:28pt;margin-bottom:8mm;">Five rules.<br>No exceptions.</h2>
      <div style="display:flex;flex-direction:column;gap:5mm;">
        {"".join(f'<div style="border-left:0.3pt solid var(--gold);padding-left:4mm;"><p style="font-family:var(--serif);font-size:9pt;color:var(--stone);line-height:1.6;"><strong style="font-weight:500;">{rule}</strong></p></div>' for rule in ["The product does not need adjectives. Describe what exists. What exists is sufficient.","Write for the person who has stopped being impressed. Speak to their fatigue, not their ambition.","Short lines earn more trust than long ones. Every headline should hold in a half-page of white space.","Specificity over grandeur. A pivot door of solid teak lands harder than a dramatic entrance experience.","Never explain the brand — embody it. The copy enacts serenity through rhythm, restraint, and negative space."])}
      </div>
    </div>
    <!-- Right: social copy sample -->
    <div style="flex:1;display:flex;flex-direction:column;justify-content:center;">
      <span class="eyebrow label-dark" style="margin-bottom:5mm;">Launch Copy · Sample</span>
      <div class="rule" style="margin-bottom:6mm;"></div>
      <div style="background:var(--basalt);padding:8mm;margin-bottom:5mm;">
        <p style="font-family:var(--serif);font-size:10.5pt;color:rgba(245,241,236,0.85);line-height:1.7;font-style:italic;">"Some addresses in this city are spoken quietly, if they're spoken at all. The ones where the gate has stayed the same for twenty years. Where the trees grew in before the roads were named."</p>
        <p style="font-family:var(--sans);font-size:6pt;letter-spacing:0.18em;text-transform:uppercase;color:var(--gold);margin-top:4mm;">Day 1 · Instagram · Curiosity Teaser</p>
      </div>
      <div style="background:var(--basalt);padding:8mm;">
        <p style="font-family:var(--serif);font-size:10.5pt;color:rgba(245,241,236,0.85);line-height:1.7;font-style:italic;">"SSquare has spent thirty-five years building the environments in which Hyderabad does its most consequential work. Virāma is the first time we have built for the people who do that work."</p>
        <p style="font-family:var(--sans);font-size:6pt;letter-spacing:0.18em;text-transform:uppercase;color:var(--gold);margin-top:4mm;">Press Note · Opening Quote</p>
      </div>
    </div>
  </div>
  <div class="ch-num" style="color:rgba(44,40,37,0.04);">15</div>
</div>

<!-- ═══════════════════════════════════════════════════════════
     PAGE 16 — CLOSE · COME HOME TO QUIET
════════════════════════════════════════════════════════════ -->
<div class="page">
  <div class="bg" style="background-image:url('{imgs["v8"]}')"></div>
  <div style="position:absolute;inset:0;background:linear-gradient(160deg,rgba(26,26,24,0.75)0%,rgba(26,26,24,0.45)50%,rgba(26,26,24,0.8)100%);"></div>
  <div class="center-block">
    <p class="eyebrow" style="margin-bottom:7mm;letter-spacing:0.3em;color:rgba(201,169,110,0.6);">Virāma by SSquare</p>
    <div class="rule" style="width:40mm;margin:0 auto 8mm;"></div>
    <h2 class="headline" style="font-size:78pt;letter-spacing:0.02em;">Come home to quiet.</h2>
    <div class="rule" style="width:40mm;margin:8mm auto 0;"></div>
  </div>
  <div class="bottom-left" style="bottom:18mm;">
    <p class="eyebrow" style="color:rgba(245,241,236,0.3);">Prashashan Nagar · Jubilee Hills · Hyderabad</p>
  </div>
  <div class="bottom-right" style="bottom:18mm;">
    <p class="eyebrow" style="color:rgba(245,241,236,0.3);">"The Standard, Privately Held."</p>
  </div>
</div>

<!-- ═══════════════════════════════════════════════════════════
     PAGE 17 — BACK COVER / CONTACT
════════════════════════════════════════════════════════════ -->
<div class="page" style="background:var(--stone);">
  <div style="position:absolute;inset:0;background:radial-gradient(ellipse at 30% 50%,rgba(201,169,110,0.06)0%,transparent 65%);"></div>
  <div style="position:absolute;left:22mm;top:0;bottom:0;width:160mm;display:flex;flex-direction:column;justify-content:center;">
    <h1 class="headline" style="font-size:64pt;letter-spacing:0.04em;margin-bottom:3mm;">Virāma</h1>
    <p style="font-family:var(--serif);font-size:20pt;color:rgba(245,241,236,0.45);letter-spacing:0.25em;margin-bottom:10mm;">विराम</p>
    <div class="rule" style="width:52mm;margin-bottom:10mm;"></div>

    <div class="contact-row">
      <div class="contact-item">
        <span class="label" style="color:rgba(201,169,110,0.65);">Sales Enquiries</span>
        <span class="body-copy" style="font-size:10pt;">[Phone number]</span>
        <span class="body-copy" style="font-size:10pt;">[Email address]</span>
      </div>
      <div class="contact-item">
        <span class="label" style="color:rgba(201,169,110,0.65);">Site Visits</span>
        <span class="body-copy" style="font-size:10pt;">By appointment only</span>
        <span class="body-copy" style="font-size:10pt;">Jubilee Hills, Hyderabad</span>
      </div>
      <div class="contact-item">
        <span class="label" style="color:rgba(201,169,110,0.65);">Developer</span>
        <span class="body-copy" style="font-size:10pt;">SSquare · Est. 1991</span>
        <span class="body-copy" style="font-size:10pt;font-style:italic;color:var(--gold);">"The Standard, Privately Held."</span>
      </div>
    </div>

    <div style="margin-top:12mm;">
      <p style="font-family:var(--sans);font-size:6pt;letter-spacing:0.2em;text-transform:uppercase;color:rgba(245,241,236,0.25);">All enquiries held in complete confidence · SSquare does not share its client list</p>
    </div>
  </div>
  <!-- Right: large S² watermark -->
  <div style="position:absolute;right:-10mm;top:50%;transform:translateY(-50%);font-family:var(--serif);font-size:280pt;font-weight:300;color:rgba(245,241,236,0.03);line-height:1;pointer-events:none;user-select:none;">S²</div>
</div>

</body>
</html>"""

out = r"C:\Users\Rohan\branding-pipeline\projects\virama\execution\Virama_Brand_Deck.html"
with open(out, "w", encoding="utf-8") as f:
    f.write(HTML)
print(f"Saved: {out}")
print(f"Size: {len(HTML)/1024:.0f} KB")
print("Open in Chrome → Ctrl+P → Save as PDF")
print("Settings: A3 Landscape, Margins: None, Background graphics: ON")
