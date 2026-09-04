# Pharmacodynamics & Drug Targets

## Concept Overview
Pharmacodynamics (PD) describes what the drug does to the body — the molecular interaction between a drug and its biological target, and the resulting physiological response.

## Key Principles

### Drug Target Classes

| Target | % of Drugs | Examples |
|--------|-----------|---------|
| GPCRs | ~34% | β-adrenergic, opioid, histamine receptors |
| Enzymes | ~22% | ACE, COX, kinases, PDE |
| Ion Channels | ~6% | Na⁺, K⁺, Ca²⁺ channels |
| Nuclear Receptors | ~16% | ER, GR, PPAR, RAR |
| Transporters | ~3% | DAT, SERT, NET |
| Structural Proteins | ~3% | Tubulin, microtubules |

### Receptor Theory
- **Occupation model**: Response ∝ fraction of receptors occupied
- **Operational model**: E = (Emax × τ × [A]) / (KA + [A] × (1 + τ))
  - τ = intrinsic efficacy / KC (efficacy term)
  - KA = equilibrium dissociation constant

### Dose-Response Relationships
- **EC₅₀**: concentration producing 50% of maximal response
- **IC₅₀**: concentration producing 50% inhibition
- **Hill equation**: E = E_bottom + (E_top - E_bottom) / (1 + 10^((log EC₅₀ - log[A]) × nH))
  - nH = Hill slope (cooperativity)
- **Ki (inhibition constant)**: true thermodynamic binding affinity
  - Cheng-Prusoff: Ki = IC₅₀ / (1 + [S]/Km)

### Drug Classification by Effect
- **Agonist**: binds and activates receptor (full, partial, inverse)
- **Antagonist**: binds but does not activate; blocks agonist (competitive, non-competitive)
- **Allosteric modulator**: binds at site distinct from orthosteric, modulates activity
- **Positive allosteric modulator (PAM)**: enhances agonist response
- **Negative allosteric modulator (NAM)**: reduces agonist response

### Signal Transduction
- GPCR: Gα_s (↑cAMP), Gα_i (↓cAMP), Gα_q (↑IP₃/DAG, Ca²⁺)
- Kinase cascades: MAPK/ERK, PI3K/Akt, JAK/STAT
- Nuclear receptor: ligand → nuclear translocation → DNA binding → gene transcription

### Therapeutic Index
```
TI = TD₅₀ / ED₅₀  (or LD₅₀ / ED₅₀)
```
- TI > 10: wide safety margin
- TI < 2: narrow therapeutic window (e.g., digoxin, warfarin)

## L3 Tools
-> `../L3_functions/medicinal_chemistry_tools.py`

## L4 Reference Data
-> `../L4_reference/medicinal_data.csv`

## L5 Worked Examples
-> `../L5_examples/medicinal_examples.md`

---

## Source Attribution: de Araujo et al., An Introduction to Medicinal Chemistry and Molecular Recognition (LibreTexts)
[Source: de Araujo et al., An Introduction to Medicinal Chemistry and Molecular Recognition](https://chem.libretexts.org/Bookshelves/Biological_Chemistry/An_Introduction_to_Medicinal_Chemistry_and_Molecular_Recognition_(de_Araujo_et_al.))

- Comprehensive resource covering small molecule drug discovery from a medicinal chemist's perspective.
- Guides reader through the entire drug development process.
- Provides knowledge and tools for interrogating structure and function of bioactive molecules.

## Source Attribution: Davis, Medicines by Design (LibreTexts)
[Source: Davis, Medicines by Design](https://chem.libretexts.org/Bookshelves/Biological_Chemistry/Medicines_by_Design_(Davis))

- NIH/NIGMS-sponsored resource explaining how medicines work in the body.
- Pharmacology = broad discipline encompassing drug discovery, development, and testing of drug action.
- Crossroads of chemistry, genetics, cell biology, physiology, and engineering.
