---
id: semiconducting_nanowires
layer: 2
title: Semiconducting Nanowires
up_links:
  - ./nanomaterials_overview.md
down_links:
  - ../L3_functions/nanomaterials_tools.py
cross_links:
  - ./carbon_nanotubes.md
  - ./band_theory.md
  - ./microscopy.md
  - ./nanomaterials_synthesis.md
source: Wikibooks Nanotechnology Ch04 - Semiconducting Nanostructures
---

## Context

Semiconducting nanowires are one-dimensional nanostructures with diameters of a few nanometers and lengths up to micrometers. They exhibit quantum confinement in two dimensions, unique electronic properties, and enable heterostructure formation. Key synthesis methods include vapor-liquid-solid (VLS) growth and metal organic vapor phase epitaxy (MOVPE).

---

## Fundamental Properties

### One-Dimensional Confinement

Nanowires confine electrons in two dimensions (radial) while allowing free motion along the wire axis:

```
Dimensions:
- Diameter: 1-100 nm (confined directions)
- Length: 1-100 μm (free direction)

Quantum confinement effects occur when:
diameter < exciton Bohr radius
```

### Density of States

**1D density of states:**
```
g(E) = (1/π) × √(2m*/ħ²) × 1/√E

Characteristics:
- Van Hove singularities at band edges
- Step-like density of states
- Different from 3D (√E) and 2D (step function)
```

### Size-Dependent Bandgap

Quantum confinement increases the bandgap:
```
E_g(nanowire) = E_g(bulk) + ħ²π²/(2R²) × (1/m_e* + 1/m_h*)

Where:
- R = nanowire radius
- m_e*, m_h* = effective masses
```

---

## Types of Semiconducting Nanowires

### Silicon Nanowires

**Properties:**
- Diameter: 2-50 nm typical
- Bandgap: 1.1 eV (bulk), size-tunable
- Crystal structure: Diamond cubic
- Surface: SiO₂ native oxide

**Applications:**
- Transistors (gate-all-around FETs)
- Sensors
- Photovoltaics
- Thermoelectrics

**Advantages:**
- CMOS compatible
- Abundant material
- Well-studied properties

**Challenges:**
- Indirect bandgap (weak optical properties)
- Surface recombination
- Oxide interface states

### III-V Nanowires

**Common materials:** GaAs, InP, GaP, InAs, GaN, InN

**Properties:**

| Material | Bandgap (eV) | Type | Key Features |
|----------|--------------|------|--------------|
| GaAs | 1.42 | Direct | High mobility, optical devices |
| InP | 1.35 | Direct | Optoelectronics |
| InAs | 0.35 | Direct | IR detectors, high mobility |
| GaP | 2.26 | Indirect | LED (red/green) |
| GaN | 3.4 | Direct | Blue LEDs, high power |
| InN | 0.7 | Direct | IR applications |

**Advantages:**
- Direct bandgaps (efficient light emission)
- High electron mobility
- Heterostructure capability
- Tunable bandgaps via composition

### Other Materials

| Material Type | Examples | Applications |
|---------------|----------|--------------|
| II-VI | ZnO, ZnS, CdS, CdSe | Optoelectronics, sensors |
| IV-VI | PbS, PbSe | IR detectors |
| Oxides | ZnO, TiO₂, Cu₂O | Photocatalysis, sensors |

---

## Synthesis Methods

### Vapor-Liquid-Solid (VLS) Growth

**Mechanism:**
1. Metal catalyst nanoparticles deposited on substrate
2. Substrate heated to form eutectic alloy
3. Precursor vapor decomposes at catalyst
4. Supersaturation → precipitation of solid nanowire
5. Wire grows with catalyst at tip

**Key parameters:**

| Parameter | Typical Range | Effect |
|-----------|---------------|--------|
| Temperature | 400-700°C | Growth rate, crystal quality |
| Catalyst size | 10-100 nm | Determines wire diameter |
| Precursor pressure | Variable | Growth rate |
| Substrate | Si, SiO₂, III-V | Epitaxial vs non-epitaxial |

**Advantages:**
- Controlled diameter (catalyst size)
- High crystal quality
- Heterostructure capability

**Common catalysts:** Au, Ni, Cu, Fe

### Metal Organic Vapor Phase Epitaxy (MOVPE)

Also called MOCVD (metal organic chemical vapor deposition)

**Process:**
```
1. Substrate preparation (clean, catalyst deposition)
2. Annealing: ~650°C (form Au-Si eutectic)
3. Growth: ~500°C with precursor gases
4. Cooling

Precursors for GaP:
- Trimethyl gallium (TMGa)
- Phosphine (PH₃)
```

**Advantages:**
- Precise composition control
- Heterostructure growth
- Scalable
- Industry-compatible

**Applications:**
- III-V nanowires
- Axial and radial heterostructures
- Core-shell structures

### Molecular Beam Epitaxy (MBE)

**Process:**
- Ultra-high vacuum (UHV)
- Solid source evaporation
- Precise flux control
- In-situ monitoring (RHEED)

**Advantages:**
- Highest purity
- Atomic-level control
- Sharp interfaces

**Disadvantages:**
- Slow growth rate
- Expensive
- Small scale

### Solution-Phase Synthesis

**Methods:**
- Solvothermal
- Hydrothermal
- Template-assisted

**Advantages:**
- Low temperature
- Scalable
- Inexpensive

**Disadvantages:**
- Lower crystal quality
- Broader size distribution
- Impurities

---

## Heterostructures

### Axial Heterostructures

**Structure:** Composition changes along wire length

**Examples:**
- GaAs/GaP segments
- InAs/InP junctions
- p-n junctions (same material, different doping)

**Applications:**
- Tunnel diodes
- Single electron transistors
- LEDs
- Photodetectors

**Growth:** Change precursor gases during growth

### Radial (Core-Shell) Heterostructures

**Structure:** Different material surrounds wire core

**Examples:**
- GaAs core / AlGaAs shell
- Si core / Ge shell
- InAs core / InP shell

**Advantages:**
- Surface passivation
- Carrier confinement
- Strain engineering

**Applications:**
- Lasers
- High-electron-mobility transistors
- Photovoltaics

### Branched Structures

- Nanotrees (nanowires on nanowires)
- Hierarchical structures
- Increased surface area

---

## Electronic Properties

### Conductance

**Landauer formula (ballistic transport):**
```
G = (2e²/h) × M × T

Where:
- M = number of conducting modes
- T = transmission coefficient
- Ballistic regime: L < mean free path
```

### Mobility

| Material | Bulk μ (cm²/V·s) | Nanowire μ (cm²/V·s) | Notes |
|----------|------------------|---------------------|-------|
| Si | 1400 (electrons) | 100-1000 | Surface scattering |
| GaAs | 8500 | 1000-5000 | Surface effects |
| InAs | 40,000 | 2000-10,000 | Surface accumulation layer |

### Quantum Effects

1. **Quantum confinement**
   - Subband formation
   - Increased bandgap
   - Density of states singularities

2. **Ballistic transport**
   - Mean free path > wire length
   - Conductance quantization
   - Minimal scattering

3. **Coulomb blockade**
   - Single electron effects
   - Charging energy: E_C = e²/2C
   - Quantum dots formed by heterostructures

---

## Optical Properties

### Absorption and Emission

**III-V Nanowires:**
- Direct bandgaps
- Strong absorption/emission
- Size-tunable wavelength

**Si Nanowires:**
- Indirect bandgap
- Weak emission
- Enhanced Raman scattering

### Photoluminescence

**Quantum yield enhancement strategies:**
1. Core-shell structures (passivation)
2. Surface treatments
3. Strain engineering
4. Heterostructure design

### Polarization

- Light emission polarized along wire axis
- Anisotropic absorption
- Waveguiding behavior

---

## Characterization

### Structural

| Technique | Information |
|-----------|-------------|
| SEM | Morphology, diameter, length, alignment |
| TEM | Crystal structure, defects, heterostructure interfaces |
| XRD | Crystal phase, orientation |
| SAED | Selected area diffraction pattern |
| AFM | Height, roughness |

### Electrical

| Technique | Information |
|-----------|-------------|
| I-V measurements | Conductance, carrier type |
| Gate dependence | FET behavior, mobility |
| Hall effect | Carrier concentration, mobility |
| C-V measurements | Doping profile |

### Optical

| Technique | Information |
|-----------|-------------|
| Photoluminescence (PL) | Bandgap, defects, quantum yield |
| Absorption | Bandgap, subband structure |
| Raman | Crystal quality, strain |
| Time-resolved PL | Carrier lifetime |

---

## Applications

### Electronics

#### 1. Transistors

**Gate-all-around (GAA) FETs:**
- Nanowire as channel
- Gate wraps around wire
- Excellent electrostatic control
- Beyond FinFET scaling

**Performance:**
- High on/off ratios (10⁶-10⁸)
- Low subthreshold swing
- Reduced short-channel effects

#### 2. Sensors

**Mechanisms:**
- Surface adsorption changes conductance
- Field effect from charged molecules
- Optical transduction

**Applications:**
- Chemical sensors (gas detection)
- Biosensors (DNA, proteins)
- pH sensors

**Advantages:**
- High surface-to-volume ratio
- Fast response
- Low power

### Optoelectronics

#### 1. LEDs

- Core-shell structures reduce non-radiative recombination
- Color tunable via material/composition
- Polarized emission

#### 2. Photodetectors

- High sensitivity
- Fast response
- Wavelength selective

#### 3. Solar Cells

- Radial p-n junctions
- Enhanced light absorption
- Decoupled light absorption and carrier collection

### Energy

#### 1. Thermoelectrics

**Figure of merit:**
```
ZT = S²σT/κ

Where:
- S = Seebeck coefficient
- σ = electrical conductivity
- κ = thermal conductivity
- T = temperature
```

**Nanowire advantages:**
- Reduced thermal conductivity (phonon scattering)
- Enhanced Seebeck coefficient (quantum confinement)
- ZT > 1 achievable

#### 2. Batteries

- Si nanowires for Li-ion anodes
- High capacity (3579 mAh/g theoretical)
- Accommodate volume expansion

### Quantum Devices

- Single electron transistors
- Quantum bits (qubits)
- Quantum dots in nanowires

---

## Challenges and Solutions

### 1. Doping Control

**Challenge:** Uniform doping, avoiding surface segregation

**Solutions:**
- Core-shell structures
- In-situ doping during growth
- Post-growth diffusion doping

### 2. Surface Recombination

**Challenge:** High surface area → trap states

**Solutions:**
- Passivation (shell growth)
- Surface treatments
- Surface functionalization

### 3. Contact Resistance

**Challenge:** High metal-nanowire contact resistance

**Solutions:**
- Annealing
- Work function matching
- Heavily doped contact regions

### 4. Position Control

**Challenge:** Precise placement on substrate

**Solutions:**
- Patterned catalyst deposition
- Template-assisted growth
- Transfer printing

### 5. Integration

**Challenge:** Incorporation into device architectures

**Solutions:**
- Bottom-up assembly
- Directed self-assembly
- Direct growth on device substrates

---

## Comparison: Nanowires vs Nanotubes

| Property | Nanowires | Carbon Nanotubes |
|----------|-----------|------------------|
| Material | Semiconductors (Si, III-V) | Carbon (sp²) |
| Structure | Crystalline solid | Cylindrical graphene |
| Bandgap | Tunable via size/material | Depends on chirality |
| Doping | Controlled, uniform | Difficult |
| Synthesis | VLS, MOVPE, MBE | CVD, arc discharge |
| Applications | Transistors, sensors, solar | Transistors, composites |

---

## Decision Flow

**Choosing nanowire material:**

1. **Optical emission needed?**
   - Yes → III-V nanowires (GaAs, InP, GaN)
   - No → Continue

2. **CMOS compatibility required?**
   - Yes → Si nanowires
   - No → Continue

3. **High mobility needed?**
   - Yes → InAs, GaAs nanowires
   - No → Continue

4. **Thermoelectric application?**
   - Yes → Si nanowires (low thermal conductivity)
   - No → Consider other materials

---

## Cross-References

**Related nanomaterials:**
- Carbon Nanotubes: [carbon_nanotubes.md](./carbon_nanotubes.md)
- Nanoparticles: [nanoparticles.md](./nanoparticles.md)
- Nanomaterials Overview: [nanomaterials_overview.md](./nanomaterials_overview.md)

**Synthesis and characterization:**
- Nanomaterials Synthesis: [nanomaterials_synthesis.md](./nanomaterials_synthesis.md)
- Microscopy: [microscopy.md](./microscopy.md)

**Fundamental concepts:**
- Band Theory: [band_theory.md](./band_theory.md)
