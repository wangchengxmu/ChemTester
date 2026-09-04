# Organic Chemistry

## Concept Overview

Organic chemistry studies carbon-containing compounds and their reactions.

## Key Principles

### Functional Groups
| Type | Structure | Suffix |
|------|-----------|--------|
| Alcohol | -OH | -ol |
| Aldehyde | -CHO | -al |
| Ketone | C=O | -one |
| Carboxylic acid | -COOH | -oic acid |
| Amine | -NH₂ | -amine |

### Hydrocarbons
- Alkanes: CₙH₂ₙ₊₂ (single bonds)
- Alkenes: CₙH₂ₙ (double bonds)
- Alkynes: CₙH₂ₙ₋₂ (triple bonds)

## Links

- **L3 Tools**: `../L3_functions/organic_chemistry_tools.py`
- **L4 Reference**: Functional group tables
- **L5 Examples**: Naming problems

## L3 Tool Call Directives


**Source:** `bioinorganic_chemistry_tools.py`

L3 tool module for bioinorganic chemistry tools

### Available functions:
- `carbonic_anhydrase_turnover(co2_concentration: float, enzyme_concentration: float, k_cat: float, K_m: float, time_seconds: float)` → dict — Calculate carbonic anhydrase activity from CO2 hydration rates.
- `zinc_water_pka(ligand_field: str, metal_charge: int)` → dict — Calculate pKa of Zn-bound water from ligand field.
- `zinc_binding_constant(inhibition_data: Dict[str, float])` → dict — Calculate Zn2+ affinity from inhibition data.
- `calcium_equilibrium_potential(ca_out: float, ca_in: float, temperature: float)` → dict — Calculate Ca2+ equilibrium potential from concentration gradient.
- `calmodulin_saturation(ca_free: float, K_d: float, hill_n: float)` → dict — Calculate fractional saturation of calmodulin.
- `ca_atpase_rate(ca_concentration: float, V_max: float, K_m: float)` → dict — Calculate Ca2+-ATPase activity from ATP hydrolysis rates.
- `oxygen_saturation_hill(pO2: float, P50: float, hill_n: float)` → dict — Calculate O2 saturation from Hill equation.
- `bohr_effect_shift(pH_initial: float, pH_final: float, P50_initial: float, bohr_coeff: float)` → dict — Calculate P50 change with pH (Bohr effect).
- `co_poisoning_effect(co_hb_fraction: float, heme_total: float)` → dict — Predict O2 saturation reduction from CO-Hb level.
- `oxygen_reduction_potential(reduction_step: str)` → dict — Calculate E for each O2 reduction step.
- `sod_activity_rate(sod_concentration: float, o2_radical_concentration: float, k_cat: float)` → dict — Calculate SOD rate from concentration.
- `fenton_reaction_rate(fe2_concentration: float, h2o2_concentration: float, k: float)` → dict — Calculate *OH production rate from Fenton reaction.
- `marcus_et_rate(delta_G: float, lambda_reorg: float, distance: float, beta: float, k0: float, temperature: float)` → dict — Calculate electron transfer rate from Marcus equation.
- `et_distance_decay(distance: float, beta: float, reference_rate: float, reference_distance: float)` → dict — Calculate rate from distance and beta.
- `nitrogenase_atp_cost(n2_moles: float, atp_per_n2: float)` → dict — Calculate ATP required for N2 fixation.
- `hydrogen_evolution_rate(hydrogenase_concentration: float, substrate_concentration: float, k_cat: float, K_m: float)` → dict — Calculate H2 production from hydrogenase.
- `fe_s_redox_potential(cluster_type: str, oxidation_state: int, protein_environment: str)` → dict — Calculate cluster potential from composition.
- `dna_binding_constant(free_dna: float, free_metal: float, bound_complex: float)` → dict — Calculate DNA binding constant from titration data.
- `melting_temp_shift(tm_alone: float, tm_complex: float, binding_constant: float)` → dict — Calculate DeltaT_m from metal binding.
- `zinc_finger_affinity(folded_fraction: float, zn_free: float)` → dict — Calculate Zn2+ binding affinity for zinc finger.
- `cisplatin_aquation_rate(chloride_concentration: float, pH: float, temperature: float)` → dict — Calculate rate of cisplatin activation.
- `chelator_affinity(metal: str, chelator: str)` → dict — Calculate K_f for metal-chelator complexes.
- `radioactivity_decay(initial_activity: float, half_life_hours: float, elapsed_hours: float)` → dict — Calculate activity after time t.
- `chelation_selectivity(chelator: str, target_metal: str, competing_metal: str)` → dict — Compare chelator affinity for different metals.
- `get_module_status()` → dict — Return status of all functions in this module.

### Common errors:
- ❌ Passing wrong parameter types (strings where numbers expected)
- ❌ Forgetting required parameters
