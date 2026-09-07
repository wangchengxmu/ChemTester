# Electrode Potentials

## Concept Overview

Standard reduction potentials quantify the tendency of species to gain electrons.

## Key Principles

### Cell Potential
```
E_cell = E_cathode - E_anode
```

### Standard Hydrogen Electrode (SHE)
- Reference electrode: E° = 0 V
- 2H⁺ + 2e⁻ → H₂

### Spontaneity
- E°_cell > 0 → spontaneous
- E°_cell < 0 → nonspontaneous

## Links

- **L3 Tools**: `../L3_functions/electrode_potentials_tools.py`
- **L4 Reference**: E° tables
- **L5 Examples**: Potential calculations

## Data Reference
- L4 Data: L4_reference/electrode_potentials.csv — Standard reduction potentials E° for 28 half-reactions
- L4 Reference: L4_reference/THERMODYNAMIC_DATABASES.md — Links to NIST, CRC Handbook

## L3 Tool Call Directives

**Source:** `electrode_potentials_tools.py`

Electrode Potentials Tools - L3 Implementation

### Available functions:
- `standard_cell_potential(E_cathode: float, E_anode: float)` → float — Calculate standard cell potential from standard reduction potentials.
- `lookup_potential(species: str)` → float — Look up standard reduction potential for a species.
- `will_reaction_occur(E_cathode: float, E_anode: float)` → bool — Determine if redox reaction will occur spontaneously.
- `compare_oxidizing_strength(E1: float, species1: str, E2: float, species2: str)` → str — Compare oxidizing strengths of two species.
- `compare_reducing_strength(E1: float, species1: str, E2: float, species2: str)` → str — Compare reducing strengths of two species.
- `calculate_cell_potential_from_notation(anode_species: str, cathode_species: str)` → float — Calculate cell potential from half-cell species.
- `list_species_by_oxidizing_strength(species_list: List[str])` → List[str] — Sort species by oxidizing strength (highest Edeg first).

### Common errors:
- ❌ Passing wrong units (check function docstring for expected units)
- ❌ Omitting required parameters
