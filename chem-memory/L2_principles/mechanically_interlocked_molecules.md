# Mechanically Interlocked Molecules (MIMs)

## Concept Overview
MIMs are molecules with mechanical bonds — components are linked not by covalent bonds but by topological constraint. Includes rotaxanes, catenanes, and molecular knots.

## Key Principles

### Rotaxanes
- **Structure**: A "ring" threaded onto a "dumbbell" (axle with two bulky stoppers)
- **Components**: Macrocycle (wheel) + axle + two stoppers
- **Stability**: Requires stoppers larger than macrocycle cavity
- **Types**: [n]rotaxane (n = number of macrocycles per axle)

### Catenanes
- **Structure**: Two or more interlocked rings (like chain links)
- **[n]Catenane**: n interlocked macrocycles
- **Amide catenane** (Sauvage, Nobel 2016): Cu(I)-templated synthesis
- **First synthesis**: Sauvage, 1983, using phenanthroline-Cu(I) template

### Template-Directed Synthesis
```
Metal template:  Cu⁺ + 2 phenanthroline → preorganized for cyclization
Hydrogen-bond template:  Amide/amide H-bonds preorganize precursors
π-Stacking template:  Donor-acceptor π-π interactions
```
Key: the template provides entropic advantage by preorganizing components.

### Molecular Shuttles
 bistable rotaxane where the ring moves between two stations on the axle:
```
[Station A]---axle---[Station B] ← ring moves between A and B
Switching stimuli: redox (viologen), pH, light, chemical, temperature
```

### Molecular Machines (Nobel Prize 2016)
- **Sauvage**: catenane synthesis
- **Stoddart**: rotaxane-based machines, switches
- **Feringa**: molecular motors (unidirectional rotation)

### Switching Mechanisms
| Stimulus | Example | Mechanism |
|----------|---------|-----------|
| Redox | TTF/cyclobis(paraquat-p-phenylene) | TTF⁰ → TTF⁺⁺ changes affinity |
| Light | Azobenzene | trans → cis isomerization changes geometry |
| pH | Benzimidazole/ammonium | Protonation/deprotonation shifts binding |
| Chemical | Competitive guest | Displacement of ring from station |

### Mechanical Bond Properties
- Co-conformational freedom (relative motion between components)
-模板作用 (Template effect) increases yield dramatically
- Applications: molecular electronics, drug delivery, stimuli-responsive materials

## L3 Tools
-> `../L3_functions/supramolecular_tools.py` — `rotaxane_efficiency()`

## L4 Reference
-> `../L4_reference/supramolecular_data.csv`

## L5 Examples
-> `../L5_examples/supramolecular_examples.md` — Example 4

---

## [Source: Wikipedia, Rotaxane]
A rotaxane = macrocycle threaded on dumbbell-shaped axle with bulky stoppers. No covalent bonds between ring and axle.

- **Template-directed synthesis**: Crown ether/ammonium, π-π stacking, or metal coordination templates pre-organize ring and axle before stoppering.
- **Shuttling**: Ring moves between stations on the axle — basis for molecular machines.
- **Stimuli-responsive**: Light, pH, redox, or chemical stimuli switch ring position.
- Bravo, Raymo, Stoddart et al. (1998): high-yielding template-directed [2]rotaxane synthesis.

## [Source: Wikipedia, Catenane]
Catenane = two or more interlocked macrocyclic rings; cannot be separated without breaking covalent bonds.

- **First synthesis**: Schill & Lüttringhaus (1964), statistical approach, very low yield.
- **High-yield route**: Sauvage (1983) used Cu(I)-templated phenanthroline ligands → Nobel Prize 2016.
- Applications: molecular machines, switchable materials, topological materials.

## [Source: Wikipedia, Molecular Self-Assembly]
- **Intermolecular**: micelles, vesicles, liquid crystals, MOFs.
- **Intramolecular**: folding (foldamers, polypeptides).
- **Thermodynamic control** → most stable arrangement; weak reversible bonds enable error correction.
- Cyanuric acid–melamine lattice (Seto & Whitesides, 1993): hexagonal rosette via triple H-bonds.

## [Source: Wikipedia, Supramolecular Chemistry — Building Blocks]
### Recognition Motifs
- π-π CT: bipyridinium/viologen with dioxyarenes → rotaxanes, crystal engineering.
- Crown ether/ammonium: ubiquitous binding.
- Bipyridine/terpyridine + Ru²⁺/Ag⁺: complex architectures.
### Active Units
- Porphyrins/phthalocyanines: tunable photochemistry.
- Photochromic groups: light-triggered shape change.
- TTF/quinones: multiple oxidation states for redox devices.
