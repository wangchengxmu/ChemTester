---
name: chem-analytical-quantitation
description: "Use for standardization, back titration, concentration and amount conversions, purification accounting, extraction stoichiometry, or assay specificity. Not for NMR structure assignment or protein workflow selection."
---

# Analytical Quantitation

## Workflow

1. Define the measurand, aliquot, dilution chain, stoichiometric reaction, blank, and calibration or standardization dependency.
2. Track phase transfer, recovery, interfering species, and which chemical response the assay actually measures.
3. Carry units and uncertainty through the balance; render the requested quantity without converting a calculation into an unsupported identity or selectivity claim.

## Load Only Relevant Procedures

Open the matching reference below only when its applicability fits the task.
Use another skill for a separate subproblem; do not load this entire library by default.

- [Coupled back-titration and cross-standardization balance](references/coupled_back_titration_standardization_balance.md): A back-titration uses one unknown reagent concentration while a separate standardization relates that concentration to another unknown titrant concentration.
- [Answer representation, scaling, tolerance adjudication, and provenance](references/answer_output_representation_and_provenance.md): A quantitative chemistry multiple-choice problem provides numeric choices, an explicit error or rounding tolerance, or a catch-all choice.
- [Purification feasibility by speciation, phase, and unit-operation audit](references/purification_phase_and_byproduct_audit.md): A purification or separation claim depends on whether reagents cause redox, complexation, dissolution, precipitation, or transfer between phases.
- [Verify reaction-based assay applicability before transferring stoichiometry](references/reaction_based_assay_scope_verification.md): A titrimetric or derivatization assay asks whether a structurally related analyte can be measured by the same reaction and conditions.
- [Dimeric acidic-extractant stoichiometry and precision audit](references/dimeric_acidic_extractant_stoichiometry.md): Liquid-liquid extraction data at two or more extractant concentrations and acidities must be used to infer a neutral metal complex, write the extraction reaction, calculate its equilibrium constant, or audit numbered statements.

## Optional Calculators

Read [calculator scope and availability](references/calculators.md) only if a numerical or structural operation would help.
Select and invoke a documented function yourself. No dispatcher, model router, or automatic tool loop is required.

## Evidence And Output

- Start from the user's actual structures, conditions, and requested quantity. If evidence is missing, ask for it or state a bounded assumption.
- Treat these procedures as conditional reasoning aids, not authority over the current evidence. Preserve equations, units, scope, and uncertainty.
- A successful calculator call is not independent scientific validation. Verify consequential empirical constants, safety claims, and exceptional chemistry against authoritative sources.
- Do not read benchmark answers, previous predictions, or evaluation logs to answer a question. Keep the model answer separate from a benchmark key and scientific adjudication.
- Missing optional references are a support limitation, not evidence that a reasoned answer is wrong. Do not invent the missing source.
