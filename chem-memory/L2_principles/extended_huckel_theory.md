---
id: extended.huckel.theory
layer: 2
title: Extended Hückel Theory
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - ../L3_functions/advanced_quantum_tools.py
cross_links:
  - ./molecular_orbital_theory.md
  - ./mo_configurations.md
  - ./computational_quantum_chemistry.md
source: Quantum States of Atoms and Molecules (Zielinski et al.), Ch10.6
---

## Context
Extended Hückel Theory (EHT) is a simple semi-empirical molecular orbital method developed by Roald Hoffmann (1963). It extends the original Hückel method from π-systems to all valence electrons (σ and π) in any molecule, providing qualitative orbital energies and wavefunctions.

## The Secular Determinant

For a basis of N atomic orbitals $\{\phi_i\}$, the MO coefficients $\{c_i\}$ satisfy:

$$\mathbf{H}\mathbf{c} = E\mathbf{S}\mathbf{c}$$

This is the generalized eigenvalue problem. Expanding:

$$\begin{vmatrix}
H_{11} - ES_{11} & H_{12} - ES_{12} & \cdots \\
H_{21} - ES_{21} & H_{22} - ES_{22} & \cdots \\
\vdots & \vdots & \ddots
\end{vmatrix} = 0$$

Non-trivial solutions exist when the determinant vanishes → gives N MO energies $E_k$.

## Parameterization

### Diagonal Elements (Coulomb Integrals)

$$H_{ii} = -\text{IP}_i$$

Where $\text{IP}_i$ is the valence-state ionization potential of orbital $\phi_i$.

| Orbital | IP (eV) | Orbital exponent ζ |
|---------|---------|-------------------|
| H 1s | 13.6 | 1.30 |
| C 2s | 21.4 | 1.625 |
| C 2p | 11.4 | 1.625 |
| N 2s | 26.0 | 1.95 |
| N 2p | 13.4 | 1.95 |
| O 2s | 32.3 | 2.275 |
| O 2p | 15.8 | 2.275 |

### Off-Diagonal Elements: Wolfsberg-Helmholz Formula

$$H_{ij} = K\,S_{ij}\,\frac{H_{ii} + H_{jj}}{2}$$

Where:
- $K$ = empirical constant, typically **K = 1.75** (Hoffmann's original value)
- $S_{ij} = \langle \phi_i | \phi_j \rangle$ = overlap integral between STOs
- The factor $(H_{ii} + H_{jj})/2$ = arithmetic mean of diagonal elements

**Alternative formulations:**
- Geometric mean: $H_{ij} = K\sqrt{H_{ii} \cdot H_{jj}}\,S_{ij}$ (sometimes used)
- Modified Wolfsberg-Helmholz: $H_{ij} = K\,S_{ij}\,\frac{|H_{ii}| + |H_{jj}|}{2}$

### Overlap Integrals

Computed analytically for Slater-type orbitals (STOs):

$$\phi_i(\mathbf{r}) = N\,r^{n-1}e^{-\zeta r}\,Y_l^m(\theta, \phi)$$

Overlap $S_{ij}$ depends on:
- Distance between atoms
- Orbital types (s-s, s-p, p-p σ, p-p π)
- Orbital exponents $\zeta_i, \zeta_j$

## Procedure

1. **Choose basis**: All valence AOs for each atom (e.g., for CH₄: 1s on H, 2s + 2p on C = 9 basis functions)
2. **Compute overlap matrix S**: Evaluate $S_{ij}$ for all pairs
3. **Set diagonal H**: $H_{ii} = -\text{IP}_i$
4. **Compute off-diagonal H**: Wolfsberg-Helmholz formula
5. **Solve secular equation**: $\mathbf{Hc} = E\mathbf{Sc}$ → eigenvalues $E_k$ and eigenvectors $\mathbf{c}_k$
6. **Populate MOs**: Place electrons following Aufbau + Hund's rules
7. **Compute properties**: Total energy, charge distribution, orbital composition

## Strengths and Limitations

### Strengths
- Treats **all valence electrons** (σ and π) — unlike simple Hückel
- Works for **any geometry** — 3D structure required as input
- Provides **qualitative MO diagrams** for any molecule
- **No SCF** needed — single-shot calculation (very fast)
- Correctly predicts **Wade's rules**, **Walsh diagrams**, orbital symmetry

### Limitations
- **No electron-electron repulsion** beyond mean-field (fixed H matrix)
- **Total energy meaningless** — not variational
- **K = 1.75 is empirical** — results depend on this choice
- **Bond lengths and angles** are input, not optimized (no forces)
- Cannot describe **charge transfer** or **electron correlation** effects
- **Overestimates** antibonding-antibonding interactions

## Applications

- **Frontier Molecular Orbital (FMO) theory**: HOMO/LUMO analysis for pericyclic reactions
- **Walsh diagrams**: Correlate MO energies with geometry changes
- **Qualitative bonding analysis**: Why is CH₄ tetrahedral? (MO picture)
- **Metal clusters**: Electronic structure predictions
- **Teaching tool**: Introduces secular determinant and MO methods

## Connection to Hartree-Fock

EHT is a **non-iterative zeroth-order** approximation to Hartree-Fock:
- HF iterates H to include electron repulsion self-consistently; EHT uses fixed H
- EHT uses experimental IPs; HF computes them from first principles
- Both solve $\mathbf{Hc} = E\mathbf{Sc}$ → same mathematical framework

## Connection to Other Concepts
- Builds on H₂⁺ LCAO-MO framework (#h2_molecular_ion_lcao)
- Overlap integrals computed as in L3 tools (#advanced_quantum_tools)
- MO populations use Aufbau (#mo_configurations)
- Predecessor to more accurate methods (#computational_quantum_chemistry, #density_functional_theory)
