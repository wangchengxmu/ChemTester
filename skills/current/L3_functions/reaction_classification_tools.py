"""
# Reaction Classification Tools (L3)
# Source: LibreTexts Chemistry 2e Ch04.02

## Solver Instructions (for AI Agent)

# When you encounter reaction classification problems (precipitation, acid-base, redox, solubility prediction), follow this decision tree:

### Step 1: Identify what is given and what is asked
# - **Solubility check**: Given cation and anion -> predict if precipitate forms
# - **Reaction type**: Given reactants -> classify as precipitation, acid-base, redox, combination, decomposition, combustion
# - **Net ionic equation**: Given molecular equation -> write net ionic form
# - **Oxidation states**: Given species -> assign oxidation numbers
# - **Redox identification**: Given reaction -> identify oxidizing/reducing agents
# - **Acid-base classification**: Given reactants -> classify as Arrhenius, Brønsted-Lowry, or Lewis

### Step 2: Choose the correct function
# - `is_soluble(cation, anion)` -> True/False based on solubility rules
# - `classify_reaction(reactants, products)` -> reaction type string
# - `net_ionic_equation(left_side, right_side)` -> balanced net ionic equation
# - `assign_oxidation_states(formula)` -> dict of {element: oxidation_state}
# - `identify_redox_agents(reactants, products)` -> (oxidizing_agent, reducing_agent)
# - `balance_redox(half_rxn_oxidation, half_rxn_reduction)` -> balanced redox equation

### Step 3: Handle special cases
# - Always-soluble cations: Group 1, NH4+
# - Insoluble exceptions: Ag+, Pb2+, Hg22+ with halides; Ba2+ with SO42-
# - Carbonates, phosphates, sulfides mostly insoluble (except Group 1, NH4+)
# - For precipitation: if products are insoluble, reaction proceeds

### Examples
# 1. **Solubility**: Will AgCl precipitate? Ag+ + Cl-
#    -> `is_soluble('Ag', 'Cl')` -> False (precipitate forms)

# 2. **Solubility**: NaNO3?
#    -> `is_soluble('Na', 'NO3')` -> True (nitrates always soluble)

# 3. **BaSO4**: Ba2+ + SO42-
#    -> `is_soluble('Ba', 'SO4')` -> False (Ba2+ is exception for sulfates)
"""

from collections import defaultdict

# Solubility rules data
SOLUBLE_ALWAYS = {
    # Cations that are always soluble
    'Li': True, 'Na': True, 'K': True, 'Rb': True, 'Cs': True,
    'NH4': True,  # Ammonium
}

SOLUBLE_ANIONS = {
    # Anions that form soluble salts (with exceptions)
    'NO3': [],      # Nitrates - always soluble
    'C2H3O2': [],   # Acetates - always soluble
    'ClO3': [],     # Perchlorates - always soluble
    'Cl': ['Ag', 'Hg2', 'Pb'],   # Chlorides - except Ag, Hg2, Pb
    'Br': ['Ag', 'Hg2', 'Pb'],   # Bromides - except Ag, Hg2, Pb
    'I': ['Ag', 'Hg2', 'Pb'],    # Iodides - except Ag, Hg2, Pb
    'SO4': ['Ag', 'Ba', 'Ca', 'Hg2', 'Pb', 'Sr'],  # Sulfates - except these
}

INSOLUBLE_ANIONS = {
    # Anions that form insoluble salts (with exceptions)
    'CO3': ['Li', 'Na', 'K', 'Rb', 'Cs', 'NH4'],  # Carbonates
    'PO4': ['Li', 'Na', 'K', 'Rb', 'Cs', 'NH4'],  # Phosphates
    'CrO4': ['Li', 'Na', 'K', 'Rb', 'Cs', 'NH4'], # Chromates
    'S': ['Li', 'Na', 'K', 'Rb', 'Cs', 'NH4'],    # Sulfides
    'OH': ['Li', 'Na', 'K', 'Rb', 'Cs', 'Ba'],    # Hydroxides
}

# Common ions with charges
ION_CHARGES = {
    # Cations
    'H': 1, 'Li': 1, 'Na': 1, 'K': 1, 'Rb': 1, 'Cs': 1,
    'NH4': 1,  # Ammonium
    'Mg': 2, 'Ca': 2, 'Sr': 2, 'Ba': 2,
    'Zn': 2, 'Fe': (2, 3), 'Cu': (1, 2),
    'Ag': 1, 'Pb': 2, 'Hg2': 2,
    'Al': 3, 'Fe3': 3, 'Cr': 3,
    # Anions
    'Cl': -1, 'Br': -1, 'I': -1, 'F': -1,
    'OH': -1, 'NO3': -1, 'C2H3O2': -1, 'ClO3': -1,
    'O': -2, 'S': -2, 'SO4': -2, 'CO3': -2, 'PO4': -3,
}


def is_soluble(cation, anion):
    """
    Check if an ionic compound is soluble based on solubility rules.
    
    Parameters:
        cation: cation name (e.g., 'Na', 'Ag', 'NH4')
        anion: anion name (e.g., 'Cl', 'SO4', 'OH')
    
    Returns:
        bool: True if soluble, False if insoluble
    
    Examples:
        >>> is_soluble('Na', 'Cl')
        True
        >>> is_soluble('Ag', 'Cl')
        False
        >>> is_soluble('Ba', 'SO4')
        False
    """
    # Check if cation is always soluble
    if cation in SOLUBLE_ALWAYS:
        return True
    
    # Check if anion is in soluble list
    if anion in SOLUBLE_ANIONS:
        exceptions = SOLUBLE_ANIONS[anion]
        return cation not in exceptions
    
    # Check if anion is in insoluble list
    if anion in INSOLUBLE_ANIONS:
        exceptions = INSOLUBLE_ANIONS[anion]
        return cation in exceptions
    
    # Default: assume insoluble
    return False


def predict_precipitation(reactants):
    """
    Predict if mixing solutions will cause precipitation.
    
    Parameters:
        reactants: list of tuples [(cation1, anion1), (cation2, anion2), ...]
    
    Returns:
        dict: {
            'precipitation': bool,
            'precipitate': (cation, anion) or None,
            'solubility_check': {compound: is_soluble}
        }
    
    Examples:
        >>> predict_precipitation([('Na', 'Cl'), ('Ag', 'NO3')])
        {'precipitation': True, 'precipitate': ('Ag', 'Cl'), ...}
    """
    # Collect all ions
    cations = set()
    anions = set()
    
    for cation, anion in reactants:
        cations.add(cation)
        anions.add(anion)
    
    # Check all possible combinations
    solubility_check = {}
    precipitate = None
    
    for cation in cations:
        for anion in anions:
            compound = f"{cation}{anion}"
            soluble = is_soluble(cation, anion)
            solubility_check[compound] = soluble
            
            # Skip compounds that are same as reactants
            if not soluble:
                # Check if this is a new compound (not one of the reactants)
                is_reactant = any(
                    c == cation and a == anion for c, a in reactants
                )
                if not is_reactant:
                    precipitate = (cation, anion)
    
    return {
        'precipitation': precipitate is not None,
        'precipitate': precipitate,
        'solubility_check': solubility_check
    }


# Strong acids and bases
STRONG_ACIDS = {'HCl', 'HBr', 'HI', 'HNO3', 'HClO4', 'H2SO4'}
STRONG_BASES = {'NaOH', 'KOH', 'LiOH', 'RbOH', 'CsOH', 'Ba(OH)2', 'Ca(OH)2', 'Sr(OH)2'}


def is_strong_acid(formula):
    """Check if compound is a strong acid."""
    return formula in STRONG_ACIDS


def is_strong_base(formula):
    """Check if compound is a strong base."""
    return formula in STRONG_BASES


def assign_oxidation_numbers(formula, charge=0):
    """
    Assign oxidation numbers to elements in a compound.
    
    This is a simplified implementation for common compounds.
    
    Parameters:
        formula: chemical formula (e.g., 'H2SO4', 'Fe2O3')
        charge: overall charge of ion (default 0 for neutral compound)
    
    Returns:
        dict: {element: oxidation_number}
    
    Examples:
        >>> assign_oxidation_numbers('H2O')
        {'H': 1, 'O': -2}
        >>> assign_oxidation_numbers('SO4', charge=-2)
        {'S': 6, 'O': -2}
    """
    from L3_functions.equation_balancing_tools import parse_formula
    
    atom_counts = parse_formula(formula)
    oxidation_numbers = {}
    
    # Known oxidation states (simplified rules)
    # Apply rules in order
    
    # Rule 1: H is +1 (except with metals)
    # Rule 2: O is -2 (except peroxides)
    # Rule 3: Group 1 = +1, Group 2 = +2
    # Rule 4: F is -1, other halogens usually -1
    
    remaining_charge = charge
    remaining_elements = set(atom_counts.keys())
    
    # Apply known oxidation states
    if 'H' in atom_counts:
        # H is usually +1
        oxidation_numbers['H'] = 1
        remaining_charge -= atom_counts['H'] * 1
        remaining_elements.discard('H')
    
    if 'O' in atom_counts:
        # O is usually -2
        oxidation_numbers['O'] = -2
        remaining_charge -= atom_counts['O'] * (-2)
        remaining_elements.discard('O')
    
    if 'F' in atom_counts:
        oxidation_numbers['F'] = -1
        remaining_charge -= atom_counts['F'] * (-1)
        remaining_elements.discard('F')
    
    # Group 1 metals
    group1 = {'Li', 'Na', 'K', 'Rb', 'Cs'}
    for elem in group1:
        if elem in atom_counts:
            oxidation_numbers[elem] = 1
            remaining_charge -= atom_counts[elem] * 1
            remaining_elements.discard(elem)
    
    # Group 2 metals
    group2 = {'Mg', 'Ca', 'Sr', 'Ba'}
    for elem in group2:
        if elem in atom_counts:
            oxidation_numbers[elem] = 2
            remaining_charge -= atom_counts[elem] * 2
            remaining_elements.discard(elem)
    
    # Al is usually +3
    if 'Al' in atom_counts:
        oxidation_numbers['Al'] = 3
        remaining_charge -= atom_counts['Al'] * 3
        remaining_elements.discard('Al')
    
    # Zn is usually +2
    if 'Zn' in atom_counts:
        oxidation_numbers['Zn'] = 2
        remaining_charge -= atom_counts['Zn'] * 2
        remaining_elements.discard('Zn')
    
    # Ag is usually +1
    if 'Ag' in atom_counts:
        oxidation_numbers['Ag'] = 1
        remaining_charge -= atom_counts['Ag'] * 1
        remaining_elements.discard('Ag')
    
    # Calculate remaining element oxidation number
    if len(remaining_elements) == 1:
        elem = list(remaining_elements)[0]
        count = atom_counts[elem]
        oxidation_numbers[elem] = remaining_charge / count
    elif len(remaining_elements) > 1:
        # Multiple unknown elements - need more sophisticated approach
        # For now, distribute charge equally (simplified)
        total_atoms = sum(atom_counts[e] for e in remaining_elements)
        for elem in remaining_elements:
            oxidation_numbers[elem] = remaining_charge / total_atoms * atom_counts[elem] / atom_counts[elem]
    
    return oxidation_numbers


def identify_redox(reactant_oxidation, product_oxidation):
    """
    Identify redox changes between reactants and products.
    
    Parameters:
        reactant_oxidation: dict {element: ox_num} for reactants
        product_oxidation: dict {element: ox_num} for products
    
    Returns:
        dict: {
            'is_redox': bool,
            'oxidized': list of elements with increased ON,
            'reduced': list of elements with decreased ON,
            'oxidizing_agent': element reduced,
            'reducing_agent': element oxidized
        }
    
    Examples:
        >>> reactants = {'Na': 0, 'Cl': 0}
        >>> products = {'Na': 1, 'Cl': -1}
        >>> identify_redox(reactants, products)
        {'is_redox': True, 'oxidized': ['Na'], 'reduced': ['Cl'], ...}
    """
    oxidized = []
    reduced = []
    
    all_elements = set(reactant_oxidation.keys()) | set(product_oxidation.keys())
    
    for elem in all_elements:
        reactant_on = reactant_oxidation.get(elem, 0)
        product_on = product_oxidation.get(elem, 0)
        
        if product_on > reactant_on:
            oxidized.append(elem)
        elif product_on < reactant_on:
            reduced.append(elem)
    
    return {
        'is_redox': len(oxidized) > 0 or len(reduced) > 0,
        'oxidized': oxidized,
        'reduced': reduced,
        'oxidizing_agent': reduced[0] if reduced else None,
        'reducing_agent': oxidized[0] if oxidized else None
    }


def classify_reaction(reactants, products):
    """
    Classify a chemical reaction type.
    
    Parameters:
        reactants: list of reactant formulas
        products: list of product formulas
    
    Returns:
        str: reaction type ('precipitation', 'acid_base', 'redox', 'combination', 
                           'decomposition', 'single_replacement', 'double_replacement', 
                           or 'unknown')
    
    Examples:
        >>> classify_reaction(['NaCl(aq)', 'AgNO3(aq)'], ['AgCl(s)', 'NaNO3(aq)'])
        'precipitation'
    """
    # Check for precipitation (solid product from aqueous reactants)
    has_aq_reactant = any('(aq)' in r or 'aq' in r.lower() for r in reactants)
    has_solid_product = any('(s)' in p or 's' in p.lower().split()[-1] == 's' 
                           for p in products)
    
    if has_aq_reactant and has_solid_product:
        return 'precipitation'
    
    # Check for acid-base (H+ transfer)
    acid_indicators = ['HCl', 'H2SO4', 'HNO3', 'HBr', 'HI', 'HClO4', 'acid']
    base_indicators = ['OH', 'oxide', 'base']
    
    has_acid = any(any(acid in r for acid in acid_indicators) for r in reactants)
    has_base = any(any(base in r for base in base_indicators) for r in reactants)
    has_water = 'H2O' in str(products)
    
    if has_acid and has_base and has_water:
        return 'acid_base'
    
    # Check for combination (A + B -> AB)
    if len(reactants) == 2 and len(products) == 1:
        return 'combination'
    
    # Check for decomposition (AB -> A + B)
    if len(reactants) == 1 and len(products) >= 2:
        return 'decomposition'
    
    # Check for combustion (hydrocarbon + O2 -> CO2 + H2O)
    has_O2 = any('O2' in r for r in reactants)
    has_CO2 = any('CO2' in p for p in products)
    has_H2O = any('H2O' in p for p in products)
    
    if has_O2 and has_CO2 and has_H2O:
        return 'combustion'
    
    return 'unknown'


if __name__ == "__main__":
    print("Reaction classification tools - implemented")
    
    # Test solubility
    print("\n=== Solubility tests ===")
    print(f"NaCl: {is_soluble('Na', 'Cl')}")  # True
    print(f"AgCl: {is_soluble('Ag', 'Cl')}")  # False
    print(f"BaSO4: {is_soluble('Ba', 'SO4')}")  # False
    print(f"CaCO3: {is_soluble('Ca', 'CO3')}")  # False
    
    # Test precipitation prediction
    print("\n=== Precipitation prediction ===")
    result = predict_precipitation([('Na', 'Cl'), ('Ag', 'NO3')])
    print(f"NaCl + AgNO3: {result}")
    
    # Test oxidation numbers
    print("\n=== Oxidation numbers ===")
    print(f"H2O: {assign_oxidation_numbers('H2O')}")
    print(f"SO4^2-: {assign_oxidation_numbers('SO4', charge=-2)}")
    print(f"Fe2O3: {assign_oxidation_numbers('Fe2O3')}")


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="assign_oxidation_numbers",
            description="Assign oxidation numbers to elements in a compound.",
            input_schema=[
            InputSchemaField(name="formula", type="string", required=True),
            InputSchemaField(name="charge", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="classify_reaction",
            description="Classify a chemical reaction type.",
            input_schema=[
            InputSchemaField(name="reactants", type="number", required=True),
            InputSchemaField(name="products", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="identify_redox",
            description="Identify redox changes between reactants and products.",
            input_schema=[
            InputSchemaField(name="reactant_oxidation", type="number", required=True),
            InputSchemaField(name="product_oxidation", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="is_soluble",
            description="Check if an ionic compound is soluble based on solubility rules.",
            input_schema=[
            InputSchemaField(name="cation", type="number", required=True),
            InputSchemaField(name="anion", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="is_strong_acid",
            description="Check if compound is a strong acid.",
            input_schema=[
            InputSchemaField(name="formula", type="string", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="is_strong_base",
            description="Check if compound is a strong base.",
            input_schema=[
            InputSchemaField(name="formula", type="string", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="predict_precipitation",
            description="Predict if mixing solutions will cause precipitation.",
            input_schema=[
            InputSchemaField(name="reactants", type="number", required=True)
            ],
            handler="{name}",
        )
    ]
