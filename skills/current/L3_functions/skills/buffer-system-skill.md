---
id: skill.buffer_system
layer: 3
title: Buffer System Skill (Problem-Solving Interface)
up_links:
  - ../../L2_principles/buffer_system.md
down_links:
  - ../code/buffer/buffer_calculators.py
  - ../../L4_database/buffer/protocol-buffer-design-and-prep.md
enables:
  - textbook problem solving for buffer pH/design
  - quick design sanity checks
---

## Inputs
- target_pH
- pKa
- total_buffer_concentration (optional)
- chosen_conjugate_pair (optional)

## Functions
1. Compute pH from acid/base amounts.
2. Compute required base/acid ratio for a target pH.
3. Score pair suitability by |target_pH - pKa|.
4. Estimate post-addition pH after small strong acid/base perturbation.

## Output policy
- Report assumptions (ideal vs non-ideal).
- Provide confidence and warning when outside practical range.

