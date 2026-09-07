---
name: chem-biomolecular-analysis
description: "Use for protein ion-exchange workflows, low-template PCR interpretation, competitive ITC identifiability, or early virtual-screening and binding-stage comparisons. Not for clinical diagnosis or unconstrained affinity prediction."
---

# Biomolecular Analysis

## Workflow

1. Identify the experimental stage, observable, controls, sample regime, and intended biological quantity.
2. Distinguish measurement sensitivity and identifiability from mechanistic plausibility; separate binding, conformational reorganization, and downstream effects.
3. Compare candidates on matched assay conditions and supported endpoints. State when sparse observations cannot identify a unique parameter or outcome.

## Load Only Relevant Procedures

Open the matching reference below only when its applicability fits the task.
Use another skill for a separate subproblem; do not load this entire library by default.

- [Protein IEX selection from sequence to empirical screening](references/protein_iex_selection_workflow_ordering.md): A protein ion-exchange chromatography problem asks for the starting information, exchanger polarity, matrix-selection sequence, or distinction between initial design and later optimization.
- [Low-template PCR directional outcome screening](references/low_template_pcr_directional_outcome_screening.md): Use for qualitative PCR or amplification questions that vary starting-template amount and ask for an expected or least-expected outcome.
- [Early virtual-screening whole-profile comparison](references/early_virtual_screening_profile_comparison.md): Comparing molecular structures using generic oral-availability, drug-likeness, or small-molecule profile cues without target-specific potency data.
- [Competitive ITC affinity identifiability](references/competitive_itc_affinity_identifiability.md): An ITC displacement or competition problem asks for an intrinsic binding constant from a fitted affinity measured in the presence of another ligand.
- [Separate conformational access from conditional binding stabilization](references/conformational_rigidity_binding_stage_separation.md): A medicinal-chemistry comparison asks how cyclization or scaffold rigidity affects conformational access, productive recognition, affinity, selectivity, or interaction strength, especially in a negative-polarity multiple-choice task.

## Optional Calculators

Read [calculator scope and availability](references/calculators.md) only if a numerical or structural operation would help.
Select and invoke a documented function yourself. No dispatcher, model router, or automatic tool loop is required.

## Evidence And Output

- Start from the user's actual structures, conditions, and requested quantity. If evidence is missing, ask for it or state a bounded assumption.
- Treat these procedures as conditional reasoning aids, not authority over the current evidence. Preserve equations, units, scope, and uncertainty.
- A successful calculator call is not independent scientific validation. Verify consequential empirical constants, safety claims, and exceptional chemistry against authoritative sources.
- Do not read benchmark answers, previous predictions, or evaluation logs to answer a question. Keep the model answer separate from a benchmark key and scientific adjudication.
- Missing optional references are a support limitation, not evidence that a reasoned answer is wrong. Do not invent the missing source.
