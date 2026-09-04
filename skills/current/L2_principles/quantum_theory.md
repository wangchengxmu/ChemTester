---
id: chem.quantum_theory
layer: 2
title: Quantum Theory and Wave-Particle Duality
source: LibreTexts Chemistry 2e Ch06.03
status: active
created: 2026-03-11
last_verified: 2026-03-11
---

# Quantum Theory and Wave-Particle Duality

## Problem type
Calculate de Broglie wavelength; apply uncertainty principle; determine quantum numbers.

## Decision tree

1. **What is asked?**
   - de Broglie wavelength → λ = h/(mv)
   - Uncertainty → Δx·Δp ≥ h/(4π)
   - Valid quantum numbers → Check ranges

2. **Particle type?**
   - Electron: m = 9.109 × 10⁻³¹ kg
   - Proton: m = 1.673 × 10⁻²⁷ kg
   - Neutron: m = 1.675 × 10⁻²⁷ kg

3. **Quantum numbers valid?**
   - n: positive integer
   - l: 0 to n-1
   - m_l: -l to +l
   - m_s: ±1/2

## Core formulas

### de Broglie wavelength
```
λ = h / (m × v)
where:
  λ = wavelength (m)
  h = Planck's constant = 6.626 × 10⁻³⁴ J·s
  m = mass (kg)
  v = velocity (m/s)
```

### Heisenberg uncertainty principle
```
Δx × Δp ≥ h / (4π)
where:
  Δx = uncertainty in position (m)
  Δp = uncertainty in momentum (kg·m/s)
```

### Quantum numbers

| Symbol | Name | Range | Description |
|--------|------|-------|-------------|
| n | Principal | 1, 2, 3, ... | Energy level |
| l | Angular momentum | 0 to n-1 | Subshell (s=0, p=1, d=2, f=3) |
| m_l | Magnetic | -l to +l | Orbital orientation |
| m_s | Spin | +½ or -½ | Electron spin |

### Orbital notation

| l value | Orbital | Shape |
|---------|---------|-------|
| 0 | s | Spherical |
| 1 | p | Dumbbell |
| 2 | d | Cloverleaf |
| 3 | f | Complex |

## Constraints
- Pauli exclusion: no two electrons same four quantum numbers
- Max 2 electrons per orbital (opposite spins)

## Common patterns
1. Calculate de Broglie wavelength of particle
2. Check validity of quantum number set
3. Count possible orbitals for given n or l
4. Determine max electrons in subshell

## Links

### L3 Implementation
- `../L3_functions/quantum_theory_tools.py` (TODO)

### L4 Reference
- `../L4_reference/quantum-mechanics-reference.md` (TODO)

### L5 Examples
- `../L5_examples/quantum-mechanics/ (TODO)

## L3 Tool Call Directive

When solving photon energy, wavelength/frequency, and photoelectric effect problems, call the appropriate L3 function:

**photon_energy_from_frequency** (`L3_functions/electromagnetic_energy_tools.py`):
- Use when: Calculate photon energy from frequency (E = hν).
- Parameters: `frequency` (Hz)

**photon_energy_from_wavelength** (`L3_functions/electromagnetic_energy_tools.py`):
- Use when: Calculate photon energy from wavelength (E = hc/λ).
- Parameters: `wavelength` (m)

**wavelength_from_energy** (`L3_functions/electromagnetic_energy_tools.py`):
- Use when: Calculate wavelength from photon energy.
- Parameters: `energy` (J)

**kinetic_energy_ejected_electron** (`L3_functions/electromagnetic_energy_tools.py`):
- Use when: Photoelectric effect — KE = hν − φ.
- Parameters: `photon_energy` (J), `work_function` (J)

**threshold_frequency** / **threshold_wavelength** (`L3_functions/electromagnetic_energy_tools.py`):
- Use when: Find minimum frequency/wavelength for photoelectric effect.
- Parameters: `work_function` (J)

**J_to_eV** / **eV_to_J** (`L3_functions/electromagnetic_energy_tools.py`):
- Use when: Convert between Joules and electron-volts.
- Parameters: `J` or `eV`

**J_to_kJ_per_mol** (`L3_functions/electromagnetic_energy_tools.py`):
- Use when: Convert photon energy to kJ/mol (multiply by Avogadro's number).
- Parameters: `J` (energy per photon)

**de_broglie_wavelength** (`L3_functions/quantum_theory_tools.py`):
- Use when: Calculate de Broglie wavelength (λ = h/mv).
- Parameters: `mass` (kg), `velocity` (m/s)

**Critical notes:**
- Wavelengths in electromagnetic_energy_tools must be in meters — use `nm_to_m(nm)` first if given nm.
- For "how many photons" problems: total energy ÷ energy per photon.

## Source trace
- `../sources/ingestion/source-electronic-structure-stepwise.md` section 6.03

## L3 Tool Call Directives

**Source:** `wavefunction_tools.py`

⚠️ Stub file — no public functions implemented yet.

### Available functions:
- *(none — file is empty)*
