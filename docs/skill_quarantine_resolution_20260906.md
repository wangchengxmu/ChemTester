# Skill Quarantine Resolution And V2.1 Retest

Resolved September 6, 2026 (UTC+08), following the user's explicit instruction
to remove quarantined material or source-check and recover it before testing.

## Disposition

All pending quarantine was resolved by **removal**, not by claiming new source
verification. No material was automatically released after an encoding change.

| Material | Disposition |
| --- | --- |
| 40 encoding-suspect L2/L4 notes | Removed from the active corpus; unchanged bytes archived. |
| 184 inactive legacy Python files | Removed from the active corpus, including 1,663 catalogued functions. |
| 6 legacy tool-discovery notes | Removed with the obsolete tool surface they advertised. |
| 36 helper/test endpoints in retained modules | Permanently removed from public discovery and execution using explicit IDs. Implementation helpers and self-tests remain internal so callers are not broken. |

The 230 archived files are under `archive/skill_retirements_20260906/chem-memory/`.
`plan.json` records every original path, archival path, reason and SHA-256.
`resolution.json` verifies all moves and the unchanged retained corpus. This is
a historical archive, not an active skill directory or pending recovery queue.
The archive is outside both retrieval roots and the frozen runtime export.

The runtime now rejects explicitly retired tool IDs even if a caller retains an
old tool specification or a future edit gives the function a new docstring.
Quarantine safety checks remain enabled for genuinely new suspect material.

## Active Release

- 71 active compact capabilities, with generated topical procedures.
- 852 retrievable documents and 8,927 indexed chunks.
- 343 enabled tool functions; the same identities as before retirement.
- Zero pending document quarantine and zero pending tool quarantine.
- No surviving document bytes or active capability content changed in retirement.
- All 42 CSV artifacts remain non-machine-lookup legacy references. Their schema
  inventory and provenance limits are not independent validation of their data.
- Seven retired registry records remain historical records. Unlisted/retired
  managed topics remain excluded by registry-aware retrieval, not awaiting promotion.

Unavailable links in legacy prose are recorded as nonblocking
`missing_reference_resource` warnings. They must not be presented as available
evidence. There are no missing local resources in the active capability registry.
This cleanup does not certify every claim or calculator in the retained corpus.

## Verification

Evidence: `outputs/chemistry_expert/skill_retirement_20260906/`.

- `tests_pass.xml`: 145 tests passed, including retirement, retrieval, content,
  V2.1 routing and scientific calculator regressions.
- `probes.json`: 11/11 diagnostic contracts pass, with three expected rejected
  invalid inputs among 12 calls.
- `structure.json`: 951 corpus files, zero structural errors and zero remaining
  replacement-character/mojibake candidates in the audit scope.
- `reachability.json`: no missing active registry links or inactive L3 links.
- `protocol_tests.xml`: 63 controller, budget, source-boundary, connection and
  grading tests passed, including an exact 120-dispatch synthetic run and
  zero-call resume. `report_tests.xml`: two completion-report tests passed.
- Native context preflight passed without a paid model inference call.

The first test invocation lacked the new temporary directory's parent and hit
an obsolete test expecting more than 1,000 quarantined tools. Its failed report
is preserved as `tests.xml`; the assertion now checks explicit retirement and
zero pending quarantine. No chemistry test was weakened to pass a wrong result.

## Retest Protocol

New run: `outputs/chemistry_expert/skill_router_v2_development/runs/gpt56sol_xhigh_20260906_v21_clean120/`.

- Exactly 120 final prediction slots in **one** `router_v2` arm using corrected
  V2.1 runtime and the post-retirement frozen skill set.
- GPT-5.6 Sol, xhigh, using isolated audited Codex transport and the existing
  local proxy that succeeded after the previous connection amendment.
- Reuse original development indices 0-119, without selection rebuilding,
  score filtering, resampling or opening validation/acceptance question files.
- Freeze current scripts, configurations and support files. Every worker
  verifies this inventory; it cannot read the retirement archive.
- Controller-only evaluator data; performers receive redacted questions only.
- Reuse five parent pilot indices 0, 1, 7, 20 and 64. Pilot validity, not accuracy,
  gates the remaining run. These five predictions count within 120.
- At most two declared infrastructure attempts per slot; no retry because an
  answer is scientifically incorrect or disagrees with the benchmark key.
- The prediction budget is not a model-call budget: planner calls and provider
  retries are separately recorded. Two planner rounds normally, with at most
  one extra action for the existing explicit V2.1 reference-to-tool fallback.
- No skill learning, repair or promotion during the run. Historical experiment
  inputs, outputs, counters and runtime snapshots remain unchanged.

This is a development regression check on already exposed families, not unseen
generalization. Prior stored totals include legacy answer postprocessing and an
older evaluator; any later comparison must disclose these changes rather than
claim a controlled skill-only ablation. The frozen 400 remain unused here.

Preparation and launch are separate. The authoritative live progress is the
new run's `latest_status.json`; this protocol document is not a completion claim.
After a successful pilot, `continue_router_v21_clean120.ps1` runs the remaining
slots through the existing proxy/AC-sleep supervisor and then writes
`completion_report.json` and `completion_report.md`. It does not start extra
arms, regrade historical answers, or perform model inference for the report.
