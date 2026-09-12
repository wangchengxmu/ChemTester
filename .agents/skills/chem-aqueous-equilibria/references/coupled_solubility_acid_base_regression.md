# Coupled solubility, precipitation, and acid-base regression

## Applicability

Solubility or precipitation is coupled to pH, buffering, protonation, or complexation, including threshold precipitation calculations and multi-point measurements used to recover equilibrium constants.

## Procedure

1. Write the solubility product, relevant acid-base equilibria, stoichiometric exponents, and mass balances together; distinguish free-ion concentrations from total dissolved concentration.
2. For threshold precipitation, use the target free-metal concentration to obtain the required hydroxide concentration, convert to pH or pOH, solve the buffer ratio, and then apply final volume and molar mass to the requested reagent amount.
3. For multi-point solubility data, derive the transformed model before fitting. Only for a 1:1 salt with a single anion-protonation equilibrium, no common-ion contribution or competing complexation, and negligible activity-coefficient effects, use s^2 = Ksp * (1 + [H+]/Ka), where s is total dissolved salt and [H+] is the equilibrium free concentration. The intercept is Ksp and slope is Ksp/Ka. Otherwise solve the full coupled balances rather than imposing this linear form.
4. Transform observations without premature rounding, compute centered-sum ordinary least squares, recover physical constants algebraically, and check positivity, residual quality, and limiting behavior.
5. Retain guard digits and accept a printed numerical choice only when the unrounded result lies within its displayed rounding interval; evaluate underlying statements independently before selecting a multiple-correct response.

## Boundaries

- Respect every stoichiometric exponent in the solubility product.
- Do not replace a free-ion concentration with total solubility when protonation or complexation is present.
- Do not mix pre-dilution and final-volume concentration bases.
- Do not regress directly against pH when the derived variable is hydrogen-ion concentration.
- Do not estimate fitted coefficients from endpoints or use answer choices as regression targets.
- Do not treat numerical proximity as valid rounding equivalence.

Only calculators listed in this package's calculator reference are callable here.
Other filenames in a procedure are historical pointers, not installed dependencies.
For missing empirical support, obtain an authoritative source or state the uncertainty.
