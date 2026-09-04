# L2 Topic: Electron Transport Chain and Oxidative Phosphorylation

**Source**: Fundamentals of Biochemistry (Jakubowski/Flatt)
**Created**: 2026-03-18
**Status**: Pass-1

---

## Concept Overview

The electron transport chain (ETC) transfers electrons from NADH and FADH₂ to O₂, creating a proton gradient that drives ATP synthesis via oxidative phosphorylation.

### Key Features
1. **Four complexes**: I, II, III, IV
2. **Proton pumping**: Creates electrochemical gradient
3. **ATP synthase**: Converts proton motive force to ATP
4. **Coupling**: ETC drives phosphorylation

---

## Core Principles

### Complex Overview

| Complex | Function | Protons Pumped | Inhibitors |
|---------|----------|----------------|------------|
| I (NADH-Q oxidoreductase) | NADH → Q | 4 | Rotenone |
| II (Succinate-Q oxidoreductase) | FADH₂ → Q | 0 | Malonate |
| III (Q-cytochrome c oxidoreductase) | Q → Cyt c | 4 | Antimycin A |
| IV (Cytochrome c oxidase) | Cyt c → O₂ | 2 | CN⁻, CO, N₃⁻ |
| V (ATP synthase) | ADP + Pi → ATP | Uses gradient | Oligomycin |

### P/O Ratios

| Substrate | Protons | ATP |
|-----------|---------|-----|
| NADH | 10 H⁺ | 2.5 |
| FADH₂ (Complex II) | 6 H⁺ | 1.5 |

### Chemiosmotic Theory

$$\Delta p = \Delta \Psi - \frac{2.303 RT}{F} \Delta pH$$

Where:
- Δp = Proton motive force (mV)
- ΔΨ = Membrane potential (~150 mV)
- ΔpH = pH gradient (~0.5 units)

### ATP Synthesis

$$\text{ADP} + P_i + nH^+_{out} \rightarrow \text{ATP} + H_2O + nH^+_{in}$$

Current estimate: n ≈ 4 H⁺ per ATP (3 for synthase + 1 for transport)

---

## Key Formulas

### Free Energy from Proton Gradient
$$\Delta G = nF\Delta p = nF(\Delta \Psi - 59 \Delta pH)$$

### ATP Yield Calculation

| Source | NADH | FADH₂ | ATP |
|--------|------|-------|-----|
| Glycolysis (cytosolic) | 2 | 0 | 3-5* |
| Pyruvate oxidation | 2 | 0 | 5 |
| TCA cycle | 6 | 2 | 17 |
| **Total** | **10** | **2** | **25-27** |

*Varies by shuttle system (malate-aspartate = 5, glycerol-3-phosphate = 3)

---

## Regulation

### Uncoupling
- **Physiological**: UCPs in brown fat (thermogenesis)
- **Chemical**: DNP, FCCP

### Respiratory Control
$$\text{RCR} = \frac{\text{State 3 rate}}{\text{State 4 rate}}$$

High RCR (>5) indicates well-coupled mitochondria.

---

## L3 Implementations Needed

| Function | Purpose |
|----------|---------|
| `etc_flux` | Model electron flow |
| `atp_yield_shuttle` | ATP with different shuttles |
| `proton_motive_force` | Calculate Δp |
| `rcr_calculation` | Respiratory control ratio |

## L4 Data Needed

| Table | Content |
|-------|---------|
| `etc_redox_potentials.csv` | E°' values |
| `uncouplers.csv` | Common uncouplers, doses |

## L5 Examples Needed

| Example | Topic |
|---------|-------|
| Complete ATP accounting | Glucose → 32 ATP |
| Shuttle comparison | Malate-Asp vs G3P |

---

**Cross-links:**
- tca_cycle.md
- thermodynamics.md
- bioenergetics.md
