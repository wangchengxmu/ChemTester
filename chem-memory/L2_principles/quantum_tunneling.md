---
id: physical.quantum_tunneling
layer: 2
title: Quantum Tunneling and Bound-State Forbidden Regions
---

## Fixed Rectangular Scattering Barrier

Assume a one-dimensional barrier of height `V0 > 0`, width `a >= 0`, equal
zero potential on both sides, particle mass `m > 0`, and incident energy
`0 < E < V0`. Use consistent SI units. Matching the wavefunction and its
derivative at both interfaces gives

```text
kappa = sqrt(2*m*(V0-E))/hbar
z = kappa*a
T = 1 / (1 + V0^2*sinh(z)^2 / (4*E*(V0-E)))
```

For large `z`, the thick-barrier asymptotic includes the interface prefactor:
`T ~ 16*E*(V0-E)/V0^2 * exp(-2*z)`.
The bare `exp(-2*z)` is only a leading exponential estimate, not the exact
finite-step result. Use stable logarithmic evaluation when hyperbolic functions
would overflow. Check `0 <= T <= 1` and `T -> 1` as width tends to zero.

At `E = V0`, take the limit:
`T = 1 / (1 + m*V0*a^2/(2*hbar^2))`.
For `E > V0`, replace the below-barrier factor by
`V0^2*sin(k_inside*a)^2/(4*E*(E-V0))`, where
`k_inside = sqrt(2*m*(E-V0))/hbar`. Above-barrier reflection generally remains;
unit transmission occurs at resonances, not for every energy above the barrier.
Bind the actual particle mass rather than assuming one atomic mass unit.

Use the formula directly, or a matching documented function only when the active
catalog exposes it. A filename in the library does not make a tool executable.

## Bound Harmonic Oscillator

For `V(x) = m*omega^2*x^2/2`, normalized eigenstate `n` has
`E_n = (n+1/2)*hbar*omega` and classical turning points
`x_t = +/-sqrt(2*n+1)*sqrt(hbar/(m*omega))`.
The probability outside these **state-dependent** turning points is not a
scattering transmission coefficient through a fixed barrier.

```text
P_0 = erfc(1) = 0.1572992071
P_1 = erfc(sqrt(3)) + 2*sqrt(3/pi)*exp(-3) = 0.1116102251
```

Thus the first excited state has a smaller forbidden-region probability than
the ground state under this definition. At high quantum number the probability
decreases asymptotically as `n^(-1/3)`; it does not grow toward the classical
limit. Do not transfer an energy trend for a fixed scattering barrier to these
moving turning points.

Source for the oscillator analysis: [Forbidden-region probabilities](https://arxiv.org/abs/1501.07483).
The rectangular-barrier expression follows directly from interface matching
under the assumptions above; WKB has separate smoothness and semiclassical limits.
