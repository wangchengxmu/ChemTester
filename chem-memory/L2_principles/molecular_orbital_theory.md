---
id: molecular.orbital.theory
layer: 2
title: Molecular Orbital Theory
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - ../L3_functions/molecular_orbital_tools.py
  - ../L4_reference/reference/crystal-structures-reference.md
cross_links:
  - ./covalent_bonding.md
  - ./lewis_structures.md
  - ./symmetry_group_theory.md
source: Inorganic Chemistry (LibreTexts), Ch05
---

## Context
Molecular orbital (MO) theory describes bonding in terms of molecular orbitals formed from the combination of atomic orbitals. Unlike valence bond theory, MO theory provides a more complete picture of electron distribution, bond order, and magnetic properties.

## Fundamental Principles

### Linear Combination of Atomic Orbitals (LCAO)
```
¦·_MO = c?¦Õ? + c?¦Õ? + ... + c?¦Õ?

Where:
¦·_MO = molecular orbital
¦Õ? = atomic orbitals
c? = coefficients (contribution weights)
```

### Requirements for Orbital Combination
1. **Similar energy**: Orbitals must be close in energy
2. **Symmetry match**: Must have the same symmetry with respect to the bond axis
3. **Spatial overlap**: Must have significant spatial overlap

## Types of Molecular Orbitals

### Bonding vs Antibonding
| Type | Energy | Electron Density | Effect |
|------|--------|------------------|--------|
| Bonding (¦Ò, ¦Ð) | Lower than AOs | Between nuclei | Stabilizing |
| Antibonding (¦Ò*, ¦Ð*) | Higher than AOs | Nodes between nuclei | Destabilizing |
| Nonbonding | Same as AO | Localized | No effect |

### Orbital Classification by Symmetry
| Type | Formation | Symmetry |
|------|-----------|----------|
| ¦Ò (sigma) | Head-on overlap | Symmetric about bond axis |
| ¦Ð (pi) | Side-on overlap | Nodal plane containing bond axis |
| ¦Ä (delta) | d-d overlap | Two nodal planes |

## Diatomic Molecules

### Homonuclear Diatomics (H? to Ne?)

**Orbital Energy Order (O? and lighter):**
```
¦Ò1s < ¦Ò*1s < ¦Ò2s < ¦Ò*2s < ¦Ð2p = ¦Ð2p < ¦Ò2p < ¦Ð*2p = ¦Ð*2p < ¦Ò*2p
```

**Orbital Energy Order (F? and heavier):**
```
¦Ò1s < ¦Ò*1s < ¦Ò2s < ¦Ò*2s < ¦Ò2p < ¦Ð2p = ¦Ð2p < ¦Ð*2p = ¦Ð*2p < ¦Ò*2p
```

### Bond Order Calculation
```
Bond order = (n_bonding - n_antibonding) / 2
```

### Properties of Diatomics
| Molecule | Configuration | Bond Order | Paramagnetic? |
|----------|---------------|------------|---------------|
| H? | ¦Ò1s2 | 1 | No |
| He? | ¦Ò1s2¦Ò*1s2 | 0 | No |
| Li? | ...¦Ò2s2 | 1 | No |
| Be? | ...¦Ò*2s2 | 0 | No |
| B? | ...¦Ð2p2 | 1 | Yes (2 unpaired) |
| C? | ...¦Ð2p? | 2 | No |
| N? | ...¦Ò2p2 | 3 | No |
| O? | ...¦Ð*2p2 | 2 | Yes (2 unpaired) |
| F? | ...¦Ð*2p? | 1 | No |
| Ne? | ...¦Ò*2p2 | 0 | No |

### Heteronuclear Diatomics
- Electronegativity difference affects orbital energies
- More electronegative atom contributes more to bonding MO
- Less electronegative atom contributes more to antibonding MO

## Polyatomic Molecules

### MO Diagram Construction
1. Determine point group
2. Generate SALCs for ligand orbitals
3. Determine symmetry of central atom orbitals
4. Match by symmetry and energy
5. Form bonding, nonbonding, and antibonding combinations

### Walsh Diagrams
- Show how MO energies change with molecular geometry
- Predict equilibrium geometry based on electron count
- Example: AH? molecules

## Frontier Molecular Orbitals

### HOMO and LUMO
- **HOMO**: Highest Occupied Molecular Orbital
- **LUMO**: Lowest Unoccupied Molecular Orbital
- Frontier orbitals determine reactivity

### FMO Theory Applications
- Electrophiles attack HOMO
- Nucleophiles attack LUMO
- Photochemistry involves HOMO-LUMO transitions

## Molecular Orbital Diagrams

### Drawing MO Diagrams
1. List atomic orbitals on both sides
2. Identify symmetry labels
3. Draw MOs in energy order
4. Fill electrons following Aufbau, Pauli, Hund
5. Calculate bond order

### Example: O?
```
          O atom    O? molecule    O atom
          
          2p ©¤©¤©¤©¤   ¦Ò*2p ©¤©¤©¤©¤©¤©¤    ©¤©¤©¤©¤ 2p
                    ¦Ð*2p ©¤©¤©Ð©¤©¤
                          ©¦    ¡û 2 unpaired e?
                    ¦Ð2p ©¤©¤©Ø©¤©¤    ©¤©¤©¤©¤ 2p
                    ¦Ò2p ©¤©¤©¤©¤©¤©¤
          2s ©¤©¤©¤©¤   ¦Ò*2s ©¤©¤©¤©¤©¤©¤    ©¤©¤©¤©¤ 2s
                    ¦Ò2s ©¤©¤©¤©¤©¤©¤
```

## Photoelectron Spectroscopy (PES)

### Principles
- Photons ionize molecules
- Measure kinetic energy of ejected electrons
- Ionization energy (IE) = h¦Í - KE

### Information from PES
- Orbital energies
- Bonding character (width of peak)
- Electronic structure verification

## Band Theory (Extended MO Theory)

### From Molecules to Solids
- Many atoms ¡ú many closely spaced MOs
- Continuous bands of energy levels
- Band structure determines properties

### Band Types
| Band | Occupancy | Property |
|------|-----------|----------|
| Valence band | Filled | Highest occupied |
| Conduction band | Empty | Lowest unoccupied |
| Band gap | - | Energy between bands |

### Classification by Band Gap
| Material | Band Gap | Conductivity |
|----------|----------|--------------|
| Conductor | None or overlapping | High |
| Semiconductor | Small (0.5-3 eV) | Moderate, temperature dependent |
| Insulator | Large (>3 eV) | Very low |

## Decision Flow
1. Identify atoms and their valence orbitals
2. Determine molecular geometry and symmetry
3. Generate SALCs for ligand orbitals
4. Match central atom orbitals by symmetry
5. Construct MO diagram
6. Fill electrons, calculate bond order
7. Predict magnetic and spectroscopic properties

## Implementations and Data
- Implementation: `../L3_functions/diatomic_mo_tools.py`
- MO calculation tools: [L3 code](../L3_functions/molecular_orbital_tools.py)
- Reference tables: [L4 reference](../L4_reference/reference/crystal-structures-reference.md)

## L3 Tool Call Directives

**Source:** `molecular_orbital_tools.py`
MO bond order, diatomic diagrams, HOMO-LUMO gaps, Walsh diagrams, ligand field splitting.

### Available functions:
- `bond_order(nelectrons, nbonding, nantibonding)` → float — BO = (Nb - Na) / 2
- `diatomic_mo_diagram(atom1, atom2, valence_electrons, period=2)` → dict — Full MO config, BO, paramagnetism, unpaired e⁻
- `homo_lumo_gap(homo_energy, lumo_energy, unit='eV')` → float — Gap in specified units
- `walsh_diagram_molecule(bond_angle, molecule_type='AH2')` → dict — Walsh diagram geometry prediction
- `orbital_symmetry_match(orbital1, orbital2)` → bool — True if orbitals share symmetry
- `ligand_field_splitting(geometry, ligand_field='intermediate')` → dict — d-orbital pattern for oct/tet/sq-planar

### Common errors:
- ❌ Wrong MO ordering: period 2 B2–N2 use π < σ₂p; O2/F2 use σ₂p < π
- ❌ Forgetting heteronuclear orbital energy shifts based on electronegativity
- ❌ Confusing bonding/antibonding electron counts — check nbonding+nantibonding = nelectrons
