# Phase Diagrams Reference
[Source: Averill, Ch11]

## Triple Points

| Substance | Temperature (K) | Temperature (°C) | Pressure (atm) |
|-----------|-----------------|------------------|----------------|
| Water | 273.16 | 0.01 | 0.00604 |
| CO₂ | 216.6 | -56.6 | 5.11 |
| Nitrogen | 63.15 | -210 | 0.124 |
| Oxygen | 54.36 | -219 | 0.0015 |
| Benzene | 278.7 | 5.6 | 0.047 |
| Argon | 83.8 | -189 | 0.68 |
| Methane | 90.7 | -183 | 0.12 |

## Critical Points

| Substance | Tc (K) | Tc (°C) | Pc (atm) | Pc (MPa) |
|-----------|--------|---------|----------|----------|
| Water | 647.1 | 374.0 | 217.7 | 22.06 |
| CO₂ | 304.2 | 31.0 | 72.79 | 7.38 |
| Nitrogen | 126.2 | -147 | 33.5 | 3.39 |
| Oxygen | 154.6 | -119 | 49.8 | 5.04 |
| Benzene | 562.2 | 289 | 48.3 | 4.90 |
| Ethane | 305.3 | 32.2 | 48.2 | 4.88 |
| Propane | 369.8 | 96.7 | 41.9 | 4.25 |
| Methane | 190.6 | -83 | 45.4 | 4.60 |
| Ammonia | 405.5 | 132 | 111.3 | 11.28 |
| Ethylene | 282.4 | 9.2 | 49.7 | 5.04 |

## Normal Boiling Points

| Substance | Tb (K) | Tb (°C) | ΔHvap (kJ/mol) |
|-----------|--------|---------|----------------|
| Helium | 4.22 | -269 | 0.084 |
| Hydrogen | 20.28 | -253 | 0.904 |
| Nitrogen | 77.36 | -196 | 5.56 |
| Oxygen | 90.20 | -183 | 6.82 |
| Methane | 111.7 | -161 | 8.17 |
| Ethane | 184.6 | -89 | 14.7 |
| Propane | 231.1 | -42 | 19.0 |
| Ammonia | 239.8 | -33 | 23.4 |
| CO₂ | Sublimes | -78.5* | 25.2 |
| Benzene | 353.3 | 80 | 30.8 |
| Ethanol | 351.5 | 78 | 38.6 |
| Water | 373.15 | 100 | 40.7 |
| Mercury | 629.9 | 357 | 59.2 |

*Sublimation point at 1 atm

## Normal Melting Points

| Substance | Tm (K) | Tm (°C) | ΔHfus (kJ/mol) |
|-----------|--------|---------|----------------|
| Helium | - | -272* | - |
| Hydrogen | 14.0 | -259 | 0.117 |
| Nitrogen | 63.15 | -210 | 0.72 |
| Oxygen | 54.36 | -219 | 0.44 |
| Water | 273.15 | 0 | 6.01 |
| Benzene | 278.7 | 5.5 | 9.87 |
| CO₂ | - | - | - |
| Mercury | 234.3 | -39 | 2.29 |
| Sodium | 371.0 | 98 | 2.60 |
| Iron | 1811 | 1538 | 13.8 |

*Helium remains liquid to 0 K at 1 atm

## Key Formulas

### Clausius-Clapeyron Equation
```
ln(P₂/P₁) = -ΔHvap/R × (1/T₂ - 1/T₁)
```

### Two-Point Form
```
ln(P) = -ΔHvap/(RT) + C
```

### Boiling Point at Different Pressure
```
1/T₂ = 1/T₁ - (R/ΔHvap) × ln(P₂/P₁)
```

## Phase Diagram Features

### Water (Anomalous)
- Solid-liquid boundary slopes LEFT
- Ice less dense than liquid water
- Pressure lowers melting point
- Triple point: 0.01°C, 0.006 atm
- Critical point: 374°C, 218 atm

### CO₂ (Normal)
- Solid-liquid boundary slopes RIGHT
- No liquid phase at 1 atm
- Sublimes at -78.5°C
- Triple point: -56.6°C, 5.11 atm
- Critical point: 31°C, 73 atm

### Phase Identification Rules

| Condition | Phase |
|-----------|-------|
| T > Tc AND P > Pc | Supercritical fluid |
| T > Tc AND P < Pc | Gas |
| T < Tc AND P > Pc | Compressed liquid |
| On solid-liquid line | Solid-liquid equilibrium |
| On liquid-gas line | Liquid-gas equilibrium |
| On solid-gas line | Sublimation/deposition |

## Supercritical Fluids Applications

| Fluid | Tc (°C) | Pc (atm) | Applications |
|-------|---------|----------|--------------|
| CO₂ | 31 | 73 | Decaffeination, extraction |
| Water | 374 | 218 | Waste destruction, oxidation |
| Ethane | 32 | 48 | Oil extraction |
| Propane | 97 | 42 | Heavy oil processing |

## Related Topics
- [intermolecular-forces-reference.md](intermolecular-forces-reference.md)
- [liquid-properties-reference.md](liquid-properties-reference.md)
