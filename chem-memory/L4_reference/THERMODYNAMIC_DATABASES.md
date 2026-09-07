# Thermodynamic Data Reference (L4)

## Key Databases

### 1. NIST Chemistry WebBook
- **URL**: https://webbook.nist.gov/chemistry/
- **Content**: ΔHf°, ΔGf°, S°, Cp, heat of vaporization, ionization energy
- **Access**: Free, searchable by formula or name
- **Coverage**: ~70,000 compounds

### 2. NIST-JANAF Thermochemical Tables
- **URL**: https://janaf.nist.gov/
- **Content**: Temperature-dependent thermochemical data (ΔHf°, ΔGf°, log Kf, Cp, S, H, G)
- **Access**: Free, downloadable PDF
- **Coverage**: 48 elements and many compounds

### 3. Wikipedia Standard Thermodynamic Properties
- **URL**: https://en.wikipedia.org/wiki/Standard_thermodynamic_properties_of_chemical_substances
- **Content**: ΔHf°, ΔGf°, S° (kJ/mol) for ~300 common compounds
- **Access**: Free, tabulated
- **Source**: CRC Handbook of Chemistry and Physics

### 4. Engineering Toolbox
- **URL**: https://www.engineeringtoolbox.com/standard-state-enthalpy-formation-definition-value-Gibbs-free-energy-entropy-molar-heat-capacity-d_1978.html
- **Content**: ΔHf°, ΔGf°, S°, Cp for common substances
- **Access**: Free, tabulated

### 5. CRC Handbook of Chemistry and Physics
- **Access**: Subscription required (print/electronic)
- **Reference**: The most comprehensive thermodynamic data collection

## Local L4 Data Files

| File | Content |
|------|---------|
| `L4_reference/thermodynamic_data.csv` | Common ΔHf°, ΔGf°, S° values |
| `L4_reference/bond_dissociation_energies.csv` | BDE values (kJ/mol) |
| `L4_reference/acid_base_constants.csv` | Ka, Kb, pKa, pKb values |
| `L4_reference/electrode_potentials.csv` | E° values (V) |
| `L4_reference/solubility_products.csv` | Ksp values |
| `L4_reference/formation_constants.csv` | Kf values for complexes |

## L3 Tool for Thermodynamic Lookup

See: `L3_functions/enthalpy_tools.py` → `lookup_thermodynamic_data(formula)`

## Common Values (Quick Reference)

### Standard Enthalpy of Formation ΔHf° (kJ/mol, 298 K)
See: `L4_reference/thermodynamic_data.csv` for full table.

### Bond Dissociation Energies (kJ/mol)
See: `L4_reference/bond_dissociation_energies.csv`

### Standard Electrode Potentials E° (V)
See: `L4_reference/electrode_potentials.csv`
