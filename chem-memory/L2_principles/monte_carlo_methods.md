# Monte Carlo Methods in Molecular Modeling

## Concept Overview
Monte Carlo (MC) methods use random sampling to compute thermodynamic and structural properties of molecular systems. Based on statistical mechanics ensemble averages.

## Metropolis Monte Carlo

### Algorithm
1. Start from initial configuration.
2. Propose random move (translation, rotation, conformational change).
3. Compute energy change ΔE.
4. Accept with probability: P = min(1, exp(−ΔE/k_BT)) (Boltzmann criterion).
5. Repeat for N steps; sample properties from accepted configurations.

### Ensemble Types
| Ensemble | Fixed Variables | Move Types |
|---|---|---|
| NVT (canonical) | N, V, T | Atom displacements |
| NPT (isothermal-isobaric) | N, P, T | Volume changes + displacements |
| μVT (grand canonical) | μ, V, T | Particle insertion/deletion |
| GCMC | μ, V, T | Gas adsorption modeling |

### Key Equations
- Average of observable A: ⟨A⟩ = (1/N) Σ A(rᵢ) (at equilibrium).
- Free energy: ΔF = −k_BT ln(P_accept) via Metropolis criterion.
- Radial distribution function: g(r) from histogram of interparticle distances.

## Applications
- **Gas adsorption**: GCMC simulation of H₂, CH₄, CO₂ in MOFs/zeolites.
- **Ligand docking**: Random sampling of ligand conformations in protein binding sites.
- **Polymer simulations**: Sampling chain conformations in melts/solutions.
- **Phase equilibria**: Gibbs ensemble MC for coexistence curves.

## MC vs Molecular Dynamics
| Feature | Monte Carlo | Molecular Dynamics |
|---|---|---|
| Trajectory | No (random moves) | Yes (Newton's equations) |
| Time evolution | No | Yes |
| Rare events | Better at crossing barriers | May get trapped |
| Transport properties | Difficult to calculate | Directly from trajectory |
| Ensemble flexibility | Easy (any ensemble) | More complex |

## Sources
[Source: Wikipedia, Monte Carlo molecular modeling]
[Source: Frenkel & Smit, Understanding Molecular Simulation]

## L3 Tools
-> `../L3_functions/mc_tools.py` — `metropolis_mc()`, `gcmc_adsorption()`

## L3 Tool Call Directives

**Source:** `mc_tools.py`
Monte Carlo methods: Metropolis criterion, Boltzmann weights, partition functions.

### Available functions:
- `metropolis_accept(dE, T)` → bool — Metropolis acceptance criterion (dE in J/mol, T in K)
- `boltzmann_weight(E, T)` → float — Calculate Boltzmann weight exp(-E/RT)
- `canonical_partition(energies, T)` → float — Canonical partition function Q = Σexp(-Eᵢ/RT)
- `estimate_free_energy(energies, T)` → float — Simplified free energy estimate from sampled energies

### Common errors:
- ❌ Using k_B instead of R for molar energies (R = 8.314 J/(mol·K) used here)
- ❌ Not recognizing that metropolis_accept is stochastic (same inputs can give different results)
