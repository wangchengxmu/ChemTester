---
id: matter.classification_change_typing
layer: 2
title: Matter Classification and Change Typing
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - ../L3_functions/measurement_quant_tools.py
  - ../L4_reference/reference/matter-classification-decision-table.md
  - ../L5_examples/measurement/case-physical-vs-chemical-change.md
cross_links:
  - ./quantitative_measurement_and_uncertainty.md
---

## Context
Before selecting equations, classify what kind of matter/process is being described. Wrong classification leads to wrong model selection.

## Core rules
- Matter categories: element, compound, homogeneous mixture, heterogeneous mixture.
- State categories: solid, liquid, gas (plus plasma in high-energy contexts).
- Change typing:
  - physical change: composition unchanged
  - chemical change: composition changes (new substances formed)

## Decision flow
1. Identify whether composition changes.
2. If no composition change -> physical-change model path.
3. If composition changes -> chemical-process path.
4. Select downstream equations accordingly.

## Implementations and data
- Heuristic classifier: [L3 code](../L3_functions/measurement_quant_tools.py)
- Decision table: [L4 reference](../L4_reference/reference/matter-classification-decision-table.md)
- Example: [L5 case](../L5_examples/measurement/case-physical-vs-chemical-change.md)
