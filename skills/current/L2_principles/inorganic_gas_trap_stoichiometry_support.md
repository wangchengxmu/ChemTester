---
id: inorganic.gas_trap_stoichiometry_support
layer: 2
title: Inorganic Gas Trap Stoichiometry Support
up_links:
  - ../L1_ontology/chemistry-core-map.md
  - ./stoichiometric_conversion.md
---

# Inorganic Gas Trap Stoichiometry Support

Use this note for inorganic gas-analysis MCQs where heated salts or solid
mixtures release gases that are passed through sequential traps. The support is
benchmark-neutral: use only visible absorber identities, mass changes, gas
volumes, and option text.

## Trap Identities

- Retrieval anchors: `ClO4`, `OH`, `CuO`, gas mass, pressure, equimolar
  mixture, salts, weighing, heated salt, residual gas, STP.
- Anhydrous magnesium perchlorate, often written as `Mg(ClO4)2`, is a drying
  trap; its mass increase is assigned to water.
- Calcium hydroxide, `Ca(OH)2`, absorbs carbon dioxide by carbonate formation.
  If the calcium hydroxide tube mass does not change, do not invent a CO2
  contribution.
- Red-hot copper removes oxidizing oxygen from a gas stream by forming copper
  oxide. A copper tube mass increase can be converted to moles of oxygen atoms
  captured as `CuO`.
- A final residual gas volume at standard temperature and pressure often maps
  to a chemically inert gas such as nitrogen after water, carbon dioxide, and
  oxygen are removed.

## Ammonium Nitrate Nitrite Nitrous Oxide Checks

Use these as neutral reaction facts for salt gas-analysis questions; they are
not answer-key shortcuts.

- Ammonium nitrite can decompose to nitrogen and water:
  `NH4NO2 -> N2 + 2 H2O`.
- Ammonium nitrate can decompose to nitrous oxide and water:
  `NH4NO3 -> N2O + 2 H2O`.
- Nitrous oxide can act as an oxygen-transfer gas at red heat; red-hot copper
  can reduce it while forming `CuO` and nitrogen. This links a copper mass gain
  to the oxygen captured from nitrous oxide, not to carbon dioxide or water.
- In an equimolar-salt problem, compare the water moles, oxygen transferred to
  copper, and residual nitrogen volume simultaneously before matching any
  formula atom-count option.

## Procedure

1. Convert each trap mass increase into moles of the absorbed species: water
   from the drying trap, carbon dioxide from the hydroxide trap, and oxygen
   atoms from copper-to-copper-oxide mass gain.
2. Convert any residual STP gas volume using the molar volume specified by the
   problem or the usual `22.4 L mol^-1` approximation if the benchmark states
   STP without a different convention.
3. Use conservation of H, O, N, and any named cations/anions to infer a simple
   formula-ratio pattern for the salts or decomposition products.
4. Match the derived atom count, formula relation, or statement set to the
   visible option text. Do not choose from option order, problem id, source row,
   or expected answer.

## Guards

- Keep absorber assignment separate from formula matching; a zero mass change
  is evidence against that absorbed gas in the visible experiment.
- Do not treat placeholder letters such as A, B, or C as element symbols.
- If two formula assignments fit the same gas balances, report ambiguity
  rather than forcing a unique option.
