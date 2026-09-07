---
id: thermal_analysis
layer: 2
title: Thermal Analysis (TGA, DSC, DTA)
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - ../L3_functions/thermal_analysis_tools.py
  - ../L4_reference/reference/thermal-analysis-data.md
  - ../L5_examples/thermal_analysis/
source:
  - LibreTexts Instrumental Analysis (Harvey) Ch31
  - LibreTexts Thermal Methods of Analysis (Shetty) Ch2-4
---

## Context

Thermal analysis encompasses techniques that measure physical and chemical properties as a function of temperature. The three primary methods—Thermogravimetric Analysis (TGA), Differential Scanning Calorimetry (DSC), and Differential Thermal Analysis (DTA)—provide complementary information about thermal stability, phase transitions, and energy changes in materials.

## Core Concepts

### 1. Thermogravimetric Analysis (TGA)

**Principle:** Monitor sample mass as function of temperature to identify decomposition steps and determine thermal stability.

**Mass Loss Percentage:**
```
% mass loss = [(m_initial - m_final) / m_initial] × 100
```

**Molar Mass Decrease from Mass Loss:**
```
ΔM = (mass_loss_fraction) × M_initial
```

**Decomposition Temperature Identification:**
- **T_onset:** Temperature where mass loss begins
- **T_peak:** Temperature of maximum decomposition rate (from DTG derivative)
- **T_final:** Temperature where mass stabilizes

**Typical Temperature Ranges:**
| Range | Common Process |
|-------|----------------|
| 100-250°C | Loss of hydration water |
| 250-400°C | CO loss, organic decomposition |
| 400-600°C | Carbonate decomposition |
| 600-800°C | Final oxide formation |
| >800°C | Stable residue |

**Thermogram Interpretation:**
- **Plateau:** Thermally stable region
- **Step:** Mass loss from decomposition
- **Multiple steps:** Sequential decomposition reactions

### 2. Differential Scanning Calorimetry (DSC)

**Principle:** Measure heat flow required to maintain sample and reference at identical temperature during controlled heating/cooling.

**Enthalpy from Peak Area:**
```
ΔH = K × A
```

Where:
- ΔH = enthalpy change (J/g or J/mol)
- K = calibration constant (J/area unit)
- A = integrated peak area

**Heat Capacity from DSC:**
```
C_p = (dQ/dt) / (dT/dt) / m
```

Where:
- C_p = specific heat capacity (J/g·K)
- dQ/dt = heat flow rate (W or mW)
- dT/dt = heating rate (K/s or °C/min)
- m = sample mass (g)

**Alternative form:**
```
C_p = heat_flow / (heating_rate × mass)
```

**Peak Sign Convention:**
| Peak Type | Process | ΔH Sign |
|-----------|---------|---------|
| Endothermic | Melting, dehydration, decomposition | ΔH > 0 (heat absorbed) |
| Exothermic | Crystallization, oxidation | ΔH < 0 (heat released) |

**Glass Transition (Tg):**
- Identified by baseline shift (step change)
- No peak; heat capacity change only
- ΔC_p = C_p(liquid) - C_p(glass)

### 3. Differential Thermal Analysis (DTA)

**Principle:** Measure temperature difference between sample and reference during heating.

**Fundamental Equation:**
```
ΔT = T_sample - T_reference
```

**Peak Interpretation:**
| Process | Heat Effect | ΔT Sign |
|---------|-------------|---------|
| Endothermic | Absorbs heat | T_sample < T_ref → ΔT > 0 |
| Exothermic | Releases heat | T_sample > T_ref → ΔT < 0 |

### 4. Technique Comparison

| Feature | TGA | DSC | DTA |
|---------|-----|-----|-----|
| Measurement | Mass change | Heat flow | ΔT |
| Detects | Mass changes only | All transitions | All transitions |
| Quantitative | Yes | Yes | Semi-quantitative |
| Reference needed | No | Yes | Yes |
| Primary application | Decomposition | Energy changes | Phase transitions |

### 5. Phase Transitions

**Classification:**
| Transition | Type | Mass Change | Detectable By |
|------------|------|-------------|---------------|
| Melting | Endothermic | No | DSC, DTA |
| Crystallization | Exothermic | No | DSC, DTA |
| Glass transition | C_p change | No | DSC |
| Evaporation | Endothermic | Yes | TGA, DSC, DTA |
| Dehydration | Endothermic | Yes | TGA, DSC, DTA |
| Decomposition | Usually endo | Yes | TGA, DSC, DTA |
| Oxidation | Exothermic | May increase | TGA, DSC, DTA |

**Identification Rules:**
1. Check TGA first: mass change → decomposition/dehydration
2. No mass change + sharp endotherm → melting
3. No mass change + exotherm → crystallization
4. Baseline shift only → glass transition

### 6. Calibration Standards (DSC/DTA)

| Standard | Melting Point (°C) | ΔH_fusion (J/g) |
|----------|-------------------|-----------------|
| Indium | 156.6 | 28.45 |
| Tin | 231.9 | 60.22 |
| Lead | 327.5 | 23.03 |
| Zinc | 419.5 | 112.0 |

**Calibration Constant:**
```
K = ΔH_known / A_measured
```

## Decision Flow

### Identifying Decomposition Products from TGA

1. Calculate % mass loss: (m_i - m_f) / m_i × 100
2. Calculate molar mass decrease: % loss × M_compound
3. Match to known volatile products (H₂O = 18, CO = 28, CO₂ = 44)
4. Verify with temperature range

### Calculating Enthalpy from DSC

1. Integrate peak area
2. Determine calibration constant from standard
3. Apply: ΔH = K × A
4. Convert to per-mole if needed: ΔH_molar = ΔH_mass × M

### Mixture Analysis (TGA)

1. Heat to sequential temperatures
2. Measure mass at each plateau
3. Use stoichiometry to calculate component amounts
4. Account for overlapping decomposition

## Quantitative Relationships

**TGA stoichiometric calculations:**
```
g compound = Δm × (1 mol gas / M_gas) × (M_compound / n_gas)
```

Where n_gas = moles of gas released per mole of compound

**DSC calibration:**
```
K = ΔH_standard / Peak_area_standard
```

**Heat capacity baseline shift:**
```
ΔC_p = (baseline_shift × heating_rate) / mass
```

## Edge Cases

- **Buoyancy effects in TGA:** Apparent mass change from gas density changes
- **Atmosphere effects:** Oxidative vs inert atmosphere changes decomposition
- **Heating rate effects:** Faster = broader peaks, shifted temperatures
- **Sample size:** Too large = thermal gradients, poor resolution
- **Reference material:** Must be inert in temperature range

## Implementations and Data

- Tool implementation: [L3 code](../L3_functions/thermal_analysis_tools.py)
- Reference database: [L4 thermal data](../L4_reference/reference/thermal-analysis-data.md)
- Worked examples: [L5 examples](../L5_examples/thermal_analysis/)

## Related Topics

- [calorimetry.md](calorimetry.md) - Heat measurement fundamentals
- [enthalpy_and_thermochemistry.md](enthalpy_and_thermochemistry.md) - Enthalpy concepts
- [solid_state_chemistry.md](solid_state_chemistry.md) - Solid state transitions

## L3 Tool Call Directives

**Source:** `thermal_analysis_tools.py`
Thermal analysis: TGA mass calculations, DSC enthalpy, heat capacity, phase transitions.

### Available functions:
- `tga_mass_percent(initial_mass, final_mass)` → float — Calculate mass loss percentage
- `tga_mass_loss_molar(initial_mass, compound_molar_mass, gas_molar_mass, n_gas)` → dict — Molar analysis of mass loss
- `tga_identify_product(compound, mass_loss_pct, temperature_range)` → dict — Identify decomposition product from TGA
- `tga_decomposition_temperature(bond_energy, pre_exp_factor, heating_rate)` → dict — Estimate decomposition temperature
- `tga_residual_mass(initial_mass, compound_formula, residue_formula)` → dict — Calculate expected residual mass
- `dsc_enthalpy(area, mass, heating_rate, calibration_factor)` → float — Calculate enthalpy from DSC peak area
- `dsc_calibration_constant(known_enthalpy, measured_area, mass)` → float — DSC calibration constant
- `dsc_heat_capacity(heat_flow, mass, heating_rate)` → float — Calculate heat capacity Cp from DSC
- `dsc_glass_transition(heat_flow, temperature, mass)` → dict — Identify glass transition parameters
- `dsc_crystallinity(dh_observed, dh_100_crystalline)` → float — Calculate crystallinity percentage
- `dta_temperature_difference(thermal_conductivity_sample, thermal_conductivity_ref, heat_capacity, heating_rate, mass)` → float — Calculate ΔT for DTA
- `dta_peak_type(Delta_T)` → str — Classify DTA peak as endothermic/exothermic
- `phase_transition_identification(temperature, delta_H, sample_type)` → dict — Identify phase transition type
- `identify_thermal_process(temperature, mass_change, heat_flow)` → dict — Classify thermal process from combined data
- `tga_mixture_analysis(masses, formulas, decomposition_temps)` → dict — Analyze multi-component TGA
- `analyze_tga_thermogram(temperature_data, mass_data)` → dict — Full TGA thermogram analysis (steps, products)
- `calculate_heat_of_fusion(mass, specific_heat_solid, specific_heat_liquid, delta_T_supercool, melting_point)` → float — Heat of fusion from cooling curve
- `estimate_purity_from_melting(observed_mp, depressed_mp, pure_mp)` → dict — Estimate purity from melting point depression

### Common errors:
- ❌ Confusing exothermic (crystallization) with endothermic (melting) in DTA/DSC
- ❌ Not accounting for baseline drift in DSC enthalpy calculations
