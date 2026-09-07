# Exact tabulated periodic-property disambiguation

## Applicability

An element-ranking or multiple-choice task depends on an exact named periodic-property scale, especially for transition metals or candidate ties.

## Procedure

1. Identify the named property and scale, then express each option as ordering and equality constraints.
2. Search exact-value knowledge once; if empty, use the declared single alternate tool-search path. If neither yields supported values, stop retrieval.
3. Require supported values for every element from one consistent scale and reject missing or sentinel values.
4. Compare at the source precision, preserve supported ties, and map the resulting relation exactly to the visible option.
5. If exact support remains unavailable, use broad trends only to eliminate contradictions and lower confidence rather than inventing values.

## Boundaries

- Across-period trends are not reliably monotonic within transition metals.
- Never interpret zero or unknown from an incomplete property table as a measured value.
- Do not create ties by mixing scales or incompatible reporting precision.

Only calculators listed in this package's calculator reference are callable here.
Other filenames in a procedure are historical pointers, not installed dependencies.
For missing empirical support, obtain an authoritative source or state the uncertainty.
