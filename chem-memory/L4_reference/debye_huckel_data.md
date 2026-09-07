# Debye-Hückel Constants and Ion Parameters
# Layer 4: Reference Data for Electrolyte Solutions
# Source: DeVoe Thermodynamics and Chemistry, Ch10

---
id: chemistry.debye_huckel_data
layer: 4
title: Debye-Hückel Constants and Ion Parameters
source: DeVoe Thermodynamics, Ch10
last_verified: 2026-03-15
---

## Debye-Hückel Constants

### Temperature Dependence

A and B parameters depend on solvent properties:

| T (°C) | A (mol/kg)^(-1/2) | B (Å^(-1)·(mol/kg)^(-1/2)) |
|--------|-------------------|---------------------------|
| 0 | 0.491 | 0.324 |
| 25 | 0.509 | 0.329 |
| 50 | 0.537 | 0.332 |
| 100 | 0.595 | 0.337 |

### Calculation from Solvent Properties

A = (2πN_A ρ)^(1/2) (e²/(4πε₀ε_r kT))^(3/2) / ln(10)

where:
- N_A = 6.022×10²³ mol⁻¹ (Avogadro constant)
- e = 1.602×10⁻¹⁹ C (elementary charge)
- ε₀ = 8.854×10⁻¹² F/m (vacuum permittivity)
- ε_r = relative permittivity of solvent
- k = 1.381×10⁻²³ J/K (Boltzmann constant)
- ρ = solvent density (kg/m³)

## Ion Size Parameters (a)

Effective ion sizes for extended Debye-Hückel equation:

| Ion | a (Å) |
|-----|-------|
| H⁺ | 9 |
| Li⁺ | 6 |
| Na⁺ | 4 |
| K⁺ | 3 |
| Rb⁺ | 3 |
| Cs⁺ | 3 |
| Ag⁺ | 2.5 |
| Tl⁺ | 2.5 |
| Mg²⁺ | 8 |
| Ca²⁺ | 6 |
| Sr²⁺ | 6 |
| Ba²⁺ | 5 |
| Fe²⁺ | 6 |
| Co²⁺ | 6 |
| Ni²⁺ | 6 |
| Cu²⁺ | 6 |
| Zn²⁺ | 6 |
| Al³⁺ | 9 |
| Fe³⁺ | 9 |
| La³⁺ | 8 |
| F⁻ | 3.5 |
| Cl⁻ | 3 |
| Br⁻ | 3 |
| I⁻ | 3 |
| OH⁻ | 3.5 |
| NO₃⁻ | 3 |
| CH₃COO⁻ | 4.5 |
| SO₄²⁻ | 4 |
| CO₃²⁻ | 4.5 |
| PO₄³⁻ | 4 |

## Activity Coefficient Validity Ranges

| Method | Valid I (mol/kg) | Notes |
|--------|------------------|-------|
| Debye-Hückel limiting law | I < 0.001 | Simplest, most accurate at very low I |
| Extended Debye-Hückel | I < 0.1 | Requires ion size parameter |
| Davies equation | I < 0.5 | Empirical extension |
| Pitzer equations | I > 0.1 | Complex, includes ion pairing |
| SIT model | I < 3 | Specific ion interaction theory |

## Mean Activity Coefficient Data (25°C)

Experimental γ± values for common electrolytes:

| Electrolyte | m = 0.001 | m = 0.01 | m = 0.1 | m = 1.0 |
|-------------|-----------|----------|---------|---------|
| HCl | 0.965 | 0.905 | 0.796 | 0.809 |
| NaCl | 0.965 | 0.903 | 0.778 | 0.657 |
| KCl | 0.965 | 0.901 | 0.769 | 0.606 |
| CaCl₂ | 0.888 | 0.732 | 0.518 | 0.725 |
| MgSO₄ | 0.744 | 0.402 | 0.150 | - |
| Na₂SO₄ | 0.887 | 0.714 | 0.452 | 0.202 |
| CuSO₄ | 0.744 | 0.404 | 0.154 | 0.043 |

## Relationships

### Mean Molality

For electrolyte: M_ν₊X_ν₋ → ν₊M^z₊ + ν₋X^z₋

m± = (m₊^ν₊ × m₋^ν₋)^(1/ν) where ν = ν₊ + ν₋

For 1:1 electrolyte: m± = m
For 1:2 electrolyte (e.g., CaCl₂): m± = 4^(1/3) × m
For 2:1 electrolyte (e.g., Na₂SO₄): m± = 4^(1/3) × m

### Ionic Strength Examples

| Electrolyte | m (mol/kg) | I (mol/kg) |
|-------------|------------|------------|
| NaCl (1:1) | m | m |
| CaCl₂ (2:1) | m | 3m |
| Na₂SO₄ (1:2) | m | 3m |
| MgSO₄ (2:2) | m | 4m |
| AlCl₃ (3:1) | m | 6m |

## References

- Robinson, R.A. and Stokes, R.H. Electrolyte Solutions, 2nd ed.
- DeVoe, H. Thermodynamics and Chemistry, Ch10
- Pitzer, K.S. Activity Coefficients in Electrolyte Solutions
