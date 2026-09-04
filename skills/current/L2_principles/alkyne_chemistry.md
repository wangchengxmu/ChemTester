---
id: alkyne.chemistry
layer: 2
title: Alkyne Chemistry - Structure and Organic Synthesis
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - ../L3_functions/alkyne_tools.py
  - ../L4_reference/reference/alkyne-reactions-reference.md
cross_links:
  - ./alkene_chemistry.md
  - ./organic_reaction_mechanisms.md
source: Organic Chemistry (OpenStax), Ch09
---

## Context
Alkynes are unsaturated hydrocarbons containing carbon-carbon triple bonds (C≡C). The triple bond consists of one σ bond and two π bonds. Alkynes are important in organic synthesis as building blocks and for functional group transformations.

## Structure and Properties

### Electronic Structure of the Triple Bond
- **σ bond**: sp-sp overlap, strong, along bond axis
- **Two π bonds**: two orthogonal p-p overlaps
- **Bond energy**: C≡C ~839 kJ/mol
- **Bond length**: C≡C ~120 pm (shorter than C=C)
- **Geometry**: Linear, 180° bond angles
- **Hybridization**: sp (50% s character)

### Comparison of Multiple Bonds
| Bond Type | Length (pm) | Energy (kJ/mol) | Geometry |
|-----------|-------------|-----------------|----------|
| C-C | 154 | 347 | Tetrahedral |
| C=C | 134 | 611 | Trigonal planar |
| C≡C | 120 | 839 | Linear |

### Acidity of Terminal Alkynes
- Terminal alkynes (R-C≡C-H) have acidic protons
- **pKa ≈ 25** (more acidic than other hydrocarbons)
- Can be deprotonated by strong bases (NaNH₂, NaH, n-BuLi)
- Form acetylide anions: R-C≡C:⁻

## Nomenclature

### IUPAC Rules
1. Find longest chain containing the triple bond
2. Number from end nearest the triple bond
3. Name as "alkyne" with position number
4. Suffix: "-yne"

### Examples
| Structure | IUPAC Name |
|-----------|------------|
| HC≡C-CH₂-CH₃ | But-1-yne |
| CH₃-C≡C-CH₃ | But-2-yne |
| HC≡CH | Ethyne (acetylene) |

## Reactions of Alkynes

### 1. Reduction (Hydrogenation)

**Complete reduction to alkane:**
```
R-C≡C-R' + 2H₂ (Pd/C) → R-CH₂-CH₂-R'
```

**Lindlar catalyst (syn addition, cis-alkene):**
```
R-C≡C-R' + H₂ (Lindlar's Pd) → R-C=C-R' (cis)
```

**Dissolving metal reduction (anti addition, trans-alkene):**
```
R-C≡C-R' + Na/NH₃(l) → R-C=C-R' (trans)
```

### 2. Electrophilic Addition

**Hydrohalogenation:**
```
R-C≡C-R' + HX → R-CX=CH-R' (Markovnikov)
R-C≡C-R' + 2HX → R-CX₂-CH₂-R'
```

**Halogenation:**
```
R-C≡C-R' + X₂ → R-CX=CX-R' (anti)
R-C≡C-R' + 2X₂ → R-CX₂-CX₂-R'
```

### 3. Hydration

**Mercury(II)-catalyzed:**
```
R-C≡C-R' + H₂O, Hg²⁺, H₂SO₄ → R-CO-CH₂-R'
```
- Forms ketone (Markovnikov)
- Terminal alkynes form methyl ketones

**Hydroboration-oxidation:**
```
R-C≡C-H + BH₃, H₂O₂/OH⁻ → R-CH₂-CHO
```
- Forms aldehyde from terminal alkyne
- Anti-Markovnikov

### 4. Acetylide Chemistry

**Formation:**
```
R-C≡C-H + NaNH₂ → R-C≡C-Na⁺ + NH₃
```

**Alkylation (C-C bond formation):**
```
R-C≡C-Na⁺ + R'-X → R-C≡C-R' + NaX
```
- Works with primary alkyl halides and methyl halides
- SN2 mechanism

**Nucleophilic addition:**
```
R-C≡C-Na⁺ + C=O → R-C≡C-C-OH (after workup)
```
- Adds to aldehydes, ketones, epoxides

## Synthesis of Alkynes

### 1. Alkylation of Terminal Alkynes
```
HC≡C-H → HC≡C-Na⁺ → HC≡C-R
```
- Best with primary alkyl halides
- Extends carbon chain

### 2. Double Elimination from Vicinal Dihalides
```
R-CHX-CHX-R' + 2 NaNH₂ → R-C≡C-R'
```
- Anti elimination via vinyl halide intermediate

### 3. Triple Bond Formation from Alkenes
```
R-C=C-R' → R-CX-CX-R' → R-C≡C-R'
```
1. Halogenation to vicinal dihalide
2. Double dehydrohalogenation

## Reaction Summary Table

| Reaction | Reagent(s) | Product | Notes |
|----------|------------|---------|-------|
| Complete hydrogenation | H₂, Pd/C | Alkane | 2 equivalents H₂ |
| Partial hydrogenation | H₂, Lindlar's | cis-Alkene | Syn addition |
| Partial hydrogenation | Na, NH₃(l) | trans-Alkene | Anti addition |
| Hydrohalogenation | HX (2 equiv) | Geminal dihalide | Markovnikov |
| Halogenation | X₂ (2 equiv) | Tetrahalide | Anti addition |
| Hydration | H₂O, Hg²⁺, H⁺ | Ketone | Markovnikov |
| Hydroboration | BH₃, H₂O₂/OH⁻ | Aldehyde | Anti-Markovnikov |
| Deprotonation | NaNH₂ | Acetylide anion | Terminal alkynes |

## Decision Flow
1. Identify alkyne type (terminal vs internal)
2. For reactions: consider partial vs complete addition
3. For synthesis: choose alkylation or elimination route
4. Use acetylide chemistry for C-C bond formation
5. Consider stereochemistry for partial reduction

## Implementations and Data
- Alkyne reaction predictor: [L3 code](../L3_functions/alkyne_tools.py)
- Reference tables: [L4 reference](../L4_reference/reference/alkyne-reactions-reference.md)

## L3 Tool Call Directives


**Source:** `alkyne_tools.py`

L3 tool module for alkyne tools

### Available functions:
- `classify_alkyne(structure: str)` → AlkyneType — Classify an alkyne as terminal or internal.
- `get_alkyne_formula(carbons: int)` → str — Get the molecular formula for a straight-chain alkyne.
- `is_terminal_alkyne(structure: str)` → bool — Check if an alkyne is terminal (has acidic proton).
- `can_form_acetylide(structure: str)` → bool — Check if an alkyne can form an acetylide anion.
- `suitable_base_for_deprotonation()` → dict — Get bases suitable for deprotonating terminal alkynes.
- `predict_partial_hydrogenation_product(catalyst: str)` → tuple — Predict the product of partial hydrogenation.
- `predict_hydration_product(alkyne_type: AlkyneType, method: str)` → str — Predict the product of alkyne hydration.
- `alkylation_with_acetylide(acetylide: str, alkyl_halide: str)` → str — Predict the product of acetylide alkylation.
- `suitable_alkyl_halides_for_alkylation()` → List[str] — Get alkyl halides suitable for acetylide alkylation.
- `synthesis_from_vicinal_dihalide()` → List[str] — Get steps for alkyne synthesis from vicinal dihalide.
- `compare_triple_bond_properties()` → dict — Compare properties of single, double, and triple bonds.
- `alkyne_naming_rules()` → List[str] — Get IUPAC naming rules for alkynes.
- `alkyne_reaction_summary()` → dict — Get summary of major alkyne reactions.
- `test_alkyne_classification()` → any — Test alkyne classification
- `test_formulas()` → any — Test formula generation
- `test_partial_hydrogenation()` → any — Test partial hydrogenation prediction
- `test_hydration()` → any — Test hydration prediction

### Common errors:
- ❌ Passing wrong parameter types (strings where numbers expected)
- ❌ Forgetting required parameters
