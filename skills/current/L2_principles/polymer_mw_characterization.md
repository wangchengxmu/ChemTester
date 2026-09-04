# Polymer Molecular Weight Characterization

[Source: Polymer Physics (Steimel), Ch6-8]

## Core Concept

Polymers have a distribution of molecular weights. Key techniques for characterization include osmometry, light scattering, viscosity, and size exclusion chromatography (SEC/GPC).

## Average Molecular Weights

| Average | Symbol | Method | Sensitivity |
|---------|--------|--------|-------------|
| Number average | $M_n$ | Osmometry | Favors low MW |
| Weight average | $M_w$ | Light scattering | Favors high MW |
| Viscosity average | $M_v$ | Viscometry | Intermediate |
| Z-average | $M_z$ | Ultracentrifuge | Favors highest MW |

### Definitions

$$M_n = \frac{\sum n_i M_i}{\sum n_i} = \frac{\sum w_i}{\sum w_i/M_i}$$

$$M_w = \frac{\sum n_i M_i^2}{\sum n_i M_i} = \frac{\sum w_i M_i}{\sum w_i}$$

### Polydispersity Index (PDI)

$$\text{PDI} = \frac{M_w}{M_n}$$

- PDI = 1: Monodisperse (living polymerization)
- PDI = 1.5-2.0: Typical step-growth (Flory distribution)
- PDI = 2.0: Most free-radical chain polymerization
- PDI > 2.0: Broad distribution (branching, multiple sites)

## Membrane Osmometry

Measures osmotic pressure $\Pi$ to determine $M_n$:

$$\frac{\Pi}{c} = RT\left(\frac{1}{M_n} + A_2 c\right) \quad \text{(at low c)}$$

Plot $\Pi/c$ vs $c$ → intercept = $RT/M_n$, slope = $RT A_2$.

## Light Scattering

### Rayleigh Scattering

$$\frac{Kc}{R_\theta} = \frac{1}{M_w P(\theta)} + 2A_2 c$$

where:
- $K = \frac{4\pi^2 n_0^2}{N_A \lambda_0^4}\left(\frac{dn}{dc}\right)^2$ (optical constant)
- $R_\theta$ = Rayleigh ratio at angle $\theta$
- $P(\theta)$ = particle scattering function (form factor)

### Zimm Plot

Debye plot extrapolated to both $c \to 0$ and $\theta \to 0$:
- Intercept: $1/M_w$
- Slope at $c=0$: related to $R_g$ (radius of gyration)
- Slope at $\theta=0$: $2A_2$

### Radius of Gyration

$$R_g^2 = \frac{1}{2} N l^2 \quad \text{(freely jointed chain)}$$

$$R_g^2 = \frac{Nb^2}{6} \quad \text{(Gaussian chain)}$$

## Size Exclusion Chromatography (SEC/GPC)

Separates by hydrodynamic volume. Calibration with narrow standards.

### Universal Calibration

$$[\eta] M = \text{constant (for same hydrodynamic volume)}$$

$$\log([\eta] M) = f(V_R)$$

Mark-Houwink equation: $[\eta] = K M^a$

### Determination of Averages from SEC

$$M_w = \frac{\sum w_i M_i}{\sum w_i}, \quad M_n = \frac{\sum w_i}{\sum w_i/M_i}$$

where $w_i$ is the weight fraction at elution volume $V_i$.

## Intrinsic Viscosity

$$[\eta] = \lim_{c \to 0} \frac{\eta - \eta_0}{\eta_0 c} = \lim_{c \to 0} \frac{\eta_{sp}}{c}$$

Huggins equation: $\frac{\eta_{sp}}{c} = [\eta] + k_H [\eta]^2 c$

Kraemer equation: $\frac{\ln(\eta_r)}{c} = [\eta] + k_K [\eta]^2 c$

## Problem Types

1. Calculate $M_n$, $M_w$, PDI from distribution data
2. Interpret Zimm plot data for $M_w$, $R_g$, $A_2$
3. Convert SEC retention times to molecular weights via universal calibration
4. Determine intrinsic viscosity from dilute solution measurements
5. Compare characterization techniques

## L3 Tools

- `../L3_functions/polymer_chemistry.py` - Number-average MW, PDI, Flory distribution
- `../L3_functions/polymer_physics.py` - Chain dimension calculations

## Related L2 Nodes

- `flory_huggins_theory.md` - Solution thermodynamics
- `polymer_properties.md` - Bulk polymer properties
