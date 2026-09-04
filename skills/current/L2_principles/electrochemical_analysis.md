---
id: electrochemical_analysis
layer: 2
title: Electrochemical Analysis (Potentiometry, Voltammetry, Coulometry, Amperometry, Conductometry)
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - ../L3_functions/electrochemical_analysis_tools.py
  - ../L4_reference/reference/electrochemical-analysis-data.md
  - ../L5_examples/electrochemical_analysis/
source:
  - LibreTexts Analytical Chemistry 2.1 (Harvey) Ch11
  - LibreTexts Instrumental Analysis Ch22, Ch25
---

## Context

Electrochemical analysis encompasses techniques that use electrical signals—potential, current, or charge—to determine analyte concentration or chemical reactivity. These methods range from potentiometry (measuring potential at zero current) to voltammetry (measuring current as a function of applied potential) to coulometry (measuring total charge from exhaustive electrolysis). Electrochemical methods offer high sensitivity, selectivity, and the ability to analyze species in complex matrices.

## Core Concepts

### 1. Potentiometry

**Principle:** Measure the potential of an electrochemical cell under static conditions (zero current) to determine analyte activity using the Nernst equation.

**Nernst Equation (25°C):**
```
E = E° - (0.05916/n) × log Q
```

Where:
- E = electrode potential (V)
- E° = standard-state reduction potential (V)
- n = number of electrons
- Q = reaction quotient

**Cell Potential:**
```
E_cell = E_cathode - E_anode + E_j
```

For potentiometric cell:
```
E_cell = E_ind - E_ref + E_j
```

**Reference Electrodes:**
| Electrode | Potential (25°C) | Reaction |
|-----------|------------------|----------|
| SHE | 0.000 V | H⁺ + e⁻ ⇌ ½H₂ |
| SCE | +0.2444 V | Hg₂Cl₂ + 2e⁻ ⇌ 2Hg + 2Cl⁻ |
| Ag/AgCl (sat'd) | +0.197 V | AgCl + e⁻ ⇌ Ag + Cl⁻ |

**Ion-Selective Electrodes (ISEs):**
```
E_cell = K + (0.05916/z) × log(a_A)_samp
```

**Selectivity Coefficient:**
```
K_A,I = (a_A)_e / (a_I)_e^(z_A/z_I)
```

When K_A,I << 1: good selectivity for analyte A

### 2. Coulometry

**Principle:** Exhaustive electrolysis of analyte; total charge proportional to moles by Faraday's law.

**Faraday's Law:**
```
Q = n × F × N_A
```

Where:
- Q = total charge (C)
- n = electrons per molecule
- F = 96,487 C/mol e⁻
- N_A = moles of analyte

**Controlled-Current:**
```
Q = i × t_e
```

**Moles from Charge:**
```
N_A = Q / (n × F) = (i × t_e) / (n × F)
```

**Current Decay (Controlled-Potential):**
```
i_t = i_0 × e^(-kt)
```

**Time for 99.99% Electrolysis:**
```
t_e = 9.21 / k
```

**Current Efficiency:** Must be 100% or accurately known; use mediators to maintain efficiency.

### 3. Voltammetry

**Principle:** Apply time-dependent potential to working electrode; measure resulting current as function of potential.

**Three-Electrode System:**
- Working electrode: Where reaction occurs
- Reference electrode: Fixed potential
- Counter electrode: Completes circuit

**Limiting Current (diffusion-controlled, stirred):**
```
i_l = K_O × [O]_bulk = (nFA D_O / δ) × [O]_bulk
```

Where:
- A = electrode area
- D_O = diffusion coefficient
- δ = diffusion layer thickness

**Half-Wave Potential:**
```
E_1/2 = (E_p,a + E_p,c) / 2
```

For reversible systems with K_O ≈ K_R:
```
E_1/2 ≈ E°
```

**Cyclic Voltammetry - Peak Current (Randles-Sevcik):**
```
i_p = (2.69 × 10^5) × n^(3/2) × A × D^(1/2) × ν^(1/2) × C_A
```

Where:
- ν = scan rate (V/s)
- A = electrode area (cm²)
- D = diffusion coefficient (cm²/s)
- C_A = concentration (mol/cm³)

**Reversible System Characteristics:**
- Peak current ratio: i_p,a / i_p,c = 1.00
- Peak separation: ΔE_p ≈ 59/n mV at 25°C

**Stripping Voltammetry:**
Two-step process:
1. Deposition (concentrate analyte)
2. Stripping (measure concentrated analyte)

Detection limits: 10⁻¹⁰ to 10⁻¹² M

### 4. Amperometry

**Principle:** Measure current at fixed applied potential as function of time.

**Steady-State Current:**
```
i = nFA D C_bulk / δ
```

**Clark Oxygen Sensor:**
Cathode: O₂ + 4H₃O⁺ + 4e⁻ → 6H₂O
Anode: Ag + Cl⁻ → AgCl + e⁻

Current proportional to dissolved O₂ concentration.

**Amperometric Biosensors:**
Example - Glucose sensor:
1. Glucose + O₂ → gluconolactone + H₂O₂ (glucose oxidase)
2. H₂O₂ + 2OH⁻ → O₂ + 2H₂O + 2e⁻ (Pt electrode)

### 5. Conductometry

**Principle:** Measure solution conductivity, proportional to total ion concentration.

**Conductance:**
```
G = 1/R = κ × (A/l)
```

Where:
- G = conductance (S)
- R = resistance (Ω)
- κ = conductivity (S/cm)
- A = electrode area
- l = electrode separation

**Cell Constant:**
```
k = l/A = κ/G
```

**Molar Conductivity:**
```
Λ_m = κ/c
```

**Kohlrausch's Law (strong electrolytes):**
```
Λ_m = Λ_m° - K × √c
```

## Decision Flow

### Selecting Electrochemical Method

1. **Need qualitative + quantitative?** → Voltammetry
2. **High accuracy needed?** → Coulometry
3. **Continuous monitoring?** → Amperometry
4. **Total ion concentration?** → Conductometry
5. **Ion-specific measurement?** → Potentiometry with ISE

### Potentiometry Calculations

**For metal ion activity:**
1. Identify redox couple and n
2. Find E° from standard tables
3. Measure E_cell
4. Apply Nernst equation
5. Solve for activity

**For ISE:**
1. Calibrate with standards
2. Determine K constant
3. Measure E_cell
4. Calculate activity from E = K + (0.05916/z)log(a)

### Voltammetry Interpretation

**From limiting current:**
1. Identify limiting plateau
2. Measure i_l
3. Calculate concentration: [A] = i_l / K

**From cyclic voltammetry:**
1. Identify peak currents
2. Check reversibility: i_p,a / i_p,c ≈ 1
3. Calculate concentration from i_p
4. Determine E_1/2 for identification

### Coulometry Calculations

**For constant current:**
1. Record current i and time t_e
2. Calculate charge: Q = i × t_e
3. Apply Faraday's law: N_A = Q / (nF)
4. Convert to mass if needed

**For purity determination:**
1. Calculate moles from charge
2. Calculate theoretical mass
3. Compare to sample mass
4. Purity = (actual/theoretical) × 100%

## Quantitative Relationships

**Nernst equation expanded:**
```
E = E° - (RT/nF) ln Q = E° - (0.05916/n) log Q (at 25°C)
```

**Coulometric titration:**
```
N_A = (i × t_e) / (n × F)
```

**Stripping voltammetry sensitivity:**
Concentration factor = t_deposition × (stirring rate enhancement)

**ISE response:**
```
E = K + (0.05916/z) log a
```

For interferent I:
```
E = K + (0.05916/z_A) log[a_A + K_A,I × a_I^(z_A/z_I)]
```

## Edge Cases

### Potentiometry
- **Junction potential:** Unknown magnitude, must standardize
- **Activity vs concentration:** Use activity for accuracy
- **Matrix effects:** Formal potential may differ from E°
- **ISE interference:** Check selectivity coefficients

### Coulometry
- **Current efficiency < 100%:** Use mediator
- **Competing reactions:** Adjust potential
- **Incomplete electrolysis:** Extend time or increase k

### Voltammetry
- **IR drop:** Distorts voltammogram
- **Electrode fouling:** Clean/renew surface
- **Oxygen interference:** Remove by N₂ purge
- **Charging current:** Use pulse techniques

### Conductometry
- **Non-specific:** Total ions only
- **Temperature sensitivity:** κ ≈ +2%/°C
- **Electrode polarization:** At high concentrations

## Comparison Table

| Technique | Measures | Selectivity | Sensitivity | Speed | Accuracy |
|-----------|----------|-------------|-------------|-------|----------|
| Potentiometry | E (zero i) | High (ISE) | 10⁻⁶ M | Fast | Good |
| Coulometry | Q (charge) | High | 10⁻¹⁰ mol | Medium | Excellent |
| Voltammetry | i vs E | Medium-High | 10⁻⁹ M | Fast | Good |
| Amperometry | i (fixed E) | High | 10⁻⁶ M | Fast | Good |
| Conductometry | G (total ions) | Low | 10⁻⁴ M | Fast | Moderate |

## Implementations and Data

- Tool implementation: [L3 code](../L3_functions/electrochemical_analysis_tools.py)
- Reference database: [L4 electrochemical data](../L4_reference/reference/electrochemical-analysis-data.md)
- Worked examples: [L5 examples](../L5_examples/electrochemical_analysis/)

## Related Topics

- [galvanic_cells.md](galvanic_cells.md) - Electrochemical cell fundamentals
- [nernst_equation.md](nernst_equation.md) - Nernst equation theory
- [electrolysis.md](electrolysis.md) - Electrolysis principles
