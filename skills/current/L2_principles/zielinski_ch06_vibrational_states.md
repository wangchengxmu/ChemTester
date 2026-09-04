# Vibrational States — Zielinski Ch6

**Source:** Quantum States of Atoms and Molecules, Ch6

## Key Concepts

### 6.1 Normal Modes and Normal Coordinates
- N atoms → 3N degrees of freedom
- Translational: 3, Rotational (nonlinear): 3, Vibrational: 3N−6
- Linear molecule: 3N−5 vibrational modes
- Normal modes: independent oscillations, each with own frequency

### 6.2 Classical Harmonic Oscillator
- Diatomic: reduced mass μ = m₁m₂/(m₁+m₂)
- V(x) = ½kx² (quadratic potential)
- Classical frequency: ν = (1/2π)√(k/μ)
- Solution: x(t) = A cos(2πνt + φ)

### 6.3 Quantum Harmonic Oscillator
- SE: −(ℏ²/2μ)(d²ψ/dx²) + ½kx²ψ = Eψ
- **Energy levels**: E_v = ℏω(v + ½), v = 0, 1, 2, ...
- ω = √(k/μ) = 2πν
- **Zero-point energy**: E₀ = ½ℏω
- **Equally spaced levels**: ΔE = ℏω

### 6.4 Harmonic Oscillator Wavefunctions
- ψ_v(x) = N_v H_v(ξ) e^{−ξ²/2} where ξ = √(α)x, α = μω/ℏ
- H_v(ξ) = Hermite polynomials
- **Turning points**: classical limit where E = V(x)
- Tunneling into classically forbidden region (ψ ≠ 0 beyond turning points)

### 6.5 Quantum Mechanical Tunneling
- Wavefunction penetrates into classically forbidden regions
- Probability decreases exponentially: ~e^{−2κx}
- Barrier penetration important in chemical reactions, scanning tunneling microscopy

### 6.6 Selection Rules
- **Δv = ±1** for harmonic oscillator
- Transition moment: M = ⟨ψ_{v'}|μ̂|ψ_v⟩
- Infrared activity requires changing dipole moment
- Fundamental transition (v=0→1) strongest

## Key Formulas

| Formula | Description |
|---------|-------------|
| E_v = ℏω(v + ½) | Vibrational energy levels |
| ω = √(k/μ) | Angular frequency |
| ψ_v = N_v H_v(√α x) e^{−αx²/2} | Wavefunctions |
| ΔxΔp ≥ ℏ/2 | Uncertainty principle |

## Cross-References
- **L2:** quantum_tunneling.md, molecular_spectroscopy.md, raman_spectroscopy.md
- **Problems:** `test_problems/textbook/zielinski_ch06_vibrational_states.json`
