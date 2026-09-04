---
id: battery_fundamentals
layer: 2
title: Battery Fundamentals (Thermodynamics, Capacity, Energy Density)
parent: ../L1_ontology/chemistry-core-map.md#entry-269
stability: high
confidence: high
last_verified: 2026-03-24
source: Brown et al. Chemistry: The Central Science Ch20.7, OpenStax Chemistry 2e Ch17.5
---

# Battery Fundamentals

## Core Concept

Batteries are electrochemical cells that convert chemical energy to electrical energy. Key performance metrics derive from thermodynamics and electrode kinetics.

---

## Thermodynamic Foundations

### Cell Potential & Gibbs Free Energy
$$\Delta G^\circ = -nFE^\circ$$

### Nernst Equation
$$E = E^\circ - \frac{RT}{nF}\ln Q$$

At 25°C: E = E° - (0.0592/n) log Q

### Maximum Work
$$w_{max} = -nFE$$

---

## Key Performance Metrics

### Theoretical Capacity
$$C = \frac{nF}{3.6 M_w} \text{ (mAh/g)}$$

Where n = electrons, M_w = molar mass of active material.

### Energy Density
$$\text{Energy density} = C \times E_{avg} \text{ (Wh/kg)}$$

### Specific Power
$$\text{Power density} = \frac{\text{Energy density}}{\text{discharge time}} \text{ (W/kg)}$$

### Coulombic Efficiency
$$\eta_C = \frac{\text{charge discharged}}{\text{charge input}} \times 100\%$$

---

## Battery Types

### Primary (Non-rechargeable)
- **Leclanché (Zn-Carbon):** Zn|NH₄Cl, ZnCl₂|MnO₂, C — E ≈ 1.5 V
- **Alkaline:** Zn|KOH|MnO₂ — E ≈ 1.5 V, 3-5× energy of dry cell
- **Li-I₂:** Li|LiI|I₂ — E ≈ 2.8 V, medical implants (long life)

### Secondary (Rechargeable)
- **Lead-Acid:** Pb|H₂SO₄|PbO₂ — E ≈ 2.0 V, automotive
- **NiCd:** Cd|KOH|NiO(OH) — E ≈ 1.2 V
- **NiMH:** MH|KOH|NiO(OH) — E ≈ 1.2 V
- **Li-ion:** LiCoO₂|LiPF₆|C₆ — E ≈ 3.7 V

---

## Battery Configuration

### Series: voltages add
$$V_{total} = V_1 + V_2 + ... + V_n$$

### Parallel: capacities add
$$C_{total} = C_1 + C_2 + ... + C_n$$

---

## Complete Extraction: Battery Chemistry (Brown et al. Ch20.7 + OpenStax Ch17.5)

### Primary (Non-Rechargeable) Batteries

#### Leclanché Dry Cell
- **Anode:** Zn(s) → Zn²⁺(aq) + 2e⁻
- **Cathode:** 2MnO₂(s) + 2NH₄⁺(aq) + 2e⁻ → Mn₂O₃(s) + 2NH₃(aq) + H₂O(l)
- **Overall:** 2MnO₂(s) + 2NH₄Cl(aq) + Zn(s) → Mn₂O₃(s) + Zn(NH₃)₂Cl₂(s) + H₂O(l)
- **E_cell:** ~1.5 V
- **Limitations:** Limited shelf life (Zn corrodes with NH₄Cl), inefficient (only nearby MnO₂ reacts)

#### Alkaline Battery
- **Anode:** Zn(s) + 2OH⁻ → ZnO(s) + H₂O(l) + 2e⁻
- **Cathode:** 2MnO₂(s) + H₂O(l) + 2e⁻ → Mn₂O₃(s) + 2OH⁻(aq)
- **Overall:** Zn(s) + 2MnO₂(s) → ZnO(s) + Mn₂O₃(s)
- **E_cell:** +1.43 V (OpenStax) / ~1.5 V (Brown)
- **Advantages:** 3-5× energy of dry cell, longer shelf life, more constant voltage

#### Button Batteries
**Mercury cell (E = 1.35 V):**
- Zn(s) + 2HgO(s) → 2Hg(l) + ZnO(s)
**Silver cell (E = 1.6 V):**
- Zn(s) + 2Ag₂O(s) → 2Ag(s) + ZnO(s)
- High output-to-mass ratio; used in watches, cameras, hearing aids

#### Lithium-Iodine Battery
- **Anode:** 2Li(s) → 2Li⁺(LiI) + 2e⁻
- **Cathode:** I₂(s) + 2e⁻ → 2I⁻(LiI)
- **Overall:** 2Li(s) + I₂(s) → 2LiI(s)
- **E_cell:** 3.5 V; solid electrolyte (LiI layer)
- **Applications:** Cardiac pacemakers (10+ year life), memory backup, smoke alarms
- **Drawback:** High internal resistance limits current

### Secondary (Rechargeable) Batteries

#### Lead-Acid Battery
- **Anode:** Pb(s) + HSO₄⁻(aq) → PbSO₄(s) + H⁺(aq) + 2e⁻
- **Cathode:** PbO₂(s) + HSO₄⁻(aq) + 3H⁺(aq) + 2e⁻ → PbSO₄(s) + 2H₂O(l)
- **Overall:** Pb(s) + PbO₂(s) + 2H₂SO₄(aq) ⇌ 2PbSO₄(s) + 2H₂O(l)
- **E_cell:** ~2 V per cell; 6 cells = 12 V car battery
- Products (PbSO₄) adhere to electrodes, allowing recharge

#### Nickel-Cadmium (NiCad)
- **Overall:** Cd(s) + 2NiO(OH)(s) + 2H₂O(l) ⇌ Cd(OH)₂(s) + 2Ni(OH)₂(s)
- **E_cell:** 1.2-1.4 V
- **Jelly-roll design** maximizes electrode surface area
- **Limitations:** Memory effect, Cd toxicity, EU directive bans >0.002% Cd

#### Nickel-Metal Hydride (NiMH)
- **Overall:** NiO(OH)(s) + MH → Ni(OH)₂(s) + M(s)
- **Advantages over NiCad:** 30-40% higher capacity, no Cd, less memory effect
- **Disadvantages:** 50% higher self-discharge, higher cost

#### Lithium-Ion Battery
- **Cathode:** Li₁₋ₓCoO₂ + xLi⁺ + xe⁻ ⇌ LiCoO₂
- **Anode:** xLiC₆ ⇌ xLi⁺ + xe⁻ + xC₆
- **E_cell:** ~3.7 V (x typically ≤ 0.5)
- **Advantages:** High energy density, light, nearly constant voltage, slow self-discharge
- **Dominant technology** for portable electronics

### Key Design Principles
- Batteries use **solids or pastes** (not solutions) to maximize energy/mass ratio
- Reactant concentrations change little during discharge → **constant voltage**
- Series connection: V_total = ΣV_i; Parallel: C_total = ΣC_i
- Rechargeable batteries form **insoluble products that adhere to electrodes**

### Source Cross-References
- Brown et al. Chemistry: The Central Science, Ch20.7
- OpenStax Chemistry 2e, Ch17.5

---

## Textbook Problems

```json
{
  "id": "P2_battery_001",
  "topic": "Battery Chemistry",
  "difficulty": "medium",
  "question": "Write the half-reactions and overall reaction for a lead-acid battery. Why can it be recharged?",
  "answer": "Anode: Pb + HSO₄⁻ → PbSO₄ + H⁺ + 2e⁻; Cathode: PbO₂ + HSO₄⁻ + 3H⁺ + 2e⁻ → PbSO₄ + 2H₂O. The PbSO₄ product is insoluble and adheres to electrodes, allowing reversal.",
  "source": "OpenStax Ch17.5"
}
```

```json
{
  "id": "P2_battery_002",
  "topic": "Battery Comparison",
  "difficulty": "easy",
  "question": "What is the cell voltage of a lithium-iodine battery and why is it used in pacemakers?",
  "answer": "E_cell = 3.5 V. Used in pacemakers because the solid-state LiI electrolyte provides exceptional longevity (10+ years) and reliability.",
  "source": "Brown et al. Ch20.7"
}
```

---

## Links

- L3: `../L3_functions/advanced_electrochemistry_tools.py` (existing) + Phase 2 additions
- L4: `../L4_reference/electrochemistry_reference.csv`
- L5: `../L5_examples/advanced_electrochemistry_examples.md`

---

## [Source: Wikipedia, Lithium-Ion Battery]
### Li-ion Battery Key Parameters

| Parameter | Typical Value |
|---|---|
| Energy density | 100–265 Wh/kg |
| Voltage (nominal) | 3.6–3.7 V |
| Cycle life | 300–5,000 cycles |
| Coulombic efficiency | >99.9% |
| Self-discharge | 1–3%/month |

### Common Cathode Materials

| Cathode | Formula | Voltage (V) | Capacity (mAh/g) | Notes |
|---|---|---|---|---|
| LCO | LiCoO₂ | 3.7–4.2 | 140–155 | Phones, laptops |
| NMC | LiNiₓMnᵧCo₂O₂ | 3.6–4.3 | 150–210 | EVs (most common) |
| NCA | LiNi₀.₈Co₀.₁₅Al₀.₀₅O₂ | 3.6–4.3 | 200 | Tesla |
| LFP | LiFePO₄ | 3.2–3.6 | 160–170 | Very safe, long life |
| LMO | LiMn₂O₄ | 3.8–4.0 | 100–120 | Power tools |

### Common Anode Materials
- **Graphite**: 372 mAh/g (LiC₆), standard.
- **Silicon**: 3,579 mAh/g (Li₁₅Si₄) theoretical, but ~300% volume expansion → capacity fade.
- **LTO**: Li₄Ti₅O₁₂, 175 mAh/g, zero strain, excellent cycle life.

## Data Reference
- L4 Data: L4_reference/electrode_potentials.csv — Standard reduction potentials E° for 28 half-reactions
- L4 Reference: L4_reference/THERMODYNAMIC_DATABASES.md — Links to NIST, CRC Handbook
