# Exact tabulated periodic-property disambiguation

**Retrieve with:** Pauling electronegativity values, periodic property table, transition metal electronegativity, element property lookup

**Use when:** An element-ranking or multiple-choice task depends on an exact named periodic-property scale, especially for transition metals or candidate ties.

## Procedure

1. Identify the named property and scale, then express each option as ordering and equality constraints.
2. Search exact-value knowledge; if absent, search tools for a matching property lookup before ending retrieval.
3. Require supported values for every element from one consistent scale and reject missing or sentinel values.
4. Compare at the source precision, preserve supported ties, and map the resulting relation exactly to the visible option.
5. If exact support remains unavailable, use broad trends only to eliminate contradictions and lower confidence rather than inventing values.

## Preferred Support

- chem-memory/L2_principles/periodic_trends.md
- chem-memory/L3_functions/periodic_trends_tools.py

## Guards

- Across-period trends are not reliably monotonic within transition metals.
- Never interpret zero or unknown from an incomplete property table as a measured value.
- Do not create ties by mixing scales or incompatible reporting precision.
