---
id: atomic_mass_spectrometry
layer: 2
title: Atomic Mass Spectrometry (ICP-MS)
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - ../L3_functions/mass_spec_tools.py
cross_links:
  - ./atomic_emission_spectrometry.md
  - ./spectroscopy.md
source: Skoog Instrumental Analysis Ch11 (LibreTexts)
---

## Context

Inductively Coupled Plasma Mass Spectrometry (ICP-MS) combines the high-temperature ICP source with mass spectrometric detection. It provides the lowest detection limits (ppt), widest linear dynamic range (9 orders), and multi-element capability with isotopic information.

---

## Fundamental Principles

### Ionization in Plasma

Atoms are ionized in the high-temperature plasma:

```
M → M⁺ + e⁻
```

Most elements have ionization efficiency > 90% in ICP.

### Mass-to-Charge Analysis

Ions are separated by m/z ratio:
```
m/z = (B²r²e)/(2V)
```

Where:
- m = ion mass
- z = charge
- B = magnetic field
- r = radius of curvature
- e = electron charge
- V = accelerating voltage

### Signal Intensity

```
I = k × c × (abundance) × (ionization efficiency)
```

---

## Instrumentation

### ICP Source

Same plasma as ICP-OES:
- Temperature: 6000-10000 K
- RF power: 1-1.5 kW
- Argon flow: ~15 L/min

### Interface Region

**Critical for transferring ions from atmospheric pressure to vacuum:**

1. **Sampling cone** - First aperture (~1 mm)
2. **Skimmer cone** - Second aperture (~0.5 mm)
3. **Ion lenses** - Focus ion beam

### Mass Analyzers

#### Quadrupole (Most Common)

- Four parallel rods with RF/DC voltages
- Mass range: 2-260 amu (extended to 300 amu)
- Resolution: ~0.7 amu
- Fast scanning (< 1 ms per mass)

**Mass filter equation:**
```
(m/z)_pass = (V)/(14.4 × f² × r₀²)
```

#### Sector Field (Magnetic + Electric)

- Higher resolution (M/ΔM up to 10,000)
- Better for resolving interferences
- More expensive

#### Time-of-Flight (TOF)

- Fastest analysis (full spectrum in μs)
- Good for transient signals
- Moderate resolution (~2000)

#### Collision/Reaction Cell

Located before mass analyzer:
- Removes polyatomic interferences
- Uses collision gases (He, H₂, NH₃)
- Reaction gases selectively react with interferences

### Detectors

| Type | Dynamic Range | Application |
|------|---------------|-------------|
| Electron multiplier | 10⁸ | Low signals |
| Faraday cup | 10⁶ | High signals |
| Daly detector | 10⁷ | Both |

---

## Interferences

### Isobaric Interferences

Different elements with same nominal mass:

| Analyte | Interference | Resolution Needed |
|---------|--------------|-------------------|
| ⁵⁸Ni | ⁵⁸Fe | ~30,000 |
| ⁸⁷Rb | ⁸⁷Sr | ~30,000 |
| ¹¹⁴Cd | ¹¹⁴Sn | ~50,000 |

**Correction:** Mathematical correction using another isotope

### Polyatomic Interferences

Molecular ions formed in plasma or interface:

| Analyte | Interference | Source |
|---------|--------------|--------|
| ⁴⁰Ca⁺ | ⁴⁰Ar⁺ | Plasma gas |
| ⁵⁶Fe⁺ | ⁴⁰Ar¹⁶O⁺ | Plasma + O |
| ⁷⁵As⁺ | ⁴⁰Ar³⁵Cl⁺ | Cl in matrix |
| ⁸⁰Se⁺ | ⁴⁰Ar²⁺ | Plasma gas |

**Correction Methods:**
1. Collision/reaction cell
2. Cool plasma conditions
3. Alternative isotope
4. High resolution

### Doubly Charged Ions

Elements with low second ionization potential:
- Ba²⁺ interferes at m/2
- Sr²⁺ interferes at m/2

### Matrix Effects

- Space charge effects (heavy elements suppress light)
- Signal suppression from high TDS
- Deposition on cones

---

## Quantitative Analysis

### Calibration Methods

#### External Calibration

```
I = m × c + b
```

Limited to simple matrices.

#### Internal Standardization

**Best for ICP-MS** - compensates for drift and matrix effects:

```
Ratio = I_analyte / I_IS
```

**Internal standard selection criteria:**
- Similar mass to analyte
- Similar ionization potential
- Not present in sample
- No interferences

| Analyte Mass Range | Internal Standard |
|--------------------|-------------------|
| Light (Li-Mg) | Sc, Ge |
| Medium (Al-Zn) | Rh, In |
| Heavy (As-U) | Re, Bi |

#### Standard Addition

For severe matrix effects:
```
Add known amounts to aliquots of sample
Plot signal vs added concentration
Extrapolate to find original concentration
```

#### Isotope Dilution

**Most accurate method:**

```
c_x = c_s × (m_s/m_x) × (A_s - R×B_s)/(R×B_x - A_x)
```

Where:
- R = measured isotope ratio
- A_x, B_x = natural abundances
- A_s, B_s = spike abundances
- m_x, m_s = masses

### Detection Limits

| Element | LOD (ng/L) | Element | LOD (ng/L) |
|---------|------------|---------|------------|
| Li | 0.5 | As | 1 |
| Mg | 0.1 | Se | 5 |
| Fe | 0.5 | Cd | 0.1 |
| Cu | 0.2 | Pb | 0.1 |
| Zn | 0.5 | U | 0.01 |

---

## Problem-Solving Examples

### Example 1: Internal Standard Calculation

**Problem**: Cd at 114 m/z, using In as IS. Calculate Cd concentration.

| Sample | Cd counts | In counts | Cd/In ratio |
|--------|-----------|-----------|-------------|
| Blank | 50 | 50000 | 0.001 |
| Std 1 ppb | 1000 | 50000 | 0.020 |
| Std 5 ppb | 5000 | 50000 | 0.100 |
| Unknown | 2800 | 48000 | 0.058 |

**Solution:**
```
Correct for blank: 0.058 - 0.001 = 0.057
Slope = (0.100 - 0.020)/(5-1) = 0.020/ppb
c = 0.057/0.020 = 2.85 ppb

Or use linear regression for more accuracy.
```

### Example 2: Isobaric Correction

**Problem**: ⁵⁸Ni signal includes contribution from ⁵⁸Fe. Calculate true Ni.

Given:
- Measured ⁵⁸ mass = 5000 cps
- Measured ⁵⁶Fe = 3000 cps
- Natural ⁵⁸Fe/⁵⁶Fe = 0.003

**Solution:**
```
⁵⁸Fe contribution = 3000 × 0.003 = 9 cps
True ⁵⁸Ni = 5000 - 9 = 4991 cps
```

### Example 3: Oxide Ratio

**Problem**: CeO⁺/Ce⁺ ratio should be < 2%. Calculate from data.

Given:
- Ce⁺ (140) = 1000000 cps
- CeO⁺ (156) = 15000 cps

**Solution:**
```
CeO⁺/Ce⁺ = 15000/1000000 = 0.015 = 1.5%
This is acceptable (< 2%).
```

---

## Decision Flow

1. **Choose mass analyzer:**
   - Routine analysis? → Quadrupole
   - Complex interferences? → Sector field
   - Fast transient signals? → TOF

2. **Select internal standard:**
   - Match mass to analytes
   - Check for presence in sample
   - Verify no interferences

3. **Address interferences:**
   - Polyatomic? → Collision cell or cool plasma
   - Isobaric? → Alternative isotope or correction
   - Matrix? → Dilution or standard addition

---

## Comparison with Other Techniques

| Parameter | ICP-OES | ICP-MS | GFAAS |
|-----------|---------|--------|-------|
| Detection limit | ppb | ppt | ppb |
| Linear range | 5 orders | 9 orders | 2 orders |
| Multi-element | Yes | Yes | No |
| Isotopic info | No | Yes | No |
| Interferences | Spectral | Mass | Chemical |
| Throughput | High | High | Low |

---

## Quick Reference - Interference Removal

| Interference Type | Method |
|-------------------|--------|
| Ar⁺ on Ca⁺ | Cool plasma, reaction cell |
| ArO⁺ on Fe⁺ | Reaction cell (H₂) |
| ArCl⁺ on As⁺ | Reaction cell (He, H₂) |
| Isobaric | High resolution or correction equation |

---

## Cross-References
- Atomic Emission: [atomic_emission_spectrometry.md](./atomic_emission_spectrometry.md)
- Mass Spectrometry: [spectroscopy.md](./spectroscopy.md)

## L3 Tool Call Directives

**Source:** `mass_spec_tools.py`

Mass spectrometry calculations: molecular weight, exact mass, isotope peak intensities, and fragmentation analysis.

### Available functions:
- `molecular_weight(formula)` → float — Average MW using average atomic masses; formula = {'C': 6, 'H': 12, 'O': 6}
- `exact_mass(formula)` → float — Exact mass using most abundant isotope masses (amu)
- `nominal_mass(formula)` → int — Integer mass of most abundant isotopes
- `m_plus_one_intensity(carbons, hydrogens=0, nitrogens=0)` → float — M+1 peak % (13C: 1.10%/C is dominant)
- `m_plus_two_intensity(carbons, oxygens, sulfurs, chlorines, bromines)` → float — M+2 peak %; Cl gives 24.23%/atom, Br gives 49.31%/atom
- `fragment_mass(molecular_ion, lost_mass)` → int — Fragment m/z from loss
- `identify_fragment_loss(molecular_ion, fragment_mz)` → dict — Returns {'lost_mass', 'possible'} identity

### Common errors:
- ❌ Forgetting Cl and Br give characteristic M+2 patterns (Cl: 3:1, Br: 1:1 doublet)
- ❌ Not using M+1 intensity to estimate carbon count (≈ 1.1 × #carbons %)
- ❌ Confusing average mass (for MW) with exact mass (for high-resolution MS)
