# Acid and Base Ionization Constants

## Concept Overview

Ka and Kb quantify the strength of weak acids and bases by measuring their extent of ionization.

## Key Principles

### Acid Ionization Constant (Ka)
```
HA + H₂O ⇌ H₃O⁺ + A⁻
Ka = [H₃O⁺][A⁻]/[HA]
```

### Base Ionization Constant (Kb)
```
B + H₂O ⇌ HB⁺ + OH⁻
Kb = [HB⁺][OH⁻]/[B]
```

### Ka-Kb Relationship
```
Ka × Kb = Kw = 1.0 × 10⁻¹⁴
pKa + pKb = 14.00
```

### Percent Ionization
```
% ionization = [H₃O⁺]eq/[HA]₀ × 100%
```

### Strong vs Weak
| Type | Ka/Kb | Ionization |
|------|-------|------------|
| Strong | >> 1 | ~100% |
| Weak | << 1 | < 100% |

### Inverse Relationship
- Stronger acid → weaker conjugate base
- Stronger base → weaker conjugate acid

## Problem-Solving Routes

1. **Calculate Ka from equilibrium**: Use ICE table
2. **Find [H₃O⁺] from Ka**: Solve Ka = x²/(C₀ - x)
3. **Convert Ka ↔ Kb**: Use Ka × Kb = Kw
4. **Calculate % ionization**: [H₃O⁺]eq/[HA]₀ × 100

## Links

- **L3 Tools**: `../L3_functions/acid_base_constants_tools.py`
- **L4 Reference**: Ka and Kb tables
- **L5 Examples**: Weak acid/base calculations

## Related Topics

- pH calculations
- Salt hydrolysis
- Buffer solutions

## L3 Tool Call Directives


**Source:** `acid_base_constants_tools.py`

L3 tool module for acid base constants tools

### Available functions:
- `Ka_Kb_relationship(Ka: float, Kb: float, temperature: float)` → float — Calculate Ka from Kb or vice versa.
- `percent_ionization(h3o_conc: float, initial_conc: float)` → float — Calculate percent ionization of a weak acid.
- `weak_acid_pH(Ka: float, initial_conc: float)` → float — Calculate pH of weak acid solution.
- `weak_base_pH(Kb: float, initial_conc: float)` → float — Calculate pH of weak base solution.
- `is_strong_acid(Ka: float)` → bool — Determine if acid is strong based on Ka.
- `is_strong_base(Kb: float)` → bool — Determine if base is strong based on Kb.
- `compare_acid_strengths(Ka1: float, Ka2: float)` → str — Compare relative acid strengths.
- `conjugate_base_strength(Ka: float, temperature: float)` → float — Calculate Kb of conjugate base.
- `validate_approximation(Ka: float, C0: float, threshold: float)` → bool — Check if small x approximation is valid.

### Common errors:
- ❌ Passing wrong parameter types (strings where numbers expected)
- ❌ Forgetting required parameters


**Source:** `acid_base_tools.py`

L3 tool module for acid base tools

### Available functions:
- `hsab_classify(acid_hardness: float, base_hardness: float)` → str — Classify acid as hard, soft, or borderline based on hardness parameter.
- `hsab_compatibility(acid_type: str, base_type: str)` → str — Predict acid-base adduct stability: hard-hard, soft-soft preferred.
- `calculate_pka_conjugate(pka: float)` → float — Calculate pKb from pKa (in water at 25degC). pKa + pKb = 14.

### Common errors:
- ❌ Passing wrong parameter types (strings where numbers expected)
- ❌ Forgetting required parameters
