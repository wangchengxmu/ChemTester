---
id: bioorthogonal_reactions
layer: 2
title: Bioorthogonal Reactions (SPAAC, CuAAC, Tetrazine Ligation)
parent: ../L1_ontology/chemistry-core-map.md#entry-274
stability: high
confidence: high
last_verified: 2026-03-28
source: Bertozzi & Raines, ACS Chem Biol (review PMC2908729), LibreTexts Biological Chemistry
down_links:
  - ../L3_functions/chemical_biology_tools.py
---

# Bioorthogonal Reactions

## Core Concept

Bioorthogonal reactions are chemical transformations that can occur inside living systems without interfering with native biochemical processes. They proceed rapidly under mild, aqueous conditions without cross-reacting with biological functional groups.

---

## Requirements for Bioorthogonality
1. **Selectivity:** no cross-reaction with biological functional groups (–OH, –NH₂, –SH, COOH)
2. **Rate:** fast kinetics (k > 10⁻³ M⁻¹s⁻¹, ideally > 1 M⁻¹s⁻¹)
3. **Mild conditions:** aqueous, pH 7.4, 37°C
4. **Biocompatibility:** non-toxic, cell-permeable (for intracellular)
5. **Orthogonal handles:** not found in biology

---

## Key Bioorthogonal Reactions

### 1. CuAAC — Copper-Catalyzed Azide-Alkyne Cycloaddition
$$\text{R-N}_3 + \text{R'-C≡CH} \xrightarrow{\text{Cu(I)}} \text{1,4-triazole}$$

- **Rate:** k ≈ 10-100 M⁻¹s⁻¹ (Cu-catalyzed)
- **Problem:** Cu(I) cytotoxic → NOT suitable for live cells
- **Use:** fixed cells, in vitro labeling

### 2. SPAAC — Strain-Promoted Azide-Alkyne Cycloaddition
$$\text{R-N}_3 + \text{BCN (or DIBAC)} \rightarrow \text{triazole}$$

- **Mechanism:** cyclooctyne ring strain drives reaction without Cu
- **Rate:** k ≈ 0.1-1 M⁻¹s⁻¹ (DIBAC), up to 3.5 M⁻¹s⁻¹ (BCN)
- **Advantage:** Cu-free, cell-compatible
- **Trade-off:** slower than CuAAC

### 3. Tetrazine Ligation (IEDDA — Inverse-Electron Demand Diels-Alder)
$$\text{tetrazine} + \text{trans-cyclooctene (TCO)} \rightarrow \text{dihydropyridazine} + N_2$$

- **Rate:** k ≈ 10³-10⁶ M⁻¹s⁻¹ (TCO-tetrazine is the fastest bioorthogonal pair)
- **Mechanism:** [4+2] cycloaddition followed by retro-Diels-Alder (N₂ elimination)
- **Advantage:** ultra-fast, no catalyst needed
- **Use:** in vivo pretargeted imaging, rapid labeling

### 4. Oxime/Hydrazone Ligation
$$\text{R-CHO} + \text{R'-NH}_2\text{OH} \rightarrow \text{oxime} + \text{H}_2\text{O}$$

- **Rate:** k ≈ 10⁻³-10⁻⁴ M⁻¹s⁻¹ (slow)
- **Acceleration:** aniline catalysis (10-50×)

### 5. Norbornene-Tetrazine (SPOCQ)
- **Rate:** k ≈ 10⁶ M⁻¹s⁻¹
- **Very fast but norbornene less stable than TCO**

---

## Rate Comparison

| Reaction | Second-order rate (M⁻¹s⁻¹) | Cu-free? |
|----------|---------------------------|----------|
| Tetrazine-TCO | 10³-10⁶ | ✓ |
| SPAAC (DIBAC-N₃) | 0.1-1 | ✓ |
| CuAAC | 10-100 | ✗ |
| Oxime ligation | 10⁻³-10⁻⁴ | ✓ |

---

## Protein Labeling Strategies (enhanced from review literature)

### Self-Labeling Tags
- **SNAP-tag** (20 kDa): Reacts with O⁶-benzylguanine derivatives
- **CLIP-tag**: Mutant of SNAP-tag, reacts with O²-benzylcytosine → orthogonal labeling
- **HaloTag** (33 kDa): Reacts with chloroalkane substrates; versatile but larger tag
- **Application**: Fusion protein expression → selective labeling with fluorophores, biotin, crosslinkers

### Non-Canonical Amino Acid (ncAA) Incorporation
- **Genetic code expansion**: Amber stop codon suppression to incorporate bioorthogonal handles
- **Examples**: Azido-homoalanine (AHA), homopropargylglycine (HPG), Norbornene-lysine, TCO-lysine
- **Advantage**: Site-specific, minimal perturbation (single atom change)
- **Limitation**: Low expression yields, requires engineered tRNA/tRNA synthetase

### Bioorthogonal Chemistry in Cellular Organelles
- Challenge: bioorthogonal reagents must cross organelle membranes
- Mitochondria: TPP-conjugated tetrazines for mitochondrial protein labeling
- Nucleus: Cell-permeable small tetrazine/TCO pairs
- Lysosome: pH considerations (acidic environment can affect reaction rates)

## Source Context & Cross-References
- No dedicated bioorthogonal chemistry chapter on LibreTexts (emerging field, mostly primary literature)
- LibreTexts Biological Chemistry hub covers general chemical biology topics: nucleic acids, DNA repair, bioconjugate chemistry, peptides, glycoscience, biomolecular structure, imaging, biological catalysis
- Related LibreTexts content: Protein labeling, conjugation chemistry modules
- Cross-reference: `chemical_probes.md` for complementary targeting strategies
- Cross-reference: `glycobiology.md` for metabolic oligosaccharide engineering applications
- Key primary sources: Bertozzi lab (copper-free click), Sharpless lab (click chemistry)

---

## Links

- L3: `../L3_functions/chemical_biology_tools.py`
- L4: `../L4_reference/chemical_biology_reference.csv`
- L5: `../L5_examples/chemical_biology_examples.md`

---

## [Source: Wikipedia, Bioorthogonal Chemistry]
### Bertozzi Bioorthogonal Reactions (Key Criteria)
1. Selective: Does not react with biological functional groups.
2. Fast: Kinetic rate constants > 10⁻³ M⁻¹ s⁻¹ in aqueous media.
3. Biocompatible: Works at pH 7.4, 37°C, in water.
4. Non-toxic: Byproducts must be nontoxic.

### [Source: Wikipedia, Click Chemistry]
### Sharpless Click Chemistry Principles
- Defined by Sharpless (2001): "Click chemistry sets out to mimic nature by joining small modular units."
- Criteria: High yield, wide scope, simple conditions, no toxic byproducts, stereospecific.

| Reaction | Conditions | Rate (M⁻¹ s⁻¹) | Byproducts |
|---|---|---|---|
| CuAAC (azide-alkyne) | Cu(I), RT, aqueous | ~10⁰–10³ | N₂, Cu salts |
| SPAAC (copper-free) | Strained cyclooctyne, RT | ~10⁻³–10⁻¹ | None |
| Tetrazine ligation | Tetrazine + TCO, RT | ~10²–10⁶ | N₂ |
| IEDDA | Very fast, inverse demand | 10²–10⁶ | N₂ |

### [Source: Wikipedia, Activity-Based Protein Profiling (ABPP)]
- ABPP: Chemical probes with reactive warheads linked to reporter tags (fluorophore/biotin).
- Activity-based (not abundance-based): Only labels active enzyme forms.
- Warhead types: Serine protease (FP), cysteine protease (DCG-04, iodoacetamide), kinases (acyl phosphate).
- Workflow: Probe incubation → click to reporter tag → gel analysis or mass spec.

### [Source: Wikipedia, Proteolysis Targeting Chimera (PROTAC)]
- PROTAC = bifunctional molecule: E3 ligase ligand + linker + target protein ligand.
- Mechanism: Brings target protein and E3 ligase into proximity → ubiquitination → proteasomal degradation.
- **Catalytic**: One PROTAC molecule degrades multiple target proteins (substoichiometric).
- First PROTAC (2001): VHL ligand linked to estradiol (degraded ER).
- Key E3 ligases used: VHL, CRBN, MDM2, cIAP1.
- Clinical candidates: ARV-110 (androgen receptor), ARV-471 (estrogen receptor).
