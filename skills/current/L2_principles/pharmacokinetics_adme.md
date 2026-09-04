# Pharmacokinetics & ADME

## Concept Overview
Pharmacokinetics (PK) describes what the body does to a drug via four processes: Absorption, Distribution, Metabolism, Excretion. PK parameters guide dosing regimen design.

## Key Principles

### Absorption
- **pH-partition hypothesis**: unionized drug crosses membranes; ratio given by Henderson-Hasselbalch
- **Biopharmaceutics Classification System (BCS)**:

| Class | Solubility | Permeability | Example |
|-------|-----------|-------------|---------|
| I | High | High | Metoprolol |
| II | Low | High | Ibuprofen |
| III | High | Low | Atenolol |
| IV | Low | Low | Furosemide |

- **Fick's Law**: J = -D × (ΔC/Δx), flux proportional to concentration gradient
- **Bioavailability (F)**: F = (AUC_oral / AUC_IV) × 100%

### Distribution
- **Volume of Distribution (Vd)**: Vd = Dose / C₀ (theoretical volume)
  - Vd < 0.6 L/kg: confined to plasma/extracellular
  - Vd > 1 L/kg: extensive tissue distribution
- **Protein Binding**: fu = unbound fraction; only unbound drug is pharmacologically active
  - Albumin: acidic drugs; α₁-acid glycoprotein: basic drugs
- **Blood-Brain Barrier**: tight junctions, P-gp efflux, logP 1–3 optimal for CNS penetration

### Metabolism
- **Phase I** (functionalization): CYP450 oxidation, reduction, hydrolysis
  - Major CYPs: 3A4 (~40% drugs), 2D6, 2C9, 2C19, 1A2
  - CYP inhibition/induction → drug-drug interactions
- **Phase II** (conjugation): glucuronidation (UGT), sulfation, acetylation, glutathione
- **First-pass metabolism**: oral drug metabolized before systemic circulation
  - Hepatic extraction ratio: E = (CL_int × fu) / (Q + CL_int × fu)

### Excretion
- **Renal**: glomerular filtration + active tubular secretion + reabsorption
  - CL_renal = fu × GFR + CL_secretion
- **Hepatobiliary**: for MW > 500 Da, amphiphilic compounds
- **Half-life (t½)**: t½ = 0.693 × Vd / CL
- **Steady state**: ~5 × t½ to reach 94% of steady-state concentration
  - Css,avg = (F × Dose) / (τ × CL) where τ = dosing interval

### Key PK Parameters
```
CL (clearance) = Dose / AUC
Vd = CL / k_elim
t½ = ln(2) / k_elim
AUC = F × Dose / CL
Cmax = (F × Dose / Vd) × (1 / (1 - e^(-k×τ)))
```

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
