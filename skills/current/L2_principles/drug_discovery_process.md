# Drug Discovery Process

## Concept Overview
The drug discovery pipeline transforms a biological hypothesis into an approved therapeutic, spanning target identification through post-market surveillance. Typical timeline: 10–15 years, cost ~$1–2.6 billion per approved drug.

## Key Principles

### Pipeline Stages

1. **Target Identification & Validation**
   - Genomics, proteomics, GWAS, CRISPR screens
   - Disease linkage, druggability assessment (binding pockets, allosteric sites)
   - Biomarker development for target engagement

2. **Hit Discovery**
   - High-throughput screening (HTS): 10⁵–10⁶ compounds, IC₅₀/EC₅₀ primary readout
   - Fragment-based drug discovery (FBDD): low MW fragments (150–250 Da)
   - Virtual screening (structure-based, ligand-based)
   - Phenotypic screening
   - Hit criteria: typically IC₅₀ < 10 µM, novel scaffold

3. **Hit-to-Lead (H2L)**
   - Confirm hit reproducibility, selectivity counterscreens
   - SAR exploration (analog synthesis)
   - Early ADME profiling (solubility, microsomal stability, permeability)
   - Lead criteria: potency < 1 µM, selectivity > 30×, drug-like properties

4. **Lead Optimization**
   - Iterative SAR + structural biology (X-ray, cryo-EM)
   - Optimize potency, selectivity, ADME, PK, safety
   - Candidate selection: preclinical efficacy in animal models

5. **Preclinical Development**
   - GLP toxicology (28-day, 90-day in two species)
   - Safety pharmacology (CNS, CV, respiratory)
   - PK/PD modeling, dose projection
   - IND-enabling studies (genotoxicity, hERG, CYP inhibition)
   - Formulation development

6. **Clinical Development**
   - Phase I: Safety, tolerability, PK in healthy volunteers (20–100 subjects)
   - Phase II: Efficacy, dose-ranging in patients (100–500)
   - Phase III: Pivotal efficacy/safety vs standard of care (1000–5000)
   - Phase IV: Post-marketing surveillance

7. **Regulatory Approval**
   - FDA: NDA (small molecule) or BLA (biologic); review ~10–12 months
   - EMA: Marketing Authorisation Application (centralised/decentralised)
   - Priority review, accelerated approval, breakthrough therapy designations

### Intellectual Property
- Composition of matter patents (20 years from filing)
- Method-of-use patents, formulation patents
- Patent term extensions, data exclusivity
- Freedom-to-operate analysis

### Attrition Rates
- Phase I → approval: ~10–15%
- Phase II → Phase III: ~30–50%
- Top failure causes: lack of efficacy (40–50%), safety/toxicity (30%)

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
