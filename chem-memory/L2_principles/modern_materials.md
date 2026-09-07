---
id: modern_materials.overview
layer: 2
title: Modern Materials — Semiconductors, Ceramics, Superconductors, Composites
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - ../L3_tools/semiconductor_tools.py
  - ../L3_tools/ceramics_tools.py
  - ../L3_tools/superconductor_tools.py
  - ../L3_tools/composite_tools.py
cross_links:
  - ./band_theory.md
  - ./solid_state_chemistry.md
  - ./nanomaterials_overview.md
source: Chemistry: The Central Science, Brown et al., Chapter 12
---

## Context

Modern materials science extends traditional solid-state chemistry to engineered materials with tailored electronic, mechanical, and thermal properties. This node covers **semiconductors**, **ceramics**, **superconductors**, and **composites** — materials central to electronics, energy, aerospace, and structural engineering.

---

## Semiconductors

### Band Theory Foundation

Semiconductors have a small band gap (E_g ≈ 0.1–3.5 eV), between insulators (>3.5 eV) and metals (no gap).

| Material | Type | E_g (eV) | Application |
|----------|------|----------|-------------|
| Si | Group IV | 1.11 | Transistors, solar cells |
| Ge | Group IV | 0.67 | Infrared detectors |
| GaAs | III-V | 1.43 | LEDs, high-speed electronics |
| InP | III-V | 1.34 | Photonics, HBTs |
| CdTe | II-VI | 1.50 | Thin-film solar cells |
| ZnO | II-VI | 3.37 | UV LEDs, transparent conductors |
| TiO₂ | Metal oxide | 3.2 | Photocatalysis, DSSCs |
| SiC | IV-IV | 2.3–3.3 | High-power, high-temperature devices |

### Intrinsic vs Extrinsic Semiconductors

- **Intrinsic**: Pure semiconductor; carrier concentration n_i depends on E_g and T.
  - n_i = √(N_c · N_v) · exp(−E_g / 2kT)
- **Extrinsic (doped)**: Deliberate impurity addition creates carriers.
  - **n-type**: Donor dopant (e.g., P in Si) adds electrons to conduction band.
  - **p-type**: Acceptor dopant (e.g., B in Si) creates holes in valence band.

### Key Formulas

**Carrier concentration (n-type):**
n ≈ N_d at room temperature (full ionization assumed)

**Conductivity:**
σ = n·q·μ_n + p·q·μ_p

where n, p = electron/hole concentrations, q = electron charge, μ = mobility.

**Temperature dependence:**
σ ∝ exp(−E_g / 2kT) (intrinsic region)

### p-n Junctions

- Depletion region forms at the interface of p- and n-type materials.
- Forward bias: reduces barrier, allows current flow.
- Reverse bias: increases barrier, blocks current.
- Applications: diodes, transistors, solar cells, LEDs.

---

## Ceramics

### Definition and Classification

Ceramics are inorganic, nonmetallic solids processed at high temperatures. They are typically **ionic and/or covalent** compounds with high melting points, hardness, and chemical inertness.

| Category | Examples | Key Properties |
|----------|----------|----------------|
| Oxides | Al₂O₃, SiO₂, ZrO₂, MgO | High hardness, electrical insulation |
| Carbides | SiC, B₄C, WC | Extreme hardness, wear resistance |
| Nitrides | Si₃N₄, AlN, BN | High thermal conductivity, thermal shock resistance |
| Glass-ceramics | Li₂O-Al₂O₃-SiO₂ | Controlled crystallization, machinability |

### Crystal Structures

- **NaCl structure**: AX compounds (e.g., MgO, CaO)
- **CaF₂ (fluorite)**: AX₂ (e.g., ZrO₂, UO₂)
- **Perovskite (ABO₃)**: BaTiO₃, SrTiO₃ — ferroelectric materials
- **Spinel (AB₂O₄)**: MgAl₂O₄ — magnetic and refractory

### Mechanical Properties

- **High compressive strength** (often 10× tensile strength)
- **Brittle fracture**: crack propagation without plastic deformation
- **Fracture toughness** K_IC is the key design parameter
  - Typical: 1–5 MPa·√m for most ceramics
  - Zirconia-toughened: up to 10 MPa·√m

### Applications

| Application | Ceramic | Why |
|-------------|---------|-----|
| Cutting tools | Al₂O₃, Si₃N₄ | Hardness, thermal stability |
| Biomedical implants | Al₂O₃, ZrO₂ | Biocompatibility, wear resistance |
| Thermal barrier coatings | YSZ (Y₂O₃-stabilized ZrO₂) | Low thermal conductivity, thermal expansion match |
| Capacitors | BaTiO₃ | High dielectric constant |
| Catalytic converters | Cordierite (Mg₂Al₄Si₅O₁₈) | Thermal shock resistance |

---

## Superconductors

### Fundamental Properties

1. **Zero electrical resistance** below critical temperature T_c
2. **Meissner effect**: complete expulsion of magnetic flux below T_c
3. **Critical magnetic field** H_c: superconductivity destroyed above H_c
4. **Critical current density** J_c: superconductivity destroyed above J_c

### Types

| Type | T_c Range | H_c | Material Examples | Distinguishing Feature |
|------|-----------|-----|-------------------|----------------------|
| I | < 10 K | Low (0.01–0.2 T) | Pb (7.2 K), Hg (4.2 K), Nb (9.3 K) | Complete Meissner effect |
| II | Higher (up to ~135 K) | High (1–100 T) | Nb₃Sn (18 K), YBCO (93 K), MgB₂ (39 K) | Mixed state (vortices) |

### High-Temperature Superconductors (HTS)

- **YBCO** (YBa₂Cu₃O₇₋ₓ): T_c = 93 K (first above liquid N₂, 77 K)
- **BSCCO** (Bi₂Sr₂Ca₂Cu₃O₁₀): T_c = 110 K
- **HgBa₂Ca₂Cu₃O₈**: T_c = 135 K (record for cuprates)
- All are **cuprate perovskites** with CuO₂ planes as superconducting layers

### Key Equations

**BCS Theory (Type I):**
- Energy gap: Δ(0) = 3.53 k_B T_c
- Critical field: H_c(0) ∝ T_c² (parabolic near T_c)

**Coherence length** ξ and **penetration depth** λ:
- ξ ≈ 1–100 nm (HTS have very short ξ)
- λ ≈ 10–500 nm
- κ = λ/ξ: Type I (κ < 1/√2), Type II (κ > 1/√2)

### Applications

- MRI magnets (NbTi, Nb₃Sn)
- Particle accelerator magnets (NbTi)
- Maglev trains (YBCO tapes)
- SQUID magnetometers
- Lossless power transmission

---

## Composites

### Definition

Composites combine two or more distinct phases (matrix + reinforcement) to achieve properties superior to either constituent alone.

### Classification

| Type | Matrix | Reinforcement | Example | Key Property |
|------|--------|---------------|---------|--------------|
| Polymer matrix (PMC) | Epoxy, polyester | Glass fiber, carbon fiber | GFRP, CFRP | High specific strength |
| Metal matrix (MMC) | Al, Ti, Mg | SiC particles, Al₂O₃ fibers | SiC/Al | High-temperature strength |
| Ceramic matrix (CMC) | SiC, Al₂O₃ | SiC fibers, carbon fibers | SiC/SiC | High-temperature toughness |
| Carbon-carbon (C/C) | Carbon | Carbon fibers | Brake discs | Ultra-high-temperature |

### Rule of Mixtures

**Longitudinal modulus (Voigt model):**
E_L = V_f · E_f + V_m · E_m

**Transverse modulus (Reuss model):**
1/E_T = V_f/E_f + V_m/E_m

where V_f, V_m = volume fractions of fiber and matrix, E_f, E_m = their moduli.

**Density:**
ρ_c = V_f · ρ_f + V_m · ρ_m

### Strength Predictions

**Tensile strength (upper bound):**
σ_c ≥ σ_f · V_f + σ_m' · V_m

where σ_m' = matrix stress at fiber failure strain.

**Critical fiber volume fraction** for reinforcement:
V_crit = (σ_m − σ_m') / (σ_f − σ_m')

---

## Thin Films

### Deposition Methods

| Method | Type | Typical Thickness | Applications |
|--------|------|-------------------|--------------|
| Physical vapor deposition (PVD) | Sputtering, evaporation | 1 nm – 10 μm | Optical coatings, electronics |
| Chemical vapor deposition (CVD) | Thermal, plasma-enhanced | 10 nm – 100 μm | Semiconductor fabrication |
| Atomic layer deposition (ALD) | Self-limiting surface reactions | 0.1–10 nm | High-k gate dielectrics |
| Electroplating | Solution-based | 1–100 μm | PCB traces, connectors |

### Key Considerations

- **Film stress**: intrinsic + thermal stress can cause cracking or delamination
- **Adhesion**: critical for reliability; promoted by interlayers
- **Grain structure**: columnar vs equiaxed affects properties
- **Step coverage**: conformality important for 3D structures
