---
id: ref.equilibrium_constants_and_datasets
layer: 4
title: Equilibrium Constants and Reference Datasets
up_links:
  - ../../L2_principles/buffer_system.md
  - ../../L2_principles/quantitative_measurement_and_uncertainty.md
down_links:
  - ../../L5_examples/buffer/case-phosphate-50mM-ph74.md
---

Purpose: central lookup repository for constants/tables used by L2 reasoning and L3 calculations.

## Include here (structured tables)
- Acid/base pKa datasets (with temperature + ionic-strength notes)
- Solubility product constants (Ksp)
- Formation/stability constants (Kf, beta)
- Key redox standard potentials (E°)
- Henry constants / partition-related constants (as needed)
- Source provenance + validity ranges

## Required metadata per entry
- value
- unit convention
- temperature
- ionic strength / medium
- source URL/reference
- confidence/quality flag
- last verified date

## Usage rule
- L3 tools should call/look up constants from L4 reference tables instead of hardcoding values when possible.

