---
name: chem-kinetics-reactors
description: "Use for integrated rate laws, rate-law fitting, isotope-effect rankings, activation-energy direction, or batch/CSTR/PFR comparisons. Not for equilibrium-only conversion or thermodynamic favorability."
---

# Kinetics And Reactors

## Workflow

1. Bind every quantity to its species, experimental stage, and forward or reverse direction.
2. Read rate-plot axes and reactor assumptions explicitly before comparing areas or fitting a model.
3. Check rate units, kinetic order, fit identifiability, and whether an empirical constant is actually supplied; do not substitute thermodynamics for a measured rate.

## Load Only Relevant Procedures

Open the matching reference below only when its applicability fits the task.
Use another skill for a separate subproblem; do not load this entire library by default.

- [Reciprocal-rate axis choice for reactor arrangements](references/reactor_arrangement_reciprocal_rate_axis_disambiguation.md): Use when selecting or comparing an arrangement of ideal reactor units from rate plots, especially when candidate methods differ by concentration versus conversion axes or by sizing versus sequencing purpose.
- [Role-scoped physical quantity binding](references/role_scoped_quantity_binding.md): A quantitative chemistry problem supplies a concentration that could denote molecules, reactive groups, or the concentration variable of an integrated rate law, especially in step-growth kinetics.
- [Rate ranking from secondary deuterium isotope effects](references/secondary_deuterium_isotope_effect_rate_ranking.md): Comparing rates of electrophilic addition to isotopologues when the labeled C-H or C-D bonds are not cleaved, especially in rigid or crowded alkenes.
- [Direction-aware empirical activation-energy estimation](references/direction_aware_empirical_activation_energy.md): An empirical activation-energy rule is qualified by reaction direction or exothermicity, especially when the requested elementary radical step is endothermic but its reverse is exothermic.

## Optional Calculators

Read [calculator scope and availability](references/calculators.md) only if a numerical or structural operation would help.
Select and invoke a documented function yourself. No dispatcher, model router, or automatic tool loop is required.

## Evidence And Output

- Start from the user's actual structures, conditions, and requested quantity. If evidence is missing, ask for it or state a bounded assumption.
- Treat these procedures as conditional reasoning aids, not authority over the current evidence. Preserve equations, units, scope, and uncertainty.
- A successful calculator call is not independent scientific validation. Verify consequential empirical constants, safety claims, and exceptional chemistry against authoritative sources.
- Do not read benchmark answers, previous predictions, or evaluation logs to answer a question. Keep the model answer separate from a benchmark key and scientific adjudication.
- Missing optional references are a support limitation, not evidence that a reasoned answer is wrong. Do not invent the missing source.
