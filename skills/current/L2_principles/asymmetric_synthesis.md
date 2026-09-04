# L2 Topic: Asymmetric Synthesis and Stereoselectivity

**Source**: LibreTexts Organic Chemistry; Advanced Organic Chemistry
**Created**: 2026-03-18
**Status**: Pass-1 (Extension of stereochemistry_chirality.md)

---

## Concept Overview

Asymmetric synthesis creates chiral molecules in enantiomerically enriched form. This is critical for pharmaceutical synthesis where one enantiomer is active and the other may be inactive or harmful.

### Key Features
1. **Enantioselectivity**: Preferential formation of one enantiomer
2. **Diastereoselectivity**: Preferential formation of one diastereomer
3. **Chiral auxiliaries**: Temporary chiral controllers
4. **Chiral catalysts**: Enantioselective catalysis
5. **Chiral pool**: Natural chiral building blocks

---

## Core Principles

### Stereochemical Descriptors

| Descriptor | Definition | Example |
|------------|------------|---------|
| ee (enantiomeric excess) | % major - % minor | 90% ee = 95:5 |
| de (diastereomeric excess) | % major - % minor diastereomer | |
| er (enantiomeric ratio) | [R]/[S] ratio | 99:1 er |
| dr (diastereomeric ratio) | Major/minor diastereomer | 10:1 dr |

### Enantiomeric Excess
$$ee = \frac{[R] - [S]}{[R] + [S]} \times 100\%$$

Or equivalently:
$$ee = \frac{[\alpha]_{obs}}{[\alpha]_{pure}} \times 100\%$$

### Methods of Asymmetric Synthesis

| Method | Strategy | Example |
|--------|----------|---------|
| Chiral pool | Natural chiral starting material | Amino acids, sugars |
| Chiral auxiliary | Temporary chiral group | Evans oxazolidinone |
| Chiral reagent | Chiral reactant | CBS reduction |
| Chiral catalyst | Enantioselective catalysis | Noyori hydrogenation |
| Resolution | Separate racemate | Diastereomeric salts |

### Important Chiral Catalysts

| Catalyst | Reaction | Typical ee |
|----------|----------|-----------|
| BINAP-Ru | Hydrogenation | 95-99% |
| Sharpless epoxidation | Epoxidation of allylic alcohols | 90-99% |
| Jacobsen catalyst | Epoxidation of alkenes | 80-98% |
| CBS oxazaborolidine | Reduction of ketones | 95-99% |
| Noyori catalyst | Transfer hydrogenation | 95-99% |
| proline | Aldol reaction | 80-99% |

### Models for Stereoselectivity

**Cram's Rule (for carbonyl addition):**
- Large (L), Medium (M), Small (S) substituents
- Nucleophile attacks from least hindered side

**Felkin-Ahn Model:**
- Considers electronegativity and sterics
- Nucleophile attacks anti to largest group

**Zimmerman-Traxler (aldol):**
- Six-membered chair transition state
- Controls syn/anti selectivity

---

## Decision Trees

### Method Selection
```
Need asymmetric synthesis?
├── Have chiral starting material? → Chiral pool
├── Need temporary control? → Chiral auxiliary
├── Catalytic approach available? → Chiral catalyst
└── Resolution feasible? → Kinetic/dynamic resolution
```

### Catalyst Selection
```
Reaction type?
├── Hydrogenation → BINAP, Noyori
├── Epoxidation → Sharpless, Jacobsen
├── Reduction → CBS, Noyori transfer
├── C-C bond → Asymmetric aldol, Michael
└── Need cheap catalyst? → Organocatalysis (proline)
```

---

## Key Formulas

### Enantiomeric Excess from Optical Rotation
$$ee = \frac{[\alpha]_{obs}}{[\alpha]_{pure}} \times 100\%$$

### Enantiomeric Ratio from ee
$$er = \frac{100 + ee}{100 - ee}$$

### Yield-ee Relationship
For kinetic resolution:
$$\text{yield}_{max} = 50\% \times (1 + \text{selectivity factor})$$

Selectivity factor (s):
$$s = \frac{k_{fast}}{k_{slow}} = \frac{\ln(1-C)(1-ee)}{\ln(1-C)(1+ee)}$$

---

## L3 Implementations Needed

| Function | Purpose |
|----------|---------|
| `ee_from_rotation` | Calculate ee from optical rotation |
| `er_to_ee` | Convert er to ee |
| `yield_from_selectivity` | Kinetic resolution yield |
| `stereochemical_outcome` | Predict Cram/Felkin product |

## L4 Data Needed

| Table | Content |
|-------|---------|
| `chiral_catalysts.csv` | Catalyst, reaction, typical ee |
| `chiral_pool_compounds.csv` | Natural chiral building blocks |

## L5 Examples Needed

| Example | Topic |
|---------|-------|
| Sharpless epoxidation calculation | Predict stereochemistry |
| ee determination | HPLC, NMR, optical rotation |
| Kinetic resolution | Selectivity and yield |

---

**Cross-links:**
- stereochemistry_chirality.md
- organic_reaction_mechanisms.md
- retrosynthetic_analysis.md

## L3 Tool Call Directives


**Source:** `asymmetric_synthesis_tools.py`

L3 tool module for asymmetric synthesis tools

### Available functions:
- `calculate_ee(major_enantiomer: float, minor_enantiomer: float)` → float — Calculate enantiomeric excess (ee%).
- `calculate_dr(major_diast: float, minor_diast: float)` → float — Calculate diastereomeric ratio (dr).
- `calculate_er(major_enantiomer: float, minor_enantiomer: float)` → float — Calculate enantiomeric ratio (er).
- `calculate_de(major_diast: float, minor_diast: float)` → float — Calculate diastereomeric excess (de%).
- `sharpless_epoxidation_prediction(allylic_alcohol_smiles: str, tartrate: str)` → dict — Predict absolute configuration of epoxy alcohol via Sharpless rules.
- `proline_catalyzed_aldol_substrate_check(aldehyde_smiles: str)` → dict — Check if an aldehyde is suitable for L-proline-catalyzed aldol reaction.
- `catalyst_loading_optimization(current_yield: float, current_ee: float, target_ee: float, current_loading: float, min_loading: float, max_loading: float)` → dict — Suggest catalyst loading adjustment based on current vs target ee.
- `binap_substrate_compatibility(substrate_class: str)` → dict — Check BINAP-Ru substrate compatibility.
- `ee_to_er(ee_percent: float)` → float — Convert ee (%) to enantiomeric ratio.
- `er_to_ee(er: float)` → float — Convert enantiomeric ratio to ee (%).
- `dr_to_de(dr: float)` → float — Convert diastereomeric ratio to diastereomeric excess (%).

### Common errors:
- ❌ Passing wrong parameter types (strings where numbers expected)
- ❌ Forgetting required parameters
