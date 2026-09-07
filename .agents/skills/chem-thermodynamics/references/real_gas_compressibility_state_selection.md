# Real-gas compressibility model and virial-order selection

## Applicability

A real-gas problem requests a compressibility factor from state data or asks for a virial approximation derived from an equation of state.

## Procedure

1. Declare whether the target is the observed-state definition, a density virial truncation, a pressure virial truncation, or the full equation of state before substituting values.
2. For the van der Waals equation, derive the second virial coefficient B2(T)=b-a/(RT).
3. For a first pressure-form virial estimate, use Z≈1+B2(T)p/(RT); retain additional terms only when the requested order supports them.
4. Use Z=pV_m/(RT), with V_m=M/rho when needed, for the supplied-state factor or as an independent consistency check.
5. Report the dimensionless result from the requested model and verify units, expansion variable, and truncation order.

## Boundaries

- Do not silently replace a virial truncation with the exact van der Waals equation.
- Do not mix pressure-form p/(RT) with density-form 1/V_m corrections.
- Do not force every supplied constant into the calculation.
- Do not let a consistency check override an explicitly requested approximation.
- Use only available documented support; otherwise apply the explicit derivation or label missing empirical evidence unresolved. A library filename is not an executable tool.

Only calculators listed in this package's calculator reference are callable here.
Other filenames in a procedure are historical pointers, not installed dependencies.
For missing empirical support, obtain an authoritative source or state the uncertainty.
