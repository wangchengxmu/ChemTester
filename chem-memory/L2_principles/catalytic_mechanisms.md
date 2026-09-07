---
id: catalytic_mechanisms.lh_er
layer: 2
title: Catalytic Mechanisms (Langmuir-Hinshelwood & Eley-Rideal)
parent: ../L1_ontology/chemistry-core-map.md#entry-265
stability: high
confidence: high
last_verified: 2026-03-24
source: LibreTexts Physical Chemistry Ch29.8, LibreTexts Catalysis Module
---

# Catalytic Mechanisms (Langmuir-Hinshelwood & Eley-Rideal)

## Core Concept

Heterogeneous catalytic reactions proceed through surface-mediated mechanisms. Two fundamental models describe how reactants interact on the catalyst surface.

---

## Five Stages of Heterogeneous Catalysis

1. **Diffusion** of reactants to the catalyst surface
2. **Adsorption** of reactants onto active sites
3. **Surface reaction** between adsorbed species
4. **Desorption** of products
5. **Diffusion** of products away from surface

---

## Langmuir-Hinshelwood (LH) Mechanism

### Definition
Both reactants are adsorbed on the catalyst surface and react on adjacent sites.

### Mechanism
```
A(g) + * ⇌ A*     (adsorption)
B(g) + * ⇌ B*     (adsorption)
A* + B* → C* + D* (surface reaction)
C* → C(g) + *     (desorption)
D* → D(g) + *     (desorption)
```

### Rate Law (irreversible surface reaction, rate-determining step)

$$r = \frac{k K_A K_B P_A P_B}{(1 + K_A P_A + K_B P_B)^2}$$

### Special Cases
- **Low coverage** (KP ≪ 1): r ≈ kK_AK_BP_AP_B (second-order overall)
- **High A coverage**: r ≈ kK_BP_B/(K_AP_A) (inverse order in A, first in B)
- **One reactant weakly adsorbed** (B, K_BP_B ≪ 1): r ≈ kK_AK_BP_AP_B/(1+K_AP_A)²

---

## Eley-Rideal (ER) Mechanism

### Definition
One reactant is adsorbed; the other reacts directly from the gas phase without adsorbing.

### Mechanism
```
A(g) + * ⇌ A*     (adsorption)
A* + B(g) → C(g) + * (direct reaction from gas phase)
```

### Rate Law

$$r = \frac{k K_A P_A P_B}{1 + K_A P_A}$$

### Key Difference from LH
- ER: no need for adjacent vacant sites for B
- LH: requires both reactants adsorbed on neighboring sites
- ER rate is first-order in the gas-phase reactant at low coverage

---

## Mars-van Krevelen Mechanism

### Definition
Reactant consumes lattice atoms from the catalyst, which are subsequently replenished.

### Common for: oxidation reactions (e.g., V₂O₅ in contact process)

```
V₂O₅ + SO₂ → V₂O₄ + SO₃
2V₂O₄ + O₂ → 2V₂O₅
```

---

## Kinetic Analysis: Steady-State Approximation

For a general surface reaction A* → P + *, applying steady-state to A*:

$$\frac{d[\text{A}^*]}{dt} = k_1[\text{A}][\text{S}] - k_{-1}[\text{A}^*] - k_2[\text{A}^*] = 0$$

Where S = vacant sites, [A*] = θ[A*]₀, [S] = (1-θ)[A*]₀.

---

## Links

- L3: `../L3_functions/heterogeneous_catalysis_tools.py`
- L4: `../L4_reference/heterogeneous_catalysis_reference.csv`
- L5: `../L5_examples/heterogeneous_catalysis_examples.md`
