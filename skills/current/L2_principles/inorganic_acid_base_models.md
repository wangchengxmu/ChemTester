---
id: inorganic.acid.base.models
layer: 2
title: Inorganic Acid-Base Models
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - ../L3_functions/acid_base_tools.py
cross_links:
  - ./bronsted_lowry.md
  - ./lewis_acid_base.md
source: Inorganic Chemistry (LibreTexts), Ch6 - Acid-Base and Donor-Acceptor Chemistry
---

## Context

Beyond the common Brønsted-Lowry and Lewis definitions, inorganic chemistry employs several specialized acid-base models for specific contexts: high-temperature systems, nonaqueous solvents, and predictive stability trends. This file covers models NOT in standard general chemistry textbooks.

---

## Summary of Acid-Base Models

| Model | Acid Definition | Base Definition | Best Used For |
|-------|----------------|-----------------|---------------|
| Arrhenius | Increases [H₃O⁺] in water | Increases [OH⁻] in water | Aqueous solutions |
| Brønsted-Lowry | H⁺ donor | H⁺ acceptor | Protic solvents, H-transfer reactions |
| **Lux-Flood** | O²⁻ acceptor | O²⁻ donor | Oxide/oxyanion reactions, geochemistry |
| **Solvent System** | Solvent cation or increases [cation] | Solvent anion or increases [anion] | Nonaqueous solvents (BrF₃, NH₃, H₂SO₄) |
| Lewis | Electron pair acceptor | Electron pair donor | Coordination chemistry, adduct formation |
| **Usanovich** | Electron acceptor | Electron donor | Includes redox reactions |
| Nucleophile-Electrophile | Electrophilic center | Nucleophile (electron pair donor) | Organic reaction mechanisms |

---

## Lux-Flood Model

**Key concept:** Acid-base reactions involve transfer of oxide ion (O²⁻), not H⁺.

### Definitions
- **Acid:** Oxide ion acceptor
- **Base:** Oxide ion donor

### Example Reactions
```
SiO₂ + CaO → CaSiO₃
(acid)   (base)

CO + H₂O → H₂ + CO₂
(base) (acid)  (oxide transfer involved in redox)
```

### Applications
- **Geochemistry:** Silicate mineral formation, oxide melt chemistry
- **High-temperature chemistry:** Reactions in molten oxides
- **Ceramic processing:** Oxide-based solid-state reactions

---

## Solvent System Acid-Base Concept

**Key concept:** Generalizes Arrhenius definition to any autoionizing solvent.

### Definitions
- **Acid:** The solvent cation OR any substance that increases [solvent cation]
- **Base:** The solvent anion OR any substance that increases [solvent anion]

### Autoionization Examples

| Solvent | Autoionization | Solvent Cation | Solvent Anion |
|---------|----------------|----------------|---------------|
| H₂O | 2H₂O ⇌ H₃O⁺ + OH⁻ | H₃O⁺ | OH⁻ |
| NH₃(l) | 2NH₃ ⇌ NH₄⁺ + NH₂⁻ | NH₄⁺ | NH₂⁻ |
| H₂SO₄(l) | 2H₂SO₄ ⇌ H₃SO₄⁺ + HSO₄⁻ | H₃SO₄⁺ | HSO₄⁻ |
| BrF₃(l) | 2BrF₃ ⇌ BrF₂⁺ + BrF₄⁻ | BrF₂⁺ | BrF₄⁻ |
| SeOCl₂(l) | 2SeOCl₂ ⇌ SeOCl⁺ + SeOCl₃⁻ | SeOCl⁺ | SeOCl₃⁻ |

### Example: Chemistry in BrF₃

```
SbF₅ + BrF₃ → SbF₆⁻ + BrF₂⁺    (SbF₅ is an acid - increases BrF₂⁺)
(acid)

KF + BrF₃ → K⁺ + BrF₄⁻          (KF is a base - increases BrF₄⁻)
(base)

KF + SbF₅ → KSbF₆               (neutralization)
(base)  (acid)
```

### Application: Thionyl Chloride (SOCl₂)
```
SOCl₂ ⇌ SOCl⁺ + SOCl₃⁻

Na₂SO₃ + SOCl₂ → 2NaCl + 2SO₂
(base)    (acid)
```
SO₃²⁻ acts as a base, SOCl₂ acts as an acid.

---

## Superacids and the Hammett Acidity Function

**Definition:** Superacids have Brønsted acidity greater than 100% H₂SO₄ (Hammett acidity H₀ < -12).

### Hammett Acidity Function (H₀)

Generalizes pH to nonaqueous/concentrated acids:

```
H₀ = -log(a_H⁺)  ≈  pK_ion - log([BH⁺]/[B])
```

Where B is a weak indicator base (e.g., nitroaromatics).

### Hammett Acidity Values

| Acid | H₀ |
|------|-----|
| H₂SO₄ (100%) | -12 |
| HClO₄ | -13.0 |
| CF₃SO₃H (triflic acid) | -14.6 |
| FSO₃H (fluorosulfonic acid) | -15.6 |
| Magic Acid (SbF₅·FSO₃H) | -21 to -24 |
| Fluoroantimonic acid (SbF₅·HF) | -21 to -24 |

### Superacid Chemistry

Superacids can protonate:
- **Ordinary acids:** H₃PO₄, HNO₃, carboxylic acids become protonated
- **Alkanes:** CH₄ + Magic Acid → CH₅⁺ → CH₃⁺ + H₂
- **Inert species:** Noble gas compounds, extremely weak bases

**Industrial use:** Solid superacids (sulfated metal oxides) for carbocation generation in isomerization and alkylation.

---

## Hard and Soft Acids and Bases (HSAB Principle)

**Key concept:** Lewis acids and bases exhibit preferential bonding based on "hardness" or "softness."

### Definitions

| | Hard | Soft |
|--|------|------|
| **Acids** | Small, high charge, low polarizability | Large, low charge, high polarizability |
| **Bases** | Donor atom: N, O, F (high electronegativity) | Donor atom: P, S, I (low electronegativity) |

### Principle
- **Hard-Hard** interactions: Electrostatic, stable
- **Soft-Soft** interactions: Covalent, stable
- **Hard-Soft** interactions: Less stable

### Examples of Hard vs. Soft

**Hard Acids:** H⁺, Li⁺, Na⁺, K⁺, Mg²⁺, Ca²⁺, Al³⁺, Fe³⁺, Ti⁴⁺

**Soft Acids:** Cu⁺, Ag⁺, Au⁺, Hg²⁺, Pt²⁺, Pd²⁺, BH₃, I₂

**Hard Bases:** H₂O, OH⁻, F⁻, Cl⁻, NH₃, RO⁻, CO₃²⁻

**Soft Bases:** H⁻, I⁻, SCN⁻, R₂S, R₃P, CN⁻, CO

### Applications

1. **Geochemistry (Goldschmidt classification)**
   - Lithophiles (oxide/halide formers): Hard acids (Na⁺, K⁺, Mg²⁺, Al³⁺)
   - Chalcophiles (sulfide formers): Soft acids (Cu⁺, Ag⁺, Hg²⁺, Pb²⁺)

2. **Bioinorganic chemistry**
   - Fe³⁺ (hard) → binds O-donors (transferrin), N-donors (heme)
   - Zn²⁺ (borderline) → binds S-donors (zinc finger proteins)
   - Cu⁺ (soft) → binds S-donors (metallothionein)

3. **Ambidentate ligand coordination**
   - SCN⁻ can bind through S (soft) or N (hard)
   - Hard metals (Fe³⁺, Al³⁺) → N-thiocyanato complexes
   - Soft metals (Hg²⁺, Au³⁺) → S-thiocyanato complexes

4. **Solubility trends**
   - Ag⁺ (soft): AgF >> AgCl > AgBr > AgI (opposite trend)
   - Li⁺ (hard): LiF << LiCl < LiBr < LiI (normal trend)

---

## Usanovich Model

**Definition:** Extends Lewis concept to include ALL electron transfer reactions.

- **Acid:** Accepts electrons (any number)
- **Base:** Donates electrons (any number)

**Includes:**
- Lewis acid-base reactions (pair transfer)
- Redox reactions (complete electron transfer)
- Radical reactions

**Example:**
```
:NH₃ + BH₃ → H₃N-BH₃    (Lewis adduct)
Fe²⁺ + Ce⁴⁺ → Fe³⁺ + Ce³⁺ (redox, also acid-base by Usanovich)
```

---

## Frontier Orbital Connection

Lewis acid-base reactions can be understood via molecular orbital theory:

- **Base HOMO** (highest occupied) donates electron pair
- **Acid LUMO** (lowest unoccupied) accepts electron pair

**Orbital energy matching:**
- Hard-hard: Large HOMO-LUMO gap → electrostatic
- Soft-soft: Small HOMO-LUMO gap → covalent

---

## Problem-Solving Strategies

### Choosing the Right Model

1. **Aqueous solution with H⁺ transfer?** → Brønsted-Lowry
2. **Oxide/oxyanion system (high T)?** → Lux-Flood
3. **Nonaqueous solvent?** → Solvent System
4. **Coordination compound formation?** → Lewis
5. **Predicting metal-ligand preferences?** → HSAB
6. **Redox involved?** → Usanovich

### Example Problems

**Problem 1:** Predict whether KF or KI is more soluble in liquid BrF₃.

**Solution:** F⁻ (hard) increases BrF₄⁻ concentration (base in BrF₃ system). I⁻ is soft and doesn't interact as effectively. KF is more soluble.

**Problem 2:** Predict the coordination mode of SCN⁻ to Fe³⁺ vs. Hg²⁺.

**Solution:**
- Fe³⁺ is hard → binds through N (harder) → N-thiocyanato complex
- Hg²⁺ is soft → binds through S (softer) → S-thiocyanato complex

---

## Links

- **L3 Tools:** Acid-base equilibrium calculators
- **L4 Reference:** Hammett acidity tables, HSAB classification tables
- **L5 Examples:** Superacid reactions, solvent system neutralizations

---

## Sources

- Inorganic Chemistry (LibreTexts), Ch6: Acid-Base and Donor-Acceptor Chemistry
- Huheey, Keiter, Keiter — Inorganic Chemistry (Usanovich quote)
- Gillespie, R. J. — Superacid chemistry, Hammett function development
