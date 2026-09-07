# Exact finite rectangular-barrier transmission

## Applicability

A particle-transmission calculation specifies a finite rectangular barrier, especially when the barrier is thin, the particle energy is near the barrier height, or the expected transmission is not very small.

## Procedure

1. For a one-dimensional rectangular barrier with equal exterior potentials, 0 < E < V0, m > 0 and a >= 0, convert units consistently, then compute kappa = sqrt(2m(V0-E))/hbar and z = kappa*a.
2. Use the interface-matched result T = [1 + V0^2*sinh^2(z)/(4E(V0-E))]^-1 with consistent SI inputs. Evaluate the expression directly; use an exact-transmission calculator only if the active catalog actually exposes a matching documented function.
3. Use exp(-2z) only as a leading WKB estimate when z is much greater than 1 or an approximation is explicitly requested; the thick-barrier finite-step asymptotic also contains the prefactor 16E(V0-E)/V0^2.
4. Check that 0 <= T <= 1 and that T approaches 1 as the width approaches zero; report the dimensionless probability rather than a percentage unless requested.

## Boundaries

- Do not use a default mass near 1 amu for an electron; bind the actual particle mass.
- Do not treat z near or below unity as a thick-barrier WKB regime.
- Do not apply the below-barrier sinh expression at or above the barrier height; use the appropriate limiting or oscillatory solution.
- Do not clip an invalid asymptotic result to one and present it as an exact transmission coefficient.
- Use only available documented support; otherwise apply the explicit derivation or label missing empirical evidence unresolved. A library filename is not an executable tool.

Only calculators listed in this package's calculator reference are callable here.
Other filenames in a procedure are historical pointers, not installed dependencies.
For missing empirical support, obtain an authoritative source or state the uncertainty.
