# Thermochemistry, Electronic Configuration, Nitrate, and Screening Support

Use this note for chemistry questions that need short, general support rather than a problem-specific lookup. Do not use it as an answer-key table: choose from the visible options by applying the rule, not by memorizing a source row.

## Reversible isothermal heat and entropy

For reversible isothermal heat transfer to or from a reservoir, block, bath, or other body held at one temperature:

- `Delta S = q_rev / T`.
- Convert heat to joules before using SI entropy units.
- Convert Celsius to kelvin: `T(K) = T(C) + 273.15`.
- The sign follows the heat flow for the object whose entropy change is requested: heat added gives positive `Delta S`, heat removed gives negative `Delta S`.

## Ground-state electronic configurations

Use atomic number and the Aufbau order for neutral atoms unless an ion is explicitly requested: `1s, 2s, 2p, 3s, 3p, 4s, 3d, 4p`. Orbital capacities are `s=2`, `p=6`, `d=10`, and `f=14`. Third-period halogens have a neon core followed by `3s^2 3p^5`; reject options that overfill a p subshell or stop before the third shell when the atom has more than ten electrons.

For a ground-state electronic configuration multiple-choice or option letter chemistry reference question, compare every visible configuration against the electron count and subshell capacities. Chlorine is a third-period halogen, so its neutral atom configuration should fill through the 3p subshell without exceeding six p electrons.

## Nitrate and nitrite chemistry

Nitrate salts and nitric-acid-derived nitrate compounds are commonly used as oxidizing agents because nitrogen is in a high oxidation state and can accept electrons under suitable conditions. Do not classify ordinary nitrate use as reducing-agent behavior.

For a common industrial use question about nitrate compounds, first check whether the visible choices include oxidizing-agent behavior. Nitrate and nitrite compounds are associated with oxidation chemistry; polymer initiation, bleaching, or reducing-agent answers need separate context.

Nitrate and nitrite exposure can disrupt oxygen transport through nitrite-mediated oxidation of hemoglobin iron to methemoglobin. This is an oxygen-carrying problem, not primarily a nerve-damage, liver/kidney, or generic-fatigue mechanism unless the question gives a different compound-specific context.

For nitrate/nitrite toxicity questions, look for oxygen transport, methemoglobinemia, or hemoglobin oxidation among the visible options.

## Early virtual-screening preference

For an early virtual-screening prompt that explicitly limits the choice to simple oral-availability and small-molecule-profile factors, compare the visible structures or SMILES for broad descriptors:

- Compare molecular weight, lipophilicity, polar surface area, hydrogen bonding, flexibility and ionization together under the same descriptor and protonation conventions. Smaller or less polar is not universally better: solubility and permeability can trade off.
- Use drug-likeness thresholds as coarse screens, not monotonic optimization targets. Salt form and macrocyclic topology need context rather than a blanket penalty. Confirm parsing before using descriptors; legitimate counts and surface areas may be zero, and cLogP may be negative.
- Do not infer target potency, safety or measured clinical bioavailability from generic descriptors alone. State which measured or estimated dimensions favor each candidate and which remain unknown.
- Do not choose by option order. If the prompt provides only a subjective preference without enough structural contrast, treat the source as weak rather than inventing a hidden scoring rule.
