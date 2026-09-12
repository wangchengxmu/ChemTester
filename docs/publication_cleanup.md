# Public branch cleanup

The public main and master branches now share the curated publication lineage.
The legacy project snapshot, internal draft document, machine-specific notes,
and uncurated textbook question batches are no longer part of either branch's
history. Existing curated preview tags and intentionally published benchmark
datasets are retained.

The active coupled-solubility procedure now states the assumptions required for
the squared-solubility regression. This is a scope correction, not a benchmark
result update. Historical skill snapshots remain unchanged for reproducibility.

Text-file checkout line endings are fixed to LF so byte-addressed native skill
manifests validate consistently on Windows.

Removing branch references does not guarantee removal of cached pages, forks,
or objects accessible through previously known commit identifiers.
