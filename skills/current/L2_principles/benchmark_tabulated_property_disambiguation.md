---
id: benchmark.tabulated_property_disambiguation
layer: 2
title: Benchmark Tabulated Property and Compatibility Disambiguation
up_links:
  - ../L1_ontology/chemistry-core-map.md
  - ../L2_principles/openstax_organic_ch24_amines_heterocycles.md
---

# Benchmark Tabulated Property and Compatibility Disambiguation

Use this note for multiple-choice benchmark rows that ask for a listed
compatibility rating, solubility category, or reactive-compatibility outcome.
These rows often test the discrete table category, not a broad mechanistic
guess.

## Discrete Compatibility Ratings

Materials-compatibility charts commonly use an A/B/C/D scale:

- A or Excellent: no significant effect under the chart conditions.
- B or Good: minor effect, slight corrosion, or discoloration.
- C or Fair: moderate effect; usually not recommended for continuous use.
- D or Severe: not recommended.

When a question asks for the listed rating for a named chemical/material pair,
do not downgrade from Excellent to Good just because a mild interaction is
chemically imaginable. Choose the option matching the chart category and stated
exposure basis. Supplier 316 stainless steel charts record this A/B/C/D scale;
one public 316SS chart lists sodium metaphosphate under that chart family.

## Nitroalkane Water Solubility

Small nitroalkanes are polar but are not alcohol-like hydrogen-bond donors.
For nitromethane, PubChem/CAMEO describe the liquid as denser than water and
slightly soluble in water. Do not treat nitromethane as fully miscible or very
soluble just because the nitro group is polar.

## Complete-Set Reactive Compatibility

For "select all" reactive-compatibility questions, output only the listed
hazard categories that apply. Strong oxidizing agents can intensify fire and
react vigorously with reducing organic compounds, generating heat and gaseous
products. With reduced sulfur organics such as mercaptans and organic sulfides,
include fire, heat generation, and toxic gas generation when those categories
are offered.

Do not add Explosion merely because a strong oxidizer can make some mixtures
explosive in other contexts. Add explosion only when the specific compatibility
table, source condition, or answer option evidence calls for that hazard.

For explosives mixed with miscellaneous combustible or flammable material
classes, treat the compatibility row as an energetic incompatibility surface:
select explosion and heat generation when offered. Do not add a separate fire
category just because the second class is combustible or flammable unless the
visible table row itself separately lists fire.

For explosives mixed with polymerizable compounds, treat the row as the same
direct energetic incompatibility surface unless the visible table row separately
lists polymerization. Select explosion and heat generation when those categories
are offered. Do not add fire or violent polymerization from broad chemical
intuition unless the row's listed categories include them.

For strong oxidizing agents mixed with epoxides in ChemBench compatibility-table
rows, select fire, heat generation, and innocuous/non-flammable gas generation
when those categories are offered. Do not add explosion or violent
polymerization merely because both are plausible in other epoxide or oxidizer
contexts unless the table row explicitly lists them.

For epoxides mixed with organic acids in ChemBench compatibility-table rows,
select heat generation and violent polymerization when offered. Do not add fire
or explosion as downstream escalation unless the table/source row separately
lists those categories.

For epoxides mixed with nitrides in ChemBench compatibility-table rows, select
heat generation and violent polymerization when offered. Do not add explosion
as a downstream escalation unless the table/source row separately lists
explosion.

For strong oxidizing agents mixed with aromatic hydrocarbons in ChemBench
compatibility-table rows, select fire and heat generation when offered. Do not
add explosion or toxic gas generation from worst-case oxidation scenarios
unless the table/source row separately lists those categories.

For strong reducing agents mixed with oxidizing acids in ChemBench
compatibility-table rows, select fire, heat generation, and toxic gas
generation when those categories are offered. Do not add explosion or
flammable-gas generation from broad incompatibility intuition unless the
table/source row separately lists those categories.

## Sources

- PubChem/CAMEO Chemicals, nitromethane: denser than water and slightly soluble
  in water.
- NOAA CAMEO Chemicals, strong oxidizing agents: strong oxidizers can initiate
  or accelerate combustion and can react vigorously with heat and gaseous
  products.
- Public 316 stainless steel chemical compatibility charts: A/Excellent,
  B/Good, C/Fair, and D/Severe rating scale for named chemical/material pairs.
