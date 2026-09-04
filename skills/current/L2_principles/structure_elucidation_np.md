---
id: structure_elucidation_np
layer: 2
title: Structure Elucidation of Natural Products (NMR, MS, IR)
parent: ../L1_ontology/chemistry-core-map.md#entry-286
stability: high
confidence: high
last_verified: 2026-03-24
source: Roberts & Caserio Ch30, spectroscopy literature
---

# Structure Elucidation of Natural Products

## Core Concept

Determining the structure of a newly isolated natural product combines isolation techniques with spectroscopic methods (NMR, MS, IR, UV) and often X-ray crystallography.

---

## Workflow

1. **Extraction:** solvent extraction of biological material
2. **Isolation:** chromatography (column, HPLC, TLC)
3. **Purity assessment:** analytical HPLC, NMR
4. **Molecular formula:** HRMS (high-resolution mass spectrometry)
5. **Functional groups:** IR, UV-Vis
6. **Skeleton & connectivity:** 1D/2D NMR
7. **Stereochemistry:** NOE, CD, ORD, X-ray
8. **Confirmation:** synthesis or comparison with literature

---

## Mass Spectrometry

### HRMS → Molecular Formula
- Accurate mass to 4-5 decimal places
- C, H, N, O composition from mass defect

### Key Ion Types
- **M⁺⁺** (EI, molecular ion)
- **[M+H]⁺** (ESI+, soft ionization)
- **[M-H]⁻** (ESI-, for acidic compounds)
- **[M+Na]⁺** (common adduct)

### Fragmentation Patterns
- α-cleavage next to heteroatoms
- McLafferty rearrangement
- Retro-Diels-Alder in steroidal systems

---

## NMR of Natural Products

### ¹H NMR
- Chemical shifts: functional group identification
- Coupling constants: stereochemistry (J values)
- Integration: proton count

### ¹³C NMR
- Number of unique carbons
- DEPT: CH₃/CH₂/CH/quaternary
- Chemical shift ranges: sp³ (0-90 ppm), sp² (100-220 ppm)

### 2D NMR (Essential for Structure)
| Experiment | Connects | Information |
|-----------|----------|-------------|
| COSY | H-H | Through-bond H coupling |
| HSQC/HMQC | H-C (1-bond) | Direct C-H connectivity |
| HMBC | H-C (2-3 bond) | Long-range connectivity |
| NOESY/ROESY | H-H (through-space) | Stereochemistry |

---

## X-ray Crystallography
- **Gold standard** for absolute configuration (with anomalous scattering)
- Requires single crystal of suitable quality
- Gives bond lengths, angles, and absolute stereochemistry

---

## Links

- L3: `../L3_functions/natural_products_tools.py`
- L4: `../L4_reference/natural_products_reference.csv`
