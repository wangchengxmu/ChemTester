# L2 Topic: Asymmetric Hydrosilylation and Transfer Hydrogenation

**Source**: Catalytic Asymmetric Synthesis (Punniyamurthy), Ch6.2
**Created**: 2026-03-20
**Status**: Pass-3
**down_links**: ../L3_functions/asymmetric_synthesis_tools.py
**Parent**: asymmetric_synthesis.md

---

## Concept Overview

Asymmetric hydrosilylation adds a silane (Si-H) across C=O or C=N bonds with enantiocontrol, followed by hydrolysis to give chiral alcohols or amines. Transfer hydrogenation uses organic hydrogen donors (HCO₂H, iPrOH) instead of H₂ gas.

### Hydrosilylation

$$\text{R₂C=O + R₃SiH} \xrightarrow{\text{chiral cat.}} \text{R₂CHOSiR₃} \xrightarrow{\text{H₃O⁺}} \text{R₂CHOH}$$

| Catalyst | Substrate | Typical ee |
|----------|-----------|-----------|
| Chiral Rh complexes | Ketones | 85-98% |
| Chiral Cu/diamine | Ketones | 90-99% |
| Chiral Ti/diol | Aldehydes/ketones | 80-95% |
| Chiral Zn/diamine | Ketones | 85-95% |

### Transfer Hydrogenation (Noyori Bifunctional)

$$\text{Ketone + HCO₂H/Et₃N (5:2)} \xrightarrow{\text{Ru-(S)-BINAP-(S,S)-DPEN}} \text{(R)-Alcohol}$$

**Key feature**: No H₂ gas needed. Formic acid/triethylamine azeotrope is safe and easy to handle.

**Mechanism**: Concerted delivery of H⁻ (from metal) and H⁺ (from amine N-H) via 6-membered transition state. Both the metal and the ligand participate.

**Selectivity**: (S)-BINAP + (S,S)-DPEN → (R)-alcohol (matched pair gives predictable config).

---

**Cross-links:**
- asymmetric_synthesis.md (parent)
- asymmetric_hydrogenation.md (H₂-based)
- asymmetric_reductions.md (CBS, borane)
