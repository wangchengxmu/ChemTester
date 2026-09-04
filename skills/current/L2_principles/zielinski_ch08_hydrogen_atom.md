# The Hydrogen Atom — Zielinski Ch8

**Source:** Quantum States of Atoms and Molecules, Ch8

## Key Concepts

### 8.1 The Schrödinger Equation
- Two-particle system → reduced mass μ = m_e m_p/(m_e + m_p) ≈ m_e
- Coulomb potential: V(r) = −e²/(4πε₀r) = −Ze²/r (in atomic units)
- Separation in spherical coordinates: R(r)Y_l^{m_l}(θ,φ)

### 8.2 The Wavefunctions
- **Hydrogen orbitals**: ψ_{nlm}(r,θ,φ) = R_{nl}(r)Y_l^{m_l}(θ,φ)
- **Radial functions** R_{nl}(r): involve associated Laguerre polynomials
- Three quantum numbers: n (principal), l (angular momentum), m_l (magnetic)
- n = 1,2,3,...; l = 0,...,n−1; m_l = −l,...,+l
- **s, p, d, f...** notation: l=0,1,2,3...

### 8.3 Energy Levels and Spectroscopy
- **E_n = −13.6 eV/n²** (hydrogen) = −μe⁴Z²/(2ℏ²n²)
- Only depends on n (accidental degeneracy)
- Selection rules: Δl = ±1, Δm_l = 0, ±1
- **Spectral series**: Lyman (→1), Balmer (→2), Paschen (→3), Brackett (→4)

### 8.4 Magnetic Properties — Zeeman Effect
- Orbital magnetic moment: μ_L = −(e/2m_e)L
- Interaction with B field: ΔE = m_l μ_B B (normal Zeeman)
- μ_B = eℏ/(2m_e) = Bohr magneton = 9.274×10⁻²⁴ J/T

### 8.5 Electron Spin
- **Intrinsic angular momentum**: s = ½
- Spin quantum numbers: m_s = ±½
- Spin magnetic moment: μ_s ≈ −2μ_B (g-factor ≈ 2)
- Stern-Gerlach experiment evidence

### 8.6 Other One-Electron Systems
- He⁺, Li²⁺, etc: E_n = −13.6Z²/n² eV
- Same wavefunctions, scaled by Z

### 8.7 Spin-Orbitals and Configurations
- Complete description: ψ = φ(x,y,z)α or φ(x,y,z)β
- α = spin-up, β = spin-down spin functions

### 8.8 Spectroscopic Term Symbols
- Coupling L + S → J
- Term symbol: ^{2S+1}L_J
- Fine structure from spin-orbit coupling

## Cross-References
- **L2:** bohr_model.md, electron_configurations.md, atomic_theory_and_subatomic_structure.md
- **Problems:** `test_problems/textbook/zielinski_ch08_hydrogen_atom.json`
