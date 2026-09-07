# LFSE Values - Reference Data

## LFSE Formulas

### Octahedral Complexes

```
LFSE = [(0.6 × #e_g) - (0.4 × #t_2g)] × Δ_o
```

### Summary Table

| d^n | High-Spin LFSE | Low-Spin LFSE |
|-----|----------------|---------------|
| d^0 | 0 | 0 |
| d^1 | -0.4Δ_o | -0.4Δ_o |
| d^2 | -0.8Δ_o | -0.8Δ_o |
| d^3 | -1.2Δ_o | -1.2Δ_o |
| d^4 | -0.6Δ_o | -1.6Δ_o + P |
| d^5 | 0 | -2.0Δ_o + 2P |
| d^6 | -0.4Δ_o | -2.4Δ_o + 2P |
| d^7 | -0.8Δ_o | -1.8Δ_o + P |
| d^8 | -1.2Δ_o | -1.2Δ_o |
| d^9 | -0.6Δ_o | -0.6Δ_o |
| d^10 | 0 | 0 |

**Note:** P = spin pairing energy; add for each pair created

---

## Pairing Energy Corrections

### Total Stabilization Energy
```
SE = LFSE + (number of pairs) × P
```

### Number of Electron Pairs

| d^n | High-Spin Pairs | Low-Spin Pairs |
|-----|-----------------|----------------|
| d^4 | 0 | 1 |
| d^5 | 0 | 2 |
| d^6 | 1 | 3 |
| d^7 | 2 | 3 |

---

## Tetrahedral Complexes

### LFSE Formula
```
LFSE = [(0.6 × #t_2) - (0.4 × #e)] × Δ_t
```

### Summary Table

| d^n | LFSE (always high-spin) |
|-----|-------------------------|
| d^0 | 0 |
| d^1 | -0.6Δ_t |
| d^2 | -1.2Δ_t |
| d^3 | -0.8Δ_t |
| d^4 | -0.4Δ_t |
| d^5 | 0 |
| d^6 | -0.6Δ_t |
| d^7 | -1.2Δ_t |
| d^8 | -0.8Δ_t |
| d^9 | -0.4Δ_t |
| d^10 | 0 |

---

## CFSE/LFSE in kJ/mol

### Octahedral High-Spin

| d^n | LFSE (Δ_o units) | With Δ_o = 10,000 cm⁻¹ |
|-----|------------------|------------------------|
| d^0 | 0 | 0 |
| d^1 | -0.4 | -48 kJ/mol |
| d^2 | -0.8 | -96 kJ/mol |
| d^3 | -1.2 | -144 kJ/mol |
| d^4 | -0.6 | -72 kJ/mol |
| d^5 | 0 | 0 |
| d^6 | -0.4 | -48 kJ/mol |
| d^7 | -0.8 | -96 kJ/mol |
| d^8 | -1.2 | -144 kJ/mol |
| d^9 | -0.6 | -72 kJ/mol |
| d^10 | 0 | 0 |

**Conversion:** 1 cm⁻¹ ≈ 0.012 kJ/mol

---

## Applications

### Ionic Radii (Jahn-Teller & LFSE Effects)

| Ion | d^n | LFSE effect on radius |
|-----|-----|----------------------|
| Mn²⁺ | d^5 (HS) | No LFSE → reference |
| Fe²⁺ | d^6 (HS) | Smaller than expected |
| Co²⁺ | d^7 (HS) | Smaller than expected |
| Ni²⁺ | d^8 | Smallest of series |
| Cu²⁺ | d^9 | Jahn-Teller distortion |

### Hydration Enthalpy Trends

LFSE affects thermodynamic stability:
- d³, d⁸ have maximum LFSE → most stable
- d⁵ has zero LFSE → least stable

---

## References
- CHM 320: Advanced Inorganic Chemistry (LibreTexts)
- Shriver, Atkins, Langford - Inorganic Chemistry
