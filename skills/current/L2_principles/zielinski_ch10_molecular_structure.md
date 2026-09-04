# Theories of Electronic Molecular Structure — Zielinski Ch10

**Source:** Quantum States of Atoms and Molecules, Ch10

## Key Concepts

### 10.1 Born-Oppenheimer Approximation
- Separate electronic and nuclear motion
- Nuclei fixed → solve electronic SE → potential energy surface (PES)
- Valid because m_nucleus >> m_electron
- **Related L2:** born_oppenheimer_approximation.md

### 10.2 Orbital Approximation
- Molecular orbitals (MOs) as building blocks
- Slater determinant for antisymmetric wavefunction
- **Related L2:** mo_configurations.md, molecular_orbital_theory.md

### 10.3 Basis Functions
- MOs expressed as LCAO: ψ_i = Σ_μ C_{μi} χ_μ
- **Minimal basis**: one AO per occupied AO of constituent atoms
- **Split-valence / double-zeta**: multiple functions per AO for flexibility
- Polarization functions (d on C, p on H); diffuse functions for anions
- **Related L2:** computational_quantum_chemistry.md

### 10.4 H₂⁺ Molecular Ion (LCAO-MO)
- Simplest molecule: two protons, one electron
- Bonding MO: ψ_+ = (1s_A + 1s_B)/√(2+2S)
- Antibonding MO: ψ_- = (1s_A − 1s_B)/√(2−2S)
- Overlap integral S = ⟨1s_A|1s_B⟩
- **Related L2:** h2_molecular_ion_lcao.md

### 10.5 Homonuclear Diatomic Molecules
- MO energy level diagram: σ(1s) < σ*(1s) < σ(2s) < σ*(2s) < π(2p) < σ(2p) < π*(2p) < σ*(2p)
- Bond order = ½(n_bonding − n_antibonding)
- O₂, N₂, F₂, Li₂ electronic configurations
- **Related L2:** molecular_orbital_theory.md

### 10.6 Semi-Empirical Methods — Extended Hückel
- Hückel theory for π-systems only
- Extended Hückel: all valence electrons
- Parameters from experiment (not ab initio)
- **Related L2:** extended_huckel_theory.md

### 10.7 Mulliken Populations
- Charge analysis: population on each atom
- **Overlap population**: bond order between atoms
- **Gross population**, **net charge**: P_A = Σ_i N_i Σ_μ∈A (C_{μi})²

### 10.8–10.9 SCF, HF, and Correlation for Molecules
- Same concepts as atomic HF (Ch9) but for molecules
- Roothaan-Hall equations: FC = SCε (matrix form)
- Correlation energy and CI methods
- Post-HF: MP2, CCSD(T), CASSCF

## Key Formulas

| Formula | Description |
|---------|-------------|
| ψ_i = Σ C_{μi} χ_μ | LCAO-MO expansion |
| Bond order = ½(n_b − n_a) | MO bond order |
| FC = SCε | Roothaan-Hall equations |

## Cross-References
- **L2:** born_oppenheimer_approximation.md, molecular_orbital_theory.md, h2_molecular_ion_lcao.md, extended_huckel_theory.md, computational_quantum_chemistry.md, density_functional_theory.md
- **Problems:** `test_problems/textbook/zielinski_ch10_molecular_structure.json`
