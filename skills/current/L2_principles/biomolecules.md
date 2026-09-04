---
id: biomolecules
layer: 2
title: Biomolecules - Carbohydrates, Lipids, Proteins, and Nucleic Acids
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - ../L3_functions/protein_tools.py
  - ../L4_reference/amino_acid_properties.csv
cross_links:
  - ./carbonyl_chemistry.md
  - ./alcohol_chemistry.md
  - ./stereochemistry_chirality.md
source: Organic Chemistry (OpenStax), Ch25-28
---

## Context
Biomolecules are organic compounds essential to life processes. The four major classes are carbohydrates, lipids, proteins, and nucleic acids. Understanding their structure and reactivity is fundamental to biochemistry and medicinal chemistry.

## Carbohydrates

### Classification
| Class | Example | General Formula |
|-------|---------|-----------------|
| Monosaccharides | Glucose, Fructose | CₙH₂ₙOₙ |
| Disaccharides | Sucrose, Lactose | Two monosaccharides |
| Polysaccharides | Starch, Cellulose | Many monosaccharides |

### Monosaccharide Structure

**Aldoses vs Ketoses:**
- **Aldose**: Aldehyde group (e.g., glucose)
- **Ketose**: Ketone group (e.g., fructose)

**D and L Configuration:**
- Based on configuration at the highest-numbered chiral center
- D-sugars: OH on right at C5 (for hexoses)
- Most natural sugars are D-sugars

**Glucose (D-Glucose):**
```
    CHO
     |
    H-C-OH
     |
    HO-C-H
     |
    H-C-OH
     |
    H-C-OH
     |
    CH₂OH
```

### Cyclic Forms

**Hemiacetal Formation:**
- Aldehyde + alcohol → hemiacetal
- Forms 5-membered (furanose) or 6-membered (pyranose) rings

**Anomers:**
- **α-Anomer**: OH on anomeric carbon is trans to CH₂OH
- **β-Anomer**: OH on anomeric carbon is cis to CH₂OH

**Mutarotation:**
- Interconversion between α and β anomers in solution
- Equilibrium: ~36% α, ~64% β for D-glucose

### Important Monosaccharides
| Sugar | Type | Key Features |
|-------|------|--------------|
| D-Glucose | Aldose | Blood sugar, most abundant |
| D-Fructose | Ketose | Fruit sugar, sweetest |
| D-Galactose | Aldose | Component of lactose |
| D-Ribose | Aldopentose | RNA component |
| D-Deoxyribose | Aldopentose | DNA component |

### Disaccharides
| Sugar | Components | Glycosidic Bond |
|-------|------------|-----------------|
| Sucrose | Glucose + Fructose | α-1,β-2 |
| Lactose | Glucose + Galactose | β-1,4 |
| Maltose | Glucose + Glucose | α-1,4 |

### Polysaccharides
| Polymer | Monomer | Structure | Function |
|---------|---------|-----------|----------|
| Starch | Glucose | α-1,4 + α-1,6 branches | Energy storage (plants) |
| Glycogen | Glucose | α-1,4 + α-1,6 branches | Energy storage (animals) |
| Cellulose | Glucose | β-1,4 | Structural (plant cell walls) |

### Carbohydrate Reactions
| Reaction | Reagent | Product |
|----------|---------|---------|
| Oxidation (Tollens) | Ag⁺ | Aldonic acid + Ag |
| Reduction | NaBH₄ | Alditol |
| Osazone formation | PhNHNH₂ | Osazone |
| Acetylation | Ac₂O | Peracetate |

## Lipids

### Classification
| Class | Structure | Example |
|-------|-----------|---------|
| Fatty acids | Long chain carboxylic acids | Palmitic acid |
| Triacylglycerols | Glycerol + 3 fatty acids | Fats and oils |
| Phospholipids | Glycerol + 2 fatty acids + phosphate | Cell membranes |
| Steroids | Fused ring system | Cholesterol |
| Waxes | Fatty acid + long alcohol | Beeswax |

### Fatty Acids

**Saturated vs Unsaturated:**
| Type | Structure | Melting Point | Example |
|------|-----------|---------------|---------|
| Saturated | No double bonds | Higher | Stearic acid (C18:0) |
| Unsaturated | One or more C=C | Lower | Oleic acid (C18:1) |

**Essential Fatty Acids:**
- Linoleic acid (C18:2, ω-6)
- Linolenic acid (C18:3, ω-3)
- Cannot be synthesized by humans

### Triacylglycerols
```
    CH₂-O-CO-R₁
     |
    CH-O-CO-R₂
     |
    CH₂-O-CO-R₃
```
- R = fatty acid chains
- **Saponification**: Base hydrolysis → glycerol + soaps

### Phospholipids
```
    CH₂-O-CO-R₁
     |
    CH-O-CO-R₂
     |
    CH₂-O-P-O-X
         |
         O⁻
```
- X = choline, ethanolamine, serine, inositol
- Form lipid bilayers in cell membranes

### Steroids
- Cholesterol: precursor to all steroids
- Four fused rings (three 6-membered, one 5-membered)
- Steroid hormones: testosterone, estrogen, cortisol

## Proteins

### Amino Acids
- **20 standard amino acids**
- General structure: H₂N-CH(R)-COOH
- L-configuration at α-carbon (except glycine)

**Classification by Side Chain:**
| Type | Amino Acids | Character |
|------|-------------|-----------|
| Nonpolar | Gly, Ala, Val, Leu, Ile, Pro, Phe, Trp, Met | Hydrophobic |
| Polar | Ser, Thr, Cys, Tyr, Asn, Gln | Hydrophilic |
| Acidic | Asp, Glu | Negative charge |
| Basic | Lys, Arg, His | Positive charge |

### Peptide Bond Formation
```
H₂N-CH(R₁)-COOH + H₂N-CH(R₂)-COOH → H₂N-CH(R₁)-CO-NH-CH(R₂)-COOH + H₂O
```
- Amide bond
- Planar due to resonance
- Trans configuration favored

### Protein Structure Levels
| Level | Description | Stabilizing Forces |
|-------|-------------|-------------------|
| Primary | Amino acid sequence | Covalent bonds |
| Secondary | α-helix, β-sheet | H-bonds |
| Tertiary | 3D structure | H-bonds, disulfide, hydrophobic |
| Quaternary | Multiple subunits | Same as tertiary |

### Common Reactions
| Reaction | Reagent | Application |
|----------|---------|-------------|
| Ninhydrin | Heat | Amino acid detection |
| Edman degradation | Phenyl isothiocyanate | Sequencing |
| Disulfide formation | Oxidation | Cys-Cys bridges |

## Nucleic Acids

### Components
- **Pentose sugar**: Ribose (RNA) or Deoxyribose (DNA)
- **Phosphate**: Links nucleotides
- **Nitrogenous bases**: Purines (A, G) and Pyrimidines (C, T, U)

### Nucleosides vs Nucleotides
| Component | Composition |
|-----------|-------------|
| Nucleoside | Base + Sugar |
| Nucleotide | Base + Sugar + Phosphate |

### DNA vs RNA
| Feature | DNA | RNA |
|---------|-----|-----|
| Sugar | Deoxyribose | Ribose |
| Bases | A, G, C, T | A, G, C, U |
| Structure | Double helix | Usually single strand |
| Function | Genetic information | Protein synthesis |

### Base Pairing
- **A-T (DNA) / A-U (RNA)**: 2 hydrogen bonds
- **G-C**: 3 hydrogen bonds

### DNA Structure (Double Helix)
- Two antiparallel strands
- Sugar-phosphate backbone outside
- Bases inside, paired by H-bonds
- ~10 base pairs per turn

### Nucleic Acid Reactions
| Reaction | Application |
|----------|-------------|
| Polymerase chain reaction (PCR) | DNA amplification |
| Restriction enzyme cleavage | DNA manipulation |
| Sequencing reactions | DNA/RNA sequencing |

## Metabolic Pathway Summary

| Pathway | Key Products | Energy Yield |
|---------|--------------|--------------|
| Glycolysis | Pyruvate, ATP, NADH | 2 ATP per glucose |
| Citric acid cycle | CO₂, NADH, FADH₂ | 2 ATP per glucose |
| Oxidative phosphorylation | ATP | ~34 ATP per glucose |
| β-Oxidation | Acetyl-CoA | ~14 ATP per 2C |

## Decision Flow
1. Identify biomolecule class
2. For carbohydrates: determine monosaccharide structure and linkages
3. For lipids: identify fatty acid composition
4. For proteins: analyze amino acid composition and structure
5. For nucleic acids: identify bases and sugar type

## Implementations and Data
- Biomolecule analysis tools: [L3 code](../L3_functions/protein_tools.py)
- Reference tables: [L4 reference](../L4_reference/amino_acid_properties.csv)
