---
id: solid.state.chemistry
layer: 2
title: Solid State Chemistry
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - ../L3_functions/solid_state_chemistry_tools.py
  - ../L3_functions/solid_state_chemistry_tools.py
  - ../L4_reference/reference/solid-state-reference.md
  - ../L5_examples/solid_state/
source:
  - Averill, Ch12
---

[Source: Averill, Ch12]

## Context

Solids are distinguished from gases and liquids by a rigid structure in which component atoms, ions, or molecules are usually locked into place. Understanding solid-state chemistry enables prediction and design of materials with specific properties (hardness, conductivity, melting point).

## Core Concepts

### 1. Classification of Solids

Based on the nature of forces holding components together:

| Type | Components | Bonding | Examples |
|------|-----------|---------|----------|
| Ionic | Cations + Anions | Electrostatic | NaCl, CaO |
| Molecular | Molecules | IMF (H-bond, dipole, London) | Ice, I₂, sugar |
| Covalent (Network) | Atoms | Covalent bonds throughout | Diamond, Si, SiO₂ |
| Metallic | Metal atoms | Metallic (delocalized e⁻) | Fe, Cu, Al |

### 2. Ionic Solids

**Structure:**
- Alternating cations and anions in extended lattice
- Each ion surrounded by ions of opposite charge
- High coordination numbers (typically 6 or 8)

**Properties:**
- High melting points (strong electrostatic forces)
- Hard but brittle (like charges align under stress → repulsion)
- Poor conductors as solids (ions locked in place)
- Good conductors when molten or dissolved
- Often soluble in polar solvents

**Lattice Energy:**
```
U ∝ (z⁺ × z⁻) / (r⁺ + r⁻)
```
Higher charge, smaller ions → stronger bonding → higher mp

### 3. Molecular Solids

**Structure:**
- Individual molecules held by intermolecular forces
- Molecules retain their identity
- Various packing arrangements depending on shape

**Properties:**
- Low melting points (weak IMFs)
- Soft, easily deformed
- Poor thermal and electrical conductors
- Often volatile (can sublimate)

**Trends:**
- Higher MW → stronger London forces → higher mp
- Symmetrical molecules pack better → higher mp
- H-bonding capability → significantly higher mp

### 4. Covalent (Network) Solids

**Structure:**
- Atoms connected by covalent bonds throughout
- Giant molecules (single crystal = one molecule)
- No individual molecules

**Properties:**
- Very high melting points (strong covalent bonds)
- Extremely hard (diamond is hardest known)
- Poor electrical conductors (except graphite)
- Chemically inert

**Examples:**
| Solid | Structure | Properties |
|-------|-----------|------------|
| Diamond | sp³ C, 3D tetrahedral | Hardest, insulator |
| Graphite | sp² C, layered | Soft lubricant, conductor |
| Silicon | Diamond structure | Semiconductor |
| SiO₂ (quartz) | Si-O network | Hard, insulator |
| SiC | Alternating Si, C | Very hard, abrasive |

### 5. Metallic Solids

**Structure:**
- Metal atoms in close-packed arrangements
- High packing efficiency (68-74%)
- Valence electrons delocalized throughout

**Properties:**
- High electrical conductivity (mobile electrons)
- High thermal conductivity (electron transport)
- Malleable and ductile (atoms slide without breaking bonds)
- Lustrous (reflect light)
- Variable melting points (depends on valence electron count)

**Electron Sea Model:**
- Positive metal ions in lattice
- Mobile valence electrons throughout
- No directionality to bonding

### 6. Strength Comparison

```
Covalent solids > Ionic solids ≈ Metallic solids > Molecular solids
(in terms of bond strength and melting points)
```

**Note:** Individual bond strengths may differ from bulk properties.

## Decision Flow

### Classifying a Solid

1. **Identify components**
   - Elements → Metallic or covalent
   - Ionic compound → Ionic
   - Discrete molecules → Molecular

2. **For elemental solids:**
   - Metals → Metallic (check periodic table position)
   - C, Si, Ge → Covalent network (check bonding)

3. **For compounds:**
   - Metal + Nonmetal → Likely ionic
   - Nonmetal + Nonmetal → Covalent or molecular

4. **Confirm with properties:**
   - High mp, hard, brittle → Ionic
   - Low mp, soft → Molecular
   - Very high mp, very hard → Covalent
   - Conducts, malleable → Metallic

### Predicting Melting Point Order

1. Classify each solid
2. Apply hierarchy: Covalent > Ionic ≈ Metallic > Molecular
3. Within same class:
   - Ionic: Higher charge, smaller ions → Higher mp
   - Molecular: Higher MW, H-bonding → Higher mp
   - Metallic: Check valence electron count

## Edge Cases

- **Graphite:** Covalent solid with metallic conductivity (delocalized π electrons)
- **Amorphous solids:** No long-range order (glass, plastics)
- **Semiconductors:** Covalent with small band gap (Si, Ge)
- **Intermetallic compounds:** Fixed stoichiometry, distinct from alloys

## Implementations and Data

- Tool implementation: [L3 code](../L3_functions/solid_state_chemistry_tools.py)
- Solver wrapper: [L3 skill](../L3_functions/solid_state_chemistry_tools.py)
- Reference tables: [L4 solid properties](../L4_reference/reference/solid-state-reference.md)
- Worked examples: [L5 examples](../L5_examples/solid_state/)

## Related Topics

- [crystal_structures.md](crystal_structures.md) - Unit cells and packing
- [band_theory.md](band_theory.md) - Electronic structure of solids
- [intermolecular_forces.md](intermolecular_forces.md) - Molecular solid bonding
- [ionic_bonding.md](ionic_bonding.md) - Ionic solid fundamentals

## L3 Tool Call Directives

**Source:** `solid_state_chemistry_tools.py`
Solid state chemistry: crystal classification, conductivity, band gaps, unit cell properties.

### Available functions:
- `classify_solid(bonding_type)` → dict — Classify solid by bonding (ionic/covalent/metallic/molecular)
- `predict_conductivity(material_type, temperature)` → str — Predict if conductor increases/decreases with T
- `band_gap_classification(band_gap_ev)` → str — Classify as conductor/semiconductor/insulator from band gap
- `unit_cell_atoms(cell_type)` → int — Number of atoms per unit cell
- `coordination_number(cell_type)` → int — Coordination number for crystal structure
- `packing_efficiency(cell_type)` → float — Packing efficiency percentage
- `density_from_cell(cell_type, atomic_mass, edge_length, z)` → float — Calculate crystal density from unit cell

### Common errors:
- ❌ Confusing metals (conductivity decreases with T) with semiconductors (increases with T)
- ❌ Using wrong z value for density calculation (SC=1, BCC=2, FCC=4)
