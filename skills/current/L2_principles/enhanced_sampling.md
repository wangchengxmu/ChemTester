# Enhanced Sampling Methods

## Concept Overview
Enhanced sampling methods overcome energy barriers in molecular dynamics simulations that trap the system in local free energy minima, enabling exploration of rare events and calculation of free energy surfaces.

## Why Standard MD Is Insufficient
- Timescale gap: MD typically reaches Î¼s; many biophysical processes occur on msâ€“s timescales.
- Energy barriers: Boltzmann probability at 300K for 20 kcal/mol barrier â‰ˆ exp(âˆ’33) â‰ˆ 10â»Â¹â´ â†’ inaccessible.

## Umbrella Sampling
- Apply harmonic bias potential along reaction coordinate Î¾: V_bias = Â½k(Î¾ âˆ’ Î¾â‚€)Â².
- Run simulations at multiple Î¾â‚€ values (windows).
- Combine with WHAM (Weighted Histogram Analysis Method) to reconstruct PMF.
- Free energy: F(Î¾) = âˆ’k_BT ln[P(Î¾)] + const.

## Metadynamics

### [Source: Wikipedia, Metadynamics]
- **Well-Tempered Metadynamics** (Barducci, Bussi, Parrinello, 2008):
  - Add Gaussian hills along collective variables (CVs) s to fill free energy minima.
  - Hill height decreases over time: w(t) = wâ‚€Â·exp(âˆ’V(s,t)/(Î”k_BT)).
  - Converges to: V(s,tâ†’âˆž) = âˆ’(Î”/(Î”+1))Â·F(s).
  - Convergence factor Î” controls accuracy vs. speed.

### Key Collective Variables (CVs)
| CV Type | Example | Use Case |
|---|---|---|
| Distance | d(NZ-CZ) | Bond formation/breaking |
| Angle | Ï†, Ïˆ dihedrals | Protein folding |
| Coordination number | n_O_Cu | Ion binding |
| Radius of gyration | R_g | Polymer collapse |
| RMSD | RMSD to reference | Folding pathways |

### Practical Considerations
- Too few CVs â†’ hysteresis; too many â†’ slow convergence.
- PLUMED (open-source) for metadynamics with GROMACS, LAMMPS, CP2K.

## Other Enhanced Sampling Methods
| Method | Principle | Best For |
|---|---|---|
| Replica Exchange MD (REMD) | Exchange between T replicas | Folding, phase transitions |
| Accelerated MD (aMD) | Boost potential energy | General exploration |
| Adaptive Biasing Force (ABF) | Flatten free energy gradient | 1D PMF |
| Forward Flux Sampling | Trajectory splitting | Rare event kinetics |

## Sources
[Source: Wikipedia, Metadynamics]
[Source: Laio & Parrinello, PNAS 2002]

## L3 Tools
-> `../L3_functions/sampling_tools.py` â€” `umbrella_sampling()`, `metadynamics_setup()`

## L3 Tool Call Directives

**Source:** sampling_tools.py
Replica exchange, umbrella sampling, WHAM helper functions.

### Available functions:
- eplica_exchange_prob(dE: float, T1: float, T2: float) ¡ú float ¡ª Acceptance probability; dE ¡Ü 0 ¡ú 1.0
- umbrella_bias(xi: float, xi0: float, k: float) ¡ú float ¡ª Bias potential V = 0.5¡¤k¡¤(xi - xi?)2
- wham_weights(trajs, kBT: float) ¡ú list ¡ª Placeholder returning uniform weights

### Common errors:
- ? Using dE in kJ/mol with T in K (internal uses R=8.314 J/(mol¡¤K), ensure dE in J/mol)
