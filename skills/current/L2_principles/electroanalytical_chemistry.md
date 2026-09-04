---
id: electroanalytical_chemistry
layer: 2
title: Electroanalytical Chemistry - Potentiometry, Coulometry, and Voltammetry
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - ../L3_functions/electrochemical_analysis_tools.py
  - ../L3_functions/electroanalytical_tools.py
cross_links:
  - ./electrochemistry.md
  - ./galvanic_cells.md
source: Skoog Instrumental Analysis Ch22-25 (LibreTexts)
---

## Context

Electroanalytical chemistry uses electrical measurements to determine chemical concentrations. Three major techniques are covered: potentiometry (potential measurement at zero current), coulometry (charge measurement), and voltammetry (current-potential relationships). These methods offer excellent selectivity and sensitivity.

---

## Part 1: Potentiometry

### Fundamental Principles

Measurement of cell potential at zero current:

```
E_cell = E_indicator - E_reference + E_junction
```

### Nernst Equation

```
E = E° - (RT/nF)ln(a_red/a_ox) = E° - (0.05916/n)log(a_red/a_ox) at 25°C
```

### Reference Electrodes

#### Standard Hydrogen Electrode (SHE)
```
E° = 0.000 V (by definition)
```

#### Saturated Calomel Electrode (SCE)
```
Hg | Hg₂Cl₂(sat'd), KCl(sat'd) || 
E = +0.244 V vs SHE
```

#### Silver/Silver Chloride
```
Ag | AgCl(sat'd), KCl(sat'd) || 
E = +0.197 V vs SHE (3.5 M KCl)
```

### Indicator Electrodes

#### 1. Metal Electrodes

**First kind:** Metal in contact with its ions
```
M | Mⁿ⁺
E = E° + (0.05916/n)log[Mⁿ⁺]
```

**Second kind:** Metal in contact with insoluble salt
```
Ag | AgCl | Cl⁻
E = E° - 0.05916 log[Cl⁻]
```

#### 2. Membrane Electrodes (Ion-Selective Electrodes)

**Glass electrode (pH):**
- Sensitive to H⁺
- Membrane potential: E = K + 0.05916 log[H⁺]

**pH measurement:**
```
pH = (E_obs - E_ref - K)/0.05916
```

**Selectivity coefficient:**
```
E = K + 0.05916 log(a_A + k_AB × a_B)
```

#### Common Ion-Selective Electrodes

| Electrode | Ion | Detection Range |
|-----------|-----|-----------------|
| Glass | H⁺ | pH 0-14 |
| Fluoride (LaF₃) | F⁻ | 10⁻⁶ - 1 M |
| Calcium (PVC) | Ca²⁺ | 10⁻⁵ - 1 M |
| Ammonium | NH₄⁺ | 10⁻⁵ - 1 M |

### Potentiometric Titration

**Advantages:**
- No indicator needed
- Works for colored solutions
- Automatic endpoint detection

| Titration Type | Electrode System |
|----------------|------------------|
| Acid-base | pH glass electrode |
| Redox | Pt electrode |
| Precipitation | ISE for ion |
| Complexometric | Hg electrode |

---

## Part 2: Coulometry

### Fundamental Principles

Based on Faraday's laws:

```
m = (Q × M)/(n × F) = (I × t × M)/(n × F)
```

Where:
- m = mass deposited
- Q = charge (coulombs)
- M = molar mass
- n = electrons per molecule
- F = Faraday constant (96485 C/mol)

### Coulometric Titrations

**Advantages:**
- No standard solution preparation
- Microgram to gram quantities
- High accuracy (0.01%)

**Requirements:**
- 100% current efficiency
- Known endpoint detection

### Controlled-Potential Coulometry

Working electrode held at constant potential:

```
Q = ∫ I dt = n × F × c × V
```

Applications: Metal determinations, electrolytic purification

### Common Coulometric Titrations

| Analyte | Generating Electrolyte | Product |
|---------|----------------------|---------|
| Acids | KI | OH⁻ |
| Bases | Na₂SO₄ | H⁺ |
| Fe²⁺ | Ce(III) | Ce⁴⁺ |
| As(III) | KI | I₂ |
| Thiosulfate | KI | I₂ |

---

## Part 3: Voltammetry

### Fundamental Principles

Current measured as function of applied potential:

```
I = f(E)
```

### Linear Sweep Voltammetry

Potential scanned linearly:
```
E(t) = E_i + νt
```

Where ν = scan rate

**Peak current (Randles-Sevcik equation):**
```
I_p = 2.69 × 10⁵ × n^(3/2) × A × D^(1/2) × C × ν^(1/2)
```

Where:
- I_p = peak current (A)
- A = electrode area (cm²)
- D = diffusion coefficient (cm²/s)
- C = concentration (mol/cm³)
- ν = scan rate (V/s)

### Cyclic Voltammetry

Potential scanned forward and back:
```
E → E_max → E (return scan)
```

**Reversible system:**
- ΔE_p = E_pa - E_pc = 59/n mV
- I_pa/I_pc = 1

**Irreversible system:**
- ΔE_p > 59/n mV
- Peak separation increases with scan rate

### Polarography

Voltammetry with dropping mercury electrode (DME):

**Ilkovic equation:**
```
I_d = 708 × n × D^(1/2) × m^(2/3) × t^(1/6) × C
```

Where:
- I_d = diffusion current (μA)
- m = mercury flow rate (mg/s)
- t = drop time (s)
- C = concentration (mM)

**Half-wave potential (E₁/₂):**
- Characteristic of analyte
- Used for qualitative identification

### Differential Pulse Voltammetry (DPV)

- Pulse superimposed on linear ramp
- Current sampled before and after pulse
- Peak-shaped response
- Enhanced sensitivity

### Square Wave Voltammetry (SWV)

- Faster than DPV
- Higher sensitivity
- Background subtraction

### Stripping Voltammetry

**Preconcentration step:**
- Analyte deposited at controlled potential
- High enrichment factor

**Stripping step:**
- Potential scanned to dissolve analyte
- Current proportional to concentration

| Technique | Preconcentration | Detection Limit |
|-----------|-----------------|------------------|
| Anodic stripping (ASV) | Metal deposited | 10⁻¹⁰ M |
| Cathodic stripping (CSV) | Film formation | 10⁻⁹ M |
| Adsorptive stripping (AdSV) | Adsorption | 10⁻¹⁰ M |

---

## Instrumentation

### Three-Electrode Cell

| Electrode | Function |
|-----------|----------|
| Working | Where reaction occurs |
| Reference | Provides stable potential |
| Counter | Completes circuit |

### Working Electrodes

| Material | Potential Range (V vs SCE) | Application |
|----------|---------------------------|-------------|
| Mercury | -2.0 to +0.4 | Cathodic, metals |
| Platinum | -0.2 to +1.5 | Anodic, oxidations |
| Glassy carbon | -1.0 to +1.3 | General purpose |
| Gold | -0.3 to +1.5 | Anodic stripping |
| Carbon paste | -1.0 to +1.0 | Modified electrodes |

### Potentiostat

- Controls working electrode potential
- Measures current
- Three-electrode configuration

---

## Problem-Solving Examples

### Example 1: pH Measurement

**Problem**: A pH electrode gives E = 0.350 V vs Ag/AgCl (E = 0.197 V). Calculate pH.

**Solution:**
```
E = K + 0.05916 × pH
pH = (E - K)/0.05916

If K = 0.400 V (determined by calibration):
pH = (0.350 - 0.400)/0.05916 = -0.84

Note: Need proper calibration with standards
```

### Example 2: Coulometric Titration

**Problem**: 50.00 mA current for 180.0 s generates I₂ to titrate As(III). Calculate As mass.

**Solution:**
```
Q = I × t = 0.050 A × 180 s = 9.0 C
As(III) + I₂ → As(V) + 2I⁻

Each As requires I₂ (n = 2 for As³⁺ → As⁵⁺)
m = Q × M/(n × F) = 9.0 × 74.92/(2 × 96485)
m = 3.50 mg As
```

### Example 3: Peak Current Calculation

**Problem**: Calculate I_p for 1 mM Fe(CN)₆³⁻ at 0.10 V/s, D = 7.6×10⁻⁶ cm²/s, A = 0.020 cm², n = 1.

**Solution:**
```
I_p = 2.69 × 10⁵ × n^(3/2) × A × D^(1/2) × C × ν^(1/2)
I_p = 2.69 × 10⁵ × 1 × 0.020 × (7.6×10⁻⁶)^(1/2) × 10⁻⁶ × (0.10)^(1/2)
I_p = 2.69 × 10⁵ × 0.020 × 2.76×10⁻³ × 10⁻⁶ × 0.316
I_p = 4.69 × 10⁻⁶ A = 4.69 μA
```

### Example 4: Stripping Analysis

**Problem**: Anodic stripping of Pb gives peak current 2.5 μA after 2 min deposition. Calibration: 1.0 μA per 10 ppb. Find Pb concentration.

**Solution:**
```
[Pb] = (2.5 μA)/(1.0 μA/10 ppb) = 25 ppb
```

---

## Decision Flow

1. **Choose technique:**
   - Need selectivity? → Potentiometry with ISE
   - Need accuracy? → Coulometric titration
   - Need sensitivity? → Stripping voltammetry
   - Need speciation? → Voltammetry

2. **Select electrode:**
   - Cathodic potential needed? → Mercury
   - Anodic potential needed? → Pt or C
   - Direct measurement? → ISE

3. **Optimize conditions:**
   - Supporting electrolyte
   - pH control
   - Oxygen removal (N₂ sparging)

---

## Quick Reference

| Technique | Detection Limit | Precision |
|-----------|-----------------|-----------|
| Potentiometry | 10⁻⁶ M | 1-2% |
| Coulometry | μg-g | 0.01% |
| Polarography | 10⁻⁵ M | 2-5% |
| Stripping voltammetry | 10⁻¹⁰ M | 5-10% |

---

## L3 Tool Call Directive

**Always use L3 tools instead of manual calculation.** Call functions from `electroanalytical_tools.py`:

- **ISE calibration**: `ise_calibration(concentrations, potentials, ion_type=None)` — fits Nernst equation. Pass `ion_type="anion"` for anion-selective electrodes (negative slope convention), `ion_type="cation"` for cation ISE.
- **Mass from electrolysis**: `mass_from_electrolysis(charge, n_electrons, molar_mass)` — Faraday's law. For dimerization/coupling reactions where 2 reactant molecules form 1 product, use `reactant_to_product_ratio=2.0`.
- **Limit of detection**: `limit_of_detection(blank_signals, sensitivity)` — LOD = 3 × s_blank / sensitivity.

## L3 Tools Reference

The `electroanalytical_tools.py` module provides:

| Function | Purpose | Key Formula |
|----------|---------|-------------|
| `ise_calibration()` | ISE calibration via E vs log(C) regression | E = E₀ + S·log₁₀(C) |
| `ilkovic_equation()` | DC polarography diffusion current | I_d = 607·n·D^½·m^⅔·t^⅙·C |
| `concentration_from_ilkovic()` | Concentration from polarographic current | Inverse Ilkovic |
| `standard_addition_concentration()` | Standard addition via x-intercept extrapolation | Signal vs added amount → extrapolate |
| `mass_from_electrolysis()` | Mass from Faraday's law | m = (M·I·t)/(n·F) — n MUST match half-reaction |
| `coulometric_concentration()` | Conc from coulometric charge | C = Q·M/(n·F·V) |
| `coulometric_molar_concentration()` | Molar conc from charge | C = Q/(n·F·V) |
| `electrons_in_reduction()` | Lookup n for common reductions | Cu→Cu²⁺: n=2, Ag→Ag⁺: n=1 |
| `half_wave_potential()` | Polarography half-wave potential | E₁/₂ vs E°' relationship |
| `cyclic_voltammetry_peak_current()` | CV peak current (Randles-Sevcik) | iₚ = 2.69×10⁵×n^(3/2)×A×D^(1/2)×C×v^(1/2) |
| `coulometric_determination()` | Mass from charge (simple Faraday) | m = QM/(nF) |
| `amperometric_detection()` | Concentration from amperometric signal | C = (I - I_blank)/S |
| `nernst_potential()` | General Nernst equation | E = E° - (RT/nF)ln(Q) |

### Critical Notes

- **ISE calibration**: Linear regression on E (mV) vs log₁₀(C). Slope ≈ 59.16/z mV/decade at 25°C (Nernstian). Non-Nernstian slopes (e.g., 47 mV/dec for penicillin ISE) are common in practice.
- **Standard addition**: Plot signal vs added analyte amount, extrapolate to signal=0. x-intercept = amount in sample.
- **Electrolysis n**: ALWAYS verify from the half-reaction. Cu→Cu²⁺ means n=2 (TWO electrons). Using n=1 gives exactly 2× the correct mass.
- **Ilkovic**: Concentration must be in mM for μA output (conventional units).

### Worked Examples

**ISE Calibration (harvey_ch11_012)**: Penicillin ISE calibrated with 1e-4, 1e-3, 1e-2 M standards giving potentials 236, 189, 142 mV. Unknown at 142 mV → ~0.01 M. Note slope ~47 mV/dec (sub-Nernstian).

**Standard Addition (harvey_ch11_019)**: NO₃⁻ analysis gives ~2.9 mg/L.

**Electrolysis (brown_ch23_012)**: Cu at 500 A for 24 h: m = 63.55×500×86400/(2×96485) = 14,228 g. Answer key says 28.3 kg but used n=1 (WRONG — correct n=2).

---

## Cross-References
- Electrochemistry: [electrochemistry.md](./electrochemistry.md)
- Galvanic Cells: [galvanic_cells.md](./galvanic_cells.md)
