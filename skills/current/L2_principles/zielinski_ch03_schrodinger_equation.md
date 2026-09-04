# The Schrödinger Equation — Zielinski Ch3

**Source:** Quantum States of Atoms and Molecules, Ch3

> This chapter covers the general Schrödinger equation and postulates. The particle-in-a-box application was previously extracted as `physchem_LT_ch3_particleinbox.json`.

## Sections

### 3.1 Introduction
- Wave-like properties → need a wave equation (Schrödinger equation)
- Wavefunction ψ(x,t) describes quantum systems

### 3.2 Classical Wave Equation
- ∂²u/∂x² = (1/v²) ∂²u/∂t²
- Starting from ψ = A sin(kx − ωt), taking derivatives

### 3.3 Invention of the Schrödinger Equation
- Total energy: E = KE + PE = p²/2m + V(x)
- Replace p → −iℏ(d/dx) and E → iℏ(∂/∂t)
- **Time-dependent SE**: −(ℏ²/2m)(∂²ψ/∂x²) + V(x)ψ = iℏ(∂ψ/∂t)
- **Time-independent SE**: −(ℏ²/2m)(d²ψ/dx²) + V(x)ψ = Eψ

### 3.4 Operators, Eigenfunctions, Eigenvalues
- **Laplacian**: ∇² = ∂²/∂x² + ∂²/∂y² + ∂²/∂z²
- Operator equation: Âψ = aψ (eigenvalue equation)

### 3.5 Momentum Operators
- **Position**: x̂ψ = xψ
- **Momentum**: p̂ψ = −iℏ(dψ/dx)
- **Kinetic energy**: T̂ψ = −(ℏ²/2m)(d²ψ/dx²)
- **Hamiltonian**: Ĥ = T̂ + V̂

### 3.6 Time-Dependent Schrödinger Equation
- Full form with time dependence
- Separation of variables: ψ(x,t) = φ(x)e^(−iEt/ℏ)

### 3.7 Meaning of the Wavefunction
- Born interpretation: |ψ|² = probability density
- Normalization: ∫|ψ|²dx = 1

### 3.8 Expectation Values
- ⟨A⟩ = ∫ψ*Âψ dτ
- Variance: σ² = ⟨A²⟩ − ⟨A⟩²

### 3.9 Postulates of Quantum Mechanics
1. System described by wavefunction ψ
2. Observable → Hermitian operator
3. Measurement yields eigenvalue; system collapses to eigenstate
4. Time evolution by TDSE
5. Wavefunction antisymmetric under particle exchange (for fermions)

## Cross-References
- **L2:** quantum_mechanics.md, quantum_theory.md, quantum_approximations.md
- **Related extraction:** `physchem_LT_ch3_particleinbox.json`
- **Problems:** `test_problems/textbook/zielinski_ch03_schrodinger_equation.json`

## L3 Tool Call Directives

**Source:** `schrodinger_tools.py`

⚠️ Stub file — no public functions implemented yet.

### Available functions:
- *(none — file is empty)*
