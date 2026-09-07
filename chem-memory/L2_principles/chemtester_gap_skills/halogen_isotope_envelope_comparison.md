# Quantitative halogen isotope-envelope comparison

**Retrieve with:** halogen isotope envelope, chlorine bromine isotope pattern, M+2 M+4 peak ratio, binomial isotope cluster

**Use when:** A mass-spectrum problem infers counts of chlorine, bromine, or other two-isotope atoms from reported M, M+2, M+4, or higher cluster intensities.

## Procedure

1. Identify which reported peak is normalized to 100 and express every observed intensity with that same denominator.
2. For each candidate composition, form the isotope generating polynomial; for chlorine and bromine use (p_light+p_heavy*x) raised to each atom count, where the coefficient of x^k represents M+2k.
3. Use supplied or tabulated natural-abundance fractions when candidates are close, expand the polynomial, and normalize its coefficients to the stated reference peak.
4. Compare all reported peaks quantitatively, rank candidates by residual error, and inspect the predicted cluster length and terminal peaks without treating unreported peaks as absent.
5. If alternatives remain within the measurement precision, report the ambiguity; otherwise select only after the numerical comparison.

## Preferred Support

- chem-memory/L4_reference/spectroscopy_tables.md
- chem-memory/L2_principles/atomic_mass_spectrometry.md

## Guards

- Do not sum heavy-isotope percentages across multiple atoms; use binomial or multinomial coefficients.
- Do not compare percentages normalized to different peaks.
- Do not let rounded 3:1 or 1:1 mnemonics decide a near tie when abundance-based calculation is available.
- Do not assume an unreported M, M+6, or terminal peak is absent.
