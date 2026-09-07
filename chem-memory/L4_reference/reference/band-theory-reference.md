# Band Theory Reference
[Source: Averill, Ch12]

## Band Gap Values

### Metals (No Band Gap)
| Metal | Band Gap | Conductivity |
|-------|----------|--------------|
| Na | 0 | Excellent |
| Cu | 0 | Excellent |
| Au | 0 | Excellent |
| Ag | 0 | Excellent |
| Al | 0 | Excellent |
| Fe | 0 | Good |

### Semiconductors
| Material | Eg (eV) | Type | Applications |
|----------|---------|------|--------------|
| Si | 1.12 | Indirect | Electronics |
| Ge | 0.67 | Indirect | Detectors |
| GaAs | 1.43 | Direct | LEDs, solar cells |
| GaP | 2.26 | Indirect | LEDs |
| InP | 1.35 | Direct | Photonics |
| InSb | 0.17 | Direct | IR detectors |
| CdS | 2.42 | Direct | Solar cells |
| CdSe | 1.74 | Direct | Quantum dots |
| ZnO | 3.37 | Direct | UV LEDs |
| GaN | 3.4 | Direct | Blue LEDs |

### Insulators
| Material | Eg (eV) | Applications |
|----------|---------|--------------|
| Diamond | 5.5 | Insulator |
| SiO₂ | 9.0 | Gate oxide |
| Al₂O₃ | 8.8 | Substrate |
| BN | 5.9 | Insulator |

## Carrier Concentrations

### Intrinsic Carrier Concentration at 300 K

| Semiconductor | nᵢ (cm⁻³) |
|---------------|-----------|
| Si | 1.5 × 10¹⁰ |
| Ge | 2.4 × 10¹³ |
| GaAs | 1.8 × 10⁶ |
| InSb | 2 × 10¹⁶ |

## Carrier Mobilities (cm²/V·s)

| Semiconductor | μₑ (electrons) | μₕ (holes) |
|---------------|----------------|------------|
| Si | 1350 | 480 |
| Ge | 3900 | 1900 |
| GaAs | 8500 | 400 |
| InP | 5400 | 200 |
| GaN | 1000 | 350 |

## Doping

### n-Type Dopants (Donors)
| Semiconductor | Dopants |
|---------------|---------|
| Si | P, As, Sb |
| GaAs | Si, Se, Te |

### p-Type Dopants (Acceptors)
| Semiconductor | Dopants |
|---------------|---------|
| Si | B, Al, Ga |
| GaAs | Zn, Be, Mg |

## Temperature Effects

### Conductivity Trends
| Material Type | Effect of T ↑ | Reason |
|---------------|---------------|--------|
| Metal | σ decreases | Lattice scattering |
| Semiconductor | σ increases | More carriers excited |
| Insulator | Little effect | Gap too large |

## Key Formulas

### Intrinsic Carrier Concentration
```
nᵢ = √(Nc × Nv) × exp(-Eg/2kT)
```

### Conductivity
```
σ = q(nμₑ + pμₕ)
```

### Fermi Level (Intrinsic)
```
E_F = Eg/2 + (kT/2)ln(Nv/Nc)
```

### Temperature Dependence (Semiconductor)
```
σ = σ₀ × exp(-Eg/2kT)
```

### Band Gap vs Temperature (Varshni)
```
Eg(T) = Eg(0) - αT²/(T + β)
```
- α ≈ 4.7×10⁻⁴ eV/K for Si
- β ≈ 636 K for Si

## Optical Properties

### Photon Energy vs Wavelength
```
E(eV) = 1240/λ(nm)
```

### Band Gap to Photon Conversion
| Eg (eV) | λ (nm) | Color |
|---------|--------|-------|
| 1.6 | 775 | IR |
| 1.9 | 653 | Red |
| 2.2 | 564 | Green |
| 2.5 | 496 | Blue |
| 3.0 | 413 | Violet |
| 3.4 | 365 | UV |

## Device Applications

### LEDs
| Material | Eg (eV) | LED Color |
|----------|---------|-----------|
| GaAs | 1.43 | IR |
| GaAsP | 1.9-2.3 | Red-Orange |
| GaP | 2.26 | Green |
| GaN | 3.4 | Blue-UV |

### Solar Cells
| Material | Eg (eV) | Max Efficiency (%) |
|----------|---------|-------------------|
| Si | 1.12 | ~27 |
| GaAs | 1.43 | ~29 |
| CdTe | 1.45 | ~22 |
| Perovskite | 1.55 | ~25 |

## Effective Densities of States (300 K)

| Semiconductor | Nc (cm⁻³) | Nv (cm⁻³) |
|---------------|-----------|-----------|
| Si | 2.8 × 10¹⁹ | 1.04 × 10¹⁹ |
| Ge | 1.04 × 10¹⁹ | 6.0 × 10¹⁸ |
| GaAs | 4.7 × 10¹⁷ | 7.0 × 10¹⁸ |

## Related Topics
- [solid-state-reference.md](solid-state-reference.md)
- [crystal-structures-reference.md](crystal-structures-reference.md)
