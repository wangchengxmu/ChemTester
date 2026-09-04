# Cyanine Dye Spectroscopy

[Source: Quantum States of Atoms and Molecules (Zielinksi et al.), Chapter 4]

## Core Concept

Cyanine dyes are conjugated organic cations whose electronic spectra can be modeled using the **particle-in-a-box** approximation. This provides a rare example where a simple quantum mechanical model yields quantitatively accurate predictions for real molecular systems.

## Key Equations

### Energy Levels (Particle-in-a-Box)

$$E_n = \frac{n^2 h^2}{8mL^2}$$

where:
- $n$ = quantum number (1, 2, 3, ...)
- $h$ = Planck constant
- $m$ = electron mass
- $L$ = length of the conjugated chain

### Absorption Wavelength

$$\lambda = \frac{8mcL^2}{h(n_f^2 - n_i^2)}$$

For HOMOÃ¢Â†Â’LUMO transition: $n_i = N/2$, $n_f = N/2 + 1$

$$\lambda = \frac{8mcL^2}{h(2N + 1)}$$

where $N$ = number of ÃÂ€ electrons

### Box Length Estimation

For cyanine dyes: $L \approx (p + 3) \times 139$ pm

where $p$ = number of carbon atoms in the polymethine chain

## Selection Rules

### Allowed Transitions

$$\Delta n = \pm 1$$

Transitions are allowed when:
- The transition dipole moment integral is non-zero
- $\int_0^L \psi_i x \psi_f dx \neq 0$

### Transition Dipole Moment

$$\mu_{if} = -e \int_0^L \psi_i x \psi_f dx$$

For particle-in-a-box:
$$\mu_{if} = \frac{eL}{\pi^2} \left[\frac{\sin(n_f - n_i)\pi}{(n_f - n_i)^2} - \frac{\sin(n_f + n_i)\pi}{(n_f + n_i)^2}\right]$$

When $\Delta n = \pm 1$: $\mu_{if} = \frac{2eL}{\pi^2 n_f n_i}$

## Problem Types

1. **Calculate absorption wavelength** from chain length
2. **Estimate box length** from experimental ÃÂ»_max
3. **Determine number of ÃÂ€ electrons** from spectral data
4. **Verify selection rules** for given transitions
5. **Calculate transition dipole moment** magnitude

## Constraints

- Model assumes: infinite potential barriers, no electron-electron repulsion
- Box length is longer than geometric chain length (electron delocalization)
- Works best for symmetric cyanine dyes with extended conjugation

## Related Topics

- Ã¢Â†?`quantum_mechanics_core.md` for SchrÃƒÂ¶dinger equation derivation
- Ã¢Â†?`uv_vis_spectroscopy.md` for Beer-Lambert law
- Ã¢Â†?`molecular_orbital_theory.md` for more advanced treatment


## Implementations

- Implementation: `../L3_functions/cyanine_dye_spectroscopy.py`

---

## L3 Tool Call Directives

**Source:** cyanine_dye_spectroscopy.py
Particle-in-a-box model for cyanine dye electronic spectra and transitions.

### Available functions:
- energy_level(n, L, m) ¡ú float ¡ª PIB energy E_n = n2h2/(8mL2) in Joules
- bsorption_wavelength(L, n_initial, n_final) ¡ú float ¡ª Transition wavelength (m)
- cyanine_wavelength_from_chain(p, N) ¡ú float ¡ª Absorption ¦Ë (nm) for cyanine dye with p C=C units
- ox_length_from_wavelength(wavelength_nm, N) ¡ú float ¡ª Box length L (pm) from observed ¦Ë
- 	ransition_dipole_moment(L, n_i, n_f) ¡ú float ¡ª ¦Ì_if for PIB transition (C¡¤m)
- is_transition_allowed(n_i, n_f) ¡ú bool ¡ª Selection rule: ¦¤n = ¡À1
- oscillator_strength(L, n_i, n_f, wavelength_nm) ¡ú float ¡ª Oscillator strength f (dimensionless)

### Common errors:
- ? Forgetting L must be in meters (not pm or ?) for energy_level/absorption_wavelength
- ? Assuming all transitions are allowed ¡ª check ¦¤n = odd (¡À1, ¡À3, ...)
