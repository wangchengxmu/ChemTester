---
id: L2.asymmetric_biocatalysis
layer: 2
title: Enzyme-Catalyzed Asymmetric Reactions (Biocatalysis)
parent_L1: chemistry.core_map
source: Punniyamurthy, Ch11 - Enzyme-Catalyzed Asymmetric Reactions
confidence: medium
change_type: new
last_verified: 2026-03-21
---

# Enzyme-Catalyzed Asymmetric Reactions (Biocatalysis)

Biocatalysis uses enzymes to perform asymmetric transformations with excellent enantioselectivity under mild conditions (aqueous, room temperature, neutral pH). Enzymes are nature's chiral catalysts â?their active sites provide stereochemical control superior to most synthetic catalysts. Biocatalytic methods are now standard in pharmaceutical manufacturing.

**Advantages**: High enantioselectivity (often >99% ee), mild conditions, environmentally benign, scalable to industrial production.

---

## 11.1 Enzymatic Resolution â?Acylation of Alcohols and Amines

### Kinetic Resolution of Alcohols
- **Lipase-catalyzed** enantioselective acylation of racemic alcohols with vinyl esters
- **Max 50% yield** for simple resolution â?overcome via **dynamic kinetic resolution (DKR)**
- **DKR = lipase resolution + metal-catalyzed racemization** of unwanted enantiomer
  - Ru complex + CAL-B (Candida antarctica lipase B) â?78-92% yield, 99% ee
  - Al complex (AlMeâ?BINOL) + CAL-B â?99% yield, 98% ee

### Resolution of Amines
- Lipase-catalyzed acylation in organic medium (MTBE)
- E values >2000 (excellent enantioselectivity)
- One enantiomer converted to amide; remaining amine recovered in enriched form

### Hydrolytic Resolution
- **Ester hydrolysis**: Lipases/esterases/proteases resolve racemic esters
  - Remote chiral center recognition possible (e.g., Lasofoxifene synthesis, E >300)
  - Scalable: 40 kg-scale indole ethyl ester resolution at 100 g/L
- **Nitrile hydrolysis**: Nitrilases (e.g., from *A. faecalis*) â?(R)-mandelic acid from Î±-hydroxynitriles
- **Hydantoin hydrolysis**: Hydantoinases + carbamoylases cascade â?Î±-amino acids
- **Epoxide hydrolysis**: Epoxide hydrolases (e.g., *Methylobacterium* sp.) â?chiral diols

---

## 11.2 Biocatalytic C-C Bond Formation

### Hydrocyanation of Aldehydes
- **Oxynitrilase-catalyzed** (Griengl process): Industrial production of (S)-cyanohydrins
- Key intermediate for pyrethroid manufacture
- Broad substrate scope for aldehydes

### Benzoin Condensation
- **Benzaldehyde lyase** (BAL) catalyzes cross-benzoin between two different benzaldehydes
- One aldehyde = donor (converted to acyl anion equivalent), other = acceptor
- Highly enantiomerically enriched mixed benzoins

### Aldol Reactions
- **Threonine aldolases**: Glycine (donor) + substituted benzaldehyde (acceptor) â?Î±-amino Î²-hydroxy acids
- Donor-specific, broad acceptor scope, excellent enantioselectivity
- Direct access to non-natural amino acid derivatives

### Nitroaldol (Henry) Reaction
- **(S)-Oxynitrilase** catalyzes nitromethane + aldehydes â?Î²-nitro alcohols
- Non-natural enzymatic reaction (enzyme promiscuity)
- Nitroalkane = donor, aldehyde = acceptor, excellent ee

---

## 11.3 Enzyme-Catalyzed Reductions

### Ketone Reduction (â?Chiral Alcohols)
- **Alcohol dehydrogenases (ADHs)** with NAD(P)H cofactor
- **Key systems**:

| ADH Source | Substrate | ee | Note |
|-----------|-----------|-----|------|
| *Leifsonia* sp. | Substituted acetophenones | High | 2-propanol as H-donor |
| *L. brevis* (in *E. coli*) | 2,5-Diketo esters | >99% | Regio- and enantioselective |
| *R. ruber* ADH | Broad ketone scope | Excellent | 2-propanol solvent |
| FDH (formate dehydrogenase) | Î²-Keto esters | >99% | Formate â?COâ?|
| *A. calcoaceticus* ADH + GDH | Statin intermediate | 99% | 6-benzyloxy-3,5-dioxohexanoate |

### Cofactor Regeneration Strategies
1. **Substrate-coupled**: 2-propanol â?acetone (reduces NADPâ?via ADH)
2. **FDH system**: Formate â?COâ?(reduces NADâ?
3. **GDH system**: D-glucose â?D-gluconolactone â?D-gluconic acid (irreversible, drives equilibrium)
4. **PNT (pyridine nucleotide transhydrogenase)**: Bridges NADH/NADPâ?pools

### Recombinant Whole-Cell Systems
- *E. coli* co-expressing ADH + GDH â?no external cofactor needed
- Works in pure aqueous media, economical and scalable
- Tailor-made biocatalysts with both enzymes overexpressed

### Reductive Amination (â?Chiral Î±-Amino Acids)
- **Amino acid dehydrogenases** + cofactor regeneration
- L-*tert*-Leucine via leucine dehydrogenase + FDH (pharma building block)
- L-6-Hydroxynorleucine via glutamate dehydrogenase + GDH
- Whole-cell DKR: *Pichia pastoris* overexpressing Phe dehydrogenase + FDH

### Reduction of C=C Bonds
- **Enoate reductases**: Reduce Î±,Î²-unsaturated ketones, carboxylic acids, nitroalkenes
- *Candida macedoniensis* enolate reductase + GDH: ketoisophorone â?(R)-levodione
- *Burkholderia* sp. enoate reductase: Î±-chloroacrylic acid â?Î±-chloropropionate
- Z-Nitroalkenes â?2-substituted 3-nitropropanoates with high ee

### Transamination (â?Chiral Amines)
- **Transaminases**: Î±-keto acids â?Î±-amino acids; ketones â?chiral amines
- Coupled with aspartate aminotransferase + cysteine sulfinic acid â?3/4-substituted glutamic acids
- (S)-Methoxyisopropylamine via recombinant whole-cell at high substrate concentration

---

## 11.4 Enzyme-Catalyzed Oxidations

### Baeyer-Villiger Oxidation
- **Baeyer-Villiger monooxygenases (BVMOs)**: Ketones â?lactones/esters
- NADPH-dependent, cofactor recycled in situ
- 4-Substituted cyclohexanones â?lactones with high ee
- Scalable: 25 g/L racemic bicyclo[3.2.0]hept-2-enone â?regioisomeric lactones
- **Double oxidation**: CHMO + ADH from *T. brockii* â?alcohol â?lactone (no external cofactor)

### Epoxidation
- **Styrene monooxygenases**: FAD/NADH-dependent alkene epoxidation
- Recombinant whole-cell catalysts in aqueous-organic emulsions
- Styrene derivatives â?(S)-epoxides with high ee

### Alcohol Oxidation (â?Ketones)
- ADH from *R. ruber* with acetone/2-propanol cofactor recycling
- Selective oxidation of one enantiomer from racemic alcohols (kinetic resolution)

### Sulfoxidation
- **Chloroperoxidase**: Sulfides â?chiral sulfoxides
- Cyclopentyl methyl sulfide â?sulfoxide with excellent conversion and ee
- Chiral sulfoxides as auxiliaries and drug intermediates (e.g., omeprazole)

### Amino Acid Oxidation
- Leucine amino dehydrogenase + NADH-oxidase: Racemic *tert*-leucine â?D-*tert*-leucine

---

## Key Design Principles

1. **Enzyme selection**: Match enzyme class to desired transformation
2. **Cofactor strategy**: Choose regeneration method based on economics
3. **Whole-cell vs isolated**: Whole-cell simpler (no cofactor addition) but may have side reactions
4. **Solvent engineering**: Organic cosolvents for hydrophobic substrates; aqueous for most enzymes
5. **Immobilization**: Enables catalyst recycling, especially important at scale

## Related L2 Files
- `enzyme_kinetics.md` â?Michaelis-Menten, enzyme efficiency
- `enzyme_mechanisms.md` â?catalytic strategies, cofactors, active site chemistry
- `asymmetric_reductions.md` â?chemical asymmetric reductions (CBS, borane)
- `protecting_groups.md` â?orthogonal protection relevant to multi-step biocatalysis


## Implementations

- Implementation: `../L3_functions/asymmetric_biocatalysis_tools.py`

## L3 Tool Call Directives


**Source:** `asymmetric_biocatalysis_tools.py`

L3 tool module for asymmetric biocatalysis tools

### Available functions:
- `dkr_calculator(conversion: float, ee_product: float)` → dict — Dynamic Kinetic Resolution calculator.
- `cofactor_regeneration_efficiency(nadh_initial_umol: float, nadh_consumed_umol: float, cosubstrate_mmol: float, ttn_target: int)` → dict — Calculate cofactor regeneration efficiency.
- `enantioselectivity_from_E(E_value: float, conversion: float)` → dict — Predict ee from E-value (and optionally conversion).

### Common errors:
- ❌ Passing wrong parameter types (strings where numbers expected)
- ❌ Forgetting required parameters
