---
id: chem.quantum_mechanics
layer: 2
title: Quantum Mechanics Core
source: LibreTexts Physical Chemistry Ch03-06
status: active
created: 2026-03-14
last_verified: 2026-03-14
---

# Quantum Mechanics Core

## Problem Types

1. **Particle in a Box** - Calculate quantized energies and wavefunctions
2. **Harmonic Oscillator** - Vibrational energy levels and spectroscopy
3. **Rigid Rotor** - Rotational energy and microwave spectroscopy
4. **Hydrogen Atom** - Electronic structure and orbital properties
5. **Expectation Values** - Average values and uncertainties
6. **Quantum Numbers** - Valid sets and degeneracies

## Decision Tree

### 1. What system is being analyzed?

- **Particle in box** → Use Eₙ = n²h²/8mL², ψₙ = √(2/L) sin(nπx/L)
- **Harmonic oscillator** → Use Eᵥ = (v + ½)hν
- **Rigid rotor** → Use Eⱼ = J(J+1)B
- **Hydrogen atom** → Use Eₙ = -13.6 eV/n²
- **General expectation** → Use ⟨A⟩ = ∫ψ*Âψ dτ

### 2. What is being calculated?

- **Energy levels** → Apply appropriate quantization formula
- **Wavefunction** → Check quantum number validity, apply formula
- **Probability** → Integrate |ψ|² over region
- **Expectation value** → Apply operator to wavefunction, integrate
- **Uncertainty** → Calculate ΔA = √(⟨A²⟩ - ⟨A⟩²)

### 3. Check constraints

- Quantum numbers must be valid (n > 0, l < n, |mₗ| ≤ l)
- Wavefunction must be normalized
- For degeneracy: count allowed mₗ values

---

## Section 1: Particle in a Box

### Energy Quantization

```
Eₙ = n²h²/(8mL²) = n²π²ℏ²/(2mL²)

where:
  n = quantum number = 1, 2, 3, ...
  m = particle mass (kg)
  L = box length (m)
```

**Key features:**
- Ground state energy (n=1) is non-zero: E₁ = h²/(8mL²) — zero-point energy
- Energy increases as n²
- Smaller box → larger energy spacing
- Heavier particle → smaller energy spacing

### Wavefunctions

```
ψₙ(x) = √(2/L) sin(nπx/L)

Properties:
- Normalized: ∫₀ᴸ |ψₙ|² dx = 1
- Orthogonal: ∫₀ᴸ ψₘψₙ dx = 0 for m ≠ n
- Nodes: n-1 nodes within the box
- Antinodes: n antinodes (including boundaries at x=0, L)
```

### 3D Particle in Box

```
E = (h²/8m)(nₓ²/Lₓ² + nᵧ²/Lᵧ² + nᵤ²/Lᵤ²)

ψ = √(8/LₓLᵧLᵤ) sin(nₓπx/Lₓ) sin(nᵧπy/Lᵧ) sin(nᵤπz/Lᵤ)

Degeneracy possible when dimensions are commensurate
```

### Expectation Values

```
⟨x⟩ = L/2              (center of box)
⟨x²⟩ = L²(1/3 - 1/2n²π²)
⟨p⟩ = 0                (no net momentum)
⟨p²⟩ = 2mEₙ            (from kinetic energy)
```

### Uncertainties

```
Δx = √(⟨x²⟩ - ⟨x⟩²)
Δp = √(⟨p²⟩ - ⟨p⟩²)
Δx·Δp ≥ ℏ/2           (Heisenberg principle)
```

---

## Section 2: Harmonic Oscillator

### Classical Foundation

```
F = -kx                    (Hooke's Law)
V(x) = ½kx²               (parabolic potential)
ω = √(k/m)                (angular frequency)
ν = ω/(2π)                (frequency in Hz)
```

### Quantum Energy Levels

```
Eᵥ = (v + ½)ℏω = (v + ½)hν

where:
  v = vibrational quantum number = 0, 1, 2, ...
  ω = √(k/μ)                  (angular frequency)
  μ = m₁m₂/(m₁ + m₂)         (reduced mass for diatomic)
```

**Key features:**
- Zero-point energy: E₀ = ½hν (cannot be removed)
- Equal spacing: ΔE = hν between adjacent levels
- Ground state has non-zero energy (quantum effect)

### Wavefunctions

```
ψᵥ(x) = Nᵥ · Hᵥ(α^½ x) · e^{-αx²/2}

where:
  α = μω/ℏ = √(μk)/ℏ
  Hᵥ = Hermite polynomial of degree v
  Nᵥ = (α/π)^¼ · 1/√(2ᵥ v!)
```

**Hermite polynomials:**
| v | Hᵥ(x) |
|---|-------|
| 0 | 1 |
| 1 | 2x |
| 2 | 4x² - 2 |
| 3 | 8x³ - 12x |
| 4 | 16x⁴ - 48x² + 12 |

**Properties:**
- v nodes for state v
- Even v → even function (symmetric)
- Odd v → odd function (antisymmetric)

### Reduced Mass

```
μ = m₁m₂/(m₁ + m₂)

For isotopic substitution:
ν' = ν · √(μ/μ')

Isotope effect: heavier isotope → lower frequency
```

### Spectroscopy

**Selection rule:** Δv = ±1

**IR transition frequency:** ν = (1/2π)√(k/μ)

---

## Section 3: Rigid Rotor

### Classical Foundation

```
E = ½Iω² = L²/(2I)
I = μr²                (moment of inertia)
L = Iω                  (angular momentum)
```

### Quantum Energy Levels

```
Eⱼ = J(J+1)ℏ²/(2I) = J(J+1)B

where:
  J = rotational quantum number = 0, 1, 2, ...
  B = rotational constant = ℏ²/(2I)
```

**Rotational constant:**
```
B = h/(8π²I) = h/(8π²μr²)

Commonly in cm⁻¹: B = h/(8π²cI)
```

**Key features:**
- E₀ = 0 (no zero-point rotational energy)
- Energy spacing increases with J
- Level J has degeneracy 2J+1

### Quantum Numbers

```
J = 0, 1, 2, ...              (total angular momentum)
mⱼ = -J, -J+1, ..., +J        (z-component, 2J+1 values)

|L| = √(J(J+1)) ℏ             (angular momentum magnitude)
Lᵤ = mⱼℏ                       (z-component)
```

### Degeneracy

```
gⱼ = 2J + 1

J=0: g=1 (non-degenerate)
J=1: g=3 (triply degenerate)
J=2: g=5 (five-fold degenerate)
```

### Spherical Harmonics

```
Yⱼ^{mⱼ}(θ,φ) = angular wavefunction

First few:
Y₀⁰ = √(1/4π)
Y₁⁰ = √(3/4π) cos θ
Y₁^{±1} = ∓√(3/8π) sin θ e^{±iφ}
```

### Spectroscopy

**Selection rule:** ΔJ = ±1

**Transition energy:** ΔE = 2B(J+1) for J → J+1

---

## Section 4: Hydrogen Atom

### Coulomb Potential

```
V(r) = -Ze²/(4πε₀r)

For hydrogen (Z=1): V(r) = -e²/(4πε₀r)
```

### Energy Levels

```
Eₙ = -Z²·13.6 eV/n² = -μe⁴/(8ε₀²h²n²)

where:
  n = principal quantum number = 1, 2, 3, ...
  Z = atomic number (1 for hydrogen)
```

**Energy level diagram:**
| n | E (eV) | Orbital types |
|---|--------|---------------|
| 1 | -13.60 | 1s |
| 2 | -3.40 | 2s, 2p |
| 3 | -1.51 | 3s, 3p, 3d |
| 4 | -0.85 | 4s, 4p, 4d, 4f |

### Quantum Numbers

| Symbol | Name | Range | Physical meaning |
|--------|------|-------|------------------|
| n | Principal | 1, 2, 3, ... | Energy, size |
| l | Angular momentum | 0 to n-1 | Shape, |L| |
| mₗ | Magnetic | -l to +l | Orientation, Lᵤ |

**Derived quantities:**
```
|L| = √(l(l+1)) ℏ         (angular momentum magnitude)
Lᵤ = mₗℏ                  (z-component)
```

### Orbital Types

| l | Type | Orbitals | Shape |
|---|------|----------|-------|
| 0 | s | 1 | Spherical |
| 1 | p | 3 | Dumbbell |
| 2 | d | 5 | Cloverleaf |
| 3 | f | 7 | Complex |

**Total orbitals for shell n:** n²

### Wavefunctions

```
ψ_{n,l,mₗ}(r,θ,φ) = R_{n,l}(r) · Y_l^{mₗ}(θ,φ)

Radial part: R_{n,l}(r)
Angular part: Spherical harmonic Y_l^{mₗ}(θ,φ)
```

**Key radial functions:**
```
1s: R₁₀ = 2(Z/a₀)^{3/2} e^{-Zr/a₀}
2s: R₂₀ ∝ (2-Zr/a₀) e^{-Zr/2a₀}
2p: R₂₁ ∝ r e^{-Zr/2a₀}
```

### Bohr Radius

```
a₀ = ε₀h²/(πmₑe²) ≈ 52.9 pm

Most probable radius for 1s electron
```

### Radial Distribution Function

```
P(r) = r² |R_{n,l}(r)|²

Maximum gives most probable radius
```

**Nodes:**
- Radial nodes: n - l - 1
- Angular nodes: l
- Total nodes: n - 1

### Ionization Energy

```
IE = |E₁| = 13.6 eV for hydrogen

For general one-electron: IE = Z² × 13.6 eV
```

---

## Section 5: Quantum Operators and Expectation Values

### Key Operators

| Observable | Operator | Form |
|------------|----------|------|
| Position | x̂ | x |
| Momentum | p̂ₓ | -iℏ ∂/∂x |
| Kinetic energy | T̂ | -ℏ²/(2m) ∂²/∂x² |
| Potential energy | V̂ | V(x) |
| Hamiltonian | Ĥ | -ℏ²/(2m)∇² + V |

### Expectation Value Formula

```
⟨A⟩ = ∫ ψ* Â ψ dτ

For normalized ψ
```

**Examples:**
```
⟨x⟩ = ∫ x |ψ|² dx
⟨p⟩ = ∫ ψ* (-iℏ ∂ψ/∂x) dx
⟨p²⟩ = ∫ ψ* (-ℏ² ∂²ψ/∂x²) dx
⟨E⟩ = ∫ ψ* Ĥ ψ dx
```

### Uncertainty

```
ΔA = √(⟨A²⟩ - ⟨A⟩²)

Heisenberg uncertainty principle:
Δx·Δp ≥ ℏ/2
ΔE·Δt ≥ ℏ/2
```

---

## Section 6: Commutators and Simultaneous Measurement

### Commutator Definition

```
[Â, B̂] = ÂB̂ - B̂Â

[Â, B̂] = 0 → operators commute → observables can be measured simultaneously
[Â, B̂] ≠ 0 → operators don't commute → uncertainty relation exists
```

### Key Commutators

```
[x̂, p̂ₓ] = iℏ          (position-momentum)
[L̂ₓ, L̂ᵧ] = iℏL̂ᵤ      (angular momentum components)
[Ĥ, L̂²] = 0          (Hamiltonian and L² commute for central potential)
```

---

## Common Patterns

1. **Calculate particle-in-box energy** → Use Eₙ = n²h²/8mL²
2. **Find wavefunction nodes** → Count n-1 for 1D box, n-l-1 radial + l angular for H
3. **Harmonic oscillator frequency** → ν = (1/2π)√(k/μ)
4. **Rotational constant** → B = h/(8π²μr²)
5. **Hydrogen energy** → Eₙ = -13.6/n² eV
6. **Degeneracy counting** → Product of degeneracies or 2J+1 or n²

---

## Links

### L3 Implementation
- `../L3_functions/quantum_mechanics_tools.py`

### L4 Reference
- `../L4_reference/quantum-mechanics-reference.md`

### L5 Examples
- `../L5_examples/quantum-mechanics/

### Source Trace
- `../sources/ingestion/source-quantum_mechanics-stepwise.md`

---

## Quick Reference Card

| System | Energy Formula | Key Feature |
|--------|---------------|-------------|
| Particle in box | Eₙ = n²h²/8mL² | Zero-point energy |
| Harmonic oscillator | Eᵥ = (v+½)hν | Equal spacing |
| Rigid rotor | Eⱼ = J(J+1)B | No zero-point |
| Hydrogen | Eₙ = -13.6/n² eV | Coulomb potential |

## L3 Tool Call Directives


**Source:** `advanced_quantum_tools.py`

L3 tool module for advanced quantum tools

### Available functions:
- `overlap_integral(R: float, alpha: float, beta: float)` → float — Overlap integral between two 1s STOs centered at ±R/2.
- `sum_1s_overlap_series(n: float, R: float)` → float — Partial sum for the incomplete gamma series (helper).
- `coulomb_integral(R: float, Z: float)` → float — Coulomb (J) integral for H2+ - attraction of 1s_A electron density to nucleus B.
- `exchange_integral(R: float, Z: float)` → float — Exchange (K / resonance) integral for H2+.
- `h2_plus_energy(R: float, Z: float)` → dict — Compute H2+ bonding and antibonding energies at internuclear distance R.
- `born_oppenheimer_energy(hamiltonian_params: Dict[str, Any])` → dict — Compute clamped-nuclei electronic energy given molecular Hamiltonian parameters.
- `h2_plus_energy_curve(R_range: Sequence[float] | None, Z: float, n_points: int)` → tuple — Generate potential energy curve for H2+ over a range of R values.
- `hartree_to_eV(E_hartree: float)` → float — Convert energy from Hartree to electron volts.
- `bohr_to_angstrom(R_bohr: float)` → float — Convert distance from Bohr radii to Ångströms.
- `integrand(r: float, theta: float)` → float — N/A
- `integrand_zA(y: float, x: float)` → float — N/A

### Common errors:
- ❌ Passing wrong parameter types (strings where numbers expected)
- ❌ Forgetting required parameters
