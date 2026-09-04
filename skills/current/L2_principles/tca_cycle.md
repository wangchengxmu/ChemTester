# L2 Topic: Citric Acid Cycle (TCA/Krebs Cycle)

**Source**: Fundamentals of Biochemistry (Jakubowski/Flatt)
**Created**: 2026-03-18
**Status**: Pass-1

---

## Concept Overview

The citric acid cycle (TCA cycle, Krebs cycle) oxidizes acetyl-CoA to COâ? generating NADH, FADHâ? and GTP. It occurs in the mitochondrial matrix and is central to aerobic metabolism.

### Key Features
1. **8 enzymatic reactions**: Acetyl-CoA â?2 COâ?2. **Energy yield**: 3 NADH + 1 FADHâ?+ 1 GTP per turn
3. **Amphibolic**: Both catabolic and anabolic functions
4. **Regulated**: Three key control points

---

## Core Principles

### The 8 Steps

| Step | Enzyme | Reaction | Product |
|------|--------|----------|---------|
| 1 | Citrate synthase | Acetyl-CoA + OAA â?Citrate | Citrate |
| 2 | Aconitase | Citrate â?Isocitrate | Isocitrate |
| 3 | Isocitrate DH | Isocitrate â?Î±-KG | NADH + COâ?|
| 4 | Î±-KG DH | Î±-KG â?Succinyl-CoA | NADH + COâ?|
| 5 | Succinyl-CoA synthetase | Succinyl-CoA â?Succinate | GTP |
| 6 | Succinate DH | Succinate â?Fumarate | FADHâ?|
| 7 | Fumarase | Fumarate â?Malate | Malate |
| 8 | Malate DH | Malate â?OAA | NADH |

### Energy Yield per Acetyl-CoA

| Product | ATP Equivalent |
|---------|----------------|
| 3 NADH | 7.5 ATP |
| 1 FADHâ?| 1.5 ATP |
| 1 GTP | 1 ATP |
| **Total** | **10 ATP** |

### Regulation Points

| Enzyme | Activators | Inhibitors |
|--------|------------|------------|
| Citrate synthase | ADP | ATP, NADH, Citrate |
| Isocitrate DH | ADP, CaÂ²â?| ATP, NADH |
| Î±-KG DH | CaÂ²â?| ATP, NADH, Succinyl-CoA |

### Anaplerotic Reactions

| Reaction | Enzyme | Tissue |
|----------|--------|--------|
| Pyruvate â?OAA | Pyruvate carboxylase | Liver, kidney |
| Pyruvate â?Malate | Malic enzyme | Many tissues |
| Glutamate â?Î±-KG | Glutamate DH | Many tissues |

---

## Key Formulas

### Total ATP from Glucose (Complete Oxidation)

| Stage | ATP |
|-------|-----|
| Glycolysis | 2 + 5 (from NADH) = 7 |
| Pyruvate â?Acetyl-CoA | 5 (from NADH) |
| TCA cycle (Ã2) | 2 Ã 10 = 20 |
| **Total** | **32 ATP** |

Using P/O ratios: NADH = 2.5 ATP, FADHâ?= 1.5 ATP

### Free Energy

$$\Delta GÂ°' = -9.8 \text{ kJ/mol (cycle)}$$

---

## L3 Implementations Needed

| Function | Purpose |
|----------|---------|
| `tca_atp_yield` | Calculate total ATP from glucose |
| `cycle_flux` | Model cycle rate |
| `anaplerotic_balance` | Check intermediate balance |

## L4 Data Needed

| Table | Content |
|-------|---------|
| `tca_enzymes.csv` | Enzyme, Km, effectors |
| `tca_intermediates.csv` | Concentrations, ÎG |

## L5 Examples Needed

| Example | Topic |
|---------|-------|
| ATP accounting | Complete glucose oxidation |
| Regulation analysis | Flux control |

---

**Cross-links:**
- glycolysis.md
- oxidative_phosphorylation.md
- metabolic_pathways.md


## Implementations

- Implementation: `../L3_functions/metabolism_tools.py`
