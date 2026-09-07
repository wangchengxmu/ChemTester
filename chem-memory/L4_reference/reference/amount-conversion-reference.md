---
id: ref.amount_conversion
layer: 4
title: Reference — Amount Conversion Constants & Rules
status: active
source_chapter: LibreTexts Chemistry 2e Ch03 (3.01)
last_verified: 2026-03-09
---

## Constants
- Avogadro constant: `N_A = 6.02214076 × 10^23 mol^-1`

## Core equation set
- `n = m / M`
- `m = nM`
- `N = nN_A`
- `n = N / N_A`

## Molar mass sourcing policy
- Use atomic masses from vetted periodic-table reference.
- For compounds, compute `M = Σ(ν_i A_i)` from formula subscripts.
- If formula ambiguity exists (hydrate, isotopic specification, ionic vs molecular form), resolve identity before conversion.

## Sig-fig quick rules
- Multiplication/division: keep least number of significant figures among inputs.
- Keep guard digits during intermediate calculations; round only final output.

## Validity checks
- Mass and molar mass must be positive.
- Particle count cannot be negative.
- Multi-step conversion should preserve dimensional consistency.
