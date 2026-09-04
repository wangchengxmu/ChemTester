---
id: measurement.quantitative_uncertainty
layer: 2
title: Quantitative Measurement and Uncertainty
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - ../L3_functions/measurement_quant_tools.py
  - ../L3_functions/measurement_quant_tools.py
  - ../L4_reference/measurement/routine-measurement-and-reporting.md
  - ../L4_reference/reference/measurement-formulas-and-unit-conversions.md
  - ../L4_reference/reference/measurement-uncertainty-rules.md
  - ../L5_examples/measurement/case-density-report.md
  - ../L5_examples/measurement/case-significant-figure-rounding-edge.md
  - ../L5_examples/measurement/case-mixed-unit-conversion-example.md
---

## Context
This principle governs how numerical chemistry answers are produced and reported without breaking validity. It applies to both textbook problems and real lab calculations.

## Core equations and rules

1. **Dimensional conversion**
   - `x_target = x_given ¡Á conversion_factor`
   - Conversion factor must equal 1 in value (unit ratio identity).

2. **Derived quantity model**
   - If `y = f(x1, x2, ..., xn)`, each input must be unit-compatible.
   - Unit trace must be explicit before final simplification.

3. **Significant figures (operational rule)**
   - Multiplication/division: keep sig figs of least precise input.
   - Addition/subtraction: keep decimal place of least precise term.

4. **Uncertainty reporting (baseline)**
   - Report as `value ¡À uncertainty` with matched decimal precision.

## Decision flow (solver)

1. Parse knowns with units and precision metadata.
2. Normalize units into coherent basis (prefer SI-compatible form).
3. Determine operation class:
   - ratio/product chain -> sig-fig rule A
   - sum/difference chain -> sig-fig rule B
4. Compute central value.
5. Apply reporting rule from [L4 uncertainty rules](../L4_reference/reference/measurement-uncertainty-rules.md).
6. Emit answer + assumptions + confidence.

## Edge cases
- Mixed-unit values copied from different sources (convert before arithmetic).
- Ambiguous precision in integer constants (treat exact counts separately).
- Over-rounded intermediate values can distort final result.

## Implementations and data
- Implementation: `../L3_functions/unit_conversion_tools.py`
- Tool implementation: [L3 code](../L3_functions/measurement_quant_tools.py)
- Solver wrapper: [L3 skill](../L3_functions/measurement_quant_tools.py)
- Formula table + conversion references: [L4 formulas](../L4_reference/reference/measurement-formulas-and-unit-conversions.md)
- Uncertainty/sigfig lookup rules: [L4 uncertainty rules](../L4_reference/reference/measurement-uncertainty-rules.md)
- Worked examples: [L5 Ch01 examples](../L5_examples/measurement/)


## L3 Tool Call Directives

**Source:** `unit_conversion_tools.py`

Temperature, pressure, energy, volume, mass, length, concentration conversions; molar mass calculation; ideal gas law solver.

### Available functions:
- `convert_temperature(value, from_unit, to_unit)` → float — C, K, F conversions
- `convert_pressure(value, from_unit, to_unit)` → float — atm, Pa, kPa, bar, mmHg, torr
- `convert_energy(value, from_unit, to_unit)` → float — J, kJ, cal, kcal, eV, L·atm
- `convert_volume(value, from_unit, to_unit)` → float — L, mL, m³, cm³, gal, fl_oz
- `convert_mass(value, from_unit, to_unit)` → float — g, kg, mg, lb, oz, amu
- `convert_length(value, from_unit, to_unit)` → float — m, cm, mm, nm, pm, Å, in, ft
- `convert_concentration(value, from_unit, to_unit, molar_mass=None)` → float — M, mM, μM, g/L, %w/v, ppm, ppb
- `calculate_molar_mass(formula)` → float — Molar mass from formula (e.g. 'H2O', 'Ca(OH)2')
- `moles_to_mass(moles, molar_mass)` → float — mass = mol × M
- `mass_to_moles(mass, molar_mass)` → float — mol = mass / M
- `ideal_gas_law(pressure=None, volume=None, moles=None, temperature=None, solve_for='unknown')` → float — Solve PV=nRT

### Common errors:
- ❌ Concentration conversions between M and g/L require molar_mass parameter
- ❌ Transmittance T is 0-1 fraction, NOT percentage — use percent_transmittance for %
- ❌ Not all 4 ideal gas law params needed — pass None for unknown + set solve_for
