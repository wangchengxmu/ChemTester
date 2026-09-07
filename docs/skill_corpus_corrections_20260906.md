# Skill Corpus Corrections, 2026-09-06

## Status

Implemented the confirmed errors and safeguards identified in the
[whole-corpus audit](skill_corpus_audit_20260906.md). Unsupported empirical
assertions were narrowed or withheld, not replaced by guessed chemistry.
The benchmark remains paused. No model calls, development/evaluation question
contents, historical result edits, or immutable snapshot edits were used.

**139 tests passed; all 11 original synthetic diagnostic contracts now pass.**
The three rejected calls in the 12-call probe are intentional: unknown element
data, absent ionization-energy data, and negative absolute pressure.

## Finding Dispositions

| Finding | Correction or containment | Remaining limit |
| --- | --- | --- |
| F01 pH | Shared pKw convention; water-inclusive monoprotic balances; temperature-consistent neutrality; inverse Ka checks; invalid inputs rejected. | 25 C and 100 C are approximate dilute-water anchors; other temperatures require explicit Kw. Concentration-based pH assumes unit activity coefficients. |
| F02 naming | Corrected the bounded IUPAC P-41 seniority order, unknown-group handling and unsupported-scope rejection. | Not a complete IUPAC parent-selection engine; unsupported sulfur-group comparisons are refused. |
| F03 periodic data | Removed fabricated zero defaults and noble-gas zero EN entries; explicit stored-precision ties and missing-data errors; Al2O3/SiO2 oxide classification corrected. | Legacy values remain approximate and provenance-unverified. Oxide mapping is restricted to the seven explicitly documented period-3 species. |
| F04 evidence | Separated execution, output-contract success and scientific validity; added physical gas-domain checks and n/state consistency checks. | A successful finite output is still only candidate evidence, not independent verification. |
| F05 dissolution | Correct signed enthalpy sum; entropy may have either sign; Gibbs-energy/composition qualifications. Removed hypothetical tool promises. | Solubility still needs appropriate activities, phases and empirical support. |
| F06 compatibility | Removed the unsourced hazard-category answer list; require the exact empirical pair record and conditions. | Missing labels mean unknown, not safe. |
| F07 exposure guidance | Educational scope, SDS/site/medical authority, dry-powder and product-specific exception guard. | Not an operational substitute for trained emergency response. |
| F08 oscillator | Reconstructed the damaged note; corrected forbidden-region trend and separated it from fixed-barrier scattering. Retained exact finite-barrier and WKB distinctions. | Assumptions and limiting regimes are explicit. |
| F09 descriptors | Parse success and per-field domains replace the nonzero requirement. | Zero counts/fractions and negative cLogP can be valid; descriptors do not establish potency or clinical exposure. |
| F10 CSV | Uniform electrode and acid/base schemas; HF name and conjugate-base correction; all 28 electrode and 23 acid/base records preserved. Inventoried all 42 CSVs without enabling generic lookup. | Forty other legacy formats require declared parsers; numeric provenance is not certified. Shape candidates are not counts of false scientific records. |
| F11 availability | Removed 20 active resource links to unavailable modules, raw CSVs or quarantined text. Mandatory unavailable-checker calls became explicit ledgers/derivations with optional available tools. | No blanket activation of the other legacy modules. Empirical evidence may remain unavailable. |
| F12 retirement | Generic and exact-linked retrieval enforce active managed-topic membership. | Seven retired/unlisted files remain preserved on disk but are not retrievable. |
| F13 answer bias | Removed Michael product-name penalties and substrate-specific retrieval anchors; screening now compares competing profile dimensions. | Examples and heuristics remain conditional, not memorized option rules. |
| F14 scope | Distinguished fugacity-based equilibrium from imposed pressure models; removed mandatory acidity/coordination inversion and unsourced IR ordering; made specialized cascades, Cannizzaro exceptions and ligand cleavage source-dependent; qualified cleavage workup and rearrangement kinetics. | Exact empirical orders/selectivities remain unresolved without matched sources. |
| F15 fallback | One declared knowledge-to-tool fallback for exact periodic values; no repeated knowledge search, second empty channel stops. | At most one additional planner action beyond the configured budget, not unlimited retrieval. |
| F16 damaged support | Forty encoding-suspect notes are quarantined at both retrieval boundaries; the quantum note was reconstructed. Sixteen explicit missing-resource candidates are nonblocking warnings. | Raw damaged notes have not been source-restored. Other structural link candidates include bibliographic/path ambiguities. |

## Verification and Scope

- Active compact capabilities: **71**, preserved; all pass the model-facing validator.
- Compact index and all active topic files match the registry after newline normalization.
- All **217** Python modules parse; the active catalog remains **343 functions in 32 modules**.
- Actual retrieval: **852 documents / 8,927 chunks**, formerly 898 / 9,801.
- Active registry: no missing local resource paths, no linked inactive L3 modules,
  and no raw CSV links advertised as text-retrievable support.
- Corpus: **40 existing files changed**, **1 scope note added**, **1,140 existing
  files unchanged**. This changed-file count is separate from the 40 quarantined
  legacy notes, which were preserved.
- Temperature round trip: 6 -> pOH -> 6 at 100 C. The 1e-9 M acid/base probes
  now give pH 6.9978406 / 7.0021594, respectively.
- The normal pytest temporary directory was inaccessible; the successful run
  used a fresh workspace-local temporary directory and disabled the cache plugin.

Evidence is under `outputs/chemistry_expert/skill_corpus_corrections_20260906/`:
`structure.json`, `reachability.json`, `probes.json`, `tests.xml`,
`maintenance.json`, and `verification.json`. The verification record contains
before/after corpus hashes and a current runtime/configuration hash inventory.
The maintenance receipt describes its intermediate rebuild; the final registry
hash is in the verification inventory after the final scope edits.

The source registry remains
`chem-memory/L2_principles/chemtester_compact_problem_solving_skill.registry.json`.
Generated Markdown was rebuilt through `update_frontier_skill.py`, not edited
independently. Historical evidence and retired registry records were retained.
This was user-authorized maintenance, **not a new model-repair promotion**.

## Scientific Sources and Remaining Work

The naming correction follows [IUPAC P-41](https://iupac.qmul.ac.uk/BlueBook/P4.html).
The water-temperature limitation follows [IAPWS R11-24](https://www.iapws.org/relguide/Ionization.html).
Exposure qualifications follow [CCOHS](https://www.ccohs.ca/oshanswers/chemicals/firstaid.html).
The oscillator trend follows the [mathematical analysis](https://arxiv.org/abs/1501.07483);
the dissolution note links its LibreTexts source directly.

This correction pass is not independent certification of every legacy equation,
constant or function. Recovering the quarantined text and completing empirical
provenance are separate curation work. Synthetic passes also do not establish
improved LLM accuracy. Keep the stopped historical experiment and frozen 400
separate; any later authorized development test must record this revised
content/runtime identity rather than silently resume under an older snapshot.
