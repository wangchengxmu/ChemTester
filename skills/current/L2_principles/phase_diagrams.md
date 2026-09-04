---
id: phase.diagrams
layer: 2
title: Phase Diagrams
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - ../L3_functions/phase_diagrams_tools.py
  - ../L3_functions/phase_diagram_tools.py
  - ../L4_reference/reference/phase-diagrams-reference.md
  - ../L5_examples/phase_diagrams/
source:
  - Averill, Ch11
---

[Source: Averill, Ch11]

## Context

A phase diagram is a graphical summary of the physical state of a substance as a function of temperature and pressure in a closed system. It shows which phase (solid, liquid, gas) is stable under any combination of T and P.

## Core Concepts

### 1. Phase Diagram Regions

A typical phase diagram has three main regions:
- **Solid region** (upper left): Low T, high P
- **Liquid region** (middle): Moderate T and P
- **Gas/vapor region** (lower right): High T, low P
- **Supercritical region** (above critical point): Tc and Pc exceeded

### 2. Key Lines and Points

#### Phase Boundary Lines
| Line | Equilibrium | Process when crossed |
|------|-------------|---------------------|
| Solid-Liquid (A-D) | Solid ? Liquid | Melting/Freezing |
| Liquid-Gas (A-B) | Liquid ? Gas | Vaporization/Condensation |
| Solid-Gas (A-C) | Solid ? Gas | Sublimation/Deposition |

#### Triple Point (Point A)
- **Definition:** The ONLY combination of T and P where all three phases coexist in equilibrium
- Only one triple point exists per substance (single component)
- Water: 0.01¡ãC (273.16 K), 0.00604 atm
- Used to define Kelvin temperature scale

#### Critical Point (Point B)
- **Definition:** Temperature and pressure above which gas and liquid become indistinguishable
- **Critical temperature (Tc):** Highest T at which liquid can exist
- **Critical pressure (Pc):** Pressure required to liquefy at Tc
- Beyond this point: Supercritical fluid

### 3. Special Cases

#### Water Phase Diagram
- **Anomalous:** Solid-liquid line slopes LEFT (not right)
- **Reason:** Ice is less dense than liquid water
- **Consequence:** Melting point DECREASES with increasing pressure
- **Practical importance:**
  - Ice floats (aquatic life survives winter)
  - Ice skating (pressure melts thin layer)
  - Freeze-drying (sublimation at low P)

#### CO? Phase Diagram
- **Normal:** Solid-liquid line slopes right
- **Triple point:** -56.6¡ãC, 5.11 atm
- **Key feature:** Liquid CO? cannot exist at 1 atm
- **Result:** "Dry ice" sublimes directly at -78.5¡ãC
- **Critical point:** 30.98¡ãC, 72.79 atm

### 4. Reading Phase Diagrams

**Given T and P ¡ú Identify phase:**
1. Locate point on diagram
2. Identify which region it falls in
3. If on a line ¡ú Two phases in equilibrium

**Given phase change ¡ú Predict path:**
1. Start at initial (T, P)
2. Draw path to final (T, P)
3. Note which lines are crossed
4. Identify phase changes at each crossing

## Decision Flow

### Predicting Phase at Given Conditions
```
1. Is T > Tc?
   ¡ú Yes: Gas or supercritical
   ¡ú No: Continue

2. Is P > Pc?
   ¡ú Yes: Supercritical (if T > Tc) or liquid
   ¡ú No: Continue

3. Locate point on diagram
   ¡ú Above solid-liquid line + left of liquid-gas line = solid
   ¡ú Between solid-liquid and liquid-gas lines = liquid
   ¡ú Below liquid-gas line and solid-gas line = gas
```

### Predicting Phase Changes
```
Heating at constant P:
- Start in solid ¡ú Cross solid-liquid line ¡ú Melt ¡ú Liquid
- Start in liquid ¡ú Cross liquid-gas line ¡ú Boil ¡ú Gas

Increasing P at constant T:
- Start in gas ¡ú Cross liquid-gas line ¡ú Condense ¡ú Liquid
- Start in liquid ¡ú Cross solid-liquid line ¡ú Freeze ¡ú Solid
(Slope direction determines which phase)
```

## Quantitative Relationships

**Clausius-Clapeyron Equation** (for liquid-gas line):
```
ln(P₂/P₁) = -ΔH_vap/R × (1/T₂ - 1/T₁)
```

**Vapor pressure vs boiling point:**
- Boiling occurs when vapor pressure = external pressure
- Normal boiling point: Temperature at which Pvap = 1 atm

### Binary Tie-Line Lever Rule

Use this for binary phase diagrams in a two-phase region, such as solid + liquid
or alpha + beta. A horizontal tie line at the specified temperature gives the
compositions of the coexisting phases. The overall composition is C0 and the
phase-boundary compositions are often written as C_alpha/C_beta or C_S/C_L.

- The tie-line endpoints determine the phase compositions. The lever rule
  determines phase fractions or amounts, not the endpoint compositions.
- The fraction of a phase is proportional to the length of the opposite arm of
  the tie line.
- If C_S < C0 < C_L, the liquid fraction is (C0 - C_S) / (C_L - C_S), so it is
  proportional to the distance from C0 to C_S.
- If C_S < C0 < C_L, the solid fraction is (C_L - C0) / (C_L - C_S), so it is
  proportional to the distance from C0 to C_L.
- Apply the lever rule only for an equilibrium point inside a two-phase region.
  In a single-phase region there is only one phase fraction, and away from
  equilibrium the tie-line construction is not valid.

## L3 Tool Call Directives

**Source:** `phase_diagram_tools.py`
Phase diagram calculations: Clausius-Clapeyron, Gibbs phase rule, lever rule, Raoult's law, colligative properties.

### Available functions:
- `clausius_clapeyron(P1=None, T1=None, P2=None, T2=None, delta_H_vap=None)` → float — Solve for any one unknown in ln(P2/P1) = -ΔHvap/R·(1/T2-1/T1); provide exactly 4 of 5 params
- `gibbs_phase_rule(C, P)` → int — Degrees of freedom F = C - P + 2
- `triple_point_pressure(T_melt, T_boil, delta_H_sub, delta_H_vap, P_atm=1.0)` → float — Estimate triple point pressure in atm
- `phase_fraction_lever_rule(x_overall, x_alpha, x_beta)` → dict — {'alpha_fraction', 'beta_fraction'} for two-phase region
- `raoults_law(x_A, P_A_star, x_B=None, P_B_star=None)` → dict — P_A, P_total, y_A for ideal solutions
- `boiling_point_elevation(K_b, molality, i=1.0)` → float — ΔTb = i·Kb·m
- `freezing_point_depression(K_f, molality, i=1.0)` → float — ΔTf = i·Kf·m

### Common errors:
- ❌ Passing ΔH_vap in kJ/mol when clausius_clapeyron expects J/mol — multiply by 1000
- ❌ Using °C instead of K — always convert temperatures first
- ❌ Providing fewer or more than 4 parameters to clausius_clapeyron
- ❌ x_alpha > x_beta in lever rule — alpha must be left boundary

---

When solving vapor pressure / phase diagram problems, ALWAYS use these tools.

### calculate_vapor_pressure(T, T_ref, P_ref, deltaH_vap) → float
- Clausius-Clapeyron equation: P = P_ref × exp(-ΔH_vap/R × (1/T - 1/T_ref))
- **CRITICAL:** All temperatures MUST be in Kelvin
- deltaH_vap should be in J/mol (the tool handles R internally)
- If ΔH_vap given in kJ/mol, convert: multiply by 1000 first
- Returns vapor pressure in same units as P_ref

### calculate_deltaH_vap_from_pressures(P1, T1, P2, T2) → float
- Inverse Clausius-Clapeyron: ΔH_vap = -R × ln(P2/P1) / (1/T2 - 1/T1)
- **CRITICAL:** T1 and T2 MUST be in Kelvin
- Returns ΔH_vap in J/mol
- Common result range: 20-50 kJ/mol for typical liquids

### calculate_boiling_point_at_pressure(P_target, T_ref, P_ref, deltaH_vap) → float
- Find temperature where vapor pressure = P_target
- deltaH_vap in J/mol

### Common caller errors to avoid:
1. ❌ Passing ΔH_vap in kJ/mol when tool expects J/mol → Multiply by 1000
2. ❌ Using °C instead of K → Always convert first
3. ❌ Swapping P1/P2 and T1/T2 → Keep corresponding pairs together
4. ❌ Using wrong R value → Tool handles R internally, don't pass it

## Edge Cases

- **Multiple solid phases:** Some substances have multiple solid forms (e.g., carbon: graphite, diamond)
- **No stable liquid:** Some substances decompose before melting
- **Helium:** No triple point under normal conditions (remains liquid to 0 K)

## Implementations and Data
- Implementation: `../L3_functions/phase_equilibria_tools.py`

- Tool implementation: [L3 code](../L3_functions/phase_diagram_tools.py)
- Solver wrapper: [L3 skill](../L3_functions/phase_diagrams_tools.py)
- Reference database: [L4 phase diagrams](../L4_reference/reference/phase-diagrams-reference.md)
- Worked examples: [L5 examples](../L5_examples/phase_diagrams/)

## Related Topics

- [intermolecular_forces.md](intermolecular_forces.md) - IMF strength determines phase boundaries
- [liquid_properties.md](liquid_properties.md) - Properties of liquid phase
- [gas_laws.md](gas_laws.md) - Gas phase behavior
- [gibbs_free_energy.md](gibbs_free_energy.md) - Thermodynamic basis for phase stability

## Data Reference
- L3 Tool: 	hermodynamic_lookup_tools.lookup_thermodynamic_data(formula) â ÎHfÂ°, ÎGfÂ°, SÂ°, Cp for 58+ compounds
- L3 Tool: 	hermodynamic_lookup_tools.calculate_reaction_dH(reactants, products) â reaction enthalpy from formation data
- L3 Tool: 	hermodynamic_lookup_tools.calculate_reaction_dG(reactants, products) â reaction Gibbs energy
- L4 Data: L4_reference/thermodynamic_data.csv â Full table with NIST/CRC values
- L4 Reference: L4_reference/THERMODYNAMIC_DATABASES.md â Links to NIST-JANAF, NIST WebBook
