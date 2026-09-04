id: chem.computational_qc
layer: 2
title: Computational Quantum Chemistry
source: LibreTexts Physical Chemistry Ch11
status: active
created: 2026-03-14
last_verified: 2026-03-14
---

# Computational Quantum Chemistry

**L1 Parent:** quantum_mechanics.md

## Problem Types

1. **Hartree-Fock Calculation** - Self-consistent field for molecular systems
2. **Basis Set Selection** - Choose appropriate basis for accuracy/cost trade-off
3. **Slater Determinant** - Construct antisymmetric wavefunctions
4. **Orbital Energy Calculation** - Compute MO energies from variational method
5. **Basis Set Evaluation** - Compare minimal, split-valence, polarized, diffuse
6. **DFT Functional Selection** - Choose exchange-correlation functional
7. **Electron Correlation** - Post-HF methods for correlation energy

## Decision Tree

### 1. What computational method is appropriate?

- **Quick estimate, small molecule** → Hartree-Fock with minimal basis (STO-3G)
- **Medium accuracy** → HF with split-valence (6-31G)
- **Accurate geometry** → HF with polarization (6-31G*)
- **Anions, Rydberg states** → Add diffuse functions (6-31+G*)
- **Electron correlation needed** → DFT, MP2, or coupled cluster
- **Bond energies** → Post-HF methods with correlation

### 2. Hartree-Fock Method

- **SCF procedure:** Iterate until self-consistent orbitals
- **Energy:** E = ⟨Ψ|Ĥ|Ψ⟩/⟨Ψ|Ψ⟩ minimized
- **HF limit:** Lowest energy with single determinant
- **Restricted HF:** Same spatial orbitals for α and β spins
- **Unrestricted HF:** Different spatial orbitals for different spins

### 3. Basis Set Selection

```
Accuracy vs Cost Trade-off:

Minimal (STO-3G)          < Split-valence (6-31G) < Polarized (6-31G*)
                                 ↓
Diffuse (6-31+G*)         < Triple-zeta (6-311G) < Correlation-consistent

Increasing accuracy →
Increasing cost →
```

**Selection criteria:**

| System Type | Recommended Basis | Reason |
|-------------|-------------------|--------|
| Neutral molecules | 6-31G | Balanced accuracy/cost |
| Geometry optimization | 6-31G* | Polarization for bonds |
| Anions | 6-31+G* | Diffuse for tail |
| H-bonding | 6-31+G** | Diffuse on H |
| Transition metals | Larger basis | d-electron complexity |
| High accuracy needed | 6-311G(2df,2pd) | Multiple polarization |

### 4. Slater Determinant Construction

**Two-electron system:**
```
Ψ(r₁,r₂) = (1/√2)|φ₁α(r₁)  φ₁β(r₁)|
                    |φ₁α(r₂)  φ₁β(r₂)|
```

**N-electron system:**
```
Ψ = (1/√N!)|χ₁(r₁)α  χ₁(r₁)β  ...  χ_{N/2}(r₁)β|
           |χ₁(r₂)α  χ₂(r₂)β  ...  χ_{N/2}(r₂)β|
           |   ⋮         ⋮         ⋮         |
           |χ₁(r_N)α  χ₂(r_N)β  ...  χ_{N/2}(r_N)β|
```

**Properties:**
- Antisymmetric under particle exchange
- Automatically satisfies Pauli exclusion
- Normalization: (N!)^{-1/2}

### 5. Orbital Energy Calculation

**Variational method:**
```
E = ⟨Ψ|Ĥ|Ψ⟩ / ⟨Ψ|Ψ⟩

Minimize E by varying orbital coefficients c_{ij}
```

**MO as linear combination:**
```
ψᵢ = Σⱼ c_{ij} φⱼ

where φⱼ = basis functions (contracted Gaussians)
```

### 6. Basis Set Notation

**STO-nG (Minimal):**
- n = number of Gaussians per STO
- STO-3G, STO-4G, STO-6G

**Split-valence (N-MPG):**
- N = core primitives
- M = inner valence primitives
- P = outer valence primitives
- G = Gaussian type
- Examples: 3-21G, 6-31G, 6-311G

**Polarization:**
- * or (d): Add d functions to heavy atoms
- ** or (d,p): Add p functions to H/He also

**Diffuse:**
- + or aug-: Add diffuse functions to heavy atoms
- ++: Add diffuse to H/He also

### 7. DFT Functional Selection

**Functional hierarchy:**

| Type | Description | Examples |
|------|-------------|----------|
| LDA | Local density only | SVWN |
| GGA | Density + gradient | BLYP, PBE |
| Hybrid | Mix HF exchange | B3LYP, PBE0 |
| Meta-GGA | Include kinetic energy | TPSS |
| Double hybrid | Include MP2 correlation | B2PLYP |

**Selection guide:**
- General use: B3LYP/6-31G*
- Thermochemistry: PBE0
- Transition metals: TPSSh
- Weak interactions: ωB97X-D

### 8. Electron Correlation Methods

**Post-Hartree-Fock hierarchy:**

```
HF → MP2 → CCSD → CCSD(T) → Full CI
 ↑      ↑       ↑         ↑
Low cost, low accuracy → High cost, high accuracy

Correlation energy recovery:
MP2: ~80-90%
CCSD: ~95-98%
CCSD(T): ~99% (gold standard)
```

**Method selection:**
- MP2: Small systems, medium accuracy
- CCSD(T): High accuracy, small systems
- DFT: Large systems, reasonable accuracy

### 9. Check Constraints

- Pauli principle: Antisymmetric wavefunction required
- Variational principle: E_trial ≥ E_true always
- Basis set completeness: More functions → better accuracy
- Computational cost: Exponential scaling with system size
- Spin contamination: Check ⟨S²⟩ in unrestricted calculations

---

## Section 1: Hartree-Fock Method

### Self-Consistent Field (SCF)

**Algorithm:**
1. Guess initial MO coefficients c_{ij}
2. Construct Fock matrix F
3. Solve Fock equations: Fψ = εψ
4. Update MO coefficients
5. Check convergence: |E_new - E_old| < threshold
6. If not converged, go to step 2

**Energy formula:**
```
E = Σᵢ ⟨φᵢ|h|φᵢ⟩ + ½ Σᵢⱼ [⟨φᵢφⱼ|φᵢφⱼ⟩ - ⟨φᵢφⱼ|φⱼφᵢ⟩]

where:
h = one-electron operator (kinetic + nuclear attraction)
⟨φᵢφⱼ|φᵢφⱼ⟩ = Coulomb integral J
⟨φᵢφⱼ|φⱼφᵢ⟩ = Exchange integral K
```

### Fock Operator

```
F̂(1) = ĥ(1) + Σⱼ [Ĵⱼ(1) - K̂ⱼ(1)]

where:
ĥ(1) = -½∇² - Σ_A Z_A/r_{1A}
Ĵⱼ(1) = ∫φⱼ*(2)φⱼ(2)/r₁₂ dτ₂  (Coulomb)
K̂ⱼ(1)φᵢ(1) = ∫φⱼ*(2)φᵢ(2)/r₁₂ dτ₂ φⱼ(1)  (Exchange)
```

### Hartree-Fock Equations

**Fock equations:**
```
F̂φᵢ = εᵢφᵢ

εᵢ = orbital energy
φᵢ = molecular orbital
```

**Koopmans' theorem:**
```
IP ≈ -ε_HOMO
EA ≈ -ε_LUMO (approximately)
```

---

## Section 2: Basis Sets

### Slater-Type Orbitals (STO)

**Radial function:**
```
R(r) = N r^{n-1} e^{-ζr}

Properties:
- Correct cusp at nucleus
- Exponential decay at large r
- Computationally difficult
```

### Gaussian-Type Orbitals (GTO)

**Radial function:**
```
G(r) = N r^{n-1} e^{-αr²}

Properties:
- Flat at nucleus (wrong)
- Gaussian decay (too fast)
- Computationally fast
```

**Solution: Contracted Gaussians**
```
S_G(r) = Σⱼ Cⱼ e^{-αⱼr²}

Fit multiple Gaussians to match STO shape
```

### Minimal Basis Sets

**STO-nG:**
- n Gaussians fit to each STO
- One function per atomic orbital
- Examples: STO-3G, STO-6G

**Advantages:**
- Computationally cheap
- Useful for initial structures

**Disadvantages:**
- Limited flexibility
- Poor accuracy for bonding

### Split-Valence Basis Sets

**Double-zeta:**
```
φ₂s = C₁·STO(ζ₁) + C₂·STO(ζ₂)

ζ₁ > ζ₂: Large ζ → inner region
         Small ζ → outer region
```

**Notation N-MPG:**
- N = core orbital primitives
- M, P = valence split (double-zeta)
- Example: 6-31G = 6 core, 3+1 valence

**Triple-zeta:**
- 6-311G: Core 6, valence 3+1+1
- Even more flexibility

### Polarization Functions

**Purpose:**
- Allow orbital shape distortion
- Account for charge polarization
- Essential for bonding accuracy

**Notation:**
- * or (d): Add d orbitals to atoms with p valence
- ** or (d,p): Also add p orbitals to H
- (2df,2pd): Multiple polarization functions

**Example: Water with 6-31G***
```
O: 1s, 2s, 2p + d functions (polarization)
H: 1s + p functions (polarization)

Result: Bent geometry correctly described
```

### Diffuse Functions

**Purpose:**
- Describe electron density tail
- Important for anions, Rydberg states
- Weak interactions (hydrogen bonds)

**Notation:**
- + or aug-: Add to heavy atoms
- ++: Add to all atoms including H

**Example:**
```
6-31+G*: 6-31G* + diffuse on heavy atoms
aug-cc-pVTZ: Dunning augmented set
```

---

## Section 3: Density Functional Theory (DFT)

### Kohn-Sham Equations

**Total energy:**
```
E[ρ] = T_s[ρ] + V_ne[ρ] + J[ρ] + E_xc[ρ]

where:
T_s = kinetic energy (non-interacting)
V_ne = nuclear-electron attraction
J = Coulomb repulsion
E_xc = exchange-correlation (unknown)
```

**Kohn-Sham equations:**
```
[-½∇² + V_eff(r)]φᵢ(r) = εᵢφᵢ(r)

V_eff(r) = V_ne(r) + ∫ρ(r')/|r-r'| dr' + V_xc(r)
```

### Exchange-Correlation Functionals

**LDA (Local Density Approximation):**
```
E_xc^{LDA}[ρ] = ∫ρ(r)ε_xc(ρ(r)) dr

Uses only local density
Good for uniform electron gas
Overbinds molecules
```

**GGA (Generalized Gradient Approximation):**
```
E_xc^{GGA}[ρ] = ∫f(ρ(r), ∇ρ(r)) dr

Uses density and gradient
Better for molecules
Examples: BLYP, PBE
```

**Hybrid Functionals:**
```
E_xc^{hybrid} = a·E_x^{HF} + (1-a)·E_x^{DFT} + E_c^{DFT}

Mix exact HF exchange with DFT
B3LYP: 20% HF exchange
PBE0: 25% HF exchange
```

---

## Section 4: Electron Correlation

### Correlation Energy

**Definition:**
```
E_corr = E_exact - E_HF

HF captures ~99% of energy
Correlation energy is ~1% but crucial for:
- Bond dissociation
- Transition states
- Weak interactions
```

### Configuration Interaction (CI)

**Wavefunction:**
```
Ψ_CI = c₀Ψ_HF + Σ_{ia} c_i^a Ψ_i^a + Σ_{ijab} c_{ij}^{ab} Ψ_{ij}^{ab} + ...

where:
Ψ_i^a = singly excited determinant
Ψ_{ij}^{ab} = doubly excited determinant
```

**Levels:**
- CIS: Singles only (excited states)
- CISD: Singles and doubles
- Full CI: All excitations (exact within basis)

### Møller-Plesset Perturbation Theory

**MP2 (second order):**
```
E_MP2 = Σ_{ijab} |⟨ij||ab⟩|² / (ε_i + ε_j - ε_a - ε_b)

where:
i, j = occupied orbitals
a, b = virtual orbitals
⟨ij||ab⟩ = two-electron integral
```

**Cost:** O(N⁵) - affordable for medium systems

**Accuracy:** Recovers ~80-90% of correlation energy

### Coupled Cluster Methods

**Exponential ansatz:**
```
Ψ_CC = e^T̂ Ψ_HF

T̂ = T₁ + T₂ + T₃ + ...

T₁ = Σ_{ia} t_i^a a^†_a a_i  (singles)
T₂ = Σ_{ijab} t_{ij}^{ab} a^†_a a^†_b a_j a_i  (doubles)
```

**Methods:**
- CCSD: Singles and doubles (O(N⁶))
- CCSD(T): Perturbative triples (O(N⁷))
  - "Gold standard" for quantum chemistry
  - ~99% of correlation energy

---

## Section 5: Molecular Orbital Analysis

### Orbital Ordering (Carbon Monoxide Example)

**From HF calculation:**

| MO | Composition | Type | Energy |
|----|-------------|------|--------|
| 1σ | 0.94·1s_O | Nonbonding | Lowest |
| 2σ | 0.92·1s_C | Nonbonding | |
| 3σ | 0.72·2s_O + 0.28·2s_C | Bonding | |
| 4σ | 0.37·2s_C + 0.54·2p_O | Antibonding | |
| 1π | 0.32·2p_C + 0.44·2p_O | Bonding | Degenerate |
| 5σ | 0.38·2s_C - 0.38·2p_C | Nonbonding | HOMO |

**Bond order:**
```
Bond order = ½(N_bonding - N_antibonding)
           = ½(8 - 2) = 3

Triple bond: C≡O
```

**Why CO binds via C:**
- 5σ HOMO is nonbonding lone pair on carbon
- Largest amplitude on carbon away from oxygen
- Donates electrons from carbon to metal

---

## Section 6: Computational Workflow

### Standard HF/DFT Calculation

```
1. Choose method and basis set
   Method: HF, B3LYP, MP2, etc.
   Basis: 6-31G*, aug-cc-pVTZ, etc.

2. Build molecular geometry
   Cartesian coordinates or Z-matrix

3. Run calculation
   SCF optimization
   Geometry optimization (optional)

4. Analyze results
   - Total energy
   - Orbital energies (HOMO, LUMO)
   - Mulliken charges
   - Dipole moment
   - Vibrational frequencies (if optimized)

5. Validate
   - Check convergence
   - Verify structure is minimum (no imaginary frequencies)
   - Compare with experimental data
```

### Basis Set Convergence

```
Strategy: Start small, increase until convergence

STO-3G → 6-31G → 6-31G* → 6-311G** → aug-cc-pVTZ

Monitor:
- Total energy (should decrease)
- Key property of interest
- Stop when change < desired threshold
```

---

## Key Formulas Summary

| Topic | Formula | Notes |
|-------|---------|-------|
| Slater determinant | Ψ = (N!)^{-1/2}∥χᵢ(rⱼ)∥ | Antisymmetric |
| Variational energy | E = ⟨Ψ\|Ĥ\|Ψ⟩/⟨Ψ\|Ψ⟩ | Upper bound |
| Fock operator | F̂ = ĥ + Σⱼ(Ĵⱼ - K̂ⱼ) | One-electron |
| STO radial | R(r) = Nr^{n-1}e^{-ζr} | Cusp at nucleus |
| GTO radial | G(r) = Nr^{n-1}e^{-αr²} | Efficient integrals |
| Contracted Gaussian | S = ΣⱼCⱼe^{-αⱼr²} | Fit to STO |
| KS energy | E = T_s + V_ne + J + E_xc | DFT |
| MP2 energy | E₂ = Σ\|⟨ij\|\|ab⟩\|²/(ε_i+ε_j-ε_a-ε_b) | Correlation |

---

## Related L2 Nodes

- `quantum_mechanics_core.md` - Schrödinger equation foundation
- `quantum_approximations.md` - Variational and perturbation methods
- `molecular_orbital_theory.md` - MO theory for bonding
- `statistical_mechanics.md` - Partition functions

---

## L3 Tool Implementations

See: `L3_functions/computational_qc_tools.py`

**Functions:**
- `hartree_fock_energy()` - HF energy calculation
- `basis_set_info()` - Basis set properties lookup
- `sto_ng_exponent()` - STO-nG exponent values
- `electron_correlation_energy()` - Post-HF correlation
- `functional_type()` - DFT functional classification

---

## L4 Reference Tables

See: `../L4_reference/basis_sets_table.md`

**Contents:**
- Complete basis set listing
- Exponent values for common basis sets
- Polarization and diffuse function details
- Functional type classification

---

## L5 Worked Examples

See: `L5_worked_examples/computational_qc_examples.md`

**Examples:**
- HF calculation for H₂
- Basis set comparison for H₂O
- CO orbital analysis
- DFT vs HF for bond energies

---

*Source: LibreTexts Physical Chemistry, Chapter 11*
*Last updated: 2026-03-14*

---

## L3 Tool Call Directives

**Source:** computational_chemistry_tools.py
DFT energy, rotational spectroscopy, molecular dynamics, QSAR, Lennard-Jones, Boltzmann distribution.

### Available functions:
- dft_energy_calculator(kinetic_energy, electron_nuclear_attraction, coulomb_energy, exchange_correlation_energy, nuclear_repulsion) → dict — Total KS-DFT energy E_KS = T_s + V_ne + J + E_xc + E_nn (Hartree)
- exchange_correlation_function(rho, grad_rho, functional_type, rho_cutoff) → dict — XC energy/potential for LDA/GGA/hybrid functionals
- 
otational_constant_calculator(masses, coordinates, units) → dict — Rotational constants A, B, C (cm⁻¹) from geometry
- 
otational_partition_function(rotational_constants, temperature, symmetry_number, molecule_type) → dict — Q_rot at given T
- md_integrator(positions, velocities, forces, masses, dt, integrator) → dict — One Velocity-Verlet/leapfrog MD step
- kinetic_energy_calculator(velocities, masses, units) → dict — KE and instantaneous temperature
- descriptor_calculator(molecular_weight, logP, h_bond_donors, ...) → dict — Lipinski/Veber descriptors, druglikeness
- qsar_model_builder(X, y, method, n_components, cross_validate) → dict — MLR/PLS/PCR model with R², Q², RMSE
- lennard_jones(r, epsilon, sigma) → dict — LJ potential and force
- oltzmann_distribution(energies, temperature) → ndarray — Population probabilities
- 
otational_energy(J, B, D) → dict — E_J = BJ(J+1) - DJ²(J+1)² in cm⁻¹
- 	ransition_frequency(J_lower, B, D) → dict — ν = 2B(J+1) - 4D(J+1)³ in cm⁻¹
- j_max(B, T) → dict — Most populated J level
- 
otational_constant(I) → dict — B from moment of inertia (kg·m²)
- moment_of_inertia(m1, m2, r) → dict — I = μr² for diatomic

### Common errors:
- ❌ Mixing units in MD (nm/ps for GROMACS vs m/s for SI)
- ❌ Using DFT XC functional name incorrectly (case-sensitive: 'B3LYP' not 'b3lyp')

---

**Source:** computational_qc_tools.py
Hartree-Fock, basis sets, DFT functional classification, electron correlation (MP2, CCSD).

### Available functions:
- hartree_fock_energy(n_electrons, orbital_energies, core_electrons) → float — HF energy from orbital energies (Hartree)
- slater_determinant_normalization(n_electrons) → float — (N!)^(-1/2)
- ock_matrix_element(h_ij, density, coulomb_integrals, exchange_integrals, i, j) → float — Fock matrix element
- koopmans_ionization_potential(orbital_energy) → float — IP ≈ -ε_HOMO (eV)
- asis_set_info(basis_name) → dict — Properties of STO-3G, 6-31G*, cc-pVDZ, etc.
- sto_ng_exponent(n, zeta, element) → list — Gaussian exponents for STO-nG
- count_basis_functions(formula, basis_name) → int — Total basis functions for molecule
- unctional_type(functional_name) → dict — Classify DFT functional (LDA/GGA/hybrid/meta-GGA/range-separated)
- dft_functional_hierarchy() → dict — All functionals grouped by type
- electron_correlation_energy(method, hf_energy, exact_energy, correlation_fraction) → float — E_corr (Hartree)
- mp2_energy_contribution(occupied_energies, virtual_energies, two_electron_integrals) → float — MP2 correction
- parse_basis_notation(notation) → dict — Parse Pople notation (e.g., '6-311+G**')
- 
ecommend_basis_set(system_type, property_of_interest, accuracy) → list — Basis set recommendations

### Common errors:
- ❌ Forgetting that Koopmans' theorem only applies to HF (not DFT) orbital energies
- ❌ Using minimal basis (STO-3G) for geometry optimization — use at least 6-31G*

## L3 Tool Call Directives

**Source:** dft_tools.py
Density Functional Theory helper functions: XC energy, Kohn-Sham energy, screening length.

### Available functions:
- exchange_correlation_energy(n: float, rs: float, functional='LDA') → float — XC energy per particle; LDA: Dirac exchange + Wigner correlation
- kohn_sham_energy(ekin: float, vh: float, vxc: float, exc: float) → float — E_KS = T_s + V_H + V_xc + E_xc
- screening_length(fermi_wavenumber: float) → float — Thomas-Fermi screening length = 1/(2k_F)

### Common errors:
- ❌ Only 'LDA' functional is implemented; others raise ValueError
- ❌ rs = (3/(4πn))^(1/3) must be pre-calculated, not passed as n directly
