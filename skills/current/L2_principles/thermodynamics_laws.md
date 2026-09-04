# Thermodynamics Laws

## Concept Overview

The Second and Third Laws of Thermodynamics establish the relationship between entropy and spontaneity, and define the absolute reference point for entropy.

## Key Principles

### Second Law
```
¦¤S_univ = ¦¤S_sys + ¦¤S_surr
```

| ¦¤S_univ | Process |
|---------|---------|
| > 0 | Spontaneous |
| < 0 | Nonspontaneous |
| = 0 | At equilibrium |

### Entropy of Surroundings
```
¦¤S_surr = q_surr / T = -¦¤H_sys / T
```
(at constant pressure)

### Third Law
- **Entropy of pure, perfect crystalline solid at 0 K = 0**
- Only one microstate possible: W = 1
- S = k ln(1) = 0

### Standard Entropy Change
```
¦¤S¡ã = ¦²¦ÍS¡ã(products) - ¦²¦ÍS¡ã(reactants)
```

### Standard Entropies (J/mol¡¤K) at 298 K
| Substance | S¡ã |
|-----------|-----|
| C(graphite) | 5.74 |
| H?(g) | 130.6 |
| O?(g) | 205.0 |
| H?O(l) | 69.9 |
| H?O(g) | 188.7 |
| CO?(g) | 213.8 |

## Problem-Solving Routes

1. **Calculate ¦¤S_univ**: Add system and surroundings contributions
2. **Predict spontaneity**: Check sign of ¦¤S_univ
3. **Calculate ¦¤S¡ã**: Use standard entropy values
4. **Find temperature effect**: Use ¦¤S_surr = -¦¤H/T

## Links

- **L3 Tools**: `../L3_functions/thermodynamics_laws_tools.py`
- **L4 Reference**: Standard entropy tables
- **L5 Examples**: Spontaneity predictions

## Related Topics

- Entropy
- Gibbs free energy
- Chemical equilibrium


## Implementations

- Implementation: `../L3_functions/thermodynamic_data_tools.py`

## Data Reference
- L3 Tool: 	hermodynamic_lookup_tools.lookup_thermodynamic_data(formula) â ÎHfÂ°, ÎGfÂ°, SÂ°, Cp for 58+ compounds
- L3 Tool: 	hermodynamic_lookup_tools.calculate_reaction_dH(reactants, products) â reaction enthalpy from formation data
- L3 Tool: 	hermodynamic_lookup_tools.calculate_reaction_dG(reactants, products) â reaction Gibbs energy
- L4 Data: L4_reference/thermodynamic_data.csv â Full table with NIST/CRC values
- L4 Reference: L4_reference/THERMODYNAMIC_DATABASES.md â Links to NIST-JANAF, NIST WebBook

## L3 Tool Call Directives

**Source:** `thermodynamics_laws_tools.py`
Thermodynamic laws: entropy of universe, spontaneity, third law, reaction entropy.

### Available functions:
- `entropy_universe(delta_S_sys, delta_S_surr)` → float — ΔS_univ = ΔS_sys + ΔS_surr
- `entropy_surroundings(delta_H, T)` → float — ΔS_surr = -ΔH_sys / T
- `spontaneity_from_Suniv(delta_S_univ)` → str — 'spontaneous' / 'nonspontaneous' / 'at equilibrium'
- `calculate_Suniv_from_process(delta_S_sys, delta_H_sys, T)` → dict — Full spontaneity analysis from process data
- `third_law_entropy(W)` → float — S = k·ln(W) at 0 K (0 for perfect crystal)
- `standard_entropy_reaction(S_values, reactants, products, coeffs)` → float — ΔS°_rxn from standard entropies

### Common errors:
- ❌ Using ΔS_sys alone to predict spontaneity (must use ΔS_univ or ΔG)
- ❌ Forgetting that ΔS_surr = -ΔH/T (negative sign is critical)
