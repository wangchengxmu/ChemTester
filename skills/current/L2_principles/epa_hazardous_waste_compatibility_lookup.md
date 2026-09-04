# EPA hazardous-waste compatibility chart lookup

Use this support when a question names two broad reactivity groups from the
legacy EPA hazardous-waste compatibility chart. The authoritative method is
EPA-600/2-80-076, *A Method for Determining the Compatibility of Hazardous
Wastes* (U.S. EPA, April 1980).

For an exact class pair, call
`hazardous_waste_compatibility.lookup_chemical_storage_compatibility` with the
two visible class names. The function returns the published hazard codes and
their decoded consequences; do not reconstruct a cell from generic chemistry.

**Retrieval anchors:** chemical storage compatibility table; EPA hazardous-waste
reactivity groups; combustible and flammable materials, miscellaneous; metals,
alkali and alkaline earth, elemental; oxidizing or reducing agents; acids;
peroxides; polymerizable compounds.

## Procedure

1. Preserve both class names exactly. Do not substitute a neighboring group or
   a single representative compound.
2. Call `hazardous_waste_compatibility.lookup_chemical_storage_compatibility`
   with the two group names or their EPA group numbers.
3. Decode only the returned codes: H heat, F fire, G innocuous and
   non-flammable gas, GT toxic gas, GF flammable gas, E explosion, P violent
   polymerization, S solubilization of a toxic substance, and U hazardous but
   unknown.
4. Keep the categories independent. In particular, heat, fire, and explosion
   are not interchangeable consequences.
5. Treat a blank chart cell as unknown, not as proof of compatibility.

## Provenance and scope

- Official report landing page:
  https://www.epa.gov/hwpermitting/method-determining-compatibility-hazardous-wastes
- Public chart rendering used for the deterministic transcription:
  https://ipo.rutgers.edu/rehs/chemical-compatibilty-chart-epa
- Transcribed chart SHA-256:
  `398e58868d2c90f2e0f771617c49e48433564e981b09e8943b7cae729192c4a8`

The chart itself cautions that it is indicative rather than definitive or
exhaustive. Waste-specific composition and handling information still governs
real safety decisions.
