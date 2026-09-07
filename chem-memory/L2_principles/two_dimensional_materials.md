# Two-Dimensional Materials

## Concept Overview
2D materials are crystalline materials consisting of a single or few atomic layers. Graphene (2004, Nobel Prize 2010: Geim & Novoselov) launched the field.

## Major 2D Material Families

### Graphene and Derivatives
| Material | Properties | Applications |
|---|---|---|
| Graphene | μ > 200,000 cm²/(V·s); 97% transparency; 1 TPa strength | Flexible electronics, composites |
| Graphene oxide (GO) | Insulating, hydrophilic, functionalizable | Membranes, sensors |
| Reduced GO (rGO) | Partially restored conductivity | Supercapacitors, conductive inks |

### Transition Metal Dichalcogenides (TMDs)
| Material | Band Gap | Type | Key Feature |
|---|---|---|---|
| MoS₂ | ~1.8 eV (monolayer) | Direct (1L), Indirect (bulk) | Valleytronics, FETs |
| WS₂ | ~2.0 eV | Direct (1L) | Photoluminescence |
| MoSe₂ | ~1.5 eV | Direct (1L) | Near-IR optoelectronics |
| WSe₂ | ~1.6 eV | Direct (1L) | p-type FETs |
| TiS₂ | ~0 eV (metallic) | Metal | Intercalation electrodes |

### Other 2D Materials
| Family | Example | Band Gap | Notes |
|---|---|---|---|
| Hexagonal BN | h-BN | ~6 eV | Insulator, "white graphene" |
| Black phosphorus | BP (phosphorene) | 0.3–2.0 eV (layer-dependent) | Anisotropic, air-unstable |
| MXenes | Ti₃C₂T_x | Metallic | Batteries, EMI shielding |
| 2D COFs | Various | Tunable | Organic porous 2D polymers |
| 2D MOFs | Various | Tunable | Catalysis, sensing |

## Key Properties of 2D Materials
- **Quantum confinement**: Band gap opens as thickness decreases to monolayer.
- **Surface-to-volume ratio**: Nearly 100% of atoms are surface atoms → high sensitivity.
- **Mechanical**: Graphene: Young's modulus ~1 TPa, breaking strength ~130 GPa.

## Synthesis Methods
| Method | Quality | Scalability | Notes |
|---|---|---|---|
| Mechanical exfoliation | Highest | Low | "Scotch tape" method |
| CVD | High | Medium | Wafer-scale growth possible |
| Liquid exfoliation | Medium | High | Sonication in solvents |
| Molecular beam epitaxy | Highest | Low | Ultra-clean, research |
| Electrochemical exfoliation | Medium | High | Intercalation-based |

## Van der Waals Heterostructures
- Stacking different 2D materials via vdW forces (no lattice matching needed).
- Examples: Graphene/MoS₂ (tunnel junction), MoSe₂/WSe₂ (interlayer exciton).
- Moiré superlattices: Twist angle controls electronic properties.

## Sources
[Source: Wikipedia, Two-dimensional materials]
[Source: Novoselov et al., Science 2004; Wang et al., Nature Nanotechnology 2012]

## L3 Tools
-> `../L3_functions/materials_tools.py` — `band_gap_2d()`, `moire_pattern()`
