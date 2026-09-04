---
id: chem.quantum_tunneling
layer: 2
title: Quantum Mechanical Tunneling
source: Quantum States of Atoms and Molecules (Zielinski et al.), Ch6.5
status: active
created: 2026-03-21
last_verified: 2026-03-21
---

# Quantum Mechanical Tunneling

## Core Concept

Quantum tunneling is the phenomenon where a particle passes through a potential energy barrier that it classically could not surmount. This occurs because the wavefunction extends into and through regions where the potential energy exceeds the total energy, giving a non-zero probability of finding the particle on the other side.

## Key Equations

### Transmission Coefficient (Rectangular Barrier)

For a rectangular barrier of height Vâ and width a, with particle energy E < Vâ:

$$T \approx \frac{16E(V_0 - E)}{V_0^2} e^{-2\kappa a}$$

where:
- $\kappa = \frac{\sqrt{2m(V_0 - E)}}{\hbar}$ is the decay constant inside the barrier

### WKB Approximation (General Barrier)

$$T \approx \exp\left(-\frac{2}{\hbar}\int_{x_1}^{x_2}\sqrt{2m[V(x) - E]}\,dx\right)$$

where xâ?and xâ?are the classical turning points.

### Tunneling Probability Dependence

- **Barrier height** (Vâ - E): Exponential decrease with increasing barrier height
- **Barrier width** (a): Exponential decrease with increasing width
- **Particle mass** (m): Heavier particles tunnel less (exponential in âm)
- **Energy** (E): Approaching barrier height increases transmission

## Chemical Applications

1. **Chemical kinetics**: Proton and electron transfer reactions proceed via tunneling, especially at low temperatures where classical over-barrier pathways are frozen out
2. **Isotope effects**: Deuterium/proton kinetic isotope effects are amplified by tunneling (KIE > classical prediction)
3. **Enzyme catalysis**: Hydrogen tunneling in enzyme active sites contributes to catalytic rate enhancement
4. **Scanning Tunneling Microscopy (STM)**: Tunneling current between tip and surface provides atomic-resolution imaging
5. **Ammonia inversion**: The umbrella inversion of NHâ?occurs via tunneling through the inversion barrier
6. **Alpha decay**: Nuclear Î±-decay is explained by tunneling through the Coulomb barrier

## Connection to Harmonic Oscillator

In the quantum harmonic oscillator, the wavefunction extends beyond the classical turning points into the classically forbidden region (where V(x) > E). The probability of finding the particle in this region:

$$P_{\text{classically forbidden}} = \int_{\text{outside turning points}} |\psi_v(x)|^2 dx$$

This probability increases with quantum number v, explaining why tunneling is more significant for excited states.

## Problem Types

1. **Calculate transmission coefficient** for a rectangular barrier
2. **Estimate tunneling probability** using WKB approximation
3. **Explain isotope effects** on reaction rates
4. **Analyze barrier penetration** in harmonic oscillator wavefunctions
5. **Estimate tunneling contribution** to rate constants

## Constraints

- Classical limit: For macroscopic masses and/or wide/high barriers, T â?0
- WKB approximation is valid when the potential changes slowly compared to the de Broglie wavelength
- For thin barriers or energies near Vâ, full quantum mechanical solution is needed

## Related Topics

- â?`quantum_mechanics.md` for wavefunctions and the SchrÃ¶dinger equation
- â?`quantum_approximations.md` for WKB and perturbation methods
- â?`microscopy.md` for STM applications
- â?`enzyme_mechanisms.md` for biological tunneling

## Downstream Layers (Pass-3 complete)

- â?L3: `../L3_functions/quantum_tunneling_tools.py` â?Transmission coefficient, WKB computation, tunneling corrections
- â?L4: `../L4_reference/quantum_tunneling_data.md` â?Barrier parameters, experimental KIE data, lookup tables
- â?L5: `../L5_examples/quantum_tunneling_examples.md â?Worked examples: rectangular barrier, NHâ?inversion, alpha decay


## Implementations

- Implementation: `../L3_functions/tunneling_calculator.py`

## L3 Tool Call Directives

**Source:** `quantum_tunneling_tools.py`
Barrier transmission (rectangular, triangular, WKB), Bell tunneling correction, Gamow factor.

### Available functions:
- `rectangular_barrier_T(energy_eV, barrier_height_eV, width_angstrom, mass_amu=1.0)` → float — T for rectangular barrier (κa >> 1 limit)
- `triangular_barrier_T(energy_eV, barrier_height_eV, width_angstrom, mass_amu=1.0)` → float — WKB triangular barrier
- `wkb_transmission(energy_eV, V_func, x1, x2, mass_amu, n_points=1000)` → float — General WKB via numerical integration
- `bell_tunneling_correction(temperature_K, imaginary_frequency_cm1=None, barrier_width_angstrom=None, ...)` → float — Q_tun (Wigner or Bell parabolic)
- `gamow_factor(energy_MeV, Z_daughter, Z_alpha=2)` → float — Gamow factor G for α-decay

### Common errors:
- ❌ Energy ≥ barrier height returns T=1 (classical regime) — tool doesn't handle resonance
- ❌ WKB invalid for thin barriers (κa ~ 1) — only valid for thick/low-transmission
- ❌ Bell correction: must provide either imaginary_frequency_cm1 (Wigner) or width+mass+height (parabolic)
- ❌ Gamow factor energy must be in MeV, not eV
