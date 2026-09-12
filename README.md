# ChemTester Skills and Benchmark Data

This repository is the collaborator-preview release of ChemTester's chemistry
problem-solving skills and evaluation data. It separates the artifacts used to
develop the external skill system from the fixed acceptance set used only for
evaluation.

## Two recommended options

Both versions are valid ways to use the chemistry skills:

| Version | Knowledge and tools | Tradeoff |
| --- | --- | --- |
| [12 native Codex skills](docs/native_chemistry_skills.md) | Self-contained packages with selected procedures and optional calculators; Codex handles selection. | Lighter and more efficient, with less orchestration overhead. **Recommended installation for most users.** |
| [Skill Router V2.1.1](docs/design/skill_router_v2.md) | A custom runtime that selectively retrieves procedures, supporting knowledge, and approved tools from `chem-memory`. | Can improve answering performance, but adds latency through routing, retrieval, and planning. |

**Start by installing the 12 native skills.** They do not require the router
or the separate `chem-memory` corpus. Choose Router V2.1.1 when access to the
broader knowledge library and potential performance gains justify the additional
runtime setup and latency. Performance gains depend on the model and questions;
the router is not guaranteed to outperform native skills on every task.

## How these skills were developed

The skills began with textbook-derived notes from an earlier
**OpenClaw-associated reading and extraction workflow**. The source scope was
the eight Chemistry LibreTexts shelves: introductory, general, organic,
inorganic, analytical, physical and theoretical, biological, and environmental
chemistry. Documented examples include targeted extraction from Averill's
general chemistry material and Harvey's analytical chemistry material, alongside
physical chemistry and crystallography sources. These notes were organized into
chemical principles, executable calculators, and reference resources rather
than retained only as chapter summaries.

The compact procedures were then refined using **GPT-5.6-sol with xhigh
reasoning** on **3,086 canonical question families** from historical open
benchmarks. Incorrect answers prompted diagnosis, repair, and checked reruns
before useful strategies were promoted into the external skill memory.
Subsequent scope, content, and tool audits consolidated the published package
into **12 native Codex skills with 70 procedures**. Codex can select these
skills and load their references and optional calculators as needed; this is
external-memory development, **not model-weight training**.

Source coverage is partial: the retained records include targeted extraction,
overlap-based skips, and blocked sources, and do not establish that every
LibreTexts book was fully read. See the
[source provenance audit](docs/paper_chemtester_skill_evolution/supplementary/source_provenance_audit.md)
for these distinctions and the
[skill catalog](docs/native_chemistry_skills.md) for the installable packages.
Source-specific attribution and licensing still apply.

## Included artifacts

- `.agents/skills/chem-*`: 12 native Codex chemistry skills containing 70
  reviewed procedures and optional standalone deterministic calculators.
- `configs/skill_router_v211.json`: the sparse Skill Router V2.1.1 policy,
  with its implementation and evidence layer under `scripts/chemistry_expert/`.
- `chem-memory/`: the corrected canonical L2/L4 knowledge corpus and approved
  L3 modules used by Router V2.1.1.
- `skills/current/`: the earlier immutable hierarchical snapshot retained for
  provenance, with a file-level SHA-256 manifest.
- `data/skill_development/canonical_families_3086.jsonl`: the 3,086 canonical
  question families used for retrospective external-memory and skill
  development. This is not model-weight training data.
- `data/evaluation/acceptance_v1/questions_and_keys_400.jsonl`: exactly 400
  fixed gating questions and their benchmark-recorded answer keys.
- `data/evaluation/acceptance_v1/assets/`: the 50 visual assets used by the
  acceptance set.
- `docs/paper_chemtester_skill_evolution/`: manuscript, project-truth record,
  provenance audit, and strict multimodel evaluation protocol.

## Important status

This first GitHub version is a **public collaborator preview**, disclosed on
September 4, 2026. The multimodel benchmark matrix was launched from an
immutable local snapshot before disclosure, but unfinished runs and replacement
rows completed after disclosure must be labeled post-release. The remaining
final-release work is tracked in `RELEASE_STATUS.md`.

Router V2.1.1 and the 12 native Codex skills were added on September 7, 2026,
before the ongoing post-release 400-question run finished. That run and its
comparison tables are not included in this commit and will be published only
after completion and audit.

The development export withholds the text and answer content of 319 GPQA-derived
families. Their identifiers and cryptographic hashes remain available for audit,
but the upstream GPQA access terms request that examples not be posted online.

The 400-question acceptance file excludes all 11 diagnostic items. It is now
public, so the suite is no longer secret and later results must be labeled
post-release rather than pooled with controlled pre-release runs.

## Validation

The data snapshot has no runtime dependency. Validate its counts, hashes, asset
set, native-skill package, Router V2.1.1 configuration, restricted-content
handling, and credential hygiene with:

```powershell
python scripts/validate_release.py
```

See [`docs/native_chemistry_skills.md`](docs/native_chemistry_skills.md) for the
12-skill catalog and usage instructions. Router V2.1.1 is the alternative
corpus-backed runtime and is not required for native Codex skill selection.

## Licensing

Repository-authored code is provided under the MIT license. Dataset records
retain their upstream terms and attribution requirements; see
`DATA_LICENSES.md`. No blanket relicensing of third-party question content is
claimed.
