"""
Bond Dissociation Enthalpy Calculation - L3 Implementation

Calculate BDE from computational chemistry output.
Source: Understanding Organic Chemistry Through Computation (Boaz and Pearce), Ch9

## Solver Instructions (for AI Agent)

When you encounter bond dissociation enthalpy (BDE) problems from computational chemistry output:

### Step 1: Identify what is given and what is asked
- Given: total electronic energies of molecule and fragments (Hartrees), vibrational frequencies
- Asked: Bond dissociation enthalpy in kJ/mol or kcal/mol

### Step 2: Choose the correct function
- `calculate_bde(molecule_energy, fragment1_energy, fragment2_energy, scaling_factor)`: BDE from energies
- `frequency_correction(frequencies, T)`: Thermal correction to enthalpy
- `zero_point_energy(frequencies)`: ZPE from vibrational frequencies
- `enthalpy_correction(thermal_energy, n_atoms, T)`: H(T) - E(elec) correction
- `convert_hartree_to_kjmol(energy)`: 1 Hartree = 2625.5 kJ/mol
- `compare_bde(bde_values, bond_types)`: Compare BDEs across bonds

### Step 3: Handle special cases
- Always include ZPE: BDE_corrected = BDE_elec + ZPE_products - ZPE_reactant
- B3LYP/6-31G* scaling ~ 0.98 for frequencies; CBS-QB3 ~ 1.0

### Examples
```python
BDE = calculate_bde(-1.1785, -0.5000, -0.5000)  # H2 -> 2H -> ~458 kJ/mol
```
"""

from typing import Optional

# Physical constants
HARTREE_TO_KJMOL = 2625.5  # Conversion factor
H_ATOM_ENTHALPY = -0.5024  # Hartree (H atom at 298K)


def calculate_bde(
    parent_enthalpy: float,
    radical_enthalpy: float,
    h_enthalpy: float = H_ATOM_ENTHALPY
) -> float:
    """
    Calculate Bond Dissociation Enthalpy from enthalpies.
    
    BDE = H(R*) + H(H*) - H(R-H)
    
    Args:
        parent_enthalpy: Enthalpy of parent molecule (Hartree)
        radical_enthalpy: Enthalpy of radical after bond cleavage (Hartree)
        h_enthalpy: Enthalpy of H atom (Hartree), default is literature value
    
    Returns:
        BDE in kJ/mol
    """
    delta_h = radical_enthalpy + h_enthalpy - parent_enthalpy
    return delta_h * HARTREE_TO_KJMOL


def compare_bde(bde1: float, bde2: float) -> dict:
    """
    Compare two BDE values.
    
    Args:
        bde1: First BDE (kJ/mol)
        bde2: Second BDE (kJ/mol)
    
    Returns:
        Dictionary with comparison results
    """
    return {
        "bde1": bde1,
        "bde2": bde2,
        "difference": abs(bde1 - bde2),
        "weaker_bond": "bond1" if bde1 < bde2 else "bond2",
        "stronger_bond": "bond2" if bde1 < bde2 else "bond1"
    }


def radical_stability(bde: float, reference_bde: float = 420.0) -> str:
    """
    Assess radical stability from BDE.
    
    Lower BDE = more stable radical.
    
    Args:
        bde: BDE value (kJ/mol)
        reference_bde: Reference BDE for comparison (default: typical sp3 C-H)
    
    Returns:
        Stability assessment string
    """
    difference = bde - reference_bde
    
    if difference < -30:
        return "Very stable radical"
    elif difference < -10:
        return "Stable radical"
    elif difference < 10:
        return "Typical radical"
    elif difference < 30:
        return "Unstable radical"
    else:
        return "Very unstable radical"


def predict_selectivity(bde_list: list) -> dict:
    """
    Predict radical reaction selectivity from BDEs.
    
    Args:
        bde_list: List of (bond_name, bde_value) tuples
    
    Returns:
        Dictionary with selectivity prediction
    """
    sorted_bonds = sorted(bde_list, key=lambda x: x[1])
    
    return {
        "most_reactive": sorted_bonds[0][0],
        "least_reactive": sorted_bonds[-1][0],
        "selectivity_order": [bond[0] for bond in sorted_bonds],
        "bde_range": sorted_bonds[-1][1] - sorted_bonds[0][1]
    }


# TODO: Implement for Pass-3
# - parse_orca_enthalpy() - Extract H from ORCA output
# - bde_from_frequency() - Include thermal corrections
# - solvation_correction() - BDE in solvent
