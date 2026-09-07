# Particle-balance ionization from colligative data

**Retrieve with:** van't Hoff factor percent ionization, freezing point depression weak acid, partial dissociation particle balance, polyprotic acid sequential ionization

**Use when:** A freezing-point, boiling-point, or osmotic measurement is used to infer the fraction or percentage of a weak electrolyte that ionizes or dissociates.

## Procedure

1. Compute solute molality from moles per kilogram of solvent and use the positive magnitude of the colligative change.
2. Infer the observed van't Hoff factor from deltaTf/(Kf*m), deltaTb/(Kb*m), or osmotic pressure/(MRT), then check its physical range.
3. Write the ionization event actually being measured, count nu product particles per ionized formula unit, and use i = (1-alpha) + nu*alpha = 1 + alpha*(nu-1).
4. Solve alpha = (i-1)/(nu-1); for one sequential weak-acid ionization, nu = 2 even when the parent acid has additional ionizable protons.
5. Convert alpha to percent, round only at the end, and verify by reconstructing both i and the measured colligative change.

## Preferred Support

- chem-memory/L2_principles/colligative_properties.md
- chem-memory/L2_principles/acid_base_constants.md

## Guards

- Do not equate the number of acidic protons with nu unless complete simultaneous dissociation is explicit.
- If several sequential ionizations materially contribute, one measured i constrains only the average particle increase and cannot uniquely recover every stepwise fraction.
- Use kilograms of solvent rather than solution mass when calculating molality.
- Require 0 <= alpha <= 1 and back-substitute into the original colligative equation.
