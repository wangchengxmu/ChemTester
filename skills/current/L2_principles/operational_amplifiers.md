---
id: operational_amplifiers
layer: 2
title: Operational Amplifiers in Chemical Instrumentation
stability: high
confidence: high
constraints:
  - Focus on instrumentation amplifier configurations
  - Emphasize signal conditioning applications
last_verified: 2026-03-17
source: Skoog Principles of Instrumental Analysis, Ch3
---

## Core Concepts

### Ideal Op-Amp Characteristics

| Parameter | Ideal Value | Typical Real Value |
|-----------|-------------|-------------------|
| Open-loop gain (Aol) | ∞ | 10⁵ - 10⁷ |
| Input impedance (Zin) | ∞ | 10⁶ - 10¹² Ω |
| Output impedance (Zout) | 0 | 10 - 100 Ω |
| Bandwidth | ∞ | 1 - 100 MHz (unity gain) |
| CMRR | ∞ | 80 - 120 dB |
| Slew rate | ∞ | 0.5 - 1000 V/μs |
| Input offset voltage | 0 | 10 μV - 5 mV |
| Input bias current | 0 | 1 pA - 1 μA |

### Golden Rules for Ideal Op-Amps

1. **No current flows into inputs**: I+ = I- = 0
2. **Inputs are at the same voltage**: V+ = V- (when in negative feedback)

---

## Basic Amplifier Configurations

### Inverting Amplifier
```
        Rf
    +---[R]---+
    |         |
Vin-[Rin]-+  |--- Vout
          |  |
         [-] |
          |  |
         [+] |
          |  |
         GND GND
```

- **Gain**: Av = -Rf/Rin
- **Input impedance**: Zin = Rin
- **Output impedance**: Zout ≈ 0

### Non-Inverting Amplifier
```
         +----[R1]---+
         |           |
        [+]        [R2]
Vin-----|            |
        [-]         GND
         |
        GND
```

- **Gain**: Av = 1 + R2/R1
- **Input impedance**: Very high (∞ ideal)
- **Output impedance**: Zout ≈ 0

### Voltage Follower (Buffer)
```
        [+]
Vin-----|------ Vout
        [-]
         |
        Vout
```

- **Gain**: Av = 1
- **Purpose**: Impedance transformation, isolation
- **Input impedance**: Very high

### Summing Amplifier
```
         Rf
    +---[R]---+
    |         |
V1-[R1]-+     |
        |     |
V2-[R2]-+[-]  |--- Vout
        |     |
V3-[R3]-+[+]  |
         |    |
        GND  GND
```

- **Output**: Vout = -Rf(V1/R1 + V2/R2 + V3/R3)
- **Applications**: DAC, signal mixing, averaging

### Difference Amplifier
```
         Rf
    +---[R]---+
    |         |
V1-[R1]-+[-]  |--- Vout
        |     |
V2-[R2]-+[+]  |
        |     |
       [R3]   |
        |     |
       GND   GND
```

- **Output**: Vout = (Rf/R1)(V2 - V1) (when R1 = R2, R3 = Rf)
- **CMRR**: Depends on resistor matching

---

## Instrumentation Amplifier

### Three-Op-Amp Configuration
```
        Rg
    +---[R]---+
    |         |
   [R]       [R]
    |         |
V1-+--[+][-]--+--[R]--+
    |         |       |
   [+][-]----[+]     [R]--- Vout
    |         |       |
V2-+--[-][+]--+--[R]--+
    |         |
   [R]       [R]
    |         |
    +---[R]---+
        Rg
```

- **Gain**: G = 1 + 2R/Rg
- **Features**: High CMRR, high input impedance, adjustable gain
- **Applications**: Bridge sensors, strain gauges, thermocouples, EEG/ECG

### Performance Parameters
| Parameter | Typical Value | Importance |
|-----------|---------------|------------|
| CMRR | 80-120 dB | Rejects common-mode noise |
| Input impedance | 10⁹ - 10¹² Ω | Doesn't load signal source |
| Gain range | 1 - 10,000 | Versatile |
| Offset drift | 0.1-5 μV/°C | Precision measurements |

---

## Active Filters

### Low-Pass Filter (Sallen-Key)
```
            R
Vin---[R]---+---[R]---+--- Vout
            |          |
           [C]       [C]
            |          |
           GND        [+]
                      |
                     GND
```

- **Cutoff frequency**: fc = 1/(2π√(R1R2C1C2))
- **Butterworth response**: Q = 0.707

### High-Pass Filter
- **Cutoff frequency**: fc = 1/(2π√(R1R2C1C2))
- **Applications**: Removing DC offset, AC coupling

### Band-Pass Filter
- **Center frequency**: f₀ = 1/(2πRC)
- **Bandwidth**: BW = fc/Q

### Notch (Band-Reject) Filter
- **Applications**: Removing 50/60 Hz line noise
- **Twin-T configuration**: Deep notch at center frequency

---

## Specialized Amplifier Configurations

### Transimpedance Amplifier (TIA)
```
        Rf
    +---[R]---+
    |         |
Iin-+[+]     |--- Vout
    |         |
   [-]---+---+
         |
        Cf (feedback capacitor)
         |
        GND
```

- **Output voltage**: Vout = -Iin × Rf
- **Applications**: Photodiode amplifiers, current-to-voltage conversion
- **Stability**: Cf required for stability with capacitive sources

### Charge Amplifier
```
        Cf
    +---[C]---+
    |         |
Qin-+[+]     |--- Vout
    |         |
   [-]       Rf (for DC feedback)
    |         |
   GND       GND
```

- **Output voltage**: Vout = -Qin/Cf
- **Applications**: Piezoelectric sensors, capacitive transducers

### Logarithmic Amplifier
```
        Diode
    +---[>|]---+
    |          |
Vin-[R]--+     |
         |     |
        [-]   [+]
         |     |
        [+]   GND
         |
        Vout
```

- **Output**: Vout = -VT ln(Vin/IsR)
- **Applications**: pH meters, spectrophotometry, concentration measurement

---

## Feedback and Stability

### Negative Feedback Benefits
1. **Gain stabilization**: Less dependent on op-amp parameters
2. **Bandwidth extension**: Gain-bandwidth product constant
3. **Reduced distortion**: Linear operation
4. **Impedance control**: Input/output impedance modification

### Gain-Bandwidth Product
- **Relationship**: GBWP = Av × f(-3dB)
- **Unity-gain bandwidth**: GBWP (when Av = 1)

### Stability Criteria
- **Phase margin**: Should be > 45° for stability
- **Bode plot analysis**: Check for 180° phase shift before unity gain
- **Compensation**: Lead, lag, or lead-lag networks

---

## Practical Considerations

### Offset Voltage and Drift
- **Nulling**: External trim potentiometer
- **Auto-zero**: Chopper-stabilized amplifiers
- **Temperature drift**: Typically 0.1-10 μV/°C

### Bias Current Effects
- **FET input op-amps**: Ibias ~ 1 pA - 1 nA
- **BJT input op-amps**: Ibias ~ 10 nA - 1 μA
- **Cancellation**: Use equal resistance at both inputs

### Noise Performance
- **Voltage noise density**: 1-100 nV/√Hz
- **Current noise density**: 0.1-10 fA/√Hz (FET), 0.1-10 pA/√Hz (BJT)
- **Total noise**: Vn,total = √(Vn² + (In×Rs)² + 4kTRs)

---

## Decision Flow: Op-Amp Selection

```
START: What is the application?
│
├── High-impedance source (>1MΩ) →
│   ├── DC/low frequency → FET-input op-amp
│   └── High frequency → Low-input-capacitance FET
│
├── Low-impedance source (<10kΩ) →
│   ├── Low noise critical → Low-voltage-noise BJT
│   └── General purpose → Standard BJT op-amp
│
├── Precision DC measurement →
│   ├── Auto-zero/chopper stabilized
│   └── Low offset drift (<1μV/°C)
│
├── High-speed application →
│   ├── Check slew rate > signal requirement
│   └── Check bandwidth > signal frequency
│
└── Differential measurement →
    ├── High CMRR required → Instrumentation amplifier
    └── General purpose → Difference amplifier
```

---

## Key Formulas

| Configuration | Gain Formula | Input Impedance |
|---------------|--------------|-----------------|
| Inverting | -Rf/Rin | Rin |
| Non-inverting | 1 + R2/R1 | Very high |
| Voltage follower | 1 | Very high |
| Difference | Rf/R1(V2-V1) | Depends on resistors |
| Instrumentation | 1 + 2R/Rg | Very high |
| Transimpedance | -Rf | ~0 (virtual ground) |

---

## Links to Other Layers

### L3 (Executable Code)
- `../L3_code/opamp_calculator.py` - Gain, bandwidth calculations
- `../L3_code/filter_design.py` - Active filter design tools

### L4 (Reference Data)
- Popular op-amp specifications comparison
- Noise calculation examples
- Standard resistor values for gain setting

### L5 (Examples)
- Photodiode TIA design example
- pH meter amplifier circuit
- Thermocouple signal conditioning
- EEG/ECG front-end design

---

## Common Instrumentation Applications

| Application | Configuration | Key Op-Amp Requirement |
|-------------|---------------|----------------------|
| pH electrode | Voltage follower/buffer | Input >10¹² Ω, low bias current |
| Photodiode | Transimpedance | Low noise, high bandwidth |
| Strain gauge | Instrumentation amp | High CMRR, low drift |
| Thermocouple | Difference amp | Cold junction compensation |
| Potentiometric sensor | Voltage follower | High input impedance |
| Conductivity cell | AC amplifier | Frequency stability |
