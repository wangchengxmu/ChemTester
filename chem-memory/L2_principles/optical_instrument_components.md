---
id: optical_instrument_components
layer: 2
title: Components of Optical Instruments
stability: high
confidence: high
constraints:
  - Focus on spectroscopic instrumentation
  - Emphasize component selection and trade-offs
last_verified: 2026-03-17
source: Skoog Principles of Instrumental Analysis, Ch7
---

## Core Concepts

### Light Sources

#### Continuum Sources

##### Tungsten-Halogen Lamp
- **Spectral range**: 320-2500 nm (visible-NIR)
- **Color temperature**: 2800-3000 K
- **Lifetime**: 500-2000 hours
- **Applications**: UV-Vis-NIR spectroscopy, colorimetry
- **Features**: Stable output, simple operation

##### Deuterium Lamp
- **Spectral range**: 160-400 nm (UV)
- **Output**: Continuous with emission lines
- **Lifetime**: 1000-2000 hours
- **Applications**: UV spectroscopy, HPLC-UV detectors
- **Features**: Requires UV-transmitting windows (quartz)

##### Xenon Arc Lamp
- **Spectral range**: 200-1000+ nm (UV-Vis-NIR)
- **Output**: High intensity, continuous + line spectrum
- **Lifetime**: 500-2000 hours
- **Applications**: Fluorescence, high-intensity applications
- **Features**: High brightness, stable output

##### Globar (Silicon Carbide)
- **Spectral range**: 1-40 μm (IR)
- **Temperature**: ~1300 K
- **Applications**: IR spectroscopy, FTIR
- **Features**: Nernst glower alternative

#### Line Sources

##### Hollow Cathode Lamp (HCL)
- **Output**: Sharp atomic emission lines
- **Elements**: Available for most elements
- **Applications**: Atomic absorption spectroscopy (AAS)
- **Features**: Narrow linewidth (<0.01 nm)

##### Electrodeless Discharge Lamp (EDL)
- **Output**: Brighter than HCL
- **Elements**: As, Se, Te, and others
- **Applications**: AAS for volatile elements
- **Features**: Higher intensity, better detection limits

##### Mercury Lamp
- **Output**: Discrete lines (254, 313, 365, 405, 436, 546, 578 nm)
- **Applications**: Fluorescence, calibration
- **Features**: Sharp lines, high intensity at specific wavelengths

#### Laser Sources

| Laser Type | Wavelength(s) | Power | Applications |
|------------|---------------|-------|--------------|
| He-Ne | 632.8 nm | 0.5-50 mW | Alignment, Raman |
| Argon ion | 488, 514 nm | 0.1-5 W | Raman, fluorescence |
| Diode | 630-1000+ nm | 1-500 mW | Raman, spectroscopy |
| Nd:YAG | 1064 nm (fundamental) | 1-100 W | LIBS, Raman |
| Ti:Sapphire | 700-1000 nm (tunable) | 0.1-5 W | Spectroscopy |
| Dye laser | Tunable (visible) | Variable | High-resolution spectroscopy |

---

### Wavelength Selection Devices

#### Filters

##### Absorption Filters
- **Mechanism**: Absorbs unwanted wavelengths
- **Bandwidth**: 30-250 nm
- **Applications**: Rough wavelength selection
- **Cost**: Low

##### Interference Filters
- **Mechanism**: Constructive/destructive interference
- **Bandwidth**: 1-20 nm (typical)
- **Peak transmission**: 40-80%
- **Applications**: Fluorescence, photometry
- **Features**: Can be tunable (tilt)

##### Neutral Density Filters
- **Purpose**: Attenuate light uniformly
- **Optical density range**: 0.1 - 4.0
- **Applications**: Preventing detector saturation

##### Long-pass / Short-pass Filters
- **Long-pass**: Transmit λ > cutoff
- **Short-pass**: Transmit λ < cutoff
- **Applications**: Order sorting, blocking unwanted light

#### Monochromators

##### Czerny-Turner Configuration
```
              [Collimating     [Focusing
[Entrance] →   Mirror] →       Mirror] → [Exit]
  Slit           ↓               ↓        Slit
               [Grating]
```

- **Features**: Versatile, good stray light rejection
- **Resolution**: 0.1-1 nm typical
- **Scan speed**: Motor-driven grating rotation

##### Ebert Configuration
- **Features**: Single mirror for collimation and focusing
- **Advantages**: Compact, fewer optical surfaces

##### Concave Holographic Grating
- **Features**: Single optical element
- **Advantages**: No mirrors needed, compact
- **Applications**: Miniature spectrometers

#### Grating Parameters

| Parameter | Definition | Typical Values |
|-----------|------------|----------------|
| Groove density | Lines per mm | 300-3600 lines/mm |
| Blaze wavelength | Maximum efficiency | Design-dependent |
| Resolution | λ/Δλ | R = nN (n = order, N = illuminated grooves) |
| Free spectral range | Wavelength range without overlap | λ/n |

#### Prisms

- **Mechanism**: Refraction and dispersion
- **Materials**: Glass (visible), quartz (UV), NaCl/KBr (IR)
- **Resolution**: Lower than gratings
- **Features**: No overlapping orders, good stray light rejection

#### Interferometers

##### Michelson Interferometer (FTIR)
```
               [Mirror]
                  ↑
[Source] → [BS] ← → [Fixed Mirror]
            ↓
         [Detector]
```

- **Resolution**: Δν = 1/(maximum retardation)
- **Advantages**: Fellgett advantage (multiplex), Jacquinot advantage (throughput)
- **Applications**: FTIR spectroscopy

---

### Detectors

#### Photon Detectors

##### Photomultiplier Tube (PMT)
- **Principle**: Photoelectric effect + electron multiplication
- **Spectral range**: 160-900 nm (depends on photocathode)
- **Gain**: 10⁶ - 10⁸
- **Dark current**: 10⁻¹² - 10⁻⁹ A
- **Response time**: <1 ns
- **Applications**: UV-Vis spectroscopy, fluorescence, scintillation counting

| Photocathode | Range | Peak QE |
|--------------|-------|---------|
| Cs-Te | 160-320 nm | 20% (solar blind) |
| Bialkali | 200-650 nm | 25% |
| Multialkali | 200-850 nm | 20% |
| GaAs | 300-900 nm | 30% |

##### Photodiodes

###### Silicon Photodiode
- **Spectral range**: 200-1100 nm
- **Peak sensitivity**: ~900 nm
- **QE**: 80-90% at peak
- **Response time**: ns to μs
- **Applications**: General photometry, power meters

###### PIN Photodiode
- **Features**: Fast response, low noise
- **Response time**: <10 ns
- **Applications**: High-speed detection

###### Avalanche Photodiode (APD)
- **Gain**: 50-200 (internal)
- **Advantages**: Higher sensitivity than PIN
- **Disadvantages**: Higher noise, requires high voltage
- **Applications**: Low-light detection, LIDAR

##### CCD (Charge-Coupled Device)
- **Architecture**: Array of photodiodes
- **Spectral range**: 200-1100 nm (back-illuminated: 180-1100 nm)
- **Features**: High QE (90%), multichannel detection
- **Read noise**: 2-20 electrons
- **Applications**: Spectroscopy (array detectors), imaging

##### CMOS Image Sensors
- **Architecture**: Active pixel sensors
- **Advantages**: Lower cost, lower power, faster readout
- **Disadvantages**: Higher noise per pixel
- **Applications**: Consumer imaging, industrial cameras

#### Thermal Detectors

##### Thermocouple
- **Principle**: Seebeck effect (temperature → voltage)
- **Spectral range**: Broad (IR)
- **Response time**: Slow (ms)
- **Applications**: IR spectroscopy, power measurement

##### Thermopile
- **Architecture**: Multiple thermocouples in series
- **Sensitivity**: Higher than single thermocouple
- **Applications**: IR thermometry, gas sensing

##### Pyroelectric Detector
- **Principle**: Temperature change → charge
- **Features**: AC only (responds to change)
- **Response time**: Fast (μs)
- **Applications**: FTIR, motion detection, laser power

##### Bolometer
- **Principle**: Resistance change with temperature
- **Sensitivity**: Very high (cooled)
- **Applications**: Far-IR, THz spectroscopy

#### Detector Comparison Table

| Detector | Wavelength Range | Sensitivity | Speed | Key Feature |
|----------|------------------|-------------|-------|-------------|
| PMT | UV-Vis-NIR | Highest | Fast | High gain |
| Si Photodiode | UV-Vis-NIR | High | Fast | Simple |
| APD | UV-Vis-NIR | Very high | Fast | Internal gain |
| CCD | UV-Vis-NIR | Very high | Medium | Multichannel |
| InGaAs | NIR | High | Fast | NIR optimized |
| Thermopile | Broad IR | Medium | Slow | Broadband |
| Pyroelectric | IR | Medium | Medium | AC response |

---

### Optical Components

#### Mirrors
- **Front-surface**: No absorption, better for UV
- **Rear-surface**: Protected, but secondary reflection
- **Coatings**: Al (general), Au (IR), Ag (high reflectivity)

#### Lenses
- **Materials**: Glass, quartz (UV), CaF₂ (UV-IR), Ge (IR)
- **Aberrations**: Spherical, chromatic, coma
- **Focusing**: Trade-off between speed and aberrations

#### Windows and Prisms
- **Materials**: Selected for wavelength range
- **Transmission**: Critical for sensitivity

#### Optical Fibers
- **Core/cladding**: Light guiding by TIR
- **Materials**: Silica (UV-Vis-NIR), fluoride glass (IR)
- **Numerical aperture**: Light collection efficiency
- **Applications**: Remote sensing, process monitoring

---

## Decision Flow: Component Selection

### Light Source Selection
```
START: What spectral range?
│
├── UV (160-400 nm) →
│   ├── Continuum → Deuterium lamp
│   ├── Atomic lines → Hollow cathode lamp
│   └── High intensity → Xenon arc
│
├── Visible (400-700 nm) →
│   ├── Broadband → Tungsten-halogen
│   ├── High intensity → Xenon arc
│   └── Coherent → Laser (HeNe, Ar+)
│
├── NIR (700-2500 nm) →
│   └── Tungsten-halogen
│
└── IR (>2500 nm) →
    ├── Globar
    └── Nernst glower
```

### Detector Selection
```
START: What are the requirements?
│
├── Need single-point detection? →
│   ├── Low light → PMT or APD
│   ├── Moderate light → Silicon photodiode
│   └── NIR region → InGaAs photodiode
│
├── Need multichannel detection? →
│   ├── UV-Vis-NIR → CCD array
│   └── High speed → CMOS sensor
│
├── IR detection? →
│   ├── Near-IR → InGaAs
│   ├── Mid-IR → MCT (HgCdTe), InSb
│   └── Far-IR → Bolometer, pyroelectric
│
└── Low cost priority? →
    └── Silicon photodiode
```

### Wavelength Selector Selection
```
START: What resolution and flexibility?
│
├── Fixed wavelength → Interference filter
│
├── Scanning, moderate resolution →
│   └── Czerny-Turner monochromator
│
├── High resolution →
│   ├── High groove density grating
│   └── Echelle grating
│
├── Multichannel →
│   └── Polychromator + CCD array
│
└── IR, high throughput →
    └── Michelson interferometer (FTIR)
```

---

## Key Formulas

| Parameter | Formula | Notes |
|-----------|---------|-------|
| Grating equation | mλ = d(sin α + sin β) | m = order, d = groove spacing |
| Resolution (grating) | R = nN | n = order, N = illuminated grooves |
| Dispersion | dλ/dx = (d cos β)/(mf) | Linear dispersion |
| QE | η = electrons out / photons in | Quantum efficiency |
| PMT gain | G = δⁿ | δ = dynode gain, n = stages |
| FTIR resolution | Δν = 1/Δx | Δx = max optical path difference |

---

## Links to Other Layers

### L3 (Executable Code)
- `../L3_code/spectral_calculator.py` - Wavelength, energy conversions
- `../L3_code/detector_noise.py` - Noise analysis for detectors
- `../L3_code/grating_calculator.py` - Grating parameters

### L4 (Reference Data)
- Photocathode spectral response curves
- Detector NEP specifications
- Optical material transmission curves

### L5 (Examples)
- UV-Vis spectrophotometer design
- Fluorescence spectrometer configuration
- FTIR instrument layout

---

## Common Instrument Configurations

| Instrument | Source | Selector | Detector | Application |
|------------|--------|----------|----------|-------------|
| UV-Vis spectrometer | D₂/W lamp | Monochromator | PMT/Si PD | Absorbance |
| Fluorometer | Xe lamp | Monochromators (2) | PMT | Fluorescence |
| AAS | HCL | Monochromator | PMT | Elemental analysis |
| FTIR | Globar | Interferometer | MCT/DLATGS | Molecular structure |
| ICP-OES | Plasma | Polychromator | CCD/PMT | Multi-element |
| Raman spectrometer | Laser | Notch filter + spectrograph | CCD | Molecular fingerprint |
