# Scaled-unit coefficient reporting

**Retrieve with:** scaled unit coefficient, power of ten answer format, scientific notation reporting

**Use when:** A calculation asks for one numeric value in units of a stated power-of-ten multiple of a physical unit.

## Procedure

1. Compute the physical quantity in base units and retain its physical unit.
2. Treat the stated reporting unit as S = 10^k times the base unit and calculate the requested coefficient a = Q/S.
3. Reconstruct Q = aS to verify the exponent, sign, and magnitude against the original calculation.
4. When exactly one numeric value is requested, emit only a in the specified scale; do not append another power of ten or revert to base-unit scientific notation.

## Guards

- Do not apply the reporting scale twice.
- Do not confuse a scaled reporting unit with a request for the full base-unit scientific-notation value.
- Do not print both the coefficient and reconstructed quantity when only one numeric value is requested.
