# L2 Topic: Advanced Electrochemistry

**Source**: Physical Chemistry (LibreTexts)
**Created**: 2026-03-13
**Status**: Scaffold (Pass-2)

---

## Concept Overview

Advanced electrochemistry extends beyond basic galvanic cells to quantitative calculations of cell potentials, electrolysis yields, and thermodynamic relationships.

### Key Features
1. **Nernst Equation**: E as function of concentration
2. **Thermodynamic relationships**: ΔG, K, and E
3. **Electrolysis calculations**: Faraday's laws
4. **Concentration cells**: Potential from concentration gradients

---

## Core Principles

### Nernst Equation
```
E = E° - (RT/nF) ln Q
```
At 25°C: E = E° - (0.0592/n) log Q

### Key Relationships
| Relationship | Equation |
|--------------|----------|
| ΔG and E | ΔG = -nFE |
| K and E° | log K = nE°/0.0592 (at 25°C) |
| Electrolysis | m = (M×I×t)/(n×F) |

### Concentration Cells
- Same electrodes, different [ion]
- E° = 0, potential from concentration gradient
- E = -(RT/nF) ln([dilute]/[concentrated])

---

## Decision Trees

### Choosing Electrochemistry Formula
```
Given E° and concentrations? → Nernst equation
Given E° and need K? → K = exp(nFE°/RT)
Given current and time? → Faraday's law
Two solutions of same ion? → Concentration cell
```

---

## Key Tables

### Standard Reduction Potentials (Selected)
| Half-reaction | E° (V) |
|---------------|--------|
| Li⁺ + e⁻ → Li | -3.04 |
| Zn²⁺ + 2e⁻ → Zn | -0.76 |
| Fe²⁺ + 2e⁻ → Fe | -0.44 |
| Cu²⁺ + 2e⁻ → Cu | +0.34 |
| Ag⁺ + e⁻ → Ag | +0.80 |
| Cl₂ + 2e⁻ → 2Cl⁻ | +1.36 |

---

## Connected Topics

- **Upstream**: [electrode_potentials.md](electrode_potentials.md), [galvanic_cells.md](galvanic_cells.md)
- **Related**: Thermodynamics, equilibrium

---

## L3 Tools Required

1. `advanced_electrochemistry_tools.py` - Nernst, electrolysis, thermodynamic relationships

---

## L4 References (TODO)

- [ ] Standard reduction potential tables
- [ ] Tafel slopes for common reactions
- [ ] Battery discharge curves

---

## L5 Worked Examples (TODO)

- [ ] Nernst equation calculations
- [ ] Electrolysis mass yield
- [ ] Equilibrium constant from cell potential

## Data Reference
- L4 Data: L4_reference/electrode_potentials.csv — Standard reduction potentials E° for 28 half-reactions
- L4 Reference: L4_reference/THERMODYNAMIC_DATABASES.md — Links to NIST, CRC Handbook

## L3 Tool Call Directives


**Source:** `advanced_electrochemistry_tools.py`

L3 tool module for advanced electrochemistry tools

### Available functions:
- `nernst_potential(e0: float, n: int, q: float, t: float)` → dict — Calculate cell potential at non-standard conditions.
- `nernst_25c(e0: float, n: int, q: float)` → dict — Calculate cell potential at 25degC using simplified Nernst equation.
- `electrolysis_mass(current: float, time_s: float, molar_mass: float, n: int)` → dict — Calculate mass produced in electrolysis.
- `electrolysis_charge(mass: float, molar_mass: float, n: int)` → dict — Calculate charge needed to produce a given mass.
- `equilibrium_constant_from_e0(e0: float, n: int, t: float)` → dict — Calculate equilibrium constant from standard cell potential.
- `gibbs_from_cell_potential(e: float, n: int)` → dict — Calculate Gibbs free energy from cell potential.
- `cell_potential_from_gibbs(delta_g: float, n: int)` → dict — Calculate cell potential from Gibbs free energy.
- `concentration_cell_potential(c_dilute: float, c_concentrated: float, n: int, t: float)` → dict — Calculate potential of a concentration cell.

### Common errors:
- ❌ Passing wrong parameter types (strings where numbers expected)
- ❌ Forgetting required parameters
