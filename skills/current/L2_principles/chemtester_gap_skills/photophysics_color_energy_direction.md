# Photophysics Color Energy Direction

**Retrieve with:** photon energy wavelength color, emitted absorbed complementary color, dye conjugated visible absorption

**Use when:** A question asks for emitted, observed, or absorbed visible color from photon energy, wavelength, or conjugated-dye wording.

## Procedure

1. Convert photon energy to wavelength, or use the given emitted or observed color only after identifying the requested direction.
2. If the prompt asks absorbed color after giving dye emission, choose the complementary absorbed band instead of repeating the emitted band.
3. When visible choices include colors with numeric wavelength labels, use the chemically requested color relation first and treat labels as secondary checks.

## Preferred Support

- L2_principles/photophysics_color_absorption_energy.md
- L3_functions/electromagnetic_energy_tools.py when a numeric photon conversion is useful

## Guards

- Keep emitted, observed, transmitted, and absorbed color directions distinct.
- Do not let a numeric value printed beside a choice override an explicit absorbed-versus-emitted relation.
