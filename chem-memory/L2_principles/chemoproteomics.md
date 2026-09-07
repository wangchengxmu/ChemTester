---
id: chemoproteomics
layer: 2
title: Chemoproteomics (ABPP, Cysteine Profiling)
parent: ../L1_ontology/chemistry-core-map.md#entry-277
stability: high
confidence: high
last_verified: 2026-03-28
source: LibreTexts Biological Chemistry, chemical biology literature
down_links:
  - ../L3_functions/chemical_biology_tools.py
---

# Chemoproteomics

## Core Concept

Chemoproteomics combines chemical probes with mass spectrometry to profile protein function, interactions, and ligandability on a proteome-wide scale. It bridges chemistry and proteomics.

---

## Activity-Based Protein Profiling (ABPP) — Proteomic Scale

### Competitive ABPP (C-ABPP)
1. Treat living cells with candidate inhibitor at various concentrations
2. Lyse cells, treat lysate with broad-spectrum activity probe
3. Enrich labeled proteins (click chemistry to biotin → streptavidin)
4. LC-MS/MS quantification (SILAC or TMT)
5. Dose-response → IC₅₀ values for each protein target

### Applications
- **Target deconvolution:** identify off-targets of drugs
- **Lead optimization:** assess selectivity across protein families
- **Phenotypic screening:** discover bioactive compounds from phenotypic assays

---

## Cysteine Profiling (IsoTOP-ABPP)

### Principle
Cysteine residues are nucleophilic and often functionally important. IsoTOP-ABPP uses cysteine-reactive probes to quantify cysteine reactivity and ligandability across the proteome.

### Workflow
1. Treat proteome with broad cysteine probe (e.g., iodoacetamide-alkyne, IA-alkyne)
2. Click to biotin-azide, enrich, trypsin digest
3. LC-MS/MS identifies labeled cysteines
4. **With inhibitor:** pre-treat cells, reduced labeling → identifies ligandable cysteines
5. Calculate **ligandability score** (ratio of labeled/unlabeled peptide intensities)

### Key Finding
~70% of cysteines are not ligandable; covalent ligands target a specific subset of hyper-reactive cysteines.

---

## Thermal Proteome Profiling (TPP / CETSA-MS)

### Principle
Ligand binding stabilizes proteins against thermal denaturation.

### Method
1. Heat cell lysates (or intact cells) at gradient temperatures
2. Separate soluble (folded) from insoluble (denatured) proteins
3. LC-MS/MS quantification
4. Protein with shifted T_m → likely bound by ligand

### Applications
- Target engagement in cells
- Off-target profiling
- MOA studies

---

## Proteolysis Targeting Chimeras (PROTACs)

### Principle
Bifunctional molecule: target ligand + E3 ligase ligand → induced protein degradation.

$$\text{Target} + \text{PROTAC} + \text{E3 Ligase} \rightarrow \text{Ubiquitination} \rightarrow \text{Proteasomal Degradation}$$

### Key Metrics
- **DC₅₀:** concentration for 50% degradation
- **D_max:** maximum degradation percentage
- **Hook effect:** at high [PROTAC], binary complexes compete with ternary

---

## Links

- L3: `../L3_functions/chemical_biology_tools.py`
- L4: `../L4_reference/chemical_biology_reference.csv`
