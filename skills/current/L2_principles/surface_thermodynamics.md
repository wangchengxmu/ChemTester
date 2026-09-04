---
id: surface-thermodynamics
layer: L2
topic: thermodynamics
source: DeVoe Ch14
depends: [thermodynamic_potentials, material_equilibrium]
tags: [thermodynamics, surface-tension, adsorption, capillarity, young-laplace]
---

# Surface Effects and Interface Thermodynamics

## Concept Overview
When a system has an interface between phases, surface effects become important. Surface tension (surface free energy per unit area) governs capillary phenomena, adsorption, and the stability of colloids.

## Key Principles

### Surface Tension (Î³)
Work required to increase surface area:
```
Î³ = (âˆ‚A/âˆ‚A_s)_{T,p}  [J/mÂ² = N/m]
```
where A is Helmholtz energy and A_s is surface area.

For a system with a surface:
```
dG = âˆ’S dT + V dp + Î³ dA_s + Î£áµ¢ Î¼áµ¢ dnáµ¢
```

### Young-Laplace Equation
Pressure difference across a curved interface:
```
Î”p = Î³(1/râ‚ + 1/râ‚‚)
```
For a sphere: Î”p = 2Î³/r
For a cylinder: Î”p = Î³/r

### Capillary Rise
```
h = 2Î³ cos Î¸ / (Ï g r)
```
where Î¸ is contact angle, r is capillary radius, Ï is liquid density.

### Kelvin Equation (vapor pressure of curved surface)
```
RT ln(p_r/p_âˆž) = 2Î³V_m/r
```
- Convex surface (droplet): p_r > p_âˆž â†’ easier to evaporate
- Concave surface (bubble): p_r < p_âˆž â†’ harder to evaporate

### Gibbs Adsorption Isotherm
Surface excess concentration:
```
Î“â‚‚ = âˆ’(1/RT)(âˆ‚Î³/âˆ‚ln aâ‚‚)_{T}
```
- Î“â‚‚ > 0: positive adsorption (surfactant concentrates at surface)
- Î“â‚‚ < 0: negative adsorption (solute depleted at surface)

### Langmuir Adsorption Isotherm
```
Î¸ = KP/(1 + KP)
```
where Î¸ = fraction of surface covered, K = adsorption equilibrium constant.

### BET Isotherm (multilayer adsorption)
```
P/[v(Pâ‚€âˆ’P)] = 1/(v_m C) + (Câˆ’1)v_m C Â· P/Pâ‚€
```
Used to determine surface area from gas adsorption data.

## L3 Tools
- `L3_functions/surface_thermo_tools.py` â€” Young-Laplace, Kelvin equation, adsorption isotherms

## L4 Data
- Surface tension data in `L4_data/surface_data/`
- See existing `surface_chemistry` L2

## Source
DeVoe, *Thermodynamics and Chemistry*, Ch14 (Surface Effects).

## L3 Tool Call Directives

**Source:** surface_thermo_tools.py
Young-Laplace, Kelvin equation, Langmuir/BET adsorption.

### Available functions:
- young_laplace(gamma: float, r1: float, r2: float) ¡ú float ¡ª ¦¤P = ¦Ã(1/r? + 1/r?)
- kelvin_radius(T: float, gamma: float, vm: float, p_ratio: float) ¡ú float ¡ª r = 2¦ÃV?/(RT¡¤ln(P/P?))
- langmuir_adsorption(P: float, KL: float, qmax: float) ¡ú float ¡ª q = qmax¡¤KL¡¤P/(1 + KL¡¤P)
- et_surface_area(n_monolayer: float, area_molecule: float, na=6.022e23) ¡ú float ¡ª Surface area from monolayer capacity

### Common errors:
- ? For sphere r1=r2=r; for cylinder r2=¡Þ (use very large number, not 0)
- ? kelvin_radius p_ratio must not equal 1.0 (returns infinity)
