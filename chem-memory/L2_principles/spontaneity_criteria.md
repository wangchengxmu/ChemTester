---
id: chemistry.spontaneity_criteria
layer: 2
title: Criteria for Spontaneity
parent: chemistry.core_map
stability: high
confidence: high
source: DeVoe Thermodynamics and Chemistry, Ch5.8
source_url: https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/DeVoes_Thermodynamics_and_Chemistry/05%3A_Thermodynamic_Potentials/5.08%3A_Criteria_for_Spontaneity
last_verified: 2026-03-15
---

## Core Concept (from source)

> "In this section we combine the first and second laws in order to derive some general relations for changes during a reversible or irreversible process of a closed system. The temperature and pressure will be assumed to be practically uniform during the process, even if the process is irreversible."

## Clausius Inequality (from source Eq 5.8.1-5.8.2)

```
dS ≥ dq/T     (rev/irrev, closed system)  Eq 5.8.1
dq ≤ TdS      (rev/irrev, closed system)  Eq 5.8.2
```
> "The inequalities in these relations refer to an irreversible process and the equalities to a reversible process."

## Combined First and Second Law Relations (from source Eq 5.8.3-5.8.6)

```
dU ≤ TdS - pdV + dw'       Eq 5.8.3
dH ≤ TdS + Vdp + dw'       Eq 5.8.4
dA ≤ -SdT - pdV + dw'      Eq 5.8.5
dG ≤ -SdT + Vdp + dw'      Eq 5.8.6
```
Where dw' is nonexpansion work.

## Spontaneity Criteria (from source)

### Helmholtz Energy (from source)
> "Equation 5.8.5 shows that during a spontaneous irreversible change at constant temperature and volume, dA is less than dw'. If the only work is expansion work (i.e., dw' is zero), the Helmholtz energy decreases during a spontaneous process at constant T and V and has its minimum value when the system reaches an equilibrium state."

**Criterion**: At constant T and V, with expansion work only:
- dA < 0 → spontaneous
- dA = 0 → equilibrium

### Gibbs Energy (from source)
> "Equation 5.8.6 is especially useful."

**Criterion**: At constant T and p, with expansion work only:
- dG < 0 → spontaneous
- dG = 0 → equilibrium

## Excess Entropy Formalism (from source Eq 5.8.7-5.8.9)

> "Ben-Amotz and Honig (J. Chem. Phys., 118, 5932–5936, 2003; J. Chem. Educ., 83, 132–137, 2006) developed a 'rectification' procedure that simplifies the mathematical manipulation of inequalities."

```
dS = dq/T + dθ      Eq 5.8.7  (where dθ ≥ 0)
dU = TdS - pdV + dw' - Tdθ      Eq 5.8.8
dG = -SdT + Vdp + dw' - Tdθ      Eq 5.8.9
```

> "Equation 5.8.9 tells us that during a process at constant T and p, with expansion work only (dw' = 0), dG has the same sign as -Tdθ: negative for an irreversible change and zero for a reversible change."

## Summary Table

| Conditions | Spontaneous | Equilibrium |
|------------|-------------|-------------|
| Isolated system | dS > 0 | dS = 0 |
| Constant T, V, w' = 0 | dA < 0 | dA = 0 |
| Constant T, p, w' = 0 | dG < 0 | dG = 0 |

## Problem-Solving Routes

1. **Identify conditions** → Determine which variables are constant
2. **Choose appropriate potential** → A for T,V; G for T,p
3. **Calculate change** → Determine sign of dA or dG
4. **Conclude spontaneity** → Negative = spontaneous

## Links to L3 Tools

- `../L3_functions/thermodynamic_potentials.py` - Spontaneity criteria functions

## Links to L5 Examples

- `../L5_examples/thermal_analysis/ - Worked examples

## Data Reference
- L3 Tool: 	hermodynamic_lookup_tools.lookup_thermodynamic_data(formula) — ΔHf°, ΔGf°, S°, Cp for 58+ compounds
- L3 Tool: 	hermodynamic_lookup_tools.calculate_reaction_dH(reactants, products) — reaction enthalpy from formation data
- L3 Tool: 	hermodynamic_lookup_tools.calculate_reaction_dG(reactants, products) — reaction Gibbs energy
- L4 Data: L4_reference/thermodynamic_data.csv — Full table with NIST/CRC values
- L4 Reference: L4_reference/THERMODYNAMIC_DATABASES.md — Links to NIST-JANAF, NIST WebBook
