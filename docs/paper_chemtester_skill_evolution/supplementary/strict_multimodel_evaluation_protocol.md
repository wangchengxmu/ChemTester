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

## Controlled Skill Ablation

Each model is run twice. The only intended within-model change is:

- Skills enabled: `tool_mode=autonomous`
- Skills disabled: `tool_mode=disabled`

Both arms retain the same model, provider, reasoning setting, maximum token budget, timeout, task profile, suite, evaluator, runtime snapshot, and vision-observation policy. A historical result is not accepted as a control when its runtime snapshot differs.

## Model Matrix

| Model | Reasoning | Skills enabled | Skills disabled | Status |
|---|---|---:|---:|---|
| GPT-5.6-sol | xhigh | 368/400 (92.00%) | Running | Current frozen snapshot |
| GLM-5.3-flash | high, thinking enabled | 346/400 (86.50%) | 344/400 (86.00%) | Complete |
| Kimi K3 | high, thinking enabled | Running | Running | Fresh controlled pair |
| Qwen 3.8 Max snapshot `qwen3.8-max-0902` | xhigh | Running | Running | Credential and one-item smoke test passed |
| DeepSeek V4 Pro snapshot `deepseek-v4-pro-0813` | max | Running | Running | Credential and one-item smoke test passed |

The July Kimi K3 results, 328/400 with skills and 333/400 without skills, used `runtime_20260726_221207`. They are historical context and are excluded from the current controlled ablation.

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
