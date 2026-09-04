# Gibbs Free Energy

## Concept Overview

Gibbs free energy (G) is a state function that predicts spontaneity at constant temperature and pressure using only system properties.

## Key Principles

### Definition
```
G = H - TS
```

### Free Energy Change
```
¦¤G = ¦¤H - T¦¤S
```

### Relationship to Spontaneity
```
¦¤G = -T¦¤S_univ
```

| ¦¤G | Process |
|-----|---------|
| < 0 | Spontaneous (forward) |
| > 0 | Nonspontaneous (reverse spontaneous) |
| = 0 | At equilibrium |

### Calculating ¦¤G¡ã

**Method 1: From ¦¤H¡ã and ¦¤S¡ã**
```
¦¤G¡ã = ¦¤H¡ã - T¦¤S¡ã
```

**Method 2: From standard free energies of formation**
```
¦¤G¡ã = ¦²¦Í¦¤G_f¡ã(products) - ¦²¦Í¦¤G_f¡ã(reactants)
```

### Temperature Dependence
| ¦¤H | ¦¤S | Low T | High T |
|----|-----|-------|--------|
| - | + | Spontaneous | Spontaneous |
| - | - | Spontaneous | Nonspontaneous |
| + | + | Nonspontaneous | Spontaneous |
| + | - | Nonspontaneous | Nonspontaneous |

### Free Energy and Equilibrium
```
¦¤G¡ã = -RT ln K
```
- R = 8.314 J/mol¡¤K
- K = equilibrium constant

### Free Energy and Work
```
¦¤G = w_max
```
(maximum useful non-PV work)

## Problem-Solving Routes

1. **Calculate ¦¤G¡ã from ¦¤H¡ã, ¦¤S¡ã**: Use ¦¤G¡ã = ¦¤H¡ã - T¦¤S¡ã
2. **Calculate ¦¤G¡ã from ¦¤G_f¡ã**: Use formation values
3. **Predict spontaneity**: Check sign of ¦¤G
4. **Find equilibrium K**: Use K = e^(-¦¤G¡ã/RT)
5. **Determine temperature range**: Solve ¦¤G = 0 for T

## Links

- **L3 Tools**: `../L3_functions/gibbs_free_energy_tools.py`
- **L4 Reference**: Standard free energy tables
- **L5 Examples**: Free energy calculations

## Related Topics

- Entropy
- Second Law
- Chemical equilibrium


## Implementations

- Implementation: `../L3_functions/potential_free_energy_tools.py`

## Data Reference
- L3 Tool: 	hermodynamic_lookup_tools.lookup_thermodynamic_data(formula) â ÎHfÂ°, ÎGfÂ°, SÂ°, Cp for 58+ compounds
- L3 Tool: 	hermodynamic_lookup_tools.calculate_reaction_dH(reactants, products) â reaction enthalpy from formation data
- L3 Tool: 	hermodynamic_lookup_tools.calculate_reaction_dG(reactants, products) â reaction Gibbs energy
- L4 Data: L4_reference/thermodynamic_data.csv â Full table with NIST/CRC values
- L4 Reference: L4_reference/THERMODYNAMIC_DATABASES.md â Links to NIST-JANAF, NIST WebBook

## L3 Tool Call Directives

**Source:** potential_free_energy_tools.py
Potential, Free Energy, and Equilibrium Tools - L3 Implementation

### Available functions:
- free_energy_from_potential(E_cell, n) → float — Calculate standard free energy change from cell potential.
- potential_from_free_energy(delta_G, n) → float — Calculate cell potential from free energy change.
- equilibrium_constant_from_potential(E_cell, n, T) → float — Calculate equilibrium constant from standard cell potential.
- potential_from_equilibrium_constant(K, n, T) → float — Calculate standard cell potential from equilibrium constant.
- nernst_equation(E_standard, n, Q, T) → float — Calculate cell potential under nonstandard conditions using Nernst equation.
- concentration_cell_potential(c_anode, c_cathode, n, T) → float — Calculate potential of a concentration cell.
- spontaneity_summary(E_cell) → Dict — Summarize spontaneity from cell potential.
- reaction_quotient_from_potential(E_cell, E_standard, n) → float — Calculate reaction quotient from measured cell potential.

### Common errors:
- ❌ Passing wrong parameter types or missing required arguments
