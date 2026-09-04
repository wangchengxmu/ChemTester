---
id: chem.bohr_model
layer: 2
title: Bohr Model and Atomic Spectra
source: LibreTexts Chemistry 2e Ch06.02
status: active
created: 2026-03-11
last_verified: 2026-03-11
---

# Bohr Model and Atomic Spectra

## Problem type
Calculate electron energy levels and wavelengths of emitted/absorbed photons.

## Decision tree

1. **What is asked?**
   - Energy of level → Use E_n = -R_H/n²
   - Energy of transition → Use ΔE = R_H(1/n_f² - 1/n_i²)
   - Wavelength of photon → Use λ = hc/|ΔE|
   - Identify spectral series → Match n_final

2. **Type of transition?**
   - Emission: n_initial > n_final (energy released)
   - Absorption: n_initial < n_final (energy absorbed)

3. **Units?**
   - Energy in J (convert to kJ/mol: multiply by Avogadro's number)
   - Wavelength in m or nm

## Core formulas

### Bohr energy levels
```
E_n = -R_H / n²
where:
  E_n = energy of electron in level n
  R_H = Rydberg constant = 2.18 × 10⁻¹⁸ J
  n = principal quantum number (1, 2, 3, ...)
```

### Energy of transition
```
ΔE = E_final - E_initial = R_H × (1/n_final² - 1/n_initial²)
```

### Wavelength from transition
```
λ = h × c / |ΔE|
```

### Rydberg formula (alternative)
```
1/λ = R × (1/n_final² - 1/n_initial²)
where R = 1.097 × 10⁷ m⁻¹ (Rydberg constant for wavelength)
```

## Spectral Series

| Series | n_final | Region | Example |
|--------|---------|--------|---------|
| Lyman | 1 | UV | n=2→1: λ = 121.5 nm |
| Balmer | 2 | Visible | n=3→2: λ = 656.3 nm (red) |
| Paschen | 3 | IR | n=4→3: λ = 1875 nm |

## Constraints
- Bohr model only accurate for H and H-like ions (single electron)
- Assumes circular orbits
- Does not work for multi-electron atoms

## Common patterns
1. Calculate energy of electron in orbit n
2. Find wavelength of emission/absorption
3. Identify spectral series from wavelength
4. Calculate ionization energy (n=∞)

## Links

### L3 Implementation
- `../L3_functions/bohr_model_tools.py` (TODO)

### L4 Reference

### L5 Examples
- `../L5_examples/quantum-mechanics/ (TODO)

## Source trace
- `../sources/ingestion/source-electronic-structure-stepwise.md` section 6.02

## L3 Tool Call Directives


**Source:** `bohr_model_tools.py`

L3 tool module for bohr model tools

### Available functions:
- `energy_level(n)` → any — Calculate energy of electron in Bohr orbit n.
- `energy_transition(n_initial, n_final)` → any — Calculate energy of photon from electron transition.
- `wavelength_transition(n_initial, n_final)` → any — Calculate wavelength of photon from electron transition.
- `frequency_transition(n_initial, n_final)` → any — Calculate frequency of photon from electron transition.
- `identify_spectral_series(n_final)` → any — Identify spectral series from final energy level.
- `ionization_energy_from_level(n)` → any — Calculate energy needed to ionize from level n.
- `ground_state_ionization_energy()` → any — Return ionization energy from ground state (n=1).
- `energy_level_hydrogen_like(Z, n)` → any — Calculate energy for hydrogen-like ion with nuclear charge Z.
- `wavelength_hydrogen_like(Z, n_initial, n_final)` → any — Calculate wavelength for hydrogen-like ion transition.
- `J_to_kJ_per_mol(J)` → any — Convert joules to kJ/mol.
- `m_to_nm(m)` → any — Convert meters to nanometers.

### Common errors:
- ❌ Passing wrong parameter types (strings where numbers expected)
- ❌ Forgetting required parameters
