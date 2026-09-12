# Native Chemistry Skills

## Current Delivery

The primary user-facing deliverable is now a collection of **12 native Codex
skills**, covering all **70 active corrected procedures** in the current compact
registry. The packages live in `.agents/skills/chem-*`. The existing
`chemistry-tool-runtime` skill is an engineering aid and remains separate.

Codex chooses relevant skills, loads their references, plans the work, and
decides whether to use a calculator. There is no additional chemistry model
router, forced reasoning loop, or answer-rewriting stage in this path. This is
a packaging change, not a claim that native selection has higher accuracy.

**Skill Router V2.1.1 does not need to be installed or run to use these skills.**
It is an optional research component whose additional orchestration can slow
answering. Modest performance improvements observed in some project test
configurations may not justify that latency and are not guaranteed for other
models or questions. Native skills without the router are the recommended
starting point for routine use.

## Catalog

| Skill | Procedures | Optional calculator functions |
| --- | ---: | ---: |
| [chem-thermodynamics](../.agents/skills/chem-thermodynamics/SKILL.md) | 7 | 44 |
| [chem-aqueous-equilibria](../.agents/skills/chem-aqueous-equilibria/SKILL.md) | 5 | 68 |
| [chem-kinetics-reactors](../.agents/skills/chem-kinetics-reactors/SKILL.md) | 4 | 30 |
| [chem-organic-mechanisms](../.agents/skills/chem-organic-mechanisms/SKILL.md) | 10 | 9 |
| [chem-spectroscopy](../.agents/skills/chem-spectroscopy/SKILL.md) | 7 | 32 |
| [chem-inorganic-reactions](../.agents/skills/chem-inorganic-reactions/SKILL.md) | 8 | 42 |
| [chem-analytical-quantitation](../.agents/skills/chem-analytical-quantitation/SKILL.md) | 5 | 44 |
| [chem-crystal-structures](../.agents/skills/chem-crystal-structures/SKILL.md) | 3 | 33 |
| [chem-safety-references](../.agents/skills/chem-safety-references/SKILL.md) | 8 | 2 |
| [chem-toxicology](../.agents/skills/chem-toxicology/SKILL.md) | 5 | 0 |
| [chem-biomolecular-analysis](../.agents/skills/chem-biomolecular-analysis/SKILL.md) | 5 | 35 |
| [chem-quantum-models](../.agents/skills/chem-quantum-models/SKILL.md) | 3 | 0 |
| **Total** | **70** | **339** |

These 339 interfaces come from 32 approved source modules. Two helper-module
copies support cross-module imports without exposing additional public
functions. An unsupported variadic function, `chemometrics_tools.one_way_anova`,
is not exposed by the keyword-only JSON interface; it remains in the source
library. Undocumented, retired, test, and policy-excluded functions are not
advertised. A count of available functions is not a count of independently
verified algorithms.

## Use In Codex

Open a new Codex task in this repository so its skill catalog includes the new
packages. Ask a chemistry question normally, or explicitly invoke a skill:

```text
Use $chem-aqueous-equilibria to check the speciation and charge balance in this calculation.
Use $chem-spectroscopy to distinguish the possible NMR assignments.
```

The descriptions define the task boundaries. `SKILL.md` links to individual
procedures, each retaining its applicability conditions, complete steps, and
guards. Codex should read only the relevant references. Related subproblems can
use more than one skill. Automatic discovery does not guarantee correct
selection; explicit invocation is useful when testing the package itself.

This follows [Codex's native skill mechanism](https://learn.chatgpt.com/docs/build-skills).
The packages do not choose a model or reasoning effort; those remain Codex
settings. They do not need a separate provider key or a running ChemTester
service. No user-wide installation, model-setting change, public push, or
benchmark launch is performed by the exporter.

## Optional Calculators

Ten packages include a small, standalone `scripts/calculate.py` interface.
It lists, describes, and explicitly invokes a selected function; it does not
decide which function to use. Full argument documentation and contracts are
available through `--describe`. Paths are relative to the skill, not the
working directory of the task.

```powershell
python .agents/skills/chem-thermodynamics/scripts/calculate.py --describe enthalpy_tools.heat_phase_change
python .agents/skills/chem-thermodynamics/scripts/calculate.py --call enthalpy_tools.heat_phase_change --arguments-json '{"moles":2,"delta_H_phase":10}'
```

Python 3.10+ is required. Some array, fitting, and chemometrics functions need
NumPy, SciPy, or scikit-learn, recorded in the affected package's
`requirements.txt`. Dependency versions are not pinned by this export. Nothing
is silently installed. JSON arrays are converted to NumPy arrays only for
parameters explicitly annotated as such.

The interface rejects unknown/inactive functions, argument-binding errors,
non-finite numbers, null/error results, and violations of recorded contracts.
The existing six-formula balancing bound is preserved. Two additional lattice
contracts reject unsupported cell labels and nonpositive dimensions rather
than accepting the legacy zero sentinel. Module content is copied without
semantic rewriting; line endings are normalized for the public repository.
These checks are not a complete domain audit of every function.

## What Was Preserved

- The full `chem-memory` source corpus, original L2 documents, L3 modules, source
  provenance, and retired-material records stay where they were. Historical
  corpus counts are not the number of native skills.
- The native reference payload contains the 70 active procedures, not every
  textbook note. The broader L2/L4 library has not been copied wholesale or
  automatically indexed into the native skills. A need for an additional
  substantive reference should lead to a reviewed, scoped addition.
- Historical evidence records, previous predictions, benchmark keys, raw
  question sets, and retired entries are not included in the native packages.
  General safeguards against reading such records remain in the instructions.
- Registry resource pointers and source/file SHA-256 hashes are recorded in
  [the export manifest](../.agents/native_chemistry_skills.manifest.json), outside
  the model-facing skill folders. Source leads are not automatically certified
  reference answers.
- Router V2/V2.1 experiments and frozen snapshots are retained as research
  artifacts. This export does not read question files, mutate experiment state,
  change historical scores, or control a running worker.

## Maintenance

The editorial grouping is in
[`configs/native_chemistry_skills.json`](../configs/native_chemistry_skills.json).
It is a build-time coverage map, not a runtime selector. Each active capability
must have exactly one owner. New or retired capabilities require an explicit
mapping change; mismatches stop the build.

```powershell
python scripts/chemistry_expert/export_native_chemistry_skills.py
python scripts/chemistry_expert/export_native_chemistry_skills.py --check
```

Maintain scientific content in its canonical reviewed source, and packaging
instructions in the configuration or exporter. Rebuild rather than hand-edit
generated packages. The exporter refuses to overwrite locally edited files or
remove unexpected/stale files. Unrelated installed skills are left untouched.

Source module copying preserves existing attribution headers. This export is
not a new licensing determination; confirm redistribution obligations before
any public release. The manifest alone is not a substitute for source licenses.

## Validation Boundary

On 2026-09-07, **69 focused release tests passed** in a clean publication
worktree using the local `pytorch_cuda12` environment. All 339 advertised
callables imported from standalone package copies, and the installed export
also passed its read-only `--check` verification. The wider source-workspace
router/native regression suite reported **203 tests and 5 subtests passed**.
These are engineering checks, not chemistry benchmark questions.

The delivery is checked for complete capability coverage, deterministic output,
source hashes, local links, native YAML/frontmatter, inactive-tool exclusion,
local-edit preservation, portable imports, JSON contracts, and synthetic
calculator examples. No new model predictions or evaluation questions are
needed for these checks.

Native Codex activation quality, selection accuracy, and task-level gains are
being evaluated separately. Historical Router V2 scores do not measure this new
delivery path. Publish completed benchmark artifacts only after their integrity
and paired comparison are audited. Keep benchmark-key access in a separate
scoring process, never in the answering agent's context.
