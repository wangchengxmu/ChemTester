---
id: microscopy.principles
layer: 2
title: Microscopy Principles (SEM, TEM, AFM, STM)
parent: instrumental_analysis
stability: high
confidence: high
constraints:
  - resolution limited by wavelength (Abbe limit)
  - electron wavelength determined by accelerating voltage
  - AFM force limited by cantilever spring constant
  - STM requires conductive samples
source: LibreTexts Instrumental Analysis Ch21 + Surface Science Ch7
---

# Microscopy Principles

## Overview

Microscopy encompasses techniques for imaging structures at scales from micrometers to angstroms. Key techniques include:
- **Optical Microscopy**: Limited by diffraction (~200 nm resolution)
- **SEM**: Electron beam scanning, surface imaging
- **TEM**: Electron transmission, atomic resolution
- **AFM**: Force-based surface profiling
- **STM**: Quantum tunneling for atomic-scale imaging

---

## 1. Resolution Fundamentals

### Abbe Diffraction Limit

The fundamental resolution limit for any wave-based imaging system:

```
d = λ / (2 × NA)
```

Where:
- d = minimum resolvable distance
- λ = wavelength of radiation
- NA = numerical aperture (n × sin θ)

**Key Insight**: Shorter wavelength → better resolution

### Numerical Aperture

```
NA = n × sin θ
```

- n = refractive index of medium
- θ = half-angle of light cone

**Typical values**:
- Dry objective: NA = 0.1-0.95
- Oil immersion: NA = 1.0-1.4

---

## 2. Electron Microscopy

### de Broglie Wavelength

Electrons have wave-like properties with wavelength determined by energy:

**Non-relativistic** (for voltages < 100 kV):
```
λ (nm) = 1.23 / √V
```

**Relativistic** (for higher voltages):
```
λ = h / √[2m_e × eV × (1 + eV/(2m_e c²))]
```

| Voltage | λ (pm) | λ_rel (pm) |
|---------|--------|------------|
| 100 kV  | 3.88   | 3.70       |
| 200 kV  | 2.74   | 2.51       |
| 300 kV  | 2.24   | 1.96       |

### SEM Resolution

```
d = 0.753 / (α × √V)
```

- α = half aperture angle (radians)
- V = accelerating voltage (kV)

### TEM Resolution

Limited by spherical aberration:

```
δ = A × Cs^(1/4) × λ^(3/4)
```

---

## 3. Scanning Probe Microscopy

### AFM (Atomic Force Microscopy)

Force measurement via cantilever deflection:

```
F = k × x
```

- k = spring constant (N/m)
- x = deflection (m)

**Spring constant from geometry**:
```
k = E × w × t³ / (4 × L³)
```

**Lateral resolution** (tip-limited):
```
δ ≈ √(R × D)
```

### STM (Scanning Tunneling Microscopy)

Tunneling current depends exponentially on distance:

```
I_t = V × e^(-C × d)
```

- C ≈ 10 nm⁻¹ for metals
- Current changes ~10× per 0.1 nm distance change

---

## 4. Depth of Field

```
DOF = λ / (2 × NA²)
```

Electron microscopes have very large depth of field due to small effective NA.

---

## Navigation

- **L3 Tools**: `../L3_functions/microscopy_tools.py`
- **L4 Reference**: `../L4_reference/microscopy_parameters.md`
- **L5 Examples**: `../L5_examples/microscopy_examples/

## Related Topics

- Electron configurations (quantum mechanics basis)
- Crystallography (atomic structure analysis)
- Surface chemistry (surface phenomena)

## L3 Tool Call Directives

**Source:** `microscopy_tools.py`
Microscopy calculations: electron wavelength, resolution (SEM/TEM/AFM/STM), magnification.

### Available functions:
- `electron_wavelength_nonrelativistic(voltage_v)` → float — Electron wavelength (pm), valid <100 kV
- `electron_wavelength_relativistic(voltage_v)` → float — Relativistic electron wavelength (pm)
- `abbe_resolution_limit(wavelength_nm, na)` → float — Optical diffraction limit d = λ/(2NA)
- `sem_resolution(working_distance_mm, beam_voltage_kv, aperture_angle_rad)` → float — SEM resolution (nm)
- `tem_resolution(spherical_aberration_mm, voltage_kv, coefficient)` → float — TEM resolution (nm)
- `sem_magnification(display_size_mm, sample_size_mm)` → float — SEM magnification
- `afm_force(spring_constant_n_m, deflection_nm)` → float — AFM cantilever force (nN) via Hooke's law
- `afm_resolution(tip_radius_nm, feature_depth_nm)` → float — AFM lateral resolution δ~√(RD)
- `afm_spring_constant(youngs_modulus_pa, width_um, thickness_um, length_um)` → float — Cantilever k (N/m)
- `stm_tunneling_current(bias_voltage_v, distance_nm, constant_c)` → float — STM tunneling current I=V·e^(-Cd)
- `stm_current_ratio(distance_change_nm, constant_c)` → float — Current ratio for tip distance change
- `depth_of_field(wavelength_nm, na)` → float — Optical DOF = λ/(2NA²)
- `numerical_aperture(refractive_index, half_angle_deg)` → float — NA = n·sin(θ)
- `wavelength_from_voltage_simplified(voltage_kv)` → float — Quick estimate λ(nm) = 1.23/√V
- `compare_optical_electron_resolution(optical_wl, optical_na, e_voltage, e_aperture)` → dict — Compare resolutions
- `optimal_tem_aperture(voltage_kv, spherical_aberration_mm)` → float — Optimal TEM semi-angle (mrad)

### Common errors:
- ❌ Using non-relativistic formula for TEM (>100 kV needs relativistic correction)
- ❌ Confusing working distance with aperture angle in SEM resolution
