# Reaction-center stereochemical descriptor audit

**Retrieve with:** tertiary amide LDA enolate, amide enolate Z selectivity, amide versus ester enolate CIP, directional SMILES E Z

**Use when:** A reaction-product choice depends on enolate E/Z geometry or slash/backslash SMILES, especially when changing among ketone, ester, and amide substrates can change both selectivity and CIP interpretation.

## Procedure

1. Classify the carbonyl derivative and record base, counterion, solvent, temperature, and additives before applying any enolate-geometry trend.
2. For simple acyclic N,N-disubstituted amides under LDA in THF at low temperature, predict the predominantly Z lithium enolate unless substrate-specific evidence or geometry-altering additives indicate otherwise.
3. State the predicted same-side or opposite-side substituent relationship independently of the E/Z label.
4. Assign CIP priorities on each candidate graph and decode directional bonds with atom order and branch placement; use a deterministic stereochemistry parser when available.
5. Match the verified encoding to the predicted geometry, then emit the requested answer format.

## Preferred Support

- chem-memory/L2_principles/chemtester_gap_skills/reaction_center_stereochemical_descriptor_audit.md
- chem-memory/L3_functions/rdkit_structure_tools.py

## Guards

- Do not transfer a generic LDA-gives-E heuristic across ketones, esters, and amides.
- Slash and backslash are local relative bond directions, not standalone E/Z labels.
- Recompute CIP when the carbonyl heteroatom substituent changes; ester and amide enolates can map the same directional pattern differently.
- A structure parser validates representation but does not predict reaction selectivity.
