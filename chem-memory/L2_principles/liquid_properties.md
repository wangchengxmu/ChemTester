---
id: liquid.properties
layer: 2
title: Liquid Properties
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - ../L3_functions/liquid_properties_tools.py
  - ../L3_functions/liquid_properties_tools.py
  - ../L4_reference/reference/liquid-properties-reference.md
  - ../L5_examples/liquid_properties/
source:
  - Averill, Ch11
---

[Source: Averill, Ch11]

## Context

Liquids exhibit unique macroscopic properties that arise directly from intermolecular forces. Unlike gases (molecules independent) or solids (molecules locked in place), liquids balance intermolecular attraction with molecular mobility.

Three key liquid properties:
- **Surface tension** - Resistance to surface area increase
- **Capillary action** - Movement in narrow tubes
- **Viscosity** - Resistance to flow

## Core Concepts

### 1. Surface Tension

**Definition:** Energy required to increase surface area of a liquid by a unit amount.

```
¦Ã = Energy/Area (J/m2 or N/m or dyn/cm)
```

**Mechanism:**
- Interior molecules: Attracted equally from all directions ¡ú No net force
- Surface molecules: Missing neighbors above ¡ú Net inward pull
- Result: Liquid minimizes surface area (spherical droplets)

**Factors affecting surface tension:**
| Factor | Effect | Reason |
|--------|--------|--------|
| Stronger IMFs | Higher ¦Ã | More energy to create surface |
| Temperature increase | Lower ¦Ã | Thermal motion overcomes IMFs |
| Surfactants | Lower ¦Ã | Disrupt surface IMFs |

**Key values:**
- Water at 20¡ãC: 72.8 mJ/m2 (very high due to H-bonding)
- Mercury: 486 mJ/m2 (metallic bonding)
- Diethyl ether: 17 mJ/m2 (weak London forces)

**Applications:**
- Water striders walking on water
- Paper clips "floating" on water
- Overfilled glass (meniscus above rim)
- Surfactants in firefighting foams

### 2. Capillary Action

**Definition:** Rise or fall of liquid in narrow tube due to cohesive vs adhesive forces.

**Cohesive forces:** IMFs between liquid molecules
**Adhesive forces:** Attraction between liquid and tube surface

**Competition:**
- Adhesion > Cohesion ¡ú Liquid rises, concave meniscus
- Cohesion > Adhesion ¡ú Liquid falls, convex meniscus

**Height of capillary rise:**
```
h = (2¦Ã cos ¦È) / (¦Ñgr)
```
Where:
- ¦Ã = surface tension
- ¦È = contact angle
- ¦Ñ = liquid density
- g = gravitational acceleration
- r = tube radius

**Examples:**
- Water in glass: Rises (H-bonding to Si-OH groups)
- Mercury in glass: Falls (cohesive metallic bonding > adhesion)
- Plant xylem: Water rises >50m via capillary action
- Paper towels: Absorb water via narrow cellulose channels

### 3. Viscosity

**Definition:** Resistance of a liquid to flow.

```
¦Ç = Viscosity (mPa¡¤s or poise, P)
```

**Mechanism:**
- Stronger IMFs ¡ú Higher viscosity
- Longer/more flexible molecules ¡ú Higher viscosity (entanglement)
- Lower temperature ¡ú Higher viscosity (less kinetic energy)

**Factors affecting viscosity:**
| Factor | Effect on ¦Ç |
|--------|-------------|
| Stronger IMFs | Increase |
| More H-bonds | Increase |
| Longer molecules | Increase |
| Higher temperature | Decrease |
| Branched vs linear | Linear higher |

**Key values:**
- Water at 20¡ãC: 1.00 mPa¡¤s
- Ethylene glycol: 16.1 mPa¡¤s (multiple H-bonds)
- Motor oil (SAE 30): ~250 mPa¡¤s at 20¡ãC

**Applications:**
- Motor oil viscosity grades (SAE 5W/50 multigrade)
- Temperature-dependent lubricant design
- Polymer melt processing

## Decision Flow

### Predicting Meniscus Shape
1. Identify liquid polarity and IMF type
2. Identify surface composition (glass = polar Si-OH)
3. Compare cohesive vs adhesive strength:
   - Polar liquid + polar surface ¡ú Concave (water in glass)
   - Nonpolar liquid + polar surface ¡ú Convex (mercury in glass)

### Predicting Viscosity Order
1. Count H-bonding sites
2. Compare molecular size/shape
3. Consider temperature if given

## Edge Cases

- **Supercooled liquids**: Can have very high viscosity
- **Glasses**: Technically supercooled liquids with extreme viscosity
- **Liquid crystals**: Anisotropic viscosity
- **Non-Newtonian fluids**: Viscosity depends on shear rate

## Implementations and Data
- Implementation: `../L3_functions/density_tools.py`

- Tool implementation: [L3 code](../L3_functions/liquid_properties_tools.py)
- Solver wrapper: [L3 skill](../L3_functions/liquid_properties_tools.py)
- Reference tables: [L4 properties tables](../L4_reference/reference/liquid-properties-reference.md)
- Worked examples: [L5 examples](../L5_examples/liquid_properties/)

## Related Topics

- [intermolecular_forces.md](intermolecular_forces.md) - Underlying cause of all liquid properties
- [phase_diagrams.md](phase_diagrams.md) - Liquid-gas boundary
- [solubility.md](solubility.md) - Dissolution in liquids

## L3 Tool Call Directives

**Source:** `liquid_properties_tools.py`

Surface tension, capillary action, viscosity, and meniscus predictions from intermolecular forces.

### Available functions:
- `capillary_rise_height(surface_tension, contact_angle_deg, density, tube_radius, g=9.81)` → float — h = 2γcosθ/(ρgr) in meters
- `meniscus_shape(cohesive_strength, adhesive_strength)` → str — Returns 'concave', 'convex', or 'flat'; strengths = 'weak'|'moderate'|'strong'
- `viscosity_trend_comparison(substances)` → List[str] — Orders substances by viscosity (lowest to highest)
- `surface_tension_prediction(imf_type, molecular_mass)` → str — Returns category like "Very high (like water)" or "Low"
- `temperature_effect_on_viscosity(activation_energy, T1, T2, viscosity_T1)` → float — Arrhenius-type: η = A·exp(Ea/RT)
- `work_of_adhesion(surface_tension_liquid, surface_tension_solid, interfacial_tension)` → float — Dupre equation: W_ad = γ_L + γ_S - γ_LS

### Common errors:
- ❌ Forgetting contact angle determines rise vs fall (θ < 90° = rise, θ > 90° = depression)
- ❌ Using wrong units for surface tension (SI: N/m, common: mN/m = mJ/m²)
- ❌ Not accounting for temperature effect on viscosity (higher T = lower viscosity)
