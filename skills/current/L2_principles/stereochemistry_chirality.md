---
id: stereochemistry.chirality
layer: 2
title: Stereochemistry and Chirality
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - - `../L3_functions/rdkit_structure_tools.py` — stereochemistry_analysis()
  - - `../L3_functions/stereoisomer_counter.py` — count_stereoisomers(), check_meso()
  - - `../L3_functions/stereochemistry_tools.py` — R/S, E/Z determination
  - ../L3_functions/stereochemistry_tools.py
  - ../L4_reference/reference/stereochemistry-rules.md
cross_links:
  - ./organic_functional_groups.md
  - ./conformational_analysis.md
---

## Context
Stereochemistry is the study of the three-dimensional arrangement of atoms in molecules. Chirality is a property of molecules that are not superimposable on their mirror images. This principle governs biological activity, drug design, and reaction mechanisms.

## Key Concepts

### Chirality
- **Chiral molecule**: Not superimposable on its mirror image
- **Achiral molecule**: Superimposable on its mirror image
- **Chirality center (stereocenter)**: An atom (usually C) bonded to four different groups
- **Enantiomers**: Non-superimposable mirror images (pair of chiral molecules)

### Types of Isomers
```
Isomers
├── Constitutional (structural) isomers - different connectivity
└── Stereoisomers - same connectivity, different 3D arrangement
    ├── Enantiomers - mirror images
    └── Diastereomers - not mirror images
        ├── Alkene E/Z isomers
        └── Compounds with multiple chiral centers
```

### Optical Activity
- **Optically active**: Rotates plane-polarized light
- **Dextrorotatory (+)**: Rotates light clockwise
- **Levorotatory (-)**: Rotates light counterclockwise
- **Specific rotation**: [α] = α / (c × l) where c = concentration (g/mL), l = path length (dm)

## R/S Nomenclature (Cahn-Ingold-Prelog Rules)

### Sequence Rules
1. Assign priority to each substituent (1 = highest, 4 = lowest)
2. Priority rules:
   - Higher atomic number = higher priority
   - For isotopes, higher mass = higher priority
   - For multiple bonds, count each bond separately
3. Orient molecule with lowest priority (4) pointing away
4. Trace path from 1 → 2 → 3
   - Clockwise = R (rectus, "right")
   - Counterclockwise = S (sinister, "left")

### Priority Examples
| Comparison | Higher Priority |
|------------|----------------|
| -Cl vs -Br | -Br (higher atomic number) |
| -CH₃ vs -CH₂OH | -CH₂OH (O > H) |
| -CH₂CH₃ vs -CH=O | -CH=O (C counted 3× due to double bond) |

## Molecules with Multiple Chiral Centers

### Maximum Number of Stereomers
- Maximum stereomers = 2ⁿ where n = number of chiral centers

### Types of Relationships
| Relationship | Definition | Property |
|--------------|------------|----------|
| Enantiomers | Mirror images | Same all properties except optical rotation |
| Diastereomers | Not mirror images | Different physical properties |
| Meso compound | Achiral despite chiral centers | Optically inactive (internal plane of symmetry) |

### Example: 2,3-Butanediol
- Has 2 chiral centers → maximum 4 stereomers
- Actually only 3 stereomers exist:
  - (2R,3R) and (2S,3S) are enantiomers
  - (2R,3S) = (2S,3R) = meso compound (same molecule)

## Racemic Mixtures and Resolution

### Racemic Mixture
- Equal amounts (50:50) of enantiomers
- Optically inactive (rotations cancel)
- Designated as (±) or rac-

### Resolution Methods
1. Diastereomeric salt formation
2. Chromatography on chiral stationary phase
3. Enzymatic resolution
4. Kinetic resolution

## Prochirality
- **Prochiral center**: Can become chiral by single change
- **Pro-R / Pro-S**: Distinguish enantiotopic groups
- **Re / Si faces**: Distinguish faces of trigonal atoms

## Biological Significance

### Enantiomer Differences
- Different biological activity (only one fits receptor)
- Example: Thalidomide tragedy (one enantiomer is teratogenic)
- Many drugs sold as single enantiomers

### Chiral Drugs
| Drug | Enantiomer Difference |
|------|----------------------|
| Ibuprofen | Only S-isomer active (but R converts to S in body) |
| Thalidomide | R = sedative, S = teratogenic |
| Albuterol | R = bronchodilator, S = causes inflammation |
| Naproxen | S = anti-inflammatory, R = liver toxin |

## Decision Flow
1. Identify chiral centers (4 different groups attached)
2. Assign R/S configuration to each
3. Determine number of possible stereomers
4. Check for meso compounds (internal symmetry)
5. For reactions, consider stereochemical outcome

## Implementations and Data
- R/S configurator: [L3 code](../L3_functions/stereochemistry_tools.py)
- Reference rules: [L4 reference](../L4_reference/reference/stereochemistry-rules.md)

## L3 Tool Call Directives

**Source:** `stereochemistry_tools.py`

CIP priority assignment, R/S configuration, chiral center counting, stereomer enumeration, optical rotation, meso compound detection.

### Available functions:
- `get_atomic_number(element)` → int — Atomic number lookup for CIP ranking
- `assign_cip_priority(substituents)` → List[int] — CIP priorities [1,2,3,4] for 4 substituents
- `assign_r_s_config(center_atoms, substituent_priorities)` → Stereochemistry — R/S assignment (simplified)
- `count_chiral_centers(molecule_structure)` → int — Count chiral centers from SMILES
- `maximum_stereomers(chiral_centers)` → int — 2^n upper limit
- `determine_enantiomer_relationship(config1, config2)` → IsomerRelationship — ENANTIOMER/IDENTICAL/DIASTEREOMER
- `calculate_optical_rotation(concentration, path_length, observed_rotation)` → float — [α] = α/(c×l)
- `predict_optical_activity(configurations)` → str — Optical activity from R/S list
- `check_meso_possibility(configurations)` → bool — True if internal symmetry plane possible
- `enumerate_stereomers(chiral_centers)` → List[List[Stereochemistry]] — All R/S combinations
- `chiral_drug_examples()` → Dict — Famous chiral drug enantiomer differences

### Common errors:
- ❌ 2^n is an upper limit — meso compounds reduce actual stereomer count
- ❌ Assigning R/S without 3D coordinates (simplified implementation; needs wedge-dash data)
