# L2 Topic: Synthetic Polymers

**Source**: Organic Chemistry (OpenStax) Ch31
**Created**: 2026-03-13
**Status**: Scaffold (Pass-2)

---

## Concept Overview

Synthetic polymers are man-made macromolecules formed by linking monomer units. They are classified by synthesis method into chain-growth and step-growth polymers.

### Key Features
1. **Chain-growth**: Radical, cationic, anionic mechanisms
2. **Step-growth**: Condensation reactions
3. **Stereochemistry**: Isotactic, syndiotactic, atactic
4. **Properties**: Crystallinity affects strength, flexibility

---

## Core Principles

### 31.1: Chain-Growth Polymers
- Radical: Most general
- Cationic: Requires EDG on monomer
- Anionic: Requires EWG on monomer
- Vinyl monomers (alkenes)

### 31.2: Ziegler-Natta Catalysts
- Stereospecific polymerization
- TiCl4 + AlR3 catalysts
- Control: isotactic, syndiotactic, atactic

### 31.3: Copolymers
- Random, alternating, block, graft
- Tunable properties

### 31.4: Step-Growth Polymers
- Difunctional monomers
- Nylons, polyesters, polyurethanes
- DP = 1/(1-p)

### 31.5-31.6: Olefin Metathesis
- ROMP (ring-opening metathesis)
- Grubbs/Schrock catalysts
- Nobel Prize 2005

### 31.7: Structure-Property
- Tg (glass transition)
- Tm (melting point)
- Crystallinity

---

## Decision Trees

### Polymerization Method Selection
```
Vinyl monomer?
    �?Has EDG? �?Cationic
Has EWG? �?Anionic
Neither? �?Radical
```

### Step-Growth vs Chain-Growth
```
Difunctional monomers? �?Step-growth
Vinyl monomers? �?Chain-growth
```

---

## Key Tables

### Common Polymers
| Polymer | Monomer | Method |
|---------|---------|--------|
| PE | Ethylene | Radical |
| PP | Propylene | Ziegler-Natta |
| PVC | Vinyl chloride | Radical |
| PS | Styrene | Radical/Anionic |
| Nylon 6,6 | Adipic acid + diamine | Step-growth |
| PET | Ethylene glycol + terephthalic acid | Step-growth |

### Stereochemistry
| Type | Arrangement | Properties |
|------|-------------|------------|
| Isotactic | All same side | Crystalline, strong |
| Syndiotactic | Alternating | Moderate |
| Atactic | Random | Amorphous, soft |

---

## Connected Topics

- **Upstream**: [alkene_chemistry.md](alkene_chemistry.md) (vinyl monomers)
- **Upstream**: Carbonyl chemistry (step-growth)
- **Related**: Materials science

---

## L3 Tools

- `../L3_functions/polymer_tools.py` - DP calculations, classification
- `../L3_functions/polymer_chemistry.py` - Carothers equation, Flory distribution, Tg (Fox equation), crystallinity, viscosity
- `../L3_functions/polymer_physics.py` - Chain models, viscoelasticity

---

## L4 References (TODO)

- [ ] Polymer property tables
- [ ] Tg and Tm values
- [ ] Industrial applications

---

## L5 Worked Examples (TODO)

- [ ] DP calculation
- [ ] Polymer classification
- [ ] Stereochemistry prediction


## Implementations

- Implementation: `../L3_functions/polymer_chemistry.py`
