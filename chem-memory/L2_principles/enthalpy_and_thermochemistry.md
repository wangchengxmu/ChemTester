---
id: chem.enthalpy_thermochemistry
layer: 2
title: Enthalpy and Thermochemistry
source: LibreTexts Chemistry 2e Ch05.03
status: active
created: 2026-03-11
last_verified: 2026-03-11
---

# Enthalpy and Thermochemistry

## Problem type
Calculate enthalpy changes using Hess's Law or standard enthalpies of formation.

## Decision tree

1. **What is asked?**
   - ΔH_rxn → Use ΔH°f values or Hess's Law
   - Unknown ΔH → Combine known reactions
   - Heat of formation → Use formation reaction

2. **Data available?**
   - ΔH°f values → Use standard formula
   - Related reactions → Use Hess's Law
   - Calorimetry data → Calculate directly

3. **Reaction type?**
   - Combustion → ΔH_comb usually negative (exothermic)
   - Formation → ΔH_f from elements
   - Phase change → Use ΔH_fus or ΔH_vap

## Core formulas

### Enthalpy from formation data
```
ΔH°_rxn = Σ(n × ΔH°_f products) - Σ(n × ΔH°_f reactants)
```

### Hess's Law
```
If: Reaction A = Reaction B + Reaction C
Then: ΔH_A = ΔH_B + ΔH_C
```

### Standard states
- Elements: most stable form at 1 atm, 298 K
- ΔH°_f (elements in standard state) = 0

### Common enthalpy changes
| Type | Definition | Sign |
|------|-----------|------|
| ΔH_f | Formation from elements | Variable |
| ΔH_comb | Combustion | Usually negative |
| ΔH_fus | Melting | Positive |
| ΔH_vap | Vaporization | Positive |
| ΔH_soln | Dissolution | Variable |

## Key standard enthalpies of formation

| Compound | ΔH°_f (kJ/mol) |
|----------|---------------|
| CO₂(g) | -393.5 |
| H₂O(l) | -285.8 |
| H₂O(g) | -241.8 |
| CH₄(g) | -74.8 |
| C₂H₅OH(l) | -277.7 |
| NH₃(g) | -46.1 |
| NO₂(g) | 33.2 |
| SO₂(g) | -296.8 |
| NaCl(s) | -411.2 |

## Constraints
- Must balance equations before applying ΔH formula
- Coefficients in equation match coefficients in enthalpy calculation
- ΔH°f values require standard conditions (298 K, 1 atm)
- Elements in standard state have ΔH°f = 0

## Common patterns
1. Calculate ΔH_rxn from ΔH°f values
2. Use Hess's Law to find unknown enthalpy
3. Manipulate reactions: reverse → change sign; multiply → multiply ΔH
4. Combine reactions → add enthalpies

## Example: Hess's Law

**Given**:
```
C(s) + O₂(g) → CO₂(g)       ΔH = -393.5 kJ
CO(g) + ½O₂(g) → CO₂(g)    ΔH = -283.0 kJ
```

**Find**: C(s) + ½O₂(g) → CO(g)  ΔH = ?

**Solution**:
```
C(s) + O₂(g) → CO₂(g)            ΔH₁ = -393.5 kJ
CO₂(g) → CO(g) + ½O₂(g)          ΔH₂ = +283.0 kJ (reverse)

Add: C(s) + ½O₂(g) → CO(g)       ΔH = -393.5 + 283.0 = -110.5 kJ
```

## Links

### L3 Implementation
- `../L3_functions/enthalpy_tools.py` (TODO)

### L4 Reference
- `../L4_reference/thermodynamic_data.csv` (TODO)

### L5 Examples
- `../L5_examples/thermal_analysis/ (TODO)

## Source trace
- `../sources/ingestion/source-thermochemistry-stepwise.md` section 5.03

## Data Reference
- L3 Tool: 	hermodynamic_lookup_tools.lookup_thermodynamic_data(formula) — ΔHf°, ΔGf°, S°, Cp for 58+ compounds
- L3 Tool: 	hermodynamic_lookup_tools.calculate_reaction_dH(reactants, products) — reaction enthalpy from formation data
- L3 Tool: 	hermodynamic_lookup_tools.calculate_reaction_dG(reactants, products) — reaction Gibbs energy
- L4 Data: L4_reference/thermodynamic_data.csv — Full table with NIST/CRC values
- L4 Reference: L4_reference/THERMODYNAMIC_DATABASES.md — Links to NIST-JANAF, NIST WebBook

## L3 Tool Call Directives

**Source:** `thermochemistry_tools.py`

⚠️ Stub file — no public functions implemented yet.

### Available functions:
- *(none — file is empty)*
