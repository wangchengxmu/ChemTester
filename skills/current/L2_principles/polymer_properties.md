---
id: chem.polymer_properties
layer: 2
title: Polymer Properties
source: Polymer Chemistry (Schaller), Ch4
status: active
created: 2026-03-18
down_links:
  - ../L3_functions/polymer_chemistry_tools.py
  - ../L3_functions/polymer_physics.py
  - ../L3_functions/polymer_tools.py
---

# Polymer Properties

[Source: Polymer Chemistry (Schaller), Ch4]

## Core Concept

Polymer properties depend on molecular structure, molecular weight, and processing conditions. Key thermal transitions include glass transition (Tg) and melting temperature (Tm).

## Key Concepts

### Glass Transition Temperature (Tg)

- Temperature below which polymer is glassy (rigid)
- Above Tg, polymer becomes rubbery
- Amorphous regions only
- Affected by chain flexibility, intermolecular forces, molecular weight

### Melting Temperature (Tm)

- Crystalline regions melt
- Only for semi-crystalline polymers
- Always above Tg
- $T_m \approx 1.5 \times T_g$ (approximate rule)

## Key Equations

### Fox Equation (for copolymer Tg)

$$\frac{1}{T_g} = \frac{w_A}{T_{g,A}} + \frac{w_B}{T_{g,B}}$$

where $w_i$ = weight fraction of monomer $i$

### Molecular Weight Effect on Tg

$$T_g = T_{g,\infty} - \frac{K}{M_n}$$

where $K$ is a constant and $M_n$ is number-average MW

## Property Classification

| Property | Amorphous | Semi-crystalline |
|----------|-----------|------------------|
| Tg | Sharp transition | Present |
| Tm | None | Present |
| Clarity | Transparent | Translucent/opaque |
| Shrinkage | Low | High |

## Problem Types

1. **Predict Tg** of copolymer from Fox equation
2. **Compare polymers** based on structure
3. **Calculate crystallinity** from density
4. **Relate MW to properties**

## Related Topics

- �?`polymerization_kinetics.md` for MW control


## Implementations

- Implementation: `../L3_functions/polymer_physics.py`

## L3 Tool Call Directives

**Source:** polymer_chemistry_tools.py
Polymer Chemistry Calculation Tools.

### Available functions:
- degree_of_polymerization(monomer_mw, polymer_mw) → dict — Calculate degree of polymerization: DP = M_polymer / M_monomer.
- molecular_weight_from_dp(dp, monomer_mw) → float — Calculate polymer molecular weight: M = DP x M_monomer.
- number_avg_mw(moles, molecular_weights) → float — Calculate number-average molecular weight: Mn = Σ(ni x Mi) / Σ(ni).
- weight_avg_mw(moles, molecular_weights) → float — Calculate weight-average molecular weight: Mw = Σ(wi x Mi).
- polydispersity_index(Mw, Mn) → float — Calculate polydispersity index: PDI = Mw / Mn.
- copolymer_composition(f1, r1, r2) → dict — Calculate instantaneous copolymer composition using Mayo-Lewis equation.
- glass_transition_temperature(Tg1, w1, Tg2, Tg_more, w_more) → float — Estimate Tg of blend/copolymer using Fox equation.
- ceiling_temperature(dH_polymerization, dS_polymerization, monomer_concentration, units) → dict — Calculate ceiling temperature (Tc) for chain-growth polymerization.
- kinetic_chain_length(rp, rt) → dict — Calculate kinetic chain length (v) = Rp / Rt = rate of propagation / rate of termination.
- kinetic_chain_length_from_k(kp, kt, M_conc, M_dot_conc) → dict — Calculate kinetic chain length from rate constants and concentrations.

### Common errors:
- ❌ Passing wrong parameter types or missing required arguments
