# Branding Pipeline

A modular Claude Code sub-agent orchestration framework for residential real estate project branding.

## What This Is

A 5-agent pipeline that takes a project brief and produces a complete Master Creative Brief — covering narrative architecture, brand identity, content strategy, marketing collaterals, and launch execution.

## Structure

```
pipeline/          ← Agent prompts (run these in sequence)
  00_orchestrator.md      Master orchestrator prompt
  01_narrative_architecture.md
  02_brand_creation.md
  03_content_experience.md
  04_marketing_collaterals.md
  05_prelaunch_launch.md
  06_consolidation.md

output/            ← Example output
  MASTER_CREATIVE_BRIEF_Virama_MyScapeBuilders.md

variables.md       ← Project brief variables reference
```

## How to Use

1. Fill in the 7 variables in `variables.md`
2. Run agents in sequence: 01 → 02 → 03 → 04 → 05
3. Pass each agent's output as context to the next
4. Run 06 consolidation to merge into one Master Creative Brief

Or invoke the Claude agent directly:
```
/agents → real-estate-branding-orchestrator
```

## Example Output

The `output/` folder contains the full Master Creative Brief for **Virāma by My Scape Builders** — a 12-villa ultra-luxury project inspired by Aman, Four Seasons, St. Regis, Binghatti, Sobha Realty, and Bvlgari Lighthouse Dubai.

~28,000 words across all 5 sections.

## Variables

| Variable | Example |
|---|---|
| PROJECT_NAME | Virāma |
| LOCATION | Prime residential enclave, Tier-1 India |
| TARGET_AUDIENCE | UHNI Indian families, NRI investors, 38–65 |
| PRICE_SEGMENT | ultra-luxury |
| USP | 12 exclusive private villas, no phase two |
| DEVELOPER_NAME | My Scape Builders |
| BRAND_TONE | Serene opulence — minimal in expression, maximal in experience |
