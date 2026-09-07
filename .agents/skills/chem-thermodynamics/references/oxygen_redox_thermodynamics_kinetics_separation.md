# Separate electrode equilibrium from kinetic onset and overpotential

## Applicability

An electrode-reaction problem compares equilibrium, onset, applied potential, overpotential, catalyst activity, or reaction rate across surfaces, conditions, or reference scales.

## Procedure

1. Assign each potential a physical role and reference scale before comparing values: equilibrium is thermodynamic, whereas onset, current, exchange current, and polarization are kinetic observables.
2. Under identical reaction conditions and reference scale, derive the equilibrium potential from the redox couple, activities, temperature, and pressure; changing only the catalyst surface changes kinetics, not equilibrium thermodynamics.
3. Compute signed overpotential as η = E_applied or E_onset - E_eq. For a cathodic process, a more-negative onset gives a lower signed η but a larger positive magnitude |η|, so identify which convention the wording uses.
4. For proton-coupled couples, align pH and reference electrodes before comparison: a potential may shift with pH versus a fixed reference while remaining invariant versus RHE.
5. Evaluate every requested descriptor and every clause of a combined choice independently; retain a choice only when its thermodynamic, kinetic, sign-convention, and reference-scale claims all agree.

## Boundaries

- Do not infer equilibrium potential from observed onset potential or catalyst identity.
- Never compare potentials before aligning reference electrodes and thermodynamic conditions.
- For cathodic polarization, do not equate a more-negative signed η with a smaller |η|.
- One true clause cannot rescue another false clause in a combined statement.
- Use only available documented support; otherwise apply the explicit derivation or label missing empirical evidence unresolved. A library filename is not an executable tool.

Only calculators listed in this package's calculator reference are callable here.
Other filenames in a procedure are historical pointers, not installed dependencies.
For missing empirical support, obtain an authoritative source or state the uncertainty.
