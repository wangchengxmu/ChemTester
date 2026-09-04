---
id: chem.flow_chemistry
layer: 2
title: Flow Chemistry
source: Wikipedia
status: active
created: 2026-03-24
down_links:
  - ../L3_functions/process_economics_tools.py
---

# Flow Chemistry

## Concept Overview
Flow chemistry (continuous flow chemistry) performs chemical reactions in continuously flowing streams rather than in batches. Reactants are pumped through a reactor (tube, chip, or packed column) at controlled rates.

## Key Principles

### Residence Time Distribution (RTD)
- **Residence time (Ï„)** = V/Q where V = reactor volume, Q = volumetric flow rate.
- In ideal plug flow: all fluid elements have same Ï„ (narrow RTD â†’ better selectivity).
- Laminar flow (Re < 2100): parabolic velocity profile â†’ RTD broadening.
- Taylor dispersion: Axial dispersion coefficient D_ax â‰ˆ D_m + uÂ²RÂ²/(48D_m) for capillary flow.

### Scaling
- **Scale-out** (numbering up): Parallel identical reactors, not scale-up (larger reactor).
- Maintains mixing, heat transfer, and residence time characteristics.
- Lab-to-production transfer with minimal re-optimization.

### Mass Transfer
- Enhanced by high surface-area-to-volume ratio (SA/V).
- Tube reactors: SA/V = 2/r (inverse proportion to radius).
- Microreactors (r ~ 100 Î¼m): SA/V ~ 20,000 mÂ²/mÂ³ vs. ~100 mÂ²/mÂ³ in batch.

### Heat Transfer
- Temperature control in flow: Î”T = (qÂ·rÂ²)/(4k) for laminar flow in tube.
- Sub-second heating/cooling achievable; prevents thermal runaway.

## Applications
- **Photochemistry**: Continuous irradiation of thin films; uniform photon flux.
- **Electrochemistry**: Efficient mass transport to electrodes; narrow electrode gaps.
- **Hazardous chemistry**: Small holdup volume â†’ safer with toxic/explosive intermediates.
- **API manufacturing**: GlaxoSmithKline, Pfizer, Lonza use flow for drug intermediates.

## Key Equipment
| Component | Function |
|---|---|
| Syringe pump | Precise flow control (Î¼L/min to mL/min) |
| HPLC pump | Higher pressure, broader flow range |
| Microreactor chip | Microliter volumes, high SA/V |
| Packed bed reactor | Immobilized catalyst or reagent |
| CSTR cascade | Multiple CSTRs approximate PFR behavior |

## Sources
[Source: Wikipedia, Flow Chemistry]
[Source: Flow chemistry literature, 2020s]

## L3 Tools
-> `../L3_functions/flow_chemistry_tools.py` â€” `residence_time_calc()`, `reynolds_number()`

---

## L3 Tool Call Directives

**Source:** low_chemistry_tools.py
Residence time, space-time yield, Reynolds number for flow reactor design.

### Available functions:
- esidence_time(volume_ml, flow_rate_ml_min) ¡ú float ¡ª ¦Ó = V/F (min)
- space_time_yield(product_g, volume_ml, time_h) ¡ú float ¡ª STY in g/(mL¡¤h)
- eynolds_number(D, v, rho, mu) ¡ú float ¡ª Re = ¦ÑvD/¦Ì (<2100 laminar, >4000 turbulent)

### Common errors:
- ? Units mismatch: volume (mL) and flow rate (mL/min) must be consistent
- ? Confusing residence time with space-time yield ¡ª ¦Ó is time; STY is productivity rate
