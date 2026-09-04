"""
Analytical Method Validation Tools (L3 Implementation)

Provides functions for LOD/LOQ calculation, precision analysis,
factorial experimental design, ANOVA, and method validation checklists.

Part of the Chemistry Memory System.
"""
## Solver Instructions (for AI Agent)

# When you encounter analytical method validation problems (LOD, LOQ, precision, ANOVA), follow this decision tree:

### Step 1: Identify what is given and what is asked
# - **Given**: calibration data (concentrations, signals), replicate measurements, group data, method type
# - **Asked**: LOD, LOQ, precision (RSD), significant differences, validation checklist

### Step 2: Choose the correct function
# | Task | Function | Key Parameters |
# |---|---|---|
# | LOD/LOQ (calibration) | `lod_loq_calculation(concentrations, signals, method='calibration')` | calibration arrays |
# | LOD/LOQ (S/N) | `lod_loq_calculation(concentrations, signals, method='signal_noise', signal_noise_ratio=)` | S/N ratio |
# | LOD/LOQ (blank) | `lod_loq_calculation(concentrations, signals, method='blank', blank_signals=)` | blank data |
# | Precision (CV%) | `precision_analysis(measurements, groups)` | data array, optional day groups |
# | Factorial design | `factorial_design(response, factors, levels)` | Y, factor matrices |
# | One-way ANOVA | `anova_analysis(groups_data, alpha)` | dict of group arrays |
# | Validation checklist | `method_validation_checklist(validation_type, results)` | 'assay'/'impurity'/etc |
# | Confidence interval | `calculate_confidence_interval(data, confidence)` | data array |
# | Horwitz RSD | `horwitz_equation(concentration)` | decimal fraction |

### Step 3: Handle special cases
# - Use `'calibration'` method for LOD/LOQ by default (ICH guidelines)
# - For intermediate precision, pass day/analyst groups to `precision_analysis`
# - `method_validation_checklist` generates ICH Q2(R1) criteria automatically

### Examples
# 1. **LOD/LOQ**: `lod_loq_calculation(np.array([0.5,1,2,5,10]), np.array([0.12,0.25,0.51,1.28,2.55]))` -> LOD~0.17, LOQ~0.51
# 2. **ANOVA**: `anova_analysis({'A': np.array([98.1,98.5]), 'B': np.array([99.2,99.0])})` -> F and p-value
# 3. **Horwitz**: `horwitz_equation(0.01)` -> ~5.7% RSD predicted for 1% concentration


import numpy as np
from typing import Dict, List, Tuple, Optional, Union
from dataclasses import dataclass
from enum import Enum


# =============================================================================
# LOD/LOQ CALCULATION
# =============================================================================

@dataclass
class LODLOQResult:
    """Results from LOD/LOQ calculation."""
    lod: float  # Limit of Detection
    loq: float  # Limit of Quantitation
    method: str  # Calculation method used
    slope: Optional[float] = None
    intercept: Optional[float] = None
    residual_std: Optional[float] = None
    signal_noise_ratio: Optional[float] = None


def lod_loq_calculation(
    concentrations: np.ndarray,
    signals: np.ndarray,
    method: str = "calibration",
    signal_noise_ratio: Optional[float] = None,
    blank_signals: Optional[np.ndarray] = None
) -> LODLOQResult:
    """
    Calculate Limit of Detection (LOD) and Limit of Quantitation (LOQ).
    
    Methods:
    --------
    1. Calibration curve method (default):
       LOD = 3.3 x (σ / S)
       LOQ = 10 x (σ / S)
       where σ = residual standard deviation, S = slope
       
    2. Signal-to-noise method:
       LOD = concentration giving S/N = 3
       LOQ = concentration giving S/N = 10
       
    3. Blank method:
       LOD = mean_blank + 3xSD_blank
       LOQ = mean_blank + 10xSD_blank
    
    Parameters
    ----------
    concentrations : np.ndarray
        Concentration values from calibration curve
    signals : np.ndarray
        Corresponding signal (response) values
    method : str
        One of: "calibration", "signal_noise", "blank"
    signal_noise_ratio : float, optional
        Current S/N ratio (for signal_noise method)
    blank_signals : np.ndarray, optional
        Blank sample signals (for blank method)
    
    Returns
    -------
    LODLOQResult
        Dataclass containing LOD, LOQ, and calculation details
    
    Examples
    --------
    >>> conc = np.array([0.1, 0.5, 1.0, 2.0, 5.0])
    >>> signals = np.array([0.05, 0.25, 0.52, 1.05, 2.60])
    >>> result = lod_loq_calculation(conc, signals)
    >>> print(f"LOD = {result.lod:.4f}, LOQ = {result.loq:.4f}")
    """
    
    if method == "calibration":
        # Linear regression
        n = len(concentrations)
        x_mean = np.mean(concentrations)
        y_mean = np.mean(signals)
        
        # Calculate slope (S) and intercept
        numerator = np.sum((concentrations - x_mean) * (signals - y_mean))
        denominator = np.sum((concentrations - x_mean) ** 2)
        slope = numerator / denominator
        intercept = y_mean - slope * x_mean
        
        # Calculate residuals and standard deviation
        y_pred = slope * concentrations + intercept
        residuals = signals - y_pred
        residual_std = np.sqrt(np.sum(residuals ** 2) / (n - 2))
        
        # LOD and LOQ from ICH guidelines
        lod = 3.3 * (residual_std / slope)
        loq = 10 * (residual_std / slope)
        
        return LODLOQResult(
            lod=lod,
            loq=loq,
            method="calibration",
            slope=slope,
            intercept=intercept,
            residual_std=residual_std
        )
    
    elif method == "signal_noise":
        if signal_noise_ratio is None:
            raise ValueError("signal_noise_ratio required for signal_noise method")
        
        # Estimate from current concentration
        # LOD at S/N = 3, LOQ at S/N = 10
        # Conc x (S/N)_current / target_S/N
        current_conc = concentrations[-1]  # Assume last point
        
        lod = current_conc * 3 / signal_noise_ratio
        loq = current_conc * 10 / signal_noise_ratio
        
        return LODLOQResult(
            lod=lod,
            loq=loq,
            method="signal_noise",
            signal_noise_ratio=signal_noise_ratio
        )
    
    elif method == "blank":
        if blank_signals is None:
            raise ValueError("blank_signals required for blank method")
        
        mean_blank = np.mean(blank_signals)
        std_blank = np.std(blank_signals, ddof=1)
        
        # Need calibration to convert signal to concentration
        slope, intercept = np.polyfit(concentrations, signals, 1)
        
        lod_signal = mean_blank + 3 * std_blank
        loq_signal = mean_blank + 10 * std_blank
        
        # Convert to concentration
        lod = (lod_signal - intercept) / slope
        loq = (loq_signal - intercept) / slope
        
        return LODLOQResult(
            lod=lod,
            loq=loq,
            method="blank",
            slope=slope,
            intercept=intercept
        )
    
    else:
        raise ValueError(f"Unknown method: {method}. Use 'calibration', 'signal_noise', or 'blank'")


# =============================================================================
# PRECISION ANALYSIS
# =============================================================================

@dataclass
class PrecisionResult:
    """Results from precision analysis."""
    repeatability: float  # Intra-day CV%
    intermediate_precision: float  # Inter-day CV%
    reproducibility: Optional[float]  # Inter-lab CV%
    mean: float
    std: float
    n_total: int


def precision_analysis(
    measurements: np.ndarray,
    groups: Optional[np.ndarray] = None,
    alpha: float = 0.05
) -> PrecisionResult:
    """
    Analyze precision of analytical method.
    
    Calculates:
    - Repeatability (intra-day precision): CV% within same conditions
    - Intermediate precision: CV% across different days/analysts
    - Reproducibility: CV% across laboratories
    
    Formulas:
    ---------
    CV% = (SD / Mean) x 100
    
    Repeatability: CV within each group
    Intermediate precision: CV across all measurements
    
    Parameters
    ----------
    measurements : np.ndarray
        Array of measurement values
    groups : np.ndarray, optional
        Group identifiers (e.g., day numbers for intermediate precision)
        If None, calculates only overall precision
    alpha : float
        Significance level for confidence intervals
    
    Returns
    -------
    PrecisionResult
        Dataclass containing precision metrics
    
    Examples
    --------
    >>> data = np.array([10.1, 10.2, 10.0, 10.3, 9.9])
    >>> result = precision_analysis(data)
    >>> print(f"Repeatability CV% = {result.repeatability:.2f}%")
    """
    
    n_total = len(measurements)
    mean = np.mean(measurements)
    std = np.std(measurements, ddof=1)
    
    # Overall CV (repeatability if no groups)
    overall_cv = (std / mean) * 100
    
    if groups is None:
        return PrecisionResult(
            repeatability=overall_cv,
            intermediate_precision=overall_cv,
            reproducibility=None,
            mean=mean,
            std=std,
            n_total=n_total
        )
    
    # Calculate within-group and between-group variances
    unique_groups = np.unique(groups)
    n_groups = len(unique_groups)
    
    # Within-group (repeatability)
    within_variances = []
    for g in unique_groups:
        group_data = measurements[groups == g]
        if len(group_data) > 1:
            within_variances.append(np.var(group_data, ddof=1))
    
    if within_variances:
        pooled_within_var = np.mean(within_variances)
        repeatability_cv = (np.sqrt(pooled_within_var) / mean) * 100
    else:
        repeatability_cv = overall_cv
    
    # Between-group (intermediate precision)
    # Total variance = within-group + between-group
    total_var = np.var(measurements, ddof=1)
    between_var = total_var - pooled_within_var if within_variances else 0
    between_var = max(0, between_var)  # Can't be negative
    
    intermediate_var = pooled_within_var + between_var if within_variances else total_var
    intermediate_cv = (np.sqrt(intermediate_var) / mean) * 100
    
    return PrecisionResult(
        repeatability=repeatability_cv,
        intermediate_precision=intermediate_cv,
        reproducibility=None,  # Requires multi-lab data
        mean=mean,
        std=std,
        n_total=n_total
    )


# =============================================================================
# FACTORIAL DESIGN
# =============================================================================

@dataclass
class FactorialResult:
    """Results from factorial experiment analysis."""
    main_effects: Dict[str, float]
    interactions: Dict[str, float]
    significant_factors: List[str]
    anova_table: Dict[str, Dict[str, float]]


def factorial_design(
    response: np.ndarray,
    factors: Dict[str, np.ndarray],
    levels: int = 2,
    alpha: float = 0.05
) -> FactorialResult:
    """
    Analyze factorial experimental design.
    
    Supports:
    - Full factorial designs (2^k, 3^k)
    - Main effects and interaction effects calculation
    - Identification of significant factors
    
    Formulas:
    ---------
    Main Effect A = (Σ Y at A_high - Σ Y at A_low) / (n x 2^(k-1))
    Interaction AB = (Σ Y at A_highxB_high + Σ Y at A_lowxB_low 
                     - Σ Y at A_highxB_low - Σ Y at A_lowxB_high) / (n x 2^(k-1))
    
    Parameters
    ----------
    response : np.ndarray
        Response values (Y)
    factors : Dict[str, np.ndarray]
        Factor levels (-1, +1 for 2-level; -1, 0, +1 for 3-level)
    levels : int
        Number of levels (2 or 3)
    alpha : float
        Significance level
    
    Returns
    -------
    FactorialResult
        Dataclass containing effects and significant factors
    
    Examples
    --------
    >>> # 2^2 factorial: Temperature and Time
    >>> response = np.array([85, 90, 88, 95])  # Yields
    >>> factors = {
    ...     'Temperature': np.array([-1, -1, 1, 1]),
    ...     'Time': np.array([-1, 1, -1, 1])
    ... }
    >>> result = factorial_design(response, factors)
    """
    
    factor_names = list(factors.keys())
    n_factors = len(factor_names)
    n_runs = len(response)
    
    # Calculate main effects
    main_effects = {}
    
    if levels == 2:
        # 2-level factorial
        for name in factor_names:
            factor_levels = factors[name]
            high_mean = np.mean(response[factor_levels == 1])
            low_mean = np.mean(response[factor_levels == -1])
            main_effects[name] = high_mean - low_mean
        
        # Calculate 2-way interactions
        interactions = {}
        for i in range(n_factors):
            for j in range(i + 1, n_factors):
                f1 = factor_names[i]
                f2 = factor_names[j]
                interaction_name = f"{f1}x{f2}"
                
                # Calculate interaction effect
                effect = 0
                for k in range(n_runs):
                    effect += response[k] * factors[f1][k] * factors[f2][k]
                interactions[interaction_name] = effect / (n_runs / 2)
    
    else:
        # 3-level factorial (simplified)
        for name in factor_names:
            factor_levels = factors[name]
            high_mean = np.mean(response[factor_levels == 1])
            low_mean = np.mean(response[factor_levels == -1])
            main_effects[name] = high_mean - low_mean
        interactions = {}
    
    # Simple significance test (compare to overall variability)
    overall_std = np.std(response, ddof=1)
    threshold = 2 * overall_std / np.sqrt(n_runs)  # Rough 95% CI
    
    significant_factors = [
        name for name, effect in main_effects.items()
        if abs(effect) > threshold
    ]
    
    # Build ANOVA-style table
    total_ss = np.sum((response - np.mean(response)) ** 2)
    
    anova_table = {}
    remaining_ss = total_ss
    
    for name, effect in main_effects.items():
        ss = (n_runs / 4) * (effect ** 2)
        ms = ss
        f_stat = (ms / (remaining_ss / (n_runs - 1 - len(main_effects)))) if remaining_ss > 0 else 0
        
        anova_table[name] = {
            'SS': ss,
            'df': 1,
            'MS': ms,
            'F': f_stat
        }
        remaining_ss -= ss
    
    anova_table['Error'] = {
        'SS': max(0, remaining_ss),
        'df': n_runs - 1 - len(main_effects),
        'MS': max(0, remaining_ss) / max(1, n_runs - 1 - len(main_effects)),
        'F': None
    }
    
    return FactorialResult(
        main_effects=main_effects,
        interactions=interactions,
        significant_factors=significant_factors,
        anova_table=anova_table
    )


# =============================================================================
# ANOVA ANALYSIS
# =============================================================================

@dataclass
class ANOVAResult:
    """Results from ANOVA analysis."""
    f_statistic: float
    p_value: float
    between_group_ss: float
    within_group_ss: float
    total_ss: float
    between_group_df: int
    within_group_df: int
    significant: bool
    groups_means: Dict[str, float]


def anova_analysis(
    groups_data: Dict[str, np.ndarray],
    alpha: float = 0.05
) -> ANOVAResult:
    """
    Perform one-way ANOVA analysis.
    
    Compares means across multiple groups to determine if there are
    statistically significant differences.
    
    Formulas:
    ---------
    SS_between = Σ n_i x (mean_i - grand_mean)2
    SS_within = Σ Σ (x_ij - mean_i)2
    F = MS_between / MS_within = (SS_between / df_between) / (SS_within / df_within)
    
    Parameters
    ----------
    groups_data : Dict[str, np.ndarray]
        Dictionary mapping group names to data arrays
    alpha : float
        Significance level (default 0.05)
    
    Returns
    -------
    ANOVAResult
        Dataclass containing ANOVA statistics
    
    Examples
    --------
    >>> groups = {
    ...     'Method_A': np.array([98.1, 98.5, 97.9]),
    ...     'Method_B': np.array([99.2, 99.0, 99.4]),
    ...     'Method_C': np.array([97.5, 97.8, 97.2])
    ... }
    >>> result = anova_analysis(groups)
    >>> print(f"F = {result.f_statistic:.3f}, p = {result.p_value:.4f}")
    """
    
    # Calculate group statistics
    group_names = list(groups_data.keys())
    k = len(group_names)  # Number of groups
    
    groups_means = {}
    group_sizes = {}
    group_vars = {}
    
    all_data = []
    
    for name, data in groups_data.items():
        groups_means[name] = np.mean(data)
        group_sizes[name] = len(data)
        group_vars[name] = np.var(data, ddof=1)
        all_data.extend(data)
    
    all_data = np.array(all_data)
    grand_mean = np.mean(all_data)
    n_total = len(all_data)
    
    # Calculate Sum of Squares
    # Between-group SS
    ss_between = sum(
        group_sizes[name] * (groups_means[name] - grand_mean) ** 2
        for name in group_names
    )
    
    # Within-group SS
    ss_within = sum(
        np.sum((groups_data[name] - groups_means[name]) ** 2)
        for name in group_names
    )
    
    # Total SS
    ss_total = ss_between + ss_within
    
    # Degrees of freedom
    df_between = k - 1
    df_within = n_total - k
    
    # Mean Squares
    ms_between = ss_between / df_between
    ms_within = ss_within / df_within
    
    # F-statistic
    f_stat = ms_between / ms_within if ms_within > 0 else float('inf')
    
    # P-value approximation using F-distribution
    # Using scipy.stats.f if available, otherwise approximation
    try:
        from scipy.stats import f
        p_value = 1 - f.cdf(f_stat, df_between, df_within)
    except ImportError:
        # Simple approximation for p-value
        p_value = _f_distribution_pvalue_approx(f_stat, df_between, df_within)
    
    significant = p_value < alpha
    
    return ANOVAResult(
        f_statistic=f_stat,
        p_value=p_value,
        between_group_ss=ss_between,
        within_group_ss=ss_within,
        total_ss=ss_total,
        between_group_df=df_between,
        within_group_df=df_within,
        significant=significant,
        groups_means=groups_means
    )


def _f_distribution_pvalue_approx(f_stat: float, df1: int, df2: int) -> float:
    """
    Approximate p-value for F-distribution (when scipy unavailable).
    
    Uses Wilson-Hilferty approximation.
    """
    if f_stat <= 0:
        return 1.0
    
    # Transform to approximately normal
    z = (2/9/df2 - 1) / np.sqrt(2/9/df2)
    z *= np.sqrt(df1 * f_stat)
    z -= (1 - 2/9/df1)
    z /= np.sqrt(2/9/df1)
    
    # Standard normal CDF approximation
    p = 0.5 * (1 + np.tanh(np.sqrt(2/np.pi) * (z + 0.044715 * z**3)))
    
    return 1 - p


# =============================================================================
# METHOD VALIDATION CHECKLIST
# =============================================================================

class ValidationParameter(Enum):
    """ICH Q2(R1) validation parameters."""
    SPECIFICITY = "Specificity"
    LINEARITY = "Linearity"
    RANGE = "Range"
    ACCURACY = "Accuracy"
    PRECISION = "Precision"
    LOD = "Limit of Detection"
    LOQ = "Limit of Quantitation"
    ROBUSTNESS = "Robustness"


@dataclass
class ValidationCheck:
    """Single validation check result."""
    parameter: str
    acceptance_criteria: str
    result: str
    passed: bool
    notes: str


def method_validation_checklist(
    validation_type: str = "assay",
    results: Optional[Dict[str, Union[float, str, bool]]] = None
) -> Dict[str, ValidationCheck]:
    """
    Generate method validation checklist per ICH Q2(R1) guidelines.
    
    Provides standard acceptance criteria for different method types:
    - Assay: Quantitative analysis of major components
    - Impurity: Related substances determination
    - Dissolution: Drug release testing
    - Identification: Qualitative methods
    
    Parameters
    ----------
    validation_type : str
        Type of method: "assay", "impurity", "dissolution", "identification"
    results : Dict, optional
        Pre-filled results for each parameter
    
    Returns
    -------
    Dict[str, ValidationCheck]
        Validation checklist with ICH-aligned acceptance criteria
    
    Examples
    --------
    >>> checklist = method_validation_checklist("assay")
    >>> for param, check in checklist.items():
    ...     print(f"{param}: {check.acceptance_criteria}")
    """
    
    # ICH Q2(R1) standard criteria by method type
    criteria = {
        "assay": {
            "Specificity": {
                "criteria": "No interference from excipients, degradation products",
                "threshold": "Peak purity ≥ 0.999, resolution ≥ 1.5"
            },
            "Linearity": {
                "criteria": "Correlation coefficient ≥ 0.999",
                "range": "80-120% of target concentration"
            },
            "Range": {
                "criteria": "80-120% of test concentration for assay",
                "justification": "Covers specification limits"
            },
            "Accuracy": {
                "criteria": "Recovery 98.0-102.0%",
                "n_levels": "3 (80, 100, 120%)"
            },
            "Precision - Repeatability": {
                "criteria": "RSD ≤ 2.0%",
                "n_replicates": "≥ 6 determinations"
            },
            "Precision - Intermediate": {
                "criteria": "RSD ≤ 3.0%",
                "conditions": "Different days, analysts, equipment"
            },
            "LOD": {
                "criteria": "Not required for assay methods",
                "note": "May be required for impurity methods"
            },
            "LOQ": {
                "criteria": "Not required for assay methods",
                "note": "Determine if relevant to method"
            },
            "Robustness": {
                "criteria": "Method performs within specifications when parameters varied",
                "parameters": "pH ± 0.2, flow rate ± 10%, column temperature ± 5degC"
            }
        },
        "impurity": {
            "Specificity": {
                "criteria": "Resolution ≥ 1.5 between all peaks",
                "threshold": "Peak purity ≥ 0.99"
            },
            "Linearity": {
                "criteria": "r ≥ 0.99 from LOQ to 120% of specification",
                "range": "LOQ to 150% of target"
            },
            "Range": {
                "criteria": "LOQ to 120% of specification limit",
                "note": "May extend to 150% for stress studies"
            },
            "Accuracy": {
                "criteria": "Recovery 80-120% at LOQ, 90-110% at specification level",
                "n_levels": "3 levels minimum"
            },
            "Precision - Repeatability": {
                "criteria": "RSD ≤ 10.0% at LOQ, ≤ 5.0% at specification",
                "n_replicates": "≥ 6"
            },
            "Precision - Intermediate": {
                "criteria": "RSD ≤ 15.0% at LOQ, ≤ 8.0% at specification",
                "conditions": "Different days, analysts"
            },
            "LOD": {
                "criteria": "S/N ≥ 3:1, typically 0.05% of API",
                "formula": "LOD = 3.3σ/S"
            },
            "LOQ": {
                "criteria": "S/N ≥ 10:1, precision RSD ≤ 10%",
                "formula": "LOQ = 10σ/S"
            },
            "Robustness": {
                "criteria": "Resolution and peak symmetry maintained",
                "parameters": "Mobile phase, temperature, flow variations"
            }
        },
        "dissolution": {
            "Specificity": {
                "criteria": "No interference from dissolution medium",
                "threshold": "Placebo blank shows no peak"
            },
            "Linearity": {
                "criteria": "r ≥ 0.999 from 20-130% of label claim",
                "range": "Q value ± 30%"
            },
            "Range": {
                "criteria": "Below Q to 130% of label claim",
                "note": "Covers dissolution profile range"
            },
            "Accuracy": {
                "criteria": "Recovery 95-105%",
                "method": "Spiked placebo in medium"
            },
            "Precision - Repeatability": {
                "criteria": "RSD ≤ 5.0% at 30 min",
                "n_replicates": "6 vessels"
            },
            "Precision - Intermediate": {
                "criteria": "RSD ≤ 7.0%",
                "conditions": "Different days, analysts"
            },
            "LOD": {
                "criteria": "Not applicable",
                "note": "Working above Q value"
            },
            "LOQ": {
                "criteria": "Not applicable",
                "note": "Quantitative range validated"
            },
            "Robustness": {
                "criteria": "Profile similarity (f2 ≥ 50) with parameter changes",
                "parameters": "RPM ± 15%, temperature ± 2degC"
            }
        },
        "identification": {
            "Specificity": {
                "criteria": "Positive identification of target analyte",
                "threshold": "Match reference standard"
            },
            "Linearity": {
                "criteria": "Not applicable",
                "note": "Qualitative method"
            },
            "Range": {
                "criteria": "Not applicable",
                "note": "Qualitative method"
            },
            "Accuracy": {
                "criteria": "Not applicable",
                "note": "Qualitative method"
            },
            "Precision": {
                "criteria": "Reproducible identification across conditions",
                "n_tests": "≥ 6 positive/negative samples"
            },
            "LOD": {
                "criteria": "Minimum identifiable concentration",
                "note": "Confirm identity at working concentration"
            },
            "LOQ": {
                "criteria": "Not applicable",
                "note": "Qualitative method"
            },
            "Robustness": {
                "criteria": "Identification maintained with parameter variations",
                "note": "Varied conditions should not affect ID"
            }
        }
    }
    
    # Get criteria for specified type
    type_criteria = criteria.get(validation_type, criteria["assay"])
    
    # Build checklist
    checklist = {}
    
    for param, details in type_criteria.items():
        result = ""
        passed = None
        
        if results and param in results:
            result = str(results[param].get("result", ""))
            passed = results[param].get("passed", None)
        
        # Build acceptance criteria string
        criteria_str = details.get("criteria", "")
        if "threshold" in details:
            criteria_str += f"; {details['threshold']}"
        if "n_levels" in details:
            criteria_str += f"; n={details['n_levels']}"
        
        checklist[param] = ValidationCheck(
            parameter=param,
            acceptance_criteria=criteria_str,
            result=result,
            passed=passed if passed is not None else False,
            notes=details.get("note", "")
        )
    
    return checklist


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def calculate_confidence_interval(
    data: np.ndarray,
    confidence: float = 0.95
) -> Tuple[float, float]:
    """
    Calculate confidence interval for mean.
    
    Parameters
    ----------
    data : np.ndarray
        Sample data
    confidence : float
        Confidence level (default 0.95)
    
    Returns
    -------
    Tuple[float, float]
        (lower_bound, upper_bound)
    """
    n = len(data)
    mean = np.mean(data)
    se = np.std(data, ddof=1) / np.sqrt(n)
    
    # t-value approximation
    try:
        from scipy.stats import t
        t_val = t.ppf((1 + confidence) / 2, n - 1)
    except ImportError:
        # Approximate for large n
        t_val = 1.96 if confidence == 0.95 else 2.576 if confidence == 0.99 else 1.645
    
    return (mean - t_val * se, mean + t_val * se)


def horwitz_equation(concentration: float) -> float:
    """
    Calculate Horwitz predicted RSD for given concentration.
    
    Horwitz formula: %RSD_R = 2^((1-0.5logC))
    where C is concentration as decimal fraction (e.g., 1% = 0.01)
    
    Parameters
    ----------
    concentration : float
        Concentration as decimal fraction (e.g., 0.01 for 1%)
    
    Returns
    -------
    float
        Predicted %RSD
    """
    if concentration <= 0:
        return float('inf')
    
    return 2 ** (1 - 0.5 * np.log10(concentration))


if __name__ == "__main__":
    # Quick validation test
    print("=== LOD/LOQ Test ===")
    conc = np.array([0.5, 1.0, 2.0, 5.0, 10.0])
    signals = np.array([0.12, 0.25, 0.51, 1.28, 2.55])
    result = lod_loq_calculation(conc, signals)
    print(f"LOD = {result.lod:.4f}, LOQ = {result.loq:.4f}")
    
    print("\n=== Precision Test ===")
    data = np.array([99.1, 99.3, 98.9, 99.2, 99.0, 98.8])
    days = np.array([1, 1, 1, 2, 2, 2])
    prec = precision_analysis(data, days)
    print(f"Repeatability = {prec.repeatability:.2f}%, Intermediate = {prec.intermediate_precision:.2f}%")
    
    print("\n=== Factorial Design Test ===")
    response = np.array([85, 90, 88, 95])
    factors = {
        'Temperature': np.array([-1, -1, 1, 1]),
        'Time': np.array([-1, 1, -1, 1])
    }
    fact = factorial_design(response, factors)
    print(f"Main effects: {fact.main_effects}")
    print(f"Interactions: {fact.interactions}")
    
    print("\n=== ANOVA Test ===")
    groups = {
        'A': np.array([98.1, 98.5, 97.9]),
        'B': np.array([99.2, 99.0, 99.4]),
        'C': np.array([97.5, 97.8, 97.2])
    }
    anova = anova_analysis(groups)
    print(f"F = {anova.f_statistic:.3f}, p = {anova.p_value:.4f}")


# MCP Tool Declarations
MCP_TOOLS = [
    {
        "name": "anova_analysis",
        "description": "Perform one-way ANOVA analysis.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "groups_data": {
                    "type": "number",
                    "description": "Groups Data"
                },
                "alpha": {
                    "type": "number",
                    "description": "Alpha",
                    "default": 0.05
                }
            },
            "required": [
                "groups_data"
            ]
        }
    },
    {
        "name": "calculate_confidence_interval",
        "description": "Calculate confidence interval for mean.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "data": {
                    "type": "number",
                    "description": "Data"
                },
                "confidence": {
                    "type": "number",
                    "description": "Confidence",
                    "default": 0.95
                }
            },
            "required": [
                "data"
            ]
        }
    },
    {
        "name": "dataclass",
        "description": "Add dunder methods based on the fields defined in the class.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "cls": {
                    "type": "number",
                    "description": "Cls",
                    "default": None
                },
                "init": {
                    "type": "number",
                    "description": "Init",
                    "default": True
                },
                "repr": {
                    "type": "number",
                    "description": "Repr",
                    "default": True
                },
                "eq": {
                    "type": "number",
                    "description": "Eq",
                    "default": True
                },
                "order": {
                    "type": "number",
                    "description": "Order",
                    "default": False
                },
                "unsafe_hash": {
                    "type": "number",
                    "description": "Unsafe Hash",
                    "default": False
                },
                "frozen": {
                    "type": "number",
                    "description": "Frozen",
                    "default": False
                },
                "match_args": {
                    "type": "number",
                    "description": "Match Args",
                    "default": True
                },
                "kw_only": {
                    "type": "number",
                    "description": "Kw Only",
                    "default": False
                },
                "slots": {
                    "type": "number",
                    "description": "Slots",
                    "default": False
                },
                "weakref_slot": {
                    "type": "number",
                    "description": "Weakref Slot",
                    "default": False
                }
            },
            "required": []
        }
    },
    {
        "name": "factorial_design",
        "description": "Analyze factorial experimental design.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "response": {
                    "type": "number",
                    "description": "Response"
                },
                "factors": {
                    "type": "number",
                    "description": "Factors"
                },
                "levels": {
                    "type": "number",
                    "description": "Levels",
                    "default": 2
                },
                "alpha": {
                    "type": "number",
                    "description": "Alpha",
                    "default": 0.05
                }
            },
            "required": [
                "response",
                "factors"
            ]
        }
    },
    {
        "name": "horwitz_equation",
        "description": "Calculate Horwitz predicted RSD for given concentration.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "concentration": {
                    "type": "number",
                    "description": "Concentration"
                }
            },
            "required": [
                "concentration"
            ]
        }
    },
    {
        "name": "lod_loq_calculation",
        "description": "Calculate Limit of Detection (LOD) and Limit of Quantitation (LOQ).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "concentrations": {
                    "type": "number",
                    "description": "Concentrations"
                },
                "signals": {
                    "type": "number",
                    "description": "Signals"
                },
                "method": {
                    "type": "number",
                    "description": "Method",
                    "default": "calibration"
                },
                "signal_noise_ratio": {
                    "type": "number",
                    "description": "Signal Noise Ratio",
                    "default": None
                },
                "blank_signals": {
                    "type": "number",
                    "description": "Blank Signals",
                    "default": None
                }
            },
            "required": [
                "concentrations",
                "signals"
            ]
        }
    },
    {
        "name": "method_validation_checklist",
        "description": "Generate method validation checklist per ICH Q2(R1) guidelines.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "validation_type": {
                    "type": "number",
                    "description": "Validation Type",
                    "default": "assay"
                },
                "results": {
                    "type": "number",
                    "description": "Results",
                    "default": None
                }
            },
            "required": []
        }
    },
    {
        "name": "precision_analysis",
        "description": "Analyze precision of analytical method.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "measurements": {
                    "type": "number",
                    "description": "Measurements"
                },
                "groups": {
                    "type": "number",
                    "description": "Groups",
                    "default": None
                },
                "alpha": {
                    "type": "number",
                    "description": "Alpha",
                    "default": 0.05
                }
            },
            "required": [
                "measurements"
            ]
        }
    }
]