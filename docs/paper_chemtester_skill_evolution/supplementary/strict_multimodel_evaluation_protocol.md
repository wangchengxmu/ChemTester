# Strict Multimodel Evaluation Protocol

## Purpose

This protocol evaluates the current ChemTester chemistry skill runtime on an untouched, sealed 400-question suite. Public artifacts contain only aggregate statistics and cryptographic identifiers. They do not contain question text, answer options, benchmark-recorded answers, item identifiers, or per-item model traces.

## Frozen Evaluation State

- Runtime snapshot: `runtime_20260831_161726`
- Snapshot frozen: `2026-08-31T16:17:50.342128+08:00`
- Runtime tree SHA-256: `cef29fa473a0bc1f2f93da9183445739807b5b943cd131602cad5f5af1d4ebf3`
- Performer manifest SHA-256: `53f8264fe58d3ac1cadf91765eca949ff70f332928c3d9ce1a26dd8ddbc759c0`
- Evaluator answer-key SHA-256: `d19340e3fa843da4c8e4e4e52ce935a6d691273ba5cc22632a3be61dbb1c266f`
- Suite SHA-256: `3997d88168fb6c70cbc31525cbb1b0f1f1797bcc870b5da872bf32ca3041d90b`
- Selection: all 400 gating questions
- Task profile: `advanced_chemistry_review`
- Self-evolution: disabled
- Web resource discovery: disabled
- Generated-tool installation: disabled
- The evaluator answer key is excluded from the candidate workspace and used only after each model answer is frozen.

The frozen runtime delegates required image observation to the same fixed vision profile in every arm. The evaluated model produces every final chemistry answer.

## Final Skill Snapshot Composition

The frozen runtime contains 1,073 versioned skill-source files:

- `L2_principles`: 847 files. This comprises 766 broad chemistry knowledge and reasoning documents, the compact guide, its structured registry, the L2 index, and 78 detailed retrospective gap-skill documents.
- `L3_functions`: 226 files. This comprises 217 Python chemistry-tool modules, the function registry and catalog, and seven Markdown index or tool-use documents.
- Compact registry state: 71 active capabilities and 7 retired or merged capabilities.

In a skills-enabled arm, `tool_skill.enabled=true`. The runtime considers all 71 registry capabilities when selecting question-relevant compact sections, permits model-directed retrieval across the complete L2 tree, and permits model-directed discovery and execution of cataloged L3 functions. The full corpus is available to the runtime but is not inserted wholesale into each prompt.

In a skills-disabled arm, the same frozen source tree remains physically present to preserve the runtime control, but `tool_skill.enabled=false`; no compact-skill selection, L2 knowledge search, L3 tool search, or L3 tool call is exposed to the answering model.

Python may create `__pycache__/*.pyc` files inside an isolated runtime during execution. These derived bytecode files are excluded from skill-source integrity comparisons.

## Controlled Skill Ablation

Each model is run twice. The only intended within-model change is:

- Skills enabled: `tool_mode=autonomous`
- Skills disabled: `tool_mode=disabled`

Both arms retain the same model, provider, reasoning setting, maximum token budget, timeout, task profile, suite, evaluator, runtime snapshot, and vision-observation policy. A historical result is not accepted as a control when its runtime snapshot differs.

## Model Matrix

| Model | Reasoning | Skills enabled | Skills disabled | Status |
|---|---|---:|---:|---|
| GPT-5.6-sol | xhigh | 368/400 (92.00%) | 359/400 (89.75%) | Complete |
| GLM-5.3-flash | high, thinking enabled | 346/400 (86.50%) | 344/400 (86.00%) | Complete |
| Kimi K3 | high, thinking enabled | 325/400 (81.25%) | 338/400 (84.50%) | Complete |
| Qwen 3.8 Max snapshot `qwen3.8-max-0902` | xhigh | 347/400; 9 provider failures | 344/400; 11 provider failures | Incomplete; provider retries required |
| DeepSeek V4 Pro snapshot `deepseek-v4-pro-0813` | max | 350/400 (87.50%) | 352/400 (88.00%) | Complete |

The July Kimi K3 results, 328/400 with skills and 333/400 without skills, used `runtime_20260726_221207`. They are historical context and are excluded from the current controlled ablation.

## Final Snapshot Audit

The current run artifacts were re-audited against `runtime_20260831_161726`. For both the enabled and disabled arm of every model listed below, the selection manifest references the frozen snapshot, its `snapshot.json` hash is `47e1e00b55a376f62563c4e5a6db402574eb2d8480646f648634d00b7b7593bc`, and all 1,073 L2/L3 source files match the frozen source tree exactly.

| Model | Enabled arm | Disabled arm | Full skill-tree match | Run completeness |
|---|---:|---:|---:|---|
| GPT-5.6-sol | Correct final snapshot | Correct final snapshot | Exact in both arms | Complete |
| GLM-5.3-flash | Correct final snapshot | Correct final snapshot | Exact in both arms | Complete |
| Kimi K3 | Correct final snapshot | Correct final snapshot | Exact in both arms | Complete |
| Qwen 3.8 Max | Correct final snapshot | Correct final snapshot | Exact in both arms | Incomplete due to provider failures |
| DeepSeek V4 Pro | Correct final snapshot | Correct final snapshot | Exact in both arms | Complete |

Older run directories that reference earlier runtime snapshots remain historical artifacts and must not be substituted into this matrix.

## Request Controls

- GPT-5.6-sol uses the Codex backend with `model_reasoning_effort=xhigh`.
- GLM-5.3-flash uses its OpenAI-compatible endpoint with thinking enabled, temperature 0, and a 16,384-token cap.
- Kimi K3 uses the Moonshot endpoint with native thinking enabled, temperature 1, and a 16,384-token cap.
- Qwen 3.8 Max will use the Alibaba Cloud Model Studio OpenAI-compatible endpoint with `reasoning_effort=xhigh`, temperature 0, and a 16,384-token cap.
- DeepSeek V4 Pro will use the Alibaba Cloud Model Studio OpenAI-compatible endpoint with `reasoning_effort=max`, temperature 0, and a 16,384-token cap.

Provider-specific request controls are recorded in each run's selection manifest. They are fixed across the enabled and disabled arms for that model.

## Reporting Rules

For each arm, report accuracy, Wilson 95% confidence interval, strict-format rate, provider-failure count, runtime-error count, median latency, P95 latency, source-level accuracy, knowledge-search use, tool-search use, model-selected tool calls, and vision completion.

For each within-model pair, report both-correct, both-incorrect, skill-only-correct, no-skill-only-correct, accuracy difference, and the exact two-sided McNemar p-value. Interpret a single deterministic run as evidence about this frozen suite, not as a universal model ranking.

## Reproduction

Run one foreground arm with:

```powershell
& .\scripts\chemistry_expert\run_strict_current_acceptance_arm.ps1 `
    -Provider kimi `
    -ToolMode autonomous `
    -Workers 4
```

Use `-Provider gpt`, `-Provider kimi`, `-Provider qwen`, or `-Provider deepseek`, and set `-ToolMode` to `autonomous` or `disabled`. `-Smoke` limits execution to one gating item for provider validation.

Qwen requires a valid Model Studio key and workspace-compatible base URL in Windows process or user scope. The launcher recognizes `DASHSCOPE_API_KEY`, `QWEN_API_KEY`, or `Aliyun_API_KEY`, and `DASHSCOPE_BASE_URL`, `QWEN_API_BASE`, or `Aliyun_API_BASE`. Credentials must never be committed or printed in logs.
