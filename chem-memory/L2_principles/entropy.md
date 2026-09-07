# Entropy

## Concept Overview

Entropy (S) is a state function that measures the dispersal of matter and energy in a system. It is related to the number of possible microstates.

## Key Principles

### Boltzmann Equation
```
S = k ln W
```
- k = 1.38 × 10⁻²³ J/K (Boltzmann constant)
- W = number of microstates

### Microstates
- Specific configurations of particle positions and energies
- More microstates → higher entropy
- Most probable distribution has maximum entropy

### Entropy Change
```
ΔS = q_rev / T
```
- q_rev = heat transferred reversibly
- T = absolute temperature (K)

### Predicting ΔS Sign
| Process | ΔS Sign | Reason |
|---------|---------|--------|
| Solid → Liquid | + | More microstates in liquid |
| Liquid → Gas | + | Much more microstates in gas |
| Gas → Liquid | - | Fewer microstates |
| Temperature increase | + | More energy distribution |

### Relative Entropies
```
S(solid) < S(liquid) < S(gas)
```

## Problem-Solving Routes

1. **Calculate ΔS from microstates**: Use Boltzmann equation
2. **Predict ΔS sign**: Assess phase/symmetry changes
3. **Calculate ΔS from heat**: Use ΔS = q_rev/T
4. **Standard entropy change**: ΔS° = ΣνS°(products) - ΣνS°(reactants)

## Links

- **L3 Tools**: `../L3_functions/entropy_tools.py`
- **L4 Reference**: Standard entropy tables
- **L5 Examples**: Entropy calculations

## Related Topics

- Spontaneity
- Second Law
- Free energy

## L3 Tool Call Directives

**Source:** `entropy_tools.py`

Entropy Tools - L3 Implementation

### Available functions:
- `entropy_from_microstates(W: float)` → float — Calculate entropy from number of microstates using Boltzmann equation.
- `entropy_change_microstates(W_initial: float, W_final: float)` → float — Calculate entropy change from initial and final microstates.
- `entropy_change_heat(q_rev: float, T: float)` → float — Calculate entropy change from reversible heat transfer.
- `predict_entropy_sign_phase_change(initial_phase: str, final_phase: str)` → str — Predict sign of entropy change for phase transition.
- `standard_entropy_change(S_products: list, S_reactants: list, coeffs_products: list, coeffs_reactants: list)` → float — Calculate standard entropy change for a reaction.
- `compare_entropies(phases: list)` → str — Compare relative entropies of different phases.

### Common errors:
- ❌ Passing wrong units (check function docstring for expected units)
- ❌ Omitting required parameters
