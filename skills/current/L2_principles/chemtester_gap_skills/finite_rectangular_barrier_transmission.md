# Exact finite rectangular-barrier transmission

**Retrieve with:** finite rectangular barrier transmission, exact tunneling coefficient, thin barrier WKB validity, electron barrier matching

**Use when:** A particle-transmission calculation specifies a finite rectangular barrier, especially when the barrier is thin, the particle energy is near the barrier height, or the expected transmission is not very small.

## Procedure

1. For E < V0, convert mass, energy, and width consistently, then compute kappa = sqrt(2m(V0-E))/hbar and z = kappa*a.
2. Use the interface-matched result T = [1 + V0^2*sinh^2(z)/(4E(V0-E))]^-1. For repeatable numerics, search for and call tunneling_calculator.transmission_rectangular_exact with SI inputs.
3. Use exp(-2z) only as a leading WKB estimate when z is much greater than 1 or an approximation is explicitly requested; the thick-barrier finite-step asymptotic also contains the prefactor 16E(V0-E)/V0^2.
4. Check that 0 <= T <= 1 and that T approaches 1 as the width approaches zero; report the dimensionless probability rather than a percentage unless requested.

## Preferred Support

- chem-memory/L2_principles/quantum_tunneling.md
- chem-memory/L3_functions/tunneling_calculator.py

## Guards

- Do not use a default mass near 1 amu for an electron; bind the actual particle mass.
- Do not treat z near or below unity as a thick-barrier WKB regime.
- Do not apply the below-barrier sinh expression at or above the barrier height; use the appropriate limiting or oscillatory solution.
- Do not clip an invalid asymptotic result to one and present it as an exact transmission coefficient.
