# Photoredox Catalysis

## Concept Overview

Photoredox catalysis uses light-absorbing catalysts to generate reactive radical intermediates under mild conditions, enabling transformations inaccessible by thermal methods.

## Key Principles

### Common Photocatalysts
| Catalyst | E₁/₂(PC*/PC⁻) (V vs SCE) | E₁/₂(PC⁺/PC*) (V vs SCE) | τ (ns) |
|----------|--------------------------|--------------------------|--------|
| Ru(bpy)₃²⁺ | -0.81 | +0.77 | ~1100 |
| Ir(ppy)₃ | -1.73 | +0.31 | ~1900 |
| Eosin Y | -1.10 | +0.83 | ~1.7 |
| 4CzIPN | -1.21 | +1.35 | ~2400 |

### Quenching Cycles
**Oxidative quenching:**
```
PC + hv → PC*
PC* + Substrate → PC⁺ + Substrate⁻
PC⁺ + Sacrificial reductant → PC
```

**Reductive quenching:**
```
PC + hv → PC*
PC* + Electron donor → PC⁻
PC⁻ + Substrate → PC + Substrate⁻
```

### Dual Catalysis
Combines photoredox with Ni, Cu, or organocatalysis:
- Photoredox-Ni: C(sp²)–C(sp³) cross-coupling
- Photoredox-organocatalysis: α-amination, alkylation

### Key Reactions
- C-H functionalization
- Decarboxylative coupling
- Atom transfer radical addition (ATRA)
- Hydrodefunctionalization

## Problem-Solving Routes

1. **Select catalyst**: Match redox potentials to substrate
2. **Determine quenching mechanism**: Compare donor/acceptor potentials to PC* redox potentials
3. **Design dual catalytic cycle**: Ensure compatibility of intermediates between catalytic cycles

## Links

- **L3 Tools**: `../L3_functions/photochemistry_tools.py`
- **L4 Data**: `../L4_reference/photochemistry_data.csv`
- **L5 Examples**: `../L5_examples/photochemistry_examples.md`
