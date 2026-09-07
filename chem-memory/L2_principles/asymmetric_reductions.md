# L2 Topic: Asymmetric Reductions (Non-H₂)

**Source**: Catalytic Asymmetric Synthesis (Punniyamurthy), Ch6.3-6.4
**Created**: 2026-03-20
**Status**: Pass-3
**down_links**: ../L3_functions/asymmetric_synthesis_tools.py
**Parent**: asymmetric_synthesis.md

---

## Concept Overview

Asymmetric reductions of C=O and C=N bonds using hydride donors (borane, silanes, formic acid) instead of molecular H₂.

### Key Methods

| Method | Reagent | Substrate | Typical ee |
|--------|---------|-----------|-----------|
| CBS reduction | BH₃·THF + oxazaborolidine | Ketones | 95-99% |
| Asymmetric borane | BH₃ + chiral amino alcohol | Ketones | 90-99% |
| Meerwein-Ponndorf-Verley (MPV) | Al(OiPr)₃ + chiral ligand | Aldehydes/ketones | 80-95% |
| Noyori transfer H₂ | HCO₂H/Et₃N + Ru-BINAP/diamine | Ketones | 95-99% |
| Asymmetric hydrosilylation | R₃SiH + chiral catalyst | Ketones/imines | 85-98% |

### CBS (Corey-Bakshi-Shibata) Reduction

Most widely used non-H₂ reduction. Chiral oxazaborolidine (derived from amino alcohol + borane) transfers hydride to si- or re-face of ketone.

$$\text{R₁R₂C=O} \xrightarrow{\text{CBS cat. (5-10 mol\%), BH₃·THF}} \text{R₁R₂CHOH}$$

**Face selectivity**: (R)-CBS catalyst → R-alcohol; (S)-CBS → S-alcohol. Determined by the amino alcohol chirality (diphenylprolinol).

**Scope**: Aryl alkyl ketones (best), dialkyl ketones (moderate), α,β-unsaturated (1,2-selective).

### Asymmetric Transfer Hydrogenation (Noyori)

Ru-BINAP + chiral diamine (e.g., DAIPEN) with formic acid/triethylamine azeotrope (5:2) as hydrogen source.

**Mechanism**: Bifunctional — metal-hydride and NH proton deliver H₂ simultaneously in a concerted 6-membered TS.

---

**Cross-links:**
- asymmetric_synthesis.md (parent)
- asymmetric_hydrogenation.md (H₂ methods)
- asymmetric_hydrosilylation.md (silane reductants)
