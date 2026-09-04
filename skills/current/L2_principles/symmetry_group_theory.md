---
id: symmetry.group.theory
layer: 2
title: Symmetry and Group Theory in Chemistry
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - ../L3_functions/group_theory_tools.py
  - ../L4_reference/reference/crystallography-data.md
cross_links:
  - ./molecular_geometry_vsepr.md
  - ./molecular_orbital_theory.md
source: Inorganic Chemistry (LibreTexts), Ch04
---

## Context
Symmetry and group theory provide a powerful mathematical framework for understanding molecular structure, predicting properties, and analyzing spectroscopic data. Point groups classify molecules by their symmetry elements, and character tables encode the transformation properties of orbitals and vibrations.

## Symmetry Elements and Operations

### Types of Symmetry Elements
| Element | Symbol | Operation |
|---------|--------|-----------|
| Identity | E | Leave molecule unchanged |
| Proper rotation | Cₙ | Rotate by 360°/n |
| Reflection (horizontal) | σₕ | Reflect through horizontal plane |
| Reflection (vertical) | σᵥ | Reflect through vertical plane |
| Reflection (dihedral) | σₐ | Reflect through diagonal plane |
| Improper rotation | Sₙ | Cₙ rotation + σₕ reflection |
| Inversion center | i | Invert through center |

### Symmetry Operations
Each symmetry element generates one or more symmetry operations:
- Cₙ generates n operations: Cₙ, Cₙ², Cₙ³, ..., Cₙⁿ = E
- Sₙ generates n operations for even n, 2n for odd n

## Point Groups

### Classification Flow
```
Is molecule linear?
  Yes → Has center of inversion?
    Yes → D∞h
    No → C∞v
  No → Has multiple high-order Cₙ axes?
    Yes → Cubic groups (T, O, I)
    No → Has Cₙ axis?
      Yes → Has n C₂ axes perpendicular to Cₙ?
        Yes → Has σₕ?
          Yes → Dₙh
          No → Has n σₐ?
            Yes → Dₙd
            No → Dₙ
        No → Has σₕ?
          Yes → Cₙh
          No → Has n σᵥ?
            Yes → Cₙv
            No → Has S₂ₙ?
              Yes → S₂ₙ
              No → Cₙ
      No → Has σ?
        Yes → Cₛ
        No → Has i?
          Yes → Cᵢ
          No → C₁
```

### Common Point Groups
| Point Group | Example | Key Elements |
|-------------|---------|--------------|
| C₁ | CHClBrF | E only |
| Cₛ | H₂O (bent) | E, σ |
| C₂ᵥ | H₂O | E, C₂, 2σᵥ |
| C₃ᵥ | NH₃ | E, 2C₃, 3σᵥ |
| C∞ᵥ | HCl | E, C∞, ∞σᵥ |
| D₂h | C₂H₄ | E, 3C₂, 3σ, i |
| D₃h | BF₃ | E, 2C₃, 3C₂, σₕ, 3σᵥ |
| D₄h | XeF₄ | E, 2C₄, C₂, 2C₂', 2C₂", σₕ, i, 2S₄, 2σᵥ, 2σₐ |
| D∞h | CO₂ | E, C∞, ∞C₂, σₕ, i, ∞σᵥ |
| Td | CH₄ | E, 8C₃, 3C₂, 6S₄, 6σₐ |
| Oh | SF₆ | E, 8C₃, 6C₂, 6C₄, 3C₂', i, 6S₄, 8S₆, 3σₕ, 6σₐ |
| Ih | C₆₀ | E, 12C₅, 12C₅², 20C₃, 15C₂, i, 12S₁₀, 12S₁₀³, 20S₆, 15σ |

## Character Tables

### Structure of a Character Table
```
C₂ᵥ  |  E  |  C₂  |  σᵥ(xz) |  σᵥ'(yz) |      | z, x², y², z²
-----|-----|------|---------|----------|------|------------------
A₁   |  1  |   1  |    1    |     1    |      | x², y², z²
A₂   |  1  |   1  |   -1    |    -1    | Rz   | xy
B₁   |  1  |  -1  |    1    |    -1    | x, Ry| xz
B₂   |  1  |  -1  |   -1    |     1    | y, Rx| yz
```

### Reading Character Tables
- **Mulliken symbols**: A, B (singly degenerate), E (doubly), T (triply)
- **Subscripts**: g/u (gerade/ungerade for i), ' / " (for σₕ)
- **Characters**: +1 (symmetric), -1 (antisymmetric) under each operation
- **Functions**: x, y, z (translations), Rx, Ry, Rz (rotations), quadratic functions

## Applications of Group Theory

### 1. Determining Polarity
- Polar molecules must have: Cₙ axis (n ≥ 1) and σᵥ planes
- Point groups with permanent dipole: Cₙ, Cₙv, Cₛ
- Non-polar: D groups, T groups, O groups

### 2. Determining Chirality
- Chiral molecules lack: improper rotation axes (Sₙ, σ, i)
- Chiral point groups: Cₙ, Dₙ
- Achiral if has any Sₙ (including σ = S₁, i = S₂)

### 3. Predicting IR and Raman Activity
- Vibration is IR active if it transforms as x, y, or z
- Vibration is Raman active if it transforms as quadratic functions (x², y², z², xy, xz, yz)
- For centrosymmetric molecules: IR and Raman modes are mutually exclusive

### 4. Orbital Symmetry
- Atomic orbitals transform according to irreducible representations
- Useful for predicting allowed transitions and bonding interactions

## Molecular Vibrations

### Number of Vibrational Modes
- **Linear molecules**: 3N - 5 modes
- **Nonlinear molecules**: 3N - 6 modes
Where N = number of atoms

### Vibration Types
| Type | Description | Activity |
|------|-------------|----------|
| Stretching | Bond length changes | Often IR active |
| Bending | Bond angle changes | Often IR active |
| Symmetric | All bonds change in same way | Often Raman active |
| Asymmetric | Bonds change in opposite ways | Often IR active |

### Reducing Vibrational Representations
1. Determine Γ_total (total representation)
2. Reduce to irreducible representations
3. Subtract translations and rotations
4. Remaining modes are vibrations

## SALCs (Symmetry Adapted Linear Combinations)

### Constructing SALCs
1. Identify symmetry of atomic orbitals
2. Use projection operator method
3. Match with central atom orbital symmetries
4. Form bonding and antibonding combinations

### Application to Molecular Orbitals
- Only orbitals of the same symmetry can mix
- SALC symmetry must match central atom orbital symmetry for bonding

## Decision Flow
1. Identify all symmetry elements
2. Assign point group
3. Consult character table
4. Determine symmetry of relevant orbitals/vibrations
5. Apply selection rules for predictions

## Implementations and Data
- Symmetry analysis tools: [L3 code](../L3_functions/group_theory_tools.py)
- Point group reference: [L4 reference](../L4_reference/reference/crystallography-data.md)

## L3 Tool Call Directives

**Source:** `symmetry_tools.py`

⚠️ Stub file — no public functions implemented yet.

### Available functions:
- *(none — file is empty)*
