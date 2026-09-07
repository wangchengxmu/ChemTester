# Electrolysis

## Concept Overview

Electrolysis uses electrical energy to drive nonspontaneous redox reactions.

## Key Principles

### Faraday's Law
```
m = (M × I × t) / (z × F)
```

### Constants
- F = 96,485 C/mol e⁻

### Anode product selection for oxygen-evolution MCQs

Use this before choosing option letters in qualitative electrolysis questions.

- Oxidation occurs at the anode.
- With inert electrodes in dilute acid or dilute sulfate solution, water is oxidized at the anode:
  `2 H2O -> O2 + 4 H+ + 4 e-`.
- With inert electrodes in molten or concentrated hydroxide media, hydroxide is oxidized at the anode:
  `4 OH- -> O2 + 2 H2O + 4 e-`.
- Concentrated aqueous chloride/brine with inert Pt or graphite usually gives chlorine at the anode:
  `2 Cl- -> Cl2 + 2 e-`; do not select oxygen just because water is present.
- A reactive metal anode can dissolve instead of evolving oxygen. For example, a Cu anode in dilute acid can oxidize to copper ions, so do not treat it like inert Pt.
- For multi-select benchmark questions, evaluate every arrangement separately and return the full set of all options that satisfy oxygen-at-anode conditions.

## Links

- **L3 Tools**: `../L3_functions/electrolysis_tools.py`
- **L4 Reference**: Industrial applications
- **L5 Examples**: Electroplating calculations

## L3 Tool Call Directives

When solving electrolysis problems, ALWAYS use these tools. Do NOT calculate manually.

### mass_from_electrolysis(current, time, molar_mass, n_electrons) → float
- Returns mass of product (g) using Faraday's law: m = I·t·M / (n·F)
- **CRITICAL:** `n_electrons` is the number of electrons per formula unit
- You MUST determine n from the half-reaction, NOT assume n=1
- Common n_electrons values:
  - Cu²⁺ → Cu: n=2
  - Al³⁺ → Al: n=3
  - Ag⁺ → Ag: n=1
  - Na⁺ → Na: n=1
  - Cl⁻ → Cl₂: n=2 (per Cl atom)
  - H₂O → H₂ + ½O₂: n=2 (per H₂O)
- Current in Amperes (A), time in seconds (s)
- If time given in hours/minutes, convert to seconds first

### moles_from_electrolysis(current, time, n_electrons) → float
- Returns moles of product from Faraday's law

### current_for_mass(mass, time, molar_mass, n_electrons) → float
- Returns required current (A) to produce given mass

### time_for_mass(mass, current, molar_mass, n_electrons) → float
- Returns required time (s) to produce given mass

### charge_from_current_time(current, time) → float
- Returns total charge (Coulombs)

### Common caller errors to avoid:
1. ❌ Using n=1 for Cu²⁺ electrolysis → n=2 for Cu²⁺ → Cu
2. ❌ Forgetting to convert hours/minutes to seconds
3. ❌ Confusing n_electrons with stoichiometric coefficients → n comes from half-reaction
4. ❌ Not accounting for the number of atoms produced (e.g., 2Cl⁻ → Cl₂ produces 1 mol Cl₂ per 2 mol e⁻)
