# L2 Topic: Chiral Lewis Acid and Brønsted Acid Catalysis

**Source**: Catalytic Asymmetric Synthesis (Punniyamurthy), Ch1; LibreTexts
**Created**: 2026-03-20
**Status**: Pass-1
**Parent**: asymmetric_synthesis.md

---

## Concept Overview

Combined chiral Lewis acid / Brønsted acid systems have been transformative in asymmetric synthesis over the past 20+ years. The synergy between Lewis acid activation of electrophiles and Brønsted acid direction of stereochemistry provides high enantioselectivity across diverse reactions.

### Three Catalytic Systems

| System | Description | Example |
|--------|-------------|---------|
| **BLA** | Brønsted Acid-Assisted Lewis Acid | Oxazaborolidine + TfOH/Tf₂NH |
| **LLA** | Lewis Acid-Assisted Lewis Acid | Achiral Lewis acid activates chiral Lewis acid |
| **LBA** | Lewis Acid-Assisted Brønsted Acid | Lewis acid + chiral Brønsted acid |
| **CPA** | Chiral Phosphoric Acid | BINOL-phosphate, bifunctional |

---

## BLA (Brønsted Acid-Assisted Lewis Acid)

### Catalyst Formation
Proline-derived oxazaborolidine protonated by TfOH or Tf₂NH → chiral BLA

### Reactions Catalyzed

**Diels-Alder**:
- Activates α,β-unsaturated ketones, esters, acids, lactones, enals, quinones
- Excellent endo/exo and face selectivity
- Counterion matters: Tf₂N⁻ (triflimide) > TfO⁻ (triflate) for stability
- Intramolecular Diels-Alder → trans-fused bicyclic products

**Stereochemical model**:
- BLA coordinates to carbonyl oxygen of electrophile
- Dienophile fixed in chiral pocket
- α-Substituted enals show opposite face selectivity vs α,β-unsaturated ketones/esters

**Michael Addition**:
- Silyl ketene acetals + cyclic/acyclic enones
- Ph₃PO additive traps Me₃Si species → improved ee
- Applied to caryophyllene synthesis

**[3+2] Cycloaddition**:
- Benzoquinones + 2,3-dihydrofuran → chiral phenolic tricycles
- Applied to aflatoxin B₂ total synthesis

**β-Lactone Synthesis**:
- Aldehyde + ketene → β-lactone (first for α-branched aldehydes)
- BLA + Bu₃SnOTf ion pair mechanism

---

## LLA (Lewis Acid-Assisted Lewis Acid)

Achiral Lewis acid (e.g., Me₃SiOTf, SnCl₄) activates chiral Lewis acid via complex formation. The reactivity of the combined system is much greater than the chiral Lewis acid alone.

---

## LBA (Lewis Acid-Assisted Brønsted Acid)

Lewis acid coordinates to heteroatom of chiral Brønsted acid → increases acidity. Chiral counterion directs enantioselectivity.

---

## Chiral Phosphoric Acids (CPAs)

BINOL-derived phosphoric acids as bifunctional Brønsted acid catalysts:
- Activate imines via protonation
- H-bond to substrates
- Chiral pocket from 3,3'-substituents on BINOL controls face selectivity
- Applications: transfer hydrogenation, Mannich, Michael, Friedel-Crafts

---

## L3 Implementations Needed

| Function | Purpose |
|----------|---------|
| `predict_bla_diels_alder_stereochemistry` | BLA + diene + dienophile → predict stereochemistry |

## L5 Examples Needed
- BLA-catalyzed total synthesis of caryophyllene
- Aflatoxin B₂ via [3+2] cycloaddition

---

**Cross-links:**
- asymmetric_synthesis.md (parent)
- lewis_acid_base.md
- pericyclic_reactions.md (Diels-Alder theory)
