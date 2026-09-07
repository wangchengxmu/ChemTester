# Early virtual-screening whole-profile comparison

## Applicability

Comparing molecular structures using generic oral-availability, drug-likeness, or small-molecule profile cues without target-specific potency data.

## Procedure

1. Build the same side-by-side profile for every candidate: molecular weight, cLogP, polar surface area, hydrogen-bond donors and acceptors, rotatable bonds, ring and aromatic burden, fraction sp3, and ionizable groups; for valid SMILES, prefer a parser-backed descriptor calculation.
2. Confirm successful parsing and each descriptor's domain separately: counts and surface areas may be zero, fractions may include zero, and cLogP may be negative. If parsing fails, label any structural proxies explicitly rather than accepting default descriptors.
3. Use Lipinski and Veber as coarse screens, then compare continuous margins and a consistently computed composite drug-likeness measure or whole-profile balance; treat several large adverse margins as material.
4. Separate solubility and salt-forming potential from permeability and exposure, then choose only after identifying which candidate wins each major dimension and any decisive liabilities.
5. Emit the requested leading option token followed by a concise rationale tied to the profile differences.

## Boundaries

- Do not let one favorable group or one binary threshold dominate several adverse continuous margins.
- Do not accept zero or default descriptors from a tool that did not parse the supplied SMILES.
- Use identical descriptor methods and protonation conventions across candidates.
- Do not infer potency, safety, or clinical bioavailability from generic drug-likeness descriptors.
- Use only available documented support; otherwise apply the explicit derivation or label missing empirical evidence unresolved. A library filename is not an executable tool.

Only calculators listed in this package's calculator reference are callable here.
Other filenames in a procedure are historical pointers, not installed dependencies.
For missing empirical support, obtain an authoritative source or state the uncertainty.
