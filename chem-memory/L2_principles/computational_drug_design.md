# Computational Drug Design

## Concept Overview
Computational methods accelerate drug discovery by predicting binding affinity, screening large chemical libraries, and guiding molecular optimization before synthesis.

## Key Principles

### Molecular Docking
- Predicts binding pose and affinity of ligand in protein binding site
- Key components: search algorithm (genetic, Monte Carlo, systematic) + scoring function
- Scoring functions: force-field-based, empirical, knowledge-based
- Tools: AutoDock Vina, Glide, GOLD, rDock
- Limitations: scoring function accuracy (~1–2 kcal/mol RMSE), protein flexibility, solvation

### Virtual Screening
- **Structure-based**: dock library into target protein structure (X-ray, cryo-EM, homology model)
- **Ligand-based**: use known actives to find similar compounds (fingerprint similarity, pharmacophore)
- Library sizes: 10⁶–10⁹ (ultra-large); enrichment factor = key metric
- False positives managed by consensus scoring, post-docking filters

### Pharmacophore Modeling
- Abstract description of steric/electronic features for bioactivity
- Features: H-bond donor/acceptor, hydrophobic, aromatic, positive/negative ionizable, metal coordinator
- 3D pharmacophore: spatial arrangement of features
- Use: virtual screening, scaffold hopping, lead hopping

### Molecular Dynamics (MD) in Drug Design
- Simulates atomic motion over time (fs–µs timescale)
- Applications:
  - Binding free energy calculation (MM/PBSA, MM/GBSA)
  - Water displacement analysis
  - Protein conformational changes (induced fit)
  - Membrane permeability simulation

### Free Energy Perturbation (FEP)
- Alchemical transformation: calculate ΔΔG for ligand modification
- Accuracy: ~1 kcal/mol (sufficient for rank ordering)
- FEP+ (Schrödinger), GROMACS, AMBER
- Critical for lead optimization: predicts potency changes from small structural modifications

### QSAR Beyond Basics
- **3D-QSAR**: CoMFA, CoMSIA — uses 3D alignment of molecules
- **Machine Learning QSAR**: random forest, gradient boosting, graph neural networks (GNN)
- **Applicability domain**: prediction valid only within chemical space of training set
- See also L1 entry 209 for foundational QSAR

### ADMET Prediction (In Silico)
- **Absorption**: Caco-2 permeability, human intestinal absorption (HIA)
- **Distribution**: Vd prediction, BBB penetration, P-gp substrate
- **Metabolism**: CYP450 substrate/inhibition prediction
- **Excretion**: renal clearance prediction
- **Toxicity**: hERG inhibition, AMES mutagenicity, hepatotoxicity, DILI
- Tools: ADMET Predictor, QikProp, pkCSM, admetSAR

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
