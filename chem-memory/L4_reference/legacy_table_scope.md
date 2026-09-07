# Legacy Reference Table Scope

The CSV files in this library are preserved historical transcriptions, not
independently validated reference datasets. Some use comments or multiple
sections and must not be read as one rectangular table without a declared
parser. The inventory in `configs/chemistry_reference_registry.json` records
their shape and verification status. None is enabled for generic machine lookup.

The electrode-potential and acid/base tables now have uniform schemas. This
repairs column interpretation and the hydrofluoric-acid/conjugate-base identity,
not the provenance of every numeric entry. A label such as "CRC" does not
identify an edition, table, solvent, temperature, pressure, standard state or
uncertainty. Preserve those unknowns instead of manufacturing source details.

For empirical use, require an independently checked source record with the
same species, units, scale, medium and conditions. A structurally valid table,
an available filename, or a finite calculator output does not establish that
its values are scientifically verified. Missing optional support is a warning;
it does not by itself invalidate an otherwise justified conclusion.
