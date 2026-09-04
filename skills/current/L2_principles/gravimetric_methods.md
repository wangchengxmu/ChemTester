---
id: gravimetric.methods
layer: 2
title: Gravimetric Methods of Analysis
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - ../L3_functions/quantitative_analysis_tools.py
  - ../L4_reference/reference/electrochemical-analysis-data.md
cross_links:
  - ./solubility_equilibria.md
  - ./quantitative_chemical_analysis.md
source: Analytical Chemistry 2.1 (Harvey), Ch08
---

## Context
Gravimetric analysis determines the amount of an analyte by measuring the mass of a pure substance containing the analyte. It is one of the most accurate and precise analytical methods, with relative errors of 0.1-0.2%.

## Types of Gravimetric Analysis

### Classification
| Type | Principle | Example |
|------|-----------|---------|
| Precipitation | Analyte precipitated, weighed | Sulfate as BaSO₄ |
| Volatilization | Analyte volatilized, mass loss | Water by heating |
| Electrodeposition | Analyte deposited on electrode | Copper by electrolysis |
| Particulate | Solid collected, weighed | Suspended solids |

## Precipitation Gravimetry

### Steps in Analysis
1. Dissolve sample
2. Precipitate analyte as insoluble compound
3. Digest precipitate (improve particle size)
4. Filter precipitate
5. Wash to remove impurities
6. Dry or ignite to constant weight
7. Weigh and calculate

### Requirements for Precipitate
| Requirement | Reason |
|-------------|--------|
| Low solubility | Quantitative recovery |
| Known composition | Stoichiometric calculation |
| High purity | Accurate results |
| Easily filtered | Practical considerations |
| Stable to heat | Weighing conditions |

## Precipitation Formation

### Nucleation and Growth
```
Supersaturation → Nucleation → Crystal Growth

High supersaturation: Many nuclei → small particles (colloids)
Low supersaturation: Few nuclei → large crystals
```

### Von Weimarn Ratio
```
Relative supersaturation = (Q - S) / S

Where:
Q = instantaneous concentration
S = solubility at equilibrium
```

Lower ratio = larger crystals = better filtration

### Digestion
- Heating precipitate in mother liquor
- Promotes Ostwald ripening (small → large particles)
- Improves purity by recrystallization

## Particle Size and Filterability

### Particle Size Classification
| Size Range | Type | Separation |
|------------|------|------------|
| >100 μm | Coarse crystalline | Filter paper |
| 10-100 μm | Fine crystalline | Filter paper |
| 0.1-10 μm | Amorphous | Filter paper, slow |
| <0.1 μm | Colloidal | Coagulation needed |

### Colloidal Precipitates
- Pass through filter paper
- Require coagulation by:
  - Heating
  - Adding electrolyte
  - Increasing ionic strength

## Purity of Precipitates

### Types of Impurities
| Type | Mechanism | Prevention |
|------|-----------|------------|
| Inclusion | Ion trapped in crystal | Slow precipitation |
| Occlusion | Ion trapped during growth | Digestion |
| Surface adsorption | Ions on surface | Washing |
| Post-precipitation | Second precipitate forms | Filter quickly |

### Peptization
- Colloidal particles redisperse during washing
- Prevented by washing with electrolyte solution
- Example: Wash BaSO₄ with dilute H₂SO₄

## Common Gravimetric Methods

### Sulfate as BaSO₄
```
Ba²⁺ + SO₄²⁻ → BaSO₄(s)

%SO₄ = (mass BaSO₄ × 96.06/233.39 / mass sample) × 100
```

### Chloride as AgCl
```
Ag⁺ + Cl⁻ → AgCl(s)

%Cl = (mass AgCl × 35.45/143.32 / mass sample) × 100
```

### Iron as Fe₂O₃
```
Fe³⁺ + 3OH⁻ → Fe(OH)₃(s) → Fe₂O₃ (ignition)

%Fe = (mass Fe₂O₃ × 111.69/159.69 / mass sample) × 100
```

### Calcium as CaC₂O₄ → CaO
```
Ca²⁺ + C₂O₄²⁻ → CaC₂O₄(s) → CaO (ignition)

%Ca = (mass CaO × 40.08/56.08 / mass sample) × 100
```

## Gravimetric Factors

### Definition
The gravimetric factor (GF) relates mass of precipitate to mass of analyte:
```
GF = (molar mass of analyte) / (molar mass of precipitate) × (moles analyte/moles precipitate)
```

### Common Gravimetric Factors
| Analyte | Precipitate | GF |
|---------|-------------|-----|
| S | BaSO₄ | 0.1374 |
| SO₄²⁻ | BaSO₄ | 0.4116 |
| Cl⁻ | AgCl | 0.2474 |
| Ca | CaO | 0.7147 |
| Ca | CaCO₃ | 0.4004 |
| Fe | Fe₂O₃ | 0.6994 |
| Al | Al₂O₃ | 0.5293 |

## Calculations

### General Formula
```
% Analyte = (mass precipitate × GF / mass sample) × 100
```

### Example
Calculate %S in a 0.5000 g sample that yields 0.2957 g BaSO₄.

```
%S = (0.2957 g × 0.1374 / 0.5000 g) × 100 = 8.12%
```

## Volatilization Gravimetry

### Direct Method
- Analyze mass loss on heating
- Example: Water in hydrate
```
% H₂O = [(mass before - mass after) / mass sample] × 100
```

### Indirect Method
- Trap and weigh volatilized product
- Example: CO₂ absorbed in Ascarite
```
% C = (mass CO₂ × 12.01/44.01 / mass sample) × 100
```

## Sources of Error

### Systematic Errors
| Source | Effect | Correction |
|--------|--------|------------|
| Incomplete precipitation | Low result | Excess precipitant |
| Co-precipitation | High or low | Proper technique |
| Solubility loss | Low result | Common ion effect |
| Insufficient washing | High result | Adequate washing |
| Over-washing | Low result | Peptization control |

### Random Errors
- Weighing errors
- Transfer losses
- Temperature variation

## Decision Flow
1. Determine if gravimetric method appropriate
2. Select suitable precipitant
3. Optimize precipitation conditions
4. Filter and wash appropriately
5. Dry/ignite to constant weight
6. Calculate with correct gravimetric factor

## Implementations and Data
- Gravimetric calculation tools: [L3 code](../L3_functions/quantitative_analysis_tools.py)
- Reference tables: [L4 reference](../L4_reference/reference/electrochemical-analysis-data.md)
