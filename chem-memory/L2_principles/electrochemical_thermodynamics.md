---
id: electrochemical-thermodynamics
layer: L2
topic: thermodynamics
source: DeVoe Ch12
depends: [reaction_equilibrium_thermo, nernst_equation, galvanic_cells]
tags: [thermodynamics, electrochemistry, nernst, cell-potential, faraday]
---

# Electrochemical Cells and Thermodynamics

## Concept Overview
Electrochemical cells convert chemical energy to electrical energy (galvanic) or vice versa (electrolytic). The cell potential is directly related to the Gibbs energy change of the cell reaction.

## Key Principles

### Cell Potential and Gibbs Energy
```
Δ_rG = −nFE_cell
Δ_rG° = −nFE°_cell
```
- n = number of moles of electrons transferred
- F = 96485 C/mol (Faraday constant)
- E_cell > 0 → spontaneous (galvanic cell)

### Nernst Equation
```
E_cell = E°_cell − (RT/nF) ln Q
     = E°_cell − (0.05916 V/n) log₁₀ Q  (at 25°C)
```

### Standard Cell Potential
```
E°_cell = E°_cathode − E°_anode = E°_reduction(cathode) − E°_reduction(anode)
```

### Temperature Dependence
```
Δ_rS = nF(∂E_cell/∂T)_p
Δ_rH = −nFE_cell + nFT(∂E_cell/∂T)_p
```

### Types of Electrodes
| Type | Example | Half-reaction |
|------|---------|-------------|
| Metal/metal ion | Zn²⁺/Zn | Zn²⁺ + 2e⁻ → Zn |
| Gas electrode | H⁺/H₂/Pt | 2H⁺ + 2e⁻ → H₂ |
| Metal insoluble salt | AgCl/Ag/Cl⁻ | AgCl + e⁻ → Ag + Cl⁻ |
| Redox electrode | Fe³⁺/Fe²⁺/Pt | Fe³⁺ + e⁻ → Fe²⁺ |

### Electrolytic Cells
```
E_applied > |E_cell| + IR + η
```
where η is overpotential, IR is ohmic loss.

### Faraday's Laws
- Mass deposited ∝ charge passed: m = (QM)/(nF)
- 1 F = charge per mole of electrons = 96485 C/mol

## L3 Tools
- See existing `nernst_equation`, `galvanic_cells`, `electrochemistry` L2s

## L4 Data
- Standard reduction potentials in `L4_data/electrochemical_data/`

## Source
DeVoe, *Thermodynamics and Chemistry*, Ch12 (Electrochemical Cells).

## Data Reference
- L4 Data: L4_reference/electrode_potentials.csv — Standard reduction potentials E° for 28 half-reactions
- L4 Reference: L4_reference/THERMODYNAMIC_DATABASES.md — Links to NIST, CRC Handbook
