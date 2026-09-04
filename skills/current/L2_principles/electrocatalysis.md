---
id: electrocatalysis
layer: 2
title: Electrocatalysis (HER, OER, ORR, Overpotential, Tafel Plots)
parent: ../L1_ontology/chemistry-core-map.md#entry-273
stability: high
confidence: high
last_verified: 2026-03-24
source: Physical Chemistry (LibreTexts), electrochemistry literature
---

# Electrocatalysis

## Core Concept

Electrocatalysis accelerates electrode reactions (HER, OER, ORR) by lowering the activation barrier, directly impacting the efficiency of fuel cells, electrolyzers, and metal-air batteries.

---

## Key Electrochemical Reactions

### Hydrogen Evolution Reaction (HER)
**Acidic:** 2H⁺ + 2e⁻ → H₂  (E° = 0 V)
**Alkaline:** 2H₂O + 2e⁻ → H₂ + 2OH⁻  (E° = -0.83 V)

**Mechanism (Volmer-Heyrovsky-Tafel):**
1. Volmer: H⁺ + e⁻ → H* (adsorption)
2. Heyrovsky: H* + H⁺ + e⁻ → H₂ (electrochemical desorption)
3. Tafel: 2H* → H₂ (chemical recombination)

### Oxygen Evolution Reaction (OER)
**Acidic:** 2H₂O → O₂ + 4H⁺ + 4e⁻  (E° = 1.23 V)
**Alkaline:** 4OH⁻ → O₂ + 2H₂O + 4e⁻  (E° = 0.40 V)

**4-electron process — high overpotential due to complex mechanism**

### Oxygen Reduction Reaction (ORR)
**Acidic:** O₂ + 4H⁺ + 4e⁻ → 2H₂O  (E° = 1.23 V)
**Alkaline:** O₂ + 2H₂O + 4e⁻ → 4OH⁻  (E° = 0.40 V)

**Desired: 4e⁻ pathway (direct to H₂O). Undesired: 2e⁻ → H₂O₂ (peroxide)**

---

## Overpotential

$$\eta = E_{applied} - E_{equilibrium}$$

The extra voltage beyond thermodynamic requirement to achieve a given current density.

### Benchmark overpotentials at 10 mA/cm²
| Reaction | Pt | IrO₂/RuO₂ | Best non-PGM |
|----------|-----|-----------|-------------|
| HER | ~30 mV | — | MoS₂ (~150 mV) |
| OER | — | ~300 mV | NiFe-LDH (~300 mV) |
| ORR | ~50 mV | — | Fe-N-C (~400 mV) |

---

## Tafel Equation & Tafel Plot

$$\eta = a + b \log |j|$$

Where:
- a = Tafel intercept (related to exchange current density)
- b = Tafel slope (mV/decade) — reveals mechanism

$$b = \frac{2.303 RT}{\alpha nF}$$

### Tafel Slope Interpretation
- **Low b** → better catalyst (less voltage increase per decade of current)
- b ≈ 120 mV/dec → RDS is first electron transfer (α ≈ 0.5, n = 1)
- b ≈ 60 mV/dec → chemical step after fast electron transfer
- b ≈ 40 mV/dec → RDS is second electron transfer (α ≈ 0.5, n = 2)

---

## Exchange Current Density (j₀)

$$j_0 = nFk_0[C]^{(1-\alpha)}$$

Higher j₀ = more facile reaction = better catalyst.

---

## Source Context & Cross-References
- Physical Chemistry (LibreTexts) Ch29.8 covers catalyst effects on mechanism and activation energy
- LibreTexts Catalysis Module covers heterogeneous catalysis fundamentals applicable to electrocatalysis
- Cross-reference: `surface_adsorption.md` for Langmuir-Hinshelwood and Eley-Rideal mechanisms
- Cross-reference: `fuel_cells.md` for Pt-catalyzed electrochemical reactions
- Cross-reference: `battery_fundamentals.md` for electrode thermodynamics
- Key topic: ORR/OER/HER catalysts (Pt, Ir, Ni, Co-based) - primarily research literature

---

## Links

- L3: `../L3_functions/advanced_electrochemistry_tools.py`
- L4: `../L4_reference/electrochemistry_reference.csv`

---

## [Source: Wikipedia, Electrocatalysis]
### Key Electrocatalytic Reactions

| Reaction | Thermodynamic Potential (V vs RHE) | Best Catalyst | Tafel Slope |
|---|---|---|---|
| HER | 0.00 | Pt/C (η ≈ 30 mV at 10 mA/cm²) | ~30 mV/dec |
| OER | 1.23 | IrO₂, RuO₂ (η ≈ 300 mV) | 40–60 mV/dec |
| ORR | 1.23 | Pt/C (η ≈ 300 mV) | 60–70 mV/dec |
| CO₂RR | −0.11 (to CO) | Au, Ag (for CO); Cu (for hydrocarbons) | Variable |

- **HER** (Hydrogen Evolution): 2H⁺ + 2e⁻ → H₂ (acidic) or 2H₂O + 2e⁻ → H₂ + 2OH⁻ (alkaline).
- **OER** (Oxygen Evolution): 2H₂O → O₂ + 4H⁺ + 4e⁻.
- **ORR** (Oxygen Reduction): O₂ + 4H⁺ + 4e⁻ → 2H₂O.
- **Descriptor approach**: d-band center position predicts activity trends.

## Data Reference
- L4 Data: L4_reference/electrode_potentials.csv — Standard reduction potentials E° for 28 half-reactions
- L4 Reference: L4_reference/THERMODYNAMIC_DATABASES.md — Links to NIST, CRC Handbook
