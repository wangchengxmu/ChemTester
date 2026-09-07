# Direction-aware empirical activation-energy estimation

## Applicability

An empirical activation-energy rule is qualified by reaction direction or exothermicity, especially when the requested elementary radical step is endothermic but its reverse is exothermic.

## Procedure

1. Inventory bonds broken and formed in the requested direction, then estimate ΔHforward as the sum of broken-bond energies minus the sum of formed-bond energies.
2. Apply a direction-qualified empirical coefficient only when that direction satisfies its stated condition; otherwise examine the reverse reaction.
3. For an endothermic target whose reverse is covered, calculate Ea,reverse from bonds broken in reverse, then use Ea,forward = Ea,reverse + ΔHforward.
4. Compare unrounded estimates with experimental values, verify difference and relative-error signs, and round only the final reported comparison.

## Boundaries

- Never apply an exothermic-step coefficient directly to an endothermic target direction.
- Require Ea,forward − Ea,reverse to equal ΔHforward with the same sign.
- Remember that bonds broken in reverse are bonds formed forward.
- If no direction satisfies a rule's stated category, do not force that coefficient.
- Use only available documented support; otherwise apply the explicit derivation or label missing empirical evidence unresolved. A library filename is not an executable tool.

Only calculators listed in this package's calculator reference are callable here.
Other filenames in a procedure are historical pointers, not installed dependencies.
For missing empirical support, obtain an authoritative source or state the uncertainty.
