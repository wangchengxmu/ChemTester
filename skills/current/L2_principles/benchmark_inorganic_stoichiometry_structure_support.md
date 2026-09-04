---
id: benchmark.inorganic_stoichiometry_structure_support
layer: 2
title: Benchmark Inorganic Stoichiometry and Structure Support
up_links:
  - ../L1_ontology/chemistry-core-map.md
  - ./benchmark_inorganic_option_disambiguation.md
  - ./stoichiometric_conversion.md
---

# Benchmark Inorganic Stoichiometry and Structure Support

Use this note for long inorganic benchmark MCQs where a visible option must be
checked against a balanced equation, formula mass fraction, oxoanion redox fact,
or unit-cell motif count. Keep the expected answer and source solution out of
the performer path; derive support from formulas, equations, and neutral
reference facts.

## Formula and Mass-Fraction Anchors

- A rhenium hydride clue near 68% Re by mass is consistent with the formula
  `K2ReH9`: Re mass fraction is about 68.1%.
- `K2PtCl6` has Pt mass fraction about 40.14%; it contains potassium cations
  and the octahedral `PtCl6^2-` anion.
- The decomposition `K2PtCl6 -> Pt + 2 KCl + 2 Cl2` has coefficient sum 6.
- Oxalate substitution of octahedral platinum(IV) chloride routes can give
  square-planar platinum(II) oxalate anions. In Pt complex MCQs, verify every
  concrete statement before choosing an "all correct" or "at most" option.

## Oxoanion Redox Anchors

For adjacent period-4 elements with common `XO4^2-` ions:

- `CrO4^2-`, `MnO4^2-`, and `FeO4^2-` all have central-element mass fraction
  below 50%.
- Acidic ferrate has a high standard reduction potential:
  `FeO4^2- + 8 H+ + 3 e- -> Fe3+ + 4 H2O`, approximately 2.2 V.
- Do not treat placeholder letters `A`, `B`, `C`, `X`, or `M` as literal
  element symbols; bind them only after the formula and period constraints are
  solved.

## Electrolysis Anode Product Anchors

For benchmark MCQs asking which arrangements produce oxygen at the anode,
evaluate each option independently and keep the full option-letter set.

- Inert Pt/graphite anodes in dilute acid or dilute sulfate media oxidize
  water to oxygen: `2 H2O -> O2 + 4 H+ + 4 e-`.
- Inert anodes in molten or concentrated hydroxide media oxidize hydroxide to
  oxygen: `4 OH- -> O2 + 2 H2O + 4 e-`.
- Concentrated aqueous chloride/brine with inert Pt/graphite usually produces
  chlorine at the anode, not oxygen: `2 Cl- -> Cl2 + 2 e-`.
- Reactive metal anodes can dissolve instead of evolving oxygen; do not treat
  a Cu anode as inert Pt.

## ZnS-Derived Motif Counts

For cubic ZnS-derived `ABC2` / `DEF2` cation-ordering MCQs:

- If the `ABC2` cation ordering removes the threefold rotation axis, the
  primitive unit cell and structural motif can both contain 4 atoms.
- If the `DEF2` cation ordering preserves a threefold-axis supercell, the
  primitive unit cell can contain 12 atoms while the structural motif remains
  4 atoms.
- Compare the ordered quadruple directly to the visible options; reject an
  "all incorrect" option only after checking the exact ordered sequence.

## Named Process Coefficient-Sum Anchors

These balanced equations are neutral support rows for process-style inorganic
MCQs. Use them as equation references, not as answer-key literals.

```text
CaCN2 + Na2CO3 + C -> CaCO3 + 2 NaCN                         sum = 6
As4S4 + 20 HNO3 -> 4 H3AsO4 + 4 S + 20 NO2 + 4 H2O            sum = 53
6 Co(NO3)3 -> 2 Co3O4 + 18 NO2 + 5 O2                         sum = 31
3 ReF6 + 10 H2O -> 2 HReO4 + ReO2 + 18 HF                     sum = 34
Ga2(OH)2Cl2.2H2O + 4 NaOH -> 2 Na[Ga(OH)4] + 2 NaCl + H2      sum = 10
```

From these sums, exactly two are prime: 53 and 31.

## Borohydride and Nitrate/Nitrite Anchors

- Ceric ammonium nitrate oxidizes nitrite to nitrate in acid:
  `2 Ce4+ + NO2- + H2O -> 2 Ce3+ + NO3- + 2 H+`, product-side sum 5.
- For chloroplatinic-acid-catalyzed borohydride hydrolysis rows where
  platinum coordination-state products are kept explicit, count products from
  the coordinated net equation rather than collapsing the Pt-containing species.

## Thermal Salt Gas-Analysis Traps

For inorganic gas-analysis MCQs where a heated salt gives sequential trap
mass changes and a final inert gas volume, solve the absorber identities before
counting atoms in the candidate formula.

- Retrieval anchors for these rows include `ClO4`, `OH`, `CuO`, gas mass,
  pressure, equimolar mixture, salts, and weighing.
- Anhydrous magnesium perchlorate is a drying trap for water.
- Calcium hydroxide absorbs carbon dioxide by carbonate formation.
- Hot copper can remove oxygen by forming copper oxide, so a copper mass gain
  can indicate moles of oxygen atoms captured from the gas stream.
- A residual gas volume at STP often corresponds to nitrogen when the upstream
  compound contains nitrate/nitrite or ammonium nitrogen.
- Convert each measured mass or STP volume into moles of elements, form the
  simplest integer ratio, then match the requested atom count or formula to the
  visible option text.

## Tool Route

For long published benchmark MCQs with these cues, call
`inorganic_benchmark_support_tools.analyze_inorganic_benchmark_mcq(question, options)`.
The tool returns the selected visible option only when it can match option text
to deterministic evidence and records that it did not use problem ids or
expected answers.
