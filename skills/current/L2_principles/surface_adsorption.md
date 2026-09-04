---
id: surface_adsorption.langmuir_bet
layer: 2
title: Surface Adsorption (Langmuir/BET)
parent: ../L1_ontology/chemistry-core-map.md#entry-264
stability: high
confidence: high
last_verified: 2026-03-24
source: LibreTexts Inorganic Chemistry (Haas), LibreTexts Catalysis Module, Physical Chemistry (LibreTexts) Ch29.8
---

# Surface Adsorption (Langmuir & BET Theory)

## Core Concept

Adsorption is the adhesion of atoms, ions, or molecules from a gas, liquid, or dissolved solid to a surface. In heterogeneous catalysis, adsorption is the critical first step — reactants must bind to the catalyst surface before reaction can occur.

**Key distinction:** Adsorption (surface binding) vs. Absorption (bulk uptake).

## Types of Adsorption

### Physisorption
- Weak van der Waals forces (~5–40 kJ/mol)
- Reversible, non-specific, multilayer possible
- Low activation energy

### Chemisorption
- Strong chemical bond formation (~40–800 kJ/mol)
- Often irreversible, specific, monolayer only
- Higher activation energy, requires activation

---

## Langmuir Isotherm

### Assumptions
1. Monolayer coverage only
2. All surface sites are equivalent
3. No interactions between adsorbed molecules
4. Dynamic equilibrium between adsorption and desorption

### Equation

$$\theta = \frac{KP}{1 + KP}$$

Where:
- θ = fractional surface coverage
- K = adsorption equilibrium constant
- P = gas pressure

### Linearized Form

$$\frac{P}{V} = \frac{1}{KV_m} + \frac{P}{V_m}$$

Where V = volume adsorbed, V_m = monolayer capacity.

### Langmuir for Dissociative Adsorption

$$\theta = \frac{\sqrt{KP}}{1 + \sqrt{KP}}$$

When molecule A₂ dissociates into 2A on the surface (e.g., H₂ on metals).

### Langmuir for Competitive Adsorption

$$\theta_A = \frac{K_A P_A}{1 + K_A P_A + K_B P_B}$$

---

## BET Isotherm (Brunauer-Emmett-Teller)

### Extends Langmuir to multilayer adsorption

$$\frac{P}{V(P_0 - P)} = \frac{1}{V_m C} + \frac{(C-1)P}{V_m C P_0}$$

Where:
- P = equilibrium pressure
- P₀ = saturation vapor pressure
- V = volume of gas adsorbed
- V_m = monolayer volume
- C = BET constant (related to heat of adsorption)

### BET Surface Area

$$A = \frac{V_m N_A \sigma}{V_{molar}}$$

Where σ = cross-sectional area of adsorbate molecule (N₂: 0.162 nm²).

### BET Classification (5 Types)
1. **Type I:** Microporous ( Langmuir-like, monolayer)
2. **Type II:** Non-porous/macroporous (multilayer)
3. **Type III:** Weak adsorbate-adsorbent interaction
4. **Type IV:** Mesoporous (capillary condensation hysteresis)
5. **Type V:** Weak interaction, porous

---

## Sticking Coefficient

$$s = \frac{\text{rate of adsorption}}{\text{collision rate with surface}}$$

Fraction of molecules striking the surface that actually adsorb.

## Isosteric Heat of Adsorption

$$\ln P = -\frac{\Delta H_{ads}}{R}\frac{1}{T} + \text{const}$$

From Clausius-Clapeyron at constant coverage.

---

## Complete Extraction: Surface Catalysis Mechanisms (Physical Chemistry Ch29.8)

### Five Stages of Heterogeneous Catalysis (Surface Adsorption Theory)
1. **Diffusion** of reactants to the surface (rate influenced by bulk concentration and boundary layer thickness)
2. **Adsorption** of reactants (bonds form; sticking coefficient = fraction of molecules that stick)
3. **Reaction** on the surface (bonds form between adsorbed species)
4. **Desorption** of products (bonds break as products leave surface)
5. **Diffusion** of products away from the surface

### Kinetic Treatment: Unimolecular Surface Catalysis
For A(g) + S(s) ⇌ AS(s) → P(g) + S(s):

**Steady-state on AS:**
$$\frac{d[AS]}{dt} = k_1[A][S] - k_{-1}[AS]_{ss} - k_2[AS]_{ss} = 0$$

**Fractional surface coverage:**
$$\theta = \frac{k_1[A]}{k_1[A] + k_{-1} + k_2}$$

**Rate of production:**
$$\frac{d[P]}{dt} = k_2\theta[S]_0 = \frac{k_1 k_2}{k_1[A] + k_{-1} + k_2}[A][S]_0$$

Key insight: High surface area [S]₀ is critical for catalytic rate.

### Langmuir-Hinshelwood Mechanism (Bimolecular)
Both A and B adsorb onto the surface before reacting:
1. A(g) + S(s) ⇌ AS(s)
2. B(g) + S(s) ⇌ BS(s)
3. AS(s) + BS(s) → P

### Eley-Rideal Mechanism (Bimolecular)
Only one species adsorbs; the other reacts from gas phase:
1. A(g) + S(s) ⇌ AS(s)
2. AS(s) + B(g) → P(g) + S(s)

**Example:** Partial oxidation of ethylene to ethylene oxide (O₂ adsorbed, C₂H₄ reacts from gas phase)

**Rate law (simplified, k₂ ≪ k₁, k₋₁):**
$$\frac{d[P]}{dt} = K k_2[B]\frac{K[A]}{K[A] + 1}[S]_0$$
where K = k₁/k₋₁ (adsorption equilibrium constant)

### General Catalysis Kinetics
For reaction A → P with catalyst C:
$$\frac{d[A]}{dt} = -k[A] - k_{cat}[A][C]$$
Since k_cat ≫ k, the uncatalyzed term is often negligible.

### Source Cross-References
- Physical Chemistry (LibreTexts) Ch29.8
- LibreTexts Catalysis Module
- LibreTexts Inorganic Chemistry (Haas) 14.4

---

## Links

- L3: `../L3_functions/heterogeneous_catalysis_tools.py`
- L4: `../L4_reference/heterogeneous_catalysis_reference.csv`
- L5: `../L5_examples/heterogeneous_catalysis_examples.md`
