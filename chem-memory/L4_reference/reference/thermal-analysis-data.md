---
id: thermal-analysis-data
layer: 4
title: Thermal Analysis Reference Data
source: LibreTexts Instrumental Analysis (Harvey) Ch31
last_updated: 2026-03-14
---

# Thermal Analysis Reference Tables

## 1. DSC Calibration Standards

### Melting Point Standards

| Compound | Melting Point (°C) | ΔH_fusion (J/g) | ΔH_fusion (J/mol) | Molar Mass (g/mol) |
|----------|-------------------|-----------------|-------------------|-------------------|
| Indium (In) | 156.6 | 28.45 | 3.27 | 114.82 |
| Tin (Sn) | 231.9 | 60.22 | 7.17 | 118.71 |
| Lead (Pb) | 327.5 | 23.03 | 4.77 | 207.2 |
| Zinc (Zn) | 419.5 | 112.0 | 7.32 | 65.38 |
| Aluminum (Al) | 660.3 | 397.0 | 10.71 | 26.98 |

### Usage Notes

- Primary standard: Indium (most commonly used)
- For high temperature: Zinc
- Calibration constant K = ΔH_known / A_measured

---

## 2. Common Decomposition Products

### Gaseous Products from Thermal Decomposition

| Product | Molar Mass (g/mol) | Temperature Range | Typical Source |
|---------|-------------------|-------------------|----------------|
| H₂O (water) | 18.015 | 100-300°C | Hydrates, hydroxides |
| CO (carbon monoxide) | 28.010 | 300-600°C | Oxalates, formates |
| CO₂ (carbon dioxide) | 44.009 | 400-900°C | Carbonates, oxalates |
| O₂ (oxygen) | 31.998 | 200-800°C | Peroxides, oxides |
| N₂ (nitrogen) | 28.013 | 200-400°C | Azides, nitrites |
| NH₃ (ammonia) | 17.031 | 100-400°C | Ammonium salts |
| SO₂ (sulfur dioxide) | 64.064 | 300-800°C | Sulfates, sulfites |
| NO₂ (nitrogen dioxide) | 46.005 | 200-500°C | Nitrates |
| HCl (hydrogen chloride) | 36.461 | 100-400°C | Chlorides |

---

## 3. Common Decomposition Reactions

### Hydrates

| Compound | Reaction | Mass Loss (%) | Temperature (°C) |
|----------|----------|---------------|------------------|
| CaC₂O₄·H₂O | → CaC₂O₄ + H₂O | 12.3 | 100-250 |
| BaCl₂·2H₂O | → BaCl₂·H₂O + H₂O | 7.9 | 100-150 |
| BaCl₂·H₂O | → BaCl₂ + H₂O | 8.6 | 150-250 |
| CuSO₄·5H₂O | → CuSO₄ + 5H₂O | 36.1 | 30-250 |
| MgC₂O₄·H₂O | → MgC₂O₄ + H₂O | 13.8 | 100-250 |

### Carbonates

| Compound | Reaction | Mass Loss (%) | Temperature (°C) |
|----------|----------|---------------|------------------|
| CaCO₃ | → CaO + CO₂ | 44.0 | 600-900 |
| MgCO₃ | → MgO + CO₂ | 52.2 | 400-600 |
| Na₂CO₃ | Stable up to 850°C | - | - |
| BaCO₃ | → BaO + CO₂ | 22.3 | 1000-1400 |

### Oxalates

| Compound | Step 1 | Step 2 | Step 3 |
|----------|--------|--------|--------|
| CaC₂O₄·H₂O | H₂O (12.3%, 100-250°C) | CO (19.2%, 350-550°C) | CO₂ (30.1%, 600-800°C) |
| MgC₂O₄·H₂O | H₂O (13.8%, 100-250°C) | CO + CO₂ (55.2%, 350-550°C) | - |

---

## 4. 100% Crystalline Melting Enthalpies

### Polymers

| Polymer | ΔH_m (J/g) | Tm (°C) | Notes |
|---------|------------|---------|-------|
| Polyethylene (PE) | 293 | 135 | HDPE reference |
| Polypropylene (PP) | 207 | 165 | Isotactic |
| Polyethylene terephthalate (PET) | 140 | 255 | |
| Nylon 6 (PA6) | 230 | 220 | |
| Nylon 66 (PA66) | 255 | 260 | |
| Polyoxymethylene (POM) | 326 | 180 | |
| Polyvinylidene fluoride (PVDF) | 105 | 170 | |
| Polytetrafluoroethylene (PTFE) | 82 | 327 | |
| Polyamide-11 (PA11) | 226 | 185 | |

### Degree of Crystallinity Calculation

```
Crystallinity (%) = (ΔH_measured / ΔH_100%) × 100
```

---

## 5. Glass Transition Temperatures

### Polymers

| Polymer | Tg (°C) | Notes |
|---------|---------|-------|
| Polyethylene (PE) | -125 to -100 | Difficult to measure |
| Polypropylene (PP) | -10 to 0 | Atactic |
| Polystyrene (PS) | 95-100 | Atactic |
| Polyethylene terephthalate (PET) | 70-80 | Amorphous regions |
| Polycarbonate (PC) | 145-150 | |
| Polyvinyl chloride (PVC) | 80-85 | |
| Polymethyl methacrylate (PMMA) | 105-115 | |
| Nylon 6 (PA6) | 50-60 | Dry |
| Nylon 66 (PA66) | 50-60 | Dry |

### Tg Detection in DSC

- Look for baseline shift (step change)
- ΔC_p at Tg typically 0.3-0.5 J/g·K for polymers
- Report as midpoint of the step

---

## 6. Typical Heating Rates

| Technique | Typical Rate | Notes |
|-----------|--------------|-------|
| TGA | 5-20 °C/min | Slower = better resolution |
| DSC | 5-10 °C/min | Higher rates = peak shift |
| DTA | 5-15 °C/min | |

### Heating Rate Effects

| Effect | Higher Rate | Lower Rate |
|--------|-------------|------------|
| Peak temperature | Shifts higher | More accurate |
| Peak width | Broader | Sharper |
| Sensitivity | Higher | Lower |
| Resolution | Lower | Higher |

---

## 7. Sample Size Guidelines

| Technique | Typical Mass | Notes |
|-----------|--------------|-------|
| TGA | 5-20 mg | Larger for small mass losses |
| DSC | 1-10 mg | Smaller = better thermal contact |
| DTA | 10-50 mg | Depends on sensitivity |

---

## 8. Atmosphere Effects

### Common Atmospheres

| Atmosphere | Use Case | Notes |
|------------|----------|-------|
| N₂ | Inert, general | Prevents oxidation |
| Air | Oxidative studies | Decomposition products |
| Ar | High temperature inert | |
| O₂ | Oxidation studies | |
| He | High thermal conductivity | Better heat transfer |

### Atmosphere Selection

- **Oxidation studies:** Air or O₂
- **Decomposition studies:** N₂ or Ar
- **Oxide formation:** Air
- **Polymer degradation:** N₂ (to study volatiles)

---

## 9. Temperature Ranges for Common Transitions

| Transition | Typical Range | Detectable By |
|------------|---------------|---------------|
| Glass transition | -150 to 300°C | DSC (baseline shift) |
| Melting | -50 to 1000°C | DSC, DTA |
| Crystallization | Varies | DSC, DTA |
| Dehydration | 50-300°C | TGA, DSC, DTA |
| Decomposition | 200-1000°C | TGA, DSC, DTA |
| Oxidation | 200-800°C | TGA (mass gain), DSC, DTA |

---

## 10. Troubleshooting Guide

### TGA Issues

| Problem | Possible Cause | Solution |
|---------|---------------|----------|
| No mass change | Heating rate too fast | Slow down rate |
| Drifting baseline | Buoyancy effect | Run blank correction |
| Mass gain | Oxidation | Use inert atmosphere |
| Noisy signal | Furnace issue | Check gas flow |

### DSC Issues

| Problem | Possible Cause | Solution |
|---------|---------------|----------|
| No peaks | Sample too small | Increase mass |
| Broad peaks | Heating rate too fast | Slow down |
| Baseline drift | Pan not sealed | Re-seal pan |
| Irreproducible | Sample packing varies | Standardize preparation |

---

## References

1. Harvey, D. *Instrumental Analysis* (LibreTexts), Chapter 31
2. Shetty, P. *Thermal Methods of Analysis* (LibreTexts)
3. TA Instruments DSC Manuals
4. ASTM E966 - Standard Test Method for Heat of Fusion
5. ASTM E794 - Standard Test Method for Melting and Crystallization
