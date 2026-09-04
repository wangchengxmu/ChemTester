# Crystal Engineering & Porous Materials

## Concept Overview
Crystal engineering designs solid-state structures through predictable non-covalent interactions (supramolecular synthons). Porous materials include metal-organic frameworks, covalent organic frameworks, hydrogen-bonded organic frameworks, and porous organic cages.

## Key Principles

### Supramolecular Synthons
Reusable structural motifs that reliably form specific interactions:
```
Carboxylic acid dimer:  R-COOH···HOOC-R  (O-H···O, ~2.7 Å)
Amide ribbon:  N-H···O=C, N-H···O=C  (parallel chains)
Pyridine-carboxylic acid:  N···H-O, ~2.6 Å
Halogen bond:  C-X···O/N  (X = Cl, Br, I)
```

### Hydrogen Bonding Networks
Ranking of common H-bond synthons (Desiraju):
1. Acid dimer (strongest, most directional)
2. Acid-pyridine heterosynthon
3. Amide-amide homosynthon
4. Alcohol-alcohol
5. N-H···π

### Coordination Polymers / MOFs
```
Metal node + organic linker → extended framework
Secondary Building Units (SBUs):  e.g., Zn₄O(CO₂)₆ in MOF-5

Key properties:
  Surface area:  1000-10000 m²/g
  Pore size:  3-30 Å (tunable via linker length)
  Applications:  gas storage, separation, catalysis
```

### Clathrates
Host frameworks trapping guest molecules without chemical bonds:
- **Gas hydrates**: water cages trapping CH₄, CO₂ (ice-like structures)
- **Hydroquinone clathrates**: trapping small molecules
- **Structure types**: I (sI), II (sII), H for gas hydrates

### Porous Organic Cages
Discrete molecules with intrinsic porosity (no extended framework needed):
```
Imine cage synthesis:  trialdehyde + diamine → [4+6] cage
Advantages: soluble, processable, amenable to solution processing
```

### Porosity Characterization
```
BET surface area:  N₂ adsorption at 77 K
Pore size distribution:  NLDFT, BJH methods
Langmuir surface area:  monolayer model
```

### Key Design Principles
- Reticular chemistry: predictable framework assembly from SBUs + linkers
- Isoreticular expansion: same topology, different linker lengths
- Post-synthetic modification (PSM): alter functionality after synthesis
- Flexible frameworks (breathing): stimuli-responsive pore opening

## L3 Tools
-> `../L3_functions/supramolecular_tools.py` — `cage_yield_calc()`

## L4 Reference
-> `../L4_reference/supramolecular_data.csv`

## L5 Examples
-> `../L5_examples/supramolecular_examples.md` — Examples 1-5 (various)
