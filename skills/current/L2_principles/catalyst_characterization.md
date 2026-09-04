---
id: catalyst_characterization
layer: 2
title: Catalyst Characterization (TEM, XRD, TPD)
parent: ../L1_ontology/chemistry-core-map.md#entry-266
stability: high
confidence: high
last_verified: 2026-03-24
source: LibreTexts Inorganic Chemistry, LibreTexts Catalysis Module
---

# Catalyst Characterization

## Core Concept

Understanding catalyst structure, composition, and surface properties is essential for rational catalyst design. Multiple techniques provide complementary information.

---

## Key Characterization Techniques

### 1. Transmission Electron Microscopy (TEM)
- **What it measures:** Direct imaging of particle size, morphology, crystal structure
- **Resolution:** ~0.1 nm (HRTEM)
- **Key info:** particle size distribution, lattice fringes, crystal defects
- **Sample prep:** thin sections (<100 nm), dispersed on grid

### 2. X-ray Diffraction (XRD)
- **What it measures:** Crystal structure, phase identification
- **Bragg's Law:** nλ = 2d sin θ
- **Key info:** crystallite size (Scherrer equation), phase composition, lattice parameters
- **Scherrer equation:** D = Kλ/(β cos θ) where K ≈ 0.9

### 3. Temperature-Programmed Desorption (TPD)
- **What it measures:** Strength and quantity of surface-adsorbed species
- **Method:** Adsorb probe molecule, then linearly ramp temperature while monitoring desorption
- **Key info:** acid/base site strength distribution, activation energy of desorption
- **Redhead equation:** E_d/RT_p² = (ν/β)(exp(-E_d/RT_p)) for estimating desorption energy

### 4. X-ray Photoelectron Spectroscopy (XPS)
- **What it measures:** Surface elemental composition, oxidation states
- **Depth:** top 1–10 nm
- **Key info:** surface vs bulk composition, chemical environment

### 5. Chemisorption (H₂, CO, N₂O)
- **What it measures:** Active metal surface area, dispersion
- **Key info:** metal particle size, fraction of surface atoms
- **Dispersion:** D = N_surface / N_total atoms

### 6. BET Surface Area Analysis
- **What it measures:** Total surface area, pore size distribution
- **Method:** N₂ adsorption at 77 K
- **Key info:** SSA (m²/g), pore volume, pore size (BJH method for mesopores)

### 7. Infrared Spectroscopy (FTIR / DRIFTS)
- **What it measures:** Surface functional groups, adsorbed species identification
- **In situ:** can monitor reactions under operating conditions

---

## Particle Size → Surface Area Relationship

For spherical nanoparticles:
$$D = \frac{6}{\rho \cdot SSA}$$

Where D = particle diameter, ρ = density, SSA = specific surface area.

---

## Links

- L3: `../L3_functions/heterogeneous_catalysis_tools.py`
- L4: `../L4_reference/heterogeneous_catalysis_reference.csv`
- L5: `../L5_examples/heterogeneous_catalysis_examples.md`
