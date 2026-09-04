# Early virtual-screening whole-profile comparison

**Retrieve with:** matched SMILES descriptors, oral developability comparison, molecule profile burden, drug-likeness continuous margins, ionization permeability tradeoff

**Use when:** Comparing molecular structures using generic oral-availability, drug-likeness, or small-molecule profile cues without target-specific potency data.

## Procedure

1. Build the same side-by-side profile for every candidate: molecular weight, cLogP, polar surface area, hydrogen-bond donors and acceptors, rotatable bonds, ring and aromatic burden, fraction sp3, and ionizable groups; for valid SMILES, prefer a parser-backed descriptor calculation.
2. Before trusting calculated descriptors, confirm that every SMILES parsed and produced plausible nonzero values; otherwise make an explicit structural-proxy table using atom and halogen burden, rings, heteroatoms, flexibility, and ionization.
3. Use Lipinski and Veber as coarse screens, then compare continuous margins and a consistently computed composite drug-likeness measure or whole-profile balance; treat several large adverse margins as material.
4. Separate solubility and salt-forming potential from permeability and exposure, then choose only after identifying which candidate wins each major dimension and any decisive liabilities.
5. Emit the requested leading option token followed by a concise rationale tied to the profile differences.

## Preferred Support

- chem-memory/L2_principles/medicinal_chemistry_principles.md
- chem-memory/L2_principles/qsar.md
- chem-memory/L3_functions/rdkit_structure_tools.py

## Guards

- Do not let one favorable group or one binary threshold dominate several adverse continuous margins.
- Do not accept zero or default descriptors from a tool that did not parse the supplied SMILES.
- Use identical descriptor methods and protonation conventions across candidates.
- Do not infer potency, safety, or clinical bioavailability from generic drug-likeness descriptors.
