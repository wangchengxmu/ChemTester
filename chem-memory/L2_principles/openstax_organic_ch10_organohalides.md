---
id: organic.openstax_ch10
layer: 2
title: Organohalides
up_links:
  - ../L1_ontology/organic_chemistry.md
---

# Organohalides

## Key Principles

### Classification of Alkyl Halides
By **carbon substitution**:
- **Primary (1°)**: One alkyl group on C-X carbon (RCH₂X)
- **Secondary (2°)**: Two alkyl groups (R₂CHX)
- **Tertiary (3°)**: Three alkyl groups (R₃CX)

By **position relative to π bonds**:
- **Alkyl halide**: No nearby π bonds
- **Allylic**: Next to C=C (CH₂=CH-CH₂-X)
- **Benzylic**: Next to aromatic ring (Ph-CH₂-X)
- **Vinyl**: Directly on C=C (CH₂=CH-X)
- **Aryl**: Directly on aromatic ring (Ph-X)

### Bond Properties
| C-X Bond | Length (pm) | Strength (kJ/mol) | Dipole (D) |
|----------|-------------|-------------------|------------|
| C-F | 139 | 460 | 1.85 |
| C-Cl | 178 | 350 | 1.87 |
| C-Br | 193 | 294 | 1.81 |
| C-I | 214 | 239 | 1.62 |

**Key trends**:
- Bond length increases down group
- Bond strength decreases down group
- C-I is weakest (most reactive in SN1/SN2)
- All C-X bonds are polar (Cδ+-Xδ-)

### Reactivity Patterns
| Type | SN1 | SN2 | E1 | E2 | Notes |
|------|-----|-----|----|----|-------|
| 1° alkyl | No | Yes | No | With strong base | Favors SN2 |
| 2° alkyl | Slow | Slow | Slow | Yes | Depends on conditions |
| 3° alkyl | Yes | No | Yes | Yes | No SN2 (steric) |
| Allylic | Yes | Yes | Yes | Yes | Resonance stabilization |
| Benzylic | Yes | Yes | Yes | Yes | Resonance stabilization |
| Vinyl | No | No | No | No | C-X too strong |
| Aryl | No | No | No | No | C-X too strong |

### Stability of Intermediates
**Carbocation stability**:
```
3° allylic ≈ 3° benzylic > 2° allylic ≈ 2° benzylic > 3° > 2° > 1° > vinyl ≈ aryl
```

**Radical stability**:
```
3° > 2° > 1° > vinyl
Allylic and benzylic radicals are ~40 kJ/mol more stable than corresponding alkyl radicals
```

### Bond Dissociation Energies (C-H)
| C-H Type | BDE (kJ/mol) | Radical Formed |
|----------|--------------|----------------|
| Allylic | ~370 | Allylic radical (stable) |
| Tertiary | ~400 | 3° radical |
| Secondary | ~410 | 2° radical |
| Primary | ~421 | 1° radical |
| Vinylic | ~465 | Vinylic radical (unstable) |

## Mechanisms

### 1. Radical Halogenation of Alkanes
```
Initiation: X₂ → 2 X· (hν or heat)
Propagation: 
  X· + R-H → HX + R·
  R· + X₂ → R-X + X·
Termination: 
  2 X· → X₂
  2 R· → R-R
  R· + X· → R-X
```

**Selectivity in chlorination**:
- 1° H : 2° H : 3° H = 1 : 3.5 : 5
- Low selectivity, mixtures result

**Selectivity in bromination**:
- 1° H : 2° H : 3° H = 1 : 82 : 1600
- High selectivity for tertiary positions

### 2. Allylic Bromination (NBS)
```
Initiation: NBS → Br· (trace HBr present)
Propagation:
  Br· + R-CH₂-CH=CH₂ → R-CH-CH=CH₂ + HBr
  HBr + NBS → Br₂ + succinimide
  R-CH-CH=CH₂ + Br₂ → R-CHBr-CH=CH₂ + Br·
```

**Why NBS?**
- Maintains low, constant [Br₂]
- Prevents addition to double bond
- Selective for allylic position

**Allylic radical resonance**:
```
R-CH-CH=CH₂ ↔ R-CH=CH-CH₂
```
- Two positions can be brominated
- Less hindered position often favored

### 3. SN1 Mechanism
```
Step 1 (slow): R-X → R⁺ + X⁻ (carbocation formation)
Step 2 (fast): R⁺ + Nu⁻ → R-Nu
```
- Rate = k[RX] (first order)
- Carbocation intermediate → rearrangements possible
- Racemization at chiral centers
- Favored by: 3° > 2°, polar solvents, good leaving groups

### 4. SN2 Mechanism
```
Nu⁻ + R-X → [Nu---R---X]‡ → Nu-R + X⁻
```
- Rate = k[RX][Nu⁻] (second order)
- Concerted, one step
- **Inversion of configuration** (Walden inversion)
- Backside attack required
- Favored by: 1° > 2°, strong nucleophile, polar aprotic solvent

### 5. E1 Mechanism
```
Step 1: R-X → R⁺ + X⁻
Step 2: Base removes H⁺ → Alkene
```
- Carbocation intermediate
- Zaitsev product (more substituted alkene)
- Competes with SN1

### 6. E2 Mechanism
```
Base + R-CH₂-CH₂-X → Alkene + H-Base⁺ + X⁻
```
- Concerted, one step
- Anti-periplanar geometry required
- Zaitsev product with weak base
- Hofmann product with bulky base

## Selectivity Rules

### SN1 vs SN2 Decision Tree
```
What is the alkyl halide?
  
  3°: SN1 (no SN2)
  2°: Check conditions
    - Strong Nu, aprotic solvent → SN2
    - Weak Nu, protic solvent → SN1
  1°: SN2 (no SN1)
  
Special cases:
  Allylic/benzylic: Both SN1 and SN2 possible
  Vinyl/aryl: Neither (C-X bond too strong)
```

### Radical Halogenation Selectivity
```
Chlorination: Low selectivity
  - Multiple products common
  - Statistical factor matters (count equivalent H atoms)
  
Bromination: High selectivity
  - Tertiary position strongly favored
  - Position next to double bond (allylic) highly favored
```

### Predicting Allylic Bromination Products
1. Identify allylic positions
2. Draw resonance forms of allylic radical
3. Products form at both resonance positions
4. Less hindered position often dominates

## Common Exam Patterns

### Pattern 1: Radical Halogenation Product Distribution
**Question**: Predict products and relative amounts from alkane chlorination

**Method**:
1. Count each type of H (1°, 2°, 3°)
2. Apply reactivity ratios (1 : 3.5 : 5)
3. Calculate: (% product) = (number of H) × (reactivity)

**Example**: 2-methylbutane + Cl₂, hν
- 9 primary H: 9 × 1 = 9 relative units
- 4 secondary H: 4 × 3.5 = 14 relative units  
- 1 tertiary H: 1 × 5 = 5 relative units
- Total: 28 units

### Pattern 2: Allylic Bromination with NBS
**Question**: Predict products from alkene + NBS

**Key points**:
- Reaction at allylic position only
- Resonance delocalization → multiple products
- Addition to double bond does NOT occur

**Example**: 1-octene + NBS
- Products: 3-bromo-1-octene AND 1-bromo-2-octene
- Both from allylic radical resonance

### Pattern 3: Vinyl/Aryl Halide Inertness
**Question**: Why doesn't vinyl or aryl halide undergo SN1/SN2?

**Answer**:
- C-X bond is shorter and stronger (sp² carbon)
- For SN2: backside attack blocked by π system
- For SN1: vinylic/aryl cations extremely unstable
- Electron density in π bond stabilizes C-X bond

### Pattern 4: Stability Ranking
**Task**: Rank carbocations or radicals by stability

**Rules**:
- More substitution = more stable
- Resonance (allylic, benzylic) = extra stability
- Order: 3° benzylic ≈ 3° allylic > 3° > 2° > 1° > vinyl/aryl

### Pattern 5: Radical Mechanism Steps
**Question**: Show initiation, propagation, termination steps

**Key requirements**:
- Initiation creates radicals
- Propagation consumes and creates radicals (chain)
- Termination destroys radicals (combination)

### Pattern 6: Resonance in Allylic/Benzylic Systems
**Task**: Draw resonance structures for allylic/benzylic radicals or cations

**Allylic radical**: Two equivalent positions
```
CH₂=CH-CH₂· ↔ ·CH₂-CH=CH₂
```

**Benzylic radical**: Multiple resonance forms
```
Ph-CH₂· ↔ ·CH₂-Ph (charge delocalized to ring positions)
```

### Pattern 7: Leaving Group Ability
**Question**: Rank halide leaving group ability

**Answer**: I⁻ > Br⁻ > Cl⁻ > F⁻
- Based on bond strength (weaker = better)
- Based on anion stability (larger = more stable)

### Pattern 8: C-X Bond Strength Implications
**Question**: Why is C-I bond most reactive?

**Answer**:
- Longest, weakest bond
- Lowest BDE (239 kJ/mol)
- I⁻ is best leaving group (large, stable anion)
- However, C-F is most polar (highest dipole)
