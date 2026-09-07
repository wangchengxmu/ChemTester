---
id: spectroscopic.methods
layer: 2
title: Spectroscopic Methods of Analysis
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - 
  - ../L4_reference/spectrochemical_series.csv
cross_links:
  - ./electromagnetic_energy.md
  - ./bohr_model.md
source: Analytical Chemistry 2.1 (Harvey), Ch10
---

## Context
Spectroscopic methods use the interaction of electromagnetic radiation with matter to identify and quantify chemical species. These are among the most widely used analytical techniques due to their sensitivity, selectivity, and versatility.

## Electromagnetic Spectrum

### Regions of Interest
| Region | Wavelength | Energy (kJ/mol) | Transitions |
|--------|------------|-----------------|-------------|
| Gamma | <0.01 nm | >10⁶ | Nuclear |
| X-ray | 0.01-10 nm | 10⁴-10⁶ | Inner shell e⁻ |
| UV | 10-400 nm | 300-1200 | Valence e⁻ |
| Visible | 400-700 nm | 170-300 | Valence e⁻ |
| IR | 0.7-1000 μm | 0.12-170 | Molecular vibration |
| Microwave | 0.1-100 cm | 0.001-0.12 | Molecular rotation |
| Radio | >100 cm | <0.001 | Nuclear spin |

### Beer-Lambert Law
```
A = εbc = -log(T)

Where:
A = absorbance (unitless)
ε = molar absorptivity (M⁻¹cm⁻¹)
b = path length (cm)
c = concentration (M)
T = transmittance = I/I₀
```

## UV-Visible Spectroscopy

### Principles
- Electronic transitions in molecules
- π → π*: typical for conjugated systems
- n → π*: typical for carbonyls
- d → d: transition metal complexes

### Chromophores
| Chromophore | λmax (nm) | ε (M⁻¹cm⁻¹) |
|-------------|----------|-------------|
| C=C | 180 | 10,000 |
| C≡C | 170 | 2,500 |
| C=O | 280 | 20 |
| Benzene | 255 | 200 |
| Naphthalene | 275 | 5,600 |
| β-Carotene | 450 | 140,000 |

### Applications
- Quantitative analysis (Beer's law)
- Determination of Ka
- Complex stoichiometry (Job's method)
- Kinetic studies

### Woodward-Fieser Rules
Empirical rules for predicting λmax of conjugated dienes and enones.

## Molecular Fluorescence

### Principles
```
Excitation: S₀ → S₁ (absorb photon)
Relaxation: S₁ → S₀ (emit photon)
```

### Stokes Shift
- Emission at longer wavelength than excitation
- Due to vibrational relaxation before emission

### Fluorescence Intensity
```
I_f = 2.303 × Φ_f × ε × b × c × P₀

Where:
Φ_f = fluorescence quantum yield
P₀ = incident radiant power
```

### Fluorescence vs Absorbance
| Aspect | Absorbance | Fluorescence |
|--------|------------|--------------|
| Sensitivity | ppm-ppb | ppb-ppt |
| Selectivity | Lower | Higher |
| Dynamic range | Higher | Lower |
| Linear range | Wider | Narrower |

## Infrared Spectroscopy

### Principles
- Molecular vibrations absorb IR radiation
- Bond stretching and bending modes
- Functional group identification

### Characteristic Absorptions
| Bond | Stretch (cm⁻¹) | Intensity |
|------|----------------|-----------|
| O-H | 3200-3600 | Strong, broad |
| N-H | 3300-3500 | Medium |
| C-H (sp³) | 2850-3000 | Strong |
| C-H (sp²) | 3000-3100 | Medium |
| C≡C | 2100-2260 | Variable |
| C=O | 1650-1750 | Strong |
| C=C | 1600-1680 | Variable |
| C-O | 1000-1300 | Strong |

### Fingerprint Region
- 600-1400 cm⁻¹
- Complex pattern unique to molecule
- Used for identification via library matching

## Atomic Spectroscopy

### Types
| Method | Sample Introduction | Analysis |
|--------|---------------------|----------|
| FAAS | Flame | Single element |
| GFAAS | Graphite furnace | Single element, trace |
| ICP-OES | Plasma | Multi-element |
| ICP-MS | Plasma | Multi-element, trace |

### Atomic Absorption (AAS)
```
A = K × C

Where K includes:
- Atomic absorption coefficient
- Path length
- Atomization efficiency
```

### Flame vs Furnace
| Aspect | Flame AAS | Furnace AAS |
|--------|-----------|-------------|
| Detection limit | ppm | ppb |
| Sample volume | mL | μL |
| Interferences | Fewer | More |
| Throughput | Higher | Lower |

### Inductively Coupled Plasma (ICP)
- Temperatures: 6000-10,000 K
- Complete atomization
- Multi-element capability
- Detection limits: ppb to ppm (OES), ppt (MS)

## Instrumentation

### UV-Vis Spectrometer Components
```
Source → Monochromator → Sample → Detector → Readout
```

| Component | Types |
|-----------|-------|
| Source | Deuterium (UV), Tungsten (Vis), Xenon (both) |
| Monochromator | Grating, prism |
| Detector | Photomultiplier, photodiode array, CCD |
| Cell | Quartz (UV), glass/plastic (Vis only) |

### Double-Beam Design
- Compensates for source fluctuations
- Reference beam subtracts background

## Applications

### Quantitative Analysis
1. Prepare standards
2. Generate calibration curve
3. Measure sample
4. Calculate concentration

### Multicomponent Analysis
- Use multiple wavelengths
- Matrix methods for overlapping spectra
- Derivative spectroscopy

### Structure Elucidation
- UV-Vis: Conjugation, chromophores
- IR: Functional groups
- Combination with other techniques

## Decision Flow
1. Determine analyte and concentration range
2. Select appropriate spectroscopic method
3. Choose wavelength/region
4. Prepare calibration standards
5. Measure samples
6. Validate results

## Implementations and Data
- Spectroscopy tools: [L3 code]()
- Reference tables: [L4 reference](../L4_reference/spectrochemical_series.csv)
