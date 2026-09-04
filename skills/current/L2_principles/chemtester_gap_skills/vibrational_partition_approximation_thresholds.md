# Vibrational partition-function convention and approximation thresholds

**Retrieve with:** vibrational partition zero point convention, harmonic oscillator high temperature error, partition function approximation threshold, exact reference relative error

**Use when:** Comparing exact and high-temperature harmonic-oscillator vibrational partition functions or finding a temperature at which their percentage difference reaches a tolerance.

## Procedure

1. Set the characteristic temperature theta = hc times wavenumber divided by k and define x = theta/T.
2. Match the energy-zero convention to the stated approximation: with the vibrational ground level as zero, use q_exact = 1/(1-exp(-x)) and q_HT = 1/x; include the exp(-x/2) factor only when zero-point energy is explicitly retained.
3. Write the fractional-error denominator explicitly. Unless another reference is specified, test the approximation against the exact value using abs(q_HT-q_exact)/q_exact.
4. Solve the dimensionless boundary error(x)=p for positive x, compute T_threshold=theta/x, and verify that increasing temperature decreases the error.
5. Use the small-x checks error approximately x/2 for the excitation-zero convention and approximately x^2/24 for the zero-point-energy-including convention to detect a convention mismatch.

## Preferred Support

- chem-memory/L2_principles/statistical_mechanics.md
- chem-memory/L3_functions/statistical_mechanics_tools.py

## Guards

- Do not mix partition functions with different energy-zero conventions.
- Do not leave the percentage-error denominator implicit.
- Distinguish the minimum threshold temperature from an arbitrary temperature satisfying the tolerance.
- Treat a numerical root as valid only after checking the high-temperature limit and monotonic direction.
