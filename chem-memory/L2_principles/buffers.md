# Buffers

## Concept Overview

Buffer solutions resist pH changes when small amounts of acid or base are added.

## Key Principles

### Buffer Composition
- Weak acid + its conjugate base (e.g., CH₃COOH + CH₃COO⁻)
- Weak base + its conjugate acid (e.g., NH₃ + NH₄⁺)

### Henderson-Hasselbalch Equation
```
pH = pKa + log([A⁻]/[HA])
```

### Buffer Capacity
- Maximum when [HA] = [A⁻] (pH = pKa)
- Determined by total concentration [HA] + [A⁻]

### Buffer Range
Effective range: pKa ± 1

### Buffer Preparation Methods
1. Mix weak acid + its salt
2. Mix weak base + its salt
3. Partial neutralization

## Problem-Solving Routes

1. **Calculate buffer pH**: Use Henderson-Hasselbalch
2. **Calculate pH after adding acid/base**: Modify [HA] and [A⁻], recalculate
3. **Design buffer**: Choose acid with pKa ≈ target pH
4. **Determine buffer capacity**: Check [HA] and [A⁻] amounts

## Links

- **L3 Tools**: `../L3_functions/buffer_tools.py`
- **L4 Reference**: Common buffer systems
- **L5 Examples**: Buffer preparation problems

## Related Topics

- Acid-base constants
- Titration curves
- Equilibrium calculations

## L3 Tool Call Directives


**Source:** `buffer_calculators.py`

L3 tool module for buffer calculators

### Available functions:
- `hh_pH(pKa: float, base_conc: float, acid_conc: float)` → float — Henderson-Hasselbalch pH estimate.
- `required_ratio_for_target_pH(pKa: float, target_pH: float)` → float — Return required [base]/[acid] ratio.
- `pair_match_score(pKa: float, target_pH: float)` → dict — Simple suitability score by distance to pKa.
- `perturbation_estimate(pKa: float, acid_moles: float, base_moles: float, added_strong_acid_moles: float, added_strong_base_moles: float)` → float — Estimate new pH after small strong acid/base addition.

### Common errors:
- ❌ Passing wrong parameter types (strings where numbers expected)
- ❌ Forgetting required parameters
