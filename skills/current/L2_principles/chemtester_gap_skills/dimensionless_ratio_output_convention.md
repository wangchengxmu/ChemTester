# Dimensionless ratio and percentage answer convention

**Retrieve with:** dimensionless ratio output, fraction versus percent, single numeric scalar, part to whole quotient

**Use when:** A prompt requests a dimensionless ratio, fraction, efficiency, yield, probability, or conversion, especially as exactly one numeric value.

## Procedure

1. Assign the requested part or outcome to the numerator and the total or reference quantity to the denominator, then compute the quotient.
2. Use percent only when explicitly requested; otherwise retain the dimensionless quotient.
3. When exactly one numeric value is requested, evaluate any a/b expression and emit only one decimal or scientific-notation numeral with adequate precision.
4. Check expected bounds and perform rounding only after evaluating the quotient.

## Preferred Support

- chem-memory/L2_principles/chemtester_gap_skills/dimensionless_ratio_output_convention.md

## Guards

- Do not leave an unevaluated a/b expression when one numeric scalar is required.
- Do not invert part and whole.
- Do not convert to percent unless requested.
- Do not print both fractional and percentage forms.
