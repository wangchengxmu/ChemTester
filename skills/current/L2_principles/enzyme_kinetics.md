# L2 Topic: Enzyme Kinetics

**Source**: Fundamentals of Biochemistry (Jakubowski and Flatt), Ch6
**Created**: 2026-03-13
**Status**: Scaffold (Pass-2)

---

## Concept Overview

Enzyme kinetics quantifies the rates of enzyme-catalyzed reactions. The Michaelis-Menten model is the foundation of enzyme kinetic analysis.

### Key Features
1. **Michaelis-Menten equation**: vâ = Vmax[S]/(KM + [S])
2. **Hyperbolic saturation**: Rate increases with [S] to Vmax
3. **KM is substrate concentration at half-maximal velocity**
4. **kcat/KM measures catalytic efficiency**

---

## Core Principles

### Michaelis-Menten Parameters
| Parameter | Definition | Units |
|-----------|------------|-------|
| Vmax | Maximum velocity | M/s |
| KM | Michaelis constant | M |
| kcat | Turnover number | sâ»Â?|
| kcat/KM | Catalytic efficiency | Mâ»Â¹sâ»Â?|

### Key Relationships
```
v = Vmax[S]/(KM + [S])
Vmax = kcat Ã [Eâ]
KM = [S] when v = Vmax/2
```

### Graphical Analysis
- **v vs [S]**: Hyperbolic curve
- **Lineweaver-Burk (1/v vs 1/[S])**: Linear
- **Eadie-Hofstee (v vs v/[S])**: Linear

---

## Decision Trees

### Determining Inhibition Type
```
KM increased, Vmax unchanged? â?Competitive
Vmax decreased, KM unchanged? â?Noncompetitive
Both decreased? â?Uncompetitive
```

### Estimating Efficiency
```
kcat/KM > 10â?Mâ»Â¹sâ»Â? â?Diffusion-limited
kcat/KM 10â?10â? â?Moderate
kcat/KM < 10â? â?Low efficiency
```

---

## Key Tables

### Special Cases
| Condition | Velocity | Order |
|-----------|----------|-------|
| [S] >> KM | v â?Vmax | Zero order |
| [S] = KM | v = Vmax/2 | - |
| [S] << KM | v â?(Vmax/KM)[S] | First order |

### Inhibition Effects
| Type | KM | Vmax | Lineweaver-Burk |
|------|-----|------|-----------------|
| Competitive | â?| â?| Same y-intercept |
| Noncompetitive | â?| â?| Same x-intercept |
| Uncompetitive | â?| â?| Parallel |

---

## Connected Topics

- **Upstream**: [chemical_kinetics.md](chemical_kinetics.md)
- **Related**: [metabolic_pathways.md](metabolic_pathways.md)

---

## L3 Tools Required

1. `enzyme_kinetics_tools.py` - Michaelis-Menten calculations

---

## L4 References (TODO)

- [ ] Enzyme KM and kcat tables
- [ ] Inhibition constants

---

## L5 Worked Examples (TODO)

- [ ] KM determination from data
- [ ] Turnover number calculation


## Implementations
- Implementation: `../L3_functions/enzym_kinetics_tools.py`

- Implementation: `../L3_functions/enzyme_kinetics.py`

## L3 Tool Call Directives

**Source:** `enzyme_kinetics_tools.py`

When you encounter enzyme kinetics problems, follow this decision tree:

### Available functions:
- `michaelis_menten_kinetics(substrate_conc: float, KM: float, Vmax: float, enzyme_conc: Optional[float])` → Dict — Calculate reaction velocity using Michaelis-Menten equation.
- `lineweaver_burk_plot(substrate_concs: List[float], velocities: List[float])` → Dict — Determine KM and Vmax from Lineweaver-Burk (double reciprocal) plot.
- `eadie_hofstee_plot(substrate_concs: List[float], velocities: List[float])` → Dict — Determine KM and Vmax from Eadie-Hofstee plot.
- `hanes_woolf_plot(substrate_concs: List[float], velocities: List[float])` → Dict — Determine KM and Vmax from Hanes-Woolf plot.
- `inhibition_analysis(control_data: List[Tuple[float, float]], inhibited_data: List[Tuple[float, float]], inhibitor_conc: float)` → Dict — Analyze enzyme inhibition from control and inhibited kinetics.
- `turnover_number(Vmax: float, enzyme_conc: float)` → Dict — Calculate turnover number (kcat) from Vmax and enzyme concentration.
- `substrate_concentration_for_velocity(target_velocity: float, KM: float, Vmax: float)` → Dict — Calculate substrate concentration needed to achieve target velocity.
- `classify_catalytic_efficiency(catalytic_efficiency: float)` → str — Classify catalytic efficiency (kcat/KM).
- `compare_kinetic_methods(substrate_concs: List[float], velocities: List[float])` → Dict — Compare KM and Vmax from different linearization methods.

### Common errors:
- ❌ Passing wrong units (check function docstring for expected units)
- ❌ Omitting required parameters
