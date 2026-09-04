---
id: alkane.nomenclature
layer: 2
title: Alkane Nomenclature and Structure
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - ../L3_functions/alkane_tools.py
  - ../L4_reference/reference/alkane-nomenclature-rules.md
cross_links:
  - ./organic_functional_groups.md
  - ./conformational_analysis.md
---

## Context
Alkanes are saturated hydrocarbons containing only C-C and C-H single bonds. They serve as the backbone for naming all organic compounds. IUPAC nomenclature provides systematic naming rules that give each compound a unique name.

## Alkane Families

### Straight-Chain Alkanes
| n | Formula | Name | Structure |
|---|---------|------|-----------|
| 1 | CH₄ | Methane | CH₄ |
| 2 | C₂H₆ | Ethane | CH₃CH₃ |
| 3 | C₃H₈ | Propane | CH₃CH₂CH₃ |
| 4 | C₄H₁₀ | Butane | CH₃(CH₂)₂CH₃ |
| 5 | C₅H₁₂ | Pentane | CH₃(CH₂)₃CH₃ |
| 6 | C₆H₁₄ | Hexane | CH₃(CH₂)₄CH₃ |
| 7 | C₇H₁₆ | Heptane | CH₃(CH₂)₅CH₃ |
| 8 | C₈H₁₈ | Octane | CH₃(CH₂)₆CH₃ |
| 9 | C₉H₂₀ | Nonane | CH₃(CH₂)₇CH₃ |
| 10 | C₁₀H₂₂ | Decane | CH₃(CH₂)₈CH₃ |

### General Formula
- **Acyclic alkanes**: CₙH₂ₙ₊₂
- **Cycloalkanes**: CₙH₂ₙ (one ring)

## Alkyl Groups

### Common Alkyl Substituents
| Alkyl Group | Structure | Derived From |
|-------------|-----------|--------------|
| Methyl | CH₃- | Methane |
| Ethyl | CH₃CH₂- | Ethane |
| Propyl | CH₃CH₂CH₂- | Propane |
| Isopropyl | (CH₃)₂CH- | Propane |
| Butyl | CH₃CH₂CH₂CH₂- | Butane |
| sec-Butyl | CH₃CH₂CH(CH₃)- | Butane |
| Isobutyl | (CH₃)₂CHCH₂- | Butane |
| tert-Butyl | (CH₃)₃C- | Butane |

### Branched Alkyl Naming
- **iso-**: (CH₃)₂CH- group (except isopropyl)
- **sec-**: Secondary carbon (attached to 2 other carbons)
- **tert-**: Tertiary carbon (attached to 3 other carbons)
- **neo-**: (CH₃)₃CCH₂- group

## IUPAC Naming Rules

### Step-by-Step Process
1. **Find the longest continuous carbon chain** (parent chain)
   - Not necessarily straight in drawing
   - Count carbons to determine parent name

2. **Number the chain**
   - Give substituents lowest possible numbers
   - Number from end nearest first substituent

3. **Name and locate substituents**
   - Use alkyl group names
   - Include position number and hyphen

4. **Arrange substituents alphabetically**
   - Ignore multiplying prefixes (di-, tri-, tetra-)
   - Use commas between numbers, hyphens between numbers and words

### Naming Format
```
[Position]-[Substituent]-[Parent chain]
```

### Examples
| Structure | IUPAC Name |
|-----------|------------|
| CH₃CH(CH₃)CH₃ | 2-methylpropane |
| CH₃CH(CH₃)CH₂CH₃ | 2-methylbutane |
| CH₃C(CH₃)₂CH₂CH₃ | 2,2-dimethylbutane |
| CH₃CH(CH₃)CH(CH₃)CH₃ | 2,3-dimethylbutane |
| CH₃CH(CH₂CH₃)CH₂CH(CH₃)CH₃ | 3-ethyl-2-methylpentane |

## Constitutional Isomers

### Number of Isomers
| Carbon Atoms | Number of Isomers |
|--------------|-------------------|
| 1-3 | 1 |
| 4 | 2 |
| 5 | 3 |
| 6 | 5 |
| 7 | 9 |
| 8 | 18 |
| 9 | 35 |
| 10 | 75 |

### Types of Isomers
- **Chain isomers**: Different carbon skeleton
- **Position isomers**: Same skeleton, different substituent position

## Cycloalkanes

### Naming
- Prefix "cyclo-" before parent alkane name
- Number to give substituents lowest possible numbers

### Examples
| Structure | Name |
|-----------|------|
| C₃H₆ (triangle) | Cyclopropane |
| C₄H₈ (square) | Cyclobutane |
| C₅H₁₀ (pentagon) | Cyclopentane |
| C₆H₁₂ (hexagon) | Cyclohexane |
| Methylcyclopentane | 1-methylcyclopentane |

## Physical Properties

### Boiling Points
- Increase with molecular weight (more London dispersion)
- Branched alkanes have lower bp than straight-chain isomers

### Solubility
- Alkanes are nonpolar → soluble in nonpolar solvents
- Insoluble in water (hydrophobic)

### Density
- All alkanes less dense than water (d < 1.0 g/mL)

## Decision Flow
1. Identify all carbon atoms and connections
2. Find longest continuous chain
3. Number chain to minimize substituent positions
4. Name substituents and parent
5. Arrange alphabetically
6. Verify unique naming

## Implementations and Data
- Name generator: [L3 code](../L3_functions/alkane_tools.py)
- Reference rules: [L4 reference](../L4_reference/reference/alkane-nomenclature-rules.md)

## L3 Tool Call Directives

**Source:** `alkane_tools.py`
Alkane naming, IUPAC conventions, isomer counting, and physical property predictions.

### Available functions:
- `get_alkane_name(carbons)` → Tuple[str, str] — Get IUPAC name and molecular formula for alkane
- `get_alkyl_group(name)` → AlkylGroup — Get alkyl group info (name, formula, carbons)
- `hydrocarbon_formula(carbons, saturation)` → str — Get molecular formula for hydrocarbon
- `count_isomers(carbons)` → int — Get number of constitutional isomers for alkane
- `generate_iupac_name(parent_chain, substituents)` → str — Generate IUPAC name from parent chain and substituent list
- `find_parent_chain_length(structure)` → int — Find longest carbon chain in structure
- `number_chain(substituent_positions)` → List[int] — Apply lowest-numbering rule
- `classify_alkyl_halide(carbons_alpha_to_halogen)` → str — Classify as primary/secondary/tertiary
- `alkane_properties(carbons)` → dict — Predict boiling point, melting point, density, state

### Common errors:
- ❌ Not applying lowest-numbering rule for substituent positions
- ❌ Confusing constitutional isomers with stereoisomers

## L3 Tool Call Directives

**Source:** `alkane_tools.py`
Alkane naming, IUPAC conventions, isomer counting, and physical property predictions.

### Available functions:
- `get_alkane_name(carbons)` → Tuple[str, str] — Get IUPAC name and molecular formula for alkane
- `get_alkyl_group(name)` → AlkylGroup — Get alkyl group info (name, formula, carbons)
- `hydrocarbon_formula(carbons, saturation)` → str — Get molecular formula for hydrocarbon
- `count_isomers(carbons)` → int — Get number of constitutional isomers for alkane
- `generate_iupac_name(parent_chain, substituents)` → str — Generate IUPAC name from parent chain and substituent list
- `find_parent_chain_length(structure)` → int — Find longest carbon chain in structure
- `number_chain(substituent_positions)` → List[int] — Apply lowest-numbering rule
- `classify_alkyl_halide(carbons_alpha_to_halogen)` → str — Classify as primary/secondary/tertiary
- `alkane_properties(carbons)` → dict — Predict boiling point, melting point, density, state

### Common errors:
- ❌ Not applying lowest-numbering rule for substituent positions
- ❌ Confusing constitutional isomers with stereoisomers
