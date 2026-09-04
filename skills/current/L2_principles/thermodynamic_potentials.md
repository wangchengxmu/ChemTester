---
id: thermodynamic-potentials
layer: L2
topic: thermodynamics
source: DeVoe Ch5
depends: [thermodynamics_laws, gibbs_free_energy, entropy]
tags: [thermodynamics, potentials, maxwell, legendre, spontaneity]
---

# Thermodynamic Potentials

## Concept Overview
The four thermodynamic potentialsâU, H, A, Gâare energy-based state functions that provide criteria for spontaneity and equilibrium under different constraints. They are related by Legendre transforms of the internal energy. Together with internal energy, they are called thermodynamic potentials (not to be confused with the chemical potential Î¼).

## Key Principles

### Definitions via Legendre Transforms
Starting from dU = TdS â pdV for a closed system, the independent variables S and V are the natural variables of U. Since entropy is especially inconvenient (cannot be measured directly), Legendre transforms change the independent variables by subtracting products of conjugate variables.

| Potential | Definition | Natural Variables | d(Potential) |
|-----------|-----------|-------------------|-------------|
| U (internal energy) | â | S, V | dU = TdS â pdV |
| H (enthalpy) | H = U + pV | S, p | dH = TdS + Vdp |
| A (Helmholtz energy) | A = U â TS | T, V | dA = âSdT â pdV |
| G (Gibbs energy) | G = H â TS = U â TS + pV | T, p | dG = âSdT + Vdp |

**Alternative names** (DeVoe/DeVoe):
- Helmholtz energy: also called Helmholtz function, Helmholtz free energy, work function (symbol F sometimes used)
- Gibbs energy: also called Gibbs function, Gibbs free energy

These are state functions (extensive). If T or p is non-uniform, apply definitions to subsystems.

### General Expressions for Infinitesimal Changes (DeVoe 5.3.4â5.3.6)
For any system or phase with uniform T and p:
```
dH = dU + p dV + V dp
dA = dU â T dS â S dT
dG = dU â T dS â S dT + p dV + V dp
```
These are NOT total differentialsâthe variables in each are not independent unless constraints are applied.

### Useful Properties at Specific Constraints (DeVoe 5.3.7â5.3.9)
- **Constant p, w'=0**: dH = dq (enthalpy change = heat) â ÎH = q
- **Constant V, w'=0**: dU = dq (internal energy change = heat) â ÎU = q
- This makes enthalpy the natural quantity for constant-pressure calorimetry

### Maxwell Relations
From the exactness of total differentials (Euler reciprocity):

| From dU | From dH | From dA | From dG |
|---------|---------|---------|---------|
| (âT/âV)_S = â(âp/âS)_V | (âT/âp)_S = (âV/âS)_p | (âS/âV)_T = (âp/âT)_V | (âS/âp)_T = â(âV/âT)_p |

The last two are most useful in practice:
- (âS/âV)_T = (âp/âT)_V â thermal pressure coefficient
- â(âS/âp)_T = (âV/âT)_p â relates to thermal expansion

### Heat Capacity Relations (DeVoe 5.5)
```
C_p â C_V = TVÎ±Â²/Îº_T
```
where Î± = (1/V)(âV/âT)_p (cubic expansion coefficient) and Îº_T = â(1/V)(âV/âp)_T (isothermal compressibility).

### Surface Work (DeVoe 5.7)
When surface effects are important (e.g., liquid droplets), the fundamental equation extends:
```
dU = TdS â pdV + Î³dA_s
```
where Î³ is surface tension and A_s is surface area. This leads to additional Maxwell relations involving surface terms.

### Criteria for Spontaneity and Equilibrium
| Constraint | Criterion | At Equilibrium |
|-----------|-----------|---------------|
| Constant S, V | dU â¤ 0 | U minimum |
| Constant S, p | dH â¤ 0 | H minimum |
| Constant T, V | dA â¤ 0 | A minimum |
| Constant T, p | dG â¤ 0 | G minimum |

### Gibbs-Helmholtz Equation
```
[â(G/T)/âT]_p = âH/TÂ²
```
Useful for temperature dependence of equilibrium constants.

### Chemical Potential (Î¼)
For open systems, the fundamental equation becomes:
```
dU = TdS â pdV + Î£Î¼áµ¢dnáµ¢
dG = âSdT + Vdp + Î£Î¼áµ¢dnáµ¢
```
where Î¼áµ¢ = (âG/ânáµ¢)_{T,p,n_jâ i}

For a pure substance in a single phase: Î¼ = G_m (molar Gibbs energy).

### Gibbs-Duhem Equation
At constant T and p:
```
Î£náµ¢dÎ¼áµ¢ = 0
```
Constrains how chemical potentials can vary in a mixture. For a binary mixture: n_A dÎ¼_A + n_B dÎ¼_B = 0.

## Physical Interpretation (DeVoe)
- **U**: total energy; minimized at constant S, V
- **H**: U + pV; heat absorbed at constant p (w'=0)
- **A**: U â TS; maximum work extractable at constant T, V (so-called "work function")
- **G**: H â TS; maximum non-pV work at constant T, p; most important for chemistry (reactions at constant T, p)

## L3 Tools
- `L3_functions/thermodynamic_potentials_tools.py` â compute Legendre transforms, Maxwell relations, spontaneity checks
- `L3_functions/gibbs_free_energy_tools.py` â Gibbs energy calculations

## L4 Data
- Standard thermodynamic data tables (ÎfHÂ°, SÂ°, ÎfGÂ°) in `L4_data/thermodynamic_tables/`

## Source
DeVoe, *Thermodynamics and Chemistry*, Ch5. LibreTexts: https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/DeVoes_Thermodynamics_and_Chemistry/05%3A_Thermodynamic_Potentials

## Data Reference
- L3 Tool: 	hermodynamic_lookup_tools.lookup_thermodynamic_data(formula) â ÎHfÂ°, ÎGfÂ°, SÂ°, Cp for 58+ compounds
- L3 Tool: 	hermodynamic_lookup_tools.calculate_reaction_dH(reactants, products) â reaction enthalpy from formation data
- L3 Tool: 	hermodynamic_lookup_tools.calculate_reaction_dG(reactants, products) â reaction Gibbs energy
- L4 Data: L4_reference/thermodynamic_data.csv â Full table with NIST/CRC values
- L4 Reference: L4_reference/THERMODYNAMIC_DATABASES.md â Links to NIST-JANAF, NIST WebBook

## L3 Tool Call Directives

**Source:** 	hermodynamic_lookup_tools.py
Standard thermodynamic data lookup and reaction thermochemistry from L4 database.

### Available functions:
- lookup_thermodynamic_data(formula: str) ¡ú dict ¡ª Returns formula, name, dHf, dGf, S, Cp; supports fuzzy matching
- calculate_reaction_dH(reactants: List[Tuple], products: List[Tuple]) ¡ú dict ¡ª ¦¤H_rxn from formation data; input as [(formula, coeff)]
- calculate_reaction_dG(reactants: List[Tuple], products: List[Tuple]) ¡ú dict ¡ª ¦¤G_rxn with spontaneity flag
- list_available_compounds() ¡ú list ¡ª All compounds in L4_reference/thermodynamic_data.csv

### Common errors:
- ? Formula must match database format (e.g., 'H2O(l)', 'CO2(g)'); use list_available_compounds() to check
- ? Coefficients in calculate_reaction_dH/dG are positive for both reactants and products (signs handled internally)

## L3 Tool Call Directives

**Source:** `thermodynamic_data_tools.py` | `thermodynamic_lookup_tools.py`
Thermodynamic data lookup, Hess's law calculations, reaction enthalpy/entropy/Gibbs.

### Available functions (thermodynamic_data_tools):
- `lookup_formation_enthalpy(species)` → float — Standard enthalpy of formation ΔH°f (kJ/mol)
- `lookup_formation_gibbs(species)` → float — Standard Gibbs energy of formation ΔG°f (kJ/mol)
- `lookup_standard_entropy(species)` → float — Standard molar entropy S° (J/(mol·K))
- `lookup_heat_capacity(species)` → float — Standard heat capacity Cp° (J/(mol·K))
- `calculate_hess_law(reaction_equation)` → float — Reaction enthalpy from Hess's law using formation data
- `calculate_reaction_entropy(reaction_equation)` → float — Reaction entropy from standard entropies
- `calculate_reaction_gibbs(reaction_equation)` → float — Reaction Gibbs energy from formation data

### Available functions (thermodynamic_lookup_tools):
- `lookup_thermodynamic_data(formula)` → dict — Look up all thermodynamic properties for a compound
- `calculate_reaction_dH(reactants, products)` → dict — Reaction enthalpy with full stoichiometric accounting
- `calculate_reaction_dG(reactants, products)` → dict — Reaction Gibbs energy with full accounting
- `list_available_compounds()` → list — List all compounds in the thermodynamic database

### Common errors:
- ❌ Forgetting to multiply by stoichiometric coefficients in Hess's law
- ❌ Confusing formation enthalpy units (kJ/mol) with entropy units (J/(mol·K)) — factor of 1000!
