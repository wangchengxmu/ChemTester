# Perovskite Materials

## Concept Overview
Perovskites are materials with the general formula ABX₃, where A and B are cations and X is an anion. Named after the mineral CaTiO₃ (discovered by Gustav Rose, 1839; named after Lev Perovski).

## Crystal Structure
- **Ideal perovskite**: Cubic, space group Pm3̄m.
- **Tolerance factor**: t = (r_A + r_X) / [√2(r_B + r_X)]
  - t ≈ 1.0: Ideal cubic
  - 0.9 < t < 1.0: Orthorhombic/tetragonal distortions
  - t < 0.9: Different structure (e.g., ilmenite)

## Types of Perovskites

### Halide Perovskites (Solar Cells)
| Formula | Band Gap (eV) | PCE Record | Notes |
|---|---|---|---|
| MAPbI₃ | ~1.55 | ~25% | Methylammonium lead iodide |
| FAPbI₃ | ~1.48 | ~26%+ | Formamidinium; most efficient |
| CsPbI₃ | ~1.73 | ~20% | All-inorganic, more stable |
| (MA,FA,Cs)Pb(I,Br)₃ | Tunable | ~26.1% (2024) | Triple-cation perovskite |

- Key advantages: High absorption coefficient, long carrier diffusion lengths, solution processable.
- Challenges: Stability (moisture, heat, light), Pb toxicity.
- Charge transport: μ_e ~ 10–100 cm²/(V·s); μ_h ~ 5–50 cm²/(V·s).

### Oxide Perovskites (Functional Materials)
| Material | Key Property | Application |
|---|---|---|
| BaTiO₃ | Ferroelectric (T_C ≈ 120°C) | Capacitors, piezoelectrics |
| SrTiO₃ | Quantum paraelectric, substrate | Epitaxial films |
| LaAlO₃/SrTiO₃ | 2D electron gas | Oxide electronics |
| YBa₂Cu₃O₇ (YBCO) | Superconductor (T_C = 93 K) | High-T_c superconductors |
| CH₃NH₃PbI₃ | Semiconductor | Solar cells |

### Double Perovskites
- A₂BB'X₆ structure; useful for lead-free alternatives (e.g., Cs₂AgBiBr₆).

## Synthesis Methods
- Solution processing: spin-coating, inkjet printing, slot-die coating.
- Vapor deposition: thermal evaporation (better uniformity).
- Single crystal growth: inverse temperature crystallization, Bridgman method.

## Sources
[Source: Wikipedia, Perovskite]
[Source: Kojima et al., J. Am. Chem. Soc. 2009 (first perovskite solar cell)]

## L3 Tools
-> `../L3_functions/materials_tools.py` — `tolerance_factor()`, `perovskite_stability()`
