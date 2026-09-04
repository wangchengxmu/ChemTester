---
id: nanoparticles
layer: 2
title: Nanoparticles and Quantum Dots
up_links:
  - ./nanomaterials_overview.md
down_links:
  - ../L3_functions/nanomaterials_tools.py
cross_links:
  - ./semiconducting_nanowires.md
  - ./band_theory.md
  - ./uv_vis_spectroscopy.md
  - ./nanomaterials_synthesis.md
source: Wikibooks Nanotechnology Ch04 - Semiconducting Nanostructures
---

## Context

Nanoparticles are zero-dimensional nanomaterials with all dimensions below 100 nm. Metal nanoparticles exhibit surface plasmon resonance, while quantum dots (semiconductor nanocrystals) show size-tunable optical properties due to quantum confinement. This page covers synthesis, properties, and applications of both types.

---

## Metal Nanoparticles

### Gold Nanoparticles

#### Properties

| Property | Value/Description |
|----------|-------------------|
| Color | Wine-red (10 nm), purple/blue (larger) |
| LSPR wavelength | ~520 nm (size-dependent) |
| Melting point depression | Lower than bulk (1064°C) |
| Surface chemistry | Easily functionalized with thiols |
| Biocompatibility | Generally good |

#### Localized Surface Plasmon Resonance (LSPR)

**Mechanism:** Collective oscillation of conduction electrons

**Resonance condition:**
```
λ_LSPR depends on:
1. Particle size and shape
2. Dielectric environment
3. Interparticle distance
4. Material composition
```

**Size dependence:**

| Diameter | Color | λ_LSPR |
|----------|-------|--------|
| 10 nm | Red | 520 nm |
| 20 nm | Orange | 524 nm |
| 40 nm | Green | 530 nm |
| 80 nm | Purple | 550 nm |
| 100 nm | Blue | 580 nm |

#### Synthesis Methods

**1. Citrate Reduction (Turkevich method):**

```
HAuCl₄ + sodium citrate → Au nanoparticles

Procedure:
1. Heat HAuCl₄ solution to boiling
2. Add sodium citrate rapidly
3. Boil until wine-red color develops
4. Cool

Typical size: 10-20 nm
Control: Citrate/gold ratio
```

**2. Two-Phase Method (Brust-Schiffrin):**

```
HAuCl₄ in water + TOAB in toluene → AuCl₄⁻ in toluene
AuCl₄⁻ + alkanethiol + NaBH₄ → thiol-capped Au nanoparticles

Advantages:
- Organic soluble
- Stable
- Narrow size distribution
- Size control: 1-5 nm
```

### Silver Nanoparticles

#### Properties

| Property | Value |
|----------|-------|
| Color | Yellow to brown |
| LSPR wavelength | ~400 nm |
| Antimicrobial activity | Strong |
| Conductivity | Highest of all metals |

#### Applications

1. **Antimicrobial:**
   - Wound dressings
   - Coatings
   - Textiles

2. **Conductive inks:**
   - Printed electronics
   - Flexible circuits

3. **SERS substrates:**
   - Surface-enhanced Raman spectroscopy
   - Enhancement factor: 10⁶-10¹⁴

### Platinum Nanoparticles

#### Properties

| Property | Value |
|----------|-------|
| Structure | Small metallic clusters |
| Color | Dark brown/black |
| Catalytic activity | Very high |

#### Applications

**Catalysis:**

| Reaction | Application |
|----------|-------------|
| Hydrogenation | Chemical synthesis |
| Fuel cells | Oxygen reduction reaction (ORR) |
| Automotive | Catalytic converters |
| Hydrogen evolution | Water splitting |

**Particle size effect:**
```
Smaller particles → Higher surface area → Higher catalytic activity
Optimal: 2-5 nm (balance of activity and stability)
```

### Silica Nanoparticles

#### Properties

| Property | Value |
|----------|-------|
| Material | SiO₂ (amorphous) |
| Color | White (transparent as dispersion) |
| Density | 2.0-2.2 g/cm³ |
| Surface | Silanol groups (Si-OH) |

#### Synthesis: Stöber Process

```
TEOS + NH₃ + H₂O + EtOH → SiO₂ nanoparticles

Where TEOS = tetraethyl orthosilicate

Control parameters:
- TEOS concentration
- NH₃ concentration
- H₂O concentration
- Reaction time

Size range: 50 nm - 2 μm
```

#### Applications

- Drug delivery carriers
- Fillers in composites
- Chromatography supports
- Thermal insulation

---

## Quantum Dots

### Definition

Semiconductor nanocrystals with size-tunable optical properties due to quantum confinement.

### Quantum Confinement

**Condition:**
```
Nanocrystal size < Exciton Bohr radius

Exciton Bohr radius:
a_B = ε·ħ²/(μ·e²)

Where μ = reduced mass (1/m_e* + 1/m_h*)⁻¹

Example values:
- CdSe: 5.6 nm
- PbS: 18 nm
- Si: 4.9 nm
```

### Bandgap Tuning

**Effective mass approximation:**
```
E_g(QD) = E_g(bulk) + ħ²π²/(2R²) × (1/m_e* + 1/m_h*) - 1.8e²/(4πε₀εR)

Terms:
1. Bulk bandgap
2. Quantum confinement (increases with decreasing R)
3. Coulomb interaction (decreases bandgap slightly)
```

**Example: CdSe Quantum Dots**

| Size (nm) | Bandgap (eV) | Emission Color |
|-----------|--------------|----------------|
| 2.0 | 2.8 | Blue (~440 nm) |
| 2.5 | 2.4 | Green (~520 nm) |
| 3.0 | 2.2 | Yellow (~560 nm) |
| 4.0 | 2.0 | Orange (~620 nm) |
| 5.0 | 1.8 | Red (~690 nm) |

### Types of Quantum Dots

| Material | Bandgap (eV) | Emission Range | Applications |
|----------|--------------|----------------|--------------|
| CdSe | 1.74 | 500-650 nm | Displays, bioimaging |
| CdTe | 1.44 | 600-750 nm | IR imaging |
| PbS | 0.41 | 800-2000 nm | IR detectors |
| PbSe | 0.27 | 1000-3000 nm | IR photodetectors |
| InP | 1.35 | 500-700 nm | Cd-free displays |
| ZnS | 3.68 | UV | UV LEDs |
| Si | 1.11 | 600-900 nm | Biocompatible |

### Synthesis Methods

#### 1. Colloidal Synthesis (Hot Injection)

```
Procedure (CdSe example):
1. Heat Cd precursor (CdO + oleic acid) to 300°C
2. Inject Se precursor (Se + TOP) rapidly
3. Nucleation burst → monodisperse nuclei
4. Growth at 250°C
5. Size control by reaction time
6. Purification

Typical precursors:
- Cd: CdO, Cd(Ac)₂, CdCl₂
- Se: Se + TOP (tri-n-octylphosphine)
- Ligands: Oleic acid, TOPO, TOP
```

**Size control:**
- Longer growth time → larger particles
- Higher temperature → faster growth
- Precursor ratio affects nucleation

#### 2. Core-Shell Structures

**Purpose:** Passivate surface, improve quantum yield

**Common combinations:**

| Core | Shell | Advantage |
|------|-------|-----------|
| CdSe | ZnS | Type-I: carriers confined in core |
| CdSe | CdS | Graded: reduced strain |
| CdSe | CdTe | Type-II: charge separation |
| InP | ZnSe | Cd-free, high QY |

**Quantum yield:**
- CdSe: 10-30%
- CdSe/ZnS: 50-90%

### Optical Properties

#### Absorption

- Broad absorption spectrum
- Discrete energy levels visible in absorption peaks
- High extinction coefficients (10⁴-10⁵ M⁻¹·cm⁻¹)

#### Emission

- Narrow, symmetric emission peaks (FWHM 20-40 nm)
- Size-tunable wavelength
- High quantum yield (core-shell)
- Photostable (superior to organic dyes)

#### Blinking (Fluorescence Intermittency)

**Phenomenon:** Random on/off emission

**Mechanism:**
- Auger ionization
- Charge trapping
- Non-radiative recombination

**Solutions:**
- Core-shell structures
- Thicker shells
- Surface modification

---

## Characterization

### Size and Structure

| Technique | Information |
|-----------|-------------|
| TEM | Direct imaging, size distribution, shape |
| DLS | Hydrodynamic diameter (solution) |
| XRD | Crystal structure, size from Scherrer equation |
| SAXS | Size distribution (solution) |

### Optical

| Technique | Information |
|-----------|-------------|
| UV-Vis | LSPR (metal), bandgap (QDs) |
| Photoluminescence | Emission wavelength, quantum yield |
| Time-resolved PL | Carrier lifetime |
| Quantum yield measurement | Efficiency |

**Quantum Yield Measurement:**
```
QY_sample = QY_ref × (I_sample/I_ref) × (A_ref/A_sample) × (n_sample/n_ref)²

Where:
- I = integrated emission intensity
- A = absorbance at excitation
- n = refractive index
```

### Surface Chemistry

| Technique | Information |
|-----------|-------------|
| XPS | Surface composition |
| FTIR | Ligand binding |
| TGA | Ligand coverage |
| Zeta potential | Surface charge |

---

## Applications

### Metal Nanoparticles

#### 1. Biomedical

| Application | Mechanism |
|-------------|-----------|
| Drug delivery | Functionalization, targeted release |
| Photothermal therapy | LSPR heating |
| Imaging | Dark field microscopy, photoacoustic |
| Diagnostics | Lateral flow assays (gold) |
| Antimicrobial | Ag⁺ release (silver) |

#### 2. Electronics

- Conductive inks (Ag, Au)
- Flexible electronics
- Touch screens

#### 3. Catalysis

- Heterogeneous catalysis
- Electrocatalysis
- Photocatalysis

#### 4. Sensing

**Colorimetric sensors:**
- Aggregation changes LSPR
- Color change visible to eye
- Example: DNA detection with Au NPs

### Quantum Dots

#### 1. Displays (QLED)

**Advantages over LCD:**
- Wider color gamut
- Higher brightness
- Lower power consumption
- Pure colors (narrow emission)

**Architecture:**
```
Device structure:
Anode / Hole transport / QD layer / Electron transport / Cathode

Performance:
- EQE up to 20%
- Lifetime: >10,000 hours (green/red)
```

#### 2. Bioimaging

**Advantages over organic dyes:**
- Higher brightness
- Better photostability
- Multiplexing (same excitation, different emission)
- Longer lifetime

**Applications:**
- Cell labeling
- In vivo imaging
- FRET donors
- Single particle tracking

#### 3. Solar Cells

**Quantum dot solar cells:**
- Tunable bandgap
- Multiple exciton generation (MEG)
- Solution processable

**Efficiency:** 16-18% (colloidal QD solar cells)

#### 4. Photodetectors

- Visible to IR range
- High sensitivity
- Fast response

#### 5. LEDs

- Pure color emission
- High efficiency
- Flexible displays

---

## Safety Considerations

### Metal Nanoparticles

**Gold:** Generally considered biocompatible

**Silver:**
- Cytotoxicity at high concentrations
- Environmental concerns
- FDA-approved for some applications

**Platinum:** Low toxicity, used in chemotherapy (cisplatin)

### Quantum Dots

**Concerns:**
- Heavy metal content (Cd, Pb)
- Long-term fate in body
- Environmental persistence

**Solutions:**
- Core-shell structures (reduce leaching)
- Cd-free QDs (InP, Si)
- Proper disposal
- Encapsulation

---

## Comparison Table

| Property | Au NPs | Ag NPs | Pt NPs | Quantum Dots |
|----------|--------|--------|--------|--------------|
| LSPR | 520 nm | 400 nm | UV | No |
| Emission | No | No | No | Size-tunable |
| Catalytic | Moderate | Good | Excellent | Photochemical |
| Biocompatibility | Good | Moderate | Good | Variable |
| Stability | High | Moderate (oxidation) | High | High (core-shell) |
| Cost | High | Moderate | Very high | High |

---

## Decision Flow

**Choosing nanoparticle type:**

1. **Optical emission needed?**
   - Yes → Quantum dots
   - No → Continue

2. **LSPR sensing?**
   - Yes → Au or Ag nanoparticles
   - No → Continue

3. **Catalysis needed?**
   - Yes → Pt nanoparticles (chemical) or QDs (photocatalytic)
   - No → Continue

4. **Antimicrobial needed?**
   - Yes → Ag nanoparticles
   - No → Continue

5. **Biocompatibility critical?**
   - Yes → Au nanoparticles or Si QDs
   - No → Consider all options

---

## Cross-References

**Related nanomaterials:**
- Semiconducting Nanowires: [semiconducting_nanowires.md](./semiconducting_nanowires.md)
- Nanomaterials Overview: [nanomaterials_overview.md](./nanomaterials_overview.md)

**Characterization:**
- UV-Vis Spectroscopy: [uv_vis_spectroscopy.md](./uv_vis_spectroscopy.md)
- Microscopy: [microscopy.md](./microscopy.md)
- Nanomaterials Synthesis: [nanomaterials_synthesis.md](./nanomaterials_synthesis.md)

**Fundamental concepts:**
- Band Theory: [band_theory.md](./band_theory.md)
