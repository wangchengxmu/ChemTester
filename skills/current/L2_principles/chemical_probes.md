---
id: chemical_probes
layer: 2
title: Chemical Probes (Activity-Based Profiling, Covalent Inhibitors)
parent: ../L1_ontology/chemistry-core-map.md#entry-275
stability: high
confidence: high
last_verified: 2026-03-24
source: LibreTexts Biological Chemistry, medicinal chemistry literature
---

# Chemical Probes

## Core Concept

Chemical probes are small molecules designed to interrogate protein function in complex biological systems. Unlike genetic tools, they provide temporal control and can distinguish between protein isoforms based on activity state.

---

## Activity-Based Protein Profiling (ABPP)

### Principle
Covalent probes that label the active site of enzymes only when they are catalytically competent. Inactive (zymogen, inhibited) enzymes are not labeled.

### ABPP Probe Design
1. **Reactive group (warhead):** covalently binds active site nucleophile (Ser, Cys, etc.)
2. **Linker:** spacer of defined length
3. **Reporter tag:** fluorophore or biotin for detection/enrichment

### Common Warheads

| Warhead | Target | Mechanism |
|---------|--------|-----------|
| FP (fluorophosphonate) | Ser hydrolases | Phosphorylates active Ser |
| Vinyl sulfone | Cysteine proteases | Michael addition |
| Epoxide | Cysteine proteases | Ring opening |
| Aziridine | Cysteine proteases | Ring opening |
| β-lactam | Penicillin-binding proteins | Acylation |
| Sulfonate ester | DUBs (deubiquitinases) | Sulfonation |

### ABPP Workflow
1. Treat proteome with activity-based probe
2. Gel electrophoresis + in-gel fluorescence
3. (Optional) Streptavidin enrichment + LC-MS/MS identification
4. Competitive ABPP: pre-treat with inhibitor, then probe → identify target

---

## Covalent Inhibitors

### Mechanism
Electrophilic "warhead" forms irreversible covalent bond with nucleophilic residue (Cys, Ser, Lys) in target protein.

### Kinetic Scheme
$$E + I \underset{k_{off}}{\overset{k_{on}}{\rightleftharpoons}} EI \xrightarrow{k_{inact}} E-I$$

### Key Parameters
- **k_inact/K_i:** efficiency of covalent inhibition (M⁻¹s⁻¹)
- **KI:** dissociation constant for non-covalent complex
- **k_inact:** rate of covalent bond formation

### Successful Examples
- **Ibrutinib (BTK):** acrylamide warhead → Cys481
- **Osimertinib (EGFR):** acrylamide → Cys797
- **Afatinib:** Michael acceptor → multiple Cys

### Warhead Types

| Warhead | Reactivity | Selectivity | Example Drug |
|---------|-----------|-------------|-------------|
| Acrylamide | Moderate | High | Ibrutinib |
| Chloroacetamide | High | Moderate | Afatinib |
| Sulfonyl fluoride | Tunable | High | SGK inhibitor |
| Vinyl sulfonate | High | Low | Research tools |
| Nitrile | Low | Very high | Cathepsin K |

---

## Source Context & Cross-References
- No dedicated chemical probes chapter on LibreTexts (research-level topic)
- LibreTexts Biological Chemistry hub: relevant background on biological catalysis, biomolecular structure, imaging
- LibreTexts Medicinal Chemistry modules cover drug-target interactions relevant to probe design
- Cross-reference: `bioorthogonal_reactions.md` for probe labeling strategies
- Cross-reference: `enzyme_kinetics.md`, `enzyme_mechanisms.md` for target validation
- Key primary literature: Cravatt lab (activity-based protein profiling), Schreiber lab (diversity-oriented synthesis)

---

## Links

- L3: `../L3_functions/chemical_biology_tools.py`
- L4: `../L4_reference/chemical_biology_reference.csv`

---

## [Source: Wikipedia, Chemical Biology]
### Chemical Biology vs Biochemistry
- Chemical biology: Uses chemical tools to study/perturb biological systems.
- Biochemistry: Studies chemistry of biological molecules.
- Key approaches: small-molecule inhibitors, fluorescent probes, chemogenetics, chemoproteomics.

### [Source: Wikipedia, Glycobiology]
### Glycobiology Key Facts
- Glycans: complex carbohydrates (oligosaccharides/polysaccharides) attached to proteins (N-linked, O-linked) and lipids.
- **Monosaccharide building blocks**: Glucose, Mannose, Galactose, Fucose, Sialic acid (Neu5Ac), Glucosamine, Galactosamine, Xylose.
- **N-linked glycosylation**: Asn-X-Ser/Thr sequon; processed in ER and Golgi.
- **O-linked glycosylation**: Ser/Thr residues; initiated in Golgi.
- **Sialic acid cap**: Often terminal; important for immune recognition, pathogen binding.
- Functions: protein folding quality control, cell-cell recognition, immune response, cancer biomarkers.
- Tools: Lectins (glycan-binding proteins), metabolic labeling (Ac₄ManNAz → azido-sialic acid), mass spectrometry.

## L3 Tool Call Directives


**Source:** `chemical_biology_tools.py`

L3 tool module for chemical biology tools

### Available functions:
- `reaction_half_life(k_second_order: float, concentration: float)` → dict — Calculate half-life for a second-order bioorthogonal reaction.
- `bioorthogonal_labeling_efficiency(k_rate: float, time_s: float, conc: float)` → dict — Estimate labeling efficiency (fraction labeled) for second-order reaction.
- `mw_increase_labeling(mw_protein: float, mw_label: float, num_labels: int)` → dict — Calculate MW shift from protein labeling.
- `abpp_ic50(probe_signal_control: float, probe_signal_inhibitor: float, inhibitor_conc: float)` → dict — Calculate apparent IC50 from competitive ABPP data.
- `fluorophore_brightness(extinction_coeff: float, quantum_yield: float)` → dict — Calculate fluorophore brightness.
- `sortase_ligation_yield(conc_substrate: float, conc_probe: float, k_cat: float, k_m: float, time_s: float, enzyme_conc: float)` → dict — Estimate sortase-mediated ligation yield using Michaelis-Menten kinetics.

### Common errors:
- ❌ Passing wrong parameter types (strings where numbers expected)
- ❌ Forgetting required parameters
