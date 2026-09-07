# Liquid Properties Reference
[Source: Averill, Ch11]

## Surface Tension Values at 20°C

| Liquid | Surface Tension (mN/m) | Dominant IMF |
|--------|------------------------|--------------|
| Water | 72.8 | H-bonding |
| Mercury | 486 | Metallic |
| Glycerol | 63.4 | H-bonding (multiple) |
| Ethylene glycol | 47.7 | H-bonding |
| Benzene | 28.9 | London dispersion |
| Chloroform | 27.1 | Dipole-dipole |
| Carbon tetrachloride | 26.9 | London dispersion |
| Acetone | 23.7 | Dipole-dipole |
| Methanol | 22.7 | H-bonding |
| Ethanol | 22.1 | H-bonding |
| Diethyl ether | 17.0 | Dipole-dipole |
| Hexane | 18.4 | London dispersion |

## Viscosity Values at 20°C

| Liquid | Viscosity (mPa·s) | Reason |
|--------|-------------------|--------|
| Honey | 10,000 | High MW sugars, H-bonding |
| Glycerol | 1412 | 3 OH groups, extensive H-bonding |
| Motor oil (SAE 30) | 250 | Long hydrocarbon chains |
| Ethylene glycol | 16.1 | 2 OH groups, H-bonding |
| Mercury | 1.55 | Metallic bonding |
| Water | 1.00 | H-bonding network |
| Ethanol | 1.20 | H-bonding |
| Benzene | 0.65 | London dispersion |
| Methanol | 0.59 | H-bonding |
| Carbon tetrachloride | 0.97 | London dispersion |
| Hexane | 0.31 | London dispersion |
| Acetone | 0.32 | Dipole-dipole |
| Diethyl ether | 0.24 | Weak IMFs |

## Contact Angles

| Liquid-Surface Pair | Contact Angle (°) | Meniscus | Behavior |
|---------------------|-------------------|----------|----------|
| Water-Glass | 10 | Concave | Strong adhesion |
| Water-Plastic | 70 | Concave | Moderate adhesion |
| Mercury-Glass | 140 | Convex | Strong cohesion |
| Ethanol-Glass | 5 | Concave | Strong adhesion |
| Hexane-Glass | 5 | Concave | Strong adhesion |
| Water-Teflon | 110 | Convex | Non-wetting |

## Key Formulas

### Capillary Rise (Jurin's Law)
```
h = 2γcos(θ) / (ρgr)
```
- γ = surface tension (N/m)
- θ = contact angle
- ρ = density (kg/m³)
- g = 9.81 m/s²
- r = tube radius (m)

### Surface Tension Temperature Dependence
```
γ(T) = γ₀ × (Tc - T)/(Tc - T₀) ^ 1.23
```

### Viscosity Temperature Dependence
```
η(T) = η₀ × exp(Ea/R × (1/T - 1/T₀))
```
- Ea ≈ 15-25 kJ/mol for most liquids

### Work of Adhesion (Dupre Equation)
```
W_ad = γ_L + γ_S - γ_LS
```

### Spreading Coefficient
```
S = γ_substrate - (γ_liquid + γ_interfacial)
```
- S > 0: Spreading occurs
- S < 0: Droplets form

## Densities at 20°C

| Liquid | Density (g/cm³) |
|--------|-----------------|
| Mercury | 13.55 |
| Glycerol | 1.261 |
| Ethylene glycol | 1.113 |
| Water | 0.998 |
| Carbon tetrachloride | 1.594 |
| Chloroform | 1.489 |
| Benzene | 0.876 |
| Acetone | 0.790 |
| Ethanol | 0.789 |
| Methanol | 0.791 |
| Diethyl ether | 0.713 |
| Hexane | 0.659 |

## Temperature Effects

### Surface Tension
- Decreases with temperature
- Approaches zero at critical point
- Water: 75.6 mN/m at 0°C → 58.9 mN/m at 100°C

### Viscosity
- Decreases exponentially with temperature
- Water: 1.79 mPa·s at 0°C → 0.28 mPa·s at 100°C
- Motor oil: Large change → need multigrade oils

## Cohesive vs Adhesive Forces

| Situation | Cohesion > Adhesion | Adhesion > Cohesion |
|-----------|---------------------|---------------------|
| Meniscus | Convex | Concave |
| Capillary | Depression | Rise |
| Contact angle | > 90° | < 90° |
| Example | Mercury in glass | Water in glass |

## Capillary Rise Examples

| System | γ (mN/m) | θ (°) | ρ (g/cm³) | Tube radius (mm) | Rise (mm) |
|--------|----------|-------|-----------|------------------|-----------|
| Water-glass | 72.8 | 10 | 0.998 | 0.5 | +29.4 |
| Water-glass | 72.8 | 10 | 0.998 | 0.1 | +147 |
| Mercury-glass | 486 | 140 | 13.55 | 0.5 | -8.9 |

## Related Topics
- [intermolecular-forces-reference.md](intermolecular-forces-reference.md)
- [phase-diagrams-reference.md](phase-diagrams-reference.md)
