---
name: chem-crystal-structures
description: "Use for crystallographic density, formula units per cell, fractional-coordinate geometry, lattice metrics, or structure/TGA composition closure. Not for molecular stereochemical nomenclature."
---

# Crystal Structures

## Workflow

1. Distinguish cell, formula unit, site occupancy, asymmetric unit, and bulk composition.
2. Transform fractional coordinates with the correct metric and periodic images; do not treat a nonorthogonal cell as Cartesian.
3. Cross-check density, stoichiometry, charge, and mass loss. State structural ambiguity when independent constraints do not determine a unique composition.

## Load Only Relevant Procedures

Open the matching reference below only when its applicability fits the task.
Use another skill for a separate subproblem; do not load this entire library by default.

- [Unit-cell density and composition constraint triangulation](references/unit_cell_density_composition_triangulation.md): A crystalline coordination compound or porous framework identity must be inferred from cell parameters, density, Z, elemental ratios, included solvent or guests, and a decomposition-product composition.
- [Fractional-coordinate polyhedron metric reconstruction](references/fractional_coordinate_polyhedron_metrics.md): A crystal-structure problem gives fractional coordinates or layered symmetry, a distorted-polyhedron angle, and asks for a lattice parameter or local geometry.
- [Peroxo-crystal speciation and TGA closure](references/peroxo_crystal_speciation_tga_closure.md): A crystalline inorganic peroxide or peroxosalt identity, component ratio, or statement set must be inferred from preparation, ionic and neutral species, and thermogravimetric mass loss.

## Optional Calculators

Read [calculator scope and availability](references/calculators.md) only if a numerical or structural operation would help.
Select and invoke a documented function yourself. No dispatcher, model router, or automatic tool loop is required.

## Evidence And Output

- Start from the user's actual structures, conditions, and requested quantity. If evidence is missing, ask for it or state a bounded assumption.
- Treat these procedures as conditional reasoning aids, not authority over the current evidence. Preserve equations, units, scope, and uncertainty.
- A successful calculator call is not independent scientific validation. Verify consequential empirical constants, safety claims, and exceptional chemistry against authoritative sources.
- Do not read benchmark answers, previous predictions, or evaluation logs to answer a question. Keep the model answer separate from a benchmark key and scientific adjudication.
- Missing optional references are a support limitation, not evidence that a reasoned answer is wrong. Do not invent the missing source.
