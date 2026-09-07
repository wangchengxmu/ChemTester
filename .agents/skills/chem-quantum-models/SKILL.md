---
name: chem-quantum-models
description: "Use for atomic-spectroscopy model limits, vibrational partition approximations, or finite-barrier transmission. Not for routine NMR peak assignment or unrestricted numerical modeling."
---

# Quantum Models

## Workflow

1. State the Hamiltonian or statistical model, assumptions, energy origin, boundary conditions, and dimensional convention.
2. Choose the expression appropriate to the energy regime; evaluate continuous limiting cases separately when a direct formula becomes singular.
3. Check dimensions, normalization, probability bounds, approximation error, and whether the model can represent the observed phenomenon.

## Load Only Relevant Procedures

Open the matching reference below only when its applicability fits the task.
Use another skill for a separate subproblem; do not load this entire library by default.

- [Atomic spectroscopy model-limit discrimination](references/atomic_spectroscopy_model_limit_discrimination.md): A conceptual atomic-spectroscopy question asks which missing feature of a model explains an observed spectral limitation, especially in multiple-choice form.
- [Vibrational partition-function convention and approximation thresholds](references/vibrational_partition_approximation_thresholds.md): Comparing exact and high-temperature harmonic-oscillator vibrational partition functions or finding a temperature at which their percentage difference reaches a tolerance.
- [Exact finite rectangular-barrier transmission](references/finite_rectangular_barrier_transmission.md): A particle-transmission calculation specifies a finite rectangular barrier, especially when the barrier is thin, the particle energy is near the barrier height, or the expected transmission is not very small.

## Evidence And Output

- Start from the user's actual structures, conditions, and requested quantity. If evidence is missing, ask for it or state a bounded assumption.
- Treat these procedures as conditional reasoning aids, not authority over the current evidence. Preserve equations, units, scope, and uncertainty.
- A successful calculator call is not independent scientific validation. Verify consequential empirical constants, safety claims, and exceptional chemistry against authoritative sources.
- Do not read benchmark answers, previous predictions, or evaluation logs to answer a question. Keep the model answer separate from a benchmark key and scientific adjudication.
- Missing optional references are a support limitation, not evidence that a reasoned answer is wrong. Do not invent the missing source.
