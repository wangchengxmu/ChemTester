---
id: fuel_cells
layer: 2
title: Fuel Cells (PEMFC, SOFC, Thermodynamics)
parent: ../L1_ontology/chemistry-core-map.md#entry-271
stability: high
confidence: high
last_verified: 2026-03-24
source: Brown et al. Chemistry: The Central Science Ch20.7, OpenStax Chemistry 2e Ch17.5
---

# Fuel Cells

## Core Concept

Fuel cells are galvanic cells that continuously convert chemical energy of a fuel (typically H₂) and oxidant (O₂) into electricity, with water as the only byproduct. Unlike batteries, fuel cells require constant fuel supply.

---

## Thermodynamics

### Overall Reaction (H₂/O₂)
$$2\text{H}_2 + \text{O}_2 \rightarrow 2\text{H}_2\text{O}$$

### Standard Potential
$$E^\circ = 1.23 \text{ V} \text{ (at 25°C, liquid water product)}$$

### Maximum Efficiency
$$\eta_{max} = \frac{\Delta G}{\Delta H} = \frac{-237.1}{-285.8} = 83\%$$

### Actual voltage: 0.6-0.8 V (losses from overpotentials)

---

## Types of Fuel Cells

### PEMFC (Proton Exchange Membrane Fuel Cell)
- **Electrolyte:** Nafion (sulfonated PTFE, H⁺ conductor)
- **Temperature:** 60-80°C
- **Fuel:** H₂ (pure, or reformate with CO < 50 ppm)
- **Anode:** Pt/C catalyst
- **Cathode:** Pt/C catalyst
- **Efficiency:** 50-60%
- **Applications:** vehicles (Toyota Mirai), backup power

### SOFC (Solid Oxide Fuel Cell)
- **Electrolyte:** YSZ (Y₂O₃-stabilized ZrO₂, O²⁻ conductor)
- **Temperature:** 800-1000°C
- **Fuel:** H₂, CO, CH₄ (internal reforming possible)
- **Anode:** Ni-YSZ cermet
- **Cathode:** LSM (La₀.₈Sr₀.₂MnO₃)
- **Efficiency:** 60-70% (85% with CHP)
- **Applications:** stationary power, CHP

### Other Types

| Type | Electrolyte | Temp (°C) | Notes |
|------|------------|-----------|-------|
| DMFC | Polymer | 60-90 | Direct methanol, low efficiency |
| PAFC | H₃PO₄ | 175-200 | 200 kW stationary |
| MCFC | Molten carbonate | 600-700 | Internal reforming |
| AFC | KOH (aq) | 60-90 | Space applications (Apollo) |

---

## Voltage Losses

### Nernst Loss (concentration)
$$\Delta V_{conc} = \frac{RT}{nF}\ln\frac{i_L}{i_L - i}$$

### Activation Loss (kinetics)
$$\eta_{act} = \frac{RT}{\alpha nF}\ln\frac{i}{i_0}$$

### Ohmic Loss
$$\Delta V_{ohm} = iR_{internal}$$

### Total: V = E - η_act,a - η_act,c - ΔV_ohm - ΔV_conc

---

## Complete Extraction: Fuel Cells (Brown et al. + OpenStax)

### Fundamental Principle
A fuel cell is a galvanic cell that requires **constant external supply** of reactants (fuel + oxidant). Unlike batteries, fuel cells do not store energy internally.

### Hydrogen Fuel Cell (PEM-type, acidic)
- **Anode:** 2H₂(g) → 4H⁺(aq) + 4e⁻
- **Cathode:** O₂(g) + 4H⁺(aq) + 4e⁻ → 2H₂O(g)
- **Overall:** 2H₂(g) + O₂(g) → 2H₂O(g)
- **E_cell:** ~1.2 V
- **Electrodes:** Graphite embedded with Pt-based catalysts
- **Efficiency:** 50-75% (vs 20-25% for internal combustion engines)

### Energy Comparison
- **Internal combustion engine:** ~20-25% thermal efficiency
- **Hydrogen fuel cell:** ~50-75% efficiency (more than double)
- The same redox reaction (2H₂ + O₂ → 2H₂O) occurs, but electrochemical pathway is far more efficient than combustion

### Applications
- Space missions (extended duration)
- Prototypes for personal vehicles (technology still maturing)
- Stationary power generation

### Key Challenges
- Hydrogen storage and transport
- Platinum catalyst cost and scarcity
- Water management in PEM cells
- Durability and degradation

### Source Cross-References
- Brown et al. Chemistry: The Central Science, Ch20.7
- OpenStax Chemistry 2e, Ch17.5

---

## Textbook Problems

```json
{
  "id": "P2_fuelcell_001",
  "topic": "Fuel Cell Efficiency",
  "difficulty": "medium",
  "question": "A hydrogen fuel cell produces 1.2 V. If the thermodynamic maximum voltage is 1.23 V, what is the voltage efficiency?",
  "answer": "Voltage efficiency = 1.2/1.23 × 100% = 97.6%. Overall efficiency is further reduced by current losses (activation, ohmic, concentration).",
  "source": "OpenStax Ch17.5"
}
```

---

## Links

- L3: `../L3_functions/advanced_electrochemistry_tools.py`
- L4: `../L4_reference/electrochemistry_reference.csv`

---

## [Source: Wikipedia, Fuel Cell]
### Fuel Cell Types

| Type | Electrolyte | Operating T (°C) | Efficiency | Application |
|---|---|---|---|---|
| PEMFC | Polymer membrane (Nafion) | 50–100 | 40–60% | Vehicles (Toyota Mirai) |
| DMFC | Polymer membrane | 50–120 | 30–40% | Portable electronics |
| PAFC | Phosphoric acid | 150–200 | 36–42% | Stationary power |
| MCFC | Molten carbonate | 600–700 | 47–50% | Stationary power |
| SOFC | Solid oxide (YSZ) | 800–1000 | 50–65% | Stationary, CHP |

- PEMFC anode: H₂ → 2H⁺ + 2e⁻ (Pt catalyst)
- PEMFC cathode: ½O₂ + 2H⁺ + 2e⁻ → H₂O
- Overall: H₂ + ½O₂ → H₂O; E° = 1.23 V

## Data Reference
- L4 Data: L4_reference/electrode_potentials.csv — Standard reduction potentials E° for 28 half-reactions
- L4 Reference: L4_reference/THERMODYNAMIC_DATABASES.md — Links to NIST, CRC Handbook
