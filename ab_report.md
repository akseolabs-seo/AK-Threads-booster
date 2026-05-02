# A/B Token-Cost Comparison Report

- Plugin root: `C:\Users\Kenneth\Claude\AK-Threads-booster`
- Working dir: `C:\Users\Kenneth\Claude\threads-personal`
- Token estimate: 3.0 chars/token (blended CJK+English)

## Per-skill comparison

| Skill | Before bytes | After bytes | Δ bytes | Δ tokens est | Reduction |
|-------|------|-------|---------|---------|-----------|
| analyze | 353,557 | 76,299 | 277,258 | 92,416 | 78.4% |
| predict | 345,713 | 68,455 | 277,258 | 92,416 | 80.2% |
| draft | 353,490 | 72,136 | 281,354 | 93,781 | 79.6% |
| review | 253,201 | 69,702 | 183,499 | 61,164 | 72.5% |
| topics | 243,602 | 67,145 | 176,457 | 58,817 | 72.4% |

## Grand total
- Before: **1,549,563 bytes** (~516,492 tokens)
- After:  **353,737 bytes** (~117,898 tokens)
- Reduction: **77.2%** (1,195,826 bytes, ~398,594 tokens)

## Per-file breakdown (analyze, before)

| File | Bytes | Tokens est |
|------|-------|------------|
| main_skill | 4,334 | 1,444 |
| analyze_skill | 14,989 | 4,996 |
| shared_principles | 2,794 | 931 |
| shared_discovery | 2,371 | 790 |
| shared_config | 3,959 | 1,319 |
| data_confidence | 3,478 | 1,159 |
| psychology_kb | 43,563 | 14,521 |
| algorithm_kb | 28,766 | 9,588 |
| ai_detection_kb | 28,472 | 9,490 |
| tracker_full | 167,951 | 55,983 |
| style_guide | 24,479 | 8,159 |
| concept_library | 12,887 | 4,295 |
| brand_voice | 15,514 | 5,171 |
