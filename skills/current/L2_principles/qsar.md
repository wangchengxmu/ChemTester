---
id: qsar.quantitative_structure_activity
layer: 2
title: Quantitative Structure-Activity Relationships (QSAR)
stability: high
confidence: high
constraints:
  - QSAR models are domain-specific; predictions reliable only within applicability domain
  - Requires quality experimental data for model training
  - Validation essential before regulatory use
last_verified: 2026-03-17
change_type: new
source: LibreTexts Organic Chemistry (Bruice Ch31.9); PMC QSAR Review; OECD Guidance
---

## Context

QSAR models mathematically relate chemical structure to biological activity or property. They enable:
- Prediction of activities for untested compounds
- Lead optimization in drug discovery
- Toxicity screening and risk assessment
- Prioritization of compounds for synthesis/testing

**Fundamental Equation**:
```
Activity = f(physicochemical properties / structural properties) + error
```

The error includes model error (bias) and observational variability.

---

## Core Principles

### 1. QSAR Dimensionality Evolution

| Type | Dimension | Description | Parameters |
|------|-----------|-------------|------------|
| 1D-QSAR | 1D | pKa and log P correlation | Dissociation constant, partition coefficient |
| 2D-QSAR | 2D | Overall structure pattern | Molecular refractivity, topological indices, dipole moment |
| 3D-QSAR | 3D | 3D structure properties | Steric hindrance, H-bond donors/acceptors, hydrophobic fields |
| 4D-QSAR | 4D | Multiple ligand conformations | Ensemble of conformers, induced fit |
| 5D-QSAR | 5D | Multiple docked representations | Ligand-receptor binding modes |
| 6D-QSAR | 6D | Molecular dynamics simulations | Time-dependent conformational changes |

### 2. Molecular Descriptors

Mathematical representations of molecular information. Three major categories:

#### 2.1 Topological Descriptors (2D)
- **Wiener Index**: Sum of all bond lengths in molecular graph
- **Molecular Connectivity Index (Ï)**: Branching and cyclicity
- **Kappa Indices (Îº)**: Shape descriptors
- **Topological Polar Surface Area (tPSA)**: Drug absorption predictor

```
Wiener Index: W = Î£_i<j d_ij
where d_ij = number of bonds between atoms i and j
```

#### 2.2 Electronic Descriptors
- **Partial charges**: Electrostatic potential-derived (Gasteiger-Marsili)
- **Dipole moment**: Molecular polarity
- **HOMO/LUMO energies**: Reactivity indicators (from quantum calculations)
- **Electrotopological state (E-state)**: Atom-level electronic environment

```
Gasteiger-Marsili charge: q_i = q_i^0 + Î£_j (q_j - q_i) / f(Ï_i, Ï_j)
```

#### 2.3 Geometric/3D Descriptors
- **Molecular volume (V)**: Steric bulk
- **Surface area**: Solvent-accessible surface area (SASA)
- **Shape indices**: Globularity, asphericity
- **Molecular refractivity (MR)**: Polarizability-related

```
MR = (nÂ² - 1) / (nÂ² + 2) Ã M/d
where n = refractive index, M = molecular weight, d = density
```

#### 2.4 Physicochemical Descriptors
- **logP (octanol-water partition coefficient)**: Lipophilicity
- **logS**: Aqueous solubility
- **pKa**: Acid dissociation constant
- **Molecular weight (MW)**: Size

### 3. Model Building Methods

#### 3.1 Multiple Linear Regression (MLR)

Simplest QSAR model for small descriptor sets:

```
Y = bâ + bâXâ?+ bâXâ?+ ... + bâXâ?+ Îµ
```

**Requirements**:
- Descriptor:compound ratio â?1:5 (minimum)
- Low multicollinearity (VIF < 5)
- Normal residuals

**R Implementation**:
```r
model <- lm(activity ~ descriptor1 + descriptor2 + descriptor3, data = dataset)
summary(model)
vif(model)  # Check multicollinearity
```

#### 3.2 Partial Least Squares (PLS)

Handles multicollinearity and many descriptors:

```
Y = TQ' + E
where T = XW (scores), W = weight matrix
```

**Advantages**:
- Works with more descriptors than compounds
- Handles correlated descriptors
- Provides variable importance (VIP scores)

**R Implementation**:
```r
library(pls)
model <- plsr(activity ~ ., ncomp = 5, data = dataset, validation = "CV")
summary(model)
VIP(model)  # Variable Importance in Projection
```

#### 3.3 Principal Component Regression (PCR)

Combines PCA with regression:

```
Step 1: X â?PC scores (T) via PCA
Step 2: Y = TÎ² + Îµ (regression on scores)
```

#### 3.4 Machine Learning Methods

| Method | Advantages | Use Cases |
|--------|------------|-----------|
| Random Forest | Non-linear, handles mixed data | Large datasets, feature importance |
| Support Vector Machine (SVM) | High-dimensional spaces | Classification QSAR |
| Neural Networks (ANN) | Complex non-linear relationships | Large training sets |
| k-Nearest Neighbors (kNN) | Simple, interpretable | Similarity-based prediction |

### 4. Model Validation

#### 4.1 OECD Validation Principles

For regulatory acceptance, QSAR models must fulfill 5 principles:

1. **Defined Endpoint**: Specific biological activity/property measured
2. **Unambiguous Algorithm**: Mathematical model clearly documented
3. **Defined Applicability Domain**: Structural/property space for reliable predictions
4. **Appropriate Measures of Goodness-of-Fit**: Statistical validation metrics
5. **Mechanistic Interpretation**: Chemical plausibility of descriptors

#### 4.2 Internal Validation

**Cross-Validation Methods**:

| Method | Description | Use Case |
|--------|-------------|----------|
| Leave-One-Out (LOO) | N models, each excluding one compound | Small datasets |
| Leave-Many-Out (LMO) | k-fold, typically 5- or 10-fold | Standard validation |
| Bootstrapping | Random sampling with replacement | Uncertainty estimation |

**Key Metrics**:
```
QÂ²_cv = 1 - Î£(y_i - Å·_i)Â² / Î£(y_i - È³)Â²
QÂ² > 0.5 = acceptable, QÂ² > 0.7 = good
```

**Y-Randomization (Y-Scrambling)**:
- Shuffle response variable randomly
- Rebuild model with scrambled data
- Compare QÂ² to original
- If scrambled QÂ² â?original â?chance correlation

```
cRÂ²p = R Ã â?RÂ² - RÂ²_random)
cRÂ²p > 0.5 indicates non-random model
```

#### 4.3 External Validation

**Test Set Approach**:
```
QÂ²_ext = 1 - Î£(y_test - Å·_test)Â² / Î£(y_test - È³_train)Â²
RÂ²_ext > 0.6, QÂ²_ext > 0.5 for acceptable external predictivity
```

**RMSE and MAE**:
```
RMSE = â[Î£(y_i - Å·_i)Â² / n]
MAE = Î£|y_i - Å·_i| / n
```

### 5. Applicability Domain (AD)

Defines the chemical space where model predictions are reliable.

#### 5.1 Range-Based Methods

**Bounding Box**: Simple descriptor ranges
```
AD: min(X_j) â?x_j â?max(X_j) for all descriptors j
```
*Drawback*: Ignores correlations between descriptors

**PCA Bounding Box**: Use principal component ranges
- Accounts for descriptor correlations
- Still includes empty regions

#### 5.2 Distance-Based Methods

**Leverage (Williams Plot)**:
```
h_i = x_i(X'X)â»Â¹x_i'
Warning leverage: h* = 3(p+1)/n

where p = number of descriptors, n = number of compounds
```
- Compounds with h > h* are outside AD
- Plot leverage vs standardized residuals

**Mahalanobis Distance**:
```
DÂ²_M = (x - Î¼)'Sâ»Â?x - Î¼)
```
- Accounts for covariance between descriptors
- Large DÂ²_M indicates outside AD

#### 5.3 Similarity-Based Methods

**k-Nearest Neighbors**:
```
AD: distance to k nearest training compounds < threshold
```

**Tanimoto Similarity** (for fingerprints):
```
T(A,B) = c / (a + b - c)
where a = bits in A, b = bits in B, c = common bits
T > 0.7 indicates similar compounds
```

### 6. Lipinski's Rule of Five

Quick filter for drug-likeness (oral bioavailability prediction):

| Rule | Threshold | Rationale |
|------|-----------|-----------|
| MW | â?500 Da | Membrane permeability |
| logP | â?5 | Lipophilicity balance |
| HBD | â?5 | Hydrogen bond donors (OH, NH) |
| HBA | â?10 | Hydrogen bond acceptors (O, N) |

**Interpretation**:
- â?1 violation: Good drug candidate
- 2 violations: Possible issues
- > 2 violations: Poor oral bioavailability likely

**Extensions**:
- **Veber's Rules**: Rotatable bonds â?10, PSA â?140 ÃÂ²
- **Pfizer 3/75 Rule**: clogP < 3, TPSA > 75 for reduced toxicity

**Python Implementation (RDKit)**:
```python
from rdkit import Chem
from rdkit.Chem import Descriptors, Lipinski

mol = Chem.MolFromSmiles('CC(=O)Oc1ccccc1C(=O)O')  # Aspirin

mw = Descriptors.MolWt(mol)           # Molecular weight
logp = Descriptors.MolLogP(mol)       # logP
hbd = Lipinski.NumHDonors(mol)        # H-bond donors
hba = Lipinski.NumHAcceptors(mol)     # H-bond acceptors
rot_bonds = Lipinski.NumRotatableBonds(mol)
psa = Descriptors.TPSA(mol)           # Polar surface area

# Check Rule of 5
violations = sum([mw > 500, logp > 5, hbd > 5, hba > 10])
print(f"Ro5 violations: {violations}")
```

---

## QSAR Workflow

```
âââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ?â?                     QSAR MODELING WORKFLOW                         â?âââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ?â?                                                                    â?â? 1. DATA PREPARATION                                                â?â?    âââ Collect compounds with known activity                      â?â?    âââ Curate structures (canonical SMILES, standardization)      â?â?    âââ Split: Training (70-80%) / Test (20-30%)                   â?â?    âââ Activity: IC50, EC50, Ki (convert to pIC50 = -log[IC50])   â?â?                        â?                                          â?â?                        â?                                          â?â? 2. DESCRIPTOR CALCULATION                                          â?â?    âââ 2D descriptors (topological, electronic)                   â?â?    âââ 3D descriptors (requires 3D structure optimization)        â?â?    âââ Descriptor selection (remove constant, highly correlated)  â?â?    âââ Software: RDKit, PaDEL, Dragon, MOE                        â?â?                        â?                                          â?â?                        â?                                          â?â? 3. MODEL BUILDING                                                  â?â?    âââ MLR (small datasets, few descriptors)                      â?â?    âââ PLS (many descriptors, collinear)                          â?â?    âââ ML methods (large datasets, non-linear)                    â?â?    âââ Variable selection (stepwise, GA, LASSO)                   â?â?                        â?                                          â?â?                        â?                                          â?â? 4. VALIDATION                                                      â?â?    âââ Internal: Cross-validation (LOO, 10-fold)                  â?â?    âââ Y-randomization (check chance correlation)                 â?â?    âââ External: Test set prediction                              â?â?    âââ Metrics: RÂ², QÂ², RMSE, MAE                                 â?â?                        â?                                          â?â?                        â?                                          â?â? 5. APPLICABILITY DOMAIN                                            â?â?    âââ Define AD (leverage, distance-based)                       â?â?    âââ Identify outliers (Williams plot)                          â?â?    âââ Report predictions with confidence                         â?â?                        â?                                          â?â?                        â?                                          â?â? 6. INTERPRETATION & APPLICATION                                    â?â?    âââ Mechanistic interpretation of key descriptors              â?â?    âââ Predict new compounds                                      â?â?    âââ Guide lead optimization                                    â?â?    âââ Document following OECD principles                         â?â?                                                                    â?âââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ?```

---

## Software Tools

### Open Source

| Tool | Language | Key Features |
|------|----------|--------------|
| **RDKit** | Python/C++ | Descriptor calculation, 2D/3D, fingerprints |
| **PaDEL-Descriptor** | Java | 1875 descriptors, free |
| **ALVAdesc** | Python | >5000 descriptors |
| **scikit-learn** | Python | ML models, validation |
| **Orange** | Python | GUI-based QSAR workflow |

### Commercial

| Tool | Features |
|------|----------|
| **MOE (Molecular Operating Environment)** | 3D-QSAR, CoMFA, extensive descriptors |
| **Dragon** | 5000+ descriptors, widely cited |
| **SYBYL-X** | CoMFA/CoMSIA 3D-QSAR |
| **SchrÃ¶dinger** | Phase QSAR, pharmacophore modeling |

### Descriptor Calculation Example (RDKit)

```python
from rdkit import Chem
from rdkit.Chem import Descriptors
import pandas as pd

smiles_list = ['CCO', 'CC(C)O', 'c1ccccc1']  # ethanol, isopropanol, benzene
descriptors = []

for smi in smiles_list:
    mol = Chem.MolFromSmiles(smi)
    desc = {
        'SMILES': smi,
        'MW': Descriptors.MolWt(mol),
        'LogP': Descriptors.MolLogP(mol),
        'TPSA': Descriptors.TPSA(mol),
        'HBD': Descriptors.NumHDonors(mol),
        'HBA': Descriptors.NumHAcceptors(mol),
        'RotBonds': Descriptors.NumRotatableBonds(mol),
        'AromaticRings': Descriptors.NumAromaticRings(mol),
        'HeavyAtoms': Descriptors.HeavyAtomCount(mol),
    }
    descriptors.append(desc)

df = pd.DataFrame(descriptors)
print(df)
```

---

## Validation Example (R)

```r
# QSAR Validation Workflow in R
library(caret)
library(pls)

# Split data
set.seed(123)
train_idx <- createDataPartition(dataset$activity, p = 0.8, list = FALSE)
train <- dataset[train_idx, ]
test <- dataset[-train_idx, ]

# Build PLS model with cross-validation
model <- plsr(activity ~ ., data = train, 
              ncomp = 10, validation = "CV", segments = 10)

# Optimal number of components
ncomp_opt <- which.min(RMSEP(model)$val[1, , ]) - 1

# Internal validation metrics
Q2_cv <- max(model$validation$adj)
R2_train <- max(R2(model)$val[1, , ])

# External validation
pred_test <- predict(model, newdata = test, ncomp = ncomp_opt)
R2_test <- cor(test$activity, pred_test)^2
RMSE_test <- sqrt(mean((test$activity - pred_test)^2))

# Y-randomization test
n_perm <- 100
Q2_random <- numeric(n_perm)
for (i in 1:n_perm) {
  train_scrambled <- train
  train_scrambled$activity <- sample(train$activity)
  model_rand <- plsr(activity ~ ., data = train_scrambled, 
                     ncomp = ncomp_opt, validation = "CV")
  Q2_random[i] <- max(model_rand$validation$adj)
}
p_random <- mean(Q2_random >= Q2_cv)  # Should be < 0.05

# Leverage-based AD
X <- as.matrix(train[, -which(names(train) == "activity")])
H <- X %*% solve(t(X) %*% X) %*% t(X)
h_star <- 3 * (ncol(X) + 1) / nrow(X)
```

---

## Decision Trees

### Choosing Model Type

```
ââ Number of descriptors vs compounds? ââââââââââââââââââââââââââââââ?â?                                                                  â?â? ââ Fewer descriptors than compounds (p < n)                      â?â? â?  âââ Descriptors uncorrelated?                                â?â? â?  â?  âââ YES â?MLR                                            â?â? â?  â?  âââ NO â?PLS or Ridge Regression                         â?â? â?  âââ Non-linear relationships?                                â?â? â?      âââ YES â?Random Forest or SVR                           â?â? â?      âââ NO â?PLS                                             â?â? â?                                                               â?â? ââ More descriptors than compounds (p > n)                       â?â?     âââ Need interpretability? â?PLS                             â?â?     âââ Best prediction only? â?LASSO or Random Forest           â?â?                                                                  â?âââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ?```

### Choosing Validation Method

```
ââ Dataset Size? ââââââââââââââââââââââââââââââââââââââââââââââââââââ?â?                                                                  â?â? ââ Small (n < 50)                                                â?â? â?  âââ LOO cross-validation + external test set                 â?â? â?                                                               â?â? ââ Medium to Large (n â?50)                                      â?â?     âââ 10-fold cross-validation                                 â?â?     âââ External test set (20-30%)                               â?â?     âââ Y-randomization (â?100 permutations)                     â?â?                                                                  â?â? Regulatory submission? â?Full OECD compliance + external set    â?â?                                                                  â?âââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ?```

---

## Related Concepts

- [[../L2_principles/multivariate_regression.md]] - PLS, PCR methods
- [[../L2_principles/calibration_curves.md]] - Linear regression foundations
- [[../L2_principles/chemometrics_principal_component_analysis.md]] - PCA for descriptor reduction
- [[../L2_principles/chemometrics_cluster_analysis.md]] - Compound clustering
- [[../L2_principles/organic_functional_groups.md]] - Structure-based classification
- [[../L2_principles/organic_chemistry.md]] - Functional group effects on activity

---

## References

1. LibreTexts: Quantitative Structure-Activity Relationships (Bruice Ch31.9)
2. OECD Guidance Document on Validation of QSAR Models (2007)
3. Tropsha A. Best Practices in QSAR Model Development (2010)
4. Cherkasov A. et al. QSAR Modeling: Where Have You Been? (2014)
5. Lipinski CA et al. Experimental and computational approaches to estimate solubility and permeability (1997)


## Implementations

- Implementation: `../L3_functions/qsar_tools.py`

## L3 Tool Call Directives

**Source:** qsar_tools.py
Quantitative Structure-Activity Relationships: drug-likeness, similarity, AD, validation.

### Available functions:
- lipinski_rule_of_five(properties: Dict[str, float]) �� Tuple[int, List[str]] �� Violation count and list; keys: mw/logp/hbd/hba
- 	animoto_similarity(fp1: Set, fp2: Set) �� float �� Coefficient 0-1; empty both sets �� 1.0
- pplicability_domain(X_train: np.ndarray, X_test: np.ndarray, threshold: float=3.0) �� Tuple[ndarray, ndarray] �� Leverage values and AD status
- if(X: np.ndarray, feature_names: List[str]=None) �� Dict[str, float] �� VIF per feature; >5 problematic, >10 severe
- mse(y_true: np.ndarray, y_pred: np.ndarray) �� float �� Root Mean Square Error
- mae(y_true: np.ndarray, y_pred: np.ndarray) �� float �� Mean Absolute Error
- _squared(y_true: np.ndarray, y_pred: np.ndarray) �� float �� R2 coefficient of determination
- q2_loo(y_true: np.ndarray, y_pred_loo: np.ndarray) �� float �� Q2 for leave-one-out CV

### Common errors:
- ? Passing raw molecular data instead of fingerprint sets to tanimoto_similarity
- ? Forgetting Q2 should be >0.5 for a reliable QSAR model
