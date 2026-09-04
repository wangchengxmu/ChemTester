# Coupled solubility, precipitation, and acid-base regression

**Retrieve with:** metal hydroxide Ksp buffer, precipitation pH buffer salt mass, weak-acid anion solubility, Ksp Ka pH regression, transformed equilibrium fit, significant-figure option check

**Use when:** Solubility or precipitation is coupled to pH, buffering, protonation, or complexation, including threshold precipitation calculations and multi-point measurements used to recover equilibrium constants.

## Procedure

1. Write the solubility product, relevant acid-base equilibria, stoichiometric exponents, and mass balances together; distinguish free-ion concentrations from total dissolved concentration.
2. For threshold precipitation, use the target free-metal concentration to obtain the required hydroxide concentration, convert to pH or pOH, solve the buffer ratio, and then apply final volume and molar mass to the requested reagent amount.
3. For multi-point solubility data, derive the transformed model before fitting; for a 1:1 salt with a protonatable anion, fit squared solubility against hydrogen-ion concentration, with intercept Ksp and slope Ksp/Ka.
4. Transform observations without premature rounding, compute centered-sum ordinary least squares, recover physical constants algebraically, and check positivity, residual quality, and limiting behavior.
5. Retain guard digits and accept a printed numerical choice only when the unrounded result lies within its displayed rounding interval; evaluate underlying statements independently before selecting a multiple-correct response.

## Preferred Support

- chem-memory/L2_principles/solubility_equilibria.md
- chem-memory/L2_principles/ph_calculations.md
- chem-memory/L2_principles/chemometrics_calibration_regression.md
- chem-memory/L3_functions/chemometrics_tools.py

## Guards

- Respect every stoichiometric exponent in the solubility product.
- Do not replace a free-ion concentration with total solubility when protonation or complexation is present.
- Do not mix pre-dilution and final-volume concentration bases.
- Do not regress directly against pH when the derived variable is hydrogen-ion concentration.
- Do not estimate fitted coefficients from endpoints or use answer choices as regression targets.
- Do not treat numerical proximity as valid rounding equivalence.
