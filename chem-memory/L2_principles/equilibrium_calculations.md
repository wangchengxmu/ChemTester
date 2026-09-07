# Equilibrium Calculations

## Concept Overview

Equilibrium calculations use the equilibrium constant to determine concentrations or pressures at equilibrium.

## Key Principles

### ICE Table Method
| Species | Initial | Change | Equilibrium |
|---------|---------|--------|-------------|
| A | [A]₀ | -ax | [A]₀ - ax |
| B | [B]₀ | -bx | [B]₀ - bx |
| C | [C]₀ | +cx | [C]₀ + cx |

### Stoichiometric Relationships
For: aA + bB ⇌ cC + dD
```
Δ[A]/a = Δ[B]/b = -Δ[C]/c = -Δ[D]/d
```

### Calculation Types

1. **Calculate K from equilibrium concentrations**
   - Direct substitution

2. **Find missing equilibrium concentration**
   - Algebraic solution from K

3. **Find equilibrium concentrations from initial**
   - ICE table + quadratic equation

### Quadratic Formula
When needed:
```
x = (-b ± √(b² - 4ac)) / 2a
```

### Small K Approximation
If K × C₀ << 1:
```
(C₀ - x) ≈ C₀
```
Valid when <5% error acceptable.

## Problem-Solving Routes

1. **Set up ICE table**: List initial, change, equilibrium rows
2. **Write K expression**: From balanced equation
3. **Substitute**: Equilibrium expressions into K
4. **Solve**: Algebra or quadratic
5. **Check**: Verify Q = K with results

## Links

- **L3 Tools**: `../L3_functions/ice_table_tools.py`
- **L4 Reference**: Quadratic solution examples
- **L5 Examples**: Complex equilibrium problems

## Related Topics

- Chemical equilibrium
- Equilibrium constants
- Le Chatelier's Principle

## L3 Tool Call Directives

**Source:** `ice_table_tools.py`

ICE table construction and equilibrium calculations: build tables, solve quadratics, small K approximation, and verification.

### Available functions:
- `build_ice_table(species, coefficients, initial, is_reactant)` → Dict — Build ICE table structure with initial/change/equilibrium rows
- `ice_table_simple(K, initial_reactant, coeff_reactant, coeff_product)` → Dict — Solve A ⇌ nB equilibrium; returns {'reactant', 'product', 'x'}
- `solve_quadratic(a, b, c)` → Tuple[float, float] — Returns (root1, root2); choose physically meaningful (positive, < initial)
- `small_k_approximation(K, initial)` → float — Approximate x ≈ √(K × initial) when K × C₀ << 1
- `check_approximation_valid(K, initial, x, threshold=0.05)` → bool — Returns True if x/initial < threshold (5% rule)
- `stoichiometric_changes(x, coefficients, is_reactant)` → Dict — Calculate concentration changes from x
- `equilibrium_from_initial(initial, changes)` → Dict — Add initial + changes to get equilibrium concentrations
- `verify_equilibrium(equilibrium, K, products, reactants)` → bool — Check if Q ≈ K (within 1%)

### Common errors:
- ❌ Using negative roots from quadratic (choose positive root that gives positive equilibrium concentrations)
- ❌ Forgetting to check 5% rule before using small K approximation
- ❌ Mixing up reactant (decreases) vs product (increases) change signs
