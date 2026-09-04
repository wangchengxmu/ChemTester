# Translational States — Zielinski Ch5

**Source:** Quantum States of Atoms and Molecules, Ch5

## Key Concepts

### 5.1 The Free Particle
- V(x) = 0 everywhere (or constant, set to zero)
- SE: −(ℏ²/2m)(d²ψ/dx²) = Eψ
- Solutions: ψ(x) = Ae^{ikx} + Be^{−ikx} where k = √(2mE)/ℏ
- **No quantization**: E = ℏ²k²/2m — continuous energy spectrum
- Not normalizable (non-bound state) → use wave packets / Dirac delta normalization

### 5.2 The Uncertainty Principle
- ΔxΔp ≥ ℏ/2
- Consequence of wave nature of matter
- Narrower wavefunction in space → broader momentum distribution
- Heisenberg microscope thought experiment

### 5.3 Linear Combinations of Eigenfunctions
- Superposition: ψ = Σ c_n φ_n
- Time evolution: ψ(t) = Σ c_n φ_n e^{−iE_n t/ℏ}
- **Non-stationary states**: probability density changes with time
- Measurement: |c_n|² = probability of finding system in state n
- Completeness relation: Σ |φ_n⟩⟨φ_n| = 1

## Cross-References
- **L2:** quantum_mechanics.md, quantum_tunneling.md
- **Problems:** `test_problems/textbook/zielinski_ch05_translational_states.json`
