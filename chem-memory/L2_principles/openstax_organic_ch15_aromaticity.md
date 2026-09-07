---
id: organic.openstax_ch15
layer: 2
title: Benzene and Aromaticity
up_links:
  - ../L1_ontology/organic_chemistry.md
---

# Benzene and Aromaticity

## Key Principles

### Hückel's Rule (4n + 2 Rule)
A molecule is **aromatic** if and only if it meets ALL criteria:
1. **Cyclic** - must form a ring
2. **Planar** - all atoms must lie in same plane (allows p-orbital overlap)
3. **Fully conjugated** - p orbital on every ring atom (continuous overlap)
4. **4n + 2 π electrons** - where n = 0, 1, 2, 3... (2, 6, 10, 14, 18 electrons)

**Aromatic electron counts**: 2, 6, 10, 14, 18, 22...
**Antiaromatic electron counts** (planar, cyclic, conjugated with 4n π electrons): 4, 8, 12, 16...

### Stability Evidence
- Benzene's heat of hydrogenation: -206 kJ/mol
- Expected for "cyclohexatriene": -354 kJ/mol (3 × -118 kJ/mol)
- **Resonance stabilization energy**: ~148 kJ/mol (35.4 kcal/mol)
- All C-C bonds: 139 pm (intermediate between single 154 pm and double 134 pm)

### Classification Decision Tree
```
Is the molecule cyclic?
    → NO: Nonaromatic
    → YES: Is every atom sp² hybridized (p orbital available)?
        → NO: Nonaromatic
        → YES: Is it planar?
            → NO: Nonaromatic (e.g., cyclodecapentaene - steric hindrance)
            → YES: Count π electrons
                → 4n + 2: AROMATIC ✓
                → 4n: ANTIAROMATIC (destabilized)
```

### Aromatic Ions
**Aromatic ions can form when**: Ionization creates the 4n + 2 electron count

| Species | π Electrons | Status | Notes |
|---------|-------------|--------|-------|
| Cyclopentadienyl cation | 4 | Antiaromatic | Very unstable |
| Cyclopentadienyl radical | 5 | Nonaromatic | Unstable |
| Cyclopentadienyl anion | 6 | **Aromatic** | pKa = 16, easily formed |
| Cycloheptatrienyl cation | 6 | **Aromatic** | Extraordinarily stable |
| Cycloheptatrienyl radical | 7 | Nonaromatic | Unstable |
| Cycloheptatrienyl anion | 8 | Antiaromatic | Unstable |
| Cyclooctatetraene | 8 | Nonaromatic | Tub-shaped (not planar) |
| Cyclooctatetraene dianion | 10 | **Aromatic** | Flat, stable |

### Heterocyclic Aromaticity
**Nitrogen in aromatic rings** - two roles:
- **Pyridine-type**: N in double bond, contributes 1 electron to π system, lone pair in sp² orbital (not in ring plane) → basic
- **Pyrrole-type**: N not in double bond, contributes 2 electrons (lone pair in p orbital), lone pair is part of π system → NOT basic

| Compound | Ring Size | N Type | π Electrons | Notes |
|----------|-----------|--------|-------------|-------|
| Pyridine | 6 | Pyridine-type | 6 | Lone pair not in π system, basic (pKa ≈ 5.2) |
| Pyrimidine | 6 | 2× Pyridine-type | 6 | Found in DNA/RNA bases |
| Pyrrole | 5 | Pyrrole-type | 6 | Lone pair in π system, NOT basic |
| Imidazole | 5 | Both types | 6 | One of each N type |
| Furan | 5 | O contributes 2 electrons | 6 | Oxygen analog of pyrrole |
| Thiophene | 5 | S contributes 2 electrons | 6 | Sulfur analog of pyrrole |

## Mechanisms

### Electrophilic Aromatic Substitution (EAS) - Overview
Aromatic compounds undergo **substitution** (not addition) to preserve aromaticity:
1. Electrophile attacks aromatic ring → arenium ion (σ complex)
2. Loss of proton regenerates aromaticity

**Key EAS reactions**:
- Halogenation (Cl₂, Br₂ with Lewis acid)
- Nitration (HNO₃/H₂SO₄)
- Sulfonation (H₂SO₄)
- Friedel-Crafts alkylation (RCl/AlCl₃)
- Friedel-Crafts acylation (RCOCl/AlCl₃)

### MO Picture of Aromaticity
- Single lowest-energy MO (contains 2 electrons)
- Pairs of degenerate MOs above (each pair holds 4 electrons)
- Stable aromatic = all bonding orbitals filled
- Partially filled = radical or ion (less stable unless aromatic ion)

**Benzene MO filling**:
- ψ₁ (lowest): 2 electrons
- ψ₂, ψ₃ (degenerate): 4 electrons
- Total: 6 electrons, all bonding orbitals filled ✓

## Selectivity Rules

### Directing Effects in EAS
**Activating groups (ortho/para directors)**:
- -OH, -OR, -NH₂, -NHR, -NR₂ (strong)
- -R, -Ar (moderate)
- Activating groups donate electron density, stabilize arenium ion

**Deactivating groups (ortho/para directors)**:
- -F, -Cl, -Br, -I (weak deactivation)
- Halogens inductively withdraw but resonance donate

**Deactivating groups (meta directors)**:
- -NO₂, -CN, -COOH, -COR, -SO₃H (strong)
- Meta directors withdraw electron density, destabilize ortho/para arenium ions

### Predicting Major Products
1. Identify all substituents and their directing effects
2. If directors conflict: activating group wins over deactivating
3. Steric hindrance: ortho less favored for bulky groups
4. Multiple products common - separations may be needed

## Common Exam Patterns

### Pattern 1: Hückel Rule Application
**Question**: Is compound X aromatic, antiaromatic, or nonaromatic?
**Approach**: 
1. Check cyclic
2. Check planar (consider steric hindrance)
3. Check continuous conjugation (sp² on all ring atoms)
4. Count π electrons (include lone pairs if in p orbital)

### Pattern 2: Resonance Energy Calculations
**Given**: Heat of hydrogenation data
**Calculate**: Resonance stabilization energy
**Method**: Compare observed ΔH to expected (sum of isolated bonds)

### Pattern 3: Aromatic Ion Formation
**Question**: Why is cyclopentadiene unusually acidic?
**Answer**: Deprotonation gives aromatic cyclopentadienyl anion (6 π electrons)

### Pattern 4: Heterocycle Basicity
**Question**: Why is pyridine basic but pyrrole is not?
**Answer**: 
- Pyridine: lone pair in sp² orbital, not in π system, available for protonation
- Pyrrole: lone pair in p orbital, part of aromatic sextet, protonation destroys aromaticity

### Pattern 5: Frost Circle / MO Diagram
**Task**: Draw MO energy levels for cyclic conjugated system
**Method**: 
- Regular polygon inscribed in circle, vertices at energy levels
- Center of circle = nonbonding level
- Fill with electrons to determine stability

### Pattern 6: Antiaromatic vs Nonaromatic
**Key distinction**: 
- Antiaromatic: Planar, cyclic, conjugated, 4n electrons (destabilized)
- Nonaromatic: Not planar OR not fully conjugated (normal stability)

**Example**: Cyclooctatetraene (COT)
- 8 π electrons (would be antiaromatic if planar)
- Adopts tub conformation → nonplanar → nonaromatic
- COT²⁻ (10 electrons) is planar and aromatic
