---
id: mo.configurations
layer: 2
title: Molecular Orbital Configurations
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - ../L3_functions/advanced_quantum_tools.py
cross_links:
  - ./molecular_orbital_theory.md
  - ./h2_molecular_ion_lcao.md
  - ./electron_configurations.md
  - ./extended_huckel_theory.md
source: Quantum States of Atoms and Molecules (Zielinski et al.), Ch10.2
---

## Context
Molecular orbital (MO) configurations extend the atomic Aufbau principle to molecules. Electrons occupy MOs in order of increasing energy, following Hund's rules and the Pauli exclusion principle. The Slater determinant formalism provides the proper antisymmetric many-electron wavefunction.

## Molecular Orbital Ordering

For homonuclear diatomics (O₂ and lighter, Li₂–N₂):

$$\sigma_{1s} < \sigma^*_{1s} < \sigma_{2s} < \sigma^*_{2s} < \pi_{2p_x} = \pi_{2p_y} < \sigma_{2p_z} < \pi^*_{2p_x} = \pi^*_{2p_y} < \sigma^*_{2p_z}$$

For O₂, F₂, Ne₂ (heavier diatomics):

$$\sigma_{1s} < \sigma^*_{1s} < \sigma_{2s} < \sigma^*_{2s} < \sigma_{2p_z} < \pi_{2p_x} = \pi_{2p_y} < \pi^*_{2p_x} = \pi^*_{2p_y} < \sigma^*_{2p_z}$$

The crossover occurs because s-p mixing is significant for light atoms but negligible for heavier ones.

## Electron Configuration Notation

Format: $(\sigma_{1s})^2(\sigma^*_{1s})^2 \cdots$

### Examples

| Molecule | Configuration | Bond Order | Magnetic |
|----------|--------------|------------|----------|
| H₂ | $(\sigma_{1s})^2$ | 1 | Diamagnetic |
| He₂ | $(\sigma_{1s})^2(\sigma^*_{1s})^2$ | 0 | — (unstable) |
| Li₂ | $(\sigma_{2s})^2$ | 1 | Diamagnetic |
| Be₂ | $(\sigma_{2s})^2(\sigma^*_{2s})^2$ | 0 | — (unstable) |
| B₂ | $(\sigma_{2s})^2(\sigma^*_{2s})^2(\pi_{2p})^2$ | 1 | Paramagnetic |
| C₂ | $(\sigma_{2s})^2(\sigma^*_{2s})^2(\pi_{2p})^4$ | 2 | Diamagnetic |
| N₂ | $(\sigma_{2s})^2(\sigma^*_{2s})^2(\pi_{2p})^4(\sigma_{2p})^2$ | 3 | Diamagnetic |
| O₂ | $(\sigma_{2s})^2(\sigma^*_{2s})^2(\sigma_{2p})^2(\pi_{2p})^4(\pi^*_{2p})^2$ | 2 | Paramagnetic |
| F₂ | $(\sigma_{2s})^2(\sigma^*_{2s})^2(\sigma_{2p})^2(\pi_{2p})^4(\pi^*_{2p})^4$ | 1 | Diamagnetic |

### Bond Order

$$\text{Bond order} = \frac{n_{\text{bonding}} - n_{\text{antibonding}}}{2}$$

- Fractional bond orders possible (e.g., NO: 2.5)
- Bond order correlates with bond length and dissociation energy

## Slater Determinant

For N electrons in spin-orbitals $\chi_i$:

$$\Psi(1,2,\ldots,N) = \frac{1}{\sqrt{N!}}
\begin{vmatrix}
\chi_1(1) & \chi_2(1) & \cdots & \chi_N(1) \\
\chi_1(2) & \chi_2(2) & \cdots & \chi_N(2) \\
\vdots & \vdots & \ddots & \vdots \\
\chi_1(N) & \chi_2(N) & \cdots & \chi_N(N)
\end{vmatrix}$$

### Properties
- **Antisymmetric**: swapping any two electrons changes the sign
- **Pauli principle**: two electrons cannot occupy the same spin-orbital (determinant = 0)
- **Normalized** when spin-orbitals are orthonormal
- Compact notation: $|\chi_1 \chi_2 \cdots \chi_N\rangle$

### Excited Configurations
- **Singlet excitation**: paired electrons → one promoted, spins paired
- **Triplet excitation**: paired electrons → one promoted, parallel spins (lower energy by exchange)
- **Configuration interaction (CI)**: mixing multiple determinants improves energy

## Hund's Rules for Molecules
1. **Maximize total spin** S (parallel spins in degenerate orbitals → lower exchange energy)
2. **Maximize orbital angular momentum** L (for atoms); for molecules: maximize degeneracy
3. O₂ ground state: $^3\Sigma_g^-$ (triplet — two unpaired electrons in $\pi^*$)

## Connection to Other Concepts
- Bond order → correlates with bond strength (#26 bond_strengths)
- Magnetic properties → arise from unpaired electrons in MOs
- MO configurations are the starting point for Hartree-Fock (#125 computational_quantum_chemistry)
- Extended Hückel theory populates MOs using this framework (#extended_huckel_theory)
