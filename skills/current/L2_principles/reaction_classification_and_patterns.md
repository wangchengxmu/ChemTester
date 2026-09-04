---
id: chem.reaction_classification
layer: 2
title: Reaction Classification and Patterns
source: LibreTexts Chemistry 2e Ch04.02
status: active
created: 2026-03-10
last_verified: 2026-03-11
---

# Reaction Classification and Patterns

## Problem type
Classify reaction by type and predict products; write balanced equation.

## Decision tree

1. **What reaction type?**
   - Precipitation → Check solubility rules
   - Acid-base → Identify acid/base, write neutralization
   - Redox → Assign oxidation numbers, identify oxidized/reduced

2. **Precipitation prediction?**
   - Identify all ions in solution
   - Check all possible cation-anion pairings
   - If any pairing is insoluble → precipitate forms

3. **Acid-base?**
   - Strong acid + strong base → salt + water
   - Weak acid/base → equilibrium (partial reaction)

4. **Redox?**
   - Assign oxidation numbers to all elements
   - If any oxidation number changes → redox
   - Species with increasing ON = oxidized
   - Species with decreasing ON = reduced

## Core patterns

### Precipitation (Double Displacement)
```
AB(aq) + CD(aq) → AD(s) + CB(aq)
Net ionic: A⁺(aq) + D⁻(aq) → AD(s)
```
- Requires one insoluble product
- Spectator ions removed from net ionic

### Acid-Base Neutralization
```
acid + base → salt + water
H₃O⁺(aq) + OH⁻(aq) → 2 H₂O(l)  (strong-strong net ionic)
```
- Strong acids: HCl, HBr, HI, HNO₃, HClO₄, H₂SO₄
- Strong bases: Group 1 hydroxides, Ba(OH)₂

### Oxidation-Reduction
```
oxidation: species loses electrons (ON increases)
reduction: species gains electrons (ON decreases)
```
- Oxidizing agent = species reduced (gains e⁻)
- Reducing agent = species oxidized (loses e⁻)

## Solubility Rules (key patterns)

### Soluble
- All Group 1 salts (Li⁺, Na⁺, K⁺, Rb⁺, Cs⁺)
- All ammonium salts (NH₄⁺)
- All nitrates (NO₃⁻)
- All acetates (C₂H₃O₂⁻)
- All perchlorates (ClO₄⁻)
- Chlorides, bromides, iodides EXCEPT Ag⁺, Hg₂²⁺, Pb²⁺
- Sulfates EXCEPT Ag⁺, Ba²⁺, Ca²⁺, Hg₂²⁺, Pb²⁺, Sr²⁺

### Insoluble
- Carbonates (CO₃²⁻), phosphates (PO₄³⁻), chromates (CrO₄²⁻), sulfides (S²⁻)
  - EXCEPT Group 1 and NH₄⁺
- Hydroxides (OH⁻)
  - EXCEPT Group 1 and Ba²⁺

## Oxidation Number Assignment

1. Element in elemental form → 0
2. Monatomic ion → ion charge
3. H: +1 with nonmetals, −1 with metals
4. O: −2 in most compounds (−1 in peroxides)
5. Sum = molecular charge

## Common patterns
- Mix two ionic solutions → check for precipitation
- Mix acid + base → neutralization
- Element + compound → often redox
- Combustion → always redox (C oxidized, O reduced)

## Links

### L3 Implementation
- `../L3_functions/reaction_classification_tools.py` (TODO - needs implementation)

### L4 Reference

### L5 Examples
- `../L5_examples/stoichiometry/ (TODO)

## Source trace
- `../sources/ingestion/source-stoichiometry-chemical-reactions-stepwise.md` section 4.02
## L3 Tool Call Directives

**Source:** 
eaction_classification_tools.py
Reaction classification, solubility rules, oxidation states, redox identification.

### Available functions:
- is_soluble(cation, anion) → bool — Solubility check based on standard rules
- predict_precipitation(reactants: List[Tuple]) → Dict — precipitation bool, precipitate tuple, solubility_check dict
- is_strong_acid(formula) → bool — Check if strong acid (HCl, HBr, HI, HNO₃, HClO₄, H₂SO₄)
- is_strong_base(formula) → bool — Check if strong base
- ssign_oxidation_numbers(formula, charge=0) → Dict — Element → oxidation number
- identify_redox(reactant_oxidation, product_oxidation) → Dict — is_redox, oxidized, reduced, agents
- classify_reaction(reactants: List[str], products: List[str]) → str — precipitation/acid_base/redox/combination/decomposition/combustion/unknown

### Common errors:
- ❌ Passing compound names instead of ion symbols to is_soluble (e.g., 'NaCl' vs 'Na','Cl')
- ❌ classify_reaction relies on phase labels like '(aq)' and '(s)' for precipitation detection
