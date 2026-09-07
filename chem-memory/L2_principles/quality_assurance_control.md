# L2 Topic: Quality Assurance and Quality Control (QA/QC)

**Source**: LibreTexts Analytical Chemistry
**Created**: 2026-03-18
**Status**: Pass-1

---

## Concept Overview

Quality Assurance (QA) and Quality Control (QC) are systematic approaches to ensure analytical measurements are reliable, accurate, and fit for purpose. QA encompasses the overall system, while QC focuses on operational techniques.

### Key Features
1. **QA**: System-level processes, documentation, training
2. **QC**: Day-to-day checks, calibration, validation
3. **Statistical Process Control**: Monitoring measurement systems
4. **Uncertainty estimation**: Quantifying measurement reliability

---

## Core Principles

### QA/QC Hierarchy

| Level | Component | Examples |
|-------|-----------|----------|
| 1 | Quality System | SOPs, training, audits |
| 2 | Quality Assurance | Documentation, review, certification |
| 3 | Quality Control | Blanks, standards, duplicates |
| 4 | Method Validation | Accuracy, precision, LOD/LOQ |

### Control Charts

**Shewhart Chart Components:**
- Center line: Mean (μ)
- Warning limits: μ ± 2σ
- Control limits: μ ± 3σ
- Rules for out-of-control:
  - 1 point beyond 3σ
  - 2 of 3 consecutive points beyond 2σ
  - 9 consecutive points on one side of mean
  - 6 consecutive points trending in one direction

### QC Samples

| Sample Type | Purpose |
|-------------|---------|
| Blank | Detect contamination |
| Standard | Verify calibration |
| Duplicate | Assess precision |
| Spike | Assess accuracy/recovery |
| Reference material | Verify method performance |

### Acceptance Criteria

| Parameter | Typical Criterion |
|-----------|-------------------|
| Blank signal | < 3× noise |
| Standard recovery | 95-105% |
| Duplicate RSD | < 5% |
| Spike recovery | 80-120% |
| Reference material | Within certified range |

---

## Decision Trees

### QC Failure Response
```
Sample fails QC?
├── Blank high → Check contamination, reagents
├── Standard low → Recalibrate, check standards
├── Duplicate mismatch → Reanalyze, check homogeneity
└── Spike fails → Check matrix effects
```

### Method Selection
```
Method validated for matrix?
├── Yes → Use validated method
└── No → Validate or find alternative method
```

---

## Key Formulas

### Percent Recovery
$$\text{Recovery} = \frac{\text{Measured}}{\text{Added}} \times 100\%$$

### Relative Standard Deviation (RSD)
$$\text{RSD} = \frac{s}{\bar{x}} \times 100\%$$

### Combined Uncertainty
$$u_c = \sqrt{u_1^2 + u_2^2 + ... + u_n^2}$$

### Expanded Uncertainty
$$U = k \cdot u_c \quad (k \approx 2 \text{ for } 95\% \text{ confidence})$$

---

## L3 Implementations Needed

| Function | Purpose |
|----------|---------|
| `control_chart_limits` | Calculate UCL, LCL, UWL, LWL |
| `westgard_rules` | Check QC violations |
| `recovery_calc` | Percent recovery |
| `combined_uncertainty` | Propagate uncertainties |
| `rpd_calc` | Relative percent difference |

## L4 Data Needed

| Table | Content |
|-------|---------|
| `qc_acceptance_criteria.csv` | Industry standard limits |
| `reference_materials.csv` | CRM values for common analytes |

## L5 Examples Needed

| Example | Topic |
|---------|-------|
| Control chart construction | Shewhart chart |
| Uncertainty budget | GUM approach |

---

**Cross-links:**
- method_validation.md (G20)
- statistics_error_analysis.md
- analytical_chemistry_overview.md
