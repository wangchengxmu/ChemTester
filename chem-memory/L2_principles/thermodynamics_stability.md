# Thermodynamics and Trends in Metal Complex Stability

**Source:** CHM 320 Advanced Inorganic Chemistry, Chapter 10

## Overview

Metal-ligand complex stability is governed by thermodynamic principles. Understanding stability constants and trends allows prediction of complex formation and ligand exchange behavior.

## Key Concepts

### Metal-Ligand Association Constants

**Stability Constant (K):** Equilibrium constant for complex formation
- For ML₅X + Y ⇌ ML₅Y + X: K = [ML₅Y][X]/[ML₅X][Y]
- Large K indicates stable complex

**Stepwise vs Overall Constants:**
- Stepwise: Kₙ for MLₙ₋₁ + L ⇌ MLₙ
- Overall: βₙ = K₁ × K₂ × ... × Kₙ

### Irving-Williams Series

Trend in stability constants for divalent first-row transition metals:

**Mn²⁺ < Fe²⁺ < Co²⁺ < Ni²⁺ < Cu²⁺ > Zn²⁺**

**Explanation:**
- Related to ionic radius and crystal field stabilization energy (CFSE)
- Cu²⁺ shows maximum due to Jahn-Teller distortion (extra stabilization)
- Zn²⁺ (d¹⁰) has no CFSE, drops in stability

### Chelate Effect

**Definition:** Multidentate ligands form more stable complexes than equivalent monodentate ligands

**Example:**
- [Ni(en)₃]²⁺ (en = ethylenediamine) more stable than [Ni(NH₃)₆]²⁺

**Thermodynamic Basis:**
- ΔG = ΔH - TΔS
- Chelate effect primarily **entropic**: more particles released upon binding
- For [M] + 3 en → [M(en)₃]: 4 particles → 1 particle (ΔS < 0 less negative than monodentate)

**Quantitative Effect:**
- Each chelate ring provides ~10²-10³ enhancement in K

### Macrocyclic Effect

**Definition:** Macrocyclic ligands form even more stable complexes than open-chain chelates

**Examples:**
- Porphyrins, crown ethers, cyclams

**Contributing Factors:**
1. **Preorganization:** Less entropy loss upon binding (ligand already in correct conformation)
2. **Enhanced chelate effect:** Multiple donor atoms in rigid geometry

### Entropy Contributions to Stability

**Key Relationship:**
- ΔG° = -RT ln K
- More negative ΔG° → larger K → more stable complex

**Entropy Sources:**
1. **Release of solvent molecules** from metal and ligand coordination spheres
2. **Number of particles** in reaction (chelate effect)
3. **Desolvation entropy** upon complex formation

## Stability Trends Summary

| Factor | Effect on Stability |
|--------|---------------------|
| Higher charge on metal | ↑ Stability (electrostatic) |
| Smaller ionic radius | ↑ Stability (electrostatic) |
| CFSE contribution | ↑ Stability (varies by dⁿ) |
| Chelating ligands | ↑ Stability (entropy) |
| Macrocyclic ligands | ↑↑ Stability (preorganization) |
| π-acceptor ligands | ↑ Stability (backbonding) |

## Related Concepts

- **L2/crystal_field_theory.md** - CFSE contributions
- **L2/coordination_chemistry.md** - Ligand types
- **L2/gibbs_free_energy.md** - Thermodynamic basis
- **L2/kinetics_lability.md** - Kinetic vs thermodynamic stability

## Problem-Solving Approaches

1. **Calculate K from ΔG°:** K = exp(-ΔG°/RT)
2. **Predict stability trends:** Apply Irving-Williams series
3. **Compare chelate vs monodentate:** Count particles, consider entropy
4. **Assess preorganization:** Evaluate ligand conformational flexibility

## Formulas

- **Stability constant:** K = [products]/[reactants]
- **Free energy:** ΔG° = -RT ln K = -2.303 RT log K
- **Van't Hoff:** d(ln K)/d(1/T) = -ΔH°/R

## Notes

- Thermodynamic stability ≠ kinetic inertness
- A complex can be thermodynamically unstable but kinetically inert (slow to react)
- Conversely, thermodynamically stable complexes can be labile (fast exchange)
