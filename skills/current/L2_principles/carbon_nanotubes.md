---
id: carbon_nanotubes
layer: 2
title: Carbon Nanotubes (CNTs)
up_links:
  - ./nanomaterials_overview.md
down_links:
  - ../L3_functions/nanomaterials_tools.py
cross_links:
  - ./fullerenes_buckyballs.md
  - ./band_theory.md
  - ./microscopy.md
  - ./raman_spectroscopy.md
source: Wikibooks Nanotechnology Ch04 - Semiconducting Nanostructures
---

## Context

Carbon nanotubes are cylindrical nanostructures consisting of rolled graphene sheets. They exhibit extraordinary mechanical, electrical, and thermal properties. Single-walled carbon nanotubes (SWCNTs) have diameters of ~0.4-3 nm, while multi-walled carbon nanotubes (MWCNTs) consist of concentric shells with diameters up to hundreds of nanometers.

---

## Geometric Structure

### Single-Walled Carbon Nanotubes (SWCNT)

Conceptually formed by wrapping a single graphene sheet into a cylinder.

#### Graphene Lattice

- Hexagonal structure from **sp² hybridization**
- Three directional σ bonds separated by 120°
- π electrons determine electronic properties

#### Chiral Vector

The nanotube structure is uniquely defined by the chiral vector **C**:

```
C = n·a₁ + m·a₂

Where:
- a₁, a₂ = graphene unit vectors
- (n,m) = integer indices (chiral indices)
- C connects equivalent lattice points
```

#### Diameter Formula

```
d = √3 × a_C-C × √(m² + n² + mn) / π

Where:
- a_C-C = C-C bond length = 1.42 Å
- Typical SWCNT diameters: 0.4-3 nm
```

### Classification by Chirality

| Type | Chiral Angle θ | Chiral Indices | Electronic Type |
|------|----------------|----------------|-----------------|
| **Zig-zag** | θ = 0° | (n,0) | Metallic if n divisible by 3 |
| **Armchair** | θ = 30° | (n,n) | Always metallic |
| **Chiral** | 0° < θ < 30° | (n,m) | Metallic if (n-m) = 3j |

**Chiral angle calculation:**
```
θ = tan⁻¹(√3m / (2n + m))
```

### Multi-Walled Carbon Nanotubes (MWCNT)

#### Structure

- Multiple concentric SWCNT shells
- Intershell spacing: ~0.34 nm (similar to turbostratic graphite)
- Diameters: 2-100+ nm
- Number of shells: 2-50+

#### Intershell Interaction

- Adjacent shells are generally **non-commensurate** (different chiralities)
- Weak inter-shell coupling
- Electrical transport dominated by outermost shell

---

## Electronic Structure

### Graphene as Reference

- Zero-gap semiconductor (semimetal)
- π and π* bands meet at six K points in Brillouin zone
- Fermi level at K points

### Nanotube Band Structure

When graphene is rolled into a tube, **periodic boundary conditions** restrict allowed wave vectors to discrete lines in the Brillouin zone.

#### Metallic vs Semiconducting Criterion

**Metallic if:**
- Allowed wave vectors pass through K point
- Condition: **(n - m) = 3j** (where j is integer)

**Semiconducting if:**
- (n - m) ≠ 3j
- Bandgap inversely proportional to diameter

### Bandgap Formula

For semiconducting SWCNTs:
```
E_g = k/d

Where:
- k = 0.7-0.8 eV·nm (experimentally determined)
- d = nanotube diameter in nm
```

**Example calculations:**
| (n,m) | Diameter (nm) | Bandgap (eV) | Type |
|-------|---------------|--------------|------|
| (10,10) | 1.36 | 0 | Metallic (armchair) |
| (10,0) | 0.78 | ~1.0 | Semiconducting |
| (15,0) | 1.17 | ~0.67 | Semiconducting |
| (9,0) | 0.70 | Small gap | Small-gap semiconducting |

### Small-Bandgap Semiconducting Tubes

When (n - m) = 3j but (n,m) ≠ (n,n):
- Wave vectors cross K point
- Curvature effects cause small band opening
- Bandgap: few to tens of meV
- Often considered metallic at room temperature

### Population Statistics

Based on chirality:
- **1/3 metallic** (including small-gap)
- **2/3 semiconducting**

---

## Electrical Properties

### Landauer Formula

For a 1-dimensional conductor:
```
G = G₀ × Σᵢ Tᵢ

Where:
- G₀ = 2e²/h = (12.9 kΩ)⁻¹ (conductance quantum)
- Tᵢ = transmission coefficient of channel i
- Each metallic nanotube: 2 conducting channels
- Ideal metallic SWCNT: G = 2G₀ = (6.5 kΩ)⁻¹
```

### Conductance Mechanisms

| Type | Mechanism | Conductance |
|------|-----------|-------------|
| Metallic | Ballistic transport | G = 2G₀ |
| Semiconducting | Thermally activated | Temperature dependent |
| MWCNT | Multiple parallel shells | Complex behavior |

### Temperature Dependence

**Metallic SWCNT:**
- Weak temperature dependence
- Ballistic transport over μm lengths at low T
- Phonon scattering at high T

**Semiconducting SWCNT:**
- Strong temperature dependence
- Thermally activated carriers
- Bandgap measurable from Arrhenius plot

---

## Mechanical Properties

### Exceptional Properties

| Property | Value | Comparison |
|----------|-------|------------|
| Tensile strength | 50-150 GPa | Steel: 0.4-2 GPa |
| Young's modulus | ~1 TPa | Steel: 0.2 TPa |
| Density | 1.3-1.4 g/cm³ | Steel: 7.8 g/cm³ |
| Specific strength | 100× steel | Highest known |

### Mechanism

- Strong C-C covalent bonds (sp² hybridization)
- No grain boundaries (single crystal)
- Hexagonal network distributes stress

---

## Thermal Properties

| Property | Value | Notes |
|----------|-------|-------|
| Thermal conductivity | 3000-6000 W/m·K | Higher than diamond |
| Thermal stability | Up to 750°C in air | Higher in inert atmosphere |
| Heat capacity | Similar to graphite | Size-dependent |

---

## Synthesis Methods

### 1. Arc Discharge

**Process:**
- High current (~100 A) between graphite electrodes
- Carbon vaporized at ~3000°C
- Nanotubes form on cathode

**Products:**
- High-quality SWCNTs (with metal catalyst)
- MWCNTs (without catalyst)
- By-products: fullerenes, amorphous carbon

### 2. Laser Ablation

**Process:**
- Pulsed laser vaporizes graphite target
- Metal catalyst (Co, Ni) present
- Carrier gas (Ar, He) transports vapor

**Products:**
- High-quality SWCNTs
- Relatively uniform diameter
- Expensive method

### 3. Chemical Vapor Deposition (CVD)

**Process:**
- Carbon source (CH₄, C₂H₄, CO)
- Metal catalyst nanoparticles (Fe, Co, Ni)
- Temperature: 500-1000°C
- Growth on substrate

**Advantages:**
- Scalable
- Controlled growth
- Aligned arrays possible

**Types:**
- Thermal CVD
- Plasma-enhanced CVD (PECVD)
- Floating catalyst CVD

### 4. High-Pressure Carbon Monoxide (HiPco)

**Process:**
- CO gas at high pressure (10-100 atm)
- Fe(CO)₅ as catalyst precursor
- Temperature: 800-1200°C

**Products:**
- SWCNTs with small diameter (0.8-1.2 nm)
- High purity
- Commercial process

---

## Characterization

### Microscopy

| Technique | Information |
|-----------|-------------|
| TEM | Diameter, number of walls, defects |
| SEM | Morphology, alignment |
| AFM | Height, length, mechanical properties |
| STM | Atomic structure, electronic density of states |

### Spectroscopy

#### Raman Spectroscopy

**Key bands:**

| Band | Position (cm⁻¹) | Information |
|------|----------------||----------|
| Radial breathing mode (RBM) | 100-300 | Diameter (ω_RBM ∝ 1/d) |
| D band | ~1350 | Defects, disorder |
| G band | ~1580 | Graphitic structure |
| G' (2D) | ~2700 | Electronic structure |

**Diameter from RBM:**
```
d (nm) = 248 / ω_RBM (cm⁻¹)

For isolated SWCNTs
```

#### Photoluminescence

- Emission from semiconducting SWCNTs
- Exciton transitions (E₁₁, E₂₂)
- Chirality identification
- Not applicable to metallic CNTs

#### UV-Vis-NIR Absorption

**Characteristic peaks:**
- Metallic tubes: M₁₁ ~ 400-600 nm
- Semiconducting tubes: S₁₁ ~ 800-1600 nm, S₂₂ ~ 600-900 nm
- Used for purity assessment

---

## Applications

### Electronics

1. **CNT Transistors (CNTFETs)**
   - High mobility
   - Ballistic transport
   - Challenges: chirality control, contacts

2. **Interconnects**
   - High current capacity (10⁹ A/cm²)
   - Lower resistivity than Cu at nanoscale

3. **Sensors**
   - Chemical: gas adsorption changes conductance
   - Biological: functionalized CNTs for detection
   - Mechanical: strain sensors

### Composites

1. **Structural**
   - Enhanced strength and stiffness
   - Aerospace, automotive applications
   - 1-5 wt% CNT loading typical

2. **Conductive**
   - EMI shielding
   - Antistatic materials
   - Transparent conductors

3. **Thermal**
   - Thermal interface materials
   - Heat spreaders

### Energy

1. **Batteries**
   - Anode material
   - Conductive additive

2. **Supercapacitors**
   - High surface area electrodes
   - Power density enhancement

3. **Fuel Cells**
   - Catalyst support
   - Electrode material

### Biomedical

1. **Drug Delivery**
   - Functionalized CNTs
   - Targeted delivery

2. **Imaging**
   - Photoacoustic imaging
   - Near-IR fluorescence

3. **Tissue Engineering**
   - Scaffolds
   - Electrical stimulation

---

## Challenges

### Synthesis

1. **Chirality Control**
   - Current methods produce mixture
   - Separation techniques available but costly
   - Selective synthesis under development

2. **Purity**
   - Metal catalyst residues
   - Amorphous carbon
   - Defects

3. **Scale**
   - Laboratory to industrial scale
   - Cost reduction needed

### Processing

1. **Dispersion**
   - Hydrophobic nature
   - Surfactants, functionalization
   - Aggregation issues

2. **Alignment**
   - Random vs aligned arrays
   - Electric/magnetic field alignment
   - Flow alignment

3. **Contact Resistance**
   - Metal-CNT interface
   - Schottky barriers
   - Annealing, doping

---

## Decision Flow

**Choosing CNT type for application:**

1. **Electrical conduction needed?**
   - Yes → Metallic CNTs or MWCNTs
   - Semiconducting → Semiconducting SWCNTs
   - Mixed OK → As-produced mixture

2. **Mechanical properties critical?**
   - Yes → SWCNTs (higher specific strength)
   - Cost sensitive → MWCNTs (cheaper)

3. **Thermal management?**
   - Individual CNTs → SWCNTs (highest conductivity)
   - Composites → MWCNTs (easier dispersion)

4. **Transparency needed?**
   - Yes → Thin SWCNT films
   - No → Any type

---

## Cross-References

**Related nanomaterials:**
- Fullerenes: [fullerenes_buckyballs.md](./fullerenes_buckyballs.md)
- Nanomaterials Overview: [nanomaterials_overview.md](./nanomaterials_overview.md)

**Characterization:**
- Raman Spectroscopy: [raman_spectroscopy.md](./raman_spectroscopy.md)
- Microscopy: [microscopy.md](./microscopy.md)

**Fundamental concepts:**
- Band Theory: [band_theory.md](./band_theory.md)
