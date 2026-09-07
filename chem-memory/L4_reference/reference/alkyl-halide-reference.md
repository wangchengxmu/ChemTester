# Alkyl Halide Chemistry Reference

## C-X Bond Properties

| Bond | Length (pm) | Strength (kJ/mol) | Strength (kcal/mol) | Dipole (D) |
|------|-------------|-------------------|---------------------|------------|
| C-F | 139 | 460 | 110 | 1.85 |
| C-Cl | 178 | 350 | 84 | 1.87 |
| C-Br | 193 | 294 | 70 | 1.81 |
| C-I | 214 | 239 | 57 | 1.62 |

**Trends:**
- Bond strength decreases down the group
- Bond length increases down the group
- Reactivity increases down the group (C-I most reactive)

---

## H-Abstraction Reactivity

### Chlorination
| H Type | Relative Reactivity |
|--------|---------------------|
| Primary (1°) | 1 |
| Secondary (2°) | 3.5 |
| Tertiary (3°) | 5 |

### Bromination (More Selective)
| H Type | Relative Reactivity |
|--------|---------------------|
| Primary (1°) | 1 |
| Secondary (2°) | 80 |
| Tertiary (3°) | 1600 |

---

## C-H Bond Energies (kJ/mol)

| Type | Energy | Radical Stability |
|------|--------|-------------------|
| Vinylic | 465 | Least stable |
| Primary | 421 | |
| Secondary | 410 | |
| Tertiary | 400 | |
| Allylic | 370 | Most stable |
| Benzylic | 375 | Very stable |

---

## Common Alkyl Halide Nomenclature

| Structure | IUPAC Name | Common Name |
|-----------|------------|-------------|
| CH₃Cl | Chloromethane | Methyl chloride |
| CH₃CH₂Br | Bromoethane | Ethyl bromide |
| CH₃CH₂CH₂I | 1-Iodopropane | Propyl iodide |
| CH₃CHClCH₃ | 2-Chloropropane | Isopropyl chloride |
| (CH₃)₃CBr | 2-Bromo-2-methylpropane | tert-Butyl bromide |
| CH₂Cl₂ | Dichloromethane | Methylene chloride |
| CHCl₃ | Trichloromethane | Chloroform |
| CCl₄ | Tetrachloromethane | Carbon tetrachloride |

---

## Alcohol to Alkyl Halide Reagents

| Alcohol Type | Target Halide | Reagent | Conditions |
|--------------|---------------|---------|------------|
| 3° | Cl, Br, I | HX | Cold ether, rapid |
| 1°, 2° | Cl | SOCl₂ | Mild, with base |
| 1°, 2° | Br | PBr₃ | Mild conditions |
| Any | F | HF/pyridine or DAST | Special |

---

## Grignard Reagent Properties

- **Formation:** R-X + Mg → R-Mg-X (in ether or THF)
- **Halogen reactivity:** I > Br > Cl >> F
- **C-Mg bond:** Polar, carbon is nucleophilic
- **Conjugate acid pKa:** 44-60 (very weak acid)
- **Must exclude:** H₂O, ROH, COOH, NH₂ groups

---

## Organometallic Coupling Summary

### Gilman Reagents (R₂CuLi)
- Formation: 2 R-Li + CuI → R₂CuLi + LiI
- Works with: Cl, Br, I (not F)
- Substrates: Alkyl, aryl, vinylic halides
- Product: R-R' (C-C bond formation)

### Suzuki-Miyaura Coupling
- Reagents: Ar-B(OH)₂ + Ar'-X + Pd cat. + base
- Works with: Aryl and vinylic halides only
- Catalyst: Pd(0), catalytic amount
- Product: Biaryl compounds

---

## Oxidation Level Reference

### Quick Reference Table

| Compound | C-H | C-O/C-N/C-X | Level |
|----------|-----|-------------|-------|
| Alkane | Maximum | 0 | Lowest |
| Alkene | Fewer | 0 | Low |
| Alcohol | -1 vs alkane | +1 | Medium |
| Aldehyde/Ketone | -2 vs alkane | +1 | Medium-High |
| Carboxylic Acid | Few | +2 | High |
| CO₂ | 0 | +4 | Highest |

### Level Hierarchy
```
Alkane < Alkene < Alcohol < Aldehyde/Ketone < Carboxylic Acid < CO₂
```

---

## Common Test Problems

### Problem 1: Product Distribution
**Question:** What is the product distribution for monochlorination of butane?

**Answer:**
- 1° H at C1: 6 H × 1 = 6 contribution
- 2° H at C2: 4 H × 3.5 = 14 contribution
- Total = 20
- 1-Chlorobutane: 6/20 × 100 = 30%
- 2-Chlorobutane: 14/20 × 100 = 70%

### Problem 2: Oxidation Classification
**Question:** Is the reaction CH₄ + Cl₂ → CH₃Cl + HCl an oxidation or reduction?

**Answer:**
- CH₄: Level = 0 - 4 = -4
- CH₃Cl: Level = 1 - 3 = -2
- Level increases (-4 → -2), so **Oxidation**

### Problem 3: Grignard Reaction
**Question:** Will CH₃MgBr react with NH₃ (pKa = 35)?

**Answer:**
- Grignard conjugate acid pKa = 44-60
- NH₃ pKa = 35 < 44
- Yes, reaction occurs: CH₃MgBr + NH₃ → CH₄ + H₂N-MgBr
