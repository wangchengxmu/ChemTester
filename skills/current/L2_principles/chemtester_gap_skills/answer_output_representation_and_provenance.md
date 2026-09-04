# Answer representation, scaling, tolerance adjudication, and provenance

**Retrieve with:** numeric option tolerance, relative percent error, none of the above, unrounded option comparison

**Use when:** A quantitative chemistry multiple-choice problem provides numeric choices, an explicit error or rounding tolerance, or a catch-all choice.

## Procedure

1. Derive each requested physical quantity independently of the options and retain unrounded guard digits.
2. Identify whether the acceptance rule is absolute or relative, percent or percentage points, and strict or inclusive.
3. For every option expressing the same quantity and units, compute the required deviation from the unrounded result; evaluate every relevant quantity when choices mix properties or analytes.
4. Select a numeric option only if it satisfies the cutoff; if none does and a catch-all choice exists, select the catch-all rather than the nearest value.
5. Return the requested answer format and, when useful, state the decisive deviation-versus-cutoff comparison.

## Preferred Support

- chem-memory/L2_principles/chemtester_gap_skills/answer_output_representation_and_provenance.md

## Guards

- Never round the calculated reference value before applying the tolerance test.
- Nearest is not equivalent to within tolerance.
- Do not confuse relative percent error with absolute error or percentage-point difference.
- Compare only options representing the same physical quantity and units.
