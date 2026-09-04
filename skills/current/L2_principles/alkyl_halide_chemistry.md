---
id: alkyl.halide.chemistry
layer: 2
title: Alkyl Halide Chemistry - Properties, Synthesis, and Reactions
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - ../L3_functions/alkyl_halide_tools.py
  - ../L4_reference/reference/alkyl-halide-reference.md
cross_links:
  - ./organic_reaction_mechanisms.md
  - ./alcohol_chemistry.md
  - ./alkene_chemistry.md
source: Organic Chemistry (OpenStax), Ch10
---

## Context
Alkyl halides (haloalkanes) contain a halogen atom bonded to an sp³ hybridized carbon. While less common in biological systems, their reactions—particularly nucleophilic substitutions and eliminations—are mechanistically important. Alkyl halides serve as versatile synthetic intermediates.

## Structure and Properties

### Classification
| Type | Structure | Example |
|------|-----------|---------|
| Primary (1°) | R-CH₂-X | CH₃CH₂Br (bromoethane) |
| Secondary (2°) | R₂CH-X | (CH₃)₂CHBr (2-bromopropane) |
| Tertiary (3°) | R₃C-X | (CH₃)₃CBr (2-bromo-2-methylpropane) |

### C-X Bond Properties

| Bond | Length (pm) | Strength (kJ/mol) | Dipole (D) |
|------|-------------|-------------------|------------|
| C-F | 139 | 460 | 1.85 |
| C-Cl | 178 | 350 | 1.87 |
| C-Br | 193 | 294 | 1.81 |
| C-I | 214 | 239 | 1.62 |

### Key Trends
- **Bond strength**: C-F > C-Cl > C-Br > C-I
- **Bond length**: C-F < C-Cl < C-Br < C-I
- **Reactivity**: C-I > C-Br > C-Cl >> C-F
- **Bond polarity**: C(δ+)–X(δ−)

## Nomenclature

### IUPAC Rules
1. Find longest chain containing halogen
2. Number from end nearer first substituent
3. Halogens listed alphabetically: bromo, chloro, fluoro, iodo

### Examples
| Structure | IUPAC Name | Common Name |
|-----------|------------|-------------|
| CH₃Cl | Chloromethane | Methyl chloride |
| CH₃CH₂Br | Bromoethane | Ethyl bromide |
| CH₃CHClCH₃ | 2-Chloropropane | Isopropyl chloride |
| (CH₃)₃CBr | 2-Bromo-2-methylpropane | tert-Butyl bromide |

## Synthesis of Alkyl Halides

### 1. From Alkanes: Radical Halogenation

**Mechanism (Chain Reaction):**
```
Initiation:    X₂ → 2X· (hν or heat)
Propagation:   X· + R-H → HX + R·
               R· + X₂ → R-X + X·
Termination:   X· + X· → X₂
               R· + R· → R-R
               R· + X· → R-X
```

**Reactivity Order for H Abstraction (Chlorination):**
| H Type | Relative Reactivity | C-H Bond Energy (kJ/mol) |
|--------|---------------------|--------------------------|
| Primary (1°) | 1 | 421 |
| Secondary (2°) | 3.5 | 410 |
| Tertiary (3°) | 5 | 400 |

**Product Distribution Formula:**
```
% product = (n × rel. reactivity) / Σ(nᵢ × rel. reactivityᵢ) × 100
```

where n = number of equivalent hydrogens

**Example - Chlorination of Butane:**
- 6 equivalent 1° H: contribution = 6 × 1 = 6
- 4 equivalent 2° H: contribution = 4 × 3.5 = 14
- Total = 20
- % 1-chlorobutane = 6/20 × 100 = 30%
- % 2-chlorobutane = 14/20 × 100 = 70%

**Limitations:**
- Produces mixtures (mono-, di-, tri-halogenated)
- Not selective for synthesis

### 2. From Alkenes: Allylic Bromination (NBS)

**Reagent:** N-Bromosuccinimide (NBS) + hν

```
Alkene + NBS + hν → Allylic bromide
```

**Example:**
```
Cyclohexene + NBS + hν → 3-Bromocyclohexene
```

**Why Allylic?** Allylic radical stability

### Radical Stability Order
| Radical Type | C-H Bond Energy (kJ/mol) | Stability |
|--------------|--------------------------|-----------|
| Allylic | 370 | Most stable |
| 3° Alkyl | 400 | |
| 2° Alkyl | 410 | |
| 1° Alkyl | 421 | |
| Vinylic | 465 | Least stable |

**Stability ordering:** Allylic > 3° > 2° > 1° > Vinylic

### 3. From Alcohols

| Alcohol Type | Reagent | Conditions | Product |
|--------------|---------|------------|---------|
| Tertiary | HCl, HBr, HI | Cold ether | Alkyl halide |
| Primary/Secondary | SOCl₂ | Mild | Alkyl chloride |
| Primary/Secondary | PBr₃ | Mild | Alkyl bromide |
| Any | HF/pyridine | | Alkyl fluoride |

**Reactions:**
```
3° Alcohol:  R₃C-OH + HX → R₃C-X + H₂O
1°/2° Alcohol: R-OH + SOCl₂ → R-Cl + SO₂ + HCl
1°/2° Alcohol: 3 R-OH + PBr₃ → 3 R-Br + H₃PO₃
```

## Grignard Reagents

### Formation
```
R-X + Mg (ether or THF) → R-Mg-X (Grignard reagent)
```

**Halogen reactivity:** I > Br > Cl >> F

### Properties
- Carbon is nucleophilic and basic
- Very strong base (conjugate base of hydrocarbon, pKa 44-60)
- Must exclude water and protic solvents

**Destruction by water:**
```
R-Mg-X + H₂O → R-H + HO-Mg-X
```

## Organometallic Coupling Reactions

### Gilman Reagents (Lithium Diorganocopper)

**Formation:**
```
2 R-Li + CuI → R₂CuLi + LiI
```

**Coupling:**
```
R₂CuLi + R'-X → R-R' + R-Cu + LiX
```

**Scope:** Works with Cl, Br, I (not F); alkyl, aryl, vinylic halides

### Suzuki-Miyaura Coupling

**General:**
```
Ar-B(OH)₂ + Ar'-X + Pd catalyst + base → Ar-Ar' (biaryl)
```

**Advantages:** Catalytic Pd, less toxic, preferred for biaryls

**Applications:** Pharmaceutical synthesis (e.g., valsartan)

## Reactions Summary

| Transformation | Reagent | Product Type |
|----------------|---------|--------------|
| Alkane → Alkyl halide | X₂, hν | Mixture (radical) |
| Alkene → Allylic bromide | NBS, hν | Allylic halide |
| 3° Alcohol → Alkyl halide | HX | Alkyl halide |
| 1°/2° Alcohol → Alkyl chloride | SOCl₂ | Alkyl chloride |
| 1°/2° Alcohol → Alkyl bromide | PBr₃ | Alkyl bromide |
| Alkyl halide → Grignard | Mg, ether | R-Mg-X |
| Alkyl halide → Alkane | Grignard + H₂O | Hydrocarbon |
| Alkyl halide → Coupled product | Gilman or Suzuki | R-R' |

## Decision Flow

1. **For synthesis from alkane:**
   - Simple alkane with limited H types? → Radical halogenation
   - Need selectivity? → Use different approach

2. **For synthesis from alkene:**
   - Need allylic product? → NBS
   - Need addition product? → HX or X₂

3. **For synthesis from alcohol:**
   - 3° alcohol? → HX
   - 1°/2° alcohol? → SOCl₂ or PBr₃

4. **For C-C bond formation:**
   - Need alkyl-alkyl coupling? → Gilman
   - Need biaryl? → Suzuki-Miyaura

## Implementations and Data
- Alkyl halide tools: [L3 code](../L3_functions/alkyl_halide_tools.py)
- Reference tables: [L4 reference](../L4_reference/reference/alkyl-halide-reference.md)

## L3 Tool Call Directives


**Source:** `alkyl_halide_tools.py`

L3 tool module for alkyl halide tools

### Available functions:
- `get_cx_bond_property(halogen: str, property_name: str)` → float — Get C-X bond property for given halogen.
- `classify_hydrogen_type(carbon_substitution: str)` → str — Classify hydrogen type based on carbon substitution.
- `calculate_halogenation_products(hydrogen_pools: List[HydrogenPool], halogen: str)` → dict — Calculate product distribution for radical halogenation.
- `predict_chlorination_products(molecule_name: str)` → dict — Predict monochlorination products for common molecules.
- `identify_allylic_positions(alkene_structure: str)` → List[str] — Identify allylic positions in an alkene.
- `predict_nbs_product(alkene_name: str)` → str — Predict the major NBS bromination product.
- `grignard_formation(alkyl_halide: str, solvent: str)` → dict — Describe Grignard reagent formation.
- `grignard_acid_base_reaction(grignard: str, acid: str, acid_pka: float)` → dict — Predict Grignard acid-base reaction.
- `gilman_coupling(gilman_reagent: str, alkyl_halide: str)` → dict — Predict Gilman coupling reaction.
- `suzuki_coupling(boronic_acid: str, aryl_halide: str)` → dict — Predict Suzuki-Miyaura coupling reaction.
- `calculate_oxidation_level(c_h_bonds: int, c_o_bonds: int, c_n_bonds: int, c_x_bonds: int)` → int — Calculate oxidation level for a carbon atom or molecule.
- `classify_redox_reaction(reactant_level: int, product_level: int)` → str — Classify reaction as oxidation, reduction, or neither.
- `compare_oxidation_levels(compounds: Dict[str, Tuple])` → List[str] — Rank compounds by oxidation level.
- `select_alcohol_to_halide_reagent(alcohol_type: str, target_halide: str)` → dict — Select appropriate reagent for alcohol to alkyl halide conversion.

### Common errors:
- ❌ Passing wrong parameter types (strings where numbers expected)
- ❌ Forgetting required parameters

---

**Source:** sn_mechanism_predictor.py
SN1/SN2/E1/E2 mechanism prediction from substrate and conditions.

### Available functions:
- predict_mechanism(substrate_type, nucleophile=None, base=None, solvent=None) → str — Returns SN1/SN2/E1/E2/SN1+E1
- is_good_nucleophile(species: str) → bool — Nucleophilicity ≥ 1000 threshold
- is_strong_base(species: str) → bool — Checks against STRONG_BASES set
- is_good_leaving_group(species: str) → bool — Checks against GOOD_LEAVING_GROUPS set
- classify_substrate(substrate_type: str) → dict — SN2/SN1/E2 suitability ratings
- 
elative_sn2_rate(substrate: str) → float — Relative rate (methyl=10⁶ reference)
- zaitsev_product(alkyl_halide: str) → str — More substituted alkene (Zaitsev)
- sn2_stereochemistry(configuration: str) → str — Inverted configuration (R↔S)
- sn1_stereochemistry() → str — Returns 'racemic mixture (R and S)'

### Common errors:
- ❌ Not normalizing nucleophile names (predict_mechanism strips Na/K prefixes internally)
- ❌ Bulky bases (tBuOK) favor E2 even with primary substrates
