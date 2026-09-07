# L2 Topic: Crystal Engineering Principles

**Source**: Expert knowledge; Desiraju, Crystal Engineering: A Holistic View (2007); G.R. Desiraju, Nature 2001
**Created**: 2026-03-24
**Status**: Pass-1

---

## Overview

Crystal engineering is the design and synthesis of crystalline solids with desired properties through understanding and manipulation of intermolecular interactions.

---

## Supramolecular Synthons

### Hydrogen Bond Motifs (Graph Set Notation: S_{a}(d))

| Motif | Description | Example |
|-------|-------------|---------|
| **R₂²(8)** | Carboxylic acid dimer (8-membered ring, 2 donors, 2 acceptors) | Benzoic acid dimer |
| **R₂²(8)** amide | Amide-amide hydrogen bond | Polypeptide β-sheet |
| **R₃³(6)** | Triple H-bond (e.g., cyanuric acid·melamine) | DAT·DAN complex |
| **R₂¹(6)** | Intramolecular H-bond ring | ortho-substituted phenols |
| **C(4)** | Chain motif | 4-aminobenzoic acid catemers |

### Other Interactions

| Interaction | Energy (kJ/mol) | Directionality | Example |
|-------------|-----------------|----------------|---------|
| **O–H···O** (strong H-bond) | 20-40 | High | Carboxylic acid dimer |
| **N–H···O** | 15-30 | Moderate | Amide β-sheet |
| **O–H···N** | 15-30 | Moderate |
| **π-π stacking** | 5-10 | Moderate (offset preferred) | Graphite, aromatic systems |
| **C–H···π** | 2-5 | Low | Alkane-arene |
| **Halogen bonding** (C–X···O/N) | 10-40 | High (linear C–X···Y) | I₂···pyridine, pharmaceutical cocrystals |
| **Chalcogen bonding** | 10-50 | Moderate-High | S/Se···O interactions |

---

## Cocrystals

- **Definition**: Multi-component crystalline material where API + conformer are in neutral form
- **Supramolecular synthon approach**: Choose conformer based on complementary H-bonding
- **Common conformers**: Carboxylic acids (succinic, fumaric), amides (nicotinamide), saccharin
- **Pharmaceutical examples**: Carbamazepine·saccharin, ibuprofen·nicotinamide
- **Methods**: Solution crystallization, neat grinding, LAG, slurry

---

## Polymorphism

- Same molecule → different crystal packing → different properties (solubility, bioavailability, stability)
- Famous case: Ritonavir (Abbott) — Form II appeared with 50% lower solubility, caused drug withdrawal
- **Conformational polymorphism**: Different molecular conformations in different forms
- **Packing polymorphism**: Same conformation, different packing
- **Prediction**: CSP (Crystal Structure Prediction) using computational methods (DFT-D, force fields, Monte Carlo)

---

## Crystal Structure Prediction (CSP)

1. Generate possible crystal packings (CrystalPredictor, Genarris)
2. Energy rank using DFT-D (dispersion-corrected DFT)
3. Compare with experimental PXRD
4. Challenges: flexible molecules, entropy, kinetics vs. thermodynamics

---

## Tools
- **Mercury** (CCDC): Visualization, H-bond analysis, powder pattern simulation
- **CrystalExplorer**: Hirshfeld surface analysis, interaction energies
- **CSD** (Cambridge Structural Database): ~1.2M structures for knowledge mining
- **Materials Studio / VASP**: DFT for CSP
