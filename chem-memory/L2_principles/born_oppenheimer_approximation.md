---
id: born.oppenheimer.approximation
layer: 2
title: Born-Oppenheimer Approximation
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - ../L3_functions/advanced_quantum_tools.py
cross_links:
  - ./quantum_mechanics.md
  - ./molecular_orbital_theory.md
  - ./h2_molecular_ion_lcao.md
source: Quantum States of Atoms and Molecules (Zielinski et al.), Ch10.1
---

## Context
The Born-Oppenheimer (BO) approximation is the foundational separation of nuclear and electronic motion in molecular quantum mechanics. It underpins the concept of a potential energy surface (PES) and makes molecular structure calculations tractable.

## Core Idea

The molecular Hamiltonian contains kinetic energy operators for all nuclei and electrons, plus all Coulomb interactions:

$$\hat{H} = \hat{T}_{nuc} + \hat{T}_{elec} + V_{nn} + V_{ne} + V_{ee}$$

### Key Approximation
Because nuclei are ~1836× heavier than electrons, electrons move much faster. The BO approximation:
1. **Fixes nuclei** at positions R (clamped-nuclei Hamiltonian)
2. **Solves electronic Schrödinger equation** for each nuclear geometry
3. **Electronic energy** becomes the potential for nuclear motion

### Clamped-Nuclei Electronic Hamiltonian

$$\hat{H}_{elec}(\mathbf{r}; \mathbf{R}) = \hat{T}_{elec} + V_{ne}(\mathbf{r}, \mathbf{R}) + V_{ee}(\mathbf{r})$$

The total energy at geometry R: $E_{total}(R) = E_{elec}(R) + V_{nn}(R)$

### The Potential Energy Surface (PES)
- $E_{elec}(R) + V_{nn}(R)$ plotted vs nuclear coordinates = PES
- Equilibrium geometry = minimum on PES
- Vibrational frequencies = curvature at minimum
- Transition states = saddle points

### Non-adiabatic Coupling (breakdown)
The BO approximation neglects terms coupling electronic and nuclear motion:
$$\hat{H}_{non-adiabatic} = -\sum_I \frac{\hbar^2}{M_I} \nabla_I \cdot \langle \psi_{elec} | \nabla_I \psi_{elec} \rangle$$
Important for: conical intersections, photochemistry, proton transfer, Jahn-Teller effect.

### Validity
- Excellent for ground states near equilibrium
- Breaks down where electronic energy surfaces approach (avoided crossings, conical intersections)
- Nuclear kinetic energy is smaller than electronic energy gaps → BO holds

## Connection to Other Concepts
- LCAO-MO theory assumes BO to define molecular orbitals at fixed R
- Molecular dynamics simulations often use BO PES
- Franck-Condon principle relies on vertical transitions (fixed nuclei)
