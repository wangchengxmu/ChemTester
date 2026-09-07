# Brønsted-Lowry Acids and Bases

## Concept Overview

The Brønsted-Lowry model defines acids as proton donors and bases as proton acceptors.

## Key Principles

### Definitions
- **Acid**: Proton (H⁺) donor
- **Base**: Proton (H⁺) acceptor
- **Conjugate pair**: Acid and base differing by one H⁺

### Conjugate Acid-Base Pairs
```
HA + H₂O ⇌ H₃O⁺ + A⁻
acid   base   conjugate  conjugate
       (solvent) acid     base
```

### Amphiprotic Species
- Can donate or accept protons
- Examples: H₂O, HCO₃⁻, H₂PO₄⁻, HS⁻

### Autoionization of Water
```
2H₂O ⇌ H₃O⁺ + OH⁻
Kw = [H₃O⁺][OH⁻] = 1.0 × 10⁻¹⁴ (at 25°C)
```

## Problem-Solving Routes

1. **Identify conjugate pairs**: Find species differing by H⁺
2. **Identify amphiprotic**: Check if can donate AND accept
3. **Calculate [H₃O⁺] or [OH⁻]**: Use Kw relationship

## Links

- **L3 Tools**: `../L3_functions/bronsted_lowry_tools.py`
- **L4 Reference**: Kw temperature dependence
- **L5 Examples**: Conjugate pair identification

## Related Topics

- pH calculations
- Acid-base constants
- Buffer solutions

## L3 Tool Call Directives


**Source:** `bronsted_lowry_tools.py`

L3 tool module for bronsted lowry tools

### Available functions:
- `conjugate_base(acid: str, formula: str)` → str — Return conjugate base of an acid.
- `conjugate_acid(base: str, formula: str)` → str — Return conjugate acid of a base.
- `identify_acid_base(reaction: str)` → dict — Identify acid, base, conjugate acid, conjugate base in reaction.
- `is_amphiprotic(formula: str)` → bool — Check if species is amphiprotic.
- `Kw_value(temperature: float)` → float — Return ion product of water at given temperature.
- `h3o_from_oh(oh_conc: float, temperature: float)` → float — Calculate [H3O+] from [OH-] using Kw.
- `oh_from_h3o(h3o_conc: float, temperature: float)` → float — Calculate [OH-] from [H3O+] using Kw.
- `classify_solution(h3o_conc: float, temperature: float)` → str — Classify solution as acidic, basic, or neutral.

### Common errors:
- ❌ Passing wrong parameter types (strings where numbers expected)
- ❌ Forgetting required parameters
