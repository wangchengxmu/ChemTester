---
id: analytical.method.design
layer: 2
title: Analytical Method Design and Validation
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - ../L3_functions/analytical_validation_tools.py
  - ../L4_reference/reference/electrochemical-analysis-data.md
cross_links:
  - ./quantitative_chemical_analysis.md
  - ./titrations.md
source: Analytical Chemistry 2.1 (Harvey), Ch01-03, Ch05, Ch14-15
---

## Context
Analytical chemistry involves the identification and quantification of chemical species. Method design, validation, and quality assurance are critical for obtaining reliable results. This topic covers the systematic approach to developing, validating, and implementing analytical methods.

## Types of Analysis

### Classification by Purpose
| Type | Goal | Example |
|------|------|---------|
| Qualitative | Identify what is present | Detect lead in water |
| Quantitative | Determine how much | Measure lead concentration |
| Characterization | Determine properties | Identify molecular structure |

### Classification by Sample
| Type | Description |
|------|-------------|
| Major component | >1% of sample |
| Minor component | 0.01% - 1% of sample |
| Trace component | <0.01% of sample |
| Ultratrace | <0.0001% of sample |

## Analytical Approach

### Steps in Analysis
1. **Define the problem**: What needs to be determined?
2. **Design the method**: Select appropriate technique
3. **Sampling**: Obtain representative sample
4. **Sample preparation**: Convert to measurable form
5. **Measurement**: Acquire data
6. **Data analysis**: Process and interpret
7. **Report results**: Communicate findings

## Method Selection Criteria

### Factors to Consider
| Criterion | Question |
|-----------|----------|
| Accuracy | How close to true value? |
| Precision | How reproducible? |
| Sensitivity | Can it detect low levels? |
| Selectivity | Does it avoid interferences? |
| Dynamic range | What concentration range? |
| Detection limit | Lowest measurable amount? |
| Robustness | Tolerant of small changes? |
| Cost | Time, equipment, reagents? |

### Accuracy vs Precision
- **Accuracy**: Closeness to true value (systematic error)
- **Precision**: Closeness of repeated measurements (random error)

```
High Accuracy, High Precision:     ●●●●
                                   ●●●●

High Accuracy, Low Precision:      ●    ●
                                  ●  ●   ●

Low Accuracy, High Precision:         ●●●●
                                      ●●●●

Low Accuracy, Low Precision:      ●      ●
                                    ●  ●
```

## Calibration and Standardization

### Calibration Methods
| Method | Description | When to Use |
|--------|-------------|-------------|
| External standards | Separate standards curve | Simple matrices |
| Standard additions | Spike sample with known | Matrix effects |
| Internal standards | Add reference compound | Instrument variation |

### Calibration Curve
```
Signal
  │         * (high conc)
  │       *
  │     *
  │   *
  │ *
  │*
  └──────────────────→ Concentration
```
- Linear range: where response is proportional
- Working range: practical usable range
- LOQ (limit of quantitation): lowest reliable quantitation
- LOD (limit of detection): lowest detectable signal

## Validation Parameters

### Key Validation Metrics
| Parameter | Definition | Test |
|-----------|------------|------|
| Accuracy | Agreement with true value | Recovery study, reference material |
| Precision | Reproducibility | Repeatability, reproducibility |
| Linearity | Proportional response | Correlation coefficient (R²) |
| Range | Valid concentration range | Upper and lower limits |
| LOD | Limit of detection | 3σ/m or 3.3σ/S |
| LOQ | Limit of quantitation | 10σ/m or 10σ/S |
| Selectivity | Freedom from interference | Specificity tests |
| Robustness | Resistance to small changes | Deliberate variation |

### Detection Limit Calculations
- **LOD (limit of detection)**: `LOD = 3 × σ_blank / slope`
- **LOQ (limit of quantitation)**: `LOQ = 10 × σ_blank / slope`

Where σ_blank is the standard deviation of blank measurements.

## Quality Assurance

### Components of QA
1. **Quality control (QC)**: Ongoing monitoring of method performance
2. **Quality assessment**: Evaluation of data quality
3. **Quality improvement**: Corrective actions

### Control Charts
```
Signal
  │ ──UCL (upper control limit)
  │
  │── Mean
  │
  │ ──LCL (lower control limit)
  └────────────────────────→ Time
    ● ●   ● ●  ●●  ● ●  ●
```
- Points within limits: process in control
- Points outside limits: investigate problem

### Reference Materials
| Type | Purpose |
|------|---------|
| Primary standard | Calibration (high purity) |
| Secondary standard | Routine calibration |
| Certified reference material (CRM) | Method validation |
| Quality control material | Daily monitoring |

## Error and Uncertainty

### Types of Error
| Type | Cause | Effect |
|------|-------|--------|
| Random | Unpredictable variation | Affects precision |
| Systematic | Consistent bias | Affects accuracy |
| Gross | Mistakes, accidents | Invalid results |

### Propagation of Uncertainty
For calculations with measured values:
```
If y = f(x₁, x₂, ...), then:
σ_y = √[(∂f/∂x₁)²σ_x₁² + (∂f/∂x₂)²σ_x₂² + ...]
```

### Significant Figures
- Report results with appropriate precision
- Calculations: retain extra digits, round at end
- Uncertainty typically 1-2 significant figures

## Decision Flow
1. Define analytical problem
2. Select appropriate method
3. Determine required accuracy/precision
4. Design sampling strategy
5. Choose calibration approach
6. Validate method parameters
7. Implement quality control
8. Document and report

## Implementations and Data
- Analytical method tools: [L3 code](../L3_functions/analytical_validation_tools.py)
- Reference tables: [L4 reference](../L4_reference/reference/electrochemical-analysis-data.md)
