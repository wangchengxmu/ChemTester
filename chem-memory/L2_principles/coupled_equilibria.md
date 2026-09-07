# Coupled Equilibria

## Concept Overview

Coupled equilibria involve multiple equilibrium reactions sharing species, where the overall equilibrium constant is the product of individual constants.

## Key Principles

### Combining Equilibrium Constants
```
Net K = K₁ × K₂ × K₃ × ...
```

### Acid-Enhanced Dissolution
```
CaCO₃(s) + H₃O⁺ ⇌ Ca²⁺ + HCO₃⁻ + H₂O
K = Ksp/Ka₂
```

### Complex-Enhanced Dissolution
```
Al(OH)₃(s) + OH⁻ ⇌ Al(OH)₄⁻
K = Ksp × Kf
```

### Common Ion Effect
- Decreases solubility
- Shifts equilibrium toward solid

### Complex Ion Effect
- Increases solubility
- Removes metal ion from solution

## Problem-Solving Routes

1. **Identify coupled reactions**: Find shared species
2. **Write individual equilibria**: With individual K values
3. **Combine reactions**: Add equations, multiply K values
4. **Calculate net K**: Product of individual constants
5. **Solve equilibrium**: Use net K

## Links

- **L3 Tools**: `../L3_functions/coupled_equilibria_tools.py`
- **L4 Reference**: Environmental examples
- **L5 Examples**: Ocean acidification, dissolution

## Related Topics

- Solubility equilibria
- Lewis acid-base
- Multiple equilibria

## L3 Tool Call Directives

**Source:** `coupled_equilibria_tools.py`

Coupled Equilibria Tools - L3 Implementation

### Available functions:
- `combine_equilibrium_constants(K_values: List[float])` → float — Combine multiple equilibrium constants for coupled reactions.
- `acid_enhanced_K(Ksp: float, Ka: float)` → float — Calculate equilibrium constant for acid-enhanced dissolution.
- `complex_enhanced_K(Ksp: float, Kf: float)` → float — Calculate equilibrium constant for complex-enhanced dissolution.
- `solubility_with_acid(Ksp: float, Ka: float, H_conc: float, anion_coeff: int)` → float — Calculate solubility enhanced by acid.
- `solubility_with_complex(Ksp: float, Kf: float, ligand_conc: float, n_ligands: int)` → float — Calculate solubility enhanced by complex formation.
- `predict_dissolution_behavior(Ksp: float, Kf: float, Ka: float, conditions: Dict)` → str — Predict dissolution behavior under various conditions.
- `common_ion_effect_factor(common_ion_conc: float, stoich_coeff: int)` → float — Calculate the reduction factor due to common ion effect.
- `coupled_system_summary(reactions: List[Dict])` → Dict — Summarize a coupled equilibrium system.

### Common errors:
- ❌ Passing wrong units (check function docstring for expected units)
- ❌ Omitting required parameters
