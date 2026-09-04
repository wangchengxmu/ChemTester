# ChemTester Compact Chemistry Skill

Use this guide as a high-signal entrance into local chemistry knowledge and tools.
When an entry applies, search its linked detail document before using the procedure.
Irrelevant retrieval must not override sound chemistry reasoning.

## Core Workflow

1. Inspect the full question, units, answer surface, and any companion vision evidence.
2. Decide whether local support would materially reduce uncertainty. Do not call tools merely to increase tool-use counts.
3. For exact calculations, search tools by operation and named inputs; call only a matching documented tool and verify units.
4. For named concepts, properties, mechanisms, or reference facts, search knowledge with a short concept-specific query.
5. If support is missing or irrelevant, stop retrieval and solve from chemistry reasoning instead of forcing weak context.
6. Treat tool or knowledge output as candidate evidence, not authority: verify argument roles, units, physical bounds, and consistency with the derivation before using it.
7. For online routes, preserve the model's explicit final answer after evidence adjudication; an unrequested parser or conflicting tool result must not overwrite it.
8. Preserve the requested final-answer format and keep answer provenance auditable.

## Verified Gap Skill Index

### Addition-mechanism selectivity disambiguation
**Use when:** An organic addition question asks why one product is observed or compares concertedness, stereospecificity, syn/anti addition, rearrangement...
**Details:** `L2_principles/chemtester_gap_skills/addition_mechanism_selectivity_disambiguation.md`
**Search:** hydroboration concerted transition state

### Answer representation, scaling, tolerance adjudication, and provenance
**Use when:** A quantitative chemistry multiple-choice problem provides numeric choices, an explicit error or rounding tolerance, or a catch-all choice.
**Details:** `L2_principles/chemtester_gap_skills/answer_output_representation_and_provenance.md`
**Search:** numeric option tolerance

### Positional substituent effects on aromatic carbonyl IR
**Use when:** Comparing carbonyl stretching frequencies among regioisomeric aromatic aldehydes or ketones bearing the same ring substituent.
**Details:** `L2_principles/chemtester_gap_skills/aromatic_carbonyl_ir_positional_effects.md`
**Search:** aromatic aldehyde IR substituent position

### Atomic spectroscopy model-limit discrimination
**Use when:** A conceptual atomic-spectroscopy question asks which missing feature of a model explains an observed spectral limitation, especially in...
**Details:** `L2_principles/chemtester_gap_skills/atomic_spectroscopy_model_limit_discrimination.md`
**Search:** Bohr model limitations

### Cannizzaro eligibility with competing carbonyl pathways
**Use when:** Counting or classifying aldehydes that can undergo Cannizzaro chemistry, especially α-branched or multifunctional carbonyl structures.
**Details:** `L2_principles/chemtester_gap_skills/cannizzaro_eligibility_competing_pathways.md`
**Search:** Cannizzaro alpha hydrogen exceptions

### Exact-scope verification of chemical application claims
**Use when:** A qualitative or multi-select chemistry question asks whether a named substance is used for a stated process, target, commodity, facility, or...
**Details:** `L2_principles/chemtester_gap_skills/chemical_application_scope_verification.md`
**Search:** exact chemical use claim

### Compound-specific toxicity within broad chemical classes
**Use when:** A qualitative toxicology question compares broad chemical families or asks whether every member of a class shares one toxicity level.
**Details:** `L2_principles/chemtester_gap_skills/class_level_toxicity_scope_control.md`
**Search:** chemical class toxicity variability

### Particle-balance ionization from colligative data
**Use when:** A freezing-point, boiling-point, or osmotic measurement is used to infer the fraction or percentage of a weak electrolyte that ionizes or dissociates.
**Details:** `L2_principles/chemtester_gap_skills/colligative_partial_ionization_particle_balance.md`
**Search:** van't Hoff factor percent ionization

### Phase-aware metal-ligand and redox speciation
**Use when:** An inorganic reaction or equation-selection problem requires product identification, balancing, coefficient-derived quantities, or exact...
**Details:** `L2_principles/chemtester_gap_skills/competing_complex_speciation.md`
**Search:** phase-aware reaction equation

### Competitive ITC affinity identifiability
**Use when:** An ITC displacement or competition problem asks for an intrinsic binding constant from a fitted affinity measured in the presence of another ligand.
**Details:** `L2_principles/chemtester_gap_skills/competitive_itc_affinity_identifiability.md`
**Search:** competitive ITC apparent affinity

### Separate conformational access from conditional binding stabilization
**Use when:** A medicinal-chemistry comparison asks how cyclization or scaffold rigidity affects conformational access, productive recognition, affinity...
**Details:** `L2_principles/chemtester_gap_skills/conformational_rigidity_binding_stage_separation.md`
**Search:** ligand rigidity bioactive conformation

### Coordination-complex composition, topology, and stereochemical symmetry audit
**Use when:** A mono- or polynuclear coordination-complex problem asks about composition or reaction balance, donor geometry or orbital types, chelate-ring...
**Details:** `L2_principles/chemtester_gap_skills/coordination_salt_composition_symmetry_speciation.md`
**Search:** polynuclear coordination stereochemistry

### Immediate response to corrosive chemical exposure
**Use when:** A visible option set asks for the first response to acid, alkali, caustic, or other corrosive contact with skin or eyes.
**Details:** `L2_principles/chemtester_gap_skills/corrosive_exposure_first_aid.md`
**Search:** corrosive skin eye exposure first aid

### Coupled back-titration and cross-standardization balance
**Use when:** A back-titration uses one unknown reagent concentration while a separate standardization relates that concentration to another unknown titrant...
**Details:** `L2_principles/chemtester_gap_skills/coupled_back_titration_standardization_balance.md`
**Search:** coupled back titration

### Coupled real-gas equilibrium and ideal-model error analysis
**Use when:** Use when an equilibrium composition, remaining phase, or reaction extent at fixed total pressure must be compared between ideal-gas and...
**Details:** `L2_principles/chemtester_gap_skills/coupled_real_gas_equilibrium_error_analysis.md`
**Search:** van der Waals reaction equilibrium

### Coupled solubility, precipitation, and acid-base regression
**Use when:** Solubility or precipitation is coupled to pH, buffering, protonation, or complexation, including threshold precipitation calculations and...
**Details:** `L2_principles/chemtester_gap_skills/coupled_solubility_acid_base_regression.md`
**Search:** metal hydroxide Ksp buffer

### Diastereotopic methylene protons and NMR multiplicity
**Use when:** A proton-NMR or structure problem contains a CH2 near a stereogenic element, asks whether its two hydrogens are equivalent, or asks for their...
**Details:** `L2_principles/chemtester_gap_skills/diastereotopic_methylene_nmr.md`
**Search:** diastereotopic methylene protons

### Diazonium salt isolation and temperature-role safety
**Use when:** A diazonium-safety or synthesis question asks for a temperature limit, especially when preparation, operation, handling, and decomposition...
**Details:** `L2_principles/chemtester_gap_skills/diazonium_salt_isolation_safety.md`
**Search:** diazonium salt heating ceiling

### Diels-Alder bridged-product face and descriptor audit
**Use when:** A Diels-Alder product choice requires connectivity, endo or exo assignment, or named and R/S-defined stereochemistry for a bridged adduct...
**Details:** `L2_principles/chemtester_gap_skills/diels_alder_bridged_stereochemistry.md`
**Search:** Diels-Alder absolute stereochemistry

### Dimeric acidic-extractant stoichiometry and precision audit
**Use when:** Liquid-liquid extraction data at two or more extractant concentrations and acidities must be used to infer a neutral metal complex, write the...
**Details:** `L2_principles/chemtester_gap_skills/dimeric_acidic_extractant_stoichiometry.md`
**Search:** dimeric acidic extractant slope analysis

### Direction-aware empirical activation-energy estimation
**Use when:** An empirical activation-energy rule is qualified by reaction direction or exothermicity, especially when the requested elementary radical step is...
**Details:** `L2_principles/chemtester_gap_skills/direction_aware_empirical_activation_energy.md`
**Search:** endothermic radical activation energy

### Early virtual-screening whole-profile comparison
**Use when:** Comparing molecular structures using generic oral-availability, drug-likeness, or small-molecule profile cues without target-specific potency data.
**Details:** `L2_principles/chemtester_gap_skills/early_virtual_screening_profile_comparison.md`
**Search:** matched SMILES descriptors

### Empirical compatibility-table hazard disambiguation
**Use when:** A safety question asks for empirical hazard categories produced by pairing broad chemical reactivity classes, especially legacy EPA...
**Details:** `L2_principles/chemtester_gap_skills/empirical_compatibility_table_disambiguation.md`
**Search:** EPA hazardous waste compatibility chart

### Equilibrium-Limited Catalytic Conversion Triage
**Use when:** A reversible catalytic reaction gives the same outlet composition after catalyst loading or catalyst-composition changes, and proposed remedies...
**Details:** `L2_principles/chemtester_gap_skills/equilibrium_limited_catalytic_conversion.md`
**Search:** equilibrium-limited reactor conversion

### Evidence-ranked transformation balance and aromaticity checks
**Use when:** A structure or reaction question compares HX-release stoichiometry, aromatization, or π-electron claims after ring opening, elimination, or...
**Details:** `L2_principles/chemtester_gap_skills/evidence_ranked_structural_aromaticity_check.md`
**Search:** gem-dihalocyclopropane aromatization

### Exact tabulated periodic-property disambiguation
**Use when:** An element-ranking or multiple-choice task depends on an exact named periodic-property scale, especially for transition metals or candidate ties.
**Details:** `L2_principles/chemtester_gap_skills/exact_tabulated_periodic_property_disambiguation.md`
**Search:** Pauling electronegativity values

### Explosive performance metric role disambiguation
**Use when:** A conceptual energetic-materials task asks which quantities characterize general detonation performance or contrasts detonation-front...
**Details:** `L2_principles/chemtester_gap_skills/explosive_performance_metric_role_disambiguation.md`
**Search:** secondary explosive performance metrics

### F-block scorpionate condition and coordination audit
**Use when:** An f-block coordination problem combines an element-identification clue, a poly(pyrazolyl)borate reagent, reaction conditions, and a requested...
**Details:** `L2_principles/chemtester_gap_skills/f_block_scorpionate_condition_speciation.md`
**Search:** f-block scorpionate complex

### Exact finite rectangular-barrier transmission
**Use when:** A particle-transmission calculation specifies a finite rectangular barrier, especially when the barrier is thin, the particle energy is near the...
**Details:** `L2_principles/chemtester_gap_skills/finite_rectangular_barrier_transmission.md`
**Search:** finite rectangular barrier transmission

### Fixed-volume real-gas enthalpy change
**Use when:** A closed real gas at fixed amount and volume receives heat or changes temperature and the requested quantity is enthalpy rather than internal energy.
**Details:** `L2_principles/chemtester_gap_skills/fixed_volume_real_gas_enthalpy.md`
**Search:** fixed volume van der Waals enthalpy

### Fractional-coordinate polyhedron metric reconstruction
**Use when:** A crystal-structure problem gives fractional coordinates or layered symmetry, a distorted-polyhedron angle, and asks for a lattice parameter or...
**Details:** `L2_principles/chemtester_gap_skills/fractional_coordinate_polyhedron_metrics.md`
**Search:** fractional coordinate bond angle

### Quantitative halogen isotope-envelope comparison
**Use when:** A mass-spectrum problem infers counts of chlorine, bromine, or other two-isotope atoms from reported M, M+2, M+4, or higher cluster intensities.
**Details:** `L2_principles/chemtester_gap_skills/halogen_isotope_envelope_comparison.md`
**Search:** halogen isotope envelope

### Heme toxicant target and oxidation-state scope
**Use when:** A qualitative chemistry or toxicology question compares ligand binding, oxidation, denaturation, or no interaction across hemoglobin states and...
**Details:** `L2_principles/chemtester_gap_skills/heme_toxicant_target_and_oxidation_state_scope.md`
**Search:** heme toxicant oxidation state

### Heteronuclear and long-range coupling in proton NMR multiplicity
**Use when:** A proton-NMR multiplicity problem contains fluorine, phosphorus, or another spin-active heteronucleus, especially when a signal appears to lack...
**Details:** `L2_principles/chemtester_gap_skills/heteronuclear_proton_nmr_multiplicity.md`
**Search:** proton fluorine NMR coupling

### Inorganic Gas Trap Stoichiometry
**Use when:** Gas-analysis or inorganic decomposition tasks pass products through drying, carbon dioxide absorption, red-hot copper, or STP volume and pressure...
**Details:** `L2_principles/chemtester_gap_skills/inorganic_gas_trap_stoichiometry.md`
**Search:** inorganic gas drying absorbent red hot copper stoichiometry

### Constraint-first inorganic reaction and coefficient audit
**Use when:** An inorganic reaction or multi-process equation-selection problem requires product identification, balancing, coefficient-derived statements, or...
**Details:** `L2_principles/chemtester_gap_skills/inorganic_reaction_constraint_ledger.md`
**Search:** inorganic process equation audit

### Low-template PCR directional outcome screening
**Use when:** Use for qualitative PCR or amplification questions that vary starting-template amount and ask for an expected or least-expected outcome.
**Details:** `L2_principles/chemtester_gap_skills/low_template_pcr_directional_outcome_screening.md`
**Search:** low-template PCR effects

### Matched acid and counteranion trend audit
**Use when:** A matched substituent series compares both Brønsted acidity and coordination or ion-pairing of the corresponding conjugate anions, especially with...
**Details:** `L2_principles/chemtester_gap_skills/matched_acid_counteranion_trend_audit.md`
**Search:** matched acid conjugate-base trend

### Mercury toxicology by species, latency, and endpoint type
**Use when:** A mercury toxicology question asks which clinical effect best matches an exposure form, route, duration, latency, or endpoint type.
**Details:** `L2_principles/chemtester_gap_skills/mercury_toxicology_speciation_timecourse.md`
**Search:** mercury species toxic effects

### Michael Enolate Product Pair Matching
**Use when:** A reaction asks for ordered major products from enolate conjugate addition or a Michael-type pair using visible structures or names.
**Details:** `L2_principles/chemtester_gap_skills/michael_enolate_product_pair_matching.md`
**Search:** Michael addition enolate product pair

### Monatomic ideal-gas absolute molar entropy
**Use when:** A monatomic ideal gas absolute entropy is requested from temperature, pressure or volume, and particle or molar mass.
**Details:** `L2_principles/chemtester_gap_skills/monatomic_ideal_gas_entropy.md`
**Search:** Sackur Tetrode molar entropy

### Water-assisted N-aryl ketonitrone–alkyne cascade mapping
**Use when:** An N-aryl alpha,beta-unsaturated ketonitrone reacts with an electron-poor alkyne and candidate products share global formula or ring-count...
**Details:** `L2_principles/chemtester_gap_skills/n_aryl_ketonitrone_activated_alkyne_cascade.md`
**Search:** N-aryl unsaturated ketonitrone activated alkyne

### Natural toxin process-fate and mechanism audit
**Use when:** A qualitative or multi-select toxicology question asks whether a natural protein toxin remains in a processed oil, is inactivated during...
**Details:** `L2_principles/chemtester_gap_skills/natural_toxin_process_fate_and_mechanism.md`
**Search:** plant protein toxin oil extraction

### Nitrate/nitrite chemistry and dual-mechanism toxicity
**Use when:** A nitrate or nitrite question asks about chemical role, toxicity mechanism, or a symptom pattern that may combine impaired oxygen transport with...
**Details:** `L2_principles/chemtester_gap_skills/nitrate_nitrite_oxidizer_toxicity.md`
**Search:** nitrite toxicity symptoms

### Nitro-Activated Aromatic Substitution Site Triage
**Use when:** A strong nucleophile reacts with a nitro-substituted arene containing multiple plausible leaving groups or another base-sensitive linkage.
**Details:** `L2_principles/chemtester_gap_skills/nitroactivated_aromatic_substitution_site_triage.md`
**Search:** nitro activated SNAr hydroxide

### NMR experiment selection by nucleus and diagnostic contrast
**Use when:** An NMR planning or multiple-choice task asks which experiment best distinguishes structures differing in stereochemistry, substitution, or a...
**Details:** `L2_principles/chemtester_gap_skills/nmr_experiment_selection_by_information_channel.md`
**Search:** NMR experiment selection

### Nucleophile-initiated strained-ring propagation versus quenched addition
**Use when:** A qualitative reactivity or compatibility question pairs a nucleophile or base with an epoxide or another strained heterocyclic monomer and asks...
**Details:** `L2_principles/chemtester_gap_skills/nucleophile_strained_ring_initiation_disambiguation.md`
**Search:** epoxide nucleophilic ring opening polymerization

### Organic nitro-subclass oxidizer and hazard comparison
**Use when:** A question compares oxidizing strength or incompatibility hazards among organic nitro subclasses, especially simple nitroalkanes and nitroaromatic...
**Details:** `L2_principles/chemtester_gap_skills/organic_nitro_oxidizer_hazard_comparison.md`
**Search:** nitroalkane oxidizing strength

### Separate electrode equilibrium from kinetic onset and overpotential
**Use when:** An electrode-reaction problem compares equilibrium, onset, applied potential, overpotential, catalyst activity, or reaction rate across surfaces...
**Details:** `L2_principles/chemtester_gap_skills/oxygen_redox_thermodynamics_kinetics_separation.md`
**Search:** equilibrium versus onset potential

### Peroxide-former recognition, concentration hazards, and response
**Use when:** A safety or mechanism question links air exposure, evaporation, purification, or distillation to explosion, especially for oximes or other...
**Details:** `L2_principles/chemtester_gap_skills/peroxide_former_visible_degradation_response.md`
**Search:** aldoxime peroxide hazard

### Peroxo-crystal speciation and TGA closure
**Use when:** A crystalline inorganic peroxide or peroxosalt identity, component ratio, or statement set must be inferred from preparation, ionic and neutral...
**Details:** `L2_principles/chemtester_gap_skills/peroxo_crystal_speciation_tga_closure.md`
**Search:** peroxocarbonate crystal speciation

### Phase-aware release hazard and response selection
**Use when:** A qualitative chemical-safety question asks for the most direct hazard or applicable response associated with gas or vapor accumulation...
**Details:** `L2_principles/chemtester_gap_skills/phase_aware_release_response_selection.md`
**Search:** confined-space gas hazard

### Stagewise phosphorus stereochemistry and 31P NMR environment counting
**Use when:** A reaction-monitoring or structure question asks how proton-decoupled phosphorus NMR signal counts change as substituents at tetrahedral...
**Details:** `L2_principles/chemtester_gap_skills/phosphorus_nmr_stagewise_environment_counting.md`
**Search:** phosphorus stereogenicity 31P NMR

### Photophysics Color Energy Direction
**Use when:** A question asks for emitted, observed, or absorbed visible color from photon energy, wavelength, or conjugated-dye wording.
**Details:** `L2_principles/chemtester_gap_skills/photophysics_color_energy_direction.md`
**Search:** photon energy wavelength color

### Condition-coupled spin, electron-configuration, and exact-geometry audit
**Use when:** A coordination or organometallic problem couples electron-count rules, magnetic state, valence-orbital occupation, or an exact geometry claim...
**Details:** `L2_principles/chemtester_gap_skills/pressure_coupled_spin_orbital_geometry.md`
**Search:** four-coordinate exact geometry

### Protein IEX selection from sequence to empirical screening
**Use when:** A protein ion-exchange chromatography problem asks for the starting information, exchanger polarity, matrix-selection sequence, or distinction...
**Details:** `L2_principles/chemtester_gap_skills/protein_iex_selection_workflow_ordering.md`
**Search:** protein IEX matrix selection

### Purification feasibility by speciation, phase, and unit-operation audit
**Use when:** A purification or separation claim depends on whether reagents cause redox, complexation, dissolution, precipitation, or transfer between phases.
**Details:** `L2_principles/chemtester_gap_skills/purification_phase_and_byproduct_audit.md`
**Search:** purification oxidation-state ledger

### Qualitative inorganic reaction-network deduction
**Use when:** Unlabeled aqueous samples, including prepared mixtures, must be identified from linked precipitate, gas, redox, and directed excess-reagent...
**Details:** `L2_principles/chemtester_gap_skills/qualitative_inorganic_constraint_deduction.md`
**Search:** qualitative inorganic reaction constraints

### Qualitative ionic solubility and aqueous causticity screening
**Use when:** Comparing ionic compounds by aqueous solubility, corrosivity, or causticity, especially salts containing a strongly basic anion such as sulfide.
**Details:** `L2_principles/chemtester_gap_skills/qualitative_ionic_solubility_causticity_screening.md`
**Search:** ionic sulfide solubility rules

### Verify reaction-based assay applicability before transferring stoichiometry
**Use when:** A titrimetric or derivatization assay asks whether a structurally related analyte can be measured by the same reaction and conditions.
**Details:** `L2_principles/chemtester_gap_skills/reaction_based_assay_scope_verification.md`
**Search:** reaction assay applicability

### Reaction-center stereochemical descriptor audit
**Use when:** A reaction-product choice depends on enolate E/Z geometry or slash/backslash SMILES, especially when changing among ketone, ester, and amide...
**Details:** `L2_principles/chemtester_gap_skills/reaction_center_stereochemical_descriptor_audit.md`
**Search:** tertiary amide LDA enolate

### Reciprocal-rate axis choice for reactor arrangements
**Use when:** Use when selecting or comparing an arrangement of ideal reactor units from rate plots, especially when candidate methods differ by concentration...
**Details:** `L2_principles/chemtester_gap_skills/reactor_arrangement_reciprocal_rate_axis_disambiguation.md`
**Search:** reactor arrangement reciprocal rate concentration

### Real-gas compressibility model and virial-order selection
**Use when:** A real-gas problem requests a compressibility factor from state data or asks for a virial approximation derived from an equation of state.
**Details:** `L2_principles/chemtester_gap_skills/real_gas_compressibility_state_selection.md`
**Search:** van der Waals virial compressibility

### Atom-scaled redox half-reaction electron ledger
**Use when:** A half-reaction must be balanced in acidic or basic medium, especially when a polyatomic reactant forms a molecular product containing multiple...
**Details:** `L2_principles/chemtester_gap_skills/redox_half_reaction_atom_electron_ledger.md`
**Search:** balance acidic half reaction

### Reversible isothermal heat entropy
**Use when:** Use when a chemistry or physical-chemistry problem asks for entropy change from reversible heat transfer at a specified constant temperature.
**Details:** `L2_principles/chemtester_gap_skills/reversible_isothermal_heat_entropy.md`
**Search:** reversible isothermal heat entropy q over T

### Role-scoped physical quantity binding
**Use when:** A quantitative chemistry problem supplies a concentration that could denote molecules, reactive groups, or the concentration variable of an...
**Details:** `L2_principles/chemtester_gap_skills/role_scoped_quantity_binding.md`
**Search:** step-growth polymerization time

### Rate ranking from secondary deuterium isotope effects
**Use when:** Comparing rates of electrophilic addition to isotopologues when the labeled C-H or C-D bonds are not cleaved, especially in rigid or crowded alkenes.
**Details:** `L2_principles/chemtester_gap_skills/secondary_deuterium_isotope_effect_rate_ranking.md`
**Search:** inverse secondary deuterium isotope effect

### Stagewise organic structure tracking to product or proton multiplicity
**Use when:** A multistep organic product or spectroscopy problem combines carbocation rearrangement, elimination or alkene cleavage, and carbonyl cyclization...
**Details:** `L2_principles/chemtester_gap_skills/stagewise_organic_structure_to_proton_multiplicity.md`
**Search:** multistep organic product tracking

### Temperature-shifted carbonate alkalinity and scale limits
**Use when:** A water-scaling or hardness problem changes temperature and couples gas-buffered carbonate speciation to saturation of more than one calcium...
**Details:** `L2_principles/chemtester_gap_skills/temperature_shifted_carbonate_scale_limit.md`
**Search:** boiler hardness carbonate scale

### Unit-cell density and composition constraint triangulation
**Use when:** A crystalline coordination compound or porous framework identity must be inferred from cell parameters, density, Z, elemental ratios, included...
**Details:** `L2_principles/chemtester_gap_skills/unit_cell_density_composition_triangulation.md`
**Search:** crystal density formula mass

### Vibrational partition-function convention and approximation thresholds
**Use when:** Comparing exact and high-temperature harmonic-oscillator vibrational partition functions or finding a temperature at which their percentage...
**Details:** `L2_principles/chemtester_gap_skills/vibrational_partition_approximation_thresholds.md`
**Search:** vibrational partition zero point convention
