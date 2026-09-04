# Rotational States — Zielinski Ch7

**Source:** Quantum States of Atoms and Molecules, Ch7

## Key Concepts

### 7.1–7.2 The Rigid Rotor Model
- Diatomic molecule as rigid rotor: fixed internuclear distance R
- Moment of inertia: I = μR² (μ = reduced mass)
- Rotational kinetic energy: E_rot = L²/(2I)

### 7.3 Solving the Rigid Rotor Schrödinger Equation
- Hamiltonian: Ĥ = −(ℏ²/2I)∇²
- Solved in spherical coordinates → separation of variables
- Solutions: **spherical harmonics** Y_J^{m_J}(θ,φ)
- **Energy levels**: E_J = ℏ²J(J+1)/(2I) = BJ(J+1)
- B = ℏ²/(2I) = rotational constant

### 7.4 Angular Momentum
- L²|J,m⟩ = J(J+1)ℏ²|J,m⟩
- L_z|J,m⟩ = m_J ℏ|J,m⟩
- J = 0, 1, 2, ... ; m_J = −J, ..., +J
- 2J+1 degeneracy for each J level

### 7.5 Properties of Rotating Molecules
- Probability density from |Y_J^{m_J}|²
- Classical vs quantum correspondence
- Centrifugal distortion (non-rigid correction): D_J J²(J+1)²

### 7.6 Rotational Spectroscopy
- Selection rules: **ΔJ = ±1** (for dipole-allowed transitions)
- Only polar molecules have pure rotational spectra
- **Transition energies**: ΔE = E_{J+1} − E_J = 2B(J+1)
- Equally spaced lines (2B apart) in microwave/far-IR
- Bond length determination from B: R = √(ℏ²/(2μB))

## Key Formulas

| Formula | Description |
|---------|-------------|
| E_J = BJ(J+1) | Rigid rotor energy levels |
| B = ℏ²/(2I) = h/(8π²cI) | Rotational constant |
| ΔE = 2B(J+1) | Transition energy |
| I = μR² | Moment of inertia |
| ΔJ = ±1 | Rotational selection rule |

## Cross-References
- **L2:** rotational_spectroscopy.md, molecular_spectroscopy.md
- **Problems:** `test_problems/textbook/zielinski_ch07_rotational_states.json`
