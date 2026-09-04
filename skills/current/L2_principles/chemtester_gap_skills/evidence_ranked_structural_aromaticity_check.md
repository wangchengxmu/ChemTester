# Evidence-ranked transformation balance and aromaticity checks

**Retrieve with:** gem-dihalocyclopropane aromatization, dehydrohalogenation atom balance, Huckel aromatic circuit count, fused-ring pi electrons, mechanophore acid release

**Use when:** A structure or reaction question compares HX-release stoichiometry, aromatization, or π-electron claims after ring opening, elimination, or rearrangement, especially for gem-dihalocyclopropane or fused-ring substrates.

## Procedure

1. Map the visible structure or SMILES into rings and bonds, marking the attachment and possible fate of every halogen rather than counting halogen atoms alone.
2. For an indene-derived gem-dihalocyclopropane, consider ring opening followed by aromatizing loss of one HX while the other halogen remains in the fused aromatic product; confirm the actual coefficient by balancing substrate, product, and HX.
3. Identify the exact cyclic conjugated circuit named by each claim, verify cyclicity, planarity, and continuous conjugation, then count unique π electrons and apply 4n+2; distinguish a six-electron benzene-like circuit from the total count of a larger fused system.
4. Evaluate every candidate independently and prefer atom-balanced or directly structure-derived claims over exact supramolecular topology or contact counts unsupported by the supplied structure.

## Preferred Support

- chem-memory/L2_principles/aromatic_chemistry.md
- chem-memory/L2_principles/organic_reaction_mechanisms.md

## Guards

- Never equate the number of substrate halogens with the number of HX molecules released.
- Do not mix a local ring-circuit π count with the unique-electron count of an entire fused aromatic system.
- Do not require lowercase aromatic SMILES notation; a Kekule-form alternating ring may sanitize as aromatic.
- Do not infer exact hydrogen-bond dimensionality or contact counts from viscosity behavior or incomplete structural evidence.
