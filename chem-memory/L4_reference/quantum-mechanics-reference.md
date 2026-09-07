# Quantum Mechanics Reference - L4

## Physical Constants

| Constant | Symbol | Value | Units | Uncertainty |
|----------|--------|-------|-------|-------------|
| Planck's constant | h | 6.62607015 × 10⁻³⁴ | J·s | exact |
| Reduced Planck | ℏ | 1.054571817 × 10⁻³⁴ | J·s | exact |
| Electron mass | mₑ | 9.1093837015 × 10⁻³¹ | kg | 2.8×10⁻⁴¹ |
| Proton mass | mₚ | 1.67262192369 × 10⁻²⁷ | kg | 5.1×10⁻³⁸ |
| Neutron mass | mₙ | 1.67492749804 × 10⁻²⁷ | kg | 9.5×10⁻³⁸ |
| Elementary charge | e | 1.602176634 × 10⁻¹⁹ | C | exact |
| Bohr radius | a₀ | 5.29177210903 × 10⁻¹¹ | m | 8.0×10⁻²¹ |
| Rydberg constant | R∞ | 1.0973731568160 × 10⁷ | m⁻¹ | 2.1×10⁻⁵ |
| Speed of light | c | 2.99792458 × 10⁸ | m/s | exact |
| Permittivity | ε₀ | 8.8541878128 × 10⁻¹² | F/m | 1.3×10⁻²¹ |

---

## Energy Conversion Factors

| From | To | Multiply by |
|------|-----|-------------|
| Joule (J) | eV | 6.241509 × 10¹⁸ |
| eV | J | 1.60217663 × 10⁻¹⁹ |
| cm⁻¹ | J | 1.986446 × 10⁻²³ |
| cm⁻¹ | eV | 1.239842 × 10⁻⁴ |
| Hz | J | 6.62607015 × 10⁻³⁴ |
| Hz | eV | 4.1356677 × 10⁻¹⁵ |
| kcal/mol | eV | 0.0433641 |
| Hartree | eV | 27.211386 |

---

## Particle in a Box Reference Values

### Ground State Energy (n=1)

| System | Mass (kg) | L (nm) | E₁ (eV) |
|--------|-----------|--------|---------|
| Electron | 9.109×10⁻³¹ | 1 | 0.376 |
| Electron | 9.109×10⁻³¹ | 0.5 | 1.505 |
| Electron | 9.109×10⁻³¹ | 2 | 0.094 |
| Proton | 1.673×10⁻²⁷ | 1 | 2.05×10⁻⁴ |
| H atom | 1.674×10⁻²⁷ | 1 | 2.05×10⁻⁴ |

### Formula Quick Reference

```
Eₙ = n²h²/(8mL²) = n² × 37.6 eV·nm² × (mₑ/m) / L(nm)²

For electron: Eₙ (eV) ≈ 0.376 × n² / L(nm)²
```

### Wavefunction Properties

| n | Nodes | ⟨x⟩/L | ⟨x²⟩/L² | (Δx)²/L² |
|---|-------|-------|---------|----------|
| 1 | 0 | 0.5 | 0.283 | 0.0328 |
| 2 | 1 | 0.5 | 0.325 | 0.0747 |
| 3 | 2 | 0.5 | 0.343 | 0.0928 |
| ∞ | n-1 | 0.5 | 1/3 | 1/12 |

---

## Harmonic Oscillator Reference

### Typical Vibrational Frequencies

| Molecule | ν (cm⁻¹) | k (N/m) | μ (amu) |
|----------|----------|---------|---------|
| H₂ | 4401 | 573 | 0.504 |
| HCl | 2990 | 516 | 0.980 |
| CO | 2170 | 1902 | 6.86 |
| N₂ | 2359 | 2297 | 7.00 |
| O₂ | 1580 | 1144 | 8.00 |
| I₂ | 215 | 172 | 63.5 |

### Energy Level Formula

```
Eᵥ = (v + ½)hν = (v + ½) × h × c × ν̃

where ν̃ is in cm⁻¹

Eᵥ (eV) = (v + ½) × 1.240 × 10⁻⁴ × ν̃ (cm⁻¹)
```

### Zero-Point Energies

| Molecule | ν (cm⁻¹) | E₀ (eV) | E₀ (kJ/mol) |
|----------|----------|---------|-------------|
| H₂ | 4401 | 0.273 | 26.3 |
| HCl | 2990 | 0.185 | 17.9 |
| CO | 2170 | 0.135 | 13.0 |
| N₂ | 2359 | 0.146 | 14.1 |
| I₂ | 215 | 0.0133 | 1.29 |

### Hermite Polynomials

```
H₀(x) = 1
H₁(x) = 2x
H₂(x) = 4x² - 2
H₃(x) = 8x³ - 12x
H₄(x) = 16x⁴ - 48x² + 12
H₅(x) = 32x⁵ - 160x³ + 120x

Recurrence: H_{n+1}(x) = 2xHₙ(x) - 2nH_{n-1}(x)
```

---

## Rigid Rotor Reference

### Rotational Constants for Diatomics

| Molecule | r (pm) | μ (amu) | B (cm⁻¹) | B (GHz) |
|----------|--------|---------|----------|---------|
| H₂ | 74.1 | 0.504 | 60.8 | 1824 |
| HF | 91.7 | 0.957 | 20.9 | 627 |
| HCl | 127.4 | 0.980 | 10.6 | 318 |
| HBr | 141.4 | 0.995 | 8.47 | 254 |
| CO | 112.8 | 6.86 | 1.93 | 57.9 |
| N₂ | 109.8 | 7.00 | 2.00 | 60.0 |
| O₂ | 120.7 | 8.00 | 1.45 | 43.5 |

### Rotational Energy Levels

```
Eⱼ = J(J+1)B    (in cm⁻¹ or same units as B)

| J | E/B | Degeneracy | Cumulative states |
|---|-----|------------|-------------------|
| 0 | 0 | 1 | 1 |
| 1 | 2 | 3 | 4 |
| 2 | 6 | 5 | 9 |
| 3 | 12 | 7 | 16 |
| 4 | 20 | 9 | 25 |
| 5 | 30 | 11 | 36 |
```

### Transition Frequencies

```
J → J+1:  ΔE = 2B(J+1)

J=0→1:  ΔE = 2B
J=1→2:  ΔE = 4B
J=2→3:  ΔE = 6B
```

---

## Hydrogen Atom Reference

### Energy Levels

| n | E (eV) | E (kJ/mol) | IE from n (eV) |
|---|--------|------------|----------------|
| 1 | -13.60 | -1312 | 13.60 |
| 2 | -3.40 | -328 | 3.40 |
| 3 | -1.51 | -146 | 1.51 |
| 4 | -0.85 | -82.0 | 0.85 |
| 5 | -0.54 | -52.5 | 0.54 |
| ∞ | 0 | 0 | 0 |

### Energy Formula

```
Eₙ = -13.6057 eV / n² (for H, Z=1)
Eₙ = -Z² × 13.6057 eV / n² (for hydrogen-like)
```

### Quantum Number Rules

| Quantum Number | Range | Count |
|----------------|-------|-------|
| n | 1, 2, 3, ... | ∞ |
| l | 0, 1, ..., n-1 | n values |
| mₗ | -l, ..., 0, ..., +l | 2l+1 values |

### Orbital Summary

| n | l | Orbital | Radial nodes | Angular nodes | Total nodes |
|---|---|---------|--------------|---------------|-------------|
| 1 | 0 | 1s | 0 | 0 | 0 |
| 2 | 0 | 2s | 1 | 0 | 1 |
| 2 | 1 | 2p | 0 | 1 | 1 |
| 3 | 0 | 3s | 2 | 0 | 2 |
| 3 | 1 | 3p | 1 | 1 | 2 |
| 3 | 2 | 3d | 0 | 2 | 2 |
| 4 | 0 | 4s | 3 | 0 | 3 |
| 4 | 1 | 4p | 2 | 1 | 3 |
| 4 | 2 | 4d | 1 | 2 | 3 |
| 4 | 3 | 4f | 0 | 3 | 3 |

### Most Probable Radii

| Orbital | r_mp (a₀) | r_mp (pm) |
|---------|-----------|-----------|
| 1s | 1.00 | 52.9 |
| 2s | 5.24 (outer) | 277 |
| 2p | 4.00 | 212 |
| 3s | 13.1 | 692 |
| 3p | 12.0 | 634 |
| 3d | 9.00 | 476 |

### Orbital Capacities

| n | Orbitals | Max electrons |
|---|----------|---------------|
| 1 | 1 | 2 |
| 2 | 4 | 8 |
| 3 | 9 | 18 |
| 4 | 16 | 32 |
| n | n² | 2n² |

---

## Spherical Harmonics Reference

### Y_l^m (θ, φ)

```
Y₀⁰ = √(1/4π)

Y₁⁰ = √(3/4π) cos θ
Y₁^{±1} = ∓√(3/8π) sin θ e^{±iφ}

Y₂⁰ = √(5/16π) (3cos²θ - 1)
Y₂^{±1} = ∓√(15/8π) sin θ cos θ e^{±iφ}
Y₂^{±2} = √(15/32π) sin²θ e^{±2iφ}

Y₃⁰ = √(7/16π) (5cos³θ - 3cos θ)
Y₃^{±1} = ∓√(21/64π) sin θ (5cos²θ - 1) e^{±iφ}
Y₃^{±2} = √(105/32π) sin²θ cos θ e^{±2iφ}
Y₃^{±3} = ∓√(35/64π) sin³θ e^{±3iφ}
```

---

## Radial Wavefunctions (Hydrogen)

### R_{n,l}(r)

Using ρ = Zr/a₀:

```
R₁₀ = 2(Z/a₀)^{3/2} e^{-ρ}

R₂₀ = (1/√32)(Z/a₀)^{3/2} (2-ρ) e^{-ρ/2}
R₂₁ = (1/√24)(Z/a₀)^{3/2} ρ e^{-ρ/2}

R₃₀ = (2/81√3)(Z/a₀)^{3/2} (27-18ρ+2ρ²) e^{-ρ/3}
R₃₁ = (1/81√6)(Z/a₀)^{3/2} (6ρ+ρ²) e^{-ρ/3}
R₃₂ = (1/81√30)(Z/a₀)^{3/2} ρ² e^{-ρ/3}

R₄₀ = (1/768)(Z/a₀)^{3/2} (192-144ρ+24ρ²-ρ³) e^{-ρ/4}
R₄₁ = (1/256√15)(Z/a₀)^{3/2} (80ρ-20ρ²+ρ³) e^{-ρ/4}
R₄₂ = (1/384√5)(Z/a₀)^{3/2} (12ρ²-ρ³) e^{-ρ/4}
R₄₃ = (1/384√35)(Z/a₀)^{3/2} ρ³ e^{-ρ/4}
```

---

## Uncertainty Principle Reference

### Heisenberg Relations

```
Position-momentum: ΔxΔp ≥ ℏ/2 = 5.27 × 10⁻³⁵ J·s
Energy-time: ΔEΔt ≥ ℏ/2
Angular momentum: ΔLₓΔLᵧ ≥ ℏ|Lᵤ|/2
```

### Typical Uncertainties

| System | Δx | Δp | ΔxΔp/ℏ |
|--------|-----|-----|--------|
| PIB n=1 | 0.181 L | nh/2L | 0.568 |
| PIB n=2 | 0.273 L | nh/2L | 0.857 |
| H 1s | a₀ | ℏ/a₀ | 1 |
| HO v=0 | √(ℏ/2mω) | √(ℏmω/2) | 0.5 |

---

## Selection Rules

### Transitions

| System | Operator | Selection Rule |
|--------|----------|----------------|
| Harmonic oscillator | μ (dipole) | Δv = ±1 |
| Rigid rotor | μ (dipole) | ΔJ = ±1 |
| Hydrogen (electronic) | r (dipole) | Δl = ±1, Δm = 0, ±1 |
| Hydrogen (electronic) | Energy | Δn = any |

---

## Spectral Line Series (Hydrogen)

| Series | n_final | n_initial | Region | λ range (nm) |
|--------|---------|-----------|--------|--------------|
| Lyman | 1 | ≥2 | UV | 91-122 |
| Balmer | 2 | ≥3 | Visible | 365-656 |
| Paschen | 3 | ≥4 | IR | 820-1875 |
| Brackett | 4 | ≥5 | IR | 1458-4051 |
| Pfund | 5 | ≥6 | IR | 2279-7458 |

### Wavelength Formula

```
1/λ = R_H (1/n_f² - 1/n_i²)

R_H = 1.097 × 10⁷ m⁻¹
```

---

## Operator Reference

### Position Space Operators

| Observable | 1D Operator | 3D Operator |
|------------|-------------|-------------|
| Position | x | r = (x, y, z) |
| Momentum | -iℏ d/dx | -iℏ ∇ |
| Kinetic energy | -ℏ²/(2m) d²/dx² | -ℏ²/(2m) ∇² |
| Angular momentum L² | - | -ℏ² [angular part of ∇²] |
| Lᵤ | - | -iℏ ∂/∂φ |

### Commutators

```
[x, pₓ] = iℏ
[Lₓ, Lᵧ] = iℏLᵤ
[L², Lᵤ] = 0
[H, L²] = 0 (for central potential)
[x, pᵧ] = 0
```

---

## End of L4 Reference
