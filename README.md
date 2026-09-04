# ChemTester Skills and Benchmark Data

This repository is the collaborator-preview release of ChemTester's chemistry
problem-solving skills and evaluation data. It separates the artifacts used to
develop the external skill system from the fixed acceptance set used only for
evaluation.

## Included artifacts

- `skills/current/`: the current hierarchical chemistry skill snapshot and
  deterministic chemistry functions, with a file-level SHA-256 manifest.
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

The development export withholds the text and answer content of 319 GPQA-derived
families. Their identifiers and cryptographic hashes remain available for audit,
but the upstream GPQA access terms request that examples not be posted online.

The 400-question acceptance file excludes all 11 diagnostic items. It is now
public, so the suite is no longer secret and later results must be labeled
post-release rather than pooled with controlled pre-release runs.

## Validation

The release has no runtime dependency. Validate its counts, hashes, asset set,
restricted-content handling, and credential hygiene with:

```powershell
python scripts/validate_release.py
```

## Licensing

Repository-authored code is provided under the MIT license. Dataset records
retain their upstream terms and attribution requirements; see
`DATA_LICENSES.md`. No blanket relicensing of third-party question content is
claimed.
