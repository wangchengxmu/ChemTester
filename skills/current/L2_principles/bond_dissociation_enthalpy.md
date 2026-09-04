# Bond Dissociation Enthalpy Calculation

[Source: Understanding Organic Chemistry Through Computation (Boaz and Pearce), Ch9]

## Core Concept

Bond Dissociation Enthalpy (BDE) is the enthalpy change when a bond is homolytically cleaved. Computational chemistry can predict BDEs with reasonable accuracy using DFT methods.

## Key Equations

### Homolytic Bond Dissociation

$$\text{R-H} \rightarrow \text{R}^\bullet + \text{H}^\bullet$$

$$\text{BDE} = H(\text{R}^\bullet) + H(\text{H}^\bullet) - H(\text{R-H})$$

### Computational Method

1. Calculate enthalpy of parent molecule: $H(\text{R-H})$
2. Calculate enthalpy of radical: $H(\text{R}^\bullet)$
3. Calculate enthalpy of H atom: $H(\text{H}^\bullet) = -0.5024$ Hartree (known)
4. BDE = $\Delta H$ (convert to kJ/mol)

### Unit Conversion

$$\text{BDE (kJ/mol)} = \Delta H \text{(Hartree)} \times 2625.5$$

## Typical BDE Values

| Bond | BDE (kJ/mol) |
|------|--------------|
| C-H (spÂ³) | 410-440 |
| C-H (spÂ²) | 460-470 |
| C-H (sp) | ~510 |
| C-C | 340-370 |
| C=C | 610-630 |
| Câ¡C | ~840 |
| O-H | 460-470 |
| N-H | 390-400 |

## Computational Protocol

1. **Method**: B3LYP/6-31G(d) or higher
2. **Optimize** both parent and radical
3. **Frequency** to get thermal corrections
4. **Calculate** enthalpy at 298 K
5. **Apply** BDE formula

## Problem Types

1. **Compare BDEs** for different C-H bonds
2. **Predict radical stability** from BDE
3. **Explain selectivity** in radical reactions
4. **Calculate** bond energies in molecules

## Related Topics

- â?`organic_reaction_mechanisms.md` for radical chemistry
- â?`thermodynamics_laws.md` for enthalpy concepts


## Implementations

- Implementation: `../L3_functions/bond_dissociation_enthalpy.py`

## L3 Tool Call Directives


**Source:** `bond_dissociation_enthalpy.py`

L3 tool module for bond dissociation enthalpy

### Available functions:
- `calculate_bde(parent_enthalpy: float, radical_enthalpy: float, h_enthalpy: float)` → float — Calculate Bond Dissociation Enthalpy from enthalpies.
- `compare_bde(bde1: float, bde2: float)` → dict — Compare two BDE values.
- `radical_stability(bde: float, reference_bde: float)` → str — Assess radical stability from BDE.
- `predict_selectivity(bde_list: list)` → dict — Predict radical reaction selectivity from BDEs.

### Common errors:
- ❌ Passing wrong parameter types (strings where numbers expected)
- ❌ Forgetting required parameters

## L3 Tool Call Directives

**Source:** `enthalpy_tools.py`

Enthalpy and Thermochemistry Tools (L3)

### Available functions:
- `delta_H_rxn_from_formation(reactants, products, delta_H_f_data)` →  — Calculate standard enthalpy of reaction from formation enthalpies.
- `hess_law_combine(reactions, target_reaction)` →  — Apply Hess's Law to combine reaction enthalpies.
- `reverse_reaction(delta_H)` →  — Reverse a reaction (multiply DeltaH by -1).
- `multiply_reaction(delta_H, factor)` →  — Multiply reaction by factor (multiply DeltaH by factor).
- `hess_from_reactions(reaction_data, target_delta_H_f)` →  — Calculate unknown enthalpy using Hess's Law.
- `heat_of_combustion_per_gram(delta_H_comb, molar_mass)` →  — Calculate heat released per gram of fuel.
- `heat_of_combustion_per_volume(delta_H_comb, molar_mass, density)` →  — Calculate heat released per volume of liquid fuel.
- `heat_phase_change(moles, delta_H_phase)` →  — Calculate heat for phase change.
- `total_heat_with_phase_change(moles, c_solid, c_liquid, delta_T_solid, delta_T_liquid, delta_H_fusion)` →  — Calculate total heat for temperature change through phase transition.
- `integrated_cp_poly(A, B, C, D, T1, T2)` →  — Integrate polynomial heat capacity Cp = A + BT + CT² + DT³ from T1 to T2.
- `heat_exchange_poly(n_mol, cp_coeffs_list, T1, T2)` →  — Calculate heat removed/added for a mixture with polynomial Cp, per component.

### Common errors:
- ❌ Passing wrong units (check function docstring for expected units)
- ❌ Omitting required parameters
