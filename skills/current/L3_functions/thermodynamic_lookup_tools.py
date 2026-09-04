"""
Thermodynamic Data Lookup Tools - L3 Implementation

Provides lookup functions for standard thermodynamic data (DeltaHfdeg, DeltaGfdeg, Sdeg, Cp)
from the L4 reference database and NIST Chemistry WebBook.

Source: L4_reference/thermodynamic_data.csv
Related: L2_principles/thermodynamics_laws.md, L2_principles/enthalpy.md
"""

## Solver Instructions (for AI Agent)

# When you encounter **thermodynamic property lookup and reaction thermochemistry** problems, follow this decision tree:

### Step 1: Identify what is given and what is asked
# - Need thermodynamic data for a compound: `lookup_thermodynamic_data(formula)`
# - Need reaction DeltaH or DeltaG: `calculate_reaction_dH(reactants, products)`, `calculate_reaction_dG(reactants, products)`
# - Need to see available compounds: `list_available_compounds()`

### Step 2: Choose the correct function
# - Single compound lookup: `lookup_thermodynamic_data(formula)` returns dict with all properties
# - Reaction enthalpy: `calculate_reaction_dH` - pass reactants and products as lists of (formula, coeff) tuples
# - Reaction Gibbs energy: `calculate_reaction_dG` - same format

### Step 3: Handle special cases
# - Formula strings must match the internal database exactly
# - Use `list_available_compounds()` to check available species
# - Reactant coefficients should be positive; the function handles signs internally

### Examples
# 1. Look up H2O(g): `lookup_thermodynamic_data("H2O(g)")` -> {DeltaH_f, DeltaG_f, Sdeg, Cp}
# 2. DeltaH for N2 + 3H2 -> 2NH3: `calculate_reaction_dH([("N2",1),("H2",3)], [("NH3",2)])`
# 3. Check available species: `list_available_compounds()` -> list of formula strings



import csv
import os

_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                           'L4_reference', 'thermodynamic_data.csv')

def _load_data():
    """Load thermodynamic data from CSV."""
    data = {}
    if os.path.exists(_DATA_PATH):
        with open(_DATA_PATH, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                formula = row['formula'].strip()
                name = row.get('compound_name', '').strip()
                try:
                    dHf = float(row.get('dHf_kJ_mol', 0) or 0)
                except ValueError:
                    continue
                try:
                    dGf = float(row.get('dGf_kJ_mol', 0) or 0)
                except ValueError:
                    dGf = 0.0
                try:
                    S = float(row.get('S_J_mol_K', 0) or 0)
                except ValueError:
                    S = 0.0
                try:
                    Cp = float(row.get('Cp_J_mol_K', 0) or 0)
                except ValueError:
                    Cp = 0.0
                data[formula] = {
                    'formula': formula,
                    'name': name,
                    'dHf': dHf,
                    'dGf': dGf,
                    'S': S,
                    'Cp': Cp,
                    'source': row.get('source', '').strip(),
                }
    return data

_THERMO_DATA = _load_data()


def lookup_thermodynamic_data(formula: str) -> dict:
    """
    Look up standard thermodynamic data for a compound.

    Args:
        formula: Chemical formula (e.g., "H2O(l)", "CO2(g)", "NaCl(s)")

    Returns:
        Dictionary with formula, name, dHf, dGf, S, Cp, or error message if not found.
        All values in standard units (kJ/mol for energies, J/(mol·K) for S and Cp).

    Examples:
        >>> lookup_thermodynamic_data("H2O(l)")
        {'formula': 'H2O(l)', 'name': 'Water', 'dHf': -285.83, 'dGf': -237.13, 'S': 69.91, 'Cp': 75.29}

        >>> lookup_thermodynamic_data("CO2(g)")
        {'formula': 'CO2(g)', 'name': 'Carbon dioxide', 'dHf': -393.51, 'dGf': -394.36, 'S': 213.79, 'Cp': 37.11}
    """
    key = formula.strip()
    # Try exact match first
    if key in _THERMO_DATA:
        result = dict(_THERMO_DATA[key])
        result['found'] = True
        return result

    # Try without phase label
    base = key.rstrip(')glqsl')
    for k, v in _THERMO_DATA.items():
        if k.split('(')[0] == base or k == base:
            result = dict(v)
            result['found'] = True
            return result

    # Try case-insensitive
    key_lower = key.lower()
    for k, v in _THERMO_DATA.items():
        if k.lower() == key_lower:
            result = dict(v)
            result['found'] = True
            return result

    return {
        'formula': formula,
        'found': False,
        'error': f'No thermodynamic data found for {formula}. Check L4_reference/thermodynamic_data.csv or consult NIST WebBook (https://webbook.nist.gov/chemistry/).'
    }


def calculate_reaction_dH(reactants: list, products: list) -> dict:
    """
    Calculate standard reaction enthalpy from formation data.

    Args:
        reactants: List of (formula, coefficient) tuples, e.g., [("CH4(g)", 1), ("O2(g)", 2)]
        products: List of (formula, coefficient) tuples, e.g., [("CO2(g)", 1), ("H2O(l)", 2)]

    Returns:
        Dictionary with dH_reaction in kJ/mol and breakdown.

    Examples:
        >>> calculate_reaction_dH(
        ...     [("CH4(g)", 1), ("O2(g)", 2)],
        ...     [("CO2(g)", 1), ("H2O(l)", 2)]
        ... )
    """
    dH_reactants = 0.0
    dH_products = 0.0
    details = []

    for formula, coeff in reactants:
        data = lookup_thermodynamic_data(formula)
        if not data.get('found'):
            return {'error': f'No data for reactant {formula}', 'dH_reaction': None}
        contrib = coeff * data['dHf']
        dH_reactants += contrib
        details.append(f"{coeff}x{formula}: {contrib:.2f}")

    for formula, coeff in products:
        data = lookup_thermodynamic_data(formula)
        if not data.get('found'):
            return {'error': f'No data for product {formula}', 'dH_reaction': None}
        contrib = coeff * data['dHf']
        dH_products += contrib
        details.append(f"{coeff}x{formula}: {contrib:.2f}")

    dH_rxn = dH_products - dH_reactants

    return {
        'dH_reaction_kJ_mol': round(dH_rxn, 2),
        'dH_reactants_kJ_mol': round(dH_reactants, 2),
        'dH_products_kJ_mol': round(dH_products, 2),
        'breakdown': details,
        'exothermic': dH_rxn < 0,
    }


def calculate_reaction_dG(reactants: list, products: list) -> dict:
    """
    Calculate standard Gibbs free energy of reaction.

    Args:
        reactants: List of (formula, coefficient) tuples
        products: List of (formula, coefficient) tuples

    Returns:
        Dictionary with dG_reaction in kJ/mol.
    """
    dG_reactants = 0.0
    dG_products = 0.0
    details = []

    for formula, coeff in reactants:
        data = lookup_thermodynamic_data(formula)
        if not data.get('found'):
            return {'error': f'No data for reactant {formula}', 'dG_reaction': None}
        contrib = coeff * data['dGf']
        dG_reactants += contrib
        details.append(f"{coeff}x{formula}: {contrib:.2f}")

    for formula, coeff in products:
        data = lookup_thermodynamic_data(formula)
        if not data.get('found'):
            return {'error': f'No data for product {formula}', 'dG_reaction': None}
        contrib = coeff * data['dGf']
        dG_products += contrib
        details.append(f"{coeff}x{formula}: {contrib:.2f}")

    dG_rxn = dG_products - dG_reactants

    return {
        'dG_reaction_kJ_mol': round(dG_rxn, 2),
        'spontaneous': dG_rxn < 0,
        'breakdown': details,
    }


def list_available_compounds() -> list:
    """List all compounds with thermodynamic data available."""
    return [v['formula'] for v in _THERMO_DATA.values()]


# MCP Tool Declarations
MCP_TOOLS = [
    {
        "name": "lookup_thermodynamic_data",
        "description": "Look up standard thermodynamic data (DeltaHfdeg, DeltaGfdeg, Sdeg, Cp) for a compound.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "formula": {
                    "type": "string",
                    "description": "Chemical formula with phase, e.g. H2O(l), CO2(g), NaCl(s)"
                }
            },
            "required": ["formula"]
        },
        "returns": "Dictionary with formula, name, dHf (kJ/mol), dGf (kJ/mol), S (J/mol/K), Cp (J/mol/K)",
        "examples": [
            {"formula": "H2O(l)"},
            {"formula": "CO2(g)"},
            {"formula": "NH3(g)"}
        ]
    },
    {
        "name": "calculate_reaction_dH",
        "description": "Calculate standard reaction enthalpy from standard formation enthalpies.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "reactants": {
                    "type": "array",
                    "description": "List of [formula, coefficient] pairs for reactants",
                    "items": {"type": "array"}
                },
                "products": {
                    "type": "array",
                    "description": "List of [formula, coefficient] pairs for products",
                    "items": {"type": "array"}
                }
            },
            "required": ["reactants", "products"]
        },
        "returns": "Dictionary with dH_reaction_kJ_mol, breakdown of contributions",
        "examples": [
            {"reactants": [["CH4(g)", 1], ["O2(g)", 2]], "products": [["CO2(g)", 1], ["H2O(l)", 2]]}
        ]
    },
    {
        "name": "calculate_reaction_dG",
        "description": "Calculate standard Gibbs free energy of reaction from formation data.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "reactants": {
                    "type": "array",
                    "description": "List of [formula, coefficient] pairs for reactants",
                    "items": {"type": "array"}
                },
                "products": {
                    "type": "array",
                    "description": "List of [formula, coefficient] pairs for products",
                    "items": {"type": "array"}
                }
            },
            "required": ["reactants", "products"]
        },
        "returns": "Dictionary with dG_reaction_kJ_mol and spontaneity indicator",
        "examples": [
            {"reactants": [["N2(g)", 1], ["H2(g)", 3]], "products": [["NH3(g)", 2]]}
        ]
    },
    {
        "name": "list_available_compounds",
        "description": "List all compounds with thermodynamic data available in L4.",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        },
        "returns": "List of compound formulas with available data"
    }
]
