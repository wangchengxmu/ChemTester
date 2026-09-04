# Release Status

## Current phase

Public collaborator preview. This is not the final archival release.

## Completed

- Exported 3,086 canonical retrospective skill-development families.
- Withheld plaintext for 319 GPQA-derived families while retaining IDs and
  content hashes.
- Exported exactly 400 non-diagnostic acceptance questions and answer keys.
- Preserved the original acceptance seal metadata and source artifact hashes.
- Exported the current hierarchical skill snapshot and deterministic functions.
- Added automated release validation and contribution/security guidance.

## Required before final archival release

- Finish the pre-release GPT, Kimi, Qwen, DeepSeek, and GLM comparison matrix.
- Retry only provider-failed Kimi and Qwen rows where applicable.
- Freeze and publish aggregate result tables with paired statistical analyses.
- Complete source-by-source review for adapted QCBench/SciBench and textbook
  material; upstream dataset-level metadata does not automatically settle every
  underlying source right.
- Confirm that all visual assets are covered by the stated dataset or generator
  terms.
- Replace preview version metadata with the final release version and DOI.

## Benchmark integrity boundary

The local suite was sealed on 2026-08-31. This GitHub repository was created
after the current benchmark jobs had been launched and was made public on
2026-09-04 (Asia/Taipei). That disclosure permanently ended the suite's use as
a secret acceptance set. Unfinished runs or replacement rows completed after
disclosure are post-release evaluations.
