# Multielectron Atoms — Zielinski Ch9

**Source:** Quantum States of Atoms and Molecules, Ch9

## Key Concepts

### 9.1–9.2 The Multi-Electron Problem
- Cannot solve SE analytically due to electron-electron repulsion: e²/r_{ij}
- **Independent electron approximation**: each electron in effective potential
- Product wavefunction: Ψ ≈ φ₁(r₁)φ₂(r₂)... (ignores correlation)

### 9.3 Perturbation Theory
- H = H⁰ + H' where H' is small perturbation
- First-order energy correction: E_n^(1) = ⟨ψ_n⁰|H'|ψ_n⁰⟩
- First-order wavefunction: ψ_n^(1) = Σ_{m≠n} ⟨ψ_m⁰|H'|ψ_n⁰⟩/(E_n⁰−E_m⁰) |ψ_m⁰⟩
- Applied to helium: H⁰ = two hydrogen-like, H' = e²/r₁₂

### 9.4 Variational Method
- E_trial ≥ E_exact (upper bound theorem)
- Optimize trial function parameters to minimize energy
- **Effective nuclear charge** Z_eff for helium: trial ψ = (Z_eff³/π)e^{−Z_eff r}
- Z_eff ≈ 27/16 = 1.6875 for He (vs Z=2)

### 9.5 Basis Functions / Single-Electron Wavefunctions
- **Slater-type orbitals (STOs)**: φ = r^{n-1}e^{−ζr}Y_l^m
- Effective nuclear charge ζ from Slater's rules
- **Gaussian-type orbitals (GTOs)**: φ = r^l e^{−αr²}Y_l^m (computationally efficient)

### 9.6 Pauli Exclusion & Slater Determinants
- **Pauli principle**: no two electrons in same spin-orbital
- **Slater determinant**: antisymmetric wavefunction
  Ψ = (1/√N!) det[φ_i(1) φ_j(2) ...]
- **Aufbau principle**: fill lowest energy orbitals first
- **Hund's rule**: maximize spin multiplicity for degenerate orbitals

### 9.7 Self-Consistent Field (Hartree-Fock)
- Each electron moves in average field of others
- Iterative SCF procedure to find optimal orbitals
- Fock operator: f_i = h + Σ_j (J_j − K_j)
- Coulomb operator J_j, exchange operator K_j
- Koopmans' theorem: −ε_i ≈ ionization energy

### 9.8 Configuration Interaction (CI)
- Hartree-Fock doesn't capture electron correlation
- CI: expand wavefunction in Slater determinants (excited configurations)
- Full CI = exact solution within basis set
- Correlation energy: E_exact − E_HF

### 9.9 Chemical Applications
- Periodic trends: ionization potential, atomic radius
- Shielding and effective nuclear charge
- Term symbols for multielectron atoms: Russell-Saunders coupling

## Key Formulas

| Formula | Description |
|---------|-------------|
| E_trial ≥ E_exact | Variational principle |
| Z_eff (Slater) | Effective nuclear charge from shielding |
| Ψ = (1/√N!) det[...] | Slater determinant |
| f_i = h + Σ(J_j − K_j) | Fock operator |
| E_corr = E_exact − E_HF | Correlation energy |

## Cross-References
- **L2:** electron_configurations.md, computational_quantum_chemistry.md, quantum_approximations.md, density_functional_theory.md
- **Problems:** `test_problems/textbook/zielinski_ch09_multielectron_atoms.json`
