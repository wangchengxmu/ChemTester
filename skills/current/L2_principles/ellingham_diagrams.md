# Ellingham Diagrams

[Source: TLP Library I (DoITPoMS), Ch25]

## Core Concept

Ellingham diagrams plot standard Gibbs free energy change (ÃŽÂ”GÃ‚Â°) vs temperature for oxide, sulfide, and other compound formation reactions. They are essential tools in extractive metallurgy for predicting reduction feasibility and selecting reducing agents.

## Key Thermodynamic Relationships

### Linear ÃŽÂ”GÃ‚Â°-T Relationship

For most oxidation reactions:
$$\Delta G^\circ = \Delta H^\circ - T\Delta S^\circ$$

This gives straight lines on Ellingham diagrams with:
- **Slope** = -ÃŽÂ”SÃ‚Â° (usually negative due to OÃ¢Â‚?consumption)
- **Intercept** = ÃŽÂ”HÃ‚Â°

### Equilibrium Oxygen Partial Pressure

$$\Delta G^\circ = RT \ln(p_{O_2}^{eq})$$

Rearranged:
$$p_{O_2}^{eq} = \exp\left(\frac{\Delta G^\circ}{RT}\right)$$

## Reading Ellingham Diagrams

### 1. Relative Stability

Lower lines = more stable oxide (more negative ÃŽÂ”GÃ‚Â°)

### 2. Reduction Feasibility

Element X can reduce oxide MO if:
$$\Delta G^\circ_{MO} > \Delta G^\circ_{XO}$$

### 3. Temperature Scale

Use diagonal scale from origin to read pOÃ¢Â‚?at any temperature.

### 4. CO/COÃ¢Â‚?and HÃ¢Â‚?HÃ¢Â‚Â‚O Ratios

$$p_{O_2} = \left(\frac{p_{CO_2}}{p_{CO}}\right)^2 \cdot K_{eq}$$

## Problem Types

1. **Calculate equilibrium pOÃ¢Â‚?* at given temperature
2. **Determine reduction temperature** for metal oxide with given reductant
3. **Compare oxide stability** between different metals
4. **Select reducing agent** for extraction process
5. **Calculate CO/COÃ¢Â‚?ratio** required for reduction

## Common Ellingham Lines

| Reaction | ÃŽÂ”HÃ‚Â° (kJ/mol) | ÃŽÂ”SÃ‚Â° (J/molÃ‚Â·K) |
|----------|--------------|---------------|
| 2Al + 3/2OÃ¢Â‚?Ã¢Â†?AlÃ¢Â‚Â‚OÃ¢Â‚?| -1676 | -313 |
| 2Fe + OÃ¢Â‚?Ã¢Â†?2FeO | -544 | -133 |
| C + OÃ¢Â‚?Ã¢Â†?COÃ¢Â‚?| -394 | +3 |
| 2C + OÃ¢Â‚?Ã¢Â†?2CO | -221 | +179 |

## Related Topics

- Ã¢Â†?`thermodynamic_equilibrium.md` for ÃŽÂ”GÃ‚Â° fundamentals
- Ã¢Â†?`electrochemistry.md` for related redox concepts


## Implementations

- Implementation: `../L3_functions/ellingham_diagrams.py`

---

## L3 Tool Call Directives

**Source:** ellingham_diagrams.py
Oxide reduction thermodynamics, Ellingham diagram generation, pO? and reducing gas ratios.

### Available functions:
- gibbs_energy_formation(dH, dS, T) ¡ú float ¡ª ¦¤G¡ã = ¦¤H¡ã ? T¦¤S¡ã (J/mol)
- equilibrium_po2(dG, T, R) ¡ú float ¡ª pO? from ¦¤G¡ã = RT ln(pO?) (atm)
- po2_from_gibbs(dG, T, R) ¡ú float ¡ª Alias for equilibrium_po2
- eduction_feasibility(dG_oxide1, dG_oxide2) ¡ú bool ¡ª True if oxide1 can reduce oxide2
- 	emperature_for_po2(dH, dS, pO2_target, R) ¡ú float ¡ª T where equilibrium pO? = target (K)
- co_co2_ratio(dG, T, R) ¡ú float ¡ª CO/CO? ratio for carbon reduction
- h2_h2o_ratio(dG, T, R) ¡ú float ¡ª H?/H?O ratio for hydrogen reduction
- ellingham_line(dH, dS, T_range, n_points) ¡ú list ¡ª (T, ¦¤G¡ã) tuples for diagram
- compare_oxide_stability(dG_values) ¡ú list ¡ª Rank oxides by ¦¤G¡ã (most stable first)
- get_oxide_data(oxide_name) ¡ú dict/None ¡ª ¦¤H¡ã, ¦¤S¡ã for Al?O?, FeO, MgO, SiO?, CO, CO?, etc.

### Common errors:
- ? Inputting ¦¤H/¦¤S in kJ instead of J/mol ¡ª all functions expect J/mol
- ? Forgetting CO line has positive slope (unusual) ¡ª carbon becomes better reductant at high T
