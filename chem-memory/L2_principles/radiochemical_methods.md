---
id: radiochemical_methods
layer: 2
title: Radiochemical Methods of Analysis
stability: high
confidence: high
constraints:
  - Focus on analytical applications
  - Include safety considerations
last_verified: 2026-03-17
source: Skoog Principles of Instrumental Analysis, Ch32
---

## Core Concepts

### Radioactive Decay

#### Types of Radiation

| Type | Symbol | Mass (amu) | Charge | Penetration | Stopped by |
|------|--------|------------|--------|-------------|------------|
| Alpha | α, ⁴He²⁺ | 4 | +2 | Low | Paper, skin |
| Beta (electron) | β⁻ | 0.00055 | -1 | Medium | Al foil, plastic |
| Beta (positron) | β⁺ | 0.00055 | +1 | Medium | Al foil |
| Gamma | γ | 0 | 0 | High | Pb, concrete |
| X-ray | X | 0 | 0 | Medium-High | Pb, concrete |
| Neutron | n | 1 | 0 | High | Water, paraffin |

#### Decay Processes

##### Alpha Decay
- **Equation**: ᴬX → ᴬ⁻⁴Y + ⁴He²⁺ + Q
- **Q-value**: Energy released (typically 4-8 MeV)
- **Examples**: ²³⁸U → ²³⁴Th + α, ²²⁶Ra → ²²²Rn + α
- **Applications**: Smoke detectors, neutron sources (α,n reactions)

##### Beta Decay (β⁻)
- **Equation**: n → p + e⁻ + ν̄
- **Process**: ᴬX → ᴬY + β⁻ + ν̄
- **Energy**: Continuous spectrum up to Emax
- **Examples**: ³H → ³He + β⁻, ¹⁴C → ¹⁴N + β⁻

##### Positron Decay (β⁺)
- **Equation**: p → n + e⁺ + ν
- **Process**: ᴬX → ᴬY + β⁺ + ν
- **Annihilation**: e⁺ + e⁻ → 2γ (511 keV each)
- **Examples**: ¹¹C → ¹¹B + β⁺, ²²Na → ²²Ne + β⁺

##### Electron Capture (EC)
- **Process**: p + e⁻ → n + ν
- **Result**: Same daughter as β⁺ decay
- **X-ray emission**: Characteristic X-rays from electron shell vacancy
- **Examples**: ⁵⁵Fe (EC), ¹²⁵I (EC)

##### Gamma Emission
- **Process**: Nuclear de-excitation
- **Isomeric transition**: Metastable state → ground state
- **Internal conversion**: Energy transferred to orbital electron
- **Applications**: Medical imaging (⁹⁹mTc), industrial gauging

### Decay Kinetics

#### Basic Equations

- **Decay law**: N = N₀e^(-λt)
- **Activity**: A = λN = A₀e^(-λt)
- **Half-life**: t½ = ln(2)/λ = 0.693/λ
- **Mean life**: τ = 1/λ = t½/ln(2)

#### Activity Units
| Unit | Definition | SI Equivalent |
|------|------------|---------------|
| Becquerel (Bq) | 1 disintegration/s | 1 s⁻¹ |
| Curie (Ci) | 3.7 × 10¹⁰ d/s | 3.7 × 10¹⁰ Bq |
| mCi | 3.7 × 10⁷ Bq | - |
| μCi | 3.7 × 10⁴ Bq | - |

#### Decay Series

##### Uranium-238 Series (4n+2)
²³⁸U → ²³⁴Th → ²³⁴Pa → ²³⁴U → ²³⁰Th → ²²⁶Ra → ²²²Rn → ²¹⁸Po → ... → ²⁰⁶Pb

##### Uranium-235 Series (4n+3)
²³⁵U → ²³¹Th → ²³¹Pa → ²²⁷Ac → ²²⁷Th → ²²³Ra → ... → ²⁰⁷Pb

##### Thorium-232 Series (4n)
²³²Th → ²²⁸Ra → ²²⁸Ac → ²²⁸Th → ²²⁴Ra → ²²⁰Rn → ... → ²⁰⁸Pb

### Statistics of Counting

#### Poisson Distribution
- **Mean**: μ = n̄ (average counts)
- **Variance**: σ² = n̄
- **Standard deviation**: σ = √n̄

#### Counting Statistics
- **Standard deviation of count**: σ = √N
- **Relative standard deviation**: RSD = 1/√N
- **To achieve 1% precision**: Need 10,000 counts

#### Error Propagation
- **Net counts**: Nnet = Ngross - Nbackground
- **σnet = √(Ngross + Nbackground)**
- **Counting rate**: R = N/t, σR = √N/t = √(R/t)

#### Optimal Counting Time
For background and sample counting:
- **Optimal ratio**: ts/tb = √(Rs/Rb)
- **Minimum time for required precision**: Derived from σ requirements

### Radiation Detection

#### Gas-Filled Detectors

##### Ionization Chamber
- **Principle**: Direct collection of ion pairs
- **Voltage**: 100-300 V
- **Output**: Proportional to energy deposited
- **Applications**: Dose measurement, alpha spectroscopy

##### Proportional Counter
- **Principle**: Gas multiplication
- **Voltage**: 300-1500 V
- **Gain**: 10² - 10⁴
- **Applications**: Alpha/beta discrimination, low-level counting

##### Geiger-Müller Counter
- **Principle**: Townsend avalanche
- **Voltage**: 800-1500 V
- **Output**: Pulse (same size regardless of energy)
- **Dead time**: 50-300 μs
- **Applications**: Survey meters, contamination monitoring

#### Scintillation Detectors

##### Sodium Iodide (NaI(Tl))
- **Mechanism**: γ → scintillation → PMT → electrical pulse
- **Efficiency**: High (dense, high Z)
- **Resolution**: 6-10% at 662 keV (¹³⁷Cs)
- **Applications**: Gamma spectroscopy, medical imaging

##### Germanium Detectors (HPGe)
- **Mechanism**: Solid-state ionization
- **Efficiency**: Lower than NaI (lower Z)
- **Resolution**: 0.2-0.5% at 662 keV (superior)
- **Requirements**: Liquid nitrogen cooling
- **Applications**: High-resolution gamma spectroscopy

##### Liquid Scintillation
- **Mechanism**: β particles excite scintillator solution
- **Efficiency**: High for low-energy beta emitters
- **Applications**: ³H, ¹⁴C dating, biochemical assays
- **Quenching**: Chemical, color, optical effects

#### Semiconductor Detectors

| Detector | Material | Band Gap | Applications |
|----------|----------|----------|--------------|
| Si(Li) | Silicon | 1.1 eV | X-ray spectroscopy |
| HPGe | Germanium | 0.7 eV | Gamma spectroscopy |
| CdTe | CdTe | 1.5 eV | Portable gamma |
| CZT | CdZnTe | 1.5 eV | Room-temperature gamma |

### Neutron Activation Analysis (NAA)

#### Principle
1. Irradiate sample with neutrons
2. Elements capture neutrons → radioactive isotopes
3. Measure characteristic gamma rays
4. Identify and quantify elements

#### Reaction Types
- **(n,γ) capture**: Most common, produces isotope with +1 mass
- **(n,p)**, **(n,α)**: Fast neutron reactions
- **(n,2n)**: High-energy neutrons

#### Advantages
- Multi-element analysis (30+ elements)
- High sensitivity (ppb to ppm)
- Non-destructive (if allowed to decay)
- Matrix-independent (mostly)
- No chemical preparation needed

#### Limitations
- Requires nuclear reactor or neutron source
- Some elements not detectable (low cross-section, stable products)
- Radioactive waste generation
- Long analysis time for long-lived isotopes

#### Quantification
- **Relative method**: Compare to standards
- **Absolute method**: Use nuclear parameters
- **k₀ method**: Standardized nuclear constants

### Isotope Dilution Analysis

#### Principle
- Add known amount of spike (enriched isotope)
- Allow equilibration
- Measure isotope ratio
- Calculate original concentration

#### Equation
```
Cx = Cs × (Ws/Wx) × (As - Rm×Bs)/(Rm×Bx - Ax)
```
Where:
- Cx = concentration of analyte
- Cs = concentration of spike
- Ws, Wx = weights of spike and sample
- Rm = measured isotope ratio
- As, Ax, Bs, Bx = abundances in spike and sample

### Applications

#### Dating Methods

##### Radiocarbon Dating (¹⁴C)
- **Half-life**: 5730 years
- **Range**: ~500 - 50,000 years
- **Principle**: ¹⁴C/¹²C ratio in organic material
- **Applications**: Archaeology, geology

##### Potassium-Argon Dating
- **Half-life**: 1.25 × 10⁹ years (⁴⁰K)
- **Principle**: ⁴⁰K → ⁴⁰Ar (electron capture)
- **Range**: >100,000 years
- **Applications**: Geological dating

#### Medical Applications
- **Diagnostic**: ⁹⁹mTc imaging, PET (¹⁸F, ¹¹C)
- **Therapeutic**: ¹³¹I (thyroid), ⁶⁰Co (external beam)

#### Industrial Applications
- **Tracer studies**: Flow measurement, leak detection
- **Thickness gauging**: Beta, gamma transmission
- **Density measurement**: Gamma backscatter

---

## Decision Flow: Detector Selection

```
START: What radiation is being measured?
│
├── Alpha particles →
│   ├── Spectroscopy → Silicon surface barrier
│   └── Survey/counting → ZnS scintillation, proportional
│
├── Beta particles →
│   ├── Low energy → Liquid scintillation
│   ├── High energy → Plastic scintillator, GM tube
│   └── Spectroscopy → Plastic scintillator
│
├── Gamma rays →
│   ├── High resolution needed → HPGe detector
│   ├── High efficiency needed → NaI(Tl)
│   ├── Field use → NaI(Tl) or CZT
│   └── Low cost → NaI(Tl)
│
├── Neutrons →
│   ├── Thermal → BF₃/³He proportional
│   ├── Fast → Organic scintillator
│   └── Spectroscopy → Liquid scintillator (recoil proton)
│
└── X-rays →
    ├── High resolution → Si(Li) or SDD
    └── General purpose → NaI(Tl) thin crystal
```

---

## Key Formulas

| Quantity | Formula | Notes |
|----------|---------|-------|
| Decay law | N = N₀e^(-λt) | Exponential decay |
| Half-life | t½ = 0.693/λ | Time for half to decay |
| Activity | A = λN | Disintegrations per time |
| Counting uncertainty | σ = √N | Poisson statistics |
| Relative uncertainty | σ/N = 1/√N | Precision = 1/√N |
| Net count uncertainty | σnet = √(Ns + Nb) | Sample - background |
| Decay constant | λ = ln(2)/t½ | Per unit time |
| Energy resolution | ΔE/E (FWHM) | Spectrometer quality |

---

## Safety Considerations

### Exposure Limits
| Category | Limit | Notes |
|----------|-------|-------|
| Occupational (whole body) | 50 mSv/year | Tracked, averaged |
| Occupational (extremity) | 500 mSv/year | Hands, feet |
| Public | 1 mSv/year | Excluding medical |
| Pregnant worker | 5 mSv/gestation | Fetal dose |

### Shielding
| Radiation | Material | Principle |
|-----------|----------|-----------|
| Alpha | Paper, air | Stopped easily |
| Beta | Plastic, Al | Low-Z to avoid bremsstrahlung |
| Gamma | Pb, concrete | Dense material, thickness by energy |
| Neutron | H₂O, polyethylene | Moderation + capture |

### ALARA Principle
- **A**s **L**ow **A**s **R**easonably **A**chievable
- Time, distance, shielding
- Monitoring and training
- Contamination control

---

## Links to Other Layers

### L3 (Executable Code)
- `../L3_code/decay_calculator.py` - Decay calculations
- `../L3_code/counting_stats.py` - Statistical analysis
- `../L3_code/naa_analysis.py` - NAA data reduction

### L4 (Reference Data)
- Nuclear decay data tables
- Gamma ray energies and intensities
- Neutron cross-sections
- Shielding thickness tables

### L5 (Examples)
- Gamma spectrum interpretation
- ¹⁴C dating calculation
- Neutron activation analysis of geological sample

---

## Common Analytical Applications

| Technique | Isotopes Used | Detection Limit | Application |
|-----------|---------------|-----------------|-------------|
| Liquid scintillation | ³H, ¹⁴C | Very low | Biochemical tracing |
| Gamma spectroscopy | Various γ emitters | nCi range | Environmental monitoring |
| NAA | Neutron capture products | ppb-ppm | Multi-element analysis |
| Isotope dilution MS | Stable/radioactive | ppt-ppb | High-precision quantitation |
| Radiocarbon dating | ¹⁴C | 1% age uncertainty | Archaeology, geology |
