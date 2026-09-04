# L2 Topic: Asymmetric Ring-Opening and Cycloaddition

**Source**: Catalytic Asymmetric Synthesis (Punniyamurthy), Ch7-9
**Created**: 2026-03-20
**Status**: Pass-3
**down_links**: ../L3_functions/asymmetric_synthesis_tools.py
**Parent**: asymmetric_synthesis.md

---

## Concept Overview

Asymmetric ring-opening of meso-epoxides and cycloaddition reactions ([3+2], [4+2], [2+2+2]) create multiple stereocenters in one step with high enantiocontrol.

### Asymmetric Epoxide Ring-Opening (Desymmetrization)

Meso-epoxides (symmetric) are opened with nucleophiles using chiral catalysts to give enantiomerically enriched 1,2-difunctional compounds.

$$\text{meso-Epoxide + NuH} \xrightarrow{\text{chiral cat.}} \text{chiral 1,2-functionalized}$$

| Catalyst | Nucleophile | Typical ee |
|----------|-------------|-----------|
| Co-salen | H₂O (hydrolytic) | 95-99% |
| Cr-salen | TMSN₃ (azidolysis) | 90-98% |
| Mn-salen | ROH (alkoxylation) | 85-95% |
| Chiral phosphoric acid | Amines (aminolysis) | 80-95% |

**Jacobsen hydrolytic kinetic resolution (HKR)**: Racemic epoxides resolved using Co-salen + H₂O. One enantiomer reacts fast, the other slow (s > 200).

### Asymmetric Cycloadditions

**[4+2] Diels-Alder**: Chiral Lewis acid or organocatalyst controls endo/exo and face selectivity (see chiral Lewis acid catalysis L2).

**[3+2] Cycloaddition**: Azomethine ylides + dipolarophiles → pyrrolidines. Cu(I)-bisoxazoline or Ag(I)-phosphine catalysts.

**[2+2+2] Cyclotrimerization**: Alkynes → chiral arenes/cyclohexadienes. Rh(I) or Co(I) with chiral ligands.

### Kinetic Resolution in Ring-Opening

$$s = \frac{k_{fast}}{k_{slow}}$$

For practical resolution: s ≥ 20 needed for >90% ee at 50% conversion.

---

**Cross-links:**
- asymmetric_synthesis.md (parent)
- asymmetric_epoxidation.md (epoxide synthesis)
- pericyclic_reactions.md (DA theory)
- chiral_lewis_acid_bronsted_acid_catalysis.md
