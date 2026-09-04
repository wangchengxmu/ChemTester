# L2 Topic: MOF Applications

**Source**: Expert knowledge; Li et al., Chem. Rev. 2016; Furukawa et al., Science 2013
**Created**: 2026-03-24
**Status**: Pass-1

---

## Gas Storage

| Gas | Target (DOE) | Best MOFs | Mechanism |
|-----|-------------|-----------|-----------|
| H₂ | 6.5 wt% @ 77 K, 100 bar | MOF-210, NU-100 | Cryogenic physisorption |
| CH₄ | 0.5 g/g @ 298 K, 65 bar | HKUST-1, MOF-5 | Room-temperature adsorption |
| CO₂ | 0.5 g/g @ 298 K, 40 bar | Mg-MOF-74, UTSA-16 | Open metal sites, amine functionalization |

### Gravimetric vs. Volumetric
- Gravimetric (wt%): favors low-density frameworks
- Volumetric (g/cm³ or v/v): favors high-density frameworks
- Tradeoff: crystal density vs. surface area

---

## Separation

| Type | Example | Principle |
|------|---------|-----------|
| CO₂/N₂ | UiO-66-NH₂, Mg-MOF-74 | Quadrupole interaction / amine affinity |
| C₂H₂/C₂H₄ | NOTT-300, SIFSIX | Size exclusion / H-bond |
| Xe/Kr | NiTPy, SBMOF-1 | Framework pore size matching |
| Propylene/propane | KAUST-7 | Thermodynamic equilibrium separation |
| Chiral | POST-1, D-POST-1 | Enantioselective pore environment |

---

## Catalysis

| Type | Mechanism | Example |
|------|-----------|---------|
| Lewis acid | Open metal sites (Zr⁴⁺, Cu²⁺, Cr³⁺) | UiO-66: Knoevenagel condensation; HKUST-1: aldol |
| Redox | Redox-active metal or linker | MIL-101(Fe): Fenton-like oxidation |
| Photocatalysis | Semiconductor-like band gap | NH₂-MIL-125(Ti): CO₂ reduction |
| Enzyme mimetic | Zr-OH₂ nodes as phosphatase | NU-1000: nerve agent hydrolysis |
| Bifunctional | Acid + base sites | Zr-MOFs: one-pot cascade reactions |

---

## Other Applications

- **Drug delivery**: MIL-100/101 for ibuprofen, cisplatin (high loading, pH-triggered release)
- **Sensors**: Luminescent MOFs (LMOFs) for VOC, explosives, metal ion detection
- **Water harvesting**: MOF-801 (Zr-fumarate) → 2.8 L water/kg/day at 20% RH in desert conditions (Yaghi, Science 2017)
- **Conductivity**: 2D MOFs (Cu-BHT) → 1580 S/cm metallic conductivity
- **Iodine capture**: Ag₀.₂₅@HKUST-1, ZIF-8 for nuclear waste

---

## Biomedical Applications (enhanced from PMC7826725)

### Drug Delivery
- High loading capacity due to large surface area and pore volume
- Controlled release via pH-responsive, stimuli-responsive frameworks
- Examples: MIL-100/101 for ibuprofen/cisplatin delivery
- Bio-MOF-1: hosts Me₂NH₂⁺ cations, retains crystallinity during drug loading/release

### Antimicrobial/Antibiotic Delivery
- MOFs as carriers for antibiotics (ciprofloxacin, tetracycline)
- Synergistic effects: MOF framework + drug (e.g., Ag-MOFs for antibacterial activity)
- Controlled release prevents antibiotic resistance development

### Biocompatibility Considerations
- Toxicity depends on metal ion leaching (Zn, Fe, Zr generally biocompatible)
- Degradation products must be non-toxic
- Size-dependent: nano-MOFs (<200 nm) for systemic delivery; larger for local implants

### Sensing Applications
- Luminescent MOFs (LMOFs) for detection of VOCs, explosives, metal ions, biomolecules
- Electrochemical MOF sensors for neurotransmitters, glucose, pathogens

## Energy Storage (enhanced)

### Li-ion and Na-ion Batteries
- MOFs as electrode materials or precursors for porous carbon/metal oxide composites
- Conductive MOFs (2D Cu-BHT: 1580 S/cm) for supercapacitors
- MOF-derived carbons for high-performance anodes

### Electrocatalysis
- MOF-derived catalysts: ORR, OER, HER
- Single-atom catalysts from MOF pyrolysis (M-N-C materials)

## L3 Tools
- `../L3_functions/mof_tools.py` → `gas_uptake_prediction()`
