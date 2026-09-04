---
id: nanomaterials.overview
layer: 2
title: Nanomaterials Overview
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - ./carbon_nanotubes.md
  - ./fullerenes_buckyballs.md
  - ./semiconducting_nanowires.md
  - ./nanoparticles.md
  - ./nanomaterials_synthesis.md
cross_links:
  - ./solid_state_chemistry.md
  - ./band_theory.md
  - ./microscopy.md
source: Wikibooks Nanotechnology Ch04 - Nanomaterials
---

## Context

Nanomaterials are materials with at least one dimension between 1-100 nm, exhibiting unique properties that differ from bulk materials due to quantum effects and high surface-to-volume ratios. Key concepts include **quantum confinement**, **surface effects**, and **size-dependent properties**.

---

## Classification by Dimension

| Dimension | Size Range | Examples | Key Property |
|-----------|------------|----------|--------------|
| 0D (zero-dimensional) | All dimensions < 100 nm | Nanoparticles, quantum dots, fullerenes | Quantum confinement in all directions |
| 1D (one-dimensional) | One dimension > 100 nm | Nanowires, nanotubes, nanofibers | Quantum confinement in 2 directions |
| 2D (two-dimensional) | Two dimensions > 100 nm | Graphene, nanofilms, nanosheets | Quantum confinement in 1 direction |
| 3D (bulk nanomaterials) | All dimensions > 100 nm | Nanocomposites, nanoporous materials | Nanoscale features throughout |

---

## Classification by Material Type

### Electronic Structure Classification

| Type | Examples | Band Structure | Properties |
|------|----------|----------------|------------|
| **Metallic** | Au, Ag, Pt nanoparticles | No bandgap | LSPR, catalytic, conductive |
| **Semiconducting** | Si nanowires, III-V nanowires, quantum dots | Size-tunable bandgap | Optical, electronic, photovoltaic |
| **Organic** | Carbon nanotubes, fullerenes | Variable (metallic/semiconducting) | Mechanical, electrical |

### Geometric Structure Classification

```
Nanomaterials Geometry Overview:

1. Particles
   - Spherical nanoparticles
   - Quantum dots (semiconductor nanocrystals)
   - Fullerenes (C₆₀, C₇₀)

2. Tubes
   - Single-walled carbon nanotubes (SWCNT)
   - Multi-walled carbon nanotubes (MWCNT)
   - Inorganic nanotubes (BN, MoS₂)

3. Wires
   - Silicon nanowires
   - III-V semiconductor nanowires
   - Metallic nanowires

4. Sheets
   - Graphene
   - Transition metal dichalcogenides (TMDs)
   - Boron nitride sheets
```

---

## Size-Dependent Properties

### Quantum Confinement

When particle size approaches the de Broglie wavelength of electrons:

**Particle-in-a-box model:**
```
E = h²n²/(8mL²)

Where:
- E = energy level
- n = quantum number
- m = effective mass
- L = particle size
```

**Consequences:**
1. **Discrete energy levels** (vs. continuous bands in bulk)
2. **Bandgap increases** as size decreases
3. **Blue shift** in optical absorption/emission

### Surface-to-Volume Ratio

```
Surface/Volume ratio ∝ 1/r

Where r = particle radius
```

**Consequences:**
1. Enhanced catalytic activity
2. Lower melting points
3. Increased reactivity
4. Dominant surface effects

### Example: Gold Nanoparticles

| Size | Color | Properties |
|------|-------|------------|
| ~10 nm | Red | Wine-red solution, LSPR at ~520 nm |
| ~20 nm | Orange | Larger LSPR shift |
| ~50 nm | Purple | Broad LSPR peak |
| ~100 nm | Blue | Multiple LSPR modes |

---

## Overview Table of Nanostructures

| Type | Structure | Production Method | Key Properties |
|------|-----------|-------------------|----------------|
| **Buckyballs/C₆₀** | 60 C atoms in football shape | Arc discharge, laser ablation | Molecular, semiconducting |
| **SWCNT** | Single graphene cylinder, d ~ 2 nm | CVD, arc discharge, laser ablation | Metallic or semiconducting |
| **MWCNT** | Concentric SWCNT shells | CVD, arc discharge | Typically metallic |
| **Si Nanowires** | Si crystals, d ~ few nm | VLS growth | Semiconducting |
| **III-V Nanowires** | GaAs, InP, etc. nanowires | MOVPE, VLS | Optically active, direct bandgap |
| **Au Nanoparticles** | Metallic clusters, d ~ 1-100 nm | Citrate reduction, wet chemical | LSPR, catalytic |
| **SiO₂ Nanoparticles** | Silica spheres | Stöber process | Dielectric, low toxicity |
| **Pt Nanoparticles** | Small metallic clusters | Wet chemical reduction | Catalytic |

---

## Key Phenomena

### 1. Surface Plasmon Resonance (SPR)

Collective oscillation of conduction electrons in metallic nanoparticles:

```
λ_SPR = 2πc × √(m_eff × ε₀)/(n_e × e²)

Where:
- λ_SPR = resonance wavelength
- m_eff = effective electron mass
- n_e = electron density
- e = electron charge
```

**Applications:**
- Biosensing
- Surface-enhanced Raman spectroscopy (SERS)
- Photothermal therapy

### 2. Quantum Size Effects

**Bandgap tuning in quantum dots:**
```
E_g(nanocrystal) = E_g(bulk) + h²/(8R²) × (1/m_e* + 1/m_h*) - 1.8e²/(4πε₀εR)

Where:
- R = nanocrystal radius
- m_e*, m_h* = effective masses
- Second term = quantum confinement
- Third term = Coulomb interaction
```

### 3. Enhanced Surface Reactivity

**Increased fraction of surface atoms:**

| Particle Size | Surface Atoms (%) | Binding Energy Shift (eV) |
|---------------|-------------------|--------------------------|
| 10 nm | ~20% | 0.1-0.2 |
| 5 nm | ~40% | 0.3-0.5 |
| 2 nm | ~80% | 0.8-1.2 |
| 1 nm | ~95% | 1.5-2.0 |

---

## Applications Overview

### Electronics
- CNT transistors and interconnects
- Quantum dot displays (QLED)
- Nanowire sensors

### Energy
- Quantum dot solar cells
- CNT-based batteries
- Nanoparticle catalysts for fuel cells

### Medicine
- Drug delivery nanoparticles
- Gold nanoparticles for photothermal therapy
- Quantum dot imaging agents

### Materials
- CNT composites (strength, conductivity)
- Nanoparticle-enhanced coatings
- Self-cleaning surfaces

---

## Characterization Techniques

### Microscopy
- **TEM** - Direct imaging of nanostructure
- **SEM** - Surface morphology
- **AFM** - Topography and mechanical properties
- **STM** - Atomic-scale imaging

### Spectroscopy
- **UV-Vis** - LSPR, bandgap determination
- **Raman** - D, G bands for carbon nanomaterials
- **Photoluminescence** - Quantum dot emission
- **XPS** - Surface composition

### Structural
- **XRD** - Crystal structure
- **SAED** - Selected area electron diffraction
- **BET** - Surface area measurement

---

## Decision Flow

**Choosing a nanomaterial for an application:**

1. **Optical properties needed?**
   - Yes → Quantum dots or metallic nanoparticles (SPR)
   - No → Continue

2. **Electrical properties needed?**
   - Metallic → CNTs (armchair), metallic nanoparticles
   - Semiconducting → Si nanowires, III-V nanowires, semiconducting CNTs
   - No → Continue

3. **Mechanical properties needed?**
   - High strength → CNTs, graphene
   - No → Continue

4. **Catalysis needed?**
   - Yes → Metal nanoparticles (Pt, Pd, Au)
   - No → Consider bulk materials

---

## Safety Considerations

### Nanotoxicity Factors
1. **Size** - Smaller particles more bioavailable
2. **Surface chemistry** - Coatings affect toxicity
3. **Shape** - Fibers may cause asbestos-like effects
4. **Composition** - Material-dependent

### Handling Guidelines
- Use fume hoods for nanoparticle powders
- Wear appropriate PPE
- Consider surface functionalization to reduce toxicity
- Proper disposal procedures

---

## Cross-References

**Detailed topics:**
- Carbon Nanotubes: [carbon_nanotubes.md](./carbon_nanotubes.md)
- Fullerenes: [fullerenes_buckyballs.md](./fullerenes_buckyballs.md)
- Semiconducting Nanowires: [semiconducting_nanowires.md](./semiconducting_nanowires.md)
- Nanoparticles: [nanoparticles.md](./nanoparticles.md)
- Synthesis Methods: [nanomaterials_synthesis.md](./nanomaterials_synthesis.md)

**Related concepts:**
- Solid State Chemistry: [solid_state_chemistry.md](./solid_state_chemistry.md)
- Band Theory: [band_theory.md](./band_theory.md)
- Microscopy: [microscopy.md](./microscopy.md)

## L3 Tool Call Directives

**Source:** nanomaterials_tools.py
Nanomaterials Tools - L3 Implementation

### Available functions:
- particle_in_a_box_energy(n, L, effective_mass_ratio, units) → float — Calculate energy of a particle in a 1D box.
- quantum_confinement_energy(radius, m_e_star, m_h_star, bulk_bandgap, dielectric_constant, units) →  — Calculate quantum confinement energy for semiconductor quantum dots.
- nanoparticle_surface_area(diameter, shape, units) →  — Calculate surface area and surface-to-volume ratio for nanoparticles.
- cnt_electronic_properties(n, m, bond_length) →  — Determine electronic properties of a carbon nanotube from chiral indices (n,m).
- plasmon_resonance(material, diameter, shape, dielectric_medium, units) →  — Calculate surface plasmon resonance wavelength for metallic nanoparticles.
- particle_size_distribution(sizes, weights) →  — Calculate statistical parameters for nanoparticle size distribution.
- exciton_bohr_radius(dielectric_constant, m_e_star, m_h_star) → float — Calculate the exciton Bohr radius for a semiconductor.
- quantum_dot_emission_wavelength(material, diameter) →  — Quick calculation of emission wavelength for common quantum dot materials.
- wavelength_to_color(wl) →  — 

### Common errors:
- ❌ Passing wrong parameter types or missing required arguments
