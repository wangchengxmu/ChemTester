# L2 Topic: Enzyme Mechanisms

**Source**: LibreTexts Biochemistry (Jakubowski and Flatt), Ch6
**Created**: 2026-03-18
**Status**: Scaffold (Pass-1)

---

## Concept Overview

Enzymes catalyze biochemical reactions through specific mechanisms that lower activation energy. Key catalytic strategies include proximity/orientation effects, acid-base catalysis, covalent catalysis, and transition state stabilization. Many enzymes require cofactors for their catalytic activity.

### Key Features
1. **Active site**: Specialized pocket that binds substrate and catalyzes reaction
2. **Catalytic strategies**: Proximity, orientation, acid-base, covalent, electrostatic
3. **Cofactors**: Metal ions and coenzymes that enhance catalysis
4. **Arrow pushing**: Electron flow from sources to sinks

---

## Core Principles

### Enzyme Classification (IUBMB EC Numbers)

| EC Class | Type | Description |
|----------|------|-------------|
| EC 1 | Oxidoreductases | Redox reactions |
| EC 2 | Transferases | Group transfer |
| EC 3 | Hydrolases | Hydrolysis reactions |
| EC 4 | Lyases | Elimination forming double bond |
| EC 5 | Isomerases | Isomer interconversions |
| EC 6 | Ligases | Condensation (ATP-dependent) |
| EC 7 | Translocases | Membrane transport |

### Catalytic Strategies

| Strategy | Mechanism | Example |
|----------|-----------|---------|
| Proximity/orientation | Brings reactants together in optimal geometry | All enzymes |
| Acid-base catalysis | Proton transfer by side chains | Serine proteases (His) |
| Covalent catalysis | Formation of covalent enzyme-substrate intermediate | Serine proteases, PLP enzymes |
| Electrostatic catalysis | Charge stabilization of transition state | Metalloenzymes |
| Transition state binding | Preferential binding to TS vs substrate | All enzymes |
| Strain/distortion | Bending substrate toward TS geometry | Lysozyme |

### Electron Sources and Sinks

**Electron Flow in Enzyme Mechanisms:**

```
SOURCE → SINK
Anion (nucleophile) → Carbonyl C (electrophile)
Lone pair → Imine/N⁺ (better sink)
Carbanion → Metal ion
Hydride (H:⁻) → NAD⁺, FAD
```

**Arrow Pushing Rules:**
- Arrows show electron movement (not atom movement)
- From lone pair or bond → electron-deficient center
- Maximum 2 electrons per arrow
- Conservation of charge and mass

### Covalent Catalysis

**Serine Proteases (Chymotrypsin Mechanism):**

1. **Acylation**: Ser-OH attacks carbonyl, His acts as base
   - Formation of tetrahedral intermediate
   - Collapse to acyl-enzyme + leaving group

2. **Deacylation**: Water attacks acyl-enzyme
   - His acts as base to deprotonate water
   - Release of product, regeneration of enzyme

**Key Catalytic Triad:**
- Ser195: Nucleophile (covalent catalysis)
- His57: General base/acid
- Asp102: Electrostatic stabilization of His⁺

### Acid-Base Catalysis

**General Acid Catalysis**: Proton donor facilitates reaction
```
HA + S → A⁻ + SH⁺ (protonated intermediate)
```

**General Base Catalysis**: Proton acceptor facilitates reaction
```
B: + SH → BH⁺ + S⁻ (deprotonated intermediate)
```

**pKa Considerations:**
- Catalytic residue pKa often perturbed by microenvironment
- His (pKa ~6-7) ideal for physiological pH
- Asp/Glu (pKa ~4) act as acids at neutral pH
- Lys (pKa ~10) acts as base when deprotonated

---

## Cofactor Chemistry

### Types of Cofactors

| Category | Examples | Function |
|----------|----------|----------|
| Metal ions | Zn²⁺, Mg²⁺, Fe²⁺/Fe³⁺, Cu²⁺ | Lewis acid, redox |
| Coenzymes (dissociable) | NAD⁺, NADP⁺, CoA | Group transfer |
| Prosthetic groups (tight) | FAD, heme, biotin | Redox, CO₂ transfer |

### Major Coenzymes and Their Reactions

| Coenzyme | Vitamin Precursor | Reaction Type |
|----------|------------------|---------------|
| NAD⁺/NADP⁺ | Niacin (B3) | Hydride transfer (oxidation) |
| FAD | Riboflavin (B2) | Hydride transfer (oxidation) |
| TPP | Thiamine (B1) | α-Keto acid decarboxylation |
| PLP | Pyridoxal (B6) | Amino acid transformations |
| CoA | Pantothenate (B5) | Acyl group transfer |
| Biotin | Biotin (B7) | CO₂ fixation |
| THF | Folate (B9) | 1-C transfer |

### Thiamine Pyrophosphate (TPP) Mechanism

**Decarboxylation of α-Keto Acids:**

1. Thiazolium ring C2 acts as nucleophile (ylide formation)
2. Attack on carbonyl of substrate
3. Electron sink: positively charged N stabilizes carbanion
4. CO₂ release, then product formation

**Key Feature**: Thiazolium C2-H is acidic (pKa ~10) due to adjacent N⁺

### FAD/NAD⁺ Hydride Transfer

**FAD Oxidation of Succinate:**
```
Succinate → Fumarate + FADH₂
:CH₂-CH₂: → :CH=CH: + 2e⁻ + H⁺
```
- Hydride (H:⁻) transfer: 2 electrons + 1 proton
- Occurs in dry active site (hydride unstable in water)

**NAD⁺ Oxidation of Alcohols:**
```
R-CH₂OH + NAD⁺ → R-CHO + NADH + H⁺
```
- NAD⁺ is dissociable (acts as substrate)
- FAD is tightly bound (must be regenerated)

### Pyridoxal Phosphate (PLP) Chemistry

**Schiff Base Formation:**
```
PLP-aldehyde + R-NH₂ → PLP-imine (Schiff base)
```
- Replaces C=O (poor sink) with C=N⁺ (excellent sink)
- Enables multiple reaction types at α-carbon

**PLP-Dependent Reactions:**

| Reaction Type | Example |
|--------------|---------|
| Transamination | Amino acid + α-keto acid → new amino acid |
| Decarboxylation | Amino acid → amine + CO₂ |
| Racemization | L-amino acid ↔ D-amino acid |
| β-Elimination | Serine → pyruvate + NH₃ |
| Condensation | Glycine + succinyl-CoA → ALA |

**Electron Sink Mechanism:**
- Pyridinium ring N⁺ stabilizes carbanion intermediates
- Quinonoid intermediate is key reactive species

### Metal Ion Catalysis

| Metal | Coordination | Role | Example |
|-------|--------------|------|---------|
| Zn²⁺ | Tetrahedral | Lewis acid, polarize substrate | Carbonic anhydrase |
| Mg²⁺ | Octahedral | Phosphate binding, charge shielding | Kinases, polymerases |
| Fe²⁺/Fe³⁺ | Various | Redox, O₂ activation | Cytochromes, P450 |
| Cu²⁺ | Various | Redox | Superoxide dismutase |

---

## Decision Trees

### Identifying Catalytic Mechanism
```
Is covalent intermediate formed? → Covalent catalysis
Is proton transferred? → Acid-base catalysis
Is metal present in active site? → Metal ion catalysis
Is transition state stabilized? → TS binding
```

### Choosing Coenzyme for Reaction
```
Need to transfer hydride? → NAD⁺/NADP⁺ or FAD
Need to decarboxylate α-keto acid? → TPP
Need to modify amino acid? → PLP
Need to transfer acyl group? → CoA
Need to fix CO₂? → Biotin
```

### Arrow Pushing in Biochemical Mechanisms
```
1. Identify electron source (nucleophile)
2. Identify electron sink (electrophile)
3. Draw arrow from source to sink
4. Account for all electrons and charges
5. Check that octets are maintained
```

---

## Key Tables

### Comparison of Coenzyme Types

| Property | NAD⁺/NADP⁺ | FAD | TPP | PLP |
|----------|------------|-----|-----|-----|
| Binding | Loose | Tight | Tight | Tight |
| Vitamin | Niacin | Riboflavin | B1 | B6 |
| Reaction | Redox | Redox | Decarboxylation | Amino transfer |
| Electrons transferred | 2 | 2 | — | — |
| Regeneration needed? | No | Yes | Yes | Yes |

### Vitamin-Deficiency Diseases

| Vitamin | Coenzyme | Deficiency Disease |
|---------|----------|-------------------|
| B1 (Thiamine) | TPP | Beriberi |
| B2 (Riboflavin) | FAD | Ariboflavinosis |
| B3 (Niacin) | NAD⁺ | Pellagra |
| B6 (Pyridoxal) | PLP | Anemia, convulsions |
| B7 (Biotin) | Biotin | Dermatitis |
| B9 (Folate) | THF | Megaloblastic anemia |

---

## Cross-Links

- **enzyme_kinetics.md**: Michaelis-Menten kinetics, inhibition
- **protein_secondary_structure.md**: Active site architecture
- **amino_acid_properties.md**: pKa values of catalytic residues
- **redox_chemistry.md**: Electron transfer mechanisms
- **cofactors.md**: Detailed cofactor structures and mechanisms

---

## References

1. LibreTexts Biochemistry (Jakubowski and Flatt), Ch6: Enzyme Activity
2. Fersht, A. (1999). Structure and Mechanism in Protein Science
3. Silverman, R.B. (2002). The Organic Chemistry of Enzyme-Catalyzed Reactions
