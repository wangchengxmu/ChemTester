---
id: capillary_electrophoresis
layer: 2
title: Capillary Electrophoresis and Electrochromatography
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - ../L3_functions/chromatography_tools.py
cross_links:
  - ./chromatography.md
  - ./electrochemistry.md
source: Skoog Instrumental Analysis Ch30 (LibreTexts)
---

## Context

Capillary Electrophoresis (CE) separates analytes based on their electrophoretic mobility in an electric field. It offers high efficiency (10⁵-10⁶ theoretical plates), minimal sample consumption (nL), and fast analysis times. Applications range from protein analysis to DNA sequencing to pharmaceutical quality control.

---

## Fundamental Principles

### Electrophoretic Mobility

Migration velocity in electric field:
```
v = μ_ep × E
```

Where:
- v = migration velocity
- μ_ep = electrophoretic mobility
- E = electric field strength (V/cm)

### Electrophoretic Mobility and Charge

```
μ_ep = q/(6πηr)
```

Where:
- q = net charge
- η = viscosity
- r = hydrodynamic radius

### Electroosmotic Flow (EOF)

Bulk flow of buffer due to charged capillary wall:

```
μ_eof = εζ/η
v_eof = μ_eof × E
```

Where:
- ε = dielectric constant
- ζ = zeta potential
- η = viscosity

### Net Migration

```
μ_app = μ_ep + μ_eof
v_app = μ_app × E
```

**Apparent mobility = electrophoretic mobility + electroosmotic mobility**

For cations: μ_app > μ_eof (migration toward cathode)
For anions: μ_app < μ_eof (can migrate toward cathode if EOF > electrophoretic mobility)

---

## Instrumentation

### Basic Components

1. **Capillary**
   - Fused silica (most common)
   - Inner diameter: 25-100 μm
   - Length: 20-100 cm
   - Outer coating: polyimide

2. **High Voltage Power Supply**
   - 10-30 kV
   - Current: typically 10-100 μA

3. **Detector**
   - UV-Vis (most common)
   - Fluorescence (higher sensitivity)
   - LIF (laser-induced fluorescence)
   - MS (mass spectrometry)

4. **Sample Introduction**
   - Hydrodynamic injection (pressure)
   - Electrokinetic injection (voltage)

### Injection Methods

#### Hydrodynamic Injection
```
V_injected = (ΔP × πr⁴ × t)/(8ηL)
```

Where:
- ΔP = pressure difference
- r = capillary radius
- t = injection time
- L = capillary length

#### Electrokinetic Injection
```
Q = μ_app × E × πr² × t × C
```

Note: Electrokinetic injection biases toward faster ions

---

## Separation Modes

### 1. Capillary Zone Electrophoresis (CZE)

**Most common mode**

Separation based on charge-to-size ratio:
```
μ_app = (q/r) × constant
```

**Migration order:** Small cations → Large cations → Neutral → Large anions → Small anions

### 2. Micellar Electrokinetic Chromatography (MEKC)

For neutral analytes using micelles:

```
k' = (t_r - t_mceo)/(t_mceo × (1 - t_r/t_mc))
```

Where:
- k' = retention factor
- t_r = analyte retention time
- t_mceo = micelle migration time
- t_mc = micelle elution time

**Surfactants:**
- SDS (anionic): Most common
- CTAB (cationic): For acidic compounds
- Bile salts: For hydrophobic compounds

### 3. Capillary Gel Electrophoresis (CGE)

Size-based separation:
```
log(MW) = a - b × t_m
```

Applications:
- DNA sequencing
- Protein sizing
- SDS-protein complexes

### 4. Capillary Isoelectric Focusing (CIEF)

Separation by isoelectric point (pI):
```
pH gradient + ampholytes
```

Analytes focus at pH = pI (net charge = 0)

### 5. Capillary Electrochromatography (CEC)

Hybrid of CE and HPLC:
- Stationary phase in capillary
- EOF drives mobile phase
- High efficiency of CE + selectivity of HPLC

---

## Efficiency and Resolution

### Theoretical Plates

```
N = μ_app × V/(2D)
```

Where:
- D = diffusion coefficient
- V = applied voltage

Typical N: 10⁵ - 10⁶ plates

### Resolution

```
R_s = (N)^(1/4) × (Δμ_app)/(μ̄_app)
```

### Factors Affecting Efficiency

| Factor | Effect |
|--------|--------|
| Higher voltage | ↑ Efficiency |
| Smaller diameter | ↑ Efficiency (better heat dissipation) |
| Lower ionic strength | ↑ Efficiency |
| Temperature control | ↑ Efficiency |
| Adsorption | ↓ Efficiency |

---

## Detection Methods

### UV-Vis Absorption

**Most common detector**
- Wavelength: 190-800 nm
- Path length limitation: capillary diameter

**Extended path length:**
- Bubble cell (3-5× sensitivity)
- Z-cell (10× sensitivity)

### Laser-Induced Fluorescence (LIF)

**Highest sensitivity:**
- Detection limit: 10⁻¹² M
- Requires fluorescent analyte or derivatization

### Mass Spectrometry (CE-MS)

- Interface: ESI (electrospray)
- Provides structural information
- Coupling challenges: buffer compatibility

---

## Applications

### Clinical Analysis

| Analyte | Mode | Detection |
|---------|------|-----------|
| Serum proteins | CZE | UV |
| Hemoglobin variants | CZE | UV |
| Urine organic acids | MEKC | UV |
| DNA fragments | CGE | LIF |

### Pharmaceutical Analysis

- Drug purity analysis
- Chiral separations
- Counterfeit drug detection

### Environmental Analysis

- Pesticide residues
- Inorganic ions
- Organic pollutants

---

## Problem-Solving Examples

### Example 1: Migration Time

**Problem**: A cation has μ_ep = 4.0×10⁻⁴ cm²/Vs. EOF mobility is 6.0×10⁻⁴ cm²/Vs. Applied voltage is 25 kV over 50 cm. Calculate migration time.

**Solution:**
```
μ_app = μ_ep + μ_eof = 4.0×10⁻⁴ + 6.0×10⁻⁴ = 1.0×10⁻³ cm²/Vs

E = V/L = 25000/50 = 500 V/cm

v = μ_app × E = 1.0×10⁻³ × 500 = 0.50 cm/s

t_m = L/v = 50/0.50 = 100 s
```

### Example 2: Injection Volume

**Problem**: Calculate injection volume for hydrodynamic injection at 0.5 psi for 5 s into a 50 cm × 50 μm capillary (water viscosity = 0.001 Pa·s).

**Solution:**
```
V = (ΔP × πr⁴ × t)/(8ηL)
V = (3447 × π × (25×10⁻⁶)⁴ × 5)/(8 × 0.001 × 0.50)
V = 1.06×10⁻⁹ L = 1.06 nL

Note: 0.5 psi = 3447 Pa
```

### Example 3: Efficiency Calculation

**Problem**: A peak has migration time 120 s with peak width 0.8 s. Calculate N.

**Solution:**
```
N = 16 × (t/w)² = 16 × (120/0.8)² = 16 × 22500 = 360,000 plates
```

### Example 4: MEKC Resolution

**Problem**: In MEKC with SDS, an analyte has t_r = 8 min. EOF marker at 3 min, micelle marker at 15 min. Calculate k'.

**Solution:**
```
k' = (t_r - t_0)/(t_0(1 - t_r/t_mc))
k' = (8 - 3)/(3 × (1 - 8/15))
k' = 5/(3 × 0.467)
k' = 3.57
```

---

## Decision Flow

1. **Choose separation mode:**
   - Charged analytes? → CZE
   - Neutral analytes? → MEKC
   - Size separation? → CGE
   - pI separation? → CIEF

2. **Select buffer:**
   - pH 2-12 range available
   - Consider analyte charge
   - Match detection method

3. **Optimize conditions:**
   - Voltage (higher = faster, more efficient)
   - Temperature
   - Buffer concentration

---

## Quick Reference - Buffer Selection

| pH Range | Buffer | Concentration |
|----------|--------|---------------|
| 2-3 | Phosphate | 20-50 mM |
| 4-6 | Acetate | 20-50 mM |
| 7-9 | Borate, Tris | 20-50 mM |
| 9-11 | Borate | 20-50 mM |

---

## Comparison with HPLC

| Parameter | CE | HPLC |
|-----------|-----|------|
| Efficiency | 10⁵-10⁶ | 10³-10⁴ |
| Sample volume | nL | μL-mL |
| Solvent consumption | mL/day | mL/min |
| Analysis time | Fast | Moderate |
| Reproducibility | Moderate | Good |
| Sensitivity | Lower | Higher |
| Cost | Lower | Higher |

---

## Cross-References
- Chromatography: [chromatography.md](./chromatography.md)
- Electrochemistry: [electrochemistry.md](./electrochemistry.md)
