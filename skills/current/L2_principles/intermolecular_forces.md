---
id: intermolecular.forces
layer: 2
title: Intermolecular Forces
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - ../L3_functions/intermolecular_forces_tools.py
  - ../L3_functions/intermolecular_forces_tools.py
  - ../L4_reference/reference/intermolecular-forces-reference.md
  - ../L5_examples/intermolecular_forces/
source:
  - LibreTexts Chemistry 2e (partial coverage in Ch11)
  - Averill, Ch11
---

[Source: Averill, Ch11]

## Context

Intermolecular forces are electrostatic interactions between molecules that determine bulk properties such as melting points, boiling points, and solubility. They are distinct from intramolecular forces (covalent/ionic bonds) and are typically 10-100x weaker.

Understanding these forces enables prediction of:
- Physical states at given conditions
- Boiling and melting points
- Solubility and miscibility
- Surface tension and viscosity

## Core Concepts

### 1. Types of Intermolecular Forces

#### Dipole-Dipole Interactions
- Occur between molecules with permanent dipole moments
- Molecules align with positive end near negative end of neighbors
- Energy proportional to 1/r⁶ (vs 1/r for ion-ion)
- Strength increases with dipole moment magnitude

#### London Dispersion Forces
- Present in ALL molecules (polar and nonpolar)
- Arise from temporary fluctuations in electron distribution
- Create instantaneous and induced dipoles
- Energy proportional to 1/r⁶
- Strength increases with:
  - Molecular mass/size
  - Surface area (linear > branched)
  - Polarizability

#### Hydrogen Bonds
- Special case of dipole-dipole interaction
- Requires H bonded to N, O, or F
- Unusually strong due to:
  - High electronegativity difference
  - Small size of H allowing close approach
- Typical energy: 15-25 kJ/mol
- Donor: H attached to N, O, F
- Acceptor: Lone pair on N, O, F

### 2. Force Strength Hierarchy

```
Ion-ion > Ion-dipole > H-bond > Dipole-dipole > London dispersion
(400+ kJ)  (40-600)    (15-25)  (5-20)          (0.1-40)
```

### 3. Predicting Relative Boiling Points

For molecules of similar mass:
1. Check for hydrogen bonding capability
2. Compare dipole moments
3. Compare surface areas (for London forces)

### 4. Key Quantitative Relationships

**Dipole-dipole energy:**
```
E ∝ -μ₁μ₂/r⁶
```

**London dispersion energy:**
```
E ∝ -α₁α₂/r⁶  (α = polarizability)
```

**Polarizability trend:**
```
Larger atoms > Smaller atoms
More electrons > Fewer electrons
Diffuse electron cloud > Tight electron cloud
```

## Decision Flow

1. **Identify molecular structure**
   - Polar or nonpolar?
   - H bonded to N, O, or F?
   - Size and shape?

2. **Determine dominant force**
   - H-bond donor AND acceptor → H-bonding
   - Polar, no H-bond → Dipole-dipole
   - Nonpolar → London dispersion

3. **Compare with other substances**
   - Same force type → Compare strength factors
   - Different forces → Use hierarchy

4. **Predict properties**
   - Stronger forces → Higher mp/bp, higher viscosity
   - Weaker forces → Lower mp/bp, lower viscosity

## Edge Cases

- **Small polar molecules** (e.g., CH₃F): Dipole-dipole may dominate over London
- **Large nonpolar molecules** (e.g., C₆₀): London forces can be very strong
- **Molecules with multiple H-bond sites** (e.g., glycerol): Very high bp, viscosity
- **Amphiphilic molecules**: Different parts have different dominant forces

## Implementations and Data

- Tool implementation: [L3 code](../L3_functions/intermolecular_forces_tools.py)
- Solver wrapper: [L3 skill](../L3_functions/intermolecular_forces_tools.py)
- Reference tables: [L4 force comparisons](../L4_reference/reference/intermolecular-forces-reference.md)
- Worked examples: [L5 examples](../L5_examples/intermolecular_forces/)

## Related Topics

- [liquid_properties.md](liquid_properties.md) - How IMFs affect bulk liquid behavior
- [phase_diagrams.md](phase_diagrams.md) - Phase boundaries determined by IMFs
- [solubility.md](solubility.md) - "Like dissolves like" principle
- [covalent_bonding.md](covalent_bonding.md) - Intramolecular vs intermolecular distinction

## L3 Tool Call Directives

**Source:** `intermolecular_forces_tools.py`

Intermolecular force classification, boiling point prediction, H-bond detection, and energy ranges.

### Available functions:
- `classify_imf(molecule_type, has_h_bond_donor=False, has_h_bond_acceptor=False)` → str — Returns 'hydrogen_bonding', 'dipole_dipole', or 'london_dispersion'
- `imf_strength_rank(force_type)` → int — Returns 1-5 (1=weakest, 5=ion-ion)
- `predict_boiling_point_order(substances)` → List[str] — Sorts substances by IMF + molecular mass
- `h_bond_capable(elements)` → Tuple[bool, bool] — Returns (can_donate, can_accept)
- `estimate_london_strength(molecular_mass, surface_area_factor=1.0)` → float — Relative strength estimate
- `imf_energy_range(force_type)` → Tuple[float, float] — Returns (min, max) in kJ/mol
- `polarizability_trend(elements)` → str — Qualitative description

### Common errors:
- ❌ Forgetting both H-bond donor AND acceptor are needed for H-bonding
- ❌ Not accounting for surface area (linear > branched for London forces)
- ❌ Confusing IMF type (all molecules have London, but polar adds dipole-dipole)
