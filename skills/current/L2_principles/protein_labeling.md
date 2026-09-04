---
id: protein_labeling
layer: 2
title: Protein Labeling (Site-Specific, Fluorescent)
parent: ../L1_ontology/chemistry-core-map.md#entry-276
stability: high
confidence: high
last_verified: 2026-03-28
source: LibreTexts Biological Chemistry, chemical biology literature
down_links:
  - ../L3_functions/chemical_biology_tools.py
---

# Protein Labeling

## Core Concept

Site-specific protein labeling attaches chemical reporters (fluorophores, affinity tags, isotopic labels) to defined positions on proteins, enabling visualization, pull-down, and structural studies in vitro and in living cells.

---

## Labeling Strategies

### 1. Cysteine Labeling
- **Reagents:** maleimides, iodoacetamides, haloacetamides
- **Reaction:** Michael addition to free Cys thiol
- **Requirement:** unique, solvent-accessible Cys (often engineered)
- **Selectivity:** over Lys/His at pH 6.5-7.5

### 2. Lysine Labeling
- **Reagents:** NHS esters, isothiocyanates, sulfonyl fluorides
- **Reaction:** amide formation with ε-amino group
- **Issue:** multiple Lys residues → heterogeneous labeling
- **NHS esters:** fast, pH 8-9 optimal

### 3. Sortase-Mediated Ligation
- **Recognition motif:** LPXTG (C-terminus)
- **Enzyme:** Sortase A from S. aureus
- **Reaction:** transpeptidation — replaces C-terminal Gly with oligoglycine probe
- **Mild conditions:** 25-37°C, aqueous, Ca²⁺-dependent

### 4. Enzyme-Mediated Labeling (Self-Labeling Tags)

| Tag | Substrate | Mechanism |
|-----|-----------|-----------|
| SNAP-tag | O⁶-benzylguanine | AGT transfer |
| CLIP-tag | O²-benzylcytosine | AGT transfer |
| HaloTag | Chloroalkane | SN2 displacement |
| APEX | Biotin-phenol | Peroxidative |
| TurboID | Biotin | Biotion ligase |

### 5. Unnatural Amino Acid (UAA) Incorporation
- **Methods:** amber codon suppression, genetic code expansion
- **Handles:** azide (AzF), alkyne (Hpg), ketone, tetrazine
- **Bioorthogonal:** enables SPAAC, CuAAC, IEDDA labeling

### 6. Biotinylation Strategies
- **Chemical:** NHS-PEGₙ-biotin, maleimide-biotin
- **Enzymatic:** BirA (biotin ligase), TurboID (engineered biotin ligase)
- **Application:** streptavidin pull-down, ChIP, proximity labeling

---

## Fluorophore Considerations

### Key Properties
- **Excitation/Emission:** spectral range
- **Brightness:** ε × Φ (extinction coeff × quantum yield)
- **Photostability:** resistance to photobleaching
- **Size:** organic dye (<1 kDa) vs fluorescent protein (>25 kDa)

### Common Dyes
| Dye | λ_ex (nm) | λ_em (nm) | Notes |
|-----|-----------|-----------|-------|
| FITC | 495 | 519 | Classic green |
| Cy3 | 550 | 570 | Bright orange |
| Cy5 | 650 | 670 | Far-red |
| Alexa Fluor 647 | 650 | 665 | Photostable |
| BODIPY | varies | varies | Small, bright |
| TAMRA | 555 | 580 | Red, pH-sensitive |

---

## Links

- L3: `../L3_functions/chemical_biology_tools.py`
- L4: `../L4_reference/chemical_biology_reference.csv`
