# Water-assisted N-aryl ketonitrone–alkyne cascade mapping

**Retrieve with:** N-aryl unsaturated ketonitrone activated alkyne, formal [5+2] nitrone catalytic water, C3-quaternary indolenine C=N, nitrone alkyne atom mapping

**Use when:** An N-aryl alpha,beta-unsaturated ketonitrone reacts with an electron-poor alkyne and candidate products share global formula or ring-count constraints but differ in connectivity after a water-assisted seven-membered intermediate.

## Procedure

1. Label the nitrone carbon and oxygen, conjugated alpha/beta carbons, N-aryl ipso and ortho atoms, and both alkyne carbons and substituents; maintain a bond-change and atom-fate table.
2. Test stepwise oxygen addition, formal [5+2] closure, and nitrone C=N geometry adjustment leading to a seven-membered intermediate instead of defaulting to an ordinary [3+2] cycloadduct.
3. When trace or catalytic water is stated, place hydrolysis of the cyclic iminium/acetal-like intermediate before or adjacent to the [3,3] rearrangement; require the resulting carbonyl-bearing open-chain connectivity and regeneration of water during condensation.
4. Carry the [3,3] rearrangement, tautomerization, and intramolecular condensation to completion; verify a C3-quaternary indolenine by an explicit fused five-membered ring containing C=N and a quaternary C3, distinguishing it from an NH indoline.
5. Filter candidate structures by formula and ring count, then compare exact nitrone-derived carbonyl-tether connectivity and placement of the activated-alkyne substituents; settle connectivity before stereochemistry.

## Preferred Support

- chem-memory/L3_functions/rdkit_structure_tools.py

## Guards

- Do not assign an indolenine label from visual resemblance; explicitly locate the ring C=N bond and quaternary C3.
- Matching molecular formula and total ring count cannot distinguish constitutional isomers.
- Do not treat a trace-water cue as generic proton transfer when the proposed cascade contains a hydrolysis step.
- Do not use stereochemical wedges as tie-breakers until constitution and functional-group placement agree.
