---
id: rotational.spectroscopy
layer: 2
title: Rotational Spectroscopy (Microwave Spectroscopy)
stability: high
confidence: high
constraints:
  - Requires permanent dipole moment for pure rotational spectra
  - Gas phase only (intermolecular interactions hinder rotation in condensed phases)
last_verified: 2026-03-17
change_type: new
source: LibreTexts Physical Chemistry - Rotational Spectroscopy Module
---

# Rotational Spectroscopy

Rotational spectroscopy measures transitions between quantized rotational energy levels of molecules in the gas phase. The spectra of polar molecules can be measured in absorption or emission by microwave spectroscopy (1-10 cmâ»Â? or far infrared spectroscopy.

## Selection Rules

### Rotational Transitions
- **ÎJ = Â±1** - photon carries one unit of angular momentum
- Molecule must have a **permanent dipole moment** that changes upon rotation
- Nonpolar molecules (Hâ? Nâ? Oâ? spherical tops) have no pure rotational spectra
- Transition dipole moment integral must be nonzero:
  $$\text{Probability} = \int \psi_{rot}^*(F) \hat{\mu} \psi_{rot}(I) d\tau$$

### Rovibrational Transitions
- **Îv = Â±1** (typically Îv = +1 at room temperature)
- **ÎJ = Â±1** gives P-branch (ÎJ = -1) and R-branch (ÎJ = +1)
- **ÎJ = 0** (Q-branch) forbidden for most diatomics, allowed for polyatomics and molecules with electronic angular momentum

## Rotational Energy Levels

### Rigid Rotor Model

The energy levels for a rotating rigid body:
$$E_J = J(J+1) \frac{\hbar^2}{2I} = BJ(J+1)h$$

where:
- **J** = rotational quantum number (J = 0, 1, 2, ...)
- **I** = moment of inertia
- **B** = rotational constant

### Rotational Constant

$$B = \frac{h}{8\pi^2 c I} \quad \text{(in cm}^{-1}\text{)}$$

or in frequency units:
$$B = \frac{h}{8\pi^2 I} \quad \text{(in Hz)}$$

### Moment of Inertia

For a diatomic molecule:
$$I = \mu r_e^2$$

where:
- **Î¼** = reduced mass = mâmâ?(mâ?mâ?
- **r_e** = equilibrium bond length

For linear polyatomic molecules:
$$I = \sum_{j=1}^{n} m_j r_{ej}^2$$

## Nonrigid Rotor (Centrifugal Distortion)

Real bonds stretch during rotation. The centrifugal distortion correction:
$$E_J = BJ(J+1) - DJ^2(J+1)^2$$

where **D** is the centrifugal distortion constant:
$$D = \frac{4B^3}{\omega^2}$$

The energy spacing between transitions:
$$E_R = (2B_e - 4D_e) + (2B_e - 12D_e)J'' - 4D_e(J'')^3$$

## Molecule Classification by Rotational Symmetry

### Diatomic Molecules
- Modeled as rigid rotor (or nonrigid rotor with centrifugal distortion)
- Single rotational constant B
- Selection rule: ÎJ = Â±1
- Spectral spacing: 2B

### Linear Molecules
- Behave same as diatomic for rotations
- Only **2 rotational degrees of freedom** (rotation around bond axis requires huge energy, I â?10Â¹â?smaller)
- Vibrational degrees: 3N - 5

### Spherical Tops
- All three principal moments of inertia equal (I_A = I_B = I_C)
- Highly symmetrical, **no permanent dipole moment**
- **No microwave rotational spectrum**
- Examples: CHâ? SFâ? CClâ?
### Symmetric Tops

Two rotational axes with equal inertia, one unique axis with different inertia.

**Oblate** (I_A > I_B = I_C, like a frisbee):
- Examples: benzene, XeFâ?- Energy levels: $E_{rot} = BJ(J+1) + (A-B)K^2$

**Prolate** (I_A < I_B = I_C, like a football):
- Examples: NHâ? CHâCl
- Energy levels: $E_{rot} = BJ(J+1) + (C-B)K^2$

where:
- **K** = additional quantum number (|K| â?J)
- **A, B, C** = rotational constants (A â?B â?C)

### Asymmetric Tops
- All three moments of inertia different (I_A â?I_B â?I_C)
- Most complex rotational spectra
- Examples: HâO, SOâ? formaldehyde

## Rovibrational Spectroscopy

### Combined Rotation-Vibration Energy
$$S(v,J) = \omega_0(v + \frac{1}{2}) + BJ(J+1)$$

### P-Branch (ÎJ = -1)
$$\Delta\tilde{\nu} = \tilde{\omega} - 2\tilde{B}J \quad (J'' = 1, 2, 3, ...)$$
Lower energy than pure vibrational transition.

### R-Branch (ÎJ = +1)
$$\Delta\tilde{\nu} = \tilde{\omega} + 2\tilde{B}(J+1) \quad (J'' = 0, 1, 2, ...)$$
Higher energy than pure vibrational transition.

### Q-Branch (ÎJ = 0)
$$\Delta\tilde{\nu} = \tilde{\omega}$$
Forbidden for most diatomics; observable in polyatomic molecules and molecules with electronic angular momentum (e.g., NO).

### Zero Gap
Gap between P(1) and R(0), where Q-branch would appear if allowed. Spacing â?4B.

## Rotation-Vibration Coupling

The rotational constant depends on vibrational level:
$$B_v = B_e - \alpha_e(v + \frac{1}{2})$$

where Î±_e is the rotation-vibration coupling constant.

Effects:
- R-branch lines converge (move closer together) at higher energy
- P-branch lines diverge (move farther apart) at lower energy

### Combination Differences Method
To determine Bâ and Bâ?
- **Bâ?from common lower state**: ÎÎ½_R(J-1) - ÎÎ½_P(J+1) = 4Bâ?J + Â½)
- **Bâ from common upper state**: ÎÎ½_R(J-1) - ÎÎ½_P(J+1) = 4Bâ(J + Â½)

Then: Î±_e = Bâ - Bâ?
## Population Distribution

### Boltzmann Distribution
$$\frac{n_J}{n_0} = (2J+1) e^{-E_{rot}(J)/kT}$$

where (2J+1) is the degeneracy from M_J values (+J to -J).

### Most Populated Level
$$J_{max} = \sqrt{\frac{kT}{2hcB}} - \frac{1}{2}$$

Population shifts to higher J for:
- Heavier molecules (smaller B)
- Higher temperatures

## Applications

### Bond Length Determination
From measured rotational constant:
$$r_e = \sqrt{\frac{h}{8\pi^2 c \tilde{B} \mu}}$$

### Spectral Characteristics
- Pure rotational spectra: equally spaced lines at 2B intervals
- Rovibrational spectra: P-branch and R-branch separated by zero gap
- Bond length from rotational constant
- Centrifugal distortion from line spacing variation

## Key Equations Summary

| Quantity | Equation | Notes |
|----------|----------|-------|
| Rotational energy | $E_J = BJ(J+1)h$ | Rigid rotor |
| Rotational constant | $B = h/(8\pi^2 cI)$ | In cmâ»Â?|
| Reduced mass | $\mu = m_1 m_2/(m_1 + m_2)$ | Diatomic |
| Moment of inertia | $I = \mu r_e^2$ | Diatomic |
| Centrifugal distortion | $E_J = BJ(J+1) - DJ^2(J+1)^2$ | Nonrigid rotor |
| Distortion constant | $D = 4B^3/\omega^2$ | From vibrational frequency |
| Transition energy | $\Delta E = 2B(J+1)$ | ÎJ = +1 |
| Boltzmann population | $n_J/n_0 = (2J+1)e^{-E_J/kT}$ | Temperature dependent |
| Most populated J | $J_{max} = \sqrt{kT/(2hcB)} - 1/2$ | Peak intensity |

## Related Concepts
- [[vibrational_spectroscopy]] - Vibrational transitions (100-3000 cmâ»Â?
- [[spectroscopic_selection_rules]] - General selection rules
- [[quantum_mechanics_core]] - SchrÃ¶dinger equation, spherical harmonics
- [[statistical_mechanics]] - Boltzmann distribution

## References
- LibreTexts Physical Chemistry: Rotational Spectroscopy Module
- Hollas, M. J. Modern Spectroscopy (3rd ed.), 1996
- Herzberg, G. Molecular Spectra and Molecular Structure (2nd ed.), 1950


## Implementations

- Implementation: `../L3_functions/rotational_spectroscopy_tools.py`

## L3 Tool Call Directives

**Source:** `rotational_spectroscopy_tools.py`

Microwave/rotational spectroscopy: moments of inertia, rotational constants, energy levels, transitions, Boltzmann populations.

### Available functions:
- `moment_of_inertia_diatomic(m1, m2, r)` → float — I = μr² (m1,m2 in amu, r in meters)
- `rotational_constant(I)` → float — B = h/(8π²cI) in cm⁻¹
- `rotational_energy(J, B, D=0)` → float — E_J = BJ(J+1) - DJ²(J+1)² in cm⁻¹
- `transition_frequency(J_lower, B, D=0)` → float — ν = 2B(J+1) for ΔJ=+1 in cm⁻¹
- `bond_length_from_B(B, m1, m2)` → float — Bond length (m) from rotational constant
- `boltzmann_population(J, B, T)` → float — Relative population n_J/n₀
- `j_max(B, T)` → int — Most populated J level
- `wavenumber_from_wavelength(wavelength_nm)` → float — nm → cm⁻¹
- `wavelength_from_wavenumber(wavenumber)` → float — cm⁻¹ → nm

### Common errors:
- ❌ Using Å for bond length instead of meters (multiply by 1e-10)
- ❌ Forgetting homonuclear diatomics (N₂, O₂) have no microwave spectrum
