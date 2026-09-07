# Le Chatelier's Principle

## Concept Overview

Le Chatelier's Principle states: if a stress is applied to an equilibrium system, the system shifts to counteract the stress and re-establish equilibrium.

## Key Principles

### Concentration Changes
| Stress | Shift |
|--------|-------|
| Add reactant | Right (→ products) |
| Remove reactant | Left (← reactants) |
| Add product | Left (← reactants) |
| Remove product | Right (→ products) |

### Pressure/Volume Changes (Gas Phase)
| Stress | Shift |
|--------|-------|
| Increase pressure (decrease volume) | Toward fewer moles gas |
| Decrease pressure (increase volume) | Toward more moles gas |
| No change in moles (Δn = 0) | No shift |

### Temperature Changes
- **Only stress that changes K**

| Reaction Type | Heat Role | T Increase Effect |
|---------------|-----------|-------------------|
| Endothermic (ΔH > 0) | Reactant | Shifts right |
| Exothermic (ΔH < 0) | Product | Shifts left |

### Catalysts
- Do NOT shift equilibrium
- Only speed up equilibrium attainment
- Rates increase equally in both directions

## Problem-Solving Routes

1. **Identify stress type**: Concentration, pressure, or temperature
2. **Determine shift direction**: Apply Le Chatelier rules
3. **Predict new composition**: More products or reactants
4. **Check K change**: Only temperature changes K

## Links

- **L3 Tools**: `../L3_functions/le_chatelier_tools.py`
- **L4 Reference**: Common equilibrium shifts table
- **L5 Examples**: Industrial applications (Haber process)

## Related Topics

- Chemical equilibrium
- Equilibrium constants
- Equilibrium calculations

## L3 Tool Call Directives

**Source:** `le_chatelier_tools.py`

Equilibrium shift predictions for concentration, pressure, and temperature changes.

### Available functions:
- `predict_shift_concentration(stress_type, species, is_reactant)` → str — Returns 'right' or 'left'; stress_type = 'add' or 'remove'
- `predict_shift_pressure(delta_n, pressure_change)` → str — delta_n = moles gas products - reactants; returns 'right', 'left', or 'no change'
- `predict_shift_temperature(delta_H, temp_change)` → Tuple[str, bool] — Returns (shift_direction, K_changes); delta_H in J/mol
- `apply_stress(K_initial, stress)` → Dict — General stress application with type and change
- `catalyst_effect()` → Dict — Returns {'shifts_equilibrium': False, 'effect': 'Increases both forward and reverse rates equally'}
- `volume_change_moles(reactant_moles, product_moles, volume_change)` → str — Shift direction from volume change
- `summarize_le_chatelier()` → Dict — Full summary table of all stress responses

### Common errors:
- ❌ Forgetting that temperature is the ONLY stress that changes K
- ❌ Not checking delta_n = 0 case (no shift for pressure/volume if moles equal)
- ❌ Confusing endothermic (ΔH > 0) with exothermic (ΔH < 0) for temperature shifts
