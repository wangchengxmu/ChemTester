# L2 Topic: Reticular Chemistry & MOF Basics

**Source**: Expert knowledge; Yaghi et al., Reticular Chemistry (2003); LibreTexts Inorganic Materials
**Created**: 2026-03-24
**Status**: Pass-1
**Parent**: N/A (new entry)

---

## Concept Overview

Reticular chemistry is the chemistry of linking molecular building blocks by strong bonds into extended structures. Metal-Organic Frameworks (MOFs) are crystalline porous materials built from metal ions/clusters (nodes) and organic linkers.

### Key Definitions

| Term | Definition |
|------|-----------|
| **MOF** | Crystalline porous polymer with metal nodes + organic linkers; permanent porosity via activation |
| **SBU** | Secondary Building Unit — inorganic cluster that serves as the structural node |
| **Topology** | Net type describing how SBUs and linkers connect (e.g., pcu, fcu, sod) |
| **Isoreticular** | Same topology with different linker lengths → systematic pore expansion |
| **RCSR** | Reticular Chemistry Structure Resource — database of topological nets |

---

## Common SBUs

| SBU | Composition | Geometry | Example MOF |
|-----|------------|----------|-------------|
| Zn₄O | Zn₄O(CO₂)₆ | Octahedral (6-c) | MOF-5 |
| Cu₂ paddlewheel | Cu₂(CO₂)₄ | Square planar (4-c) | HKUST-1 |
| Zr₆O₄(OH)₄ | Zr₆O₄(OH)₄(CO₂)₁₂ | Cuboctahedral (12-c) | UiO-66 |
| Cr₃O | Cr₃O(CO₂)₆ | Trigonal (6-c) | MIL-100/101 |
| Zn(N)₄ | Zn(mIm)₄ | Tetrahedral (4-c) | ZIF-8 |

---

## Topology

- **pcu** (primitive cubic): MOF-5 — 6-c octahedral + linear linker
- **nbo** (NbO): ZIF-8 — tetrahedral node + imidazolate linker (analogous to zeolite sodalite)
- **fcu** (face-centered cubic): UiO-66 — 12-c node
- **spn**: HKUST-1 — 4-c paddlewheel + 3-c BTC linker

### Isoreticular Expansion
Vary linker length while keeping topology constant: MOF-5 → IRMOF-1 through IRMOF-16 (linker from BDC → BPDC → TPDC etc.). Pore size increases systematically from ~8 Å to ~29 Å.

---

## Synthetic Methods (enhanced from review, PMC7826725)

### 1. Solvo(hydro)thermal (classic method)
- Closed vessels (autoclaves), 50-260°C, hours to days
- Common solvents: DMF, DEF, MeCN, MeOH, EtOH, H₂O, acetone
- Can form new ligands in situ
- Temperature affects morphology; slow cooling favors crystal growth

### 2. Slow Evaporation / Diffusion
- Room temperature, no energy input
- Diffusion: layers separated by solvent barrier; crystals form at interface
- Example: MOF-5 via diffusion of Et₃N into Zn(NO₃)₂/H₂BDC in DMF/chlorobenzene

### 3. Microwave-Assisted
- Faster crystallization (minutes vs. days)
- Better control of particle size
- Energy-efficient, scalable

### 4. Mechanochemical (Ball Milling)
- Solvent-free or minimal solvent (liquid-assisted grinding, LAG)
- Green method, no bulk solvent waste
- Rapid, amenable to scale-up

### 5. Electrochemical
- Metal ions supplied by anodic dissolution
- Continuous production possible
- Room temperature

### 6. Sonochemical
- Ultrasound promotes nucleation
- Smaller, more uniform particles

### 7. Iono-thermal
- Ionic liquids as solvent AND template
- Low vapor pressure, nonflammable, high thermal stability

### IUPAC Classification (2013)
- **Coordination polymer**: repeating coordination entities extending in 1-3D
- **Coordination network**: coordination polymer with specific topology
- **MOF**: sub-class of coordination network with potential voids

### Structural Factors
- Metal coordination geometry (varies with electronic structure)
- SBUs as nodes: enable topological design
- Organic linker: rigid vs. flexible (flexible → unpredictable structures)
- Common ligands: carboxylates, pyridyl, phosphonates, sulfonates, crown ethers
- Pore classification: nano (<20 Å), meso (20-500 Å), macro (>500 Å)
- Interpenetration: limits free pore space (favored by π-stacking ligands)

## L3 Tools
- `../L3_functions/mof_tools.py` → `topology_analysis()`, `framework_density_calc()`

## L4 Data
- `../L4_reference/mof_data.csv`

## L5 Examples
- `../L5_examples/mof_examples.md`

---

## [Source: Wikipedia, Metal–Organic Framework]

### MOF Definition & Scope
Metal–organic frameworks (MOFs) are crystalline porous materials consisting of metal ions/clusters coordinated to organic linkers, forming 1D, 2D, or 3D extended structures with permanent porosity.

### Key MOF Examples

| MOF | Metal Cluster | Linker | BET Surface Area (m²/g) | Key Feature |
|---|---|---|---|---|
| MOF-5 | Zn₄O | BDC (benzene-1,4-dicarboxylate) | ~3,800 | First highly porous MOF (Yaghi, 1999) |
| HKUST-1 | Cu₂(COO)₄ | BTC (benzene-1,3,5-tricarboxylate) | ~1,850 | Open metal sites, gas storage |
| UiO-66 | Zr₆O₄(OH)₄ | BDC | ~1,200 | Exceptional stability (Zr-oxo cluster) |
| MIL-101 | Cr₃O | BTC | ~4,000+ | Very high porosity, large pores |
| NU-1000 | Zr₆ | TBAPy (pyrene-based) | ~2,300 | Mesoporous, catalytic applications |

### Classification by Dimensionality
- 1D: Coordination polymers (chains/ladders)
- 2D: Layers (e.g., many Zn-based paddlewheel structures)
- 3D: True frameworks with permanent porosity

### Gas Storage Milestones
- CH₄ storage: MOF-5, MOF-177, MOF-210 exceeded DOE targets (2005–2010)
- H₂ storage: MOF-210 achieved ~17.6 wt% at 77 K, 80 bar
- CO₂ capture: Mg-MOF-74 (MM-74) shows ~8.9 wt% CO₂ at 1 bar, 25°C

---

## [Source: Wikipedia, Zeolite]
### Zeolites: Inorganic Porous Materials
Zeolites are microporous aluminosilicate minerals (framework: TO₄ tetrahedra, T = Si or Al) with uniform pore sizes (3–10 Å).

| Zeolite | Pore Size (Å) | Si/Al Ratio | Key Application |
|---|---|---|---|
| Zeolite A (LTA) | ~4.1 | ~1–5 | Detergent builder, ion exchange |
| Zeolite X/Y (FAU) | ~7.4 | 1–∞ | FCC cracking catalyst |
| ZSM-5 (MFI) | ~5.5 | 10–∞ | Hydrocarbon isomerization |
| Zeolite Beta (BEA) | ~6.6×6.7 | 5–100 | Alkylation, cracking |
| MCM-22 (MWW) | ~4.0×5.5 | 10–50 | Ethylation, aromatization |

- **Key property**: Framework negative charge (from Al³⁻ substitution for Si⁴⁺) balanced by exchangeable cations.
- **Catalysis**: ~40% of all petroleum refining uses zeolite catalysts.
- **Ion exchange**: Water softening, radioactive waste treatment, Cs⁺/Sr²⁺ capture.
- **SAPO-34**: Silicoaluminophosphate for methanol-to-olefins (MTO) process.

---

## [Source: Wikipedia, Covalent Organic Framework]
### COFs: Organic Porous Polymers
Covalent organic frameworks (COFs) are crystalline porous polymers formed entirely from light elements (C, H, N, O, B) linked by strong covalent bonds.

### Key COF Examples

| COF | Linkage | Functional Group | Surface Area (m²/g) |
|---|---|---|---|
| COF-1 | Boroxine (B₃O₃) | BO₃ | ~750 |
| COF-5 | Boronate ester | BO₂C₂ | ~1,590 |
| COF-300 | Imine | C=N | ~1,360 |
| TpPa-1 | β-ketoenamine | C=N/C=O | ~560 (very stable) |
| COF-42 | Imine | C=N | ~1,335 |

### Advantages over MOFs
- Higher chemical/thermal stability (no metal–ligand bonds to hydrolyze).
- Lighter elements → lower density.
- Tunable functionality through organic linker design.
- Applications: gas storage, catalysis, optoelectronics, drug delivery.

---

## [Source: Wikipedia, Porous Material]
### IUPAC Pore Classification
| Type | Pore Width | Examples |
|---|---|---|
| Microporous | < 2 nm | Zeolites, activated carbons, some MOFs |
| Mesoporous | 2–50 nm | MCM-41, SBA-15, some MOFs |
| Macroporous | > 50 nm | Porous glass, aerogels, some polymers |

### Key Mesoporous Materials
- **MCM-41** (Mobil, 1992): Hexagonal, 1.5–10 nm pores, surface area ~1000 m²/g.
- **SBA-15**: Larger pores (5–30 nm), thicker walls, higher hydrothermal stability.
- Synthesis: surfactant-templated sol-gel (liquid crystal template mechanism).
