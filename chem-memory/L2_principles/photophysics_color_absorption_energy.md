# Photophysics: Photon Energy, Wavelength, And Absorbed Color

Use this note when a chemistry question connects dye color, conjugated pi systems,
emitted photon energy, absorbed light, or visible wavelength.

## Energy To Wavelength

- Photon energy and wavelength are related by `E = h c / lambda`.
- A convenient visible-light conversion is:
  - `lambda_nm = 1240 / E_eV`
  - `E_eV = 1240 / lambda_nm`
- Approximate visible bands:
  - violet: 380-450 nm
  - blue: 450-495 nm
  - green: 495-570 nm
  - yellow: 570-590 nm
  - orange: 590-620 nm
  - red: 620-750 nm

## Emitted Versus Absorbed Color

- Fluorescence or emission color is the color of the emitted photon.
- For a nonfluorescent sample under broad illumination, transmitted or reflected
  color can approximately complement selectively absorbed light. This depends on
  the illumination and spectrum, not just a single wavelength.
- Fluorescence is a different process: emission and absorption bands are separated
  by a Stokes shift. An emission wavelength alone does not determine an absorption
  wavelength or complementary absorbed color.
- Approximate complementary pairs:
  - green transmitted color can accompany red or magenta absorption.
  - blue corresponds to orange.
  - violet corresponds to yellow-green.
  - red corresponds to cyan or blue-green.

## Guards

- Keep direction clear: "emits" identifies the emitted photon. Require an absorption
  spectrum, transition information, or an explicitly imposed color convention to
  infer absorption from emission; do not invent the missing spectrum.
- If the prompt asks for a color option rather than a numeric wavelength, compute
  or estimate wavelength first, map it to a visible band, then apply the stated
  emitted/absorbed relation.
- Do not infer a hidden spectrum, solvent shift, or exact color boundary unless
  the problem provides those data.

## Reference

[IUPAC Gold Book: Stokes shift](https://goldbook.iupac.org/terms/view/S06031).
Ordinary fluorescence usually has longer-wavelength emission than absorption;
this trend is not an exact inversion rule and anti-Stokes processes exist.
