---
id: glycobiology
layer: 2
title: Glycobiology (Glycan Labeling, Metabolic Incorporation)
parent: ../L1_ontology/chemistry-core-map.md#entry-278
stability: high
confidence: high
last_verified: 2026-03-28
source: LibreTexts Biological Chemistry, Bertozzi lab publications
down_links:
  - ../L3_functions/chemical_biology_tools.py
---

# Glycobiology

## Core Concept

Glycobiology studies the structure, biosynthesis, and function of glycans (carbohydrate chains attached to proteins and lipids). Chemical methods enable glycan visualization and analysis in living systems.

---

## Glycan Basics

### Major Glycan Classes
1. **N-linked:** attached to Asn (N-X-S/T sequon, X ≠ Pro)
   - High-mannose, hybrid, complex types
2. **O-linked:** attached to Ser/Thr
   - Mucin-type (GalNAc-Ser/Thr), O-GlcNAc (nuclear/cytoplasmic)
3. **Glycolipids:** attached to ceramide (lipid anchor)
4. **GPI anchors:** glycosylphosphatidylinositol membrane anchors

### Monosaccharide Building Blocks
Glc, Gal, Man, GlcNAc, GalNAc, Fuc, Neu5Ac (sialic acid), Xyl, GlcA

---

## Metabolic Glycan Labeling

### Principle (Bertozzi, 2000s)
Feed cells unnatural sugars bearing bioorthogonal handles → cells biosynthetically incorporate them into glycans → chemoselective detection.

### Key Example: Ac₄ManNAz
1. Peracetylated N-azidoacetylmannosamine (Ac₄ManNAz) crosses cell membrane
2. Esterases remove acetyl groups → ManNAz
3. Metabolic conversion: ManNAz → sialic acid azide (SiaNAz)
4. SiaNAz incorporated into cell surface glycans
5. Click with DBCO-fluorophore → fluorescence imaging

### Common Metabolic Labels

| Unnatural Sugar | Handle | Target Glycan | Click Partner |
|----------------|--------|---------------|---------------|
| Ac₄ManNAz | Azide | Sialic acid | DBCO, BCN |
| Ac₄GalNAz | Azide | O-GlcNAc/GalNAc | DBCO, BCN |
| Ac₄GlcNAz | Azide | N-linked GlcNAc | DBCO, BCN |
| Alkynyl fucose | Alkyne | Fucose | Azide-CuAAC |
| 6-alkynyl GlcNAc | Alkyne | O-GlcNAc | Azide-CuAAC |

---

## Chemoenzymatic Glycan Labeling

### Strategy
Use recombinant glycosyltransferases to install modified sugars onto glycans.

### Example: GalT1-Y289L (mutant galactosyltransferase)
- Transfers azido-Gal (GalNAz) onto terminal GlcNAc
- Enables labeling of any glycan with terminal GlcNAc
- More specific than metabolic labeling

---

## Glycan-Targeted Chemical Probes

### Lectins
Proteins that bind specific glycan epitopes (used as detection reagents).
- ConA (mannose), WGA (GlcNAc/sialic acid), RCA (Gal), SNA (α2,6-sialic acid)

### Glycan Microarrays
Printed glycans on glass slides for high-throughput profiling of glycan-binding proteins (GBPs), antibodies.

---

## Source Context & Cross-References
- LibreTexts Biological Chemistry hub lists glycoscience as a key interest area
- Roberts & Caserio Ch30 covers carbohydrates as natural products
- LibreTexts Organic Chemistry modules: carbohydrate chemistry (glycosidic bonds, stereochemistry)
- Cross-reference: `carbohydrate_chemistry.md` for fundamental sugar chemistry
- Cross-reference: `bioorthogonal_reactions.md` for metabolic glycan labeling
- Key primary sources: Seeberger lab (automated glycan synthesis), Paulson lab (glycan microarrays)

---

## Links

- L3: `../L3_functions/chemical_biology_tools.py`
- L4: `../L4_reference/chemical_biology_reference.csv`
