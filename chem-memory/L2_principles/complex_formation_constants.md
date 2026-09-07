---
id: complex_formation_constants
layer: 2
title: Complex Formation Constants and Chelate Effect
source: Bertini et al. Bioinorganic Chemistry; Miessler & Tarr Inorganic Chemistry Ch9
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - ../L4_reference/formation_constant_reference.md
cross_links:
  - ./chemical_equilibrium.md
  - ../L1_ontology/chemistry-core-map.md
status: active
---

## Problem intent
Route problems involving formation constants (Kf, β), stepwise constants, chelate effect, and stability comparisons between complexes.

## Canonical equations
- Overall formation constant: βₙ = [MLₙ]/([M][L]ⁿ)
- Stepwise constants: K₁ = [ML]/([M][L]), K₂ = [ML₂]/([ML][L]), ...
- βₙ = K₁ × K₂ × ... × Kₙ
- Free metal: [M]free ≈ [M]tot / (βₙ × [L]ⁿ) when βₙ is large
- Per-donor effective constant: K_eff ≈ βₙ^(1/n) for n-dentate ligand

## Key concepts

### Chelate effect
Multidentate ligands (chelates) form much more stable complexes than equivalent monodentate ligands.
- Entropic advantage: one chelation reaction releases more particles than multiple single ligand exchanges
- Example: [Fe(en)₃]³⁺ (β₃ ≈ 10²¹) vs [Fe(NH₃)₆]³⁺ (β₆ ≈ 10⁸) — 6 N-donors but chelate is far stronger
- Effective per-donor: en ≈ 10⁷ vs NH₃ ≈ 10¹·³

### Stepwise vs overall constants
- Stepwise constants Kᵢ typically decrease: K₁ > K₂ > K₃ (statistical + electrostatic)
- Overall constant βₙ accumulates: always larger than any individual Kᵢ

### Comparing complex stability
- Compare log K or log β values
- For different denticities, compare per-donor effective constants
- Account for factors: charge, size, Irving-Williams series, hard/soft acid-base

## Decision stub
1. Given βₙ → find [M]free: use [M]free ≈ [M]tot / (βₙ × [L]ⁿ) for large β
2. Compare complexes → compare β values; if different denticity, compute K_eff = β^(1/n)
3. Relate stepwise to overall: β = product of Kᵢ
4. Chelate vs monodentate: same donor atoms → compare β; chelate wins by entropy
