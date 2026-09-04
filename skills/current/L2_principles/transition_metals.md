# Transition Metals

## Concept Overview

Transition metals have partially filled d orbitals and exhibit multiple oxidation states.

## Key Principles

### Definition
- Groups 3-11 (d-block)
- Partially filled d orbitals
- Multiple oxidation states

### Electron Configuration
- Remove s electrons before d for ions
- Fe → Fe²⁺ [Ar]3d⁶, Fe³⁺ [Ar]3d⁵

### Oxidation States
- Early transition metals: high oxidation states
- Middle: multiple stable states
- Late: lower oxidation states

## Links

- **L3 Tools**: `../L3_functions/transition_metals_tools.py`
- **L4 Reference**: Oxidation state tables
- **L5 Examples**: Electron configuration problems

## L3 Tool Call Directives

**Source:** `transition_metals_tools.py`
Transition metal chemistry: electron configurations, d-electron counts, oxidation states, unpaired electrons.

### Available functions:
- `ion_electron_config(element, charge)` → str — Full electron configuration for transition metal ion
- `count_d_electrons(element, charge)` → int — Count d-electrons in transition metal ion
- `count_unpaired_electrons(d_count, geometry, spin_state, pairing_energy)` → int — Count unpaired electrons considering LFSE
- `common_oxidation_states(element)` → list — Common oxidation states for transition metal

### Common errors:
- ❌ Not removing s-electrons first when determining d-electron count for cations
- ❌ Assuming high-spin for all geometries (strong-field ligands produce low-spin in octahedral)
