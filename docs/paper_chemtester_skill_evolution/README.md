# ChemTester Skill-Evolution Paper Package

## Main files

- `manuscript.md`: complete working manuscript.
- `project_truth.md`: frozen claims, counts, and prohibited interpretations.
- `supplementary/source_provenance_audit.md`: source-state definitions and coverage conclusions.
- `supplementary/libretexts_canonical_work_audit.csv`: one row per canonical named work.
- `supplementary/libretexts_live_catalog_audit.csv`: raw shelf rows, including aliases and containers.
- `supplementary/libretexts_live_catalog_snapshot.json`: machine-readable live API snapshot.
- `supplementary/libretexts_live_catalog_summary.md`: concise catalog summary.
- `supplementary/strict_multimodel_evaluation_protocol.md`: sealed-suite controls, hashes, model matrix, and reporting rules.
- `scripts/audit_libretexts_catalog.ps1`: reproducible live catalog audit.

## Current interpretation

The 4 September 2026 live audit found 139 immediate shelf entries and 129 canonical named works. Forty-two canonical works have an exact title or book-root trace in `chem-memory`; 87 do not. These are provenance-screening results, not a definitive binary reading ledger.
