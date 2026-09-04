# Galvanic Cells

## Concept Overview

Galvanic cells convert chemical energy to electrical energy through spontaneous redox reactions.

## Key Principles

### Cell Components
| Component | Function |
|-----------|----------|
| Anode | Oxidation site (electrons flow out) |
| Cathode | Reduction site (electrons flow in) |
| Salt bridge | Ion flow, charge balance |
| Electrodes | Conductive surfaces |

### Cell Notation
```
anode | anode solution || cathode solution | cathode
```

### Electron Flow
- Anode → Cathode (through external circuit)
- Anions → Anode (through salt bridge)
- Cations → Cathode (through salt bridge)

## Links

- **L3 Tools**: `../L3_functions/galvanic_cells_tools.py`
- **L4 Reference**: Standard cell diagrams
- **L5 Examples**: Cell notation problems

## L3 Tool Call Directives

**Source:** `galvanic_cells_tools.py`

Galvanic cell calculations: cell potentials, spontaneity predictions, electrode identification, and oxidizing/reducing agent strength.

### Available functions:
- `cell_potential(E_cathode, E_anode)` → float — Calculate E°_cell = E°_cathode - E°_anode
- `identify_anode_cathode(E1, E2)` → Dict — Returns {'cathode_E', 'anode_E', 'spontaneous'} from two half-cell potentials
- `predict_spontaneity(E_cell)` → str — Returns 'spontaneous', 'nonspontaneous', or 'at equilibrium'
- `cell_notation(anode_species, anode_solution, cathode_solution, cathode_species)` → str — Generate "anode | anode_soln || cathode_soln | cathode"
- `half_reactions_balanced(anode_reaction, cathode_reaction, n_electrons)` → Dict — Returns balanced half-reaction info
- `overall_reaction(anode_half, cathode_half)` → str — Combine half-reactions into overall cell reaction
- `strongest_oxidizing_agent(E_values)` → str — Species with highest reduction potential
- `strongest_reducing_agent(E_values)` → str — Species with lowest reduction potential

### Common errors:
- ❌ Using oxidation potentials instead of reduction potentials (ALL E° values must be reduction)
- ❌ Confusing anode (oxidation, lower E°) with cathode (reduction, higher E°)
- ❌ Forgetting that E°_cell > 0 means spontaneous
