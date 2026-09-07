# Magnetic Moments - Reference Data

## Spin-Only Magnetic Moments

### Formula
```
μ_eff = √(n(n+2)) μ_B
```
Where n = number of unpaired electrons

### Calculated Values

| n | μ_eff (μ_B) | μ_eff² |
|---|-------------|--------|
| 0 | 0.00 | 0 |
| 1 | 1.73 | 3 |
| 2 | 2.83 | 8 |
| 3 | 3.87 | 15 |
| 4 | 4.90 | 24 |
| 5 | 5.92 | 35 |

### Observed Ranges (First-Row Transition Metals)

| n | μ_eff (observed) | Typical Complexes |
|---|------------------|-------------------|
| 1 | 1.7 - 2.2 | Cu(II), low-spin Fe(III) |
| 2 | 2.8 - 3.5 | Ni(II), low-spin Mn(III) |
| 3 | 3.8 - 4.5 | Cr(III), high-spin Co(II) |
| 4 | 4.8 - 5.5 | High-spin Fe(II), Mn(III) |
| 5 | 5.8 - 6.5 | High-spin Mn(II), Fe(III) |

---

## Magnetic Data for Common Complexes

### Iron Complexes

| Complex | d^n | Spin State | Unpaired | μ_eff (μ_B) |
|---------|-----|------------|----------|-------------|
| [Fe(H₂O)₆]²⁺ | d⁶ | High | 4 | 5.1-5.5 |
| [Fe(CN)₆]⁴⁻ | d⁶ | Low | 0 | 0 (diamag) |
| [Fe(H₂O)₆]³⁺ | d⁵ | High | 5 | 5.7-6.0 |
| [Fe(CN)₆]³⁻ | d⁵ | Low | 1 | 2.0-2.5 |

### Cobalt Complexes

| Complex | d^n | Spin State | Unpaired | μ_eff (μ_B) |
|---------|-----|------------|----------|-------------|
| [Co(H₂O)₆]²⁺ | d⁷ | High | 3 | 4.8-5.2 |
| [Co(NH₃)₆]³⁺ | d⁶ | Low | 0 | 0 (diamag) |
| [CoF₆]³⁻ | d⁶ | High | 4 | 5.0-5.5 |

### Nickel Complexes

| Complex | d^n | Spin State | Unpaired | μ_eff (μ_B) |
|---------|-----|------------|----------|-------------|
| [Ni(H₂O)₆]²⁺ | d⁸ | - | 2 | 3.2-3.5 |
| [Ni(CN)₄]²⁻ | d⁸ | Square planar | 0 | 0 (diamag) |
| [NiCl₄]²⁻ | d⁸ | Tetrahedral | 2 | 3.5-4.0 |

### Copper Complexes

| Complex | d^n | Spin State | Unpaired | μ_eff (μ_B) |
|---------|-----|------------|----------|-------------|
| [Cu(H₂O)₆]²⁺ | d⁹ | - | 1 | 1.7-2.0 |
| [Cu(NH₃)₄]²⁺ | d⁹ | - | 1 | 1.7-2.0 |

### Manganese Complexes

| Complex | d^n | Spin State | Unpaired | μ_eff (μ_B) |
|---------|-----|------------|----------|-------------|
| [Mn(H₂O)₆]²⁺ | d⁵ | High | 5 | 5.9-6.1 |
| [Mn(H₂O)₆]³⁺ | d⁴ | High | 4 | 4.8-5.2 |
| [Mn(CN)₆]³⁻ | d⁴ | Low | 2 | 3.0-3.5 |

---

## Spin-Orbit Coupling Corrections

### Orbital Contribution Formula
```
μ_eff = √(4S(S+1) + L(L+1)) μ_B
```

### When Orbital Contribution Matters
- Free ions (no ligand field)
- Some octahedral complexes with ground state T term
- Not significant for octahedral complexes with A or E ground states

### Ground State Term Symbols

| d^n | Octahedral High-Spin | Octahedral Low-Spin |
|-----|---------------------|---------------------|
| d¹ | ²T₂g | - |
| d² | ³T₁g | - |
| d³ | ⁴A₂g | - |
| d⁴ | ⁵E_g | ³T₁g |
| d⁵ | ⁶A₁g | ²T₂g |
| d⁶ | ⁵T₂g | ¹A₁g |
| d⁷ | ⁴T₁g | ²E_g |
| d⁸ | ³A₂g | - |
| d⁹ | ²E_g | - |

---

## Measurement Methods

### Gouy Balance
- Measures weight difference with/without magnetic field
- Paramagnetic samples appear heavier
- μ_eff calculated from susceptibility

### Evans Method (NMR)
- Measures shift of reference peak
- Useful for solution measurements
- Formula: χ_M = (3Δf)/(4πfc) + χ_0

### SQUID Magnetometer
- Superconducting Quantum Interference Device
- Most sensitive method
- Measures both DC and AC susceptibility

---

## Bohr Magneton (μ_B)

### Definition
```
μ_B = eh/4πm_e = 9.274 × 10⁻²⁴ J/T
```

### Units
- e = electron charge
- h = Planck constant
- m_e = electron mass

---

## References
- CHM 320: Advanced Inorganic Chemistry (LibreTexts)
- Housecroft, Sharpe - Inorganic Chemistry
