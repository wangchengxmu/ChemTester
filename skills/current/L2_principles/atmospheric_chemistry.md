---
id: atmospheric_chemistry.expanded
layer: 2
title: Atmospheric Chemistry
parent: ../L1_ontology/chemistry-core-map.md#entry-239
stability: high
confidence: high
last_verified: 2026-03-24
source: NCERT Ch14, LibreTexts Environmental Chemistry, IPCC AR6
---

# Atmospheric Chemistry

## Core Concept

Atmospheric chemistry studies the chemical composition, reactions, and processes occurring in Earth's atmosphere, including ozone formation/depletion, air pollution, greenhouse gas dynamics, and aerosol-climate interactions.

---

## Earth's Atmosphere Composition

| Layer | Altitude (km) | Key Characteristics |
|-------|--------------|---------------------|
| Troposphere | 0â12 | Weather, temperature decrease with altitude |
| Stratosphere | 12â50 | Ozone layer (15â35 km), temperature inversion |
| Mesosphere | 50â85 | Meteor ablation |
| Thermosphere | 85â600+ | Ionosphere, auroras |

**Major constituents (dry air):** Nâ (78.1%), Oâ (20.9%), Ar (0.93%), COâ (~0.042% or 420 ppm)

**Trace gases:** CHâ (~1.9 ppm), NâO (~0.33 ppm), Oâ (variable, 0.01â10 ppm)

---

## Stratospheric Ozone

### Chapman Mechanism (1930)

The natural cycle of ozone formation and destruction:

1. **Oâ photolysis:** Oâ + hÎ½ (Î» < 240 nm) â 2O
2. **Oâ formation:** O + Oâ + M â Oâ + M
3. **Oâ photolysis:** Oâ + hÎ½ (Î» < 320 nm) â O + Oâ
4. **Oâ destruction:** O + Oâ â 2Oâ

**Steady-state approximation:**
$$[O_3] \propto \sqrt{[O_2]} \cdot \left(\frac{k_1 J_1}{k_4}\right)^{1/2}$$

### Catalytic Ozone Destruction by CFCs

CFCs (e.g., CClâFâ) are photolyzed in the stratosphere:

$$CCl_2F_2 + hÎ½ â CClF_2 + Cl$$

**Catalytic cycle (Cl atoms):**
$$Cl + O_3 â ClO + O_2$$
$$ClO + O â Cl + O_2$$

Net: Oâ + O â 2Oâ (each Cl atom destroys ~100,000 Oâ molecules)

**Ozone Depletion Potential (ODP):** CFC-11 = 1.0 (reference), HCFCs ~0.02â0.05, HFCs = 0

### Montreal Protocol (1987)

- Phased out CFCs, halons, carbon tetrachloride
- Amended to cover HCFCs (developing countries: 2040 phaseout)
- **Result:** Ozone layer recovering; projected 2066 (Antarctic) return to 1980 levels

---

## Tropospheric Chemistry & Smog

### NOâ Cycle

$$NO_2 + hÎ½ (Î» < 420 nm) â NO + O$$
$$O + O_2 + M â O_3 + M$$
$$O_3 + NO â NO_2 + O_2$$

**VOC oxidation generates peroxy radicals:**
$$RO_2 + NO â NO_2 + RO$$

### Photochemical Smog

**Key products:** Oâ (ground-level), PAN (peroxyacetyl nitrate), aldehydes, HNOâ

**PAN formation:**
$$CH_3CHO + OH + O_2 â CH_3C(O)O_2 + H_2O$$
$$CH_3C(O)O_2 + NO_2 â CH_3C(O)O_2NO_2 \text{ (PAN)}$$

**Criteria pollutants (EPA):** Oâ, CO, NOâ, SOâ, PMââ, PMâ.â, Pb

---

## Greenhouse Gases & Radiative Forcing

### Major GHGs

| Gas | Pre-industrial (ppm/ppb) | 2020 | Lifetime (yr) | GWPâââ |
|-----|--------------------------|------|---------------|---------|
| COâ | 278 ppm | 421 ppm | 300â1000 | 1 |
| CHâ | 722 ppb | 1866 ppb | ~12 | 27.9 |
| NâO | 270 ppb | 332 ppb | 109 | 273 |

### Radiative Forcing

$$\Delta F = \alpha \ln\left(\frac{C}{C_0}\right)$$

where Î± = 5.35 WÂ·mâ»Â² for COâ, Câ = pre-industrial concentration

**Climate sensitivity:** ÎT = Î» Ã ÎF, where Î» â 0.8 K/(WÂ·mâ»Â²)

### Aerosols

**Scattering (cooling):** sulfate (SOâÂ²â» from SOâ), nitrate, organic carbon
**Absorbing (warming):** black carbon (soot), brown carbon
**Net aerosol effect:** -0.5 to -1.5 WÂ·mâ»Â² (significant uncertainty, net cooling)

---

## Key Equations Summary

| Equation | Use |
|----------|-----|
| Beer-Lambert: $I = I_0 e^{-\epsilon c l}$ | Atmospheric absorption/attenuation |
| Chapman steady-state | Ozone concentration prediction |
| Radiative forcing (COâ) | Climate impact calculation |
| GWP | Relative GHG impact comparison |

---

## L3 Tools
â `../L3_functions/environmental_tools.py` â `greenhouse_forcing()`
## L4 Data
â `../L4_reference/environmental_data.csv` â GHG lifetimes, GWP values
## L5 Examples
â `../L5_examples/environmental_examples.md` â Worked examples

---

## Source Attribution: Brown et al., Chemistry: The Central Science, Ch18.3 (LibreTexts)
[Source: Brown et al., Chemistry: The Central Science, 18.3: Ozone in the Upper Atmosphere](https://chem.libretexts.org/Bookshelves/General_Chemistry/Map%3A_Chemistry_-_The_Central_Science_(Brown_et_al.)/18%3A_Chemistry_of_the_Environment/18.03%3A_Ozone_in_the_Upper_Atmostphere)

### Ozone Layer Chemistry
- **Ozone formation**: O? + h¦Í ¡ú 2O; O? + O + M ¡ú O? + M* (requires third body M)
- **Ozone destruction**: O? + h¦Í ¡ú O? + O; O? + O ¡ú 2O?
- **Dynamic equilibrium**: 3O? ? 2O? (¦¤H = 286 kJ for 3O? ¡ú 2O?)
- **Ozone bond energy**: Average O-O bond in O? ¡Ö 445 kJ/mol (vs. O=O in O? = 498 kJ/mol)
- **Dobson Unit (DU)**: 0.01 mm thickness of ozone at STP; 100 DU = 1 mm

### UV Radiation Categories
- UV-A: 400¨C320 nm (vitamin D synthesis; photoaging at high doses)
- UV-B: 320¨C280 nm (absorbed by ozone; most damaging to DNA)
- UV-C: <280 nm (strongly absorbed by ozone; very little reaches surface)

### CFC Ozone Depletion Mechanism
- **CFC naming**: First digit = C-1; second = H+1; third = F-1. E.g., CFC-12 = CF?Cl?
- **Catalytic cycle**: Cl + O? ¡ú ClO + O?; ClO + O ¡ú Cl + O?; Net: 2O? ¡ú 3O?
- **Polar ozone hole**: At 190 K, ice crystals catalyze HCl + ClONO? ¡ú HNO? + Cl?; Cl? photolyzed to Cl radicals.
- **Montreal Protocol (1987)**: 149 nations agreed to phase out CFCs.

### Quantitative Example: O=O Bond Photodissociation
- O=O bond energy = 498 kJ/mol ¡ú photon wavelength = hc/E = 240 nm (UV-C region)
- Confirms visible light (300¨C700 nm) cannot break O=O bond; UV required.
