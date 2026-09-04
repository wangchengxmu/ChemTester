---
id: electrical_circuits_instrumentation
layer: 2
title: Electrical Components and Circuits for Instrumentation
stability: high
confidence: high
constraints:
  - Focus on instrumentation applications
  - Emphasize signal conditioning and measurement circuits
last_verified: 2026-03-17
source: Skoog Principles of Instrumental Analysis, Ch2
---

## Core Concepts

### Passive Components

#### Resistors
- **Ohm's Law**: V = IR
- **Power dissipation**: P = I²R = V²/R
- **Temperature coefficient**: R(T) = R₀[1 + α(T - T₀)]
- **Types for instrumentation**:
  - Metal film (precision, low noise)
  - Wire-wound (high power)
  - Thermistor (temperature sensing)

#### Capacitors
- **Capacitance**: C = Q/V = ε₀εᵣA/d
- **Energy stored**: E = ½CV²
- **Impedance**: Xc = 1/(jωC) = 1/(2πfC)
- **Types**: Ceramic, electrolytic, film, tantalum
- **Applications**: Filtering, coupling, timing circuits

#### Inductors
- **Inductance**: L = NΦ/I
- **Energy stored**: E = ½LI²
- **Impedance**: XL = jωL = 2πfL
- **Applications**: Chokes, transformers, filters

### Circuit Analysis

#### Kirchhoff's Laws
1. **Current Law (KCL)**: ΣI (node) = 0
2. **Voltage Law (KVL)**: ΣV (loop) = 0

#### Series and Parallel Combinations
- **Resistors in series**: Rs = R₁ + R₂ + ...
- **Resistors in parallel**: 1/Rp = 1/R₁ + 1/R₂ + ...
- **Capacitors in series**: 1/Cs = 1/C₁ + 1/C₂ + ...
- **Capacitors in parallel**: Cp = C₁ + C₂ + ...

### RC and RL Circuits

#### RC Circuit (Low-Pass Filter)
```
Vin ---[R]---+--- Vout
             |
            [C]
             |
            GND
```
- **Transfer function**: H(f) = 1/(1 + jf/fc)
- **Cutoff frequency**: fc = 1/(2πRC)
- **Time constant**: τ = RC
- **Step response**: V(t) = V₀(1 - e^(-t/τ))

#### RC High-Pass Filter
```
Vin ---[C]---+--- Vout
             |
            [R]
             |
            GND
```
- **Transfer function**: H(f) = jf/fc / (1 + jf/fc)
- **Cutoff frequency**: fc = 1/(2πRC)

#### RL Circuit
- **Time constant**: τ = L/R
- **Low-pass cutoff**: fc = R/(2πL)
- **High-pass cutoff**: fc = R/(2πL)

### Impedance and AC Analysis

#### Complex Impedance
- **Resistor**: ZR = R
- **Capacitor**: ZC = 1/(jωC) = -j/(ωC)
- **Inductor**: ZL = jωL
- **Series combination**: Ztotal = Z₁ + Z₂ + ...
- **Parallel combination**: 1/Ztotal = 1/Z₁ + 1/Z₂ + ...

#### Phasor Analysis
- **Voltage phasor**: V = Vm∠φ
- **Current phasor**: I = Im∠θ
- **Power factor**: cos(φ - θ)

### Bridge Circuits

#### Wheatstone Bridge
```
    R1         R2
Vin ----+----+---- Vout
         |    |
        [R3] [Rx]  (unknown)
         |    |
GND -----+----+
```
- **Balance condition**: R₁/R₂ = R₃/Rx
- **Sensitivity**: Maximum when all resistances equal
- **Applications**: Strain gauges, resistance thermometers, conductivity measurements

#### AC Bridges
- **Maxwell bridge**: Measures inductance
- **Wien bridge**: Measures capacitance, oscillator frequency
- **Schering bridge**: High-voltage capacitance measurement

### Noise in Electrical Circuits

#### Noise Types
1. **Thermal (Johnson) noise**: Vn = √(4kTRΔf)
2. **Shot noise**: In = √(2qIΔf)
3. **Flicker (1/f) noise**: Power ∝ 1/f
4. **Contact noise**: Variable resistance

#### Signal-to-Noise Ratio
- **SNR (power)**: S/N = Psignal/Pnoise
- **SNR (voltage)**: S/N = Vsignal/Vnoise
- **Noise figure**: NF = 10 log(SNRin/SNRout)

### Grounding and Shielding

#### Ground Types
- **Signal ground**: Reference for measurements
- **Chassis ground**: Safety and shielding
- **Earth ground**: Safety connection

#### Shielding Principles
- **Electrostatic shielding**: Faraday cage, conductive enclosures
- **Magnetic shielding**: Mu-metal, high-permeability materials
- **Guard circuits**: Driven shields for high-impedance measurements

---

## Decision Flow: Circuit Selection for Signal Conditioning

```
START: What type of signal conditioning?
│
├── Filter noise → 
│   ├── Low-frequency noise → Low-pass RC/RL filter (fc above signal band)
│   ├── High-frequency noise → High-pass filter (fc below signal band)
│   └── Both → Band-pass or cascaded LP+HP
│
├── Amplify signal →
│   ├── High source impedance → FET input amplifier
│   ├── Low source impedance → BJT input amplifier
│   └── Differential signal → Instrumentation amplifier
│
├── Measure resistance →
│   ├── Direct measurement → Ohmmeter circuit
│   ├── High accuracy → Wheatstone bridge
│   └── Small changes → Bridge with amplifier
│
└── Isolate signal →
    ├── Transformer isolation → AC signals
    └── Optical isolation → Digital/DC signals
```

---

## Key Formulas

| Quantity | Formula | Units |
|----------|---------|-------|
| Ohm's Law | V = IR | V, A, Ω |
| Power | P = I²R = V²/R | W |
| RC time constant | τ = RC | s |
| RL time constant | τ = L/R | s |
| Low-pass cutoff | fc = 1/(2πRC) | Hz |
| High-pass cutoff | fc = 1/(2πRC) | Hz |
| Capacitive reactance | Xc = 1/(2πfC) | Ω |
| Inductive reactance | XL = 2πfL | Ω |
| Thermal noise | Vn = √(4kTRΔf) | V |
| Q factor | Q = fc/Δf | - |

---

## Links to Other Layers

### L3 (Executable Code)
- `../L3_code/circuit_analysis.py` - RC/RL filter calculator
- `../L3_code/noise_calculator.py` - Thermal noise estimation

### L4 (Reference Data)
- Standard resistor values (E-series)
- Capacitor dielectric properties
- Temperature coefficients for common materials

### L5 (Examples)
- pH meter input circuit analysis
- Thermocouple signal conditioning
- Photodiode amplifier design

---

## Common Instrumentation Applications

| Application | Circuit Type | Key Consideration |
|-------------|--------------|-------------------|
| pH measurement | High-impedance buffer | Input >10¹² Ω |
| Thermocouple | Differential amplifier | Cold junction compensation |
| Strain gauge | Wheatstone bridge | Temperature compensation |
| Photodiode | Transimpedance amplifier | Low noise, high bandwidth |
| Conductivity | AC bridge | Frequency selection |
