# Spontaneity

## Concept Overview

A spontaneous process occurs naturally under given conditions without requiring continuous external energy input. Spontaneity is determined by matter and energy dispersal, not by speed.

## Key Principles

### Spontaneous vs Nonspontaneous
| Type | Definition |
|------|------------|
| Spontaneous | Occurs naturally without continuous external energy |
| Nonspontaneous | Requires continuous energy input |

### Key Insight
- Spontaneity ≠ rate (speed)
- Diamond → graphite is spontaneous but extremely slow
- Spontaneity is about direction, not kinetics

### Driving Forces
1. **Matter dispersal**: Expansion of gas into vacuum
2. **Energy dispersal**: Heat flow from hot to cold

## Problem-Solving Routes

1. **Identify spontaneous direction**: Which way does process occur naturally?
2. **Assess matter dispersal**: Does matter become more distributed?
3. **Assess energy dispersal**: Does energy become more uniformly distributed?

## Links

- **L3 Tools**: `../L3_functions/spontaneity_tools.py`
- **L4 Reference**: Spontaneous process examples
- **L5 Examples**: Real-world spontaneity

## Related Topics

- Entropy
- Second Law
- Gibbs free energy

## Data Reference
- L3 Tool: 	hermodynamic_lookup_tools.lookup_thermodynamic_data(formula) — ΔHf°, ΔGf°, S°, Cp for 58+ compounds
- L3 Tool: 	hermodynamic_lookup_tools.calculate_reaction_dH(reactants, products) — reaction enthalpy from formation data
- L3 Tool: 	hermodynamic_lookup_tools.calculate_reaction_dG(reactants, products) — reaction Gibbs energy
- L4 Data: L4_reference/thermodynamic_data.csv — Full table with NIST/CRC values
- L4 Reference: L4_reference/THERMODYNAMIC_DATABASES.md — Links to NIST-JANAF, NIST WebBook

## L3 Tool Call Directives

**Source:** `spontaneity_tools.py`

Gibbs free energy spontaneity checks, matter/energy dispersal predictions, entropy direction.

### Available functions:
- `is_spontaneous(delta_G)` → bool — True if ΔG < 0
- `spontaneity_direction(delta_G)` → str — 'forward (spontaneous)' / 'reverse (spontaneous)' / 'equilibrium'
- `predict_matter_dispersal(initial_volume, final_volume)` → str — Expansion spontaneity
- `predict_energy_dispersal(T_hot, T_cold)` → str — Heat flow direction prediction
- `distinguish_spontaneity_from_rate(is_spontaneous_process, observed_rate='slow')` → Dict — Spontaneity ≠ rate

### Common errors:
- ❌ Confusing spontaneity with rate — spontaneous ≠ fast
- ❌ Forgetting ΔG = 0 means equilibrium, not "no reaction"
