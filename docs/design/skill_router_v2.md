# Skill Router V2.1.1

## Purpose

Skill Router V2.1.1 reduces harmful support injection and unnecessary planner calls. It treats the final compact skill registry as a sparse routing index instead of a prompt that must be attached to every chemistry question.

The router does not modify the final skill set or the frozen pre-evaluation snapshot. It changes only when and how existing capability procedures, linked support documents, knowledge search, and deterministic tools are exposed to the answering model.

## Routes

| Route | Skill procedure | Planner | Intended use |
| --- | --- | --- | --- |
| `direct` | none | no | No support signal clears an activation gate. |
| `skill` | one confident registry capability | no | A transferable procedure matches the visible question. |
| `tool` | none | yes | The question has an explicit calculation or conversion signal. |
| `skill_tool` | one confident registry capability | yes | Both a procedure and a calculation or conversion signal are present. |
| `knowledge_search` | none | yes | The question explicitly requests an empirical or tabulated reference fact. |

V2 uses visible question text, options, and given values only. It does not use benchmark-recorded answers, evaluator keys, source solutions, or result history for routing.

## Capability Gate

The current policy selects at most one capability. A registry entry must satisfy all configured conditions:

- anchor coverage at least `0.65`;
- at least `2` anchor-token hits; and
- either an exact retrieval phrase or a score margin of at least `0.10` over the next candidate.

If no entry passes, the router abstains. A selected capability is rendered from the registry's applicability statement, procedure steps, guards, and resource links. V2 may exact-load one linked L2/L4 Markdown or text document under `chem-memory`; it rejects path traversal and does not load L3 code as prose.

Planner rationale is not copied into final answer synthesis. Only structured retrieved documents and results from tools the planner actually called are passed as supporting evidence.

## Development Families

The development-family builder uses the non-sealed, question-family-deduplicated retrospective open-benchmark corpus:

- raw archival items: `7,381`;
- canonical question families: `3,086`;
- deterministic development split: `240` families;
- disjoint internal validation split: `120` families;
- prior incorrect families retained: `99` development and `28` validation;
- development/validation family overlap: `0`;
- overlap with the current frozen-suite selected item IDs: `0`.

The split is created before family selection by a stable seeded hash. Selection retains prior-error families within each pool, adds high-confidence examples for routed capabilities, and fills remaining positions across route, dataset family, and answer format.

Performer manifests contain no benchmark-recorded answer, expected answer, tolerance, matching function, or hidden multi-select answer metadata. Evaluator keys are stored in separate files. The builder reads only the frozen selection's item IDs as an exclusion list; it does not read frozen question or answer content.

These retrospective families are suitable for router tuning and internal validation. They are not an untouched publication test because the skill set was developed through the retrospective workflow.

## Artifacts

- Runtime policy: `configs/skill_router_v211.json`
- Router implementation: `scripts/chemistry_expert/chemistry_tool_skill.py`
- Evidence and tool catalog: `scripts/chemistry_expert/curated_support.py`
- Canonical knowledge and calculators: `chem-memory/`
- Sanitized public runtime example:
  `configs/examples/self_evolving_chemistry_expert.json`

Verify the native export and release package with:

```powershell
python scripts\chemistry_expert\export_native_chemistry_skills.py --check
python scripts\validate_release.py
```

Development-set builders, run state, predictions, evaluator keys, and result
tables are deliberately outside this interim skills/router commit. Completed
benchmark artifacts will be published separately after audit.

## Evaluation Protocol

Tune activation thresholds and routing behavior only on the 240 development families. Freeze the router, then run one confirmatory comparison on the 120 internal validation families.

Use matched model, reasoning effort, prompt, question order, answer parser, retry policy, and evaluator settings for all arms:

1. No skill or tool support.
2. Core chemistry workflow only.
3. Skill Router V2 with sparse L2 procedure injection.
4. Skill Router V2 with sparse L2 procedure injection plus linked L3 tools.

Report overall accuracy, paired question-level deltas, McNemar tests, route-level accuracy, activation rate, planner-call rate, tool-call rate, prompt characters, latency, and failure categories. A future publication claim still requires an untouched evaluation set that was not used to develop the skills or the router.
