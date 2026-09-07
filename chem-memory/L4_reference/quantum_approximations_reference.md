id: chem.quantum_approximations.reference
layer: 4
title: Quantum Approximations Reference Tables
source: LibreTexts Physical Chemistry Ch07-08
created: 2026-03-14
---

# Quantum Approximations Reference Tables

## 1. Term Symbol Letter Codes

| L Value | Letter | Historical Origin | Number of m_L Values |
|---------|--------|-------------------|---------------------|
| 0 | S | Sharp | 1 |
| 1 | P | Principal | 3 |
| 2 | D | Diffuse | 5 |
| 3 | F | Fundamental | 7 |
| 4 | G | Alphabetical | 9 |
| 5 | H | Alphabetical | 11 |
| 6 | I | Alphabetical | 13 |
| 7 | K | (J skipped) | 15 |

**Note:** J is skipped to avoid confusion with total angular momentum J.

---

## 2. Multiplicity Names

| S (Total Spin) | 2S+1 | Name | Spin States |
|----------------|------|------|-------------|
| 0 | 1 | Singlet | All paired |
| ½ | 2 | Doublet | One unpaired |
| 1 | 3 | Triplet | Two parallel |
| 3/2 | 4 | Quartet | Three parallel |
| 2 | 5 | Quintet | Four parallel |
| 5/2 | 6 | Sextet | Five parallel |
| 3 | 7 | Septet | Six parallel |

---

## 3. Ground State Terms for pⁿ Configurations

| Config | Electrons | Fraction | S | L | J | Term | Degeneracy |
|--------|-----------|----------|---|---|---|------|------------|
| p¹ | 1 | 1/6 | ½ | 1 | 3/2 | ²P_{3/2} | 4 |
| p² | 2 | 2/6 | 1 | 1 | 0 | ³P₀ | 1 |
| p³ | 3 | 3/6 | 3/2 | 0 | 3/2 | ⁴S_{3/2} | 4 |
| p⁴ | 4 | 4/6 | 1 | 1 | 2 | ³P₂ | 5 |
| p⁵ | 5 | 5/6 | ½ | 1 | 3/2 | ²P_{3/2} | 4 |

**Key:** pⁿ and p^{6-n} have same terms (complement rule)
- p¹ and p⁵: both ²P
- p² and p⁴: both ³P
- p³: ⁴S (half-filled, unique)

---

## 4. Ground State Terms for dⁿ Configurations

| Config | Electrons | Fraction | S | L | J | Term | Degeneracy |
|--------|-----------|----------|---|---|---|------|------------|
| d¹ | 1 | 1/10 | ½ | 2 | 3/2 | ²D_{3/2} | 4 |
| d² | 2 | 2/10 | 1 | 3 | 2 | ³F₂ | 5 |
| d³ | 3 | 3/10 | 3/2 | 3 | 3/2 | ⁴F_{3/2} | 4 |
| d⁴ | 4 | 4/10 | 2 | 2 | 0 | ⁵D₀ | 1 |
| d⁵ | 5 | 5/10 | 5/2 | 0 | 5/2 | ⁶S_{5/2} | 6 |
| d⁶ | 6 | 6/10 | 2 | 2 | 4 | ⁵D₄ | 9 |
| d⁷ | 7 | 7/10 | 3/2 | 3 | 9/2 | ⁴F_{9/2} | 10 |
| d⁸ | 8 | 8/10 | 1 | 3 | 4 | ³F₄ | 9 |
| d⁹ | 9 | 9/10 | ½ | 2 | 5/2 | ²D_{5/2} | 6 |

**Key:** dⁿ and d^{10-n} have same terms (complement rule)
- d¹ and d⁹: both ²D
- d² and d⁸: both ³F
- d⁵: ⁶S (half-filled, unique)

---

## 5. Ground State Terms for fⁿ Configurations

| Config | S | L | J | Term |
|--------|---|---|---|------|
| f¹ | ½ | 3 | 5/2 | ²F_{5/2} |
| f² | 1 | 5 | 4 | ³H₄ |
| f³ | 3/2 | 6 | 9/2 | ⁴I_{9/2} |
| f⁴ | 2 | 6 | 4 | ⁵I₄ |
| f⁵ | 5/2 | 5 | 5/2 | ⁶H_{5/2} |
| f⁶ | 3 | 3 | 0 | ⁷F₀ |
| f⁷ | 7/2 | 0 | 7/2 | ⁸S_{7/2} |
| f⁸ | 3 | 3 | 6 | ⁷F₆ |
| f⁹ | 5/2 | 5 | 15/2 | ⁶H_{15/2} |
| f¹⁰ | 2 | 6 | 8 | ⁵I₈ |
| f¹¹ | 3/2 | 6 | 15/2 | ⁴I_{15/2} |
| f¹² | 1 | 5 | 6 | ³H₆ |
| f¹³ | ½ | 3 | 7/2 | ²F_{7/2} |

**Key:** f⁷ is half-filled → ⁸S term

---

## 6. Selection Rules Summary

### Electric Dipole Transitions (L-S Coupling)

| Rule | Allowed Values | Forbidden |
|------|---------------|-----------|
| ΔS | 0 | ≠ 0 |
| ΔL | 0, ±1 | |ΔL| > 1 |
| ΔJ | 0, ±1 | |ΔJ| > 1, J=0↔J=0 |
| Δm_J | 0, ±1 | |Δm_J| > 1 |

### Single Electron Rules

| Rule | Allowed Values |
|------|---------------|
| Δl | ±1 only |
| Δm_l | 0, ±1 |

### Physical Basis

1. **ΔS = 0**: Electric dipole operator doesn't affect spin
2. **Δl = ±1**: Photon carries one unit of angular momentum
3. **ΔJ = 0, ±1**: Conservation of total angular momentum
4. **J=0 → J=0**: Forbidden by symmetry

---

## 7. Spin-Orbit Coupling Constants (Selected Atoms)

| Atom | Z | Ground Config | ζ (cm⁻¹) | Notes |
|------|---|---------------|----------|-------|
| H | 1 | 1s¹ | ~0 | Negligible |
| Li | 3 | 2s¹ | ~0.2 | Small |
| Na | 11 | 3s¹ | 17.2 | D-line splitting |
| K | 19 | 4s¹ | 38.5 | Larger splitting |
| Rb | 37 | 5s¹ | 158 | Heavy atom |
| Cs | 55 | 6s¹ | 370 | Very large |
| Hg | 80 | 6s² | ~5000 | Strong spin-orbit |

**Trend:** ζ increases with Z (heavier atoms have stronger spin-orbit coupling)

---

## 8. Fine Structure Examples

### Sodium D-Lines

| Transition | λ (nm) | E (cm⁻¹) | ΔE (cm⁻¹) |
|------------|--------|----------|-----------|
| ²P_{3/2} → ²S_{1/2} | 588.995 | 16973.4 | +17.2 |
| ²P_{1/2} → ²S_{1/2} | 589.592 | 16956.2 | 0 |

**Splitting:** 17.2 cm⁻¹ = 0.6 nm

### Hydrogen Fine Structure

For n=2 level:
- ²S_{1/2} and ²P_{1/2}: degenerate
- ²P_{3/2}: 0.365 cm⁻¹ higher

---

## 9. Complement Rule Summary

For a subshell with capacity n:
- pⁿ and p^{6-n} have same terms
- dⁿ and d^{10-n} have same terms
- fⁿ and f^{14-n} have same terms

**Reason:** Holes in a filled subshell behave like electrons

| Configuration | Equivalent To | Reason |
|--------------|---------------|--------|
| p⁵ | p¹ | One hole ≈ one electron |
| p⁴ | p² | Two holes ≈ two electrons |
| d⁹ | d¹ | One hole ≈ one electron |
| d⁸ | d² | Two holes ≈ two electrons |
| f¹³ | f¹ | One hole ≈ one electron |

---

## 10. Variational Method: Common Trial Functions

### Particle in a Box

| System | Trial Function | Parameters |
|--------|---------------|------------|
| 1D box | ψ = x(L-x) | None (fixed shape) |
| 1D box | ψ = x(L-x)e^{-αx²} | α (Gaussian decay) |
| 3D box | ψ = xyz(L-x)(L-y)(L-z) | None |

### Harmonic Oscillator

| System | Trial Function | Parameters |
|--------|---------------|------------|
| Ground state | ψ = e^{-αx²} | α (width) |
| First excited | ψ = xe^{-αx²} | α (width) |

### Hydrogen-like Atoms

| System | Trial Function | Parameters |
|--------|---------------|------------|
| 1 electron | ψ = e^{-ζr} | ζ (effective Z) |
| He atom | ψ = e^{-ζ(r₁+r₂)} | ζ (screening) |

---

## 11. Perturbation Theory: Common Systems

### Particle in a Box Perturbations

| Perturbation | First-Order E¹ | Exact? |
|-------------|----------------|--------|
| Constant V₀ | V₀ (exact) | Yes |
| Step V₀/2 | V₀/2 | No |
| Linear V=kx | 0 (by symmetry) | No |

### Harmonic Oscillator Perturbations

| Perturbation | E¹ (Ground) | Notes |
|-------------|-------------|-------|
| λx³ | 0 | Odd integrand |
| λx⁴ | 3λℏ²/(4m²ω²) | Positive shift |
| λx⁶ | Higher order | Need 2nd order |

---

## 12. Angular Momentum Formulas

### Magnitudes

| Quantity | Formula |
|----------|---------|
| \|L\| | √(L(L+1)) ℏ |
| \|S\| | √(S(S+1)) ℏ |
| \|J\| | √(J(J+1)) ℏ |

### Projection (z-component)

| Quantity | Range |
|----------|-------|
| L_z | m_L ℏ, where m_L = -L, ..., +L |
| S_z | m_S ℏ, where m_S = -S, ..., +S |
| J_z | m_J ℏ, where m_J = -J, ..., +J |

### Coupling

| Quantity | Formula |
|----------|---------|
| L·S | ½[J(J+1) - L(L+1) - S(S+1)] ℏ² |

---

## 13. Orbital Capacity and Microstates

| Orbital | l | m_l Values | Capacity | Spin States |
|---------|---|------------|----------|-------------|
| s | 0 | 0 | 2 | 1 orbital × 2 spins |
| p | 1 | -1, 0, +1 | 6 | 3 orbitals × 2 spins |
| d | 2 | -2, -1, 0, +1, +2 | 10 | 5 orbitals × 2 spins |
| f | 3 | -3, -2, -1, 0, +1, +2, +3 | 14 | 7 orbitals × 2 spins |

### Microstate Count Formula

For n electrons in orbital with capacity m:
```
Number of microstates = C(m, n) = m! / (n! × (m-n)!)
```

| Config | Formula | Microstates |
|--------|---------|-------------|
| p¹ | C(6,1) | 6 |
| p² | C(6,2) | 15 |
| p³ | C(6,3) | 20 |
| d² | C(10,2) | 45 |
| d⁵ | C(10,5) | 252 |

---

## Cross-References

- **L2:** `../L2_principles/quantum_approximations.md`
- **L3:** `../L3_functions/quantum_approximations_tools.py`
- **L5:** `../L5_examples/quantum_approximations/`
- **Source:** `../sources/ingestion/source-quantum_approximations-stepwise.md`
