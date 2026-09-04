# Self-Assembly

## Concept Overview
Self-assembly is the spontaneous organization of molecules into ordered, functional structures driven by non-covalent interactions. Core principle: components contain encoded instructions for assembly.

## Key Principles

### Thermodynamics of Self-Assembly
```
nA â Aâ  (e.g., micelle formation)
K = [Aâ]/[A]â¿
ÎGÂ° = -RT ln K = ÎHÂ° - TÎSÂ°
```
Entropy often increases through hydrophobic effect (water release) despite reduced translational entropy of assembled species.

### Critical Micelle Concentration (CMC)
For amphiphiles in solution:
```
CMC â exp(ÎG_micellization / RT)
```
Below CMC: monomers; Above CMC: micelles (spherical â cylindrical â bilayer as concentration increases).

### Cooperative Effects
- **Isothermal titration calorimetry (ITC)** reveals stepwise vs. all-or-none binding
- **Chelate effect (supramolecular)**: multivalent binding >> sum of individual interactions
- **Allosteric cooperativity**: binding at one site affects affinity at another

### Self-Assembly Types

| Type | Driving Forces | Typical Size | Examples |
|------|---------------|-------------|----------|
| Micelles | Hydrophobic effect | 2-10 nm | SDS, CTAB |
| Vesicles/Liposomes | Hydrophobic + packing parameter | 50 nm-Î¼m | Phospholipid bilayers |
| SAMs | Chemisorption (Au-S) + van der Waals | ~1 nm thick | Alkanethiols on Au |
| Supramolecular polymers | H-bonding, Ï-Ï stacking, metal-ligand | nm-Î¼m | UPy dimers, pillarene threads |
| Liquid crystals | Anisotropic shape + dispersion | Î¼m domains | 5CB, calamitic LCs |
| Metal-organic frameworks | Coordination bonds | Î¼m crystals | ZIF-8, MOF-5 |

### Packing Parameter (Israelachvili)
```
g = v / (aâ Ã l_c)
g < 1/3: spherical micelles
1/3 < g < 1/2: cylindrical micelles
1/2 < g < 1: vesicles/bilayers
g â 1: planar bilayers
g > 1: inverted structures
```
v = tail volume, aâ = headgroup area, l_c = tail length

### Supramolecular Polymers
- **Hydrogen-bonded**: UPy (ureidopyrimidinone), Hamilton wedge
- **Ï-Stacked**: perylene bisimide, aromatic amide
- **Host-guest**: crown-ether/ammonium, cyclodextrin/adamantane
- **Metal-ligand**: terpyridine/ZnÂ²âº, phenanthroline/Cuâº

### Self-Assembled Monolayers (SAMs)
Alkanethiols on gold: chemisorption via Au-S bond, chain packing via van der Waals. Applications: biosensors, surface patterning, molecular electronics.

## L3 Tools
-> `../L3_functions/supramolecular_tools.py` â `self_assembly_cmc()`

## L4 Reference
-> `../L4_reference/supramolecular_data.csv`

## L5 Examples
-> `../L5_examples/supramolecular_examples.md` â Examples 3

---

## Source Attribution: Schaller, Structure and Reactivity, Ch12.8 (LibreTexts)
[Source: Schaller, Ch12.8: Supramolecular Assemblies](https://chem.libretexts.org/Bookshelves/General_Chemistry/Book:_Structure_and_Reactivity_in_Organic_Biological_and_Inorganic_Chemistry_(Schaller)/I:__Chemical_Structure_and_Properties/12:_Macromolecules_and_Supramolecular_Assemblies/12.08:_Supramolecular_Assemblies)

### Methods of Supramolecular Assembly Formation
1. **Hydrogen bonding**: Bert Meijer's graft copolymers; pendant chains attached via H-bonds; increased entanglement reduces diffusion.
2. **Host-guest interactions**: Cyclodextrin/amine systems; form elastic self-healing gels when cut pieces rejoin.
3. **Coordination chemistry**: Stephen Craig (Duke) ¡ª Pd(II) complexes crosslink poly(vinylpyridine); associative ligand exchange mechanism; Pd > Pt in binding constant Kb due to kinetic lability.

### Key Principles
- Supramolecular assemblies held by noncovalent interactions but very strong ones.
- Cross-linked architecture provides elasticity; flexible chains can distort but crosslinks restore original shape.
- Self-healing occurs because cut surfaces expose hosts/guests that can rebind.
- **Kinetic data**: Methyl-substituted ligands react faster than ethyl (less steric crowding at Pd center); square planar Pd(II) d? geometry.
