---
name: chem-spectroscopy
description: "Use for NMR environments and splitting, IR interpretation, isotope envelopes, optical transition energies, or selecting spectroscopic experiments. Not for bulk analytical standardization or atomic-model theory."
---

# Spectroscopy

## Workflow

1. Identify the observed nucleus, experiment, structure, timescale, solvent, and coupling or exchange assumptions.
2. Count environments and allowed interactions before mapping them to peaks; distinguish chemical equivalence from magnetic equivalence.
3. Use trends as conditional evidence, not unique identification. Report degeneracies, unresolved assignments, and what measurement would discriminate them.

## Load Only Relevant Procedures

Open the matching reference below only when its applicability fits the task.
Use another skill for a separate subproblem; do not load this entire library by default.

- [Photophysics Color Energy Direction](references/photophysics_color_energy_direction.md): A question asks for emitted, observed, or absorbed visible color from photon energy, wavelength, or conjugated-dye wording.
- [Stagewise phosphorus stereochemistry and 31P NMR environment counting](references/phosphorus_nmr_stagewise_environment_counting.md): A reaction-monitoring or structure question asks how proton-decoupled phosphorus NMR signal counts change as substituents at tetrahedral phosphorus are replaced or hydrolyzed.
- [Quantitative halogen isotope-envelope comparison](references/halogen_isotope_envelope_comparison.md): A mass-spectrum problem infers counts of chlorine, bromine, or other two-isotope atoms from reported M, M+2, M+4, or higher cluster intensities.
- [Positional substituent effects on aromatic carbonyl IR](references/aromatic_carbonyl_ir_positional_effects.md): Comparing carbonyl stretching frequencies among regioisomeric aromatic aldehydes or ketones bearing the same ring substituent.
- [Diastereotopic methylene protons and NMR multiplicity](references/diastereotopic_methylene_nmr.md): A proton-NMR or structure problem contains a CH2 near a stereogenic element, asks whether its two hydrogens are equivalent, or asks for their individual multiplicities.
- [NMR experiment selection by nucleus and diagnostic contrast](references/nmr_experiment_selection_by_information_channel.md): An NMR planning or multiple-choice task asks which experiment best distinguishes structures differing in stereochemistry, substitution, or a heteronuclear probe environment.
- [Heteronuclear and long-range coupling in proton NMR multiplicity](references/heteronuclear_proton_nmr_multiplicity.md): A proton-NMR multiplicity problem contains fluorine, phosphorus, or another spin-active heteronucleus, especially when a signal appears to lack neighboring protons or the nuclei are connected by a plausible long-range or constrained close-contact pathway.

## Optional Calculators

Read [calculator scope and availability](references/calculators.md) only if a numerical or structural operation would help.
Select and invoke a documented function yourself. No dispatcher, model router, or automatic tool loop is required.

## Evidence And Output

- Start from the user's actual structures, conditions, and requested quantity. If evidence is missing, ask for it or state a bounded assumption.
- Treat these procedures as conditional reasoning aids, not authority over the current evidence. Preserve equations, units, scope, and uncertainty.
- A successful calculator call is not independent scientific validation. Verify consequential empirical constants, safety claims, and exceptional chemistry against authoritative sources.
- Do not read benchmark answers, previous predictions, or evaluation logs to answer a question. Keep the model answer separate from a benchmark key and scientific adjudication.
- Missing optional references are a support limitation, not evidence that a reasoned answer is wrong. Do not invent the missing source.
