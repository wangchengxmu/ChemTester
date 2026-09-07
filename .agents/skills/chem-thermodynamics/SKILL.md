---
name: chem-thermodynamics
description: "Use for gas-state changes, enthalpy, entropy, free energy, real-gas corrections, and equilibrium-limited conversion. Not for kinetic rate fitting or aqueous titration speciation."
---

# Thermodynamics

## Workflow

1. Define system, state variables, process constraints, sign convention, and molar versus total quantities.
2. Choose the equation of state and thermodynamic identity before substituting numbers; retain correction terms until cancellation is shown.
3. Separate equilibrium feasibility from kinetic accessibility. Check limiting cases, units, and state-function closure.

## Load Only Relevant Procedures

Open the matching reference below only when its applicability fits the task.
Use another skill for a separate subproblem; do not load this entire library by default.

- [Fixed-volume real-gas enthalpy change](references/fixed_volume_real_gas_enthalpy.md): A closed real gas at fixed amount and volume receives heat or changes temperature and the requested quantity is enthalpy rather than internal energy.
- [Monatomic ideal-gas absolute molar entropy](references/monatomic_ideal_gas_entropy.md): A monatomic ideal gas absolute entropy is requested from temperature, pressure or volume, and particle or molar mass.
- [Reversible isothermal heat entropy](references/reversible_isothermal_heat_entropy.md): Use when a chemistry or physical-chemistry problem asks for entropy change from reversible heat transfer at a specified constant temperature.
- [Real-gas compressibility model and virial-order selection](references/real_gas_compressibility_state_selection.md): A real-gas problem requests a compressibility factor from state data or asks for a virial approximation derived from an equation of state.
- [Separate electrode equilibrium from kinetic onset and overpotential](references/oxygen_redox_thermodynamics_kinetics_separation.md): An electrode-reaction problem compares equilibrium, onset, applied potential, overpotential, catalyst activity, or reaction rate across surfaces, conditions, or reference scales.
- [Equilibrium-Limited Catalytic Conversion Triage](references/equilibrium_limited_catalytic_conversion.md): A reversible catalytic reaction gives the same outlet composition after catalyst loading or catalyst-composition changes, and proposed remedies use temperature or catalyst changes to raise per-pass conversion.
- [Coupled real-gas equilibrium and ideal-model error analysis](references/coupled_real_gas_equilibrium_error_analysis.md): Use when an equilibrium composition, remaining phase, or reaction extent at fixed total pressure must be compared between ideal-gas and componentwise van der Waals models, especially when inert gases are present.

## Optional Calculators

Read [calculator scope and availability](references/calculators.md) only if a numerical or structural operation would help.
Select and invoke a documented function yourself. No dispatcher, model router, or automatic tool loop is required.

## Evidence And Output

- Start from the user's actual structures, conditions, and requested quantity. If evidence is missing, ask for it or state a bounded assumption.
- Treat these procedures as conditional reasoning aids, not authority over the current evidence. Preserve equations, units, scope, and uncertainty.
- A successful calculator call is not independent scientific validation. Verify consequential empirical constants, safety claims, and exceptional chemistry against authoritative sources.
- Do not read benchmark answers, previous predictions, or evaluation logs to answer a question. Keep the model answer separate from a benchmark key and scientific adjudication.
- Missing optional references are a support limitation, not evidence that a reasoned answer is wrong. Do not invent the missing source.
