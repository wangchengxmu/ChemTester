---
name: chem-aqueous-equilibria
description: "Use for acid-base, buffer, solubility, ionic speciation, colligative ionization, or temperature-dependent carbonate equilibria. Not for general gas thermodynamics or instrumental assay selection."
---

# Aqueous Equilibria

## Workflow

1. Write species, mass balances, charge balance, and equilibrium definitions using compatible activities or stated concentration approximations.
2. Identify the temperature and convention of each constant; do not assume pH + pOH = 14 at every temperature.
3. Solve coupled balances before selecting a limiting approximation, then check positivity, charge closure, and approximation validity.

## Load Only Relevant Procedures

Open the matching reference below only when its applicability fits the task.
Use another skill for a separate subproblem; do not load this entire library by default.

- [Particle-balance ionization from colligative data](references/colligative_partial_ionization_particle_balance.md): A freezing-point, boiling-point, or osmotic measurement is used to infer the fraction or percentage of a weak electrolyte that ionizes or dissociates.
- [Coupled solubility, precipitation, and acid-base regression](references/coupled_solubility_acid_base_regression.md): Solubility or precipitation is coupled to pH, buffering, protonation, or complexation, including threshold precipitation calculations and multi-point measurements used to recover equilibrium constants.
- [Qualitative ionic solubility and aqueous causticity screening](references/qualitative_ionic_solubility_causticity_screening.md): Comparing ionic compounds by aqueous solubility, corrosivity, or causticity, especially salts containing a strongly basic anion such as sulfide.
- [Matched acid and counteranion trend audit](references/matched_acid_counteranion_trend_audit.md): A matched substituent series compares both Brønsted acidity and coordination or ion-pairing of the corresponding conjugate anions, especially with highly electrophilic cations and weakly coordinating cluster anions.
- [Temperature-shifted carbonate alkalinity and scale limits](references/temperature_shifted_carbonate_scale_limit.md): A water-scaling or hardness problem changes temperature and couples gas-buffered carbonate speciation to saturation of more than one calcium, magnesium, carbonate, or hydroxide solid.

## Optional Calculators

Read [calculator scope and availability](references/calculators.md) only if a numerical or structural operation would help.
Select and invoke a documented function yourself. No dispatcher, model router, or automatic tool loop is required.

## Evidence And Output

- Start from the user's actual structures, conditions, and requested quantity. If evidence is missing, ask for it or state a bounded assumption.
- Treat these procedures as conditional reasoning aids, not authority over the current evidence. Preserve equations, units, scope, and uncertainty.
- A successful calculator call is not independent scientific validation. Verify consequential empirical constants, safety claims, and exceptional chemistry against authoritative sources.
- Do not read benchmark answers, previous predictions, or evaluation logs to answer a question. Keep the model answer separate from a benchmark key and scientific adjudication.
- Missing optional references are a support limitation, not evidence that a reasoned answer is wrong. Do not invent the missing source.
