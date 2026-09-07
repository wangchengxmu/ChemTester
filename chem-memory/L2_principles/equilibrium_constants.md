# Equilibrium Constants

## Concept Overview

The equilibrium constant (K) quantifies the ratio of products to reactants at equilibrium. The reaction quotient (Q) measures this ratio at any point in the reaction.

## Key Principles

### Reaction Quotient (Q)
For reaction: mA + nB ⇌ xC + yD

**Concentration-based:**
```
Q_c = [C]^x[D]^y / [A]^m[B]^n
```

**Pressure-based:**
```
Q_p = P_C^x × P_D^y / P_A^m × P_B^n
```

### Equilibrium Constant (K)
```
K ≡ Q at equilibrium
```

### Kc and Kp Relationship
For gas-phase reactions:
```
K_p = K_c(RT)^Δn
```
where Δn = moles gas products - moles gas reactants

### Interpreting K Values
| K Value | Meaning |
|---------|---------|
| K >> 1 | Products favored |
| K << 1 | Reactants favored |
| K ≈ 1 | Neither favored |

### Predicting Direction
| Comparison | Direction |
|------------|-----------|
| Q < K | Forward (→) |
| Q > K | Reverse (←) |
| Q = K | At equilibrium |

### Heterogeneous Equilibria
- Pure solids/liquids: activity = 1
- Omitted from Q expression

## Problem-Solving Routes

1. **Write Q expression**: Products^coefficients / Reactants^coefficients
2. **Calculate Q**: Substitute concentrations/pressures
3. **Compare Q to K**: Determine direction
4. **Convert Kc ↔ Kp**: Use K_p = K_c(RT)^Δn

## Links

- **L3 Tools**: `../L3_functions/equilibrium_constant_tools.py`
- **L4 Reference**: K value tables by temperature
- **L5 Examples**: Q calculations, direction predictions

## Related Topics

- Chemical equilibrium
- Le Chatelier's Principle
- Equilibrium calculations

## L3 Tool Call Directives

**Source:** `reaction_quotient_tools.py`

⚠️ Stub file — no public functions implemented yet.

### Available functions:
- *(none — file is empty)*
