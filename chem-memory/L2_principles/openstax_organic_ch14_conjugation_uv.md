---
id: organic.openstax_ch14
layer: 2
title: Conjugated Compounds and UV Spectroscopy
up_links:
  - ../L1_ontology/organic_chemistry.md
down_links:
  - ../L4_reference/woodward_fieser_rules.md
---

# Conjugated Compounds and UV Spectroscopy

## Key Principles

### Conjugation Definition
- Alternating single and double bonds (or lone pairs)
- p-orbitals overlap across adjacent atoms
- Delocalization lowers overall energy

### Stability from Conjugation
- Conjugated dienes more stable than isolated dienes
- Heat of hydrogenation lower than expected
- 1,3-butadiene: ~15 kJ/mol stabilization

### Molecular Orbital View
- Conjugation lowers HOMO-LUMO gap
- More conjugated = smaller energy gap
- Longer wavelength absorption in UV-Vis

## Mechanisms

### Electrophilic Addition to Conjugated Dienes

**Key Feature:** Allylic carbocation intermediates

1,3-Butadiene + HBr:
```
Step 1: H⁺ adds to C1 → allylic carbocation (resonance stabilized)
        [⁺CH2-CH=CH-CH3 ↔ CH2=CH-CH⁺-CH3]
Step 2: Br⁻ attacks either C1 (1,2-addition) or C3 (1,4-addition)
```

**Resonance of Allylic Cation:**
- Positive charge shared between C1 and C3
- Both positions can react with nucleophile
- Leads to mixture of 1,2 and 1,4 products

### 1,2 vs 1,4 Addition

| Feature | 1,2-Addition | 1,4-Addition |
|---------|--------------|--------------|
| Nucleophile attacks | C1 (original carbocation) | C3 (resonance carbon) |
| Product | Double bond at original position | Double bond migrated |
| Temperature | Favored at LOW temp | Favored at HIGH temp |
| Control | Kinetic | Thermodynamic |
| Stability | Less stable product | More stable product |

### Kinetic vs Thermodynamic Control

**Kinetic Control (Low Temperature):**
- Product forms faster wins
- 1,2-addition predominates
- Reaction irreversible under conditions
- Lower activation energy pathway

**Thermodynamic Control (High Temperature):**
- More stable product wins
- 1,4-addition predominates
- Reaction reversible, reaches equilibrium
- 1,4 product has more substituted double bond

**Energy Diagram:**
```
        TS(1,2)    TS(1,4)
           |\      /|
           | \    / |
           |  \/   |
    Reactants     Products
                   |      \
                   |       \  (1,4 more stable)
                   |        \
                (1,2)     (1,4)
```

### Diels-Alder Cycloaddition

**General Reaction:**
```
Diene + Dienophile → Cyclohexene
```

**Mechanism:**
- Concerted pericyclic reaction (single step)
- No intermediates
- Cyclic transition state
- Two new σ bonds form simultaneously

**Key Requirements:**

1. **Diene must be in s-cis conformation**
   - s-trans dienes cannot react (ends too far apart)
   - Cyclic dienes locked in s-cis are highly reactive

2. **Dienophile reactivity:**
   - Electron-withdrawing groups increase reactivity
   - Good dienophiles: alkenes with -CHO, -COR, -CO2R, -CN, -NO2
   - Ethylene itself is sluggish

3. **Stereospecificity:**
   - Configuration of dienophile retained
   - cis-dienophile → cis-substituted cyclohexene
   - trans-dienophile → trans-substituted cyclohexene

4. **Endo Selectivity:**
   - Endo product favored over exo
   - Dienophile EWG oriented toward diene in transition state
   - More orbital overlap in endo transition state

**Diels-Alder Examples:**
```
1,3-butadiene + ethylene → cyclohexene (slow)
1,3-butadiene + maleic anhydride → bicyclic adduct (fast)
1,3-cyclopentadiene + maleic anhydride → norbornene derivative (endo)
```

## Selectivity & Regiochemistry Rules

### Predicting 1,2 vs 1,4 Products

**Rule 1:** At low temperature (<0°C), 1,2-addition predominates (kinetic)
**Rule 2:** At high temperature (>40°C), 1,4-addition predominates (thermodynamic)
**Rule 3:** 1,4-products have more substituted double bonds → more stable

### Regiochemistry in Diels-Alder

**Unsymmetrical components:**
- Electron-rich end of diene bonds to electron-poor end of dienophile
- "Ortho/para" orientation rule for substituted systems

## UV-Vis Spectroscopy

### Basic Principles
- π → π* transitions absorb in UV region
- λmax depends on HOMO-LUMO gap
- More conjugation = longer λmax (lower energy)

### Woodward-Fieser Rules (Basic)
Each additional feature adds to base value:

| Feature | λmax increment (nm) |
|---------|---------------------|
| Base diene | 217 |
| Each additional conjugated double bond | +30 |
| Alkyl substituent on double bond | +5 |
| Exocyclic double bond | +5 |
| Endocyclic double bond in ring | +36 (cyclohexadiene) |

### Representative λmax Values

| Compound | λmax (nm) |
|----------|-----------|
| Ethylene | 171 |
| 1,3-Butadiene | 217 |
| 1,3,5-Hexatriene | 258 |
| 1,3,5,7-Octatetraene | 290 |
| Benzene | 203, 255 |
| α,β-Unsaturated ketone | ~220-250 |

### UV in Structure Determination
- Presence of absorption >200 nm indicates conjugation
- Cannot distinguish between isomers
- Used with IR, NMR for complete identification
- Extent of conjugation estimated from λmax

## Common Exam Patterns & Traps

### Pattern 1: Predict Both 1,2 and 1,4 Products
```
1,3-cyclohexadiene + HBr → ?
1,2: 3-bromocyclohexene
1,4: 3-bromocyclohexene (same in this case!)
```

### Pattern 2: Diels-Alder Stereochemistry
```
trans-1,2-dideuterioethylene + 1,3-butadiene → ?
Answer: trans-3,6-dideuteriocyclohexene (stereochemistry retained)
```

### Pattern 3: Temperature Effect
```
At 0°C: 1,2-product predominates
At 40°C: 1,4-product predominates
Products interconvert at high temperature via common allylic cation
```

### Trap 1: s-cis Requirement
- Not all conjugated dienes undergo Diels-Alder
- (2E,4E)-2,4-hexadiene cannot achieve s-cis (methyl steric clash)
- Rigid s-trans dienes unreactive

### Trap 2: Kinetic vs Equilibrium Product
- Don't assume thermodynamic product always forms
- Check temperature conditions
- Low temp = kinetic; high temp = thermodynamic

### Trap 3: Endo vs Exo
- Endo is kinetic product (lower activation energy)
- Exo is thermodynamic product (more stable)
- Usually endo predominates under normal conditions

### Trap 4: UV Wavelength Direction
- Longer λmax means LOWER energy (not higher)
- More conjugation → longer wavelength → lower energy gap

### Decision Framework for Addition to Dienes

1. Protonate at both possible positions of diene
2. Draw resonance forms of each allylic carbocation
3. Identify more stable carbocation (more substituted)
4. Attack by nucleophile at both charged positions
5. Determine kinetic product (lower activation energy)
6. Determine thermodynamic product (more substituted double bond)
7. Check temperature to determine which predominates

### Decision Framework for Diels-Alder

1. Verify diene can adopt s-cis conformation
2. Identify electron-rich end of diene
3. Identify electron-poor end of dienophile
4. Match ends for bond formation
5. Apply stereochemistry rules (cis/trans retained)
6. Predict endo product as major
