# Spectroscopic Selection Rules

[Source: Quantum States of Atoms and Molecules (Zielinksi et al.), Chapter 4.5-4.7]

## Core Concept

Selection rules determine whether a spectroscopic transition between two quantum states is **allowed** (non-zero intensity) or **forbidden** (zero or very weak intensity). They arise from the transition dipole moment integral.

## Key Equations

### Transition Dipole Moment Integral

$$\mu_{if} = \langle \psi_i | \hat{\mu} | \psi_f \rangle = \int \psi_i^* \hat{\mu} \psi_f d\tau$$

where $\hat{\mu} = -e \hat{r}$ for electronic transitions.

### Selection Rule Criteria

- **Allowed**: $\mu_{if} \neq 0$
- **Forbidden**: $\mu_{if} = 0$

### Particle-in-a-Box Selection Rule

$$\Delta n = n_f - n_i = \pm 1$$

**Derivation**:
$$\mu_{if} = -e \int_0^L \psi_n^*(x) x \psi_m(x) dx$$

This integral is non-zero only when $|n_f - n_i| = 1$

### Harmonic Oscillator Selection Rule

$$\Delta v = \pm 1$$

### Rotational Selection Rule

$$\Delta J = \pm 1$$

## Symmetry Analysis

### Using Parity (Inversion Symmetry)

- $\psi_i$, $\psi_f$, and $\mu$ have definite parity (even or odd under inversion)
- Integral is non-zero only when: **odd Ã odd Ã odd = odd** or **even Ã even Ã odd = odd**

General rule: $\int f(x) dx \neq 0$ only if $f(x)$ has even parity.

### Group Theory Selection Rules

For molecules, use character tables:
1. Determine irreducible representations of $\psi_i$, $\psi_f$, and $\mu$
2. Check if $\Gamma_i \otimes \Gamma_\mu \otimes \Gamma_f$ contains $A_1$ (totally symmetric)
3. If yes â?allowed; if no â?forbidden

## Problem Types

1. **Determine if transition is allowed** given initial and final quantum numbers
2. **Find allowed transitions** from a set of levels
3. **Use symmetry to identify zero integrals**
4. **Apply selection rules to predict spectra**

## Physical Interpretation

- Selection rules arise from **conservation laws** (angular momentum, parity)
- "Forbidden" transitions can still occur weakly through:
  - Vibronic coupling
  - Spin-orbit coupling
  - Symmetry breaking

## Related Topics

- â?`cyanine_dye_spectroscopy.md` for application
- â?`symmetry_group_theory.md` for group theory methods
- â?`electronic_spectroscopy.md` for more examples


## Implementations

- Implementation: `../L3_functions/spectroscopic_selection_rules.py`
