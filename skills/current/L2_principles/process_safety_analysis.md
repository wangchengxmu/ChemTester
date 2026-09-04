---
id: chem.process_safety_analysis
layer: 2
title: Process Safety Analysis
source: Foundations of Chemical and Biological Engineering I (Verret), Ch8
status: active
created: 2026-03-18
down_links:
  - ../L3_functions/process_safety_analysis.py
---

# Process Safety Analysis

[Source: Foundations of Chemical and Biological Engineering I (Verret), Ch8]

## Core Concept

Process safety analysis identifies, evaluates, and mitigates hazards in chemical processes. It is essential for preventing accidents and protecting people, environment, and assets.

## Analysis Methods

### 1. HAZOP (Hazard and Operability Study)

Systematic examination using guide words:
- **No/None** - Absence of flow, temperature, etc.
- **More** - Higher flow, temperature, pressure
- **Less** - Lower flow, temperature, pressure
- **Reverse** - Flow in wrong direction
- **Other than** - Wrong material, wrong phase

### 2. Fault Tree Analysis (FTA)

- Top-down approach
- Starts with undesired event
- Works backward to identify causes
- Uses logic gates (AND, OR)

### 3. Event Tree Analysis (ETA)

- Bottom-up approach
- Starts with initiating event
- Branches to show consequences

## Risk Assessment

$$\text{Risk} = \text{Frequency} \times \text{Consequence}$$

### Risk Matrix

| Frequency/Severity | Minor | Moderate | Major | Severe |
|-------------------|-------|----------|-------|--------|
| Frequent | Medium | High | Extreme | Extreme |
| Occasional | Low | Medium | High | Extreme |
| Rare | Low | Low | Medium | High |
| Remote | Very Low | Low | Low | Medium |

## Problem Types

1. **Conduct HAZOP** for a process unit
2. **Build fault tree** for specific hazard
3. **Calculate risk** from frequency/consequence data
4. **Recommend safeguards** to reduce risk

## Related Topics

- ï¿½?`process_economics.md` for cost of safety systems
- ï¿½?`green_engineering.md` for environmental safety


## Implementations

- Implementation: `../L3_functions/process_safety_analysis.py`

## L3 Tool Call Directives

**Source:** process_safety_analysis.py
Safety analysis calculations: risk scoring, HAZOP, LOPA, fault tree, SIL.

### Available functions:
- isk_score(frequency: float, consequence: float) ¡ú float ¡ª Risk = Frequency ¡Á Consequence
- isk_matrix_category(frequency: str, severity: str) ¡ú str ¡ª Risk level ('very low' to 'extreme'); freq: frequent/occasional/rare/remote; sev: minor/moderate/major/severe
- hazop_deviation(parameter: str, guide_word: str) ¡ú str ¡ª Deviation description (guide words: no/more/less/reverse/other)
- ault_tree_probability(and_gate: bool, probabilities: List[float]) ¡ú float ¡ª AND gate product, OR gate complement product
- layers_of_protection_analysis(initiating_freq: float, ipls: List[float]) ¡ú float ¡ª Mitigated frequency after IPLs
- safety_integrity_level(pfd: float) ¡ú str ¡ª SIL 1-4 from PFD (<0.1, <0.01, <0.001, <0.0001)

### Common errors:
- ? Using wrong frequency/severity category strings in risk_matrix_category
- ? LOPA: PFD is probability of failure (e.g. 0.01), not probability of success
