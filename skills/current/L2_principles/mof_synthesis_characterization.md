# L2 Topic: MOF Synthesis & Characterization

**Source**: Expert knowledge; Furukawa et al., Chem. Rev. 2013
**Created**: 2026-03-24
**Status**: Pass-1

---

## Synthesis Methods

| Method | Conditions | Pros | Cons |
|--------|-----------|------|------|
| **Solvothermal** | Metal salt + linker in DMF/DEF, 80-220°C, autogenous pressure | High crystallinity, scalable | Long reaction times (hours-days), toxic solvents |
| **Microwave** | Same reagents, microwave heating | Minutes, better nucleation control | Equipment cost, limited scale |
| **Mechanochemical** | Ball milling, LAG (liquid-assisted grinding) | Green, room temp, fast | Poor crystallinity for some systems |
| **Modulator (CTF)** | Competing monocarboxylic acid (acetic, formic) as modulator | Crystal size control, defect engineering | Additional purification |
| **Electrochemical** | Metal anode dissolution in linker solution | Continuous, no metal salt needed | Limited to conductive substrates |
| **Layer-by-layer** | Sequential deposition of metal and linker on substrate | Thin films, controlled thickness | Very slow |

### Modulator Method Detail
Competitive coordination of modulator (e.g., acetic acid) vs. multidentate linker controls nucleation rate. Higher [modulator]/[linker] ratio → larger crystals, more missing-linker defects.

---

## Characterization Techniques

| Technique | Information | Notes |
|-----------|------------|-------|
| **PXRD** | Phase identification, crystallinity | Simulated vs. experimental pattern match |
| **Single crystal XRD** | Full 3D structure | Requires crystals >10 μm |
| **N₂ adsorption (77 K)** | BET surface area, pore size distribution (NLDFT/BET) | Type I isotherm for microporous |
| **CO₂ adsorption (273 K)** | Ultra-micropore analysis | Better for pores <7 Å |
| **TGA** | Thermal stability, solvent content | Activation protocol validation |
| **SEM/TEM** | Crystal morphology, size | |
| **FT-IR** | Linker coordination (ν(C=O) shift ~1600→1650 cm⁻¹) | Open vs. coordinated carboxylate |
| **¹H/¹³C NMR** (digested) | Linker integrity, defect quantification | Digest in DCl/DMSO-d₆ |
| **XPS** | Metal oxidation state | Zr⁴⁺ confirmation in UiO-66 |

### BET Surface Area Analysis
- Relative pressure range: P/P₀ = 0.05–0.30
- Rouquerol criteria for microporous materials
- Typical: MOF-5 ~3800 m²/g, UiO-66 ~1200 m²/g, HKUST-1 ~1500-1850 m²/g

---

## L3 Tools
- `../L3_functions/mof_tools.py` → `surface_area_bet()`, `pore_volume_calc()`

## L3 Tool Call Directives

**Source:** mof_tools.py
MOF/COF computational tools for surface area, porosity, gas uptake, and topology analysis.

### Available functions:
- surface_area_bet(n_adsorbed, p_relative, cross_section) → dict — Calculate BET surface area from adsorption isotherm data.
- pore_volume_calc(n_adsorbed_sat, molar_volume) → float — Calculate total pore volume from adsorption at saturation (P/P0 ~ 0.99).
- gas_uptake_prediction(surface_area, pressure, temperature, gas, isosteric_heat) → dict — Estimate gas uptake using simplified Langmuir model.
- topology_analysis(connectivity_node, connectivity_linker) → dict — Predict net topology from node and linker connectivity.
- framework_density_calc(molar_mass, unit_cell_volume, z) → dict — Calculate crystal framework density.

### Common errors:
- ❌ Passing wrong parameter types or missing required arguments
