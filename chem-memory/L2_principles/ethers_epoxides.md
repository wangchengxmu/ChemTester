# L2 Topic: Ethers and Epoxides

**Source**: Organic Chemistry (OpenStax) Ch18
**Created**: 2026-03-13
**Status**: Scaffold (Pass-2)

---

## Concept Overview

Ethers (R-O-R') are relatively inert compounds used as solvents. Epoxides (three-membered cyclic ethers) are highly reactive due to ring strain and undergo stereospecific ring-opening reactions.

### Key Features
1. **Ether synthesis**: Williamson, alkoxymercuration
2. **Ether cleavage**: Acidic conditions (HI, HBr)
3. **Epoxide reactivity**: Acid vs base conditions differ
4. **Thiols/sulfides**: Sulfur analogues of alcohols/ethers

---

## Core Principles

### 18.1-18.2: Ethers
- **Williamson synthesis**: Alkoxide + primary alkyl halide
- **Alkoxymercuration**: Markovnikov addition to alkene
- **Properties**: Polar, good solvents, form explosive peroxides

### 18.3: Ether Cleavage
- **SN2** for primary/secondary ethers
- **SN1** for tertiary ethers
- Products: Alkyl halide + alcohol

### 18.4-18.5: Epoxides
- **Preparation**: Peroxyacid or halohydrin cyclization
- **Acid-catalyzed opening**: Attack at more substituted carbon
- **Base-catalyzed opening**: Attack at less substituted carbon
- **trans stereochemistry** in all cases

### 18.6: Crown Ethers
- Cavity size matches specific cations
- Phase-transfer catalysis

### 18.7: Thiols and Sulfides
- Thiols oxidize to disulfides
- Sulfides oxidize to sulfoxides, then sulfones

---

## Decision Trees

### Epoxide Ring-Opening Regiochemistry
```
Epoxide + Nucleophile:
    ↓
Acidic conditions (H+, HX) → Attack at MORE substituted C
    ↓
Basic conditions (OH-, RO-, RNH2, RMgX) → Attack at LESS substituted C
```

### Williamson Ether Synthesis
```
Can I make R-O-R' via Williamson?
    ↓
Check alkyl halide:
- Primary: YES (SN2 works)
- Secondary: Maybe (competing E2)
- Tertiary: NO (elimination only)
```

---

## Key Tables

### Epoxide Opening Regiochemistry
| Epoxide Type | Acidic | Basic |
|--------------|--------|-------|
| Symmetrical | Either C | Either C |
| Unsymmetrical (primary/secondary) | Less substituted | Less substituted |
| Unsymmetrical (with tertiary) | MORE substituted | Less substituted |

### Crown Ether Sizes
| Crown Ether | Cavity (Å) | Cation |
|-------------|------------|--------|
| 12-crown-4 | 1.2 | Li⁺ |
| 15-crown-5 | 1.7 | Na⁺ |
| 18-crown-6 | 2.7 | K⁺ |

---

## Connected Topics

- **Upstream**: [alkyl_halide_reactions.md](alkyl_halide_reactions.md) (SN1/SN2 mechanisms)
- **Upstream**: [alkene_chemistry.md](alkene_chemistry.md) (epoxidation)
- **Downstream**: Carbonyl chemistry (Ch19+)

---

## L3 Tools Required

1. `epoxide_tools.py` - Epoxide ring-opening predictions
2. `ether_tools.py` - Williamson synthesis and cleavage

---

## L4 References (TODO)

- [ ] Epoxide ring strain energies
- [ ] Crown ether cavity sizes
- [ ] Thiol pKa values

---

## L5 Worked Examples (TODO)

- [ ] Epoxide ring-opening product prediction
- [ ] Williamson synthesis feasibility
- [ ] Grignard + epoxide reactions

## L3 Tool Call Directives

**Source:** `epoxide_tools.py`
Epoxide formation, ring-opening, and regiochemistry prediction.

### Available functions:
- `epoxide_ring_opening(epoxide, nucleophile, conditions)` → dict — Predict ring-opening product, attack site, and stereochemistry
- `epoxide_from_alkene(alkene, method)` → dict — Predict epoxide synthesis (peroxyacid/halohydrin methods)
- `predict_regiochemistry(epoxide, conditions)` → dict — Predict which carbon is attacked (SN1-like vs SN2)

### Common errors:
- ❌ Confusing acidic (SN1-like, more substituted) with basic (SN2, less substituted) regiochemistry
- ❌ Forgetting trans stereochemistry in epoxide ring-opening

## L3 Tool Call Directives

**Source:** `epoxide_tools.py`
Epoxide formation, ring-opening, and regiochemistry prediction.

### Available functions:
- `epoxide_ring_opening(epoxide, nucleophile, conditions)` → dict — Predict ring-opening product, attack site, and stereochemistry
- `epoxide_from_alkene(alkene, method)` → dict — Predict epoxide synthesis (peroxyacid/halohydrin methods)
- `predict_regiochemistry(epoxide, conditions)` → dict — Predict which carbon is attacked (SN1-like vs SN2)

### Common errors:
- ❌ Confusing acidic (SN1-like, more substituted) with basic (SN2, less substituted) regiochemistry
- ❌ Forgetting trans stereochemistry in epoxide ring-opening
