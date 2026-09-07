---
id: chemistry.debye_huckel
layer: 2
title: Debye-Hückel Theory for Electrolyte Solutions
parent: chemistry.core_map
stability: high
confidence: high
source: DeVoe Thermodynamics and Chemistry, Ch10.4
source_url: https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/DeVoes_Thermodynamics_and_Chemistry/10%3A_Electrolyte_Solutions/10.04%3A_The_Debye-Huckel_Theory
last_verified: 2026-03-15
---

## Core Concept (from source)

> "The theory of Peter Debye and Erich Hückel (1923) provides theoretical expressions for single-ion activity coefficients and mean ionic activity coefficients in electrolyte solutions. The expressions in one form or another are very useful for extrapolation of quantities that include mean ionic activity coefficients to low solute molality or infinite dilution."

## Ionic Atmosphere (from source)

> "The only interactions the theory considers are the electrostatic interactions between ions. These interactions are much stronger than those between uncharged molecules, and they die off more slowly with distance."

> "If the positions of ions in an electrolyte solution were completely random, the net effect of electrostatic ion–ion interactions would be zero, because each cation–cation or anion–anion repulsion would be balanced by a cation–anion attraction. The positions are not random, however: each cation has a surplus of anions in its immediate environment, and each anion has a surplus of neighboring cations. Each ion therefore has a net attractive interaction with the surrounding ion atmosphere."

## Ionic Strength (from source Eq 10.4.2)

```
I_m = (1/2) Σ m_i z_i²
```

**Historical note** (from source):
> "Lewis and Randall (J. Am. Chem. Soc., 1112–1154, 1921) introduced the term ionic strength, defined by Eq. 10.4.2, two years before the Debye–Hückel theory was published. They found empirically that in dilute solutions, the mean ionic activity coefficient of a given strong electrolyte is the same in all solutions having the same ionic strength."

## Single-Ion Activity Coefficient (from source Eq 10.4.1)
```
ln γ_i = -A_DH × z_i² × I_m / (1 + B_DH × a × I_m)
```
Where:
- γ_i = single-ion activity coefficient of ion i
- A_DH = Debye-Hückel A parameter
- B_DH = Debye-Hückel B parameter
- a = ion size parameter (Å)
- I_m = ionic strength (mol/kg)

## Mean Ionic Activity Coefficient (from source Eq 10.4.7)
```
ln γ± = -A_DH × |z₊z₋| × I_m / (1 + B_DH × a × I_m)
```
Where:
- γ± = mean ionic activity coefficient
- z₊, z₋ = charge numbers of cation and anion

## Debye-Hückel Parameters (from source Eq 10.4.3-10.4.4)

```
A_DH = (N_A² × e³ / 8π)^(1/2) × (2ρ_A*)^(1/2) × (ε_r × ε_0 × R × T)^(-3/2)

B_DH = N_A × e × (2ρ_A*)^(1/2) × (ε_r × ε_0 × R × T)^(-1/2)
```
Where:
- N_A = 6.022×10²³ mol⁻¹ (Avogadro constant)
- e = 1.602×10⁻¹⁹ C (elementary charge)
- ρ_A* = solvent density
- ε_r = relative permittivity (dielectric constant)
- ε_0 = 8.854× 10⁻¹² F/m (electric constant)
- R = 8.314 J/(mol·K) (gas constant)
- T = temperature (K)

## Values for Water at 25°C (from source)
- A_DH = 0.509 (mol/kg)^(-1/2)
- B_DH = 0.329 Å^(-1)·(mol/kg)^(-1/2)

## Key Rules (from source)

1. "Since the right side of Eq. 10.4.7 is negative at finite solute molalities, and zero at infinite dilution, the theory predicts that γ± is less than 1 at finite solute molalities and approaches 1 at infinite dilution."

2. "In dilute solutions, the mean ionic activity coefficient of a given strong electrolyte is the same in all solutions having the same ionic strength."

## Validity Range

| Model | Valid I (mol/kg) |
|-------|-------------------|
| Limiting Law | I < 0.001 |
| Extended DH | I < 0.1 |
| Davies equation | I < 0.5 |

## Problem-Solving Routes

1. **Calculate ionic strength** → Sum over all ions
2. **Find γ±** → Apply Debye-Hückel equation
3. **Correct equilibrium constant** → Use activities instead of concentrations
4. **Determine mean activity** → Combine individual ion activities

## Links to L3 Tools

- `../L3_functions/debye_huckel.py` - Ionic strength and γ± calculations

## Links to L4 Data


## Links to L5 Examples

- `../L5_examples/acid_base_examples.md - Worked examples
## Data Reference
- L4 Data: L4_reference/acid_base_constants.csv — Ka, Kb, pKa, pKb for common acids/bases
- L4 Data: L4_reference/solubility_products.csv — Ksp values for 30 sparingly soluble salts
- L4 Data: L4_reference/formation_constants.csv — Kf values for 24 metal complexes

---

## L3 Tool Call Directives

**Source:** debye_huckel.py
Debye-Hückel activity coefficients, ionic strength, limiting law (DeVoe Ch10.4).

### Available functions:
- ionic_strength(molalities, charges) → float — I_m = ½ Σ m_i z_i²
- debye_huckel_A_parameter(temperature, epsilon_r, rho_A) → float — A_DH parameter (0.509 at 25°C water)
- debye_huckel_B_parameter(temperature, epsilon_r, rho_A) → float — B_DH parameter
- single_ion_activity_coefficient(z, ionic_strength, ion_size, A_DH, B_DH, temperature) → float — γ_i from extended DH
- mean_ionic_activity_coefficient(z_plus, z_minus, ionic_strength, ion_size, A_DH, B_DH, temperature) → float — γ± for salt
- limiting_law_activity_coefficient(z, ionic_strength, A_DH, temperature) → float — γ_i from limiting law (I < 0.001 M)
- ionic_strength_from_conductivity(conductivity, molar_conductivity) → float — Approximate I from κ and Λ_m

### Common errors:
- ❌ Using limiting law for I > 0.001 M — use extended DH or Davies equation instead
- ❌ Confusing molal (m) and molar (M) concentration scales for ionic strength
