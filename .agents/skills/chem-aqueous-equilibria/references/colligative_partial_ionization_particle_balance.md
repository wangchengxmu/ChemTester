# Particle-balance ionization from colligative data

## Applicability

A freezing-point, boiling-point, or osmotic measurement is used to infer the fraction or percentage of a weak electrolyte that ionizes or dissociates.

## Procedure

1. Compute solute molality from moles per kilogram of solvent and use the positive magnitude of the colligative change.
2. Infer the observed van't Hoff factor from deltaTf/(Kf*m), deltaTb/(Kb*m), or osmotic pressure/(MRT), then check its physical range.
3. Write the ionization event actually being measured, count nu product particles per ionized formula unit, and use i = (1-alpha) + nu*alpha = 1 + alpha*(nu-1).
4. Solve alpha = (i-1)/(nu-1); for one sequential weak-acid ionization, nu = 2 even when the parent acid has additional ionizable protons.
5. Convert alpha to percent, round only at the end, and verify by reconstructing both i and the measured colligative change.

## Boundaries

- Do not equate the number of acidic protons with nu unless complete simultaneous dissociation is explicit.
- If several sequential ionizations materially contribute, one measured i constrains only the average particle increase and cannot uniquely recover every stepwise fraction.
- Use kilograms of solvent rather than solution mass when calculating molality.
- Require 0 <= alpha <= 1 and back-substitute into the original colligative equation.

Only calculators listed in this package's calculator reference are callable here.
Other filenames in a procedure are historical pointers, not installed dependencies.
For missing empirical support, obtain an authoritative source or state the uncertainty.
