---
id: aquatic_chemistry.expanded
layer: 2
title: Aquatic Chemistry
parent: ../L1_ontology/chemistry-core-map.md#entry-240
stability: high
confidence: high
last_verified: 2026-03-24
source: NCERT Ch14, Sawyer et al. Chemistry for Environmental Engineering, EPA standards
---

# Aquatic Chemistry

## Core Concept

Aquatic chemistry examines chemical species, reactions, and equilibria in water systems, covering water quality, the carbonate system, heavy metals, nutrient pollution, and treatment processes.

---

## Water Quality Parameters

### Dissolved Oxygen (DO)

$$\text{DO}_{sat} = 14.62 - 0.3898T + 0.006969T^2 - 0.00005896T^3 \quad (\text{mg/L, } T \text{ in } Â°\text{C})$$

**DO deficit:** D = DO_sat â DO_actual

### BOD (Biochemical Oxygen Demand)

$$\text{BOD}_t = L_0(1 - e^{-kt})$$

where Lâ = ultimate BOD, k = rate constant (base e), t = time in days

**Standard BODâ:** measured at 20Â°C over 5 days

### COD (Chemical Oxygen Demand)

- Measures total oxidizable matter (including non-biodegradable)
- COD â¥ BOD always (COD includes both biodegradable + refractory organic matter)
- **BOD/COD ratio:** Indicator of biodegradability (>0.6 = readily biodegradable)

### pH and Alkalinity

**pH ranges for natural waters:** 6.5â8.5 (EPA drinking water)

---

## Carbonate System

### Equilibria

$$CO_2(g) \rightleftharpoons CO_2(aq) \quad (H = [CO_2(aq)]/P_{CO_2})$$
$$CO_2(aq) + H_2O \rightleftharpoons H_2CO_3 \quad (K_h)$$
$$H_2CO_3^* \rightleftharpoons H^+ + HCO_3^- \quad (pK_{a1} = 6.35)$$
$$HCO_3^- \rightleftharpoons H^+ + CO_3^{2-} \quad (pK_{a2} = 10.33)$$

### Alkalinity

$$\text{Alkalinity} = [HCO_3^-] + 2[CO_3^{2-}] + [OH^-] - [H^+]$$

### Hardness

$$\text{Hardness} = 2.497[Ca^{2+}] + 4.118[Mg^{2+}] \quad (\text{mg/L as CaCO}_3)$$

- Soft: <60 mg/L; Moderate: 60â120; Hard: 120â180; Very hard: >180

---

## Heavy Metals

### Speciation & Bioavailability

Metal speciation determines toxicity:
- **Free ion (MÂ²âº):** most bioavailable and toxic
- **Complexed (with ligands, organic matter):** less bioavailable
- **Precipitated (as sulfides, hydroxides):** least bioavailable

**Hard-Soft Acid-Base (HSAB) principle applies:** soft metals (HgÂ²âº, CdÂ²âº) bind preferentially to soft ligands (S, organic matter)

### Minamata Disease

- Methylmercury (CHâHgâº) bioaccumulation in fish
- Biomagnification through food chain
- HgÂ²âº â CHâHgâº via microbial methylation in sediments

### EPA Drinking Water Limits

| Metal | MCL (mg/L) | Health Effect |
|-------|-----------|---------------|
| As | 0.010 | Cancer, skin lesions |
| Cd | 0.005 | Kidney damage |
| Cr (total) | 0.100 | Skin irritation |
| Pb | 0.015 | Neurological (children) |
| Hg | 0.002 | Neurological |
| Se | 0.050 | Selenosis |

---

## Eutrophication

**Stages:** Oligotrophic â Mesotrophic â Eutrophic â Hypertrophic

**Causes:** Excess N and P from agriculture runoff, sewage

**Chlorophyll-a thresholds:** Oligotrophic (<2.7 Î¼g/L), Eutrophic (>7.3 Î¼g/L)

**Consequences:** Algal blooms â DO depletion â fish kills â dead zones

---

## Water Treatment

### Coagulation-Flocculation
- **Coagulants:** Alum (Alâ(SOâ)â), FeClâ, PACl
- Destabilize colloids via charge neutralization, sweep flocculation
- pH optimum: 5.5â7.5 (alum)

### Disinfection
- **Chlorination:** HOCl (pH < 7.5, more effective) vs OClâ» (pH > 7.5)
- **Ozonation:** Oâ, stronger oxidant, no THM formation
- **UV:** 254 nm, inactivation via DNA damage

### Activated Carbon
- Adsorption of organics, taste/odor compounds
- Isotherms: Langmuir, Freundlich

---

## Key Equations

| Equation | Use |
|----------|-----|
| DO saturation (empirical) | Water quality assessment |
| BODâ = Lâ(1âeâ»áµáµ) | Pollution loading |
| Henderson-Hasselbalch (carbonate) | pH speciation |
| Hardness calculation | Water classification |

---

## L3 Tools
â `../L3_functions/environmental_tools.py` â `bod_calc()`, `henry_law_volatilization()`
## L4 Data
â `../L4_reference/environmental_data.csv` â EPA limits, water quality standards
## L5 Examples
â `../L5_examples/environmental_examples.md` â Worked examples

---

## Source Attribution: Brown et al., Chemistry: The Central Science, Ch18.5-18.6 (LibreTexts)
[Source: Brown et al., Ch18: Chemistry of the Environment](https://chem.libretexts.org/Bookshelves/General_Chemistry/Map%3A_Chemistry_-_The_Central_Science_(Brown_et_al.)/18%3A_Chemistry_of_the_Environment)

- Water is the most important resource. From a chemical perspective, pure water is a compound, but natural water contains dissolved gases, minerals, organic and inorganic substances.
- **Section 18.5: The World Ocean** ¡ª covers composition and chemistry of seawater.
- **Section 18.6: Fresh Water** ¡ª essential electrolytes (ions) dissolved in natural water; these ionize and conduct electricity.
