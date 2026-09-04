# Reptation and Polymer Dynamics

[Source: Polymer Physics (Steimel), Ch11]

## Core Concept

Polymer chain dynamics in melts and concentrated solutions are governed by topological constraints (entanglements). The reptation model describes how chains move by snaking through a tube formed by neighboring chains.

## Rouse Model (Unentangled Melts)

For short chains below the entanglement molecular weight $M_e$:

**Center-of-mass diffusion:**
$$D_{Rouse} = \frac{k_B T}{N \zeta} = \frac{k_B T}{N_6\pi\eta_s a}$$

**Longest relaxation time:**
$$\tau_R = \frac{\zeta N^2 b^2}{3\pi^2 k_B T}$$

**Viscosity:**
$$\eta \propto M \quad (M < M_e)$$

## Entanglement

- **Entanglement molecular weight** $M_e$: critical MW for entanglement onset
- **Entanglement length** $N_e$: number of monomers per entanglement strand
- Typical values: $M_e \approx 10-40$ kDa (varies with polymer)

## Reptation Model (de Gennes/Doi-Edwards)

For chains with $M > M_e$ (entangled regime):

### Tube Concept
Each chain is confined in a tube formed by surrounding chains. The chain can only move along the tube axis (reptate).

### Disengagement Time
$$\tau_d \propto N^3 \propto M^3$$

### Diffusion Coefficient
$$D_{rept} \propto \frac{1}{N^2} \propto \frac{1}{M^2}$$

### Viscosity
$$\eta \propto M^3 \quad (M > M_e, \text{ experimental: } \eta \propto M^{3.4})$$

## Viscoelastic Regimes

| Regime | Time Scale | Behavior | $G'(\omega)$ |
|--------|-----------|----------|-------------|
| Glassy | $t < \tau_e$ | Elastic, $G \approx G_0$ | Plateau |
| Entanglement plateau | $\tau_e < t < \tau_d$ | Rubber-like | $G' \approx G_N^0 = \frac{\rho RT}{M_e}$ |
| Terminal flow | $t > \tau_d$ | Viscous flow | $G' \propto \omega^2$ |

### Plateau Modulus
$$G_N^0 = \frac{4}{5} \frac{\rho RT}{M_e}$$

## Constraint Release

Neighboring chains also move, relaxing the tube constraints. This provides an additional relaxation mechanism beyond reptation.

## Problem Types

1. Calculate Rouse relaxation time and diffusion coefficient
2. Estimate entanglement molecular weight from plateau modulus
3. Predict molecular weight scaling of viscosity and diffusion
4. Interpret viscoelastic spectra in terms of Rouse/reptation models
5. Estimate tube diameter from $M_e$

## Related L2 Nodes

- `polymer_viscoelasticity.md` — Viscoelastic behavior
- `polymer_chain_models.md` — Static chain conformations
