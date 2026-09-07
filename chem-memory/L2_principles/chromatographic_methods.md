---
id: chromatographic.methods
layer: 2
title: Chromatographic and Separation Methods
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - ../L3_functions/chromatography_tools.py
  - ../L4_reference/reference/electrochemical-analysis-data.md
cross_links:
  - ./spectroscopic_methods.md
source: Analytical Chemistry 2.1 (Harvey), Ch12
---

## Context
Chromatography separates components of a mixture based on differential distribution between a stationary phase and a mobile phase. It is the most versatile separation technique in analytical chemistry, capable of analyzing complex mixtures with high resolution.

## Chromatographic Principles

### Basic Setup
```
Mobile Phase → [Stationary Phase] → Detector
                  (column)
```

### Distribution Equilibrium
```
K = C_s / C_m

Where:
K = distribution constant
C_s = concentration in stationary phase
C_m = concentration in mobile phase
```

### Retention Factor (k')
```
k' = (t_R - t_M) / t_M = K × (V_s / V_m)

Where:
t_R = retention time
t_M = dead time (unretained)
V_s = stationary phase volume
V_m = mobile phase volume
```

### Selectivity Factor (α)
```
α = k'₂ / k'₁ = K₂ / K₁  (for two components)
```

### Resolution (R_s)
```
R_s = 2(t_R₂ - t_R₁) / (w₁ + w₂)

Where w = peak width at base
```

### Van Deemter Equation
```
H = A + B/u + Cu

Where:
H = plate height
A = eddy diffusion term
B = longitudinal diffusion term
C = mass transfer term
u = linear velocity
```

## Column Efficiency

### Theoretical Plates (N)
```
N = 16(t_R/w)² = 5.54(t_R/w₁/₂)²

Where w₁/₂ = peak width at half height
```

### Plate Height (H)
```
H = L/N

Where L = column length
```

## Gas Chromatography (GC)

### Principles
- Mobile phase: inert gas (He, N₂, H₂)
- Stationary phase: liquid coated on solid or bonded phase
- Separation based on volatility and polarity

### Columns
| Type | Diameter | Length | Efficiency |
|------|----------|--------|------------|
| Packed | 2-4 mm | 1-3 m | Lower |
| Capillary (WCOT) | 0.1-0.5 mm | 15-100 m | Higher |
| Megabore | 0.53 mm | 15-30 m | Intermediate |

### Detectors
| Detector | Principle | Selectivity | Detection Limit |
|----------|-----------|-------------|-----------------|
| FID | Flame ionization | Organic | ~1 ng |
| TCD | Thermal conductivity | Universal | ~100 ng |
| ECD | Electron capture | Halogens, nitro | ~0.1 pg |
| NPD | Nitrogen-phosphorus | N, P compounds | ~1 pg |
| MS | Mass spectrometry | Universal | ~1 pg |

### Temperature Programming
- Linear ramp: Start temp → Ramp rate → Final temp
- Improves separation of wide boiling range mixtures
- Reduces analysis time

## Liquid Chromatography (LC/HPLC)

### Principles
- Mobile phase: liquid (various solvents)
- Stationary phase: bonded silica or polymer
- Separation based on polarity, size, or affinity

### Modes of HPLC
| Mode | Mechanism | Stationary Phase | Mobile Phase |
|------|-----------|------------------|--------------|
| Normal phase | Polarity | Polar (silica) | Nonpolar |
| Reverse phase | Polarity | Nonpolar (C18) | Polar (water/organic) |
| Ion exchange | Charge | Ion exchange resin | Buffer |
| Size exclusion | Size | Porous gel | Various |
| Affinity | Specific binding | Ligand | Buffer |

### Common Detectors
| Detector | Principle | Application |
|----------|-----------|-------------|
| UV-Vis | Absorbance | Chromophores |
| Fluorescence | Emission | Fluorescent compounds |
| Refractive index | Refraction | Universal, less sensitive |
| Electrochemical | Redox | Electroactive compounds |
| MS | Mass | Universal, sensitive |

### Gradient Elution
- Mobile phase composition changes during run
- Analogous to temperature programming in GC
- Improves separation of compounds with wide polarity range

## Thin Layer Chromatography (TLC)

### Principles
- Stationary phase: silica or alumina on plate
- Mobile phase: solvent ascending by capillary action
- Development and visualization

### Rf Value
```
Rf = distance traveled by compound / distance traveled by solvent
```

### Visualization Methods
| Method | Application |
|--------|-------------|
| UV light | UV-active compounds |
| Iodine vapor | Organic compounds |
| Ninhydrin | Amino acids |
| KMnO₄ | Alkenes, alcohols |
| Sulfuric acid charring | Organic compounds |

## Method Development

### Optimization Parameters
| Parameter | Effect |
|-----------|--------|
| Column length | Longer = more plates, more time |
| Particle size | Smaller = more efficiency, higher pressure |
| Flow rate | Optimal = minimum H |
| Temperature | GC: affects retention; LC: affects efficiency |
| Mobile phase | Strongly affects selectivity |

### Resolution Optimization
```
R_s ∝ √N × (α-1)/α × k'/(1+k')
      efficiency  selectivity  retention
```

1. Adjust retention (k' = 2-10 optimal)
2. Adjust selectivity (α > 1.1 needed)
3. Increase efficiency (more plates)

## Quantitative Analysis

### Peak Area vs Height
- Area: Preferred for broad peaks, asymmetric peaks
- Height: Preferred for narrow peaks, less baseline sensitive

### Calibration Methods
| Method | Description | Best For |
|--------|-------------|----------|
| External standard | Calibration curve | Simple matrices |
| Internal standard | Add known compound | Instrument variation |
| Standard addition | Spike sample | Matrix effects |

### Validation Parameters
- Linearity (R² > 0.999)
- Precision (RSD < 2%)
- Accuracy (recovery 98-102%)
- LOD/LOQ
- Selectivity (peak purity)

## Decision Flow
1. Determine sample type and analytes
2. Choose GC vs HPLC based on volatility
3. Select column and mobile phase
4. Optimize separation conditions
5. Choose detector
6. Validate method

## Implementations and Data
- Chromatography tools: [L3 code](../L3_functions/chromatography_tools.py)
- Reference tables: [L4 reference](../L4_reference/reference/electrochemical-analysis-data.md)
