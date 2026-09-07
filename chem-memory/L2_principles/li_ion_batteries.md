---
id: li_ion_batteries
layer: 2
title: Li-ion Batteries (Intercalation, SEI, Electrode Materials)
parent: ../L1_ontology/chemistry-core-map.md#entry-270
stability: high
confidence: high
last_verified: 2026-03-24
source: Brown et al. Chemistry: The Central Science Ch20.7, OpenStax Chemistry 2e Ch17.5
---

# Li-ion Batteries

## Core Concept

Li-ion batteries are the dominant rechargeable battery technology, relying on lithium intercalation into host electrode structures. The solid-electrolyte interphase (SEI) is critical for long-term stability.

---

## Operating Principle

### Discharge (Full Cell)
$$\text{Li}_{1-x}\text{CoO}_2 + x\text{LiC}_6 \rightarrow \text{LiCoO}_2 + x\text{C}_6$$

### Anode (Oxidation)
$$x\text{LiC}_6 \rightleftharpoons x\text{Li}^+ + xe^- + x\text{C}_6$$

### Cathode (Reduction)
$$\text{Li}_{1-x}\text{CoO}_2 + x\text{Li}^+ + xe^- \rightleftharpoons \text{LiCoO}_2$$

### Cell Voltage: ~3.7 V

---

## Intercalation Chemistry

Lithium ions insert into layered or framework structures without destroying the host lattice. Key requirement: host structure must be stable over a range of x values.

---

## Cathode Materials

| Material | Voltage (V) | Capacity (mAh/g) | Pros | Cons |
|----------|-------------|-------------------|------|------|
| LiCoO₂ | 3.9 | 140 | High energy | Co toxicity, cost |
| LiFePO₄ | 3.4 | 160 | Safe, cheap, long life | Lower voltage |
| LiMn₂O₄ | 4.0 | 120 | Cheap, safe | Mn dissolution |
| NMC (111) | 3.7 | 160 | Balanced | Cost |
| NCA | 3.6 | 180 | High capacity | Thermal instability |

## Anode Materials

| Material | Capacity (mAh/g) | Notes |
|----------|-------------------|-------|
| Graphite | 372 | Standard, intercalation |
| Si | 4200 | ~10× graphite, huge volume expansion (300%) |
| Li₄Ti₅O₁₂ | 175 | Zero-strain, long cycle life |
| Hard carbon | 300-500 | Na-ion compatible |

---

## Solid Electrolyte Interphase (SEI)

### Formation
During first charge, electrolyte reduction on anode forms a passivating layer:
- Components: LiF, Li₂CO₃, ROLi, ROCO₂Li
- Thickness: 10-100 nm
- Li⁺ conductive, e⁻ insulating

### SEI Trade-offs
- **Good:** prevents further electrolyte decomposition
- **Bad:** consumes Li⁺ (irreversible capacity loss), increases resistance
- **Stability:** decomposes above ~60°C → thermal runaway risk

---

## Energy Density Calculations

### Gravimetric: ~250 Wh/kg (cell level)
### Volumetric: ~650 Wh/L (cell level)

---

## Links

- L3: `../L3_functions/advanced_electrochemistry_tools.py`
- L4: `../L4_reference/electrochemistry_reference.csv`
