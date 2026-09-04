# Experimental Techniques in Inorganic Chemistry

**Source:** CHM 320 Advanced Inorganic Chemistry, Chapter 14

## Overview

Characterization of inorganic compounds requires diverse analytical techniques. This document covers the main methods used to determine structure, composition, and properties.

## Separation and Purification

### Gas Chromatography (GC)
- **Use:** Volatile compounds, separation based on boiling point and polarity
- **Carrier gas:** He, Nâ? Hâ?- **Detectors:** FID, TCD, MS

### Liquid Chromatography (LC/HPLC)
- **Use:** Non-volatile compounds, metal complexes
- **Modes:** Normal phase, reverse phase, ion exchange
- **HPLC:** High pressure, higher resolution

### Recrystallization
- **Principle:** Solubility difference at different temperatures
- **Key:** Choose solvent where compound has steep solubility curve

## Elemental Analysis

### CHN Analysis (Combustion)
- Combust sample â?COâ? HâO, Nâ?- Quantitative determination of C, H, N content
- Compare to theoretical formula

### Atomic Absorption Spectroscopy (AAS)
- **Principle:** Atoms absorb at characteristic wavelengths
- **Source:** Hollow cathode lamp (element-specific)
- **Atomization:** Flame or graphite furnace
- **Use:** Metal quantification (ppm-ppb levels)

## Spectroscopic Methods

### Infrared (IR) Spectroscopy

**Principle:** Molecular vibrations absorb IR radiation

**Wavenumber Range:** 4000-400 cmâ»Â?
**Key Regions:**
| Region (cmâ»Â? | Assignment |
|---------------|------------|
| 4000-2500 | X-H stretching (O-H, N-H, C-H) |
| 2500-2000 | Triple bonds (Câ¡C, Câ¡N), CO |
| 2000-1500 | Double bonds (C=O, C=C) |
| 1500-400 | Fingerprint region, M-L |

**Special Applications:**
- Metal carbonyls: Î½(CO) indicates electron density on metal
- Lower Î½(CO) = more backbonding = more electron-rich metal

### Raman Spectroscopy

**Principle:** Inelastic scattering of monochromatic light
- Complementary to IR (different selection rules)
- Useful for symmetric vibrations (IR-inactive)
- Metal-ligand bonds often Raman-active

### UV-Visible Spectroscopy

**Principle:** Electronic transitions in UV-Vis region

**Transition Types:**
1. **d-d transitions:** Splitting of d orbitals (colors of transition metal complexes)
2. **Charge transfer:** LMCT, MLCT (intense bands)
3. **Ligand-centered:** ÏâÏ*, nâÏ*

**Beer-Lambert Law:**
```
A = Îµcl
A = absorbance
Îµ = molar absorptivity (Mâ»Â¹cmâ»Â?
c = concentration (M)
l = path length (cm)
```

### NMR Spectroscopy

**NMR-Active Nuclei in Inorganic Chemistry:**
| Nucleus | Spin | Natural Abundance | Receptivity |
|---------|------|-------------------|-------------|
| Â¹H | 1/2 | 99.98% | 1.00 |
| Â¹Â³C | 1/2 | 1.11% | 0.016 |
| Â³Â¹P | 1/2 | 100% | 0.066 |
| Â¹â¹F | 1/2 | 100% | 0.83 |
| Â²â·Al | 5/2 | 100% | 0.21 |
| âµÂ¹V | 7/2 | 99.76% | 0.38 |
| âµâ¹Co | 7/2 | 100% | 0.28 |
| Â¹â¹âµPt | 1/2 | 33.8% | 0.0094 |

**Special Considerations:**
- Paramagnetic complexes: Broad peaks, large chemical shift ranges
- Fluxional molecules: Temperature-dependent spectra

### Electron Paramagnetic Resonance (EPR/ESR)

**Principle:** Unpaired electrons in magnetic field

**Use:** Paramagnetic species, transition metals with unpaired electrons

**Information Obtained:**
- g-value (electronic environment)
- Hyperfine coupling (interaction with nuclear spins)
- Zero-field splitting (geometry)

### MÃ¶ssbauer Spectroscopy

**Principle:** Recoilless nuclear resonance fluorescence

**Most Common:** âµâ·Fe

**Parameters:**
1. **Isomer Shift (Î´):** Electron density at nucleus â?oxidation state
2. **Quadrupole Splitting (ÎE_Q):** Electric field gradient â?symmetry
3. **Magnetic Splitting:** Magnetic ordering

**Applications:**
- Fe oxidation state determination
- Spin state assignment
- Distinguish FeÂ²â?vs FeÂ³â? high-spin vs low-spin

## Diffraction Methods

### Single Crystal X-ray Diffraction (SCXRD)

**Gold standard for structure determination**

**Information Obtained:**
- Atomic positions
- Bond lengths and angles
- Molecular geometry
- Crystal packing

**Bragg's Law:** nÎ» = 2d sin Î¸

### Powder X-ray Diffraction (PXRD)

**Use:** Phase identification, purity checking

**Pattern Matching:** Compare to database (ICDD PDF)

### Neutron Diffraction

**Advantages:**
- Locates light atoms (H, Li) better than X-rays
- Distinguishes isotopes
- Magnetic structure determination

**Disadvantage:** Requires neutron source (reactor or spallation)

## Mass Spectrometry

### Ionization Methods for Inorganic Compounds

| Method | Best For | Softness |
|--------|----------|----------|
| EI (Electron Ionization) | Volatile organics | Hard (fragmentation) |
| FAB (Fast Atom Bombardment) | Non-volatile, polar | Medium |
| MALDI-TOF | Large biomolecules | Soft |
| ESI (Electrospray) | Ionic compounds in solution | Soft |

**ESI-MS for Metal Complexes:**
- Can observe intact complexes
- Multiple charge states possible
- Useful for speciation in solution

## Magnetic Measurements

### Magnetic Susceptibility

**Types of Magnetism:**
- **Diamagnetism:** All substances, opposes field (negative Ï)
- **Paramagnetism:** Unpaired electrons, aligns with field (positive Ï)

**Magnetic Moment:**
```
Î¼_eff = â?8Ï_M T) Bohr magnetons (BM)
Î¼_eff â?â?n(n+2)) BM  (spin-only formula)
```

**Methods:**
- Gouy balance
- SQUID magnetometer
- Evans method (NMR)

### Spin State Determination

| dâ?| High-spin Î¼_eff | Low-spin Î¼_eff |
|----|-----------------|----------------|
| dâ?| 4.90 BM | 2.83 BM |
| dâ?| 5.92 BM | 1.73 BM |
| dâ?| 4.90 BM | 0 BM (diamagnetic) |
| dâ?| 3.87 BM | 1.73 BM |

## Computational Methods

### Hartree-Fock (HF)
- Ab initio, wavefunction-based
- Good starting point, misses electron correlation

### Density Functional Theory (DFT)
- Most popular for inorganic chemistry
- Good balance of accuracy and cost
- Functionals: B3LYP, PBE, M06

### Applications
- Geometry optimization
- Electronic structure (MOs, spin density)
- Reaction mechanisms
- Spectroscopic property prediction

## Related Concepts

- **L2/spectroscopic_methods.md** - General spectroscopy
- **L2/crystallography.md** - Diffraction fundamentals
- **L2/crystal_field_theory.md** - d-orbital splitting
- **L2/magnetic_properties.md** - Detailed magnetism

## Problem-Solving Approaches

1. **Identify oxidation state:** Use XPS, MÃ¶ssbauer, magnetic moment
2. **Determine geometry:** SCXRD, EXAFS, spectroscopy
3. **Characterize ligands:** IR, NMR, elemental analysis
4. **Check purity:** Elemental analysis, PXRD, chromatography

## Selection Guide

| Information Needed | Recommended Technique |
|-------------------|----------------------|
| Molecular structure | SCXRD |
| Oxidation state (Fe) | MÃ¶ssbauer |
| Unpaired electrons | EPR, magnetic susceptibility |
| Ligand identification | IR, NMR |
| Formula verification | CHN analysis, MS |
| Phase identification | PXRD |
| Solution speciation | NMR, UV-Vis, ESI-MS |

## Notes

- Always use multiple complementary techniques
- Consider sample requirements (solid vs solution, air-sensitive)
- Temperature can affect spectra (fluxionality, spin crossover)


## Implementations

- Implementation: `../L3_functions/advanced_inorganic_tools.py`
