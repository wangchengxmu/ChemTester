---
id: ref.formula_determination
layer: 4
title: Reference — Formula Determination Rules
status: active
source_chapter: LibreTexts Chemistry 2e Ch03 (3.02)
last_verified: 2026-03-09
---

## Standard workflow
1. Convert mass/percent composition to moles for each element.
2. Normalize all moles by smallest value.
3. Integerize ratio set.
4. Reduce to simplest whole-number ratio (empirical formula).
5. If molecular molar mass given, compute multiplier `k = M_mol / M_emp`.

## Fraction-to-integer scaling hints
- ~0.50 -> ×2
- ~0.33 or ~0.67 -> ×3
- ~0.25 or ~0.75 -> ×4
- ~0.20, ~0.40, ~0.60, ~0.80 -> ×5

## Typical tolerance guidance
- Ratio integerization tolerance: ~±0.05 around near-integer targets.
- Molecular multiplier `k` should be near integer; if not, flag data quality/measurement error.

## Noisy-data notes
- Use an explicit basis (often 100 g) to simplify percent->mass mapping.
- Keep extra precision until final integerization decision.
- If multiple integerizations are plausible, report alternatives and required additional constraints.
