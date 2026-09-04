---
id: chem.polymer_chain_models
layer: 2
title: Polymer Chain Models
source: Polymer Physics (Steimel), Ch3
status: active
created: 2026-03-18
down_links:
  - ../L3_functions/polymer_physics.py
  - ../L3_functions/polymer_tools.py
---

# Polymer Chain Models

[Source: Polymer Physics (Steimel), Ch3]

## Core Concept

Polymer chain models describe the statistical properties of polymer conformations. These models relate molecular structure to measurable properties like radius of gyration and end-to-end distance.

## Key Models

### 1. Freely Jointed Chain (FJC)

- N segments of length l
- No restrictions on bond angles
- Random walk in 3D

$$\langle R^2 \rangle = Nl^2$$

### 2. Freely Rotating Chain

- Fixed bond angle θ
- Free rotation around bonds

$$\langle R^2 \rangle = Nl^2 \frac{1+\cos\theta}{1-\cos\theta}$$

### 3. Gaussian Chain

- Continuous limit of FJC
- Valid for long chains

$$P(R) = \left(\frac{3}{2\pi\langle R^2\rangle}\right)^{3/2} \exp\left(-\frac{3R^2}{2\langle R^2\rangle}\right)$$

## Key Equations

### Radius of Gyration

$$R_g^2 = \frac{1}{N}\sum_{i=1}^{N} \langle (\vec{r}_i - \vec{r}_{cm})^2 \rangle$$

For Gaussian chain:
$$R_g^2 = \frac{\langle R^2 \rangle}{6}$$

### Characteristic Ratio

$$C_\infty = \frac{\langle R^2 \rangle}{Nl^2}$$

- Measures chain stiffness
- C∞ = 1 for freely jointed
- C∞ > 1 for real chains

### Persistence Length

$$L_p = \frac{l}{1-\cos\theta}$$

## Problem Types

1. **Calculate Rg** from chain parameters
2. **Estimate chain dimensions** from molecular weight
3. **Compare chain stiffness** using characteristic ratio
4. **Apply Gaussian statistics** to chain conformations

## L3 Tools

- `../L3_functions/polymer_physics.py` - Chain model calculations (R2, Rg, persistence length, Gaussian distribution)

## Related Topics

- → `polymer_properties.md` for Tg/Tm
- → `polymer_viscoelasticity.md` for mechanical properties

## L3 Tool Call Directives

**Source:** polymer_physics.py
Polymer Physics - L3 Implementation

### Available functions:
- freely_jointed_chain_R2(N, l) → float — Calculate mean squared end-to-end distance for freely jointed chain.
- radius_of_gyration(R2) → float — Calculate radius of gyration from mean squared end-to-end distance.
- characteristic_ratio(R2, N, l) → float — Calculate characteristic ratio.
- persistence_length(bond_length, bond_angle) → float — Calculate persistence length from bond geometry.
- gaussian_distribution(R, R2) → float — Gaussian probability distribution for end-to-end distance.
- maxwell_relaxation(G0, t, tau) → float — Maxwell model stress relaxation modulus.
- complex_modulus(G_prime, G_double_prime) →  — Calculate magnitude and phase of complex modulus.
- complex_viscosity(G_prime, G_double_prime, omega) → float — Calculate complex viscosity.
- wlf_shift(T, T_ref, C1, C2) → float — Calculate WLF shift factor.
- arrhenius_shift(T, T_ref, Ea, R) → float — Calculate Arrhenius shift factor.

### Common errors:
- ❌ Passing wrong parameter types or missing required arguments
