# Thermodynamic Potentials - Reference Data
# Layer 4: Constants and reference values
# Source: DeVoe Thermodynamics and Chemistry

---
id: chemistry.thermodynamic_potentials_data
layer: 4
title: Thermodynamic Potentials Reference Data
source: DeVoe Thermodynamics, Ch5; NIST Chemistry WebBook
last_verified: 2026-03-15
---

## Standard Thermodynamic Properties (25°C, 1 bar)

### Common Substances

| Substance | ΔH°_f (kJ/mol) | ΔG°_f (kJ/mol) | S° (J/mol·K) |
|-----------|----------------|----------------|--------------|
| H₂(g) | 0 | 0 | 130.68 |
| O₂(g) | 0 | 0 | 205.14 |
| N₂(g) | 0 | 0 | 191.61 |
| C(graphite) | 0 | 0 | 5.74 |
| H₂O(l) | -285.83 | -237.13 | 69.91 |
| H₂O(g) | -241.82 | -228.57 | 188.83 |
| CO₂(g) | -393.51 | -394.36 | 213.74 |
| CH₄(g) | -74.81 | -50.72 | 186.26 |
| C₂H₆(g) | -84.68 | -32.82 | 229.60 |
| NH₃(g) | -46.11 | -16.45 | 192.45 |
| NaCl(s) | -411.15 | -384.14 | 72.13 |
| HCl(g) | -92.31 | -95.30 | 186.90 |
| HCl(aq) | -167.16 | -131.23 | 56.60 |

## Heat Capacities

### Ideal Gas Heat Capacities (J/mol·K)

C_p = a + bT + cT² + dT³ (T in K, valid 298-1500 K)

| Gas | a | b×10³ | c×10⁶ | d×10⁹ |
|-----|---|-------|-------|-------|
| H₂ | 29.09 | -0.836 | 20.1 | - |
| O₂ | 29.35 | 11.39 | -6.17 | - |
| N₂ | 26.98 | 5.91 | -0.34 | - |
| CO₂ | 44.22 | 8.79 | -8.62 | - |
| H₂O(g) | 30.54 | 10.29 | - | - |
| CH₄ | 12.45 | 76.59 | 17.44 | - |

### Simple Models

- **Monatomic ideal gas**: C_V = (3/2)R, C_p = (5/2)R
- **Diatomic ideal gas**: C_V = (5/2)R, C_p = (7/2)R (at moderate T)
- **Relationship**: C_p - C_V = R (ideal gas)

## Natural Variables Summary

| Potential | Symbol | Definition | Natural Variables | Differential |
|-----------|--------|------------|-------------------|--------------|
| Internal Energy | U | - | S, V | dU = TdS - pdV |
| Enthalpy | H | U + pV | S, p | dH = TdS + Vdp |
| Helmholtz Energy | A | U - TS | T, V | dA = -SdT - pdV |
| Gibbs Energy | G | H - TS | T, p | dG = -SdT + Vdp |

## Units and Conversions

| Quantity | SI Unit | Common Unit | Conversion |
|----------|---------|-------------|------------|
| Energy | J | kJ, cal, eV | 1 cal = 4.184 J; 1 eV = 96.485 kJ/mol |
| Pressure | Pa | bar, atm | 1 bar = 10⁵ Pa; 1 atm = 101325 Pa |
| Entropy | J/K | J/(mol·K) | - |
| Temperature | K | °C | T(K) = T(°C) + 273.15 |

## Thermodynamic Relations

### Maxwell Relations

From dU: (∂T/∂V)_S = -(∂p/∂S)_V
From dH: (∂T/∂p)_S = (∂V/∂S)_p
From dA: (∂S/∂V)_T = (∂p/∂T)_V
From dG: (∂S/∂p)_T = -(∂V/∂T)_p

### Useful Derivatives

- C_V = T(∂S/∂T)_V = (∂U/∂T)_V
- C_p = T(∂S/∂T)_p = (∂H/∂T)_p
- α (thermal expansion) = (1/V)(∂V/∂T)_p
- κ_T (isothermal compressibility) = -(1/V)(∂V/∂p)_T

## References

- NIST Chemistry WebBook: https://webbook.nist.gov/chemistry/
- DeVoe, H. Thermodynamics and Chemistry, Ch5
