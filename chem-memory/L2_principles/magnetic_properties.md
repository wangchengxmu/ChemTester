# Magnetic Properties of Coordination Compounds

## Overview

Magnetic properties provide experimental evidence for high-spin vs low-spin configurations. The number of unpaired electrons determines magnetic behavior.

**Source:** CHM 320 Chapter 9.4 (LibreTexts)

---

## Basic Concepts

### Types of Magnetic Behavior

| Type | Unpaired Electrons | Interaction with Field | Example |
|------|-------------------|------------------------|---------|
| **Diamagnetic** | 0 | Repelled (weak) | [Fe(CN)_6]^4- |
| **Paramagnetic** | ≥1 | Attracted | [Fe(H_2O)_6]^2+ |

### Origin of Magnetism
- Unpaired electrons have magnetic moments due to spin
- **Paramagnetism:** Random orientation, aligns with external field
- **Diamagnetism:** Induced magnetic field opposes external field

---

## Magnetic Moment

### Spin-Only Formula
For first-row transition metals (orbital contribution quenched):
```
μ_eff = √(n(n+2)) μ_B
```
Where:
- μ_eff = effective magnetic moment
- n = number of unpaired electrons
- μ_B = Bohr magneton (9.274 × 10^-24 J/T)

### Calculated vs Experimental Values

| n (unpaired e^-) | μ_eff (spin-only, μ_B) | μ_eff (observed range, μ_B) |
|------------------|------------------------|----------------------------|
| 1 | 1.73 | 1.7-2.2 |
| 2 | 2.83 | 2.8-3.5 |
| 3 | 3.87 | 3.8-4.5 |
| 4 | 4.90 | 4.8-5.5 |
| 5 | 5.92 | 5.8-6.5 |

### Orbital Contribution
For accurate predictions, consider spin-orbit coupling:
```
μ_eff = √(4S(S+1) + L(L+1)) μ_B
```
In octahedral complexes, orbital contribution often quenched due to crystal field.

---

## Magnetic Susceptibility

### Measurement Methods

1. **Gouy Balance**
   - Weigh sample with and without magnetic field
   - Paramagnetic samples appear heavier (attracted to field)
   - Δm ∝ susceptibility

2. **Evans Method (NMR)**
   - Measure shift of reference peak
   - Calculate susceptibility from shift

3. **SQUID Magnetometer**
   - Superconducting Quantum Interference Device
   - Very sensitive, measures small magnetic moments

### Calculating Unpaired Electrons

From magnetic susceptibility (χ), calculate μ_eff, then:
```
n = (μ_eff/μ_B)² - 2
n ≈ √((μ_eff/μ_B)² + 1) - 1
```

---

## Predicting Magnetic Properties

### Step 1: Determine d-electron count
```
d^n = group number - oxidation state
```

### Step 2: Determine spin state
Use ligand field strength:
- **Strong field ligands (CN^-, CO, NO_2^-):** Low-spin
- **Weak field ligands (F^-, Cl^-, H_2O):** High-spin
- **Consider metal period and charge**

### Step 3: Count unpaired electrons

| d^n | High-Spin Unpaired | Low-Spin Unpaired |
|-----|-------------------|-------------------|
| d^1 | 1 | 1 |
| d^2 | 2 | 2 |
| d^3 | 3 | 3 |
| d^4 | 4 | 2 |
| d^5 | 5 | 1 |
| d^6 | 4 | 0 |
| d^7 | 3 | 1 |
| d^8 | 2 | 2 |
| d^9 | 1 | 1 |
| d^10 | 0 | 0 |

### Step 4: Calculate magnetic moment
```
μ_eff = √(n(n+2)) μ_B
```

---

## Examples

### Example 1: [Fe(CN)_6]^4-
- Fe²⁺: d^6
- CN^- is strong field → low-spin
- Configuration: t_2g^6 e_g^0
- Unpaired electrons: 0
- **Diamagnetic**

### Example 2: [Fe(H_2O)_6]^2+
- Fe²⁺: d^6
- H_2O is weak field → high-spin
- Configuration: t_2g^4 e_g^2
- Unpaired electrons: 4
- μ_eff = √(4×6) = 4.90 μ_B
- **Paramagnetic**

### Example 3: [FeF_6]^3-
- Fe³⁺: d^5
- F^- is weak field → high-spin
- Configuration: t_2g^3 e_g^2
- Unpaired electrons: 5
- μ_eff = √(5×7) = 5.92 μ_B
- **Strongly paramagnetic**

### Example 4: [Fe(CN)_6]^3-
- Fe³⁺: d^5
- CN^- is strong field → low-spin
- Configuration: t_2g^5 e_g^0
- Unpaired electrons: 1
- μ_eff = 1.73 μ_B
- **Weakly paramagnetic**

---

## Spin Crossover

### Definition
Some complexes can switch between high-spin and low-spin states:
- Triggered by temperature, pressure, or light
- Common for Fe(II) (d^6) complexes
- Molecular spintronics applications

### Characteristics
- Abrupt or gradual transition
- Hysteresis possible
- Color change accompanies spin state change

---

## Types of Magnetism in Solids

| Type | Description | Example |
|------|-------------|---------|
| **Ferromagnetic** | Spins align parallel | Fe, Co, Ni metal |
| **Antiferromagnetic** | Spins align antiparallel | MnO |
| **Ferrimagnetic** | Unequal antiparallel alignment | Fe_3O_4 |
| **Paramagnetic** | Random spins, aligns with field | Most complexes |

---

## Experimental Applications

### 1. Determining Spin State
Compare μ_eff to spin-only values:
- Matches high-spin → high-spin complex
- Matches low-spin → low-spin complex
- Intermediate values → spin crossover or mixed

### 2. Identifying Oxidation State
Different oxidation states have different d^n and thus different μ_eff

### 3. Detecting Spin Crossover
Measure μ_eff vs temperature:
- Change in μ_eff indicates spin crossover

### 4. Bioinorganic Chemistry
- Hemoglobin: Fe(II) changes spin state upon O_2 binding
- Cytochromes: Monitor redox state via magnetic properties

---

## Related Topics
- [[crystal_field_theory]] - High-spin vs low-spin
- [[tanabe_sugano_diagrams]] - Electronic transitions
- [[coordination_chemistry]] - Complex structure

## References
- CHM 320 Chapter 9.4 (LibreTexts)
- Housecroft, Sharpe - Inorganic Chemistry

## L3 Implementation
→ `../L3_functions/chm320_inorganic_tools.py`

## L4 Reference Data
→ `../L4_reference/magnetic_moments.md`

## L5 Examples
→ `../L5_examples/crystal_field_examples.md
