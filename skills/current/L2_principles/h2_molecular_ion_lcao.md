---
id: h2.molecular.ion.lcao
layer: 2
title: H₂⁺ Molecular Ion - LCAO-MO Theory
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - ../L3_functions/advanced_quantum_tools.py
cross_links:
  - ./molecular_orbital_theory.md
  - ./born_oppenheimer_approximation.md
  - ./quantum_mechanics.md
source: Quantum States of Atoms and Molecules (Zielinski et al.), Ch10.4
---

## Context
The H₂⁺ molecular ion (two protons, one electron) is the simplest molecule and the prototype for developing molecular orbital theory. Its exact solution exists but the LCAO-MO approximation provides the conceptual framework applicable to all molecules.

## The Electronic Hamiltonian

$$\hat{H}_{elec}(r, R) = -\frac{\hbar^2}{2m}\nabla^2 - \frac{e^2}{4\pi\epsilon_0 r_A} - \frac{e^2}{4\pi\epsilon_0 r_B} + \frac{e^2}{4\pi\epsilon_0 R}$$

Where:
- $r$ = electron coordinates
- $R$ = internuclear distance
- $r_A$, $r_B$ = electron distances to protons A, B
- Last term = nuclear repulsion (constant for fixed R under BO approximation)

## LCAO-MO Ansatz

$$\psi(r) = C_A 1s_A(r) + C_B 1s_B(r)$$

By symmetry ($|C_A|^2 = |C_B|^2$), two solutions:

### Bonding MO: $\psi_+ = C_+(1s_A + 1s_B)$
- Electron density **enhanced** between nuclei
- Charge accumulation pulls protons together

### Antibonding MO: $\psi_- = C_-(1s_A - 1s_B)$  
- Electron density **diminished** between nuclei (nodal plane)
- Cannot compensate nuclear repulsion

## Overlap Integral

$$S = \langle 1s_A | 1s_B \rangle = \int 1s_A^*(r) 1s_B(r) d\tau$$

- Range: 0 (R→∞) to 1 (R→0)
- Measures spatial overlap of basis functions
- Orthogonal functions have S = 0

## Normalization

$$C_\pm = [2(1 \pm S)]^{-1/2}$$

## Energy Expression

$$E_\pm = \frac{1}{1 \pm S}(H_{AA} \pm H_{AB})$$

### Coulomb Integral: $H_{AA}$
$$H_{AA} = \langle 1s_A | \hat{H}_{elec} | 1s_A \rangle = E_H + \frac{e^2}{4\pi\epsilon_0 R} + J$$

Where:
- $E_H$ = hydrogen atom energy (-13.6 eV)
- $J$ = electron-nucleus B attraction (negative, stabilizing)
- Physically: energy of electron around A interacting with proton B

### Resonance/Exchange Integral: $H_{AB}$
$$H_{AB} = \langle 1s_A | \hat{H}_{elec} | 1s_B \rangle = E_H S + \frac{e^2}{4\pi\epsilon_0 R}S + K$$

Where:
- $K$ = exchange integral (negative, stabilizing)
- Electron "exchanges" between A and B orbitals
- Key driver of covalent bonding

### Final Energy Decomposition
$$E_\pm = E_H + \frac{e^2}{4\pi\epsilon_0 R} + \frac{J \pm K}{1 \pm S}$$

| Component | Physical meaning |
|-----------|-----------------|
| $E_H$ | Isolated H atom energy |
| $e^2/(4\pi\epsilon_0 R)$ | Nuclear-nuclear repulsion |
| $J/(1\pm S)$ | Coulomb interaction contribution |
| $\pm K/(1\pm S)$ | Exchange (bonding/antibonding) contribution |

### Bonding Condition
For a stable molecule: $\frac{J + K}{1 + S}$ must be sufficiently negative to overcome $\frac{e^2}{4\pi\epsilon_0 R}$

## Key Physical Insights
1. **Bonding arises from electron density between nuclei** — not from orbitals "overlapping" per se
2. **Exchange integral K is uniquely quantum mechanical** — no classical analog
3. **Antibonding orbital is destabilized MORE** than bonding is stabilized (asymmetric splitting)
4. **Molecular orbitals form from atomic orbitals of matching symmetry**

## Connection to General MO Theory
- H₂⁺ establishes the LCAO-MO framework used for all molecules
- H_AA, H_AB, S matrices generalize to the secular determinant for N basis functions
- The qualitative picture (bonding/antibonding, sigma bonding from s+s) extends directly
