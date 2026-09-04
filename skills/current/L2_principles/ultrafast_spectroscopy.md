# Ultrafast Spectroscopy

## Concept Overview

Ultrafast spectroscopy uses femtosecond-to-picosecond laser pulses to observe real-time molecular dynamics, bond breaking, and energy transfer.

## Key Principles

### Pump-Probe Technique
- **Pump**: excitation pulse (initiates photochemical process)
- **Probe**: delayed pulse (interrogates system state)
- Time delay controlled by optical path length difference:
```
Δt = Δx / c
```
- 1 fs time resolution requires ~0.3 μm path control

### Transient Absorption Spectroscopy
- Measures ΔA (change in absorbance) vs time and wavelength
- Ground state bleach (GSB): negative signal at absorption λ
- Stimulated emission (SE): negative signal at emission λ
- Excited state absorption (ESA): positive signal at new λ

### Time-Resolved Fluorescence
- Time-correlated single photon counting (TCSPC)
- Streak camera
- Fluorescence upconversion (sub-ps resolution)

### Typical Timescales
| Process | Timescale |
|---------|-----------|
| Vibrational relaxation | 10–100 fs |
| Internal conversion | 100 fs – 1 ps |
| ISC | 100 ps – 10 ns |
| Fluorescence | 0.1 – 10 ns |
| Phosphorescence | μs – s |
| Solvent reorganization | 100 fs – 10 ps |

### Femtochemistry
- Study of transition states in real time (Ahmed Zewail, Nobel 1999)
- Observation of bond breaking/forming as it occurs

## Problem-Solving Routes

1. **Interpret transient spectra**: Identify GSB, SE, ESA features
2. **Extract kinetics**: Global analysis → decay-associated spectra (DAS)
3. **Determine mechanism**: Map time constants to known processes (IC, ISC, charge transfer)

## Links

- **L3 Tools**: `../L3_functions/photochemistry_tools.py`
- **L4 Data**: `../L4_reference/photochemistry_data.csv`
- **L5 Examples**: `../L5_examples/photochemistry_examples.md`
