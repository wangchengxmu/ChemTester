---
id: fullerenes_buckyballs
layer: 2
title: Fullerenes and Buckyballs
up_links:
  - ./nanomaterials_overview.md
down_links:
  - ../L3_functions/nanomaterials_tools.py
cross_links:
  - ./carbon_nanotubes.md
  - ./band_theory.md
  - ./main_group_chemistry_groups_13_16.md
source: Wikibooks Nanotechnology Ch04 - Semiconducting Nanostructures
---

## Context

Fullerenes are molecular allotropes of carbon with cage-like structures. The most famous is buckminsterfullerene (C₆₀), discovered in 1985. They represent zero-dimensional nanomaterials with unique electronic, optical, and chemical properties arising from their curved π-conjugated surfaces.

---

## Fundamental Structure

### Buckminsterfullerene C₆₀

**IUPAC name:** (C₆₀-Iₕ)[5,6]fullerene

**Structure:**
- Truncated icosahedron (soccer ball shape)
- 20 hexagons + 12 pentagons
- 60 carbon atoms at vertices
- Each carbon bonded to 3 neighbors

**Dimensions:**
- van der Waals diameter: ~1 nm
- Nuclear diameter: ~0.7 nm
- C-C bond lengths:
  - 6:6 ring bonds (hexagon-hexagon): 1.40 Å
  - 6:5 ring bonds (hexagon-pentagon): 1.46 Å
  - Average: 1.44 Å

### Structural Rule

**Euler's theorem for fullerenes:**
```
|V| - |E| + |F| = 2

Where:
- |V| = number of vertices (carbon atoms)
- |E| = number of edges (bonds)
- |F| = number of faces

Result: All fullerenes have exactly 12 pentagons
Number of hexagons = |V|/2 - 10
```

**For C₆₀:**
- |V| = 60
- Hexagons = 60/2 - 10 = 20
- Total faces = 12 pentagons + 20 hexagons = 32

### Stability Criterion

**Isolated Pentagon Rule (IPR):**
- Most stable fullerenes have no adjacent pentagons
- Adjacent pentagons cause strain and instability
- C₆₀ is the smallest fullerene satisfying IPR

---

## Types of Fullerenes

### By Carbon Number

| Fullerene | Formula | Structure | Notes |
|-----------|---------|-----------|-------|
| **C₂₀** | Smallest | Dodecahedron | 12 pentagons, no hexagons, highly strained |
| **C₆₀** | Most common | Truncated icosahedron | IPR satisfied |
| **C₇₀** | Common | Ellipsoidal | Similar to C₆₀ but elongated |
| **C₇₂, C₇₆, C₈₄** | Higher | Various isomers | Multiple stable isomers |
| **C₁₀₀+** | Giant | Complex cages | Many possible structures |

### Number of Isomers

The number of possible fullerene structures grows rapidly:

| Carbon Atoms | Number of Isomers | IPR-Satisfying |
|--------------|-------------------|----------------|
| C₆₀ | 1812 | 1 (the buckminsterfullerene) |
| C₇₀ | 8149 | 1 |
| C₈₀ | 31924 | 7 |
| C₁₀₀ | 285,914 | 450 |
| C₂₀₀ | 214,127,713 | 15,655,672 |

### Non-Carbon Fullerenes

#### Boron Buckyball (B₈₀)

- Predicted at Rice University
- More stable than C₆₀ (theoretically)
- Each atom forms 5-6 bonds
- Structure: triangles instead of hexagons
- Additional B atom in center of each 6-member ring
- **Controversy:** Later calculations suggest Th symmetry, not Iₕ

#### Silicon Buckyballs

- Created around metal ions
- Less stable than C fullerenes
- Form metallofullerenes

---

## Electronic Structure

### Molecular Orbital Diagram

C₆₀ has:
- 60 π electrons
- 30 occupied π molecular orbitals
- 30 unoccupied π* orbitals
- HOMO-LUMO gap: ~1.9 eV

### Electronic Properties

| Property | Value |
|----------|-------|
| HOMO-LUMO gap | 1.9 eV |
| Ionization energy | 7.6 eV |
| Electron affinity | 2.7 eV |
| Electrical behavior | Semiconductor |

### Consequences

1. **Semiconducting behavior**
2. **Can accept electrons easily** (good electron acceptor)
3. **Forms anions readily:** C₆₀ⁿ⁻ (n = 1-6)
4. **Useful for organic photovoltaics**

---

## Synthesis Methods

### 1. Arc Discharge

**Process:**
- High current between graphite electrodes
- Helium atmosphere
- Carbon vapor condenses

**Products:**
- C₆₀ (dominant)
- C₇₀ (~10-20%)
- Higher fullerenes (minor)
- Carbon soot

**Extraction:**
- Solvent extraction (toluene, benzene)
- Chromatographic separation

### 2. Laser Ablation

- Pulsed laser on graphite target
- Similar products to arc discharge
- Higher quality but lower yield

### 3. Combustion Synthesis

- Hydrocarbon flames under specific conditions
- Scalable
- Lower purity

---

## Properties

### Physical Properties

| Property | Value |
|----------|-------|
| Molecular weight (C₆₀) | 720.66 g/mol |
| Density (solid) | 1.65 g/cm³ |
| Sublimation point | ~800 K |
| Solubility in toluene | 2.8 mg/mL |
| Crystal structure (solid) | FCC (face-centered cubic) |

### Chemical Properties

#### Reactivity Patterns

1. **Electron acceptance:**
   ```
   C₆₀ + e⁻ → C₆₀⁻    EA = 2.7 eV
   C₆₀ + 6e⁻ → C₆₀⁶⁻
   ```

2. **Addition reactions:**
   - Hydrogenation: C₆₀H₃₆, C₆₀H₁₈
   - Halogenation: C₆₀Br₆, C₆₀Br₂₄
   - Cycloadditions: [2+2], [4+2] Diels-Alder

3. **Oxidation:**
   - Forms fullerene oxides (C₆₀O)
   - Epoxide formation

4. **Functionalization:**
   - Easily derivatized
   - Preserves cage structure
   - Water-soluble derivatives possible

#### Characteristic Reactions

**Diels-Alder cycloaddition:**
```
C₆₀ + diene → adduct

The reaction occurs at 6:6 bonds (higher double bond character)
```

**Prato reaction (1,3-dipolar addition):**
```
C₆₀ + azomethine ylide → fulleropyrrolidine

Common functionalization method
```

---

## Types of Fullerene Compounds

### 1. Endohedral Fullerenes

Atoms or molecules encapsulated inside the cage:

**Endohedral metallofullerenes:**
- M@C₆₀ (metal inside C₆₀)
- Sc₃N@C₈₀
- La@C₈₂

**Applications:**
- MRI contrast agents
- Radiopharmaceuticals

**Trimetaspheres:**
- C₈₀ cage with 3 metal atoms + 1 N atom
- Licensed to Luna Innovations
- Potential: imaging, therapy, solar cells

### 2. Exohedral Derivatives

Functional groups attached to the exterior:

- Fullerenols: C₆₀(OH)ₙ
- Fullerene esters
- Fullerene-polymer conjugates
- Water-soluble derivatives

### 3. Heterofullerenes

Carbon atoms replaced by other elements:

- C₅₉N (azafullerene)
- C₅₉B (borafullerene)
- Altered electronic properties

---

## Applications

### 1. Organic Photovoltaics (OPV)

**Mechanism:**
- C₆₀ derivatives as electron acceptors
- Polymer or small molecule as donor
- Bulk heterojunction architecture

**Performance:**
- Efficiencies up to 18% (with PCBM derivatives)
- Flexible, lightweight solar cells

### 2. Biomedical Applications

| Application | Fullerene Type | Mechanism |
|-------------|----------------|-----------|
| Antioxidant | Fullerenols | Radical scavenging |
| Drug delivery | Functionalized C₆₀ | Targeted delivery |
| Photodynamic therapy | C₆₀ derivatives | ROS generation |
| MRI contrast | Endohedral | Paramagnetic metals |
| HIV inhibition | C₆₀ derivatives | Enzyme binding |

### 3. Materials Science

1. **Superconductivity**
   - Alkali-doped: K₃C₆₀, Rb₃C₆₀
   - Tc up to 33 K (RbCs₂C₆₀)
   - Type-II superconductors

2. **Ferromagnetism**
   - TDAE-C₆₀
   - Organic ferromagnet

3. **Lubricants**
   - Molecular ball bearings
   - Low friction coefficient

### 4. Electronics

- Organic field-effect transistors (OFETs)
- Memory devices
- Sensors

---

## Characterization

### Spectroscopy

| Technique | Information |
|-----------|-------------|
| UV-Vis | Characteristic absorption at 213, 257, 329, 404, 450, 540, 570, 590, 625 nm |
| IR | 4 IR-active modes (T₁ᵤ): 527, 576, 1182, 1429 cm⁻¹ |
| Raman | 10 Raman-active modes (A₉ + H₉): 273, 437, 496, 710, 774, 1099, 1248, 1428, 1469, 1575 cm⁻¹ |
| NMR | ¹³C: single peak at 143 ppm (all carbons equivalent) |
| Mass spec | M⁺ peak at m/z 720 (C₆₀) |

### Microscopy

- **STM:** Imaging individual molecules
- **TEM:** Crystal structure in solid state
- **AFM:** Molecular manipulation

---

## Comparison: C₆₀ vs C₇₀

| Property | C₆₀ | C₇₀ |
|----------|-----|-----|
| Shape | Spherical | Ellipsoidal |
| Symmetry | Iₕ | D₅ₕ |
| Hexagons | 20 | 25 |
| Pentagons | 12 | 12 |
| Color (solution) | Magenta | Red-orange |
| HOMO-LUMO gap | 1.9 eV | 1.6 eV |
| Solubility (toluene) | 2.8 mg/mL | Higher |
| Stability | Higher | Lower |

---

## Mathematical Description

### Symmetry

**C₆₀ symmetry group: Iₕ**

- Icosahedral symmetry (60 rotational symmetry operations)
- 120 symmetry operations total (including reflections)
- Highest symmetry for a molecule

**Consequences:**
- Single ¹³C NMR peak
- Simplified vibrational spectrum
- All C-C bonds equivalent (on average)

### Graph Theory

Fullerenes are:
- **Planar graphs** (no crossing bonds)
- **3-regular graphs** (each vertex has degree 3)
- **Pentagon-hexagon faces only**

---

## Stability and Reactivity Trends

### Thermodynamic Stability

1. **Isolated Pentagon Rule (IPR)** satisfied
2. **Spherical shape** (strain distributed evenly)
3. **Maximal hexagon content** for given size

### Kinetic Stability

- Aromatic stabilization (60 π electrons)
- High activation barriers for cage opening
- Stable up to ~800 K

### Reactivity

**Most reactive sites:**
- 6:6 bonds (between hexagons)
- Higher double bond character
- Addition reactions preferentially here

---

## Decision Flow

**Choosing fullerene type:**

1. **Electron acceptor needed?**
   - Yes → C₆₀ or PCBM derivatives
   - No → Continue

2. **Water solubility needed?**
   - Yes → Fullerenols, functionalized derivatives
   - No → Pristine C₆₀

3. **Encapsulation needed?**
   - Yes → Endohedral fullerenes
   - No → Pristine or exohedral

4. **Size/shape flexibility?**
   - Yes → C₇₀ or higher fullerenes
   - No → C₆₀

---

## Cross-References

**Related nanomaterials:**
- Carbon Nanotubes: [carbon_nanotubes.md](./carbon_nanotubes.md)
- Nanomaterials Overview: [nanomaterials_overview.md](./nanomaterials_overview.md)

**Fundamental concepts:**
- Band Theory: [band_theory.md](./band_theory.md)
- Main Group Chemistry (Carbon): [main_group_chemistry_groups_13_16.md](./main_group_chemistry_groups_13_16.md)
