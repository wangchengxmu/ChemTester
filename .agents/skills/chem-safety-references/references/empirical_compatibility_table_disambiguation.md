# Empirical compatibility-table hazard disambiguation

## Applicability

A safety question asks for empirical hazard categories produced by pairing broad chemical reactivity classes, especially legacy EPA chemical-storage or hazardous-waste compatibility groups.

## Procedure

1. Preserve the exact class pair, roles, physical forms, and qualifiers.
2. Treat requested categories as empirical pair outputs rather than consequences inferred from generic reactivity.
3. For legacy EPA names, call hazardous_waste_compatibility.lookup_chemical_storage_compatibility with both visible class names.
4. Decode only returned codes and assess heat, fire, explosion, gas formation, and polymerization independently.
5. Translate supported categories only after classification; a blank chart cell means unknown, not safe.

## Boundaries

- Do not select a category without exact-pair evidence.
- Heat, fire, and explosion are distinct categories.
- Reject neighboring classes and member-specific substitutions.
- A blank chart cell is not evidence of compatibility.

Only calculators listed in this package's calculator reference are callable here.
Other filenames in a procedure are historical pointers, not installed dependencies.
For missing empirical support, obtain an authoritative source or state the uncertainty.
