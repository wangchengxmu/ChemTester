---
id: mixtures-partial-molar
layer: L2
topic: thermodynamics
source: DeVoe Ch9
depends: [thermodynamic_potentials, material_equilibrium]
tags: [thermodynamics, mixtures, partial-molar, chemical-potential, fugacity]
---

# Mixtures and Partial Molar Quantities

## Concept Overview
A homogeneous mixture is a phase with more than one substance. Partial molar quantities describe how extensive properties change with composition. The chemical potential is the key driver of mass transfer and reaction equilibrium.

## Key Principles

### Partial Molar Quantities
```
Xᵢ ≡ (∂X/∂nᵢ)_{T,p,n_{j≠i}}
```
where X is any extensive property (V, H, S, G, etc.).

**Total property from partial molar quantities:**
```
X = Σᵢ nᵢ Xᵢ
```

**Relation between molar and partial molar (binary):**
```
X = x_A X_A + x_B X_B
X_A = X + x_B (dX/dx_B)_{T,p}
X_B = X − x_A (dX/dx_B)_{T,p}
```
(Intercept method: plot X vs x_B, extrapolate to x_B=0 and x_B=1)

### Chemical Potential
For substance i in a mixture:
```
μᵢ = (∂G/∂nᵢ)_{T,p,n_{j≠i}} = Gᵢ
```

**Fundamental equation for open systems:**
```
dG = −S dT + V dp + Σᵢ μᵢ dnᵢ
```

### Fugacity and Fugacity Coefficient
For real gases, fugacity f replaces pressure:
```
μᵢ = μᵢ°(T) + RT ln(fᵢ/p°)
φᵢ ≡ fᵢ/pᵢ  (fugacity coefficient)
```

For ideal gas: φᵢ = 1, fᵢ = pᵢ

**Relation via equation of state:**
```
RT ln φᵢ = ∫₀^p [Vᵢ − RT/p] dp  (constant T)
```

For virial EOS: ln φᵢ = B'_i p/(RT)

### Activity and Activity Coefficient (condensed phases)
```
aᵢ ≡ γᵢ · (basis quantity)
```
Standard states:
- Solvent (Raoult's law basis): a_A = γ_A x_A, γ_A → 1 as x_A → 1
- Solute (Henry's law basis):
  - Mole fraction: a_B = γ_{x,B} x_B
  - Molality: a_B = γ_{m,B} m_B/m°
  - Concentration: a_B = γ_{c,B} c_B/c°

### Gas Mixtures (Dalton's Law)
```
pᵢ = yᵢ p
Σᵢ pᵢ = p  (always valid)
```
Ideal gas mixture: pᵢ = nᵢ RT/V

**Virial equation for mixtures:**
```
B = Σᵢ Σⱼ yᵢ yⱼ Bᵢⱼ
```

### Ideal Mixtures
```
μᵢ = μᵢ* + RT ln xᵢ
ΔG_mix = nRT Σᵢ xᵢ ln xᵢ  (always < 0)
ΔS_mix = −nR Σᵢ xᵢ ln xᵢ  (always > 0)
ΔV_mix = 0,  ΔH_mix = 0
```

### Colligative Properties (dilute solutions)
- **Boiling point elevation:** ΔT_b = K_b · m_B
- **Freezing point depression:** ΔT_f = K_f · m_B
- **Osmotic pressure:** Π = c_B RT (van't Hoff)

## L3 Tools
- `L3_functions/mixture_tools.py` — partial molar calculations, activity coefficients, mixing properties
- See existing `colligative_properties` L2

## L4 Data
- Virial coefficients, Henry's law constants in `L4_data/solution_data/`

## Source
DeVoe, *Thermodynamics and Chemistry*, Ch9 (Mixtures). LibreTexts sections 9.2, 9.3 verified.
