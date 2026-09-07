---
id: organometallic.chemistry
layer: 2
title: Organometallic Chemistry - Metal-Carbon Bonds
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - ../L3_functions/transition_metals_tools.py
  - ../L4_reference/reference/electrochemical-analysis-data.md
cross_links:
  - ./coordination_chemistry.md
  - ./crystal_field_theory.md
  - ./organic_reaction_mechanisms.md
source: Inorganic Chemistry (LibreTexts), Ch13-14
---

## Context
Organometallic chemistry studies compounds containing metal-carbon bonds. These compounds are central to catalysis, materials science, and synthetic chemistry. The 18-electron rule and Wade's rules help predict stability and structure.

## Classification of Organometallic Compounds

### By Bond Type
| Type | Description | Example |
|------|-------------|---------|
| σ-bonded | Metal-alkyl, metal-aryl | (C₅H₅)₂Ti(CH₃)₂ |
| π-bonded | Alkene, alkyne complexes | Zeise's salt |
| π-arene | Benzene, cyclopentadienyl | Ferrocene |
| Carbene | Metal=CR₂ | Tebbe's reagent |
| Carbonyl | Metal-CO | Fe(CO)₅ |
| Carbide | Metal≡CR | Fischer carbynes |

### By Ligand Type
| Ligand | Hapticity | Electrons Donated |
|--------|-----------|-------------------|
| CO | η¹ | 2 |
| CNR (isocyanide) | η¹ | 2 |
| PR₃ (phosphine) | η¹ | 2 |
| H⁻ (hydride) | η¹ | 2 |
| CH₃⁻ (alkyl) | η¹ | 2 |
| η²-C₂H₄ (ethylene) | η² | 2 |
| η⁴-C₄H₆ (butadiene) | η⁴ | 4 |
| η⁵-C₅H₅ (Cp) | η⁵ | 6 |
| η⁶-C₆H₆ (benzene) | η⁶ | 6 |

## Electron Counting Rules

### 18-Electron Rule
- Stable complexes often have 18 valence electrons
- Corresponds to filled valence shell (ns²np⁶(n-1)d¹⁰)
- Exceptions: early transition metals, bulky ligands

### Counting Methods

**Neutral Atom Method:**
1. Count metal valence electrons (group number)
2. Adjust for complex charge (add for anions, subtract for cations)
3. Count electrons from each ligand (cleave bonds to form neutral fragments)

**Oxidation State Method:**
1. Count metal valence electrons (group number)
2. Determine oxidation state (all bonds considered dative)
3. Subtract electrons for positive oxidation state
4. Add electrons for negative oxidation state
5. Count electrons from ligands (always 2e⁻ per bond)

**Ligand Electron Contributions:**
| Ligand | Neutral Method | Oxidation Method | Charge (for OS) |
|--------|----------------|------------------|-----------------|
| H (hydride) | 1 e⁻ | 2 e⁻ | -1 |
| Cl, Br, I | 1 e⁻ | 2 e⁻ | -1 |
| NH₃, H₂O | 2 e⁻ | 2 e⁻ | 0 |
| CO, PR₃ | 2 e⁻ | 2 e⁻ | 0 |
| η⁵-Cp | 5 e⁻ | 6 e⁻ | -1 |
| Bridging Cl | 3 e⁻ | 4 e⁻ | -1 |

### Coordinative Unsaturation

**Coordinatively Unsaturated:** < 18 electrons
- Tends to add ligands
- Easily reduced
- Higher reactivity

**Coordinatively Oversaturated:** > 18 electrons
- Tends to lose ligands
- Easily oxidized

**16-Electron Square Planar Complexes:**
- Common for Group 10 metals (Ni²⁺, Pd²⁺, Pt²⁺)
- 16 e⁻ is preferred for square planar geometry
- Example: [PdCl₂(NH₃)₂] - 16 e⁻, stable

### Example: Fe(CO)₅
```
Fe (Group 8): 8 e⁻
5 CO: 5 × 2 = 10 e⁻
Total: 18 e⁻ ✓
```

### Example: Ferrocene, Fe(C₅H₅)₂
```
Fe (Group 8): 8 e⁻
2 Cp⁻: 2 × 6 = 12 e⁻
Total: 20 e⁻... but wait!
Fe²⁺: 6 e⁻
2 Cp⁻: 2 × 6 = 12 e⁻
Total: 18 e⁻ ✓
```

## Bonding Models

### CO as Ligand
- σ donation: CO donates lone pair to metal
- π backbonding: Metal d → π* of CO
- Stronger backbonding → weaker C-O bond → lower ν(CO)

### 18-Electron Rule Exceptions
| Type | Reason | Example |
|------|--------|---------|
| Early transition metals | Few d electrons | TiCl₄ (0 e⁻) |
| Square planar | 16 e⁻ is stable | Pd(PPh₃)₄ (16 e⁻) |
| Bulky ligands | Steric hindrance | Pt(PtBu₃)₂ (14 e⁻) |
| High-spin complexes | Weak field | [Fe(H₂O)₆]²⁺ (16 e⁻) |

## Important Ligand Systems

### Cyclopentadienyl (Cp)
- η⁵-bonding (pentahapto) most common
- Cp⁻ is 6-electron donor
- Forms "sandwich" complexes (metallocenes)

### Common Metallocenes
| Complex | Electron Count | Notes |
|---------|----------------|-------|
| Ferrocene, FeCp₂ | 18 | Most stable |
| Cobaltocene, CoCp₂ | 19 | Easily oxidized |
| Nickelocene, NiCp₂ | 20 | Less stable |
| Titanocene dichloride, TiCp₂Cl₂ | 16 | Precursor |

### Carbonyl Clusters
- Metal-metal bonding common
- Wade's rules predict structure
- Examples: Fe₃(CO)₁₂, Co₄(CO)₁₂

## Organometallic Reactions

### Ligand Substitution
```
MLₙX + Y → MLₙY + X
```
- Associative: Common for 16 e⁻ complexes
- Dissociative: Common for 18 e⁻ complexes

### Oxidative Addition
```
MLₙ + X-Y → M(X)(Y)Lₙ  (oxidation +2)
```
- Metal oxidation state increases by 2
- Coordination number increases by 2
- Examples: H₂ addition, alkyl halide addition

### Reductive Elimination
```
M(X)(Y)Lₙ → MLₙ + X-Y  (reduction -2)
```
- Reverse of oxidative addition
- Forms new X-Y bond
- Important in catalytic cycles

### Insertion Reactions
```
M-R + CO → M-C(O)-R (CO insertion)
M-R + C=C → M-C-C-R (olefin insertion)
```

### β-Hydride Elimination
```
M-CH₂-CH₂-R → M-H + CH₂=CH-R
```
- Requires β-hydrogen
- Vacant site on metal
- Forms alkene

### Transmetalation
```
M-R + M'-X → M-X + M'-R
```
- Transfer of organic group between metals
- Important in cross-coupling reactions

## Catalytic Cycles

### Wilkinson's Catalyst (Hydrogenation)
```
RhCl(PPh₃)₃ + H₂ → RhCl(H)₂(PPh₃)₃
RhCl(H)₂(PPh₃)₃ + alkene → RhCl(H)(alkyl)(PPh₃)₃
RhCl(H)(alkyl)(PPh₃)₃ → RhCl(PPh₃)₃ + alkane
```

### Cross-Coupling Reactions
**Suzuki Coupling:**
```
R-X + R'-B(OH)₂ → R-R' + XB(OH)₂
Catalyst: Pd(0)
```

**Heck Reaction:**
```
R-X + alkene → R-alkene + HX
Catalyst: Pd(0)
```

**Sonogashira Coupling:**
```
R-X + R'-C≡CH → R-C≡C-R'
Catalyst: Pd(0)/Cu(I)
```

### Olefin Metathesis
```
R-CH=CH-R + R'-CH=CH-R' → R-CH=CH-R' + R'-CH=CH-R
Catalyst: Grubbs, Schrock catalysts
```

## Organometallic Catalysts

### Important Industrial Catalysts
| Catalyst | Process | Product |
|----------|---------|---------|
| Ziegler-Natta | Polymerization | Polyethylene, polypropylene |
| Wilkinson's | Hydrogenation | Alkanes |
| Wacker | Ethylene oxidation | Acetaldehyde |
| Monsanto | Methanol carbonylation | Acetic acid |
| Rh/PPh₃ | Hydroformylation | Aldehydes |

### Metallocene Catalysts
- Single-site polymerization catalysts
- Control of polymer microstructure
- Example: rac-Et(Ind)₂ZrCl₂ for isotactic polypropylene

## Decision Flow
1. Identify metal and oxidation state
2. Count valence electrons
3. Check 18-electron rule compliance
4. Identify ligand types and hapticity
5. Predict reaction pathways based on electron count
6. Consider catalytic cycles for applications

## Implementations and Data
- Organometallic tools: [L3 code](../L3_functions/transition_metals_tools.py)
- Reference tables: [L4 reference](../L4_reference/reference/electrochemical-analysis-data.md)
