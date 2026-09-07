# Flory-Huggins Solution Theory

[Source: Polymer Physics (Steimel), Ch4]

## Core Concept

Flory-Huggins theory describes the thermodynamics of polymer solutions, explaining miscibility, phase separation, and solvent quality through a lattice model.

## Free Energy of Mixing

$$\Delta G_{mix} = RT \left( n_1 \ln \phi_1 + n_2 \ln \phi_2 + n_1 \phi_2 \chi_{12} \right)$$

where:
- $n_1$, $n_2$ = moles of solvent and polymer
- $\phi_1$, $\phi_2$ = volume fractions
- $\chi_{12}$ = Flory-Huggins interaction parameter

## Chemical Potentials

$$\Delta \mu_1 = RT \left[ \ln(1-\phi_2) + \left(1 - \frac{1}{N}\right)\phi_2 + \chi_{12}\phi_2^2 \right]$$

$$\Delta \mu_2 = RT \left[ \ln \phi_2 + (1-N)\phi_1 + N\chi_{12}\phi_1^2 \right]$$

where $N$ is the degree of polymerization.

## Osmotic Pressure (for polymer solutions)

$$\Pi = -\frac{\Delta \mu_1}{V_1} = \frac{RT}{V_1}\left[ \frac{\phi_2}{N} + \left(\frac{1}{2} - \chi_{12}\right)\phi_2^2 + \frac{\phi_2^3}{3} + \cdots \right]$$

This relates to virial expansion: $\Pi/RTc = M_n^{-1} + A_2 c + A_3 c^2 + \cdots$

## Second Virial Coefficient

$$A_2 = \frac{V_1}{M_1^2}\left(\frac{1}{2} - \chi_{12}\right)$$

- $A_2 > 0$: Good solvent ($\chi_{12} < 0.5$)
- $A_2 = 0$: Theta condition ($\chi_{12} = 0.5$)
- $A_2 < 0$: Poor solvent ($\chi_{12} > 0.5$)

## Phase Separation

### Spinodal Condition (instability onset)
$$\frac{\partial^2 \Delta G_{mix}}{\partial \phi_2^2} = 0$$

$$\frac{1}{1-\phi_2} + \frac{1}{N\phi_2} - 2\chi_{12} = 0$$

### Critical Point
$$\phi_{2,c} = \frac{1}{1 + \sqrt{N}}, \quad \chi_{c} = \frac{1}{2}\left(1 + \frac{1}{\sqrt{N}}\right)^2$$

For large $N$: $\chi_c \approx 0.5 + N^{-1/2}$

### Binodal (coexistence curve)
Equal chemical potential condition: $\Delta\mu_1(\phi') = \Delta\mu_1(\phi'')$ and $\Delta\mu_2(\phi') = \Delta\mu_2(\phi'')$

## Temperature Dependence

$$\chi_{12} = \alpha + \frac{\beta}{T}$$

- Upper Critical Solution Temperature (UCST): phase separates on cooling
- Lower Critical Solution Temperature (LCST): phase separates on heating

## Polymer Blends

For two polymers with degrees of polymerization $N_A$ and $N_B$:

$$\chi_c = \frac{1}{2}\left(\frac{1}{\sqrt{N_A}} + \frac{1}{\sqrt{N_B}}\right)^2$$

For high MW: $\chi_c \approx 0$, making most polymer blends immiscible.

## Problem Types

1. Calculate $\Delta G_{mix}$ for a polymer solution
2. Determine solvent quality from $\chi$ parameter
3. Find spinodal and binodal curves
4. Calculate osmotic pressure and molecular weight
5. Predict phase behavior of polymer blends

## L3 Tools

- `polymer_physics.py` — Flory-Huggins calculations

## Related L2 Nodes

- `polymer_chain_models.md` — Chain conformation in solution
- `polymer_properties.md` — Bulk properties
