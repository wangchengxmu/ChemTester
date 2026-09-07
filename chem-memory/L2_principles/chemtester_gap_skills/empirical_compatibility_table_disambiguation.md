# Empirical compatibility-table hazard disambiguation

**Retrieve with:** EPA hazardous waste compatibility chart, chemical storage compatibility class pair, legacy reactivity group matrix, exact hazard code lookup, fire versus explosion hazard, blank chart cell not safe

**Use when:** A safety question asks for empirical hazard categories produced by pairing broad chemical reactivity classes, especially legacy EPA chemical-storage or hazardous-waste compatibility groups.

## Procedure

1. Preserve the exact class pair, roles, physical forms, and qualifiers.
2. Treat requested categories as empirical pair outputs rather than consequences inferred from generic reactivity.
3. For legacy EPA names, call hazardous_waste_compatibility.lookup_chemical_storage_compatibility with both visible class names.
4. Decode only returned codes and assess heat, fire, explosion, gas formation, and polymerization independently.
5. Translate supported categories only after classification; a blank chart cell means unknown, not safe.

## Preferred Support

- chem-memory/L2_principles/epa_hazardous_waste_compatibility_lookup.md
- chem-memory/L3_functions/hazardous_waste_compatibility.py
- chem-memory/L2_principles/chemtester_gap_skills/empirical_compatibility_table_disambiguation.md

## Guards

- Do not select a category without exact-pair evidence.
- Heat, fire, and explosion are distinct categories.
- Reject neighboring classes and member-specific substitutions.
- A blank chart cell is not evidence of compatibility.
