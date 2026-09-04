# Acceptance Evaluation Set

`questions_and_keys_400.jsonl` contains exactly the 400 gating items selected
before the current model comparison. The 11 diagnostic items in the internal
suite are excluded, so this file is the complete scored acceptance set.

The file joins each performer-visible problem with its benchmark-recorded
answer key for reproducibility. `original_seal.json` records the hashes of the
original split performer/evaluator artifacts and the frozen runtime snapshot.

This repository is currently private. Making this directory public ends the
suite's secrecy. Results generated after that event must be labeled
post-release and should not be compared as if they were controlled pre-release
measurements.

