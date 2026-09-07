---
id: supercapacitors
layer: 2
title: Supercapacitors (EDLC, Pseudocapacitance)
parent: ../L1_ontology/chemistry-core-map.md#entry-272
stability: high
confidence: high
last_verified: 2026-03-24
source: Brown et al. Chemistry: The Central Science, electrochemistry literature
---

# Supercapacitors

## Core Concept

Supercapacitors (electrochemical capacitors) bridge the gap between conventional capacitors and batteries, offering high power density (>10 kW/kg) with moderate energy density (5-10 Wh/kg).

---

## Energy Storage Mechanisms

### 1. Electric Double Layer Capacitance (EDLC)
- Non-Faradaic: charge separation at electrode-electrolyte interface
- No electron transfer, purely electrostatic
- **Helmholtz model:** C = εε₀A/d (parallel plate)
- **Stern model:** Helmholtz + diffuse layer (Gouy-Chapman)
- **Typical C:** 10-30 μF/cm² for smooth electrodes
- **Materials:** activated carbon (SSA > 2000 m²/g), graphene, CNTs

### 2. Pseudocapacitance
- Faradaic: fast, reversible redox reactions at/near surface
- Surface-confined, not diffusion-limited
- **Types:**
  - Underpotential deposition (e.g., Pb on Au)
  - Redox pseudocapacitance (e.g., RuO₂, MnO₂, conducting polymers)
  - Intercalation pseudocapacitance (e.g., Nb₂O₅)
- **Typical C:** 200-2000 μF/cm²

---

## Energy & Power

$$E = \frac{1}{2}CV^2$$

$$P = \frac{V^2}{4R}$$

Where C = capacitance, V = voltage window, R = ESR (equivalent series resistance).

---

## Performance Comparison

| Metric | Supercapacitor | Battery | Conventional Capacitor |
|--------|---------------|---------|----------------------|
| Energy density | 5-10 Wh/kg | 100-250 Wh/kg | 0.01-0.05 Wh/kg |
| Power density | 10-15 kW/kg | 0.1-2 kW/kg | >100 kW/kg |
| Cycle life | >10⁶ | 500-5000 | >10⁶ |
| Charge time | seconds | hours | microseconds |
| Voltage (cell) | 2.7-3.0 V | 3.0-4.2 V | hundreds |

---

## Ragone Plot
Energy density (y-axis) vs power density (x-axis) — supercapacitors occupy the high-power, low-energy region.

---

## Source Context & Cross-References
- No dedicated supercapacitor chapter found on LibreTexts (emerging technology topic)
- Related LibreTexts content: Brown et al. Ch20.7 (batteries/fuel cells), OpenStax Ch17.5
- Cross-reference: `battery_fundamentals.md` for electrochemical energy storage comparison
- Cross-reference: `electrocatalysis.md` for electrode materials science
- Cross-reference: `surface_chemistry.md` for high-surface-area electrode principles
- Key primary literature: Conway, "Electrochemical Supercapacitors" (1999)

---

## Links

- L3: `../L3_functions/advanced_electrochemistry_tools.py`
- L4: `../L4_reference/electrochemistry_reference.csv`

---

## [Source: Wikipedia, Supercapacitor]
### Supercapacitor Types

| Type | Mechanism | Energy Density (Wh/kg) | Power Density (kW/kg) | Cycle Life |
|---|---|---|---|---|
| EDLC (double layer) | Electrostatic charge separation | 3–10 | 10–100 | >10⁶ |
| Pseudocapacitor | Surface redox reactions | 10–30 | 5–20 | >10⁵ |
| Hybrid | Both mechanisms | 10–40 | 3–15 | >10⁵ |

- EDLC: Activated carbon electrodes, organic electrolyte; C = εA/d.
- Pseudocapacitor: RuO₂, MnO₂, conducting polymers (PANI, PEDOT).
- Key advantage: Orders of magnitude higher power density than batteries, but lower energy density.

## L3 Tool Call Directives

**Source:** `supercapacitor_tools.py`

⚠️ Stub file — no public functions implemented yet.

### Available functions:
- *(none — file is empty)*
