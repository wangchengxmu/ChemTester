# L2 Topic: Spectroscopy - Mass Spectrometry and IR

**Source**: Organic Chemistry (OpenStax) Ch12
**Created**: 2026-03-13
**Status**: Scaffold (Pass-2)

---

## Concept Overview

Mass spectrometry and infrared spectroscopy are fundamental analytical techniques for determining molecular structure. MS provides molecular weight and fragmentation patterns; IR identifies functional groups through bond vibration frequencies.

---

## Core Principles

### Mass Spectrometry

1. **Ionization**: Sample bombarded with high-energy electrons
2. **Fragmentation**: Cation radicals break into characteristic pieces
3. **Detection**: Ions separated by m/z ratio

**Key Peaks**:
- M⁺ (molecular ion): Gives molecular weight
- Base peak: Most abundant fragment
- M+1, M+2: Isotope peaks

### Infrared Spectroscopy

1. **Bond Vibrations**: Bonds absorb IR at characteristic frequencies
2. **Four Regions**:
   - 4000-2500 cm⁻¹: X-H stretches
   - 2500-2000 cm⁻¹: Triple bonds
   - 2000-1500 cm⁻¹: Double bonds
   - 1500-400 cm⁻¹: Fingerprint

**Bond Strength Rule**: Stronger bonds → higher frequency

---

## Key Tables

### MS Fragmentation Patterns

| Functional Group | Characteristic Fragment |
|------------------|------------------------|
| Alkanes | M-15, M-29, M-43, M-57 |
| Alcohols | M-18 (loss of H₂O) |
| Aldehydes | M-1 (loss of H•) |
| Ketones | α-cleavage products |
| Halides | M-35 (Cl), M-79 (Br) |

### IR Absorption Frequencies

| Functional Group | Range (cm⁻¹) | Intensity |
|------------------|--------------|-----------|
| O-H (alcohol) | 3400-3650 | Strong, broad |
| C=O | 1670-1780 | Strong |
| C=C | 1640-1680 | Medium |
| C≡C | 2100-2260 | Medium |
| C≡N | 2210-2260 | Medium |

---

## Connected Topics

- **Upstream**: [organic_functional_groups.md](organic_functional_groups.md)
- **Downstream**: NMR spectroscopy (Ch13)
- **Related**: [analytical_method_design.md](analytical_method_design.md) (Harvey)

---

## L3 Tools Required

1. `mass_spec_tools.py` - MW, exact mass, fragmentation
2. `ir_spectroscopy_tools.py` - Functional group identification
3. `spectral_analysis_tools.py` - Combined analysis

---

## L4 References (TODO)

- [ ] Exact isotope masses table
- [ ] Complete IR absorption table
- [ ] Fragmentation pattern database

---

## L5 Worked Examples (TODO)

- [ ] Molecular formula from exact mass
- [ ] Functional group identification from IR
- [ ] Compound identification from MS + IR

## L3 Tool Call Directives

**Source:** `vibrational_spectroscopy_tools.py`

⚠️ Stub file — no public functions implemented yet.

### Available functions:
- *(none — file is empty)*

## L3 Tool Call Directives

**Source:** `electronic_spectroscopy_tools.py`
Electronic spectroscopy: transition energies, Franck-Condon factors, selection rules, FRET.

### Available functions:
- `transition_energy_eV(wavelength_nm)` → float — Convert wavelength to transition energy in eV
- `transition_energy_wavenumber(wavelength_nm)` → float — Convert wavelength to wavenumber (cm⁻¹)
- `transition_energy_wavelength(E_J)` → float — Convert energy (J) to wavelength (nm)
- `wavelength_from_wavenumber(wavenumber_cm)` → float — Convert wavenumber to wavelength (nm)
- `franck_condon_factor(v1, v2, delta_q, omega_ratio)` → float — Calculate Franck-Condon factor
- `huang_rhys_factor(delta_q, omega)` → float — Calculate Huang-Rhys factor
- `vertical_transition_energy(E_0, delta_E_reorg)` → float — Calculate vertical (Franck-Condon) transition energy
- `vibronic_progression_positions(E_00, omega_cm, max_v)` → list — Calculate vibronic band positions
- `electronic_term_symbol(multiplicity, L, J)` → str — Construct electronic term symbol (e.g., ²S₁/₂)
- `ground_state_term(p_electrons)` → str — Determine ground state term for pⁿ configuration
- `electronic_selection_rules(L1, S1, J1, L2, S2, J2)` → Tuple[bool, str] — Check ΔS=0, ΔL=0,±1, ΔJ=0,±1 rules
- `laporte_selection_rule(g_u_initial, g_u_final)` → Tuple[bool, str] — Check g↔u parity selection
- `fluorescence_rate(A)` → float — Calculate radiative decay rate (s⁻¹)
- `intersystem_crossing_rate(S1_T1_gap_J, spin_orbit_coupling_J)` → float — Estimate ISC rate
- `phosphorescence_lifetime(A, ISC_rate)` → float — Calculate phosphorescence lifetime
- `quantum_yield_fluorescence(k_f, k_nr, k_isc)` → float — Calculate fluorescence quantum yield Φ_f
- `quantum_yield_phosphorescence(k_p, k_nr_T)` → float — Calculate phosphorescence quantum yield Φ_p
- `forster_radius(k_D, tau_D, J_overlap, n_refractive, kappa2)` → float — Calculate FRET Förster radius R₀ (m)
- `energy_transfer_efficiency_distance(R, R0)` → float — Calculate FRET efficiency E = R₀⁶/(R⁶+R₀⁶)
- `molar_absorptivity_from_oscillator(f, bandwidth_nm, lambda_max_nm)` → float — Estimate ε from oscillator strength

### Common errors:
- ❌ Using spin-only formula for non-S-state ions (needs J-dependent moment)
- ❌ Forgetting Laporte rule for centrosymmetric molecules (d-d transitions are parity-forbidden)

## L3 Tool Call Directives

**Source:** `electronic_spectroscopy_tools.py`
Electronic spectroscopy: transition energies, Franck-Condon factors, selection rules, FRET.

### Available functions:
- `transition_energy_eV(wavelength_nm)` → float — Convert wavelength to transition energy in eV
- `transition_energy_wavenumber(wavelength_nm)` → float — Convert wavelength to wavenumber (cm⁻¹)
- `transition_energy_wavelength(E_J)` → float — Convert energy (J) to wavelength (nm)
- `wavelength_from_wavenumber(wavenumber_cm)` → float — Convert wavenumber to wavelength (nm)
- `franck_condon_factor(v1, v2, delta_q, omega_ratio)` → float — Calculate Franck-Condon factor
- `huang_rhys_factor(delta_q, omega)` → float — Calculate Huang-Rhys factor
- `vertical_transition_energy(E_0, delta_E_reorg)` → float — Calculate vertical (Franck-Condon) transition energy
- `vibronic_progression_positions(E_00, omega_cm, max_v)` → list — Calculate vibronic band positions
- `electronic_term_symbol(multiplicity, L, J)` → str — Construct electronic term symbol (e.g., ²S₁/₂)
- `ground_state_term(p_electrons)` → str — Determine ground state term for pⁿ configuration
- `electronic_selection_rules(L1, S1, J1, L2, S2, J2)` → Tuple[bool, str] — Check ΔS=0, ΔL=0,±1, ΔJ=0,±1 rules
- `laporte_selection_rule(g_u_initial, g_u_final)` → Tuple[bool, str] — Check g↔u parity selection
- `fluorescence_rate(A)` → float — Calculate radiative decay rate (s⁻¹)
- `intersystem_crossing_rate(S1_T1_gap_J, spin_orbit_coupling_J)` → float — Estimate ISC rate
- `phosphorescence_lifetime(A, ISC_rate)` → float — Calculate phosphorescence lifetime
- `quantum_yield_fluorescence(k_f, k_nr, k_isc)` → float — Calculate fluorescence quantum yield Φ_f
- `quantum_yield_phosphorescence(k_p, k_nr_T)` → float — Calculate phosphorescence quantum yield Φ_p
- `forster_radius(k_D, tau_D, J_overlap, n_refractive, kappa2)` → float — Calculate FRET Förster radius R₀ (m)
- `energy_transfer_efficiency_distance(R, R0)` → float — Calculate FRET efficiency E = R₀⁶/(R⁶+R₀⁶)
- `molar_absorptivity_from_oscillator(f, bandwidth_nm, lambda_max_nm)` → float — Estimate ε from oscillator strength

### Common errors:
- ❌ Using spin-only formula for non-S-state ions (needs J-dependent moment)
- ❌ Forgetting Laporte rule for centrosymmetric molecules (d-d transitions are parity-forbidden)


## L3 Tools
- - `../L3_functions/rdkit_structure_tools.py` — predict_nmr_1h(), predict_nmr_13c(), predict_ir()
- - `../L3_functions/nmr_tools.py` — NMR splitting and coupling
