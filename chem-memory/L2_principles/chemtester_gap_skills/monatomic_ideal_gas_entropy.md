# Monatomic ideal-gas absolute molar entropy

**Retrieve with:** Sackur Tetrode molar entropy, monatomic ideal gas absolute entropy

**Use when:** A monatomic ideal gas absolute entropy is requested from temperature, pressure or volume, and particle or molar mass.

## Procedure

1. Convert mass to the per-particle quantity required by the translational partition expression and keep SI units throughout.
2. Use the volume-per-particle or equivalent pressure form consistently, including the additive five-halves term.
3. Convert the per-particle entropy to molar entropy and report joules per mole-kelvin.

## Preferred Support

- L2_principles/statistical_thermodynamics.md
- L2_principles/statistical_mechanics.md

## Guards

- Do not insert molar mass directly where single-particle mass is required.
- Do not omit Planck-constant powers or mix pressure and volume forms.
