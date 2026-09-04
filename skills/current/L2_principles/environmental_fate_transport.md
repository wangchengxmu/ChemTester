---
id: environmental_fate_transport.expanded
layer: 2
title: Environmental Fate & Transport
parent: ../L1_ontology/chemistry-core-map.md#entry-242
stability: high
confidence: high
last_verified: 2026-03-24
source: Mackay Multimedia Environmental Models, Schwarzenbach Environmental Organic Chemistry, EPA
---

# Environmental Fate & Transport

## Core Concept

Environmental fate and transport describes how chemicals distribute, transform, and move through environmental compartments (air, water, soil, biota), governed by partition coefficients, degradation rates, and bioaccumulation factors.

---

## Partition Coefficients

### Octanol-Water (Kow)
$$K_{ow} = \frac{C_{octanol}}{C_{water}}$$
$$\log K_{ow} = \log P$$

**Interpretation:**
- log P < 0: highly hydrophilic
- log P 0–3: moderate; log P 3–5: hydrophobic; log P > 5: very hydrophobic

### Organic Carbon-Water (Koc)
$$K_{oc} = \frac{K_d}{f_{oc}}$$

**Estimation from log Kow:**
$$\log K_{oc} = 0.81 \log K_{ow} + 0.10 \quad \text{(Karickhoff, 1981)}$$

### Soil-Water (Kd)
$$K_d = f_{oc} \times K_{oc} = f_{oc} \times 0.63 \times K_{ow}$$

### Air-Water: Henry's Law
$$K_H = \frac{P}{C_w} \quad (\text{atm·L/mol})$$
$$H' = \frac{C_{air}}{C_{water}} \quad (\text{dimensionless})$$

---

## Bioaccumulation

### Bioconcentration Factor (BCF)
$$BCF = \frac{C_{organism}}{C_{water}}$$

**Estimation:** $\log BCF = 0.85 \log K_{ow} - 0.70$ (for fish, moderate lipids)

### Biomagnification
- Trophic transfer increases concentration up the food chain
- **Trophic Magnification Factor (TMF):** ratio per trophic level
- Classic example: DDT, PCBs, methylmercury

### BSAF (Biota-Sediment Accumulation Factor)
$$BSAF = \frac{C_{biota}}{C_{sediment}}$$

---

## Degradation Pathways

### Hydrolysis
- SN1/SN2 mechanisms for alkyl halides, esters, amides
- pH-dependent: acid-catalyzed (pH < 5), base-catalyzed (pH > 8), neutral

### Photolysis
- **Direct:** chemical absorbs UV/visible light
- **Indirect (photosensitized):** reactive intermediates (·OH, ¹O₂) from DOM, NO₃⁻
- Rate: depends on light absorption spectrum, quantum yield, sunlight intensity

### Biodegradation
- **Primary biodegradation:** structural change only
- **Ultimate biodegradation:** complete mineralization to CO₂, H₂O, inorganics
- **Half-lives:** aerobic (hours–months), anaerobic (months–years)
- **Ready biodegradability (OECD 301):** >60% ThOD removal in 28 days

---

## Persistence, Bioaccumulation, Toxicity (PBT) Assessment

### Persistence Criteria (EU REACH / EPA)
| Metric | Persistent (P) | Very Persistent (vP) |
|--------|----------------|---------------------|
| Marine water half-life | >60 days | >180 days |
| Freshwater/sediment half-life | >40 days | >120 days |
| Soil half-life | >120 days | >180 days |

### Bioaccumulation Criteria
| Metric | Bioaccumulative (B) | Very Bioaccumulative (vB) |
|--------|--------------------|-----------------------|
| BCF | >2000 | >5000 |
| log Kow | >4.5 | >5.0 |

### Toxicity Criterion
- T: CMR (carcinogenic, mutagenic, reproductive toxicant), or chronic NOEC < 0.01 mg/L

---

## Environmental Risk Assessment

$$\text{Risk Quotient (RQ)} = \frac{PEC}{PNEC}$$

- **PEC** = Predicted Environmental Concentration
- **PNEC** = Predicted No-Effect Concentration
- RQ < 1: acceptable risk; RQ > 1: potential concern

**PNEC estimation:** $PNEC = \frac{LC_{50} \text{ or } EC_{50}}{AF}$ (AF = assessment factor, 10–1000)

---

## Multimedia Models (Fugacity)

$$f_i = \frac{C_i}{Z_i}$$

Level I: equilibrium partitioning; Level II: steady-state with reactions; Level III: inter-compartment transfer

---

## Key Equations

| Equation | Use |
|----------|-----|
| log Koc = 0.81·log Kow + 0.10 | Estimate soil sorption |
| log BCF = 0.85·log Kow − 0.70 | Estimate bioaccumulation |
| RQ = PEC/PNEC | Risk screening |
| Fugacity: f = C/Z | Multimedia distribution |

---

## L3 Tools
→ `../L3_functions/environmental_tools.py` — `partition_coefficient()`
## L4 Data
→ `../L4_reference/environmental_data.csv`
## L5 Examples
→ `../L5_examples/environmental_examples.md`
