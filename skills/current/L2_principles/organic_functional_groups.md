---
id: organic.functional_groups
layer: 2
title: Organic Functional Groups
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - - `../L3_functions/rdkit_structure_tools.py` — analyze_functional_groups()
  - ../L3_functions/functional_group_tools.py
  - ../L4_reference/reference/functional-group-reference.md
cross_links:
  - ./organic_reaction_mechanisms.md
  - ./alkane_nomenclature.md
---

## Context
Functional groups are atoms or small groups of atoms (two to four) that exhibit characteristic reactivity. A particular functional group will almost always display its characteristic chemical behavior when present in a compound. This principle enables systematic study of organic chemistry by grouping compounds by reactivity patterns.

## Core Functional Groups

### Hydrocarbons
| Group | Structure | General Formula | Example |
|-------|-----------|-----------------|---------|
| Alkane | C-C single bonds | R-H | CH₄ (methane) |
| Alkene | C=C double bond | R₂C=CR₂ | C₂H₄ (ethylene) |
| Alkyne | C≡C triple bond | RC≡CR | C₂H₂ (acetylene) |
| Aromatic | Benzene ring | Ar-H | C₆H₆ (benzene) |

### Oxygen-Containing Groups
| Group | Structure | Suffix | Example |
|-------|-----------|--------|---------|
| Alcohol | R-OH | -ol | CH₃OH (methanol) |
| Ether | R-O-R' | ether | CH₃OCH₃ (dimethyl ether) |
| Aldehyde | R-CHO | -al | HCHO (formaldehyde) |
| Ketone | R-CO-R' | -one | CH₃COCH₃ (acetone) |
| Carboxylic acid | R-COOH | -oic acid | CH₃COOH (acetic acid) |
| Ester | R-COO-R' | -oate | CH₃COOCH₃ (methyl acetate) |
| Anhydride | R-CO-O-CO-R' | anhydride | (CH₃CO)₂O (acetic anhydride) |

### Nitrogen-Containing Groups
| Group | Structure | Suffix | Example |
|-------|-----------|--------|---------|
| Amine | R-NH₂, R₂NH, R₃N | -amine | CH₃NH₂ (methylamine) |
| Amide | R-CONH₂ | -amide | CH₃CONH₂ (acetamide) |
| Nitrile | R-C≡N | -nitrile | CH₃CN (acetonitrile) |
| Nitro | R-NO₂ | nitro- | CH₃NO₂ (nitromethane) |

### Halogen-Containing Groups
| Group | Structure | Prefix | Example |
|-------|-----------|--------|---------|
| Alkyl halide | R-X | halo- | CH₃Cl (chloromethane) |
| Acyl halide | R-COX | -oyl halide | CH₃COCl (acetyl chloride) |

### Sulfur-Containing Groups
| Group | Structure | Suffix | Example |
|-------|-----------|--------|---------|
| Thiol | R-SH | -thiol | CH₃SH (methanethiol) |
| Sulfide | R-S-R' | sulfide | CH₃SCH₃ (dimethyl sulfide) |

## Polarity Patterns

### Electron-Withdrawing Groups (EWG)
- Make adjacent atoms more electron-deficient
- Examples: -NO₂, -CN, -COOH, -CHO, -COR
- Stabilize carbanions, destabilize carbocations

### Electron-Donating Groups (EDG)
- Make adjacent atoms more electron-rich
- Examples: -OH, -OR, -NH₂, -NR₂, alkyl groups
- Stabilize carbocations, destabilize carbanions

## Decision Flow
1. Identify all functional groups in molecule
2. Determine which is the principal group (highest priority)
3. Use principal group for suffix naming
4. Use other groups as prefixes
5. Consider intermolecular forces based on functional groups

## Intermolecular Force Implications
| Functional Group | Key IM Forces | Effect on Properties |
|------------------|--------------|---------------------|
| Alkane | London dispersion | Low bp, hydrophobic |
| Alcohol | H-bonding | Higher bp, water soluble |
| Carboxylic acid | H-bonding (dimer) | Highest bp among organics |
| Aldehyde/Ketone | Dipole-dipole | Moderate bp |
| Amine | H-bonding (primary/secondary) | Moderate-high bp |

## Implementations and Data
- Functional group identifier: [L3 code](../L3_functions/functional_group_tools.py)
- Reference table: [L4 reference](../L4_reference/reference/functional-group-reference.md)
