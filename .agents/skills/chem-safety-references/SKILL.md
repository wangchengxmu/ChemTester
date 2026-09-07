---
name: chem-safety-references
description: "Use for interpreting SDS or compatibility evidence, chemical application scope, phase-dependent hazard distinctions, or recognizing unstable-material warning signs. Not for hazardous synthesis optimization, emergency treatment, or authorization to handle or mix chemicals."
---

# Safety Reference Review

## Workflow

1. For actual exposure or unstable material, prioritize emergency services, site safety staff, and current product-specific SDS instructions; do not infer a safe procedure from these notes.
2. Bind every claim to chemical identity, concentration, phase, contact time, material, and source scope. A missing table entry does not establish compatibility.
3. Use these procedures for conceptual discrimination and source interpretation only. Do not optimize energetic formulations, prescribe treatment, or authorize handling from an unverified calculation.

## Load Only Relevant Procedures

Open the matching reference below only when its applicability fits the task.
Use another skill for a separate subproblem; do not load this entire library by default.

- [Immediate response to corrosive chemical exposure](references/corrosive_exposure_first_aid.md): An educational question asks about initial corrosive skin or eye decontamination; the substance and any product-specific instructions must be identified.
- [Peroxide-former recognition, concentration hazards, and response](references/peroxide_former_visible_degradation_response.md): A safety or mechanism question links air exposure, evaporation, purification, or distillation to explosion, especially for oximes or other peroxide-forming organics, and candidate answers mix a broad reaction class with a more specific causal pathway.
- [Empirical compatibility-table hazard disambiguation](references/empirical_compatibility_table_disambiguation.md): A safety question asks for empirical hazard categories produced by pairing broad chemical reactivity classes, especially legacy EPA chemical-storage or hazardous-waste compatibility groups.
- [Diazonium salt isolation and temperature-role safety](references/diazonium_salt_isolation_safety.md): A diazonium-safety or synthesis question asks for a temperature limit, especially when preparation, operation, handling, and decomposition temperatures could be confused.
- [Explosive performance metric role disambiguation](references/explosive_performance_metric_role_disambiguation.md): A conceptual energetic-materials task asks which quantities characterize general detonation performance or contrasts detonation-front, thermochemical, and metal-acceleration metrics.
- [Organic nitro-subclass oxidizer and hazard comparison](references/organic_nitro_oxidizer_hazard_comparison.md): A question compares oxidizing strength or incompatibility hazards among organic nitro subclasses, especially simple nitroalkanes and nitroaromatic compounds.
- [Exact-scope verification of chemical application claims](references/chemical_application_scope_verification.md): A qualitative or multi-select chemistry question asks whether a named substance is used for a stated process, target, commodity, facility, or purpose, especially when historical and current uses may differ.
- [Phase-aware release hazard and response selection](references/phase_aware_release_response_selection.md): A qualitative chemical-safety question asks for the most direct hazard or applicable response associated with gas or vapor accumulation, especially in a confined or poorly ventilated space.

## Optional Calculators

Read [calculator scope and availability](references/calculators.md) only if a numerical or structural operation would help.
Select and invoke a documented function yourself. No dispatcher, model router, or automatic tool loop is required.

## Evidence And Output

- Start from the user's actual structures, conditions, and requested quantity. If evidence is missing, ask for it or state a bounded assumption.
- Treat these procedures as conditional reasoning aids, not authority over the current evidence. Preserve equations, units, scope, and uncertainty.
- A successful calculator call is not independent scientific validation. Verify consequential empirical constants, safety claims, and exceptional chemistry against authoritative sources.
- Do not read benchmark answers, previous predictions, or evaluation logs to answer a question. Keep the model answer separate from a benchmark key and scientific adjudication.
- Missing optional references are a support limitation, not evidence that a reasoned answer is wrong. Do not invent the missing source.
