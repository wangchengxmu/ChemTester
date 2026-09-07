---
name: chem-organic-mechanisms
description: "Use for organic reaction pathways, competing mechanisms, regiochemistry, aromaticity, stereochemical descriptors, or reaction-stage product assignment. Not for standalone spectral peak assignment."
---

# Organic Mechanisms

## Workflow

1. Recover the exact substrate connectivity, reagents, medium, and reaction stage before naming a mechanism.
2. Track atom connectivity and competing pathways; use analogy only after checking its structural and condition requirements.
3. Recompute stereochemical descriptors after the reaction. Distinguish spatial retention/inversion from changes in CIP labels.

## Load Only Relevant Procedures

Open the matching reference below only when its applicability fits the task.
Use another skill for a separate subproblem; do not load this entire library by default.

- [Michael Enolate Product Pair Matching](references/michael_enolate_product_pair_matching.md): A reaction asks for ordered major products from enolate conjugate addition or a Michael-type pair using visible structures or names.
- [Diels-Alder bridged-product face and descriptor audit](references/diels_alder_bridged_stereochemistry.md): A Diels-Alder product choice requires connectivity, endo or exo assignment, or named and R/S-defined stereochemistry for a bridged adduct, including ordinary cyclopentadiene with a monosubstituted electron-poor alkene.
- [Addition-mechanism selectivity disambiguation](references/addition_mechanism_selectivity_disambiguation.md): An organic addition question asks why one product is observed or compares concertedness, stereospecificity, syn/anti addition, rearrangement, regiochemistry, and temperature effects.
- [Evidence-ranked transformation balance and aromaticity checks](references/evidence_ranked_structural_aromaticity_check.md): A structure or reaction question compares HX-release stoichiometry, aromatization, or π-electron claims after ring opening, elimination, or rearrangement, especially for gem-dihalocyclopropane or fused-ring substrates.
- [Cannizzaro eligibility with competing carbonyl pathways](references/cannizzaro_eligibility_competing_pathways.md): Counting or classifying aldehydes that can undergo Cannizzaro chemistry, especially α-branched or multifunctional carbonyl structures.
- [Stagewise organic structure tracking to product or proton multiplicity](references/stagewise_organic_structure_to_proton_multiplicity.md): A multistep organic product or spectroscopy problem combines carbocation rearrangement, elimination or alkene cleavage, and carbonyl cyclization, making the result depend on propagated connectivity and competing ring closures.
- [Nitro-Activated Aromatic Substitution Site Triage](references/nitroactivated_aromatic_substitution_site_triage.md): A strong nucleophile reacts with a nitro-substituted arene containing multiple plausible leaving groups or another base-sensitive linkage.
- [Reaction-center stereochemical descriptor audit](references/reaction_center_stereochemical_descriptor_audit.md): A reaction-product choice depends on enolate E/Z geometry or slash/backslash SMILES, especially when changing among ketone, ester, and amide substrates can change both selectivity and CIP interpretation.
- [Nucleophile-initiated strained-ring propagation versus quenched addition](references/nucleophile_strained_ring_initiation_disambiguation.md): A qualitative reactivity or compatibility question pairs a nucleophile or base with an epoxide or another strained heterocyclic monomer and asks whether the outcome is initiation, propagation, or an isolated ring-opened product.
- [Water-assisted N-aryl ketonitrone–alkyne cascade mapping](references/n_aryl_ketonitrone_activated_alkyne_cascade.md): An N-aryl alpha,beta-unsaturated ketonitrone reacts with an electron-poor alkyne and candidate products share global formula or ring-count constraints but differ in connectivity after a water-assisted seven-membered intermediate.

## Optional Calculators

Read [calculator scope and availability](references/calculators.md) only if a numerical or structural operation would help.
Select and invoke a documented function yourself. No dispatcher, model router, or automatic tool loop is required.

## Evidence And Output

- Start from the user's actual structures, conditions, and requested quantity. If evidence is missing, ask for it or state a bounded assumption.
- Treat these procedures as conditional reasoning aids, not authority over the current evidence. Preserve equations, units, scope, and uncertainty.
- A successful calculator call is not independent scientific validation. Verify consequential empirical constants, safety claims, and exceptional chemistry against authoritative sources.
- Do not read benchmark answers, previous predictions, or evaluation logs to answer a question. Keep the model answer separate from a benchmark key and scientific adjudication.
- Missing optional references are a support limitation, not evidence that a reasoned answer is wrong. Do not invent the missing source.
