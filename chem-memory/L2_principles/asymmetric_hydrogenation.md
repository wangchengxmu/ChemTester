# L2 Topic: Asymmetric Hydrogenation

**Source**: Catalytic Asymmetric Synthesis (Punniyamurthy), Ch6; LibreTexts
**Created**: 2026-03-20
**Status**: Pass-1
**Parent**: asymmetric_synthesis.md

---

## Concept Overview

Catalytic asymmetric hydrogenation adds H₂ across C=C, C=O, or C=N bonds with high enantioselectivity. The most important class of industrial asymmetric catalysis.

### Key Catalyst Systems

| Catalyst | Substrate | Metal | Typical ee |
|----------|-----------|-------|-----------|
| BINAP-Ru | α,β-Unsaturated acids | Ru(II) | 95-99% |
| BINAP-Ru | Allylic alcohols | Ru(II) | 94-99% |
| DIPAMP-Rh | α,β-Unsaturated α-amino acids | Rh(I) | 95-99% |
| DuPHOS-Rh | α,β-Unsaturated α-amino acids | Rh(I) | 95-99% |
| BINAP-Rh | Allylic amines | Rh(I) | 96-99% |
| Noyori-Ru | Ketones (transfer H₂) | Ru(II) | 95-99% |
| CBS | Ketones (hydride) | B | 95-99% |
| Phosphanodihydrooxazole-Ir | Allylic alcohols | Ir | high |

---

## BINAP Ligand

### Structure & Synthesis
- 2,2'-Bis(diphenylphosphino)-1,1'-binaphthyl
- Axially chiral (atropisomerism)
- (S)-BINAP: [α]²¹D = −29.4° (THF), mp 205°C, 99% ee
- (R)-BINAP: [α]²¹D = +26.2 to 30.9° (THF), mp 207°C, 99% ee
- Synthesized via resolution of racemic BINOL or 2,2'-dibromo-BINAP

---

## Substrate Classes

### 1. α,β-Unsaturated Carboxylic Acids
$$\text{ArCH=CHCOOH} \xrightarrow{\text{Ru-(S)-BINAP, H₂ (50-100 atm)}} \text{(S)-ArCH₂CHCOOH}$$

**Key example**: (S)-Naproxen synthesis (98% ee) — NSAID

### 2. Allylic Alcohols
- Geraniol → (S)-citronellol (94% ee) → L-(+)-menthol
- Nerol → (S)-citronellol (99% ee)
- Lillial synthesis via Ir-phosphanodihydrooxazole

### 3. Allylic Amines (Isomerization-Hydrogenation)
- Rh-(S)-BINAP isomerizes geranyl diethylamine → (R)-citronellal enamine
- Hydrolysis → (R)-citronellal (96-99% ee)
- Industrial L-(+)-menthol route

### 4. α,β-Unsaturated α-Amino Acids
- Rh-DIPAMP → L-DOPA (Parkinson's drug) — **Monsanto process**
- Rh-DuPHOS → chiral amino acids (excellent ee)
- Most successful chiral biphosphines: DIPAMP, DuPHOS, BPE

### 5. Ketones (Asymmetric Hydrogenation)
- Ru-BINAP + diamine (Noyori system)
- Chiral phosphines: BICP, BPPM, DIOP for Rh-catalyzed C=O reduction
- α-Keto esters: Rh catalysts effective

### 6. Imines (C=N Reduction)
- Key for chiral amine synthesis (pharmaceutical intermediates)
- Chiral Rh and Ir catalysts developed

---

## Mechanistic Principles

### Ru-BINAP Hydrogenation (C=C)
1. H₂ oxidative addition to Ru center
2. Substrate coordination via carboxylate group
3. Migratory insertion of C=C into Ru-H
4. Reductive elimination → saturated product
5. Steric bulk of BINAP determines face of approach

### Kinetic Resolution
For racemic substrates:
$$s = \frac{k_{fast}}{k_{slow}} = \frac{\ln(1-C)(1-ee)}{\ln(1-C)(1+ee)}$$

---

## L3 Implementations Needed

| Function | Purpose |
|----------|---------|
| `predict_hydrogenation_config` | BINAP chirality + substrate → product (R/S) |
| `ee_from_selectivity_factor` | Kinetic resolution yield and ee |

## L5 Examples Needed
- Monsanto L-DOPA process (Rh-DIPAMP)
- Takasago L-menthol process (Rh-BINAP isomerization)
- (S)-Naproxen synthesis

---

**Cross-links:**
- asymmetric_synthesis.md (parent)
- organometallic_chemistry.md (metal-ligand complexes)
- stereochemistry_chirality.md
