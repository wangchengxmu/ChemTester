---
id: chem.stoichiometric_conversion
layer: 2
title: Stoichiometric Conversion from Equations
source: LibreTexts Chemistry 2e Ch04.03
status: active
created: 2026-03-10
last_verified: 2026-03-10
---

# Stoichiometric Conversion from Equations

## Problem type
Convert between amounts of reactants/products using balanced equation coefficients.

## Decision tree

1. **What quantities given?**
   - Moles → Direct stoichiometric ratio
   - Mass → Convert to moles first
   - Particles → Use Avogadro's number
   - Volume (solution) → Use molarity
   - Volume (gas) → Use molar volume or ideal gas

2. **What conversion path?**
   - Reactant → Product: use ratio directly
   - Reactant A → Reactant B: via product stoichiometry
   - Multi-step: chain of ratios

## Core formulas

### Mole-to-mole
```
mol_B = mol_A × (coefficient_B / coefficient_A)
```

### Mass-to-mass
```
mass_B = mass_A × (1/M_A) × (coeff_B/coeff_A) × M_B
```

### Moles to particles
```
particles = mol × 6.022 × 10^23
```

### Solution stoichiometry
```
mol = M × V(L)
```

## Constraints
- Equation must be balanced
- Coefficients are MOLE ratios (not mass)
- Use molar masses for mass conversions
- Avogadro's number for particle counts

## Common patterns
- Given mass A, find mass B: mass → mol A → mol B → mass B
- Given volume solution, find mass: M×V → mol → mass
- Given particles, find mass: particles → mol → mass

## Links

### L3 Implementation
- `../L3_functions/stoichiometric_conversion_tools.py` (TODO)
- `../L3_functions/stoichiometric_conversion_tools.py` (TODO)

### L4 Reference
- `../L4_reference/stoichiometric-conversion-reference.md` (TODO)

### L5 Examples
- `../L5_examples/stoichiometry/ (TODO)

## L3 Tool Call Directive

When solving stoichiometric conversion problems (mass↔moles↔particles↔volume), call the appropriate L3 function:

**mass_to_mass** (`L3_functions/stoichiometric_conversion_tools.py`):
- Use when: Converting mass of reactant A to mass of product B using balanced equation.
- Parameters: `mass_A`, `molar_mass_A`, `molar_mass_B`, `coeff_A`, `coeff_B`

**mole_to_mole** (`L3_functions/stoichiometric_conversion_tools.py`):
- Use when: Converting moles of one substance to moles of another via mole ratio.
- Parameters: `mol_A`, `coeff_A`, `coeff_B`

**mass_to_moles** / **moles_to_mass** (`L3_functions/stoichiometric_conversion_tools.py`):
- Use when: Basic mass-mole conversions.
- Parameters: `mass, molar_mass` or `mol, molar_mass`

**moles_to_particles** / **particles_to_moles** (`L3_functions/stoichiometric_conversion_tools.py`):
- Use when: Converting between moles and number of particles (atoms/molecules).
- Parameters: `mol` or `particles`

**solution_moles** (`L3_functions/stoichiometric_conversion_tools.py`):
- Use when: Convert molarity and volume to moles (for solution stoichiometry).
- Parameters: `molarity`, `volume_L`

**ideal_gas_moles** (`L3_functions/stoichiometric_conversion_tools.py`):
- Use when: Use PV=nRT to find moles from gas conditions (alternative to ideal_gas_law_tools).
- Parameters: `P, V, T, R=0.08206`

**empirical_formula** (`L3_functions/stoichiometric_conversion_tools.py`):
- Use when: Determine empirical formula from percent composition.
- Parameters: `percent_composition_dict` (e.g. `{"C": 40.0, "H": 6.7, "O": 53.3}`)

**stoichiometric_calculation** (`L3_functions/stoichiometric_conversion_tools.py`):
- Use when: Given moles and coefficients, calculate moles and mass of product.
- Parameters: `given_moles`, `given_coeff`, `target_coeff`, `target_molar_mass`

**Critical notes:**
- For titration problems, combine `solution_moles` with mole-to-mole conversion.
- For gas stoichiometry, first use `ideal_gas_moles` or `moles_at_stp` to get moles, then apply mole ratio.

## Source trace
- `../sources/ingestion/source-stoichiometry-chemical-reactions-stepwise.md` section 4.03

## L3 Tool Call Directives

**Source:** `stoichiometric_conversion_tools.py`

Mole-to-mole, mass-to-mass, solution stoichiometry, limiting reactant, percent yield, empirical formula.

### Available functions:
- `mole_to_mole(mol_A, coeff_A, coeff_B)` → float — mol_B = mol_A × (coeff_B/coeff_A)
- `mass_to_moles(mass, molar_mass)` → float — mol = mass/M
- `moles_to_mass(mol, molar_mass)` → float — mass = mol × M
- `mass_to_mass(mass_A, molar_mass_A, molar_mass_B, coeff_A, coeff_B)` → float — Full mass-to-mass via stoichiometry
- `moles_to_particles(mol)` → float — mol × 6.022e23
- `particles_to_moles(particles)` → float — particles / 6.022e23
- `solution_moles(molarity, volume_L)` → float — M × V
- `solution_molarity(mol, volume_L)` → float — M = mol/V
- `ideal_gas_moles(P, V, T, R=0.08206)` → float — n = PV/RT
- `limiting_reactant(reactants_dict, stoichiometry)` → Tuple — (limiting_species, theoretical_yield_dict)
- `percent_yield(actual, theoretical)` → float — (actual/theoretical) × 100
- `empirical_formula(percent_composition_dict)` → str — Formula from % composition (e.g. 'CH2O')
- `stoichiometric_calculation(given_moles, given_coeff, target_coeff, target_molar_mass)` → float — Full calc

### Common errors:
- ❌ Swapping coeff_A and coeff_B in mole_to_mole — coeff_A is GIVEN substance
- ❌ Forgetting to convert mL→L or kg→g before calculation
- ❌ Not dividing by GCD in empirical formula
