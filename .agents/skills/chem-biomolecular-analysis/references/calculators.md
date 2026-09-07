# Optional Calculators

These are selected existing implementations, not independently certified chemistry.
Read a function's complete description, units, domain, and return type before calling it.
Legacy embedded empirical tables are approximate unless independently source-checked for the claim.
Do not equate an implementation's self-reported validation with independent verification.

## Invocation

Resolve scripts relative to this skill folder, not the caller's working directory.
Use the available Python 3.10+ environment. No provider key, Codex SDK, MCP service, or ChemTester checkout is required.

```text
python <skill-folder>/scripts/calculate.py --list
python <skill-folder>/scripts/calculate.py --describe module.function
python <skill-folder>/scripts/calculate.py --call module.function --arguments-json '{"parameter": 1.0}'
```

Replace the placeholder with an ID and arguments from its description.
A JSON error and nonzero exit code mean no usable result. Never reinterpret an error as an answer.

## Optional Dependencies

`numpy`, `scikit-learn`, `scipy`.
Only the functions that import these packages require them. A `requirements.txt` records the package names; versions are not pinned or certified by this export.
Use an existing suitable environment or explain a missing dependency; do not silently install software.

## Function Index

Read `--describe` for full signatures and contracts; this index is not a substitute.

### chemometrics_tools

- `chemometrics_tools.biplot_data`: Prepare coordinates for a biplot.
- `chemometrics_tools.chromatography_resolution`: Calculate chromatographic resolution Rs = 2(tR2-tR1)/(w1+w2).
- `chemometrics_tools.cls_calibration`: Classical Least Squares calibration (Beer's law approach).
- `chemometrics_tools.cls_predict`: Predict concentrations from absorbance using CLS.
- `chemometrics_tools.confidence_interval`: Calculate confidence interval for the mean.
- `chemometrics_tools.cross_validate`: Cross-validation for component selection.
- `chemometrics_tools.descriptive_stats`: Calculate comprehensive descriptive statistics.
- `chemometrics_tools.hypothesis_test`: Perform common hypothesis tests.
- `chemometrics_tools.internal_standard`: Internal standard method.
- `chemometrics_tools.leverage`: Calculate leverage for samples in PCA/PLS model.
- `chemometrics_tools.linear_regression`: Simple linear regression y = mx + b.
- `chemometrics_tools.mean_center`: Mean-center data by subtracting column (or row) means.
- `chemometrics_tools.msc`: Multiplicative Scatter Correction (MSC).
- `chemometrics_tools.outlier_detection`: Detect outliers in PCA/PLS model.
- `chemometrics_tools.pca_fit`: Fit a PCA model to data.
- `chemometrics_tools.pca_transform`: Transform new data using fitted PCA model.
- `chemometrics_tools.pcr_fit`: Principal Component Regression.
- `chemometrics_tools.pcr_predict`: Predict using PCR model.
- `chemometrics_tools.plate_count`: Calculate number of theoretical plates N = 16*(tR/w)^2.
- `chemometrics_tools.plate_height`: Calculate plate height H = L/N.
- `chemometrics_tools.pls_fit`: Fit a PLS regression model.
- `chemometrics_tools.pls_predict`: Predict Y values from X using fitted PLS model.
- `chemometrics_tools.propagation_uncertainty`: Error propagation.
- `chemometrics_tools.propagation_uncertainty_expression`: Error propagation via partial derivatives.
- `chemometrics_tools.rmsec_rmsep`: Calculate calibration/prediction error metrics.
- `chemometrics_tools.rsd`: Relative standard deviation (RSD) = std/mean * 100 (%).
- `chemometrics_tools.scores_loadings`: Extract scores and loadings from PCA model.
- `chemometrics_tools.scree_plot_data`: Generate data for scree plot.
- `chemometrics_tools.single_point_standard_addition`: Single-point standard addition with multi-step dilution support.
- `chemometrics_tools.snv`: Standard Normal Variate (SNV) transformation.
- `chemometrics_tools.standard_addition`: Standard addition method to determine concentration.
- `chemometrics_tools.standardize`: Z-score standardization: center and scale to unit variance.
- `chemometrics_tools.t_test`: One-sample t-test comparing data mean to true_value.
- `chemometrics_tools.van_deemter`: Van Deemter equation: H = A + B/u + C*u.
- `chemometrics_tools.variance_explained`: Get variance explained by each principal component.

Private helpers and retired/test functions present in original module source are not advertised or callable through this interface.
