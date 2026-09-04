# Advanced NMR: Two-Dimensional Techniques

## Concept Overview
2D NMR correlates two NMR frequency dimensions, revealing through-bond or through-space connectivity between nuclei.

## Key 2D NMR Experiments

| Experiment | Correlation | Information | Typical Use |
|---|---|---|---|
| COSY | ¹H-¹H (J-coupled) | Scalar coupling network | Identify spin systems |
| TOCSY | ¹H-¹H (all in spin system) | Complete coupling network | Sugar residues, amino acids |
| HSQC | ¹H-¹³C (¹J_CH) | Direct H-C bonds | Carbon-proton connectivity |
| HMBC | ¹H-¹³C (nJ_CH, n=2,3) | Long-range H-C coupling | Quaternary carbons, connectivity |
| NOESY | ¹H-¹H (NOE) | Through-space (<5 Å) | 3D structure, stereochemistry |
| ROESY | ¹H-¹H (ROE) | Through-space (small molecules) | When NOE is weak/near zero |

## Pulse Sequence Concepts
- **Evolution time (t₁)**: First frequency dimension encoded during variable delay.
- **Detection time (t₂)**: Second dimension acquired during FID.
- **2D Fourier transform**: Sequential FT over t₂, then t₁ → frequency-frequency correlation map.

## Key Parameters
- **Spectral width (SW)**: Must cover full chemical shift range in both dimensions.
- **Number of increments (N₁)**: Resolution in F1 dimension; total time = N₁ × NS × recycle delay.
- **Mixing time (τ_m)**: For NOESY/TOCSY; determines cross-peak intensity.

## Applications
- **Natural product structure elucidation**: COSY + HSQC + HMBC + NOESY workflow.
- **Protein NMR**: ¹⁵N/¹³C-labeled samples; 3D/4D experiments (HNCA, HNCO, etc.).
- **Metabolomics**: 2D HSQC-TOCSY for metabolite identification.

## Sources
[Source: Wikipedia, Two-dimensional nuclear magnetic resonance]
[Source: NMR spectroscopy textbooks]

## L3 Tools
-> `../L3_functions/nmr_tools.py` — `cosy_analysis()`, `hmqc_correlation()`

## L3 Tool Call Directives

**Source:** `nmr_tools.py`
NMR unit conversion, multiplicity prediction (n+1 rule), coupling constants.

### Available functions:
- `chemical_shift_to_freq(delta_ppm, freq_mhz)` → float — Convert ppm to Hz offset (Hz = ppm × MHz)
- `coupling_constant(j_hz)` → float — Absolute J coupling value in Hz
- `multiplicity(n_neighbors)` → str — Signal multiplicity: singlet(0), doublet(1), triplet(2), quartet(3), quintet(4), {n+1}-let

### Common errors:
- ❌ Forgetting to specify spectrometer frequency — chemical shift in Hz depends on MHz
- ❌ Using negative J values — always report coupling constants as positive
- ❌ Applying n+1 rule to non-equivalent neighbors — only works for equivalent sets

**Source:** nmr_splitting_tools.py
L3 Tool: NMR Splitting Tools

### Available functions:
- splitting_pattern(n_neighbors) → dict — Return multiplet name and intensity ratios for given neighbors.
- multiplet_name(n_peaks) → str — Return multiplet name from number of peaks.
- intensity_ratios(n_neighbors) → list — Calculate intensity ratios using n + 1 rule (Pascal's triangle).
- predict_spectrum_group(protons, neighbors) → dict — Predict NMR signal for a group of equivalent protons.
- spectrum_group(protons, neighbors) → dict — Alias for predict_spectrum_group - for solver compatibility.
- neighbors_from_multiplet(multiplet) → int — Calculate number of neighboring protons from multiplet name.
- coupling_relationship(j_values) → list — Identify coupled proton groups from coupling constants.

### Common errors:
- ❌ Passing wrong parameter types or missing required arguments
