# Lewis Acids and Bases

## Concept Overview

Lewis acids accept electron pairs; Lewis bases donate electron pairs. This model encompasses all Brønsted-Lowry reactions and extends to non-proton reactions.

## Key Principles

### Definitions
- **Lewis acid**: Electron pair acceptor
- **Lewis base**: Electron pair donor
- **Adduct**: Product of Lewis acid-base reaction

### Coordinate Covalent Bond
- Both bonding electrons from one species
- Formed when Lewis base donates to Lewis acid

### Comparison with Brønsted-Lowry
| Model | Acid | Base |
|-------|------|------|
| Brønsted | H⁺ donor | H⁺ acceptor |
| Lewis | e⁻ pair acceptor | e⁻ pair donor |

### Complex Ions
- Central metal cation (Lewis acid)
- Ligands (Lewis bases)
- Formation constant Kf

## Problem-Solving Routes

1. **Identify Lewis acid/base**: Find electron pair acceptor/donor
2. **Write complex formation**: Metal + ligands → complex
3. **Calculate Kf**: Formation constant
4. **Predict dissolution**: Complex formation can increase solubility

## Links

- **L3 Tools**: `../L3_functions/lewis_acid_base_tools.py`
- **L4 Reference**: Formation constant tables
- **L5 Examples**: Complex ion calculations

## Related Topics

- Brønsted-Lowry theory
- Solubility equilibria
- Coupled equilibria

---

## L3 Tool Call Directives

**Source:** lewis_acid_base_tools.py
Lewis acid/base identification, formation constants (Kf), complex ion stability, ligand dissolution.

### Available functions:
- identify_lewis_acid_base(species1, species2, species1_has_lone_pair, species2_has_lone_pair) → dict — Classify acid/base
- ormation_constant(complex_conc, metal_conc, ligand_conc, n_ligands) → float — Kf = [MLn]/([M][L]ⁿ)
- metal_concentration_from_Kf(Kf, complex_conc, ligand_conc, n_ligands) → float — [M] from Kf
- complex_ion_concentration(Kf, metal_conc, ligand_conc, n_ligands) → float — [MLn] from Kf
- dissociation_constant(Kf) → float — Kd = 1/Kf
- is_complex_ion_stable(Kf, threshold) → bool — True if Kf > 10¹⁰ (default)
- ligand_needed_for_dissolution(Ksp, Kf, metal_conc_target, n_ligands) → float — [L] needed to dissolve salt
- compare_brønsted_lewis(acid_type, base_type) → str — Compare Brønsted-Lowry vs Lewis definitions

### Common errors:
- ❌ Confusing Kf (formation) with Kd (dissociation) — Kd = 1/Kf, lower Kd = more stable
- ❌ Assuming all Lewis acids are Brønsted acids — Lewis is broader (e.g., BF₃ is Lewis but not Brønsted)
