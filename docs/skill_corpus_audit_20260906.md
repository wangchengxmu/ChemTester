# Whole skill-corpus audit, 2026-09-06

## Decision

Keep the V2.1 120-prediction run on hold. There are confirmed scientific and implementation defects in support that the current runtime can retrieve or execute. Improving routing alone will not remove them. No skill content, runtime code, support policy, historical result, or benchmark question was changed by this audit.

This is a complete structural inventory of the current L2/L3/L4 corpus plus manual review of all 71 active compact capabilities and targeted scientific verification. It is **not** a claim that every equation in every legacy document or every function has been independently validated.

## Coverage and evidence

| Surface | Inspected inventory | Verification performed |
| --- | ---: | --- |
| L2 principles | 847 files: 846 Markdown and one registry | Full structural scan; all 71 active registry procedures/guards reviewed; selected broad notes scientifically checked |
| L3 functions | 226 files, including 217 Python modules | Every Python file AST-parsed; active catalog inspected; targeted synthetic calls |
| L4 references | 107 files: 64 Markdown, 42 CSV, one JSON | Full structural scan; every CSV checked for single-table shape; selected records checked |
| Total | 1,180 files, 9,127,612 bytes | Per-file SHA-256 inventory |
| Current retrieval | 898 documents, 9,801 chunks | Built the actual memory index and searched synthetic topic queries |
| Current executable catalog | 343 functions from 32 modules | Actual CuratedToolCatalog, not an inferred list from filenames |

The catalog also reports 1,699 quarantined functions. Having 217 Python modules on disk does not mean that all 217 are exposed to the model. Likewise, a resource listed in a capability is not necessarily executable or retrievable.

Audit artifacts are in `outputs/chemistry_expert/skill_corpus_audit_20260906/`:

- `structure.json`: every file's size/hash, AST results, link/encoding/placeholder/CSV candidates, and registry/build checks.
- `reachability.json`: indexed paths, registry-resource availability, active-module inventory, and synthetic retrieval results.
- `probes.json`: exact inputs, outputs, errors, and runtime evidence classifications for 11 targeted checks using 12 tool calls.
- `scientific_invariants.json`: analytic oscillator probabilities, a valid-zero RDKit descriptor example, dissolution sign counterexample, and actual CSV field interpretation.

All 11 deliberately selected suspect contracts failed their diagnostic checks. There were no tool-call exceptions or unavailable targets in those probes. **This is not a random sample and is not an overall accuracy estimate.** No paid inference was used. The frozen 400 questions and development question contents were not accessed.

## P1: Correct or quarantine before the next benchmark

### F01. Active pH functions disagree with each other and mishandle dilute solutions

Locations: `chem-memory/L3_functions/ph_calculations_tools.py:139`, `:158`, `:177`, `:293`, `:362`.

Observed through the active catalog:

| Synthetic operation | Returned | Required invariant |
| --- | --- | --- |
| pH 6 -> pOH -> pH, both at 100 C | 7.748188027 | Round trip must return 6 |
| Weak acid, Ka=1.8e-5, C=1e-9 M | pH 9.000024125 | Adding only this acid to water cannot produce a basic solution |
| Weak base, Kb=1.8e-5, C=1e-9 M | pH 4.999975875 | Adding only this base to water cannot produce an acidic solution |
| Classify pH 6.126 at 100 C | acidic | Approximately neutral under the module's own Kw=5.6e-13 |

One conversion uses temperature-dependent pKw while its inverse effectively retains 14. The dilute quadratic omits water autoionization. For a monoprotic acid, a suitable ideal-dilute balance is `H = C*Ka/(Ka+H) + Kw/H`, not the acid-only quadratic when water dominates. The same Kw convention must govern conversion, neutrality, and equilibrium calculations. Temperature/density dependence is documented by [IAPWS R11-24](https://www.iapws.org/relguide/Ionization.html).

Action: use a common, explicitly scoped Kw implementation; include water in dilute balances or return an unsupported-domain error; test inverse identities and dilution limits. Do not present a 25 C approximation as a general temperature calculation.

### F02. Active functional-group naming priority is wrong

Locations: `chem-memory/L3_functions/functional_group_tools.py:19`, `:256` and its priority table.

`determine_principal_group(['ester','amide'])` returns `amide`; `determine_principal_group(['nitrile','aldehyde'])` returns `aldehyde`. Both disagree with the relevant ordinary acyclic class seniority: ester precedes amide, and nitrile precedes aldehyde. The table also misorders anhydride/ester/acid-halide classes. [IUPAC Blue Book P-41, Table 4.1](https://iupac.qmul.ac.uk/BlueBook/P4.html).

Action: replace the ad hoc ranking with a sourced seniority table and explicitly delimit cases requiring cyclic-parent or other nomenclature rules. Add pairwise priority tests; do not infer IUPAC validation from the function's name or docstring.

### F03. Active periodic-property tools invent support and overgeneralize oxide behavior

Locations: `chem-memory/L3_functions/periodic_trends_tools.py:93`, `:114`, `:135`, `:172`.

- Unknown `Xx` receives electronegativity zero, a numerical difference from fluorine, and a ranking.
- Fe is absent from the ionization-energy table but is still ranked against H using zero internally. The returned H > Fe ordering happens to be correct; the defect is unsupported data substitution, not that particular ordering.
- `oxide_type('Al')` returns basic oxide and `oxide_type('Si')` returns amphoteric oxide. For Al2O3 and SiO2 these are incorrect: amphoteric and acidic, respectively. [LibreTexts: acid-base behavior of period-3 oxides](https://chem.libretexts.org/Bookshelves/Inorganic_Chemistry/Supplemental_Modules_and_Websites_%28Inorganic_Chemistry%29/Descriptive_Chemistry/Elements_Organized_by_Period/Period_3_Elements/Acid-base_Behavior_of_the_Oxides).

The compact exact-property capability already forbids sentinel values, but the supporting tool violates that guard. Element category alone also cannot identify a unique oxide or oxidation state.

Action: return explicit missing-data status; attach property scale, units and provenance; classify defined oxide species, or state the limited heuristic and its exceptions.

### F04. Runtime usability still permits these scientifically invalid outputs

Location: `scripts/chemistry_expert/curated_support.py:625` and the affected L3 functions.

Every one of the 12 diagnostic tool calls returned `classification=usable`, `evidence_valid=true`, `usable=true`. The current metadata correctly warns that allowlisting does not establish scientific correctness, but callers still receive a positive evidence flag. Null/nonfinite checks cannot detect a finite but physically incorrect result.

An additional probe, Boyle's law with P1=-1, V1=2, P2=2, returns V2=-1 without rejecting the invalid absolute-pressure input. This is an input-domain failure, not a failure of the algebraic rearrangement.

Action: separate successful execution, domain validity, and independently verified scientific support. Add per-function preconditions and invariants; quarantine known-invalid functions until corrected. Do not solve this by applying a blanket nonzero filter.

### F05. The dissolution teaching note contains a sign error and a false universal rule

Location: `chem-memory/L2_principles/dissolution_process.md:43` and `:46`.

The file defines mixing enthalpy as negative, then uses a signed comparison that reverses the decision-tree conclusion. For arbitrary consistent units, `100 + 20 - 150 = -30` is exothermic, although its decision tree takes the endothermic branch. Use the total enthalpy, or compare the magnitude of the negative mixing contribution with the two positive terms.

The statement that dissolution entropy always increases is false. Solvent ordering can outweigh solute dispersal; an authored LibreTexts example explicitly gives negative dissolution entropy for calcium chloride. [Gibbs energy and solubility](https://chem.libretexts.org/Bookshelves/General_Chemistry/CLUE:_Chemistry_Life_the_Universe_and_Everything/06:_Solutions/6.4:_Gibbs_Energy_and_Solubility).

This is not a dormant file: it is the first result for the audit's dissolution query. Action: correct the rule and its limits, then test the retrieved chunk, not only the compact registry.

### F06. A source-specific safety answer pattern is presented without its source row

Location: `chem-memory/L2_principles/energetic_materials_oxidizer_classification.md:38`.

The reducing-agent/oxidizing-acid section tells the model to select a particular subset of visible hazard categories without attaching the exact compatibility source row. This conflicts with the active empirical-compatibility capability's instruction to retrieve the named pair and not infer an absent table entry. The note is returned by normal retrieval.

Action: remove answer-selection instructions from generic chemistry guidance, or make the statement an explicitly sourced, versioned, narrowly applicable table record. Do not treat a missing hazard label as evidence that a hazard is absent. This is a provenance/scope defect; this audit is not replacing it with a different universal hazard list.

### F07. Safety guidance has wider applicability than its exception handling

Location: `chem-memory/L2_principles/chemtester_gap_skills/corrosive_exposure_first_aid.md:5`.

The prompt covers any corrosive skin/eye contact but its operational rule lacks explicit powder-removal and product-specific exception handling. Prompt decontamination is sound general guidance, not the error. The scope needs to defer to the relevant SDS/site protocol and appropriately trained responders rather than flatten every case to one option-selection rule. [CCOHS chemical-exposure first aid](https://www.ccohs.ca/oshanswers/chemicals/firstaid.html) documents these qualifications.

Action: narrow the educational scope and add a source-linked exception guard. Do not frame this skill as a substitute for emergency medical or site procedures.

## P2: Content, integration and provenance corrections

### F08. Harmonic-oscillator forbidden-region probability is given the wrong trend

Location: `chem-memory/L2_principles/quantum_tunneling.md:56`.

The note says probability outside the classical turning points increases with vibrational quantum number. For normalized oscillator states, the synthetic analytic check gives `P0=erfc(1)=0.1572992071` and `P1=erfc(sqrt(3))+2*sqrt(3/pi)*exp(-3)=0.1116102251`. This directly contradicts the claimed increase. The high-n probability decreases asymptotically as n^(-1/3). [Original mathematical analysis](https://arxiv.org/abs/1501.07483).

Action: distinguish a bound oscillator's tail beyond its own energy-dependent turning points from transmission through a fixed scattering barrier. Keep the newer exact finite-barrier formula and its WKB validity guards; they address a different problem and were not disproved by this check. The flawed legacy note remains indexed and retrieved.

### F09. The compact descriptor rule incorrectly demands nonzero descriptors

Locations: `chem-memory/L2_principles/chemtester_compact_problem_solving_skill.registry.json:1847`; generated topic `early_virtual_screening_profile_comparison.md:10`.

A correctly parsed benzene molecule in RDKit 2025.09.5 produces HBD=0, HBA=0, TPSA=0, rotatable bonds=0 and fraction-sp3=0. These are valid outputs, not parser failure. The current step asks for plausible nonzero values. Its separate guard against defaults from a failed parse is sensible but does not fix the overly broad step.

Action: validate parse success and each descriptor's actual domain separately. Counts may be zero, bounded fractions may be zero, and signed properties may be negative. Preserve the whole-profile comparison and the prohibition on inferring potency or clinical bioavailability from these descriptors.

### F10. Reference tables are not consistently machine-readable or attributable

Locations: `chem-memory/L4_reference/electrode_potentials.csv:1`; `acid_base_constants.csv:5` and `:21`.

The electrode table declares four columns but all 28 data rows have three. A standard DictReader places `+2.87` in `half_reaction`, `CRC` in `E0_V`, and leaves `source` null. This is a demonstrated parsing defect, not just formatting.

The acid/base table labels the HF entry "Hydric acid" and puts HF in the conjugate-base column; it should identify hydrofluoric acid and F-. It also embeds a second, base-specific header in the same file. References such as "CRC" need edition/table/conditions for defensible empirical lookup.

Across 42 CSV files, the generic single-table checker flagged 735 row-width mismatches in 21 files and embedded-header candidates in seven files. Some files intentionally contain comments or multiple sections. Those aggregate flags are **not 735 confirmed bad scientific records**; each format needs an explicit parser/schema.

The linked electrode/solubility CSV files are not directly ingested by the present Markdown/text memory loader. Thus malformed CSV is a library/publication defect and a future integration risk, not proof that every current electrochemistry lookup reads this broken table.

### F11. Capability resource links promise unavailable tools

Locations: active registry resource fields; `configs/chemistry_support_policy.json`; `chemtester_gap_skills/inorganic_reaction_constraint_ledger.md:9`.

Ten distinct linked L3 modules exist on disk but are outside the active core allowlist:

`electromagnetic_energy_tools`, `mof_tools`, `non_ideal_gas_tools`, `polymer_chemistry`, `rdkit_structure_tools`, `reaction_constraint_tools`, `solubility_tools`, `statistical_mechanics_tools`, `thermal_analysis_tools`, `tunneling_calculator`.

The inorganic constraint procedure explicitly requires calling `reaction_constraint_tools.audit_gas_product_constraints` and receiving `accepted=true`, which the current active catalog cannot supply. The finite-barrier procedure recommends a similarly unavailable exact-transmission tool, although it also supplies an analytic formula.

Action: synchronize procedure requirements with the tested function-level catalog. Enable only verified functions, or provide an explicit no-tool fallback and stop condition. Do not broadly enable all 217 modules: inactive `electrochemical_analysis_tools.py:480`, for example, contains 11 documented TODO/pass stubs.

All local resource paths in the active registry exist. Missing execution access is different from a missing file. Twelve capabilities have no resource links, but a self-contained procedure does not automatically require an external resource.

### F12. Seven unlisted managed-topic files remain in the retrieval index

Locations: `chem-memory/L2_principles/chemtester_gap_skills/`; memory enumeration in `scripts/chemistry_expert/curated_support.py:203`.

Four files correspond to explicitly retired capability IDs: `hydroxide_buffer_precipitation`, `dimensionless_ratio_output_convention`, `scaled_unit_coefficient_reporting`, `role_scoped_temperature_and_answer_provenance`. Three more are outside the active registry: `living_block_copolymer_architecture`, `proton_nmr_equivalence_and_coupling_core`, `strecker_sequence_state_tracking`.

All seven are still indexed. This does not prove they are scientifically wrong, but retirement/consolidation at the registry level is not enforced at the generic retrieval boundary. A compact update can therefore coexist with obsolete or duplicative operational instructions.

Action: make managed-topic retrieval registry-aware, with explicit archived/unlisted status and a documented policy. Preserve historical files rather than deleting them. Verify the chunks available to the model after a retirement, not merely the active-capability count.

### F13. Some narrow lessons retain problem-specific answer bias

Locations: registry `michael_enolate_product_pair_matching` step at line 317; `michael_enolate_product_pair_support.md:19`; `thermo_electronic_nitrate_screening_support.md`.

The Michael procedure generically penalizes a named succinate distractor rather than relying solely on atom mapping and product connectivity. Its linked note includes particular substrate retrieval anchors and a better conditional qualification. The compact wording drops that qualification. Older screening support also pushes a one-direction "simpler/lower burden" profile more strongly than the newer balanced comparison does.

Action: replace answer-category penalties with a condition-driven structural test; preserve examples as labeled examples. Check that an empirical preference carries the actual source, molecule set, solvent/phase and applicability. This audit found scope/anchoring risk, **not evidence of access to or leakage from the frozen acceptance set**.

### F14. A few compact rules require narrower physical assumptions or better empirical provenance

- `coupled_real_gas_equilibrium_error_analysis` (registry line 2046) permits pressure-based equilibrium by default while using nonideal equations of state. Explicitly separate an imposed textbook pressure-quotient approximation from thermodynamic real-gas equilibrium, which uses activities/fugacities. Do not silently change the problem's stated model. [IUPAC fugacity](https://goldbook.iupac.org/terms/view/F02543).
- `matched_acid_counteranion_trend_audit` (registry line 2449) demands an inversion from acidity to anion coordination. Its interaction-specific checks are useful, but proton basicity does not alone determine coordination to every cation. Make inversion a conditional hypothesis under stated controls, not a mandatory universal ranking.
- Empirical IR isomer ordering, specialized cascades and named reagent selectivities need an exact supporting source and matched conditions where these decide an answer. Generic topic links or a molecule parser do not independently establish an empirical mechanism or spectrum. These are unresolved provenance/scope flags, not blanket declarations that their chemistry is false.

Action: introduce per-rule assumptions, exceptions and evidence class. Retain conservation and identifiability checks; soften only the unsupported inference.

### F15. Some local procedures conflict with the global retrieval stop policy

Location: `chemtester_gap_skills/exact_tabulated_periodic_property_disambiguation.md:10` and V2.1 empty-search stopping behavior.

The local procedure explicitly says to search tools after an empty exact-value knowledge search. A global stop after an empty search can prevent that fallback. The correct fix is a bounded, declared alternate evidence path for this capability, not restoration of unlimited searching. Use one governing contract for query limits, fallbacks and unsupported-answer behavior.

### F16. Encoding damage and unresolved support links reduce reliability

The structural scan found 115 lines with replacement-character candidates across nine files, and 692 mojibake-pattern lines across 32 files. These are candidate-line counts, with possible overlap, not independent scientific error counts. Confirmed visible examples include damaged quantum-tunneling subscripts/arrows and electron-transfer notation. Missing-link and placeholder findings also require interpretation: bibliographic titles are not file paths, and a deliberate `return None` is not necessarily a stub.

Action: repair encoding against identifiable source text, not by guessing the missing symbol; validate formulas after restoration. Treat absent supporting resources as nonblocking warnings unless the conclusion actually depends on the missing evidence. Do not reject an otherwise correct answer or promotion solely for `missing_reference_resource`.

## What should be retained

The audit does not justify discarding the skill system. The useful core remains: explicit atom/charge/electron ledgers; quantity and unit binding; image-evidence limits; competing-model and identifiability checks; condition-specific reaction scope; distinguishing benchmark-recorded answers from scientific verification; and refusing unsupported empirical-table inference.

The current finite-barrier skill correctly distinguishes interface matching from a leading WKB exponential. The modern whole-profile screening rule appropriately separates exposure-related descriptors from target potency. The recent runtime disclaimer about allowlisting versus scientific validity is also correct, although the underlying scientific checks need strengthening.

An initially surprising classification should not be reversed just because it sounds unusual: the nitroalkane reactive-group description was checked against [NOAA CAMEO group 27](https://cameochemicals.noaa.gov/react/27). Keep source-specific classification distinct from a universal claim about every nitro compound.

All 217 Python files parse. All 71 active registry entries pass the existing model-facing structural validator. The compact index and all 71 generated active topics match the registry render after newline normalization: 72 byte-level differences are CRLF/LF only, with zero content mismatches. These are useful engineering checks, not scientific certification. There are no byte-identical duplicate-file groups in the audited corpus; semantic duplication remains a separate issue.

## Why support can hurt a correct unaided answer

The observed failure mechanisms are concrete: a retrieved note can contain a wrong rule; a finite tool result can violate chemistry while being labeled usable; a narrow lesson can bias the solver toward an earlier answer pattern; and old support can remain retrievable after compact-level consolidation. These are plausible mechanisms supported by the audit, not a causal attribution for every historical benchmark regression.

## Recommended next step

1. Correct or quarantine the confirmed active tool errors and the two false teaching notes. Add synthetic boundary/invariant tests and sourced nomenclature tests without using benchmark questions.
2. Repair the compact descriptor guard and safety/scope statements; remove unsourced answer-selection shortcuts from generic support.
3. Reconcile managed-topic membership, linked tools and CSV loading with the actual runtime. Avoid enabling unverified legacy modules merely to satisfy a link.
4. Rebuild generated compact documents from the corrected registry through the existing managed path, keeping history and immutable evaluation snapshots unchanged. Verify normalized content separately from platform line endings.
5. Freeze an auditable content/runtime manifest, verify synthetic tests and retrieval examples, then resume only the requested 120 development predictions. Do not use the frozen 400 for this repair cycle.

This audit has not implemented those corrections or launched the benchmark. Outstanding semantic/provenance items remain explicitly unverified, rather than being silently accepted or automatically rewritten.

## Close-out verification

Recomputed SHA-256 for all 1,180 inventoried skill files after the audit: zero changed files. No development runner or supervisor was present in the final process check. Only audit scripts, audit output artifacts and this report were added. Structural candidates were manually interpreted before reporting: bibliographic frontmatter was excluded from file-path failures, retired topics were distinguished from unlisted topics, and line-ending differences were not reported as content corruption.
