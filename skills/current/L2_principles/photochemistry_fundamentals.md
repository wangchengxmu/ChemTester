# Photochemistry Fundamentals

## Concept Overview

Photochemistry studies chemical reactions initiated by absorption of light. Molecules in excited states have vastly different reactivity compared to their ground states.

## Key Principles

### Jablonski Diagram
- Vertical axis: energy; horizontal axis: spin multiplicity
- **S₀**: ground singlet state
- **S₁, S₂**: excited singlet states
- **T₁**: lowest triplet state
- Transitions: absorption, fluorescence, phosphorescence, IC, ISC

### Radiative Transitions
| Process | Transition | Timescale | Direction |
|---------|-----------|-----------|-----------|
| Absorption | S₀ → Sₙ | ~10⁻¹⁵ s | Up |
| Fluorescence | S₁ → S₀ | ~10⁻⁹ s | Down |
| Phosphorescence | T₁ → S₀ | ~10⁰–10² s | Down |

### Non-Radiative Transitions
| Process | Description | Spin change? |
|---------|-------------|-------------|
| Internal Conversion (IC) | Sₙ → Sₙ₋₁ (same multiplicity) | No |
| Intersystem Crossing (ISC) | S₁ → T₁ (spin flip) | Yes |
| Vibrational Relaxation | Within same electronic state | No |

### Kasha's Rule
Emission (fluorescence or phosphorescence) generally occurs from the lowest excited state of a given multiplicity (S₁ or T₁).

### Stokes Shift
```
λ_emission - λ_absorption > 0
```
Emission is red-shifted due to energy loss to vibrational relaxation in S₁ before emission.

### Quantum Yield (Φ)
```
Φ = (number of events) / (number of photons absorbed)
```
- Φ < 1: non-radiative pathways compete
- Φ = 1: all absorbed photons produce the event

## Problem-Solving Routes

1. **Predict emission type**: From Jablonski diagram, determine if fluorescence or phosphorescence dominates
2. **Calculate quantum yield**: Φ = k_r / (k_r + k_nr) where k_r = radiative rate, k_nr = non-radiative
3. **Estimate Stokes shift**: Δν = ν_abs - ν_em (in cm⁻¹ or nm)

## Links

- **L3 Tools**: `../L3_functions/photochemistry_tools.py`
- **L4 Data**: `../L4_reference/photochemistry_data.csv`
- **L5 Examples**: `../L5_examples/photochemistry_examples.md`

---

## Source Attribution: Roberts & Caserio, Ch28 (LibreTexts)
[Source: Roberts & Caserio, Basic Principles of Organic Chemistry, 2nd ed., Ch28: Photochemistry](https://chem.libretexts.org/Bookshelves/Organic_Chemistry/Basic_Principles_of_Organic_Chemistry_(Roberts_and_Caserio)/28%3A_Photochemistry)

- "The role of light in effecting chemical change has been recognized for many years. The connection between solar energy and the biosynthesis of plant carbohydrates from CO? and water was known by the early 1800s."
- Progress became rapid following development of spectroscopy and detection of transient species.
- Modern organic photochemistry correlates the nature of **excited electronic states** with the reactions they undergo.
- ISBN: 0-8053-8329-8. Copyright W. A. Benjamin, Inc., Menlo Park, CA (1977).

## Source Attribution: Chang, Physical Chemistry for the Biosciences, Ch15 (LibreTexts)
[Source: Physical Chemistry for the Biosciences (LibreTexts), Ch15: Photochemistry and Photobiology](https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/Physical_Chemistry_for_the_Biosciences_(LibreTexts)/15%3A_Photochemistry_and_Photobiology)

### 15.1: Key Principles Extracted
- **Franck-Condon Principle**: Electronic transitions are vertical �� nuclei don't move during electronic excitation. The molecule lands in an excited vibrational state.
- **Laporte Selection Rule**: Donor and acceptor orbitals must have different symmetry for allowed transitions. Centrosymmetric vs. antisymmetric orbitals.
- **Extinction coefficients by transition type**:
  - �С���*: 3,000�C25,000 M?1 cm?1 (strongly allowed)
  - p����*: 20�C150 M?1 cm?1 (weakly allowed)
  - p����*: 100�C7,000 M?1 cm?1
  - d��d: 5�C400 M?1 cm?1 (Laporte-forbidden)
- **Spin selection rule**: Spin state must be preserved during electronic transitions (singlet��singlet, triplet��triplet).
- **Ionizing vs nonionizing radiation**: Ionizing radiation (��, ��, ��, X-ray, high-energy UV) can break bonds and ionize molecules; nonionizing (visible, IR, microwave) causes heating only.

---

## [Source: Wikipedia, Jablonski Diagram]
### Jablonski Diagram Components
Named after Aleksander Jablonski (1933). Electronic states arranged vertically by energy, grouped horizontally by spin multiplicity.

**Transitions:**
- **Radiative** (straight arrows): Absorption, Fluorescence, Phosphorescence.
- **Nonradiative** (squiggly arrows):
  - **Vibrational Relaxation (VR)**: Rapid energy dissipation to surroundings.
  - **Internal Conversion (IC)**: Vibrational coupling between electronic states.
  - **Intersystem Crossing (ISC)**: Transition to different spin multiplicity. Enhanced by heavy atoms.

### [Source: Wikipedia, Fluorescence]
- S1->S0 (spin-allowed), lifetime 10^-9 to 10^-7 s.
- Stokes shift: emission > absorption wavelength.
- Quantum yield: Phi_F = photons emitted / photons absorbed.

### [Source: Wikipedia, Phosphorescence]
- T1->S0 (spin-forbidden), lifetime 10^-6 to 10^3 s.
- Heavy atom effect enhances ISC.

### [Source: Wikipedia, FRET]
- FRET efficiency: E = 1/(1 + (r/R0)^6), R0 typically 2-9 nm.
- Requirements: donor emission overlaps acceptor absorption; dipole orientation factor.
- Applications: molecular rulers, protein interaction studies.

### [Source: Wikipedia, Photochemistry]
**Key Laws:**
1. **Grotthuss-Draper (1818)**: Only absorbed light causes chemical change.
2. **Stark-Einstein**: 1 photon per molecule for primary process.
3. 1 einstein = Avogadro's number of photons.

## L3 Tool Call Directives

**Source:** `photochemistry_tools.py`
Quantum yield, excited state lifetimes, Stern-Volmer quenching, FRET, Marcus theory, Stokes shift.

### Available functions:
- `quantum_yield_calc(k_radiative, k_nonradiative=0, k_other=0)` → float — Φ = kr/(kr+knr+k_other), range 0–1
- `excited_state_lifetime(k_radiative, k_nonradiative=0, k_other=0)` → float — τ = 1/Σk (seconds)
- `stern_volmer_quenching(I0, I)` → float — I0/I ratio
- `stern_volmer_fit(quencher_concs, intensity_ratios)` → dict — Linear regression for K_SV
- `fret_efficiency(r, R0)` → float — E = 1/(1+(r/R0)⁶)
- `fret_distance(efficiency, R0)` → float — r = R0·(1/E-1)^(1/6)
- `marcus_rate(dG, lambda_reorg, V, T=298.15, in_eV=True)` → float — ET rate (s⁻¹)
- `stokes_shift(wavelength_abs, wavelength_em)` → dict — Shift in nm and cm⁻¹

### Common errors:
- ❌ Confusing radiative vs non-radiative rates — k_radiative gives Φ directly
- ❌ Not converting rate constants to consistent units (s⁻¹)
- ❌ Stern-Volmer curvature doesn't always mean static quenching — check for other causes
- ❌ Marcus theory: ΔG and λ must be in same units (eV or J, set in_eV accordingly)


---

**Source:** laser_photochemistry_tools.py
Einstein coefficients, Beer-Lambert law, laser physics (gain/threshold/modes), photochemistry (quantum yield, Stern-Volmer, photolysis).

### Available functions:
- einstein_A_from_B(B_value, frequency_Hz) → float — A = (8πhν³/c³)B
- einstein_B_from_A(A_value, frequency_Hz) → float — B = (c³/8πhν³)A
- einstein_B_absorption_from_B_emission(B_emission, g_upper, g_lower) → float — B_abs = (g_u/g_l)B_em
- spontaneous_emission_lifetime(A_value) → float — τ = 1/A (s)
- 
atural_linewidth(A_value) → float — Δν = A/(2π) (Hz)
- doppler_linewidth(frequency_Hz, temperature, mass_amu) → float — Doppler FWHM (Hz)
- eer_lambert_absorbance(concentration, path_length, epsilon) → float — A = εcl
- eer_lambert_transmittance(concentration, path_length, epsilon) → float — T = 10^(−A)
- concentration_from_absorbance(absorbance, path_length, epsilon) → float — c = A/(εl)
- epsilon_from_absorbance(absorbance, concentration, path_length) → float — ε = A/(cl)
- bsorbance_from_transmittance(transmittance) → float — A = −log₁₀(T)
- 	ransmittance_from_absorbance(absorbance) → float — T = 10^(−A)
- population_inversion_ratio(T, delta_E) → float — N_upper/N_lower (Boltzmann)
- small_signal_gain_cross_section(A_value, wavelength_m, lineshape_width_Hz) → float — σ (m²)
- laser_gain_coefficient(sigma, delta_N) → float — g = σ·ΔN (m⁻¹)
- laser_threshold_gain(gain_coefficient, mirror_R1, mirror_R2, length, loss_per_pass) → float — Net gain vs threshold
- cavity_mode_spacing(cavity_length) → float — Δν = c/(2L) (Hz)
- cavity_finesse(R) → float — F = π√R/(1−R)
- coherence_length(wavelength, linewidth) → float — L_coh = c/Δν (m)
- photon_energy(wavelength_nm) → float — E = hc/λ (J)
- photon_energy_eV(wavelength_nm) → float — Photon energy in eV
- photon_flux_moles(power_W, wavelength_nm) → float — Photon flux (einstein/s)
- quantum_yield(reactant_consumed, photons_absorbed) → float — Φ = mol reacted / einstein absorbed
- photochemical_rate(k, I_absorbed, quantum_yield) → float — rate = k·I·Φ
- excited_state_concentration(I_absorbed, tau) → float — [M*] = I·τ (steady state)
- luorescence_lifetime(natural_lifetime, quenching_rate) → float — 1/τ_obs = 1/τ₀ + k_q[Q]
- stern_volmer_quenching(tau_0, tau, quencher_concentration) → float — k_q from τ₀/τ = 1 + k_q[Q]
- energy_transfer_efficiency(k_ET, tau_0) → float — E = k_ET/(k_ET + 1/τ₀)
- photolysis_rate_constant(I_0, epsilon, path_length, quantum_yield) → float — k (s⁻¹)
- get_laser_info(laser_type) → dict — Properties of HeNe, Nd:YAG, CO₂, Ti:Sapphire, etc.

### Common errors:
- ❌ Mixing wavelength units: m for laser physics, nm for photochemistry
- ❌ Using Beer-Lambert for A > 2 (nonlinear regime — deviates from linearity)
- ❌ Forgetting Φ > 1 means chain reaction, not impossible
