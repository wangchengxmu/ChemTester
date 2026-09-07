---
id: gas-mixtures
layer: L2
topic: thermodynamics
source: DeVoe Ch9 Sec 9.3
depends: [thermodynamic_potentials, non_ideal_gases]
tags: [thermodynamics, gas-mixture, fugacity, virial, dalton, partial-pressure]
---

# Gas Mixtures

## Concept Overview
Mixtures of nonreacting gaseous substances. Key topics: partial pressure, ideal gas mixtures, fugacity in real gas mixtures, partial molar quantities, and virial equation of state for mixtures.

## Key Principles

### Partial Pressure (DeVoe 9.3.1)
```
p_i ≡ y_i · p     (y_i = mole fraction of i in gas phase)
Σ p_i = p          (Dalton's Law — valid for any gas mixture)
```

### Ideal Gas Mixtures (DeVoe 9.3.2)
An ideal gas mixture has negligible intermolecular interactions. It obeys pV = nRT and U depends only on T.
```
p_i = n_i RT / V   (partial pressure = pressure pure i would have at same T, V)
```
This "same T, V" interpretation of partial pressure is ONLY valid for ideal gas mixtures.

### Standard State for Gas Mixtures
Same as for pure gas: hypothetical state where pure gaseous i at mixture temperature, at standard pressure p°, behaves as an ideal gas.

### Chemical Potential in Gas Mixtures (DeVoe 9.3.3)
```
μ_i(p') = μ_i°(g) + RT ln(p'_i/p°) + ∫₀^p' [V_i − RT/p] dp
```
Analogous to pure gas equation (7.9.2), with partial molar volume V_i replacing molar volume V_m.

### Fugacity in Gas Mixtures
```
φ_i = f_i / p_i    (fugacity coefficient of component i)
μ_i = μ_i°(g) + RT ln(f_i/p°)
```

### Virial Equation of State for Mixtures (DeVoe 9.3.3)
```
pV/n = RT[1 + B/(V/n) + C/(V/n)² + ...]
```
Same form as pure gas, but virial coefficients depend on composition AND temperature.

At low-to-moderate pressures:
```
V/n = RT/p + B     (compression factor: Z = 1 + Bp/RT)
```

**Composition dependence of B**:
```
B = Σᵢ Σⱼ yᵢyⱼ Bᵢⱼ    (Bᵢⱼ = Bⱼᵢ)
```
For binary A-B: B = y_A² B_AA + 2y_A y_B B_AB + y_B² B_BB

### Partial Molar Volume in Virial Gas Mixtures
```
V_i = RT/p + B'_i
B'_i = 2 Σⱼ yⱼ Bᵢⱼ − B
```
For binary:
```
B'_A = B_AA + (−B_AA + 2B_AB − B_BB) y_B²
B'_B = B_BB + (−B_AA + 2B_AB − B_BB) y_A²
```

### Fugacity Coefficient from Virial Expansion
```
ln φ_i = B'_i · p / (RT)
```

### Partial Molar Quantities from B'_i (DeVoe Table 9.1)
Same formulas as pure gas with B'_i replacing B:
- H_i − H_i° = −RT²(dB'_i/dT)(p/RT)
- S_i − S_i° = R[ln(p/p°) + (dB'_i/dT)(p/RT)]  (with correction)
- etc.

## L3 Tools
- `L3_functions/non_ideal_gases_tools.py` (if exists) — virial coefficient calculations
- `L3_functions/thermodynamic_potentials_tools.py` — partial molar quantity computations

## Source
DeVoe, *Thermodynamics and Chemistry*, Ch9 Sec 9.3. LibreTexts: https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/DeVoes_Thermodynamics_and_Chemistry/09%3A_Mixtures/9.03%3A_Gas_Mixtures

## L3 Tool Call Directives

**Source:** `gas_laws_tools.py` (partial pressure functions)

Core Dalton's law calculations for gas mixtures: partial pressures, mole fractions, and multi-component mixtures.

### Available functions:
- `partial_pressure_dalton(mole_fraction, total_pressure)` → float — Calculate P_i = X_i × P_total
- `mole_fraction(moles_component, total_moles)` → float — Calculate X_i = n_i / n_total
- `dalton_law_partial_pressures(moles_dict, total_pressure)` → dict — Returns {'P_species': value} for all components

### Common errors:
- ❌ Mole fraction > 1 (check that moles_component ≤ total_moles)
- ❌ Forgetting that partial_pressure_dalton requires mole fraction, not raw moles
