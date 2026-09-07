# Router V2.1.1 Runtime Fixes

## Scope

Implemented the four runtime fixes from the ten-case development review. This is
a runtime revision, not a new chemistry-skill promotion or a new accuracy result.
No model inference, historical regrading, benchmark-key edits, chemistry-content
edits, or frozen 400-question access was performed.

## Changes

1. Chemical compatibility hazard intent is detected from the question stem,
   independently of compact-skill selection. It requests pair-specific reference
   evidence and permits the existing bounded empty-knowledge fallback to tool
   search. The model must still select the tool and supply explicit arguments.
   There is no automatic lookup or answer override.
2. Source-only, navigation-only and scrape-error stubs do not count as substantive
   evidence. Source paths/titles and availability warnings remain inspectable in
   index metadata or runtime traces. `missing_reference_resource` remains a
   nonblocking warning for otherwise usable evidence.
3. Retrieval, exact-linked loading, planner prompts and final answer prompts use
   complete Markdown evidence packets. Heading subtrees retain relevant parent
   definitions/units and scoped guard sections. Tables and fenced blocks are not
   character-sliced. Per-document budget: 3,200 characters; prompt evidence budget:
   6,400 characters across at most five documents. Oversized packets are omitted,
   not shortened into incomplete evidence. This can change retrieval ranking and
   increase delivered support relative to the previous clipped prompts.
4. The final answer prompt uses the existing multi-select detector, consistent with
   the model-call system prompt. Multi-select requests all correct letters in
   ascending order; single-select still requests exactly one letter.

## Checks

The combined regression run passed **141 tests and five subtests** in 23.17 seconds,
including 17 new synthetic acceptance tests in `tests/test_router_evidence_fixes.py`.
The machine-readable report is
`outputs/chemistry_expert/skill_router_v2_development/analyses/router_v211_runtime_fixes_20260906/regression_tests.xml`.
The default Windows pytest temporary directory was inaccessible; verification uses
a unique workspace `--basetemp` instead, without changing its permissions.

Static replay of the previously exposed development cases, without calling a model:

| Case | Confirmed runtime behavior |
| --- | --- |
| 0 | Full 2,014-character real-gas evidence packet reaches the final prompt, including final applicability/units guards. |
| 43 | Empty hazard source is excluded; no retrieved document is counted; multi-select contract only. |
| 110 | Multi-select contract only; no answer repair or stored-result change. |
| 116 | `knowledge_search`, `reference_task=chemical_compatibility`, despite zero selected capabilities; multi-select contract only. |

All 329 input hashes recorded by the previous ten-case review were verified
unchanged. Those inputs are under the development-run/analysis directory, not the
frozen acceptance suite. Runtime snapshots automatically include the new Python
helper through the existing snapshot inventory mechanism; existing snapshots were
not updated.

## Limits

- These checks verify routing, evidence packaging and prompt contracts, not an
  accuracy improvement. The previous 120-question scores remain historical results.
- The compatibility detector is a lexical intent gate, not a chemistry adjudicator.
  A successful search is not independent verification of its scientific contents.
- Evidence that cannot fit as a complete packet is unavailable for that prompt.
  This deliberately prefers omission to a partial table, formula or procedure.
- Legacy offline review prompts and tool-result serialization were not redesigned.
  The new shared packet policy covers document evidence in the adaptive runtime.

## Reproduction

Use Python 3.10+ with `-B -X utf8 -m pytest`,
`-p no:cacheprovider` and a fresh `--basetemp` directory. Run these test files:

- `tests/test_router_evidence_fixes.py`
- `tests/test_router_v21_regressions.py`
- `tests/test_skill_corpus_corrections.py`
- `tests/test_chemistry_tool_skill.py`
- `tests/test_curated_chemistry_support.py`
- `tests/test_router_v2_grading_contract.py`
- `tests/test_prepare_router_v21_retest.py`
- `tests/test_router_development_single_arm.py`
- `tests/test_skill_router_development_runner.py`
- `tests/test_skill_router_v2_development_set.py`
- `tests/test_router_v21_completion_report.py`
- `tests/test_model_policy.py`
