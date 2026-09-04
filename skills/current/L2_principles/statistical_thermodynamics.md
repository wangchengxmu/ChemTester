---
id: statistical-thermodynamics
layer: L2
topic: thermodynamics
source: DeVoe Ch15
depends: [entropy, quantum_theory, thermodynamics_laws]
tags: [thermodynamics, statistical-mechanics, partition-function, boltzmann, ensemble]
---

# Statistical Thermodynamics

## Concept Overview
Statistical thermodynamics connects microscopic molecular properties to macroscopic thermodynamic quantities through the partition function. The Boltzmann distribution governs the population of energy levels at thermal equilibrium.

## Key Principles

### Boltzmann Distribution
Probability of a system being in microstate i with energy εᵢ:
```
P_i = exp(−εᵢ/kT) / Q
```

### Molecular Partition Function (q)
For a single molecule:
```
q = Σᵢ gᵢ exp(−εᵢ/kT)
```

For an ideal gas, q factors into contributions:
```
q = q_trans · q_rot · q_vib · q_el
```

### Translational Partition Function
```
q_trans = (2πmkT/h²)^(3/2) · V
```

### Rotational Partition Function (linear molecule)
```
q_rot = T/(σθ_rot)  where θ_rot = ℏ²/(2Ik)
```
σ = symmetry number (σ = 1 for heteronuclear, 2 for homonuclear diatomic)

### Vibrational Partition Function (harmonic oscillator)
```
q_vib = exp(−θ_vib/2T) / [1 − exp(−θ_vib/T)]
```
where θ_vib = hν/k (vibrational temperature)

### Electronic Partition Function
```
q_el = g₀ + g₁ exp(−ε₁/kT) + ...
```
Usually g₀ >> others at ordinary temperatures.

### Thermodynamic Functions from q
For an ideal gas of N indistinguishable molecules:
```
U = NkT² (∂ln q/∂T)_V
C_V = Nk [∂/∂T(T² ∂ln q/∂T)]_V
S = Nk [ln(q/N) + 1 + T(∂ln q/∂T)_V]
A = −NkT [ln(q/N) + 1]
G = −NkT ln(q/N)
μ = −kT ln(q/N)
```

### Canonical Ensemble (NVT)
System with fixed N, V, T:
```
Q = Σᵢ exp(−E_i/kT)  (system partition function)
A = −kT ln Q
```

### Equipartition Theorem
Each quadratic degree of freedom contributes ½kT to <E>:
- Monatomic gas: 3 translational → U = 3/2 NkT, C_V = 3/2 R
- Diatomic (rigid rotor): +2 rotational → U = 5/2 NkT, C_V = 5/2 R
- Diatomic (with vibration): +2 vibrational → U = 7/2 NkT, C_V = 7/2 R

### Residual Entropy
```
S_residual = k ln W₀
```
where W₀ is the number of configurations at T→0 (for imperfect crystals).

## L3 Tools
- `L3_functions/statistical_thermo_tools.py` — partition function calculations, thermodynamic properties from spectroscopic data
- See existing `statistical_mechanics` L2

## L4 Data
- Spectroscopic constants (rotational, vibrational) in `L4_data/spectroscopic_data/`

## Source
DeVoe, *Thermodynamics and Chemistry*, Ch15 (Statistical Thermodynamics).

## L3 Tool Call Directives

**Source:** `statistical_thermo_tools.py`
Statistical thermodynamics: partition functions, thermodynamic quantities from Q.

### Available functions:
- `q_translational(T, M_kg, V)` → float — Translational partition function
- `q_rotational(T, B_cm, sigma)` → float — Rotational partition function
- `q_vibrational(T, nu_cm)` → float — Vibrational partition function
- `thermo_from_q(T, q, N)` → dict — Calculate A, S, U, H, G, CV from partition function
- `residual_entropy(W0)` → float — Residual entropy S₀ = k·ln(W₀)
- `boltzmann_population(energies, T, degeneracies)` → list — Boltzmann population of energy levels

### Common errors:
- ❌ Forgetting symmetry number σ in rotational partition function (σ=2 for homonuclear diatomics)
- ❌ Using atomic mass in amu instead of kg for translational partition function
