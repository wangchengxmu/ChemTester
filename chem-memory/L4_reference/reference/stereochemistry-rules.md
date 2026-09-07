# Stereochemistry Reference
[Source: Organic Chemistry OpenStax, Ch05]

## Cahn-Ingold-Prelog Priority Rules

### Rule 1: Atomic Number
Higher atomic number = higher priority

| Element | Atomic Number | Priority |
|---------|---------------|----------|
| I | 53 | 1 (highest) |
| Br | 35 | 2 |
| Cl | 17 | 3 |
| S | 16 | 4 |
| F | 9 | 5 |
| O | 8 | 6 |
| N | 7 | 7 |
| C | 6 | 8 |
| H | 1 | 9 (lowest) |

### Rule 2: Isotopes
Higher mass = higher priority

| Isotope | Mass | Priority |
|---------|------|----------|
| T (³H) | 3 | Highest |
| D (²H) | 2 | Middle |
| H (¹H) | 1 | Lowest |

### Rule 3: Extended Comparison
If first atoms are identical, compare the next atoms outward

| Group | First Atom | Next Atoms | Priority |
|-------|------------|------------|----------|
| -CH₃ | C | H,H,H | Lower |
| -CH₂OH | C | O,H,H | Higher |
| -CH₂NH₂ | C | N,H,H | Middle |

### Rule 4: Multiple Bonds
Count each multiple bond as multiple single bonds

| Group | Equivalent | Priority Calculation |
|-------|------------|---------------------|
| -CHO | C bonded to O,O,H | High |
| -CH=O | Same as above | Same |
| -C≡N | C bonded to N,N,N | Very high |

## R/S Assignment Procedure

```
Step 1: Identify chiral center (4 different groups)
Step 2: Assign priorities 1-4 (CIP rules)
Step 3: Orient molecule with group 4 pointing AWAY
Step 4: Trace path 1 → 2 → 3
    │
    ├─ Clockwise → R (rectus, "right")
    └─ Counterclockwise → S (sinister, "left")
```

## Common Chiral Molecules

### Naturally Occurring
| Molecule | Configuration | [α]D | Notes |
|----------|---------------|------|-------|
| L-Alanine | S | +14.7° | Protein amino acid |
| L-Lactic acid | S | +3.8° | Muscle metabolism |
| D-Glucose | Multiple | +52.7° | Blood sugar |
| L-Sucrose | Multiple | +66.5° | Table sugar |

### Pharmaceutical Examples
| Drug | Active Enantiomer | Other Enantiomer |
|------|-------------------|------------------|
| Ibuprofen | S (anti-inflammatory) | R (converts to S) |
| Thalidomide | R (sedative) | S (teratogenic) |
| Albuterol | R (bronchodilator) | S (pro-inflammatory) |
| Naproxen | S (anti-inflammatory) | R (liver toxin) |
| Escitalopram | S (antidepressant) | R (less active) |

## Stereoisomer Relationships

### Types of Isomers
```
Isomers
├── Constitutional (structural)
│   └── Different connectivity
└── Stereoisomers
    ├── Enantiomers
    │   └── Mirror images, non-superimposable
    └── Diastereomers
        ├── Not mirror images
        ├── E/Z (alkene) isomers
        └── Compounds with multiple chiral centers
```

### Comparison Table
| Property | Enantiomers | Diastereomers |
|----------|-------------|---------------|
| Mirror images | Yes | No |
| Superimposable | No | No |
| Same connectivity | Yes | Yes |
| Same physical properties | Yes* | No |
| Same chemical properties | Yes* | No |
| *Except optical rotation | Opposite signs | Different |

## Optical Activity

### Specific Rotation Formula
```
[α] = α / (c × l)

Where:
[α] = specific rotation (°)
α = observed rotation (°)
c = concentration (g/mL)
l = path length (dm)
```

### Sign Convention
| Sign | Name | Rotation Direction |
|------|------|-------------------|
| (+) | Dextrorotatory | Clockwise |
| (-) | Levorotatory | Counterclockwise |
| (±) | Racemic | No net rotation |

## Maximum Number of Stereoisomers

### Formula
Maximum = 2ⁿ where n = number of chiral centers

### Examples
| Chiral Centers | Maximum Stereoisomers | Example |
|----------------|----------------------|---------|
| 1 | 2 | Lactic acid |
| 2 | 4 | Tartaric acid (3 actual, 1 meso) |
| 3 | 8 | Aldotriose |
| 4 | 16 | Aldotetrose |
| n | 2ⁿ | - |

## Meso Compounds

### Definition
Achiral compound with chiral centers (internal plane of symmetry)

### Example: 2,3-Butanediol
| Isomer | Configuration | Optical Activity |
|--------|---------------|------------------|
| (2R,3R) | R,R | Active (+) |
| (2S,3S) | S,S | Active (-) |
| (2R,3S) = (2S,3R) | meso | Inactive |

### Identifying Meso Compounds
1. Multiple chiral centers present
2. Internal plane of symmetry exists
3. Two chiral centers with opposite configurations
4. Overall molecule is achiral

## Resolution Methods

### 1. Diastereomeric Salt Formation
- React racemic mixture with chiral resolving agent
- Form diastereomeric salts with different properties
- Separate by crystallization

### 2. Chromatography
- Use chiral stationary phase
- Enantiomers have different retention times
- High purity separation possible

### 3. Enzymatic Resolution
- Enzymes are chiral catalysts
- React selectively with one enantiomer
- Often kinetic resolution

### 4. Kinetic Resolution
- Chiral reagent/catalyst
- Different reaction rates for enantiomers
- Maximum 50% yield of each

## Prochirality

### Definitions
| Term | Definition |
|------|------------|
| Prochiral | Can become chiral by one change |
| Pro-R | Group that would become R if prioritized |
| Pro-S | Group that would become S if prioritized |
| Re face | Clockwise priority order |
| Si face | Counterclockwise priority order |

### Example: Ethanol
- CH₃-CH₂-OH has prochiral CH₂
- Two H atoms are enantiotopic
- Oxidation to acetaldehyde creates chiral aldehyde
