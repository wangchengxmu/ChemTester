---
id: chem.dissolution_process
layer: 2
title: The Dissolution Process and Solution Formation
---

## Enthalpy Balance

In the simple separation-and-mixing cycle,
`Delta H_soln = Delta H_solute + Delta H_solvent + Delta H_mix`.
Separating particles costs energy (positive); forming attractive solute-solvent
interactions releases energy (negative). Compare the **sum** with zero:

- Negative total: exothermic dissolution.
- Positive total: endothermic dissolution.
- Equivalently, with these signs, dissolution is exothermic when
  `abs(Delta H_mix) > Delta H_solute + Delta H_solvent`.

For example, `100 + 20 - 150 = -30` in consistent units is exothermic.
Do not compare a negative mixing enthalpy directly against the positive
separation terms to decide which energy contribution is larger.

## Entropy and Solubility

Dissolution entropy may be positive or negative. Dispersing solute can increase
entropy, but ordering of solvent around solute can outweigh that contribution.
Neither exothermicity nor a qualitative "like dissolves like" heuristic alone
establishes spontaneity or the equilibrium solubility.

At fixed temperature and pressure use `Delta G = Delta H - T*Delta S` for the
specified process and composition. A negative Gibbs-energy change favors that
direction; equilibrium requires equality of the appropriate chemical potentials.
Account for concentration/activity and phase changes when comparing saturation
states. An ideal-mixture enthalpy approximation is not a universal statement
about solid dissolution or lattice separation.

## Evidence and Calculation

Bind signs, units, temperature and the amount basis before adding contributions.
Use a documented calculator only if present in the active tool catalog; this
note does not advertise hypothetical solubility-prediction functions. Empirical
constants require traceable conditions, not merely a legacy table filename.

Source: [LibreTexts, Gibbs Energy and Solubility](https://chem.libretexts.org/Bookshelves/General_Chemistry/CLUE%3A_Chemistry_Life_the_Universe_and_Everything/06%3A_Solutions/6.4%3A_Gibbs_Energy_and_Solubility).
The calcium-chloride example illustrates that dissolution entropy can be negative.
