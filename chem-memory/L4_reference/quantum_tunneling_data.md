# Quantum Tunneling Reference Data

## Key Physical Constants

| Constant | Symbol | Value | Units |
|----------|--------|-------|-------|
| Reduced Planck constant | ℏ | 1.054571817×10⁻³⁴ | J·s |
| Electron mass | m_e | 9.10938370×10⁻³¹ | kg |
| Atomic mass unit | u | 1.660539067×10⁻²⁷ | kg |
| Boltzmann constant | k_B | 1.380649×10⁻²³ | J/K |

## Particle Masses

| Particle | Mass (amu) | Mass (kg) |
|----------|------------|-----------|
| Electron | 5.4858×10⁻⁴ | 9.109×10⁻³¹ |
| Proton (H) | 1.0078 | 1.673×10⁻²⁷ |
| Deuteron (D) | 2.0141 | 3.344×10⁻²⁷ |
| Muon | 0.1134 | 1.884×10⁻²⁸ |

## Typical Barrier Parameters

### STM/AFM Tunneling
- Barrier height: 1-5 eV
- Barrier width: 0.5-1 nm
- Electron energies: 0.1-10 eV

### Proton Transfer Reactions
- Barrier heights: 10-100 kJ/mol
- Barrier widths: 0.3-0.8 Å
- Imaginary frequencies: 500-2000 cm⁻¹

## Transmission Coefficient Formulas

### Rectangular Barrier (E < V₀)
```
κ = √(2m(V₀-E))/ℏ
T ≈ 16E(V₀-E)/V₀² × exp(-2κa)
```

### WKB Approximation
```
T ≈ exp(-2∫√(2m(V(x)-E))/ℏ dx)
```

For rectangular barrier: T_WKB ≈ exp(-2κa) (no prefactor)

## Tunneling Corrections

### Wigner Correction
```
κ = 1 + (1/24)(ℏω‡/k_BT)²
```
Valid for ℏω‡ ≪ k_BT

Typical values (298 K):
| ν‡ (cm⁻¹) | u = ℏω‡/k_BT | κ_Wigner |
|-----------|--------------|----------|
| 500 | 0.24 | 1.002 |
| 1000 | 0.48 | 1.010 |
| 1500 | 0.72 | 1.022 |
| 2000 | 0.96 | 1.038 |

### Bell Correction
```
κ = u / (2 tanh(u/2))
```
Reduces to Wigner for small u.

## H/D Kinetic Isotope Effects

For proton transfer at 298 K:

| Barrier (kJ/mol) | Width (Å) | KIE_tunnel |
|------------------|-----------|------------|
| 20 | 0.5 | ~2-5 |
| 30 | 0.5 | ~5-15 |
| 40 | 0.5 | ~20-50 |
| 30 | 0.8 | ~100+ |

## Classical vs Quantum Behavior

### QHO Ground State
- Classically forbidden probability: P(v=0) = erfc(1)/2 ≈ **15.7%**
- This is independent of frequency and mass!

### Heavier Particle = Less Tunneling
For same barrier: T_H/T_D ≈ exp(factor × (√m_D - √m_H))
