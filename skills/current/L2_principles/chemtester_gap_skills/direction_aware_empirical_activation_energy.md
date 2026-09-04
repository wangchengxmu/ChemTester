# Direction-aware empirical activation-energy estimation

**Retrieve with:** endothermic radical activation energy, forward reverse activation barriers, bond energy reaction enthalpy, microscopic reversibility kinetics, empirical bond-energy barrier rule

**Use when:** An empirical activation-energy rule is qualified by reaction direction or exothermicity, especially when the requested elementary radical step is endothermic but its reverse is exothermic.

## Procedure

1. Inventory bonds broken and formed in the requested direction, then estimate ΔHforward as the sum of broken-bond energies minus the sum of formed-bond energies.
2. Apply a direction-qualified empirical coefficient only when that direction satisfies its stated condition; otherwise examine the reverse reaction.
3. For an endothermic target whose reverse is covered, calculate Ea,reverse from bonds broken in reverse, then use Ea,forward = Ea,reverse + ΔHforward.
4. Compare unrounded estimates with experimental values, verify difference and relative-error signs, and round only the final reported comparison.

## Preferred Support

- chem-memory/L2_principles/bond_dissociation_enthalpy.md
- chem-memory/L2_principles/enthalpy_and_thermochemistry.md

## Guards

- Never apply an exothermic-step coefficient directly to an endothermic target direction.
- Require Ea,forward − Ea,reverse to equal ΔHforward with the same sign.
- Remember that bonds broken in reverse are bonds formed forward.
- If no direction satisfies a rule's stated category, do not force that coefficient.
