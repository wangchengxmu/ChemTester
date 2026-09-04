# Dataset Licenses and Use Conditions

This file records upstream dataset metadata for the included or referenced
question families. It is an attribution and release-control record, not legal
advice and not a blanket relicense of third-party content.

| Source | Upstream metadata or condition | Release handling |
|---|---|---|
| ChemBench | MIT; <https://huggingface.co/datasets/jablonkagroup/ChemBench> | Included in the private preview with source identifiers retained. The upstream canary warns against use in training corpora. |
| QCBench | Apache-2.0; <https://huggingface.co/datasets/jiaxie/QCBench> | Included in the private preview. Underlying textbook/SciBench provenance still requires row-level review before public release. |
| GPQA | CC BY 4.0 plus an access condition requesting that examples not be revealed online; <https://huggingface.co/datasets/Idavidrein/gpqa> | Plaintext questions, options, and answers are withheld. IDs and SHA-256 hashes are retained. |
| SUPERChem | MIT; <https://huggingface.co/datasets/ZehuaZhao/SUPERChem> | Included in the private preview. The upstream canary warns against use in training corpora. |
| MMLU | MIT; <https://huggingface.co/datasets/cais/mmlu> | Included with dataset/config/split provenance. |
| ChemBench4K | MIT; <https://huggingface.co/datasets/AI4Chem/ChemBench4K> | Included with source identifiers retained. |
| OlympicArena | CC BY-NC-SA 4.0; <https://huggingface.co/datasets/GAIR/OlympicArena> | Private-preview use only pending final attribution and share-alike review. |
| ChemTester parameterized and unit-format items | Repository-authored deterministic generators | Included as project-authored evaluation data; generator provenance is retained. |
| ChemTester native vision items | Repository-authored deterministic generator and locally sealed assets | Included in the private preview pending final visual-asset review. |

## Attribution requirements

Any public release must retain each record's source repository and source
question identifier, include the citations requested by the upstream dataset
cards, and preserve all applicable copyright and license notices.

## Training terminology

The 3,086-family corpus was used to improve an external, inspectable chemistry
memory and skill registry. It did not update model weights. It is therefore
described in this repository as a `skill-development` set, not a model-training
set. Benchmark canary warnings still apply and are not removed.

