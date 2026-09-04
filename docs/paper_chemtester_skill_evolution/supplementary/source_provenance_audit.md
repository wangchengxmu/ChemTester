# Source Provenance and Coverage Audit

## Scope

The intended source universe is the set of named book-level works in the eight curated Chemistry LibreTexts shelves, not a historical list of 25 books. The live snapshot on 4 September 2026 contains 139 immediate entries. After excluding six generic supplemental-module containers and collapsing four normalized alias groups, the catalog contains 129 canonical named works.

The complete row-level snapshot is in:

- `libretexts_live_catalog_audit.csv`
- `libretexts_canonical_work_audit.csv`
- `libretexts_live_catalog_snapshot.json`
- `libretexts_live_catalog_summary.md`

## Evidence states

| State | Operational definition | What may be claimed |
|---|---|---|
| Extracted | A retained record states that source content was processed into memory artifacts. | The documented content was processed. |
| Partial/delta | Only material judged novel or relevant was extracted. | The specified portions were processed; the book was not necessarily read in full. |
| Assessed/skipped | A source was reviewed for overlap or utility and intentionally not extracted. | The source was assessed, not incorporated completely. |
| Blocked | The source was unavailable, empty, or otherwise inaccessible. | Extraction was attempted but could not proceed. |
| Catalog-only | The source appears only as a discovered or recommended alternative. | The source was known, but reading is unproven. |
| Untraced | No exact normalized title or book-root trace was found. | Manual review is required; unread status is not proven. |

## Representative evidence

| Source or record | State | Repository evidence |
|---|---|---|
| Physical chemistry scan | Partial/delta | Records a first-pass chapter inventory and NEW/MATCH/DELTA/SKIP decisions. |
| Averill chapter mapping | Partial/delta | Maps chapters and records targeted extraction of new topics. |
| Oxtoby Unit 6: Materials | Assessed/skipped | Reports greater than 85% overlap and lists minerals, ceramics, pigments, and phosphors as not extracted. |
| Skoog, Principles of Instrumental Analysis | Blocked | Records a 404/under-construction placeholder with no extractable content. |
| Petrucci replacement search | Catalog-only for listed replacements | Establishes that the original path failed and identifies alternatives; the list alone does not prove extraction of those alternatives. |
| Harvey analytical chemistry | Extracted, title drift | Multiple local analytical-chemistry records use Harvey material, although the live title `Analytical Chemistry 2.1 by David Harvey` does not exactly match the retained paths. |
| Crystallography detailed extraction | Extracted from multiple sources | Records source URLs and derived crystallographic coverage. |

## Current screening result

| Measure | Count |
|---|---:|
| Immediate shelf entries | 139 |
| Generic supplemental-module containers | 6 |
| Named rows before alias collapse | 133 |
| Canonical named works | 129 |
| Exact title or book-root trace | 42 |
| No exact title or book-root trace | 87 |

The 87 no-trace works are candidates for manual provenance adjudication, not a definitive unread count. A title can be untraced because the page was renamed or moved. The 42 traced works also require manual state classification because a mention can reflect extraction, a failed attempt, an overlap assessment, or only a replacement recommendation.

## Answer to the completeness question

The retained artifacts do not support the claim that all books in the current online library were read. There are explicit examples of skipped and blocked sources, and most current canonical titles have no exact repository trace. The exact number never read cannot be recovered automatically from the current records. Establishing that number requires row-by-row adjudication against the six-state taxonomy above.

## Recommended ledger fields

A future source ledger should store one record for every canonical work with:

- stable source identifier and current URL;
- title and author as observed at retrieval;
- shelf and catalog snapshot date;
- license and terms snapshot;
- retrieval agent and software version;
- chapter-level state and completion date;
- extracted artifact identifiers;
- overlap decision and reason;
- access failures and replacement relationships;
- reviewer and adjudication timestamp.
