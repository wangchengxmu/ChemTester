---
id: chem.molecular_spectroscopy_advanced
layer: 2
title: Molecular Spectroscopy (Advanced) - Rovibrational, Electronic, and Group Theory Applications
source: LibreTexts Physical Chemistry Ch13
status: active
created: 2026-03-18
last_verified: 2026-03-18
---

# Molecular Spectroscopy (Advanced)

**L1 Parent:** spectroscopy.md, quantum_mechanics_core.md

## Overview

Spectroscopy is the area of science concerned with the absorption, emission, and scattering of electromagnetic radiation by atoms and molecules. This advanced module covers rovibrational coupling, anharmonicity, electronic spectra, selection rules from quantum mechanics, and group theory applications.

## Key Concepts

### 1. Rovibrational Spectroscopy

**Combined rotational-vibrational transitions:**
- Vibrational transitions accompanied by rotational transitions
- Selection rules: Îv = Â±1, ÎJ = Â±1
- P-branch (ÎJ = -1), R-branch (ÎJ = +1)
- Q-branch (ÎJ = 0) allowed for some molecules

**Unequal spacings:**
- Rotational-vibrational coupling: B_v = B_e - Î±_e(v + Â½)
- Centrifugal distortion: E_J = BJ(J+1) - DJÂ²(J+1)Â²
- R-branch spacing decreases with J
- P-branch spacing increases with decreasing J

### 2. Anharmonicity and Overtones

**Beyond harmonic oscillator:**
```
G(v) = Ïâ?v + Â½) - Ïâxâ?v + Â½)Â² + Ïâyâ?v + Â½)Â³ + ...
```

**Vibrational overtones:**
- Fundamental: Î½Ìââ?= Ïâ?- 2Ïâxâ?- First overtone: Î½Ìââ?= 2Ïâ?- 6Ïâxâ?- Second overtone: Î½Ìââ?= 3Ïâ?- 12Ïâxâ?- Overtones weaker than fundamentals

### 3. Electronic Spectroscopy

**Electronic transitions contain:**
- Electronic energy change (largest)
- Vibrational fine structure
- Rotational fine structure (often unresolved)

**Franck-Condon Principle:**
- Electronic transitions occur faster than nuclear motion
- Vertical transitions on potential energy surfaces
- Transition probability â?overlap integral between vibrational wavefunctions
- Franck-Condon factors determine vibronic band intensities

### 4. Time-Dependent Perturbation Theory

**Foundation for spectroscopy:**
- Time-independent perturbation: static Hamiltonians
- Time-dependent perturbation: dynamic Hamiltonians, state evolution
- Transition probability between states
- Fermi's Golden Rule for transition rates

### 5. Selection Rules

**From quantum mechanics:**
- Dipole moment operator determines allowed transitions
- Integration over wavefunctions must be nonzero
- Symmetry constraints from group theory

**Rotational selection rules:**
- Rigid rotor: ÎJ = Â±1
- Requires permanent dipole moment
- Nonpolar molecules: no pure rotational spectra

**Vibrational selection rules:**
- Harmonic oscillator: Îv = Â±1
- Requires change in dipole moment
- Anharmonicity allows Îv = Â±2, Â±3 (overtones)

**Electronic selection rules:**
- Spin: ÎS = 0 (spin-forbidden if violated)
- Orbital: Îl = Â±1
- Laporte: g â?u (centrosymmetric molecules)

### 6. Group Theory and Spectroscopy

**Determining IR and Raman activity:**
- IR active: dipole moment changes (transform as x, y, z)
- Raman active: polarizability changes (transform as xÂ², yÂ², zÂ², xy, xz, yz)
- Character tables show irreducible representations

**Mutual exclusion rule:**
- Centrosymmetric molecules (with inversion center)
- IR active modes: ungerade (u) symmetry
- Raman active modes: gerade (g) symmetry
- No mode can be both IR and Raman active

### 7. Normal Modes in Polyatomic Molecules

**Vibrational degrees of freedom:**
- Nonlinear molecules: 3N - 6
- Linear molecules: 3N - 5
- Each normal mode is independent

**Symmetry classification:**
- Normal modes classified by irreducible representations
- Water (Câv): 3 modes - 2Aâ?+ Bâ?- Use character tables to determine activity

### 8. Rotational Spectra of Polyatomic Molecules

**Molecular classification:**
- Linear: one moment of inertia (I), 2 rotational degrees
- Spherical tops: I_A = I_B = I_C (e.g., CHâ? SFâ? - no dipole, no pure rotation spectrum
- Symmetric tops: I_A â?I_B = I_C
  - Prolate: I_A < I_B (e.g., CHâCl)
  - Oblate: I_A > I_B (e.g., BFâ?
- Asymmetric tops: I_A â?I_B â?I_C (most complex spectra)

---

## Key Equations

### Rovibrational Energy
```
E(v,J) = Ïâ?v + Â½) - Ïâxâ?v + Â½)Â² + BJ(J+1) - DJÂ²(J+1)Â²
```

### Rotational-Vibrational Coupling
```
B_v = B_e - Î±_e(v + Â½)

P-branch: Î½Ì_P(J) = Ïâ?- 2B_eJ - Î±_eJ(J+1)
R-branch: Î½Ì_R(J) = Ïâ?+ 2B_e(J+1) - Î±_e(J+1)(J+2)
```

### Franck-Condon Factor
```
FCF = |â¨Ï_v'|Ï_v''â©|Â²

where Ï_v' = final state vibrational wavefunction
      Ï_v'' = initial state vibrational wavefunction
```

### Anharmonic Frequency
```
Î½Ì_obs = Ïâ?- 2Ïâxâ?(fundamental)
Î½Ì_obs = 2Ïâ?- 6Ïâxâ?(first overtone)
```

---

## Problem Types

1. **Rovibrational spectrum analysis** - Identify P, Q, R branches, extract B and Ï values
2. **Anharmonicity calculations** - Determine Ïâ?and Ïâxâ?from overtone frequencies
3. **Selection rule determination** - Use group theory to predict IR/Raman activity
4. **Electronic spectrum interpretation** - Apply Franck-Condon principle
5. **Polyatomic molecule spectra** - Classify by symmetry, predict active modes

---

## Cross-References

**L1:** `../L1_ontology/chemistry-core-map.md`

**L2:**
- `molecular_spectroscopy.md` - Rotational, vibrational, Raman basics
- `quantum_mechanics_core.md` - SchrÃ¶dinger equation, perturbation theory
- `spectroscopy.md` - General spectroscopy principles

**Source:** LibreTexts Physical Chemistry Ch13: Molecular Spectroscopy
- https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/Physical_Chemistry_(LibreTexts)/13%3A_Molecular_Spectroscopy

---

## Subtopics Covered

| Topic | Description |
|-------|-------------|
| 13.1 | Electromagnetic Spectrum |
| 13.2 | Rotations Accompany Vibrational Transitions |
| 13.3 | Unequal Spacings in Vibration-Rotation Spectra |
| 13.4 | Unequal Spacings in Pure Rotational Spectra |
| 13.5 | Vibrational Overtones |
| 13.6 | Electronic Spectra |
| 13.7 | Franck-Condon Principle |
| 13.8 | Rotational Spectra of Polyatomic Molecules |
| 13.9 | Normal Modes in Polyatomic Molecules |
| 13.10 | Irreducible Representation of Point Groups |
| 13.11 | Time-Dependent Perturbation Theory |
| 13.12 | Selection Rule for Rigid Rotor |
| 13.13 | Harmonic Oscillator Selection Rule |
| 13.14 | Group Theory Determines Infrared Activity |

---

*L2 Principle Document*
*Generated: 2026-03-18*
*Source: LibreTexts Physical Chemistry Ch13*


## Implementations

- Implementation: `../L3_functions/laser_photochemistry_tools.py`
