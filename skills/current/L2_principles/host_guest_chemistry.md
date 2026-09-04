# Host-Guest Chemistry

## Concept Overview
Host-guest chemistry studies non-covalent interactions between a molecular "host" (cavity-containing molecule) and a "guest" (bound species). Central to supramolecular chemistry and molecular recognition.

## Key Principles

### Complementarity
Host and guest must match in:
- **Size/shape** — guest fits the cavity
- **Electrostatics** — charge-charge, dipole, H-bonding alignment
- **Solvation** — desolvation penalty offset by binding energy

### Preorganization Principle (Cram)
Preorganized hosts bind guests more strongly because less conformational reorganization is needed upon binding. Binding constant K reflects the degree of preorganization.

### Binding Constant
```
H + G ⇌ HG
K_a = [HG]/([H][G])  (association)
ΔG° = -RT ln K_a
ΔG° = ΔH° - TΔS°
```

### Major Host Families

| Host | Cavity (Å) | Key Guests | Ka (M⁻¹) typical |
|------|-----------|------------|-------------------|
| 12-crown-4 | 1.2-1.5 | Li⁺ | ~10² |
| 15-crown-5 | 1.7-2.2 | Na⁺ | ~10⁴ |
| 18-crown-6 | 2.6-3.2 | K⁺ | ~10⁶ |
| [2.2.2]cryptand | Variable | K⁺, Ba²⁺ | ~10¹⁰ |
| α-cyclodextrin | ~4.7 | Benzene | ~10² |
| β-cyclodextrin | ~6.0 | Naphthalene | ~10³ |
| γ-cyclodextrin | ~7.5 | Anthracene | ~10² |
| CB[6] | ~3.9 | Alkylammonium | ~10⁹ |
| CB[7] | ~5.4 | Viologen | ~10¹² |
| CB[8] | ~6.9 | Two guests | ~10¹¹ |
| p-tert-butylcalix[4]arene | ~1.0 | Small cations | ~10³-⁴ |

### Crown Ether Selectivity (Ionic Radius Match)
```
12-crown-4: Li⁺ (0.76 Å), Na⁺ (1.02 Å) → prefers Li⁺
15-crown-5: Na⁺ (1.02 Å), K⁺ (1.38 Å) → prefers Na⁺
18-crown-6: K⁺ (1.38 Å) → optimal fit
```

### Cryptands — Enhanced Selectivity
Three-dimensional encapsulation gives higher Ka (10⁸-10¹²) vs. crowns. [2.2.2]cryptand binds K⁺ with Ka ~ 10¹⁰ in water.

### Cyclodextrins
Glucose-based cyclic oligomers (α=6, β=7, γ=8 units). Hydrophobic cavity, hydrophilic exterior. Widely used in drug delivery and food chemistry.

### Cucurbiturils (CB[n])
Rigid, highly symmetric macrocycles from glycoluril + formaldehyde. Exceptional binding affinities (CB[7] > 10¹² M⁻¹ for viologen derivatives).

### Calixarenes
Phenol-formaldehyde macrocycles. Tunable via rim functionalization. p-tert-butylcalix[4]arene = classic example.

## L3 Tools
-> `../L3_functions/supramolecular_tools.py` — `binding_constant_calc()`, `host_guest_stoichiometry()`

## L4 Reference
-> `../L4_reference/supramolecular_data.csv` — binding constants, cavity sizes, pKa values

## L5 Examples
-> `../L5_examples/supramolecular_examples.md` — Examples 1-2

---

## Source Attribution: Schaller, Structure and Reactivity, Ch12.8 (LibreTexts)
[Source: Schaller, Ch12.8: Supramolecular Assemblies](https://chem.libretexts.org/Bookshelves/General_Chemistry/Book:_Structure_and_Reactivity_in_Organic_Biological_and_Inorganic_Chemistry_(Schaller)/I:__Chemical_Structure_and_Properties/12:_Macromolecules_and_Supramolecular_Assemblies/12.08:_Supramolecular_Assemblies)

### Host-Guest Complexes
- Host-guest complexes: one molecule has a cavity/opening for another molecule to fit inside (like basketball in peach basket).
- Physical attraction (intermolecular forces) may exist but isn't required �� steric confinement alone can stabilize complexes.
- **Julius Rebek (Scripps)**: Developed host complexes holding normally aloof guests such as N?; guest must take particular escape path.
- **Taichi Ikeda (NIMS, Japan)**: Polymer host-guest system where cyclodextrin hosts bind positively charged amine guests; forms elastic, self-healing gels via cross-linked supramolecular architecture.

### DNA as Supramolecular Assembly
- DNA: Each strand = alternating sugar-phosphate copolymer with pendant bases (A, C, G, T).
- Two strands form helical assembly through preferential H-bonding: T-A and C-G.
- Supramolecular = held together by strong noncovalent interactions, not covalent bonds.

### Bert Meijer (Eindhoven): H-Bonding Assemblies
- Graft copolymers assembled via hydrogen bonds: pendant chains on polymer backbone.
- Higher entanglement → lower diffusion coefficient → higher viscosity (D inversely related to viscosity).

---

## Source Attribution: Wikipedia

### [Source: Wikipedia, Crown Ether]
Crown ethers are cyclic oligomers of ethylene oxide (−CH₂CH₂O−). Naming: first number = total ring atoms, second = number of oxygen atoms.

| Crown Ether | Cavity Size (Å) | Favored Ion | Effective Ion Radius (Å) |
|---|---|---|---|
| 12-crown-4 | 0.60–0.75 | Li⁺ | 0.76 |
| 15-crown-5 | 0.86–0.92 | Na⁺ | 1.02 |
| 18-crown-6 | 1.34–1.55 | K⁺ | 1.38 |
| 21-crown-7 | 1.70–2.10 | Cs⁺ | 1.67 |

- Cavity size must match ion radius for optimal binding (macrocyclic effect + chelate effect).
- 18-crown-6 also binds protonated amines via 3 H-bonds between NH₃⁺ hydrogens and crown ether oxygens.
- Crown ethers enable phase transfer catalysis: hydrophobic exterior allows solubility in nonpolar solvents.
- Discovered by Charles J. Pedersen (DuPont, 1967); Nobel Prize 1987.

### [Source: Wikipedia, Cyclodextrin]
Cyclodextrins (CDs) are cyclic oligosaccharides from starch enzymatic conversion. Toroidal shape with hydrophobic interior, hydrophilic exterior.

| Type | Glucose Units | Cavity Diameter (Å) | Water Solubility (g/L, 25°C) |
|---|---|---|---|
| α-CD | 6 | ~4.7–5.3 | 145 |
| β-CD | 7 | ~6.0–6.5 | 18.5 |
| γ-CD | 8 | ~7.5–8.3 | 232 |

- Drug delivery: CDs form inclusion complexes with hydrophobic drugs (itraconazole, nitroglycerin). FDA GRAS status.
- β-CD used as chiral stationary phase in HPLC. Used in Febreze (odor trapping) and dryer sheets.

### [Source: Wikipedia, Cucurbituril]
Cucurbit[n]urils are macrocyclic molecules from glycoluril units; pumpkin-shaped with rigid hydrophobic cavity.

| CB Type | Units | Cavity Volume (Å³) | Ka (max, M⁻¹) |
|---|---|---|---|
| CB[5] | 5 | ~82 | ~10⁴ |
| CB[6] | 6 | ~164 | ~10⁵ |
| CB[7] | 7 | ~279 | ~10¹⁵ |
| CB[8] | 8 | ~479 | ~10¹² |

- Extremely strong binding; prefer neutral/positively charged guests. Applications: drug delivery, molecular switches.

### [Source: Wikipedia, Calixarene]
Calix[n]arenes are phenolic macrocycles (p-alkylphenol + formaldehyde). Upper/lower rims independently functionalizable.
- Conformations: cone, partial cone, 1,2-alternate, 1,3-alternate.
- Applications: ion sensors, extraction agents, biomimetic receptors.

### [Source: Wikipedia, Macrocyclic Effect]
Enhanced stability of macrocyclic vs. acyclic complexes:
- Preorganization: macrocycle already in correct conformation (less entropy loss).
- Reduced solvation of free macrocycle (cavity shields donor atoms).
- Enhancement factor: typically 10²–10⁴× compared to acyclic analogues.
