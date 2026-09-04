---
id: chem.molecular_spectroscopy
layer: 2
title: Molecular Spectroscopy - Rotational, Vibrational, and Raman
source: LibreTexts Physical Chemistry Ch13-15
status: active
created: 2026-03-14
last_verified: 2026-03-14
---

# Molecular Spectroscopy - Rotational, Vibrational, and Raman

**L1 Parent:** spectroscopy.md, quantum_mechanics_core.md

## Problem Types

1. **Rotational Spectroscopy** - Microwave transitions, rotational constants, bond lengths
2. **Vibrational Spectroscopy** - IR transitions, vibrational frequencies, anharmonicity
3. **Vibrational-Rotational Spectroscopy** - Combined vib-rot bands, P and R branches
4. **Raman Spectroscopy** - Stokes/anti-Stokes lines, selection rules
5. **Selection Rules** - IR vs Raman activity, mutual exclusion principle

## Decision Tree

### 1. What type of spectroscopy?

- **Microwave region (1-100 GHz)** → Rotational spectroscopy
- **Infrared region (400-4000 cm⁻¹)** → Vibrational spectroscopy
- **Visible/UV excitation** → Raman spectroscopy
- **Multiple transitions** → Vibrational-rotational analysis

### 2. Rotational Spectroscopy Analysis

```
Given spectrum → Measure line positions → Calculate line spacing
Line spacing = 2B → B = spacing/2
From B → Calculate moment of inertia I = h/(8π²Bc)
From I → Calculate bond length r = √(I/μ)
```

**Key equations:**
```
E(J) = BJ(J+1)              [rigid rotor energy]
ν̃ = 2B(J+1)                 [transition wavenumber]
Δν̃ = 2B                     [line spacing]
g(J) = 2J+1                  [degeneracy]
```

**With centrifugal distortion:**
```
E(J) = BJ(J+1) - DJ²(J+1)²
ν̃ = 2B(J+1) - 4D(J+1)³
D ≈ 4B³/ω²                   [approximation]
```

### 3. Vibrational Spectroscopy

**Harmonic oscillator:**
```
G(v) = ω(v + ½)              [vibrational term]
ΔG = ω                        [constant spacing]
```

**Anharmonic oscillator:**
```
G(v) = ωₑ(v + ½) - ωₑxₑ(v + ½)²

ν̃₀₁ = ωₑ - 2ωₑxₑ            [fundamental]
ν̃₀₂ = 2ωₑ - 6ωₑxₑ           [first overtone]
```

**Dissociation energy:**
```
D₀ = ωₑ²/(4ωₑxₑ) - ωₑ/2
```

### 4. Vibrational-Rotational Bands

**P-branch (ΔJ = -1):**
```
ν̃_P(J) = ω - 2BJ
```

**R-branch (ΔJ = +1):**
```
ν̃_R(J) = ω + 2B(J+1)
```

**Band gap:**
```
Gap = ν̃_R(0) - ν̃_P(1) = 4B
```

### 5. Raman Spectroscopy

**Stokes and anti-Stokes:**
```
Δν̃_Stokes = ω               [energy lost]
Δν̃_anti-Stokes = ω          [energy gained]

I_S/I_AS = exp(hcω/kT)       [intensity ratio]
```

**Rotational Raman:**
```
ΔJ = 0, ±2                   [selection rule]
S-branch: ΔJ = +2, Δν̃ = B(4J+6)
O-branch: ΔJ = -2, Δν̃ = B(4J-6)
```

### 6. Selection Rules Summary

| Type | IR | Raman |
|------|-----|-------|
| Requirement | Dipole change | Polarizability change |
| Rotational | ΔJ = ±1 | ΔJ = 0, ±2 |
| Vibrational | Δv = ±1 | Δv = ±1 |

**Mutual exclusion (centrosymmetric):**
- IR active modes: ungerade (u)
- Raman active modes: gerade (g)
- No mode is both IR and Raman active

---

## Section 1: Rotational Spectroscopy

### Energy Levels

For a rigid diatomic rotor:
```
E_J = J(J+1)ℏ²/(2I) = BJ(J+1)  [in cm⁻¹ or energy units]

where:
  J = 0, 1, 2, ...    (rotational quantum number)
  I = μr²             (moment of inertia)
  B = h/(8π²cI)       (rotational constant in cm⁻¹)
```

### Transition Frequencies

Microwave spectroscopy observes transitions ΔJ = +1:
```
ν̃ = E(J+1) - E(J) = 2B(J+1)

Lines are equally spaced by 2B!
```

### Intensity Distribution

Population in level J:
```
N_J ∝ (2J+1) exp(-E_J/kT)
```

Most populated level:
```
J_max ≈ √(kT/2Bhc) - ½
```

---

## Section 2: Centrifugal Distortion

### Non-rigid Rotor

Real molecules stretch under rotation:
```
E(J) = BJ(J+1) - DJ²(J+1)²

where D = centrifugal distortion constant
```

D can be estimated:
```
D ≈ 4B³/ω²
```

Effect on spectrum:
- Lines slightly closer together at high J
- Deviation increases with J³

---

## Section 3: Vibrational Spectroscopy

### Harmonic Oscillator

Energy levels:
```
E_v = (v + ½)hν = (v + ½)hcω̃

v = 0, 1, 2, ...

Transition: v=0 → v=1 at frequency ν̃ = ω
```

### Anharmonicity

Real molecules are not perfectly harmonic:
```
G(v) = ωₑ(v + ½) - ωₑxₑ(v + ½)² + ...

where:
  ωₑ = harmonic frequency
  ωₑxₑ = anharmonicity constant (always positive)
```

Consequences:
- Energy levels get closer together
- Overtones become weakly allowed
- Dissociation limit reached at finite v

### Dissociation Energy

From vibrational constants:
```
D_e = ωₑ²/(4ωₑxₑ)         [well depth]
D₀ = D_e - ωₑ/2            [from ground state]
```

---

## Section 4: Vibrational-Rotational Bands

### Combined Transitions

When a molecule vibrates, it also rotates:
```
Δv = +1 (fundamental)
ΔJ = ±1 (rotational change)
```

**P-branch (ΔJ = -1):**
- Lower frequency side
- J ≥ 1 required (J=0 has no lower level)

**R-branch (ΔJ = +1):**
- Higher frequency side
- J ≥ 0 possible

### Band Structure

```
         R(2)
            R(1)
               R(0)        band origin
                           ↓
     P(3)  P(2)  P(1)    |    R(0)  R(1)  R(2)  R(3)
                        ←|→
                    lower ν̃    higher ν̃
```

**Gap at band center:**
- No Q-branch (ΔJ = 0) for diatomics
- Gap = 4B between R(0) and P(1)

---

## Section 5: Raman Spectroscopy

### Principle

Inelastic light scattering:
- Stokes: photon loses energy → molecule gains vibrational quantum
- Anti-Stokes: photon gains energy → molecule loses vibrational quantum

### Intensity Ratio

Population of v=0 vs v=1:
```
I_Stokes/I_Anti-Stokes = exp(hcω/kT)
```

At room temperature:
- Most molecules in v=0
- Stokes much more intense

### Rotational Raman

Selection rule: ΔJ = 0, ±2

**S-branch (ΔJ = +2):**
```
Δν̃ = B(4J + 6)
```

**O-branch (ΔJ = -2):**
```
Δν̃ = B(4J - 6)
```

---

## Tool Functions

See: `../L3_functions/molecular_spectroscopy_tools.py`

**Rotational:**
- `rotational_energy_J(J, B_cm)` - Energy in cm⁻¹
- `rotational_line_position(J, B_cm)` - Transition wavenumber
- `bond_length_from_B(B_cm, mu_amu)` - Get bond length from B

**Vibrational:**
- `vibrational_energy_v(v, wavenumber_cm)` - Harmonic energy
- `anharmonic_fundamental(omega_e, omega_e_x_e)` - Anharmonic transition
- `dissociation_energy_vibrational(omega_e, omega_e_x_e)` - D₀

**Vib-Rot:**
- `rotation_vibration_branch_position(J, B, omega, branch)` - Line positions

**Raman:**
- `raman_line_positions(excitation_nm, wavenumber_cm)` - Wavelengths
- `stokes_antistokes_intensity_ratio(wavenumber, T)` - Intensity ratio

---

## Cross-References

**L1:** `../L1_ontology/chemistry-core-map.md`

**L2:** 
- `quantum_mechanics_core.md` - Schrödinger equation
- `spectroscopy.md` - Mass spec and IR (organic)
- `nmr_spectroscopy.md` - NMR techniques

**L3:** `../L3_functions/molecular_spectroscopy_tools.py`

**Source:** LibreTexts Physical Chemistry Ch13-15

---

## Quick Reference Tables

### Common Diatomic Molecules

| Molecule | B (cm⁻¹) | ωₑ (cm⁻¹) | rₑ (pm) |
|----------|----------|-----------|---------|
| H₂ | 60.86 | 4401 | 74.1 |
| N₂ | 1.998 | 2359 | 109.8 |
| O₂ | 1.446 | 1580 | 120.7 |
| CO | 1.931 | 2170 | 112.8 |
| HCl | 10.59 | 2991 | 127.5 |
| HBr | 8.47 | 2650 | 141.4 |

### Selection Rules

| Transition | IR | Raman |
|------------|-----|-------|
| Rotational | ΔJ=±1 | ΔJ=0,±2 |
| Vibrational | Δv=±1 | Δv=±1 |
| Requirement | μ changes | α changes |

---

*L2 Principle Document*
*Generated: 2026-03-14*

## L3 Tool Call Directives

**Source:** molecular_spectroscopy_tools.py
Molecular Spectroscopy Tools - L3 Implementation

### Available functions:
- rotational_energy_J(J, B_cm) → float — Calculate rotational energy level in wavenumbers.
- rotational_energy_joules(J, B_cm) → float — Calculate rotational energy in Joules.
- rotational_line_position(J_lower, B_cm) → float — Calculate position of rotational transition J -> J+1.
- rotational_line_frequency_GHz(J_lower, B_cm) → float — Calculate rotational transition frequency in GHz.
- rotational_line_spacing(B_cm) → float — Calculate spacing between adjacent rotational lines.
- rotational_degeneracy(J) → int — Calculate degeneracy of rotational level J.
- rotational_population(J, B_cm, temperature) → float — Calculate Boltzmann population of rotational level J.
- rotational_partition_function_diatomic(B_cm, temperature) → float — Calculate rotational partition function for diatomic molecule.
- most_populated_rotational_level(B_cm, temperature) → int — Find the most populated rotational level at given temperature.
- rotational_constant_from_line_spacing(spacing_cm) → float — Calculate rotational constant from line spacing.
- bond_length_from_B(B_cm, reduced_mass_amu) → float — Calculate bond length from rotational constant.
- rotational_constant_from_geometry(m1_amu, m2_amu, bond_length_m) → float — Calculate rotational constant from atomic masses and bond length.
- rotational_energy_with_distortion(J, B_cm, D_cm) → float — Calculate rotational energy with centrifugal distortion.
- distorted_rotational_line(J_lower, B_cm, D_cm) → float — Calculate rotational line position with distortion correction.
- centrifugal_distortion_constant(B_cm, wavenumber_cm) → float — Estimate centrifugal distortion constant from vibrational frequency.
- vibrational_energy_v(v, wavenumber_cm) → float — Calculate harmonic oscillator vibrational energy.
- vibrational_transition_fundamental(wavenumber_cm) → float — Calculate fundamental vibrational transition (v=0->1).
- vibrational_first_overtone(wavenumber_cm) → float — Calculate first overtone (v=0->2).
- anharmonic_vibrational_energy(v, omega_e, omega_e_x_e) → float — Calculate anharmonic vibrational energy.
- anharmonic_fundamental(omega_e, omega_e_x_e) → float — Calculate anharmonic fundamental transition.
- dissociation_energy_vibrational(omega_e, omega_e_x_e) → float — Calculate dissociation energy from vibrational constants.
- rotation_vibration_branch_position(J, B_cm, wavenumber_cm, branch) → float — Calculate line position in vibrational-rotational band.
- vibration_rotation_band_gap(B_cm, wavenumber_cm) → Dict — Calculate band origin and spacing in vibration-rotation spectrum.
- raman_stokes_shift(wavenumber_cm) → float — Calculate Stokes Raman shift.
- raman_antistokes_shift(wavenumber_cm) → float — Calculate anti-Stokes Raman shift.
- raman_line_positions(excitation_nm, wavenumber_cm) →  — Calculate Raman line positions for given excitation wavelength.
- stokes_antistokes_intensity_ratio(wavenumber_cm, temperature) → float — Calculate intensity ratio of Stokes to anti-Stokes Raman lines.
- rotational_raman_selection_rules(J_initial) →  — Calculate allowed DeltaJ values for rotational Raman transitions.
- rotational_raman_line_position(J, B_cm, branch) → float — Calculate rotational Raman line position.
- rotational_selection_rule_microwave(J_initial) →  — Allowed rotational transitions for microwave spectroscopy.
- vibrational_selection_rule_ir(v_initial) →  — Allowed vibrational transitions for IR spectroscopy.
- is_ir_active(dipole_moment_change) → bool — Determine if vibrational mode is IR active.
- is_raman_active(polarizability_change) → bool — Determine if vibrational mode is Raman active.
- mutual_exclusion_rule(point_group) →  — Apply mutual exclusion rule for centrosymmetric molecules.
- wavelength_to_wavenumber(wavelength_nm) → float — Convert wavelength to wavenumber.
- wavenumber_to_wavelength(wavenumber_cm) → float — Convert wavenumber to wavelength.
- frequency_to_wavenumber(frequency_GHz) → float — Convert frequency to wavenumber.
- wavenumber_to_frequency(wavenumber_cm) → float — Convert wavenumber to frequency.
- spectral_resolution_required(delta_nu_cm) → float — Calculate required spectral resolution to resolve lines.
- doppler_broadening(wavenumber_cm, temperature, mass_amu) → float — Calculate Doppler broadening width.
- get_spectroscopic_constants(molecule) → Dict — Get spectroscopic constants for a diatomic molecule.
- predict_rotational_spectrum(molecule, J_max) →  — Predict rotational spectrum for a diatomic molecule.
- predict_vibrational_rotational_band(molecule, J_max) → Dict — Predict vibrational-rotational band structure.

### Common errors:
- ❌ Passing wrong parameter types or missing required arguments
