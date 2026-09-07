---
name: chem-toxicology
description: "Use for interpreting chemical toxicology mechanisms, species-specific exposure evidence, toxin process fate, or limits of class-level hazard comparisons. Not for diagnosis, antidote selection, dosing, or individual treatment advice."
---

# Toxicology Evidence

## Workflow

1. Specify chemical species, exposure route, dose context, timing, and endpoint before interpreting a toxicology claim.
2. Distinguish molecular mechanism from clinical diagnosis, and processing conditions from evidence that a toxin was removed.
3. Use current authoritative sources for consequential claims. For a real exposure, refer to poison control or emergency care rather than extrapolating a treatment from mechanism.

## Load Only Relevant Procedures

Open the matching reference below only when its applicability fits the task.
Use another skill for a separate subproblem; do not load this entire library by default.

- [Nitrate/nitrite chemistry and dual-mechanism toxicity](references/nitrate_nitrite_oxidizer_toxicity.md): A nitrate or nitrite question asks about chemical role, toxicity mechanism, or a symptom pattern that may combine impaired oxygen transport with cardiovascular effects.
- [Natural toxin process-fate and mechanism audit](references/natural_toxin_process_fate_and_mechanism.md): A qualitative or multi-select toxicology question asks whether a natural protein toxin remains in a processed oil, is inactivated during processing, or acts through a proposed cellular target.
- [Heme toxicant target and oxidation-state scope](references/heme_toxicant_target_and_oxidation_state_scope.md): A qualitative chemistry or toxicology question compares ligand binding, oxidation, denaturation, or no interaction across hemoglobin states and other hemoprotein targets.
- [Mercury toxicology by species, latency, and endpoint type](references/mercury_toxicology_speciation_timecourse.md): A mercury toxicology question asks which clinical effect best matches an exposure form, route, duration, latency, or endpoint type.
- [Compound-specific toxicity within broad chemical classes](references/class_level_toxicity_scope_control.md): A qualitative toxicology question compares broad chemical families or asks whether every member of a class shares one toxicity level.

## Evidence And Output

- Start from the user's actual structures, conditions, and requested quantity. If evidence is missing, ask for it or state a bounded assumption.
- Treat these procedures as conditional reasoning aids, not authority over the current evidence. Preserve equations, units, scope, and uncertainty.
- A successful calculator call is not independent scientific validation. Verify consequential empirical constants, safety claims, and exceptional chemistry against authoritative sources.
- Do not read benchmark answers, previous predictions, or evaluation logs to answer a question. Keep the model answer separate from a benchmark key and scientific adjudication.
- Missing optional references are a support limitation, not evidence that a reasoned answer is wrong. Do not invent the missing source.
