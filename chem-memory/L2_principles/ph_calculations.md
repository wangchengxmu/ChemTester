# pH and pOH Calculations

## Concept Overview

pH and pOH provide convenient scales for expressing hydronium and hydroxide ion concentrations.

## Key Principles

### pH Definition
```
pH = -log[H?O?]
[H?O?] = 10^(-pH)
```

### pOH Definition
```
pOH = -log[OH?]
[OH?] = 10^(-pOH)
```

### pH-pOH Relationship
```
pH + pOH = pKw = 14.00 (at 25¡ãC)
```

### Classification (25¡ãC)
| pH Range | Classification |
|----------|----------------|
| pH < 7 | Acidic |
| pH = 7 | Neutral |
| pH > 7 | Basic |

### pX Convention
```
pKa = -log(Ka)
pKb = -log(Kb)
pKw = -log(Kw) = 14.00
```

## Problem-Solving Routes

1. **Given [H?O?]**: Calculate pH = -log[H?O?]
2. **Given [OH?]**: Calculate pOH, then pH = 14 - pOH
3. **Given pH**: Calculate [H?O?] = 10^(-pH)

## L3 Tool Call Directives

**Always use L3 tools instead of manual calculation.** Call functions from `ph_calculations_tools.py`:

### Strong acid/base:
- `strong_acid_pH(concentration)` — pH = -log10(C) for complete dissociation
- `strong_base_pH(concentration)` — pOH = -log10(C), pH = 14 - pOH

### Weak acid/base:
- `weak_acid_pH(concentration, Ka)` — solves quadratic: [H⁺]² + Ka[H⁺] - Ka·C = 0
- `weak_base_pH(concentration, Kb)` — analogous for bases

### Key conversion functions:
- `Ka_from_pKa(pKa)` — Ka = 10^(-pKa)
- `pKa_from_Ka(Ka)` — pKa = -log10(Ka)
- `H3O_from_pH(pH)` — [H₃O⁺] = 10^(-pH)
- `pH_from_H3O(H3O)` — pH = -log10([H₃O⁺])
- `classify_by_pH(pH)` — acid/base/neutral classification

### Common caller errors to avoid:
1. ❌ Using simple sqrt(Ka×C) approximation for concentrated weak acids → Tool uses quadratic, which is more accurate
2. ❌ Treating a strong acid (HCl, HNO₃, HClO₄) as weak → Check if acid is on the strong acid list first
3. ❌ Forgetting that polyprotic acids (H₂SO₄, H₃PO₄) need stepwise treatment
4. ❌ For very dilute acids (< 10⁻⁶ M), water autoionization matters — tool handles this automatically
5. ❌ Mixing up Ka and pKa → Use Ka_from_pKa() to convert first

## Links

- **L3 Tools**: `../L3_functions/ph_calculations_tools.py`
- **L4 Reference**: pH of common substances
- **L5 Examples**: pH calculation problems

## Related Topics

- Br?nsted-Lowry theory
- Acid-base constants
- Buffer calculations


## Implementations

- Implementation: `../L3_functions/vant_hoff.py`
