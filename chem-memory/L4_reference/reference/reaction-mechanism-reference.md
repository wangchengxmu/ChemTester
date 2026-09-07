# Reaction Mechanism Reference
[Source: Organic Chemistry OpenStax, Ch06]

## Carbocation Stability

| Type | Structure | Relative Energy (kJ/mol) | Stability |
|------|-----------|-------------------------|-----------|
| Methyl | CH₃⁺ | 0 (reference) | Least stable |
| Primary | RCH₂⁺ | -50 | Unstable |
| Secondary | R₂CH⁺ | -85 | Moderate |
| Tertiary | R₃C⁺ | -120 | Most stable |
| Allylic | CH₂=CH-CH₂⁺ | -100 | Very stable |
| Benzylic | Ph-CH₂⁺ | -105 | Very stable |
| Vinyl | CH₂=CH⁺ | +50 | Highly unstable |

## Radical Stability

| Type | Structure | Relative Energy (kJ/mol) | Stability |
|------|-----------|-------------------------|-----------|
| Methyl | CH₃· | 0 (reference) | Least stable |
| Primary | RCH₂· | -30 | Low |
| Secondary | R₂CH· | -50 | Moderate |
| Tertiary | R₃C· | -70 | Most stable |
| Allylic | CH₂=CH-CH₂· | -80 | Very stable |
| Benzylic | Ph-CH₂· | -85 | Very stable |

## Carbanion Stability

| Type | Structure | Relative Energy (kJ/mol) | Stability |
|------|-----------|-------------------------|-----------|
| Methyl | CH₃:⁻ | 0 (reference) | Most stable |
| Primary | RCH₂:⁻ | -10 | Stable |
| Secondary | R₂CH:⁻ | +15 | Less stable |
| Tertiary | R₃C:⁻ | +35 | Least stable |

## Nucleophile Strength

### Strong Nucleophiles
| Nucleophile | Type | Base Strength |
|-------------|------|---------------|
| HO⁻ | Anion | Strong |
| RO⁻ | Anion | Strong |
| CN⁻ | Anion | Moderate |
| N₃⁻ | Anion | Weak |
| RS⁻ | Anion | Strong |
| I⁻ | Halide | Very weak |
| HS⁻ | Anion | Strong |

### Moderate Nucleophiles
| Nucleophile | Type | Base Strength |
|-------------|------|---------------|
| Br⁻ | Halide | Very weak |
| NH₃ | Neutral | Moderate |
| RNH₂ | Neutral | Moderate |
| R₂NH | Neutral | Moderate |

### Weak Nucleophiles
| Nucleophile | Type | Base Strength |
|-------------|------|---------------|
| H₂O | Neutral | Weak |
| ROH | Neutral | Weak |
| Cl⁻ | Halide | Very weak |
| F⁻ | Halide | Weak |

## Electrophile Strength

### Very Strong Electrophiles
| Electrophile | Type | Reactivity |
|--------------|------|------------|
| H⁺ | Proton | Extremely reactive |
| RCO⁺ | Acylium ion | Very reactive |

### Strong Electrophiles
| Electrophile | Type | Reactivity |
|--------------|------|------------|
| HBr, HCl, HI | Hydrogen halide | Strong |
| R-X (3°) | Alkyl halide | Strong |

### Moderate Electrophiles
| Electrophile | Type | Reactivity |
|--------------|------|------------|
| R-X (1°, 2°) | Alkyl halide | Moderate |
| RCHO | Aldehyde | Moderate |
| RCOR' | Ketone | Moderate |
| Br₂, Cl₂ | Halogen | Moderate |

### Weak Electrophiles
| Electrophile | Type | Reactivity |
|--------------|------|------------|
| RCOOH | Carboxylic acid | Weak |
| RCOOR' | Ester | Weak |

## SN1 vs SN2 Comparison

| Feature | SN1 | SN2 |
|---------|-----|-----|
| Mechanism | Two steps | One step |
| Intermediate | Carbocation | None |
| Rate law | Rate = k[RX] | Rate = k[RX][Nu] |
| Stereochemistry | Racemization | Inversion |
| Substrate preference | 3° > 2° > 1° | Methyl > 1° > 2° |
| Nucleophile | Weak OK | Strong required |
| Solvent | Polar protic | Polar aprotic |
| Rearrangements | Possible | No |

## E1 vs E2 Comparison

| Feature | E1 | E2 |
|---------|-----|-----|
| Mechanism | Two steps | One step |
| Intermediate | Carbocation | None |
| Rate law | Rate = k[RX] | Rate = k[RX][Base] |
| Stereochemistry | No preference | Anti-periplanar |
| Substrate preference | 3° > 2° | 3° > 2° > 1° |
| Base | Weak OK | Strong required |
| Temperature | High | Moderate-high |
| Rearrangements | Possible | No |

## Radical Chain Reaction Steps

### Initiation
```
X₂ → 2X·
Requires: Heat (Δ) or Light (hν)
```

### Propagation
```
X· + R-H → H-X + R·
R· + X₂ → R-X + X·
```

### Termination
```
X· + X· → X₂
R· + R· → R-R
X· + R· → R-X
```

## Curved Arrow Notation

| Arrow Type | Meaning | Example |
|------------|---------|---------|
| Curved arrow | Pair of electrons | Nu: → C⁺ |
| Fishhook arrow | Single electron | X· → X⁻ |
| Arrow from bond | Bond breaking | A-B → A⁺ + :B⁻ |
| Arrow to bond | Bond forming | A· + ·B → A-B |

## Energy Diagram Features

```
Energy
  │
  │        TS (transition state)
  │       ╱ ╲
  │      ╱   ╲  Ea
  │     ╱     ╲
  │ Reactants  ╲
  │             ╲ Products
  └───────────────────→ Reaction coordinate
        ΔH
```

| Term | Definition | Sign |
|------|------------|------|
| ΔH | Enthalpy change | - for exothermic |
| ΔG | Free energy change | - for spontaneous |
| Ea | Activation energy | Always positive |
| ΔH‡ | Enthalpy of activation | Related to Ea |

## Hammond Postulate

| Reaction Type | TS Character | Reason |
|---------------|--------------|--------|
| Exothermic | Early (reactant-like) | TS closer to reactants in energy |
| Endothermic | Late (product-like) | TS closer to products in energy |
| Thermoneutral | Midway | TS intermediate |

## Solvent Effects

### Polar Protic Solvents
- Water, alcohols, carboxylic acids
- Can H-bond with nucleophiles
- Stabilize ions (good for SN1)
- Slow down nucleophiles (bad for SN2)

### Polar Aprotic Solvents
- DMSO, DMF, acetone, acetonitrile
- Cannot H-bond with nucleophiles
- Do not stabilize ions as well
- Keep nucleophiles "naked" (good for SN2)

### Solvent Preference Table
| Reaction | Best Solvent Type |
|----------|------------------|
| SN1 | Polar protic |
| SN2 | Polar aprotic |
| E1 | Polar protic |
| E2 | Polar aprotic |
