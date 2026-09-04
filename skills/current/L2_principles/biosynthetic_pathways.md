---
id: biosynthetic_pathways
layer: 2
title: Biosynthetic Pathways (Acetate, Shikimate, Mevalonate)
parent: ../L1_ontology/chemistry-core-map.md#entry-285
stability: high
confidence: high
last_verified: 2026-03-24
source: Roberts & Caserio Ch30, LibreTexts Organic Chemistry
---

# Biosynthetic Pathways

## Core Concept

Living organisms synthesize complex natural products from simple building blocks via enzyme-catalyzed pathways. Three major pathways — acetate (polyketide), mevalonate (terpenoid), and shikimate — account for most natural product diversity.

---

## 1. Acetate (Malonate) Pathway → Polyketides & Fatty Acids

### Building Block
Acetyl-CoA (C₂) + Malonyl-CoA (C₃, donated as C₂ with CO₂ loss)

### Process (PKS cycle)
1. Starter unit: acetyl-CoA loaded onto PKS
2. Extension: malonyl-CoA adds C₂ (decarboxylative Claisen condensation)
3. Optional modifications: reduction, dehydration, enoyl reduction
4. Repeat for chain extension
5. Release: cyclization or hydrolysis

### Products
- **Fatty acids:** fully reduced (C₁₆, C₁₈)
- **Polyketides:** partially reduced → diverse oxygenation patterns
- **Aromatics:** C₆-C₃ (phenylpropanoids from phenylalanine)

---

## 2. Mevalonate (MVA) Pathway → Terpenoids & Steroids

### Building Block
Acetyl-CoA → HMG-CoA → Mevalonate → IPP (isopentenyl pyrophosphate, C₅) + DMAPP (dimethylallyl PP)

### Key Steps
1. 2 Acetyl-CoA → Acetoacetyl-CoA (thiolase)
2. + Acetyl-CoA → HMG-CoA (HMG-CoA synthase)
3. HMG-CoA → Mevalonate (HMG-CoA reductase — target of statins!)
4. Mevalonate → IPP (2 ATP)
5. IPP ⇌ DMAPP (isomerase)
6. IPP + DMAPP → GPP (C₁₀), FPP (C₁₅), GGPP (C₂₀) — prenyltransferases

### Alternative: MEP/DOXP Pathway (Plants, Bacteria)
- Glyceraldehyde-3-P + pyruvate → DOXP → MEP → IPP/DMAPP
- Not present in animals — target for antimalarials/antibiotics

---

## 3. Shikimate Pathway → Aromatic Amino Acids & Derived Products

### Building Block
Erythrose-4-P (C₄) + PEP (C₃) → shikimate → chorismate

### Products
- **Amino acids:** phenylalanine, tyrosine, tryptophan
- **Derived natural products:**
  - Alkaloids (morphine, caffeine, nicotine)
  - Phenylpropanoids (lignin, flavonoids, coumarins)
  - Pigments (anthocyanins)

### Why Important
- This pathway does NOT exist in animals
- Many herbicides target the shikimate pathway (glyphosate inhibits EPSP synthase)

---

## Pathway Summary

| Pathway | Building Block | Products | Drug Examples |
|---------|---------------|----------|---------------|
| Acetate | Acetyl-CoA | Fatty acids, polyketides | Erythromycin, doxorubicin |
| Mevalonate | Acetyl-CoA | Terpenes, steroids | Taxol, steroids, artemisinin |
| Shikimate | E4P + PEP | Aromatics, alkaloids | Morphine, caffeine |

---

## Complete Extraction: Biosynthesis (Roberts & Caserio Ch30.5)

### Definition
Biosynthesis is a multi-step, **enzyme-catalyzed** process where simple substrates are converted into more complex products in living organisms. Simple building blocks are modified, converted, or joined to form macromolecules.

### Key Biosynthetic Pathways

#### Mevalonate Pathway (Isoprenoids/Steroids)
1. **Acetyl-CoA** → Acetoacetyl-CoA → HMG-CoA → **Mevalonate** (HMG-CoA reductase, target of statins)
2. Mevalonate → IPP (isopentenyl pyrophosphate) → DMAPP
3. IPP/DMAPP → Geranyl-PP (C₁₀) → Farnesyl-PP (C₁₅) → Squalene (C₃₀) → Steroids
4. **Key products:** Cholesterol, ergosterol, steroid hormones, vitamin D, bile acids

#### Acetate (Polyketide) Pathway
1. **Acetyl-CoA + Malonyl-CoA** → polyketide chain (CLaisen-type condensations)
2. Cyclizations, reductions, aromatizations produce diverse structures
3. **Key products:** Fatty acids, macrolide antibiotics (erythromycin), anthracyclines (doxorubicin), tetracyclines

#### Shikimate Pathway (Aromatics)
1. **Erythrose-4-phosphate + Phosphoenolpyruvate** → Shikimate → Chorismate
2. Branches to: aromatic amino acids (Phe, Tyr, Trp), alkaloids, flavonoids
3. **Does NOT exist in animals** → basis of many herbicides (glyphosate targets EPSP synthase)
4. **Key products:** Morphine, caffeine, lignin, flavonoids, coumarins

#### Non-Ribosomal Peptide Synthesis
- Large multifunctional enzyme complexes (NRPS)
- Can incorporate non-proteinogenic amino acids
- **Products:** Vancomycin, penicillin, cyclosporine

#### Mixed Pathways
Many natural products combine elements of multiple pathways:
- **Alkaloids:** Shikimate-derived (morphine) or terpene-derived (taxol side chain)
- **Prostaglandins:** Fatty acid-derived (arachidonic acid → C₂₀ eicosanoids)

### Enzymatic Key Steps
- **Cyclases:** Form rings (terpene cyclases, polyketide cyclases)
- **Oxidases:** Introduce oxygen (P450 enzymes)
- **Glycosyltransferases:** Add sugar moieties
- **Methyltransferases:** Add methyl groups (SAM-dependent)

### Source Cross-References
- Roberts & Caserio, Basic Principles of Organic Chemistry, Ch30.5
- Organic Chemistry III (Morsch et al.)

---

## Links

- L3: `../L3_functions/natural_products_tools.py`
- L4: `../L4_reference/natural_products_reference.csv`

---

## [Source: Wikipedia, Biosynthesis]
### Major Biosynthetic Pathways

| Pathway | Building Blocks | Key Products | Enzyme Type |
|---|---|---|---|
| Acetate-malonate (PKS) | Acetyl-CoA + Malonyl-CoA | Polyketides, Fatty acids | Polyketide synthase |
| Mevalonate (MVA) | Acetyl-CoA 鈫?IPP | Sterols, Sesquiterpenes | HMGR, Prenyltransferase |
| MEP/DOXP | Pyruvate + G3P 鈫?IPP | Monoterpenes, Diterpenes | DXS, DXR |
| Shikimate | PEP + E4P 鈫?Chorismate | Aromatics, Amino acids | DAHP synthase, EPSP synthase |
| Amino acid | 伪-Ketoglutarate etc. | Alkaloids, Peptides | Transaminases, Decarboxylases |

**Isoprene rule**: Terpenoids are built from isopentenyl pyrophosphate (IPP) and dimethylallyl pyrophosphate (DMAPP), both C鈧?units.
