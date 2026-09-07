---
id: band.theory
layer: 2
title: Band Theory
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - ../L3_functions/band_theory_tools.py
  - ../L3_functions/band_theory_tools.py
  - ../L4_reference/reference/band-theory-reference.md
  - ../L5_examples/band_theory/
source:
  - Averill, Ch12
---

[Source: Averill, Ch12]

## Context

Band theory explains the electrical properties of solids by considering how atomic orbitals combine to form continuous energy bands. This theory explains why metals conduct electricity, why insulators don't, and how semiconductors bridge the gap.

## Core Concepts

### 1. Formation of Energy Bands

**From atomic orbitals to bands:**
1. In isolated atoms: discrete energy levels
2. In molecules: molecular orbitals (bonding, antibonding)
3. In solids: so many atoms that levels merge into continuous bands

**Key principle:**
- n atoms with n atomic orbitals → n molecular orbitals
- As n → 10²³, spacing between levels → 0
- Result: Continuous bands of allowed energies

### 2. Band Structure Terminology

| Term | Definition |
|------|------------|
| **Valence Band** | Highest energy band that is occupied at 0 K |
| **Conduction Band** | Lowest energy band that is empty at 0 K |
| **Band Gap (Eg)** | Energy difference between valence and conduction bands |
| **Bandwidth** | Energy range within a single band |
| **Fermi Level** | Energy at which occupation probability = 0.5 |

### 3. Metals, Insulators, Semiconductors

**Metals:**
- Partially filled valence band, OR
- Overlapping valence and conduction bands
- No band gap (or effectively zero)
- Electrons easily excited to empty levels
- High electrical conductivity
- Conductivity decreases with temperature

**Insulators:**
- Completely filled valence band
- Large band gap (> 3 eV, typically > 5 eV)
- Electrons cannot be excited at normal temperatures
- Very low electrical conductivity
- Example: Diamond (Eg = 5.5 eV)

**Semiconductors:**
- Completely filled valence band
- Small band gap (< 3 eV)
- Some electrons thermally excited to conduction band
- Moderate conductivity that increases with temperature
- Examples: Si (Eg = 1.1 eV), Ge (Eg = 0.7 eV)

### 4. Band Gap Values

| Material | Band Gap (eV) | Classification |
|----------|---------------|----------------|
| Na | 0 (overlap) | Metal |
| Cu | 0 (partial fill) | Metal |
| Diamond | 5.5 | Insulator |
| Si | 1.1 | Semiconductor |
| Ge | 0.67 | Semiconductor |
| GaAs | 1.4 | Semiconductor |

### 5. Conduction Mechanisms

**In Metals:**
- Partially filled band → electrons free to move
- Small energy input excites electrons to empty states
- Both electron flow and hole flow possible

**In Semiconductors:**
- Thermal excitation: e⁻ jumps from valence to conduction band
- Creates: free electron in conduction band + hole in valence band
- Both electrons and holes contribute to conductivity

### 6. Doping Semiconductors

**n-Type Semiconductors:**
- Dopant has MORE valence electrons than host
- Example: P (5 e⁻) in Si (4 e⁻)
- Extra electrons easily excited to conduction band
- Negative charge carriers (electrons)

**p-Type Semiconductors:**
- Dopant has FEWER valence electrons than host
- Example: B (3 e⁻) in Si (4 e⁻)
- Creates holes in valence band
- Positive charge carriers (holes)

**Effect of doping:**
- Dramatically increases conductivity
- Allows precise control of electrical properties
- Basis of all semiconductor devices

### 7. Temperature Effects

| Material Type | Effect of Increasing T on Conductivity |
|---------------|---------------------------------------|
| Metal | Decreases (more lattice vibrations scatter electrons) |
| Semiconductor | Increases (more electrons excited across gap) |
| Insulator | Little effect (gap too large) |

## Decision Flow

### Classifying Material from Band Structure

1. Is there a partially filled band?
   → Yes: Metal
   → No: Check band gap

2. Is band gap > 3 eV?
   → Yes: Insulator
   → No: Semiconductor

### Predicting Conductivity Changes

1. Identify material type
2. Apply temperature rule:
   - Metal: σ decreases with T
   - Semiconductor: σ increases with T

3. For doped semiconductors:
   - Higher doping → higher σ
   - n-type vs p-type determines carrier type

## Quantitative Relationships

**Conductivity of semiconductor:**
```
σ = σ₀ × exp(-Eg / 2kT)
```

**Intrinsic carrier concentration:**
```
n_i ∝ exp(-Eg / 2kT)
```

**Temperature dependence:**
- For metals: σ ∝ 1/T (approximately)
- For semiconductors: ln(σ) ∝ -1/T

## Edge Cases

- **Semimetals:** Very small band overlap (Bi, Sb)
- **Wide-bandgap semiconductors:** Eg 2-4 eV (GaN, SiC)
- **Organic semiconductors:** π-conjugated systems
- **Superconductors:** Zero resistance below Tc

## Applications

1. **Solar cells:** Light excites electrons across band gap
2. **LEDs:** Electrons fall across band gap, emit light
3. **Transistors:** Control flow of carriers between n and p regions
4. **Thermistors:** Temperature-dependent resistance

## Implementations and Data

- Tool implementation: [L3 code](../L3_functions/band_theory_tools.py)
- Solver wrapper: [L3 skill](../L3_functions/band_theory_tools.py)
- Reference database: [L4 band gaps](../L4_reference/reference/band-theory-reference.md)
- Worked examples: [L5 examples](../L5_examples/band_theory/)

## Related Topics

- [solid_state_chemistry.md](solid_state_chemistry.md) - Types of solids
- [crystal_structures.md](crystal_structures.md) - Solid-state structure
- [electron_configurations.md](electron_configurations.md) - Atomic orbital origins
- [electrochemistry.md](electrochemistry.md) - Electronic processes

## L3 Tool Call Directives


**Source:** `band_theory_tools.py`

L3 tool module for band theory tools

### Available functions:
- `band_gap_energy(conductivity_300K: float, conductivity_0K: float)` → float — Estimate band gap from conductivity ratio.
- `conductivity_temperature_dependence(Eg: float, T1: float, T2: float, sigma1: float)` → float — Calculate conductivity at new temperature for semiconductor.
- `intrinsic_carrier_concentration(Eg: float, temperature: float, Nc: float, Nv: float)` → float — Calculate intrinsic carrier concentration.
- `fermi_level_intrinsic(Eg: float, Nc: float, Nv: float)` → float — Calculate Fermi level for intrinsic semiconductor.
- `doping_type_effect(dopant_type: str)` → dict — Describe effect of doping type.
- `semiconductor_material_properties(material: str)` → dict — Return key semiconductor properties.
- `pn_junction_bias(bias_type: str)` → dict — Describe PN junction behavior under bias.

### Common errors:
- ❌ Passing wrong parameter types (strings where numbers expected)
- ❌ Forgetting required parameters
