# Medicinal Chemistry Principles

## Concept Overview
Medicinal chemistry applies chemical principles to design and optimize drug molecules. Core concepts balance potency, selectivity, pharmacokinetics, and safety through molecular modification.

## Key Principles

### Lipinski's Rule of Five (Ro5)
For oral bioavailability, most "drug-like" molecules satisfy:
- MW ≤ 500 Da
- logP ≤ 5
- H-bond donors (OH, NH) ≤ 5
- H-bond acceptors (N, O) ≤ 10
- Violations of ≥2 → likely poor oral absorption

### Bioisosteres
Replace a functional group with one having similar steric/electronic properties:

| Original | Bioisostere | Example |
|----------|------------|---------|
| -COOH | -Tetrazole | Losartan |
| -NH₂ | -OH, -F | Fluoro-aniline |
| Phenyl | Thiophene, pyridine | Thiophene swap |
| -CH₂- | -O-, -S-, -NH- | Ether bridge |
| -CF₃ | -Cl, -CN | Trifluoromethyl swap |

### logP and logD
- **logP**: partition coefficient (octanol/water) for neutral species
- **logD₇.₄**: distribution coefficient at pH 7.4 (accounts for ionization)
- logD = logP + log(fraction unionized)
- Optimal CNS drugs: logP 1–3, logD₇.₄ 1–3

### Solubility
- Aqueous solubility critical for absorption: >10 µg/mL desirable
- Henderson-Hasselbalch governs pH-dependent solubility for ionizable drugs
- Salt formation, prodrugs, co-crystals improve solubility

### Prodrugs
- Promote absorption, mask toxicity, improve solubility or targeting
- Types: carrier-linked (ester, amide) and bioprecursor
- Examples: enalapril → enalaprilat, clopidogrel (prodrug), valacyclovir

### Drug Metabolism & Reactive Metabolites
- Soft drugs: designed for rapid metabolism after action
- Hard drugs: metabolically stable (risk of bioaccumulation)
- **Toxicophores**: structural alerts for reactive metabolite formation
  - Anilines → N-oxide, nitroso → hepatotoxicity
  - Thiophenes → epoxide → liver injury
  - Michael acceptors → protein adducts
  - Aromatic nitro → reduction → mutagenic metabolites

### Veber's Rules (supplementary)
- Rotatable bonds ≤ 10 (oral bioavailability)
- Polar surface area ≤ 140 Å²

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

## L3 Tool Call Directives

**Source:** medicinal_chemistry_tools.py
Medicinal Chemistry Tools - L3 Implementation

### Available functions:
- lipinski_check(mw, logp, hbd, hba) →  — Evaluate Lipinski's Rule of Five for drug-likeness.
- bioavailability_calc(f_abs, f_gut, f_hepatic) → float — Calculate overall oral bioavailability.
- half_life_from_clearance(cl, vd) → float — Calculate elimination half-life from clearance and volume of distribution.
- ic50_to_ki(ic50, substrate_conc, km) → float — Convert IC50 to Ki using the Cheng-Prusoff equation.
- pk_parameters(dose, auc, f, c0, tau) →  — Calculate core PK parameters.
- hill_response(conc, ec50, emax, emin, hill_slope) → float — Calculate response using the Hill equation.
- therapeutic_index(td50, ed50) → float — Calculate therapeutic index: TD50/ED50.

### Common errors:
- ❌ Passing wrong parameter types or missing required arguments
