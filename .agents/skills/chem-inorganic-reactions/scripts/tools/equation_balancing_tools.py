"""
Equation Balancing Tools (L3)
Source: LibreTexts Chemistry 2e Ch04.01
## Solver Instructions (for AI Agent)

When you encounter chemical equation balancing problems, follow this decision tree:

### Step 1: Identify what is given and what is asked
- Unbalanced equation -> Balance it? Use `balance_equation(equation_string)`
- Need element counts in formula? Use `parse_formula(formula)` -> {element: count}
- Need to verify balance? Use `verify_balance(reactants, products, coeffs)` -> True/False
- Need molar masses? Use `molar_mass(formula)`
- Need to balance with specific method? Try `balance_equation` first (general solver)

### Step 2: Handle special cases
- **Format**: Use standard chemical notation: "H2 + O2 -> H2O" or "H2 + O2 = H2O"
- **Polyatomic ions**: Supported via parentheses: "Ca(OH)2 + HCl -> CaCl2 + H2O"
- **Ions**: Include charge: "Fe3+ + OH- -> Fe(OH)3"
- **States**: Phase labels in parentheses are ignored during balancing

### Examples
```python
# Example 1: Balance combustion
balance_equation("C3H8 + O2 -> CO2 + H2O")
# -> {'C3H8': 1, 'O2': 5, 'CO2': 3, 'H2O': 4}

# Example 2: Parse formula
parse_formula("Al2(SO4)3")  # -> {'Al': 2, 'S': 3, 'O': 12}

# Example 3: Molar mass
molar_mass("C6H12O6")  # -> 180.16 g/mol
```
"""

import re
from collections import defaultdict


def parse_formula(formula):
    """
    Parse a chemical formula into element counts.
    
    Handles:
    - Simple formulas: H2O, NaCl
    - Parentheses: Ca(OH)2, Al2(SO4)3
    - Nested not supported for simplicity
    
    Parameters:
        formula: chemical formula string (e.g., "H2O", "Ca(OH)2")
    
    Returns:
        dict: {element: count}
    
    Examples:
        >>> parse_formula("H2O")
        {'H': 2, 'O': 1}
        >>> parse_formula("Ca(OH)2")
        {'Ca': 1, 'O': 2, 'H': 2}
    """
    elements = defaultdict(int)
    
    # Pattern for element + optional count: Element symbol followed by optional number
    # Pattern for (group) + count: parenthesized group followed by number
    i = 0
    while i < len(formula):
        if formula[i] == '(':
            # Find matching closing paren
            depth = 1
            j = i + 1
            while j < len(formula) and depth > 0:
                if formula[j] == '(':
                    depth += 1
                elif formula[j] == ')':
                    depth -= 1
                j += 1
            # j now points to char after ')'
            group = formula[i+1:j-1]
            
            # Get multiplier after ')'
            k = j
            while k < len(formula) and formula[k].isdigit():
                k += 1
            multiplier = int(formula[j:k]) if j < k else 1
            
            # Recursively parse group and multiply
            group_elements = parse_formula(group)
            for elem, count in group_elements.items():
                elements[elem] += count * multiplier
            
            i = k
        elif formula[i].isupper():
            # Element symbol
            j = i + 1
            while j < len(formula) and formula[j].islower():
                j += 1
            element = formula[i:j]
            
            # Get count
            k = j
            while k < len(formula) and formula[k].isdigit():
                k += 1
            count = int(formula[j:k]) if j < k else 1
            
            elements[element] += count
            i = k
        else:
            i += 1
    
    return dict(elements)


def count_atoms(formula, coefficient=1):
    """
    Count atoms in a chemical formula with coefficient.
    
    Parameters:
        formula: chemical formula string (e.g., "H2O", "Ca(OH)2")
        coefficient: coefficient in equation
    
    Returns:
        dict: {element: count}
    
    Examples:
        >>> count_atoms("H2O", coefficient=2)
        {'H': 4, 'O': 2}
    """
    if coefficient <= 0:
        raise ValueError("Coefficient must be positive")
    
    base_counts = parse_formula(formula)
    return {elem: count * coefficient for elem, count in base_counts.items()}


def check_balance(reactants, products):
    """
    Check if equation is balanced.
    
    Parameters:
        reactants: list of (formula, coefficient) tuples
        products: list of (formula, coefficient) tuples
    
    Returns:
        tuple: (is_balanced: bool, element_counts: dict)
        element_counts: {element: (reactant_count, product_count)} for debugging
    
    Examples:
        >>> check_balance([("H2", 2), ("O2", 1)], [("H2O", 2)])
        (True, {'H': (4, 4), 'O': (2, 2)})
        >>> check_balance([("H2", 1), ("O2", 1)], [("H2O", 1)])
        (False, {'H': (2, 2), 'O': (2, 1)})
    """
    # Sum up atoms on each side
    reactant_atoms = defaultdict(int)
    product_atoms = defaultdict(int)
    
    for formula, coeff in reactants:
        counts = count_atoms(formula, coeff)
        for elem, count in counts.items():
            reactant_atoms[elem] += count
    
    for formula, coeff in products:
        counts = count_atoms(formula, coeff)
        for elem, count in counts.items():
            product_atoms[elem] += count
    
    # Compare
    all_elements = set(reactant_atoms.keys()) | set(product_atoms.keys())
    element_counts = {}
    is_balanced = True
    
    for elem in all_elements:
        r_count = reactant_atoms.get(elem, 0)
        p_count = product_atoms.get(elem, 0)
        element_counts[elem] = (r_count, p_count)
        if r_count != p_count:
            is_balanced = False
    
    return is_balanced, element_counts


def _get_all_elements(formulas):
    """Extract all unique elements from a list of formulas."""
    elements = set()
    for formula in formulas:
        elements.update(parse_formula(formula).keys())
    return elements


def balance_by_inspection(reactant_formulas, product_formulas, max_coeff=20):
    """
    Balance equation using systematic coefficient search.
    
    For simple equations, tries integer coefficients up to max_coeff.
    
    Parameters:
        reactant_formulas: list of formula strings
        product_formulas: list of formula strings
        max_coeff: maximum coefficient to try (default 20)
    
    Returns:
        dict: {'reactants': [(formula, coeff), ...], 
               'products': [(formula, coeff), ...]}
        or None if cannot balance
    
    Examples:
        >>> balance_by_inspection(["H2", "O2"], ["H2O"])
        {'reactants': [('H2', 2), ('O2', 1)], 'products': [('H2O', 2)]}
    """
    from itertools import product as cartesian_product
    from math import gcd
    from functools import reduce
    
    n_reactants = len(reactant_formulas)
    n_products = len(product_formulas)
    all_formulas = reactant_formulas + product_formulas
    n_compounds = len(all_formulas)
    elements = sorted(_get_all_elements(all_formulas))
    
    if n_compounds == 0:
        return None
    
    # Build atom matrix as list of lists (pure Python, no numpy)
    # Each column is a compound, each row is an element
    # Reactants are positive, products are negative
    matrix = []
    for elem in elements:
        row = []
        for formula in reactant_formulas:
            counts = parse_formula(formula)
            row.append(counts.get(elem, 0))
        for formula in product_formulas:
            counts = parse_formula(formula)
            row.append(-counts.get(elem, 0))  # Products are negative
        matrix.append(row)
    
    def check_balance(coeffs):
        """Check if coefficients balance the equation."""
        for row in matrix:
            total = sum(row[col] * coeffs[col] for col in range(n_compounds))
            if total != 0:
                return False
        return True
    
    def normalize_coeffs(coeffs):
        """Reduce coefficients to smallest integers."""
        g = reduce(gcd, (c for c in coeffs if c > 0), 0)
        if g > 1:
            return tuple(c // g for c in coeffs)
        return coeffs
    
    # Brute force coefficient search
    # Only search for reasonable number of compounds
    if n_compounds <= 6:
        # Search all coefficient combinations
        for coeffs in cartesian_product(range(1, max_coeff + 1), repeat=n_compounds):
            if check_balance(coeffs):
                norm_coeffs = normalize_coeffs(coeffs)
                reactant_coeffs = norm_coeffs[:n_reactants]
                product_coeffs = norm_coeffs[n_reactants:]
                
                return {
                    'reactants': list(zip(reactant_formulas, reactant_coeffs)),
                    'products': list(zip(product_formulas, product_coeffs))
                }
    
    return None


def molecular_to_ionic(molecular_eq, solubility_rules=None):
    """
    Convert molecular equation to complete ionic equation.
    
    Parameters:
        molecular_eq: dict with 'reactants' and 'products' lists of (formula, coeff, state)
                      state should be 'aq', 's', 'l', or 'g'
        solubility_rules: optional dict mapping ions to solubility (True = soluble)
                          If None, uses basic rules
    
    Returns:
        dict with 'reactants' and 'products' as lists of (ion_formula, coeff, original_compound)
    
    Note: This is a simplified implementation for common ionic compounds.
    """
    # Common solubility rules (simplified)
    if solubility_rules is None:
        solubility_rules = {
            # All Group 1 salts are soluble
            'Na': True, 'K': True, 'Li': True, 'Rb': True, 'Cs': True,
            # All ammonium salts are soluble
            'NH4': True,
            # All nitrates are soluble
            'NO3': True,
            # Most chlorides are soluble (except Ag, Pb, Hg)
            'Cl': True, 'Br': True, 'I': True,
            # Most sulfates are soluble (except Ba, Pb, Ca)
            'SO4': True,
        }
    
    # Common ion pairs for dissociation
    ion_pairs = {
        'NaCl': (['Na+', 'Cl-'], 1, 1),
        'NaOH': (['Na+', 'OH-'], 1, 1),
        'HCl': (['H+', 'Cl-'], 1, 1),
        'H2SO4': (['H+', 'SO4^2-'], 2, 1),
        'Na2SO4': (['Na+', 'SO4^2-'], 2, 1),
        'CaCl2': (['Ca^2+', 'Cl-'], 1, 2),
        'KCl': (['K+', 'Cl-'], 1, 1),
        'KOH': (['K+', 'OH-'], 1, 1),
        'AgNO3': (['Ag+', 'NO3-'], 1, 1),
        'NaNO3': (['Na+', 'NO3-'], 1, 1),
        'Ca(NO3)2': (['Ca^2+', 'NO3-'], 1, 2),
        'BaCl2': (['Ba^2+', 'Cl-'], 1, 2),
        'Na2CO3': (['Na+', 'CO3^2-'], 2, 1),
        'HNO3': (['H+', 'NO3-'], 1, 1),
        'NH4Cl': (['NH4+', 'Cl-'], 1, 1),
        'MgCl2': (['Mg^2+', 'Cl-'], 1, 2),
        'AlCl3': (['Al^3+', 'Cl-'], 1, 3),
    }
    
    result = {'reactants': [], 'products': []}
    
    for side in ['reactants', 'products']:
        for item in molecular_eq.get(side, []):
            if len(item) == 3:
                formula, coeff, state = item
            else:
                formula, coeff = item
                state = 'aq'  # Default to aqueous
            
            if state == 'aq' and formula in ion_pairs:
                ions, n_cation, n_anion = ion_pairs[formula]
                cation, anion = ions
                result[side].append((cation, coeff * n_cation, formula))
                result[side].append((anion, coeff * n_anion, formula))
            else:
                # Keep as molecular (solid, liquid, gas, or insoluble)
                result[side].append((formula, coeff, formula))
    
    return result


def complete_to_net_ionic(complete_ionic_eq):
    """
    Remove spectator ions from complete ionic equation.
    
    Parameters:
        complete_ionic_eq: dict with 'reactants' and 'products' as lists of (ion, coeff, original)
    
    Returns:
        dict with 'reactants' and 'products' as lists of (ion, coeff)
    
    Examples:
        >>> eq = {
        ...     'reactants': [('Ag+', 1, 'AgNO3'), ('Cl-', 1, 'NaCl'), ('Na+', 1, 'NaCl'), ('NO3-', 1, 'AgNO3')],
        ...     'products': [('AgCl', 1, 'AgCl'), ('Na+', 1, 'Na+'), ('NO3-', 1, 'NO3-')]
        ... }
        >>> complete_to_net_ionic(eq)
        {'reactants': [('Ag+', 1), ('Cl-', 1)], 'products': [('AgCl', 1)]}
    """
    # Count ions on each side
    reactant_counts = defaultdict(int)
    product_counts = defaultdict(int)
    
    for ion, coeff, _ in complete_ionic_eq.get('reactants', []):
        reactant_counts[ion] += coeff
    
    for ion, coeff, _ in complete_ionic_eq.get('products', []):
        product_counts[ion] += coeff
    
    # Find spectator ions (appear on both sides with same count)
    all_species = set(reactant_counts.keys()) | set(product_counts.keys())
    spectators = set()
    
    for species in all_species:
        if reactant_counts.get(species, 0) == product_counts.get(species, 0):
            spectators.add(species)
    
    # Build net ionic equation
    net_reactants = []
    net_products = []
    
    for ion, coeff, _ in complete_ionic_eq.get('reactants', []):
        if ion not in spectators:
            net_reactants.append((ion, coeff))
    
    for ion, coeff, _ in complete_ionic_eq.get('products', []):
        if ion not in spectators:
            net_products.append((ion, coeff))
    
    # Remove duplicates by summing coefficients
    def consolidate(species_list):
        consolidated = defaultdict(int)
        for ion, coeff in species_list:
            consolidated[ion] += coeff
        return [(ion, coeff) for ion, coeff in consolidated.items() if coeff > 0]
    
    return {
        'reactants': consolidate(net_reactants),
        'products': consolidate(net_products)
    }


def format_equation(balanced_eq):
    """
    Format a balanced equation dict as a readable string.
    
    Parameters:
        balanced_eq: dict with 'reactants' and 'products' lists
    
    Returns:
        str: formatted equation
    
    Examples:
        >>> format_equation({'reactants': [('H2', 2), ('O2', 1)], 'products': [('H2O', 2)]})
        '2 H2 + O2 -> 2 H2O'
    """
    def format_side(species_list):
        parts = []
        for formula, coeff in species_list:
            if coeff == 1:
                parts.append(formula)
            else:
                parts.append(f"{coeff} {formula}")
        return ' + '.join(parts)
    
    reactants = format_side(balanced_eq.get('reactants', []))
    products = format_side(balanced_eq.get('products', []))
    
    return f"{reactants} → {products}"


def balance_redox_half_reaction(
    reactant_formula,
    reactant_charge,
    product_formula,
    product_charge,
    medium="acidic",
):
    """Balance a one-reactant/one-product redox half-reaction.

    The caller supplies formulas without charge suffixes and integer species
    charges separately. The function balances the conserved redox-active atoms
    first, then H/O and charge with H2O, H+, OH-, and electrons. It returns a
    structured atom/charge audit plus the electron side and count.

    Examples:
        balance_redox_half_reaction("MnO4", -1, "Mn", 2, "acidic")
        balance_redox_half_reaction("MnO4", -1, "MnO2", 0, "basic")
    """
    from fractions import Fraction
    from functools import reduce
    from math import gcd

    medium = str(medium).strip().lower()
    if medium not in {"acidic", "basic"}:
        raise ValueError("medium must be 'acidic' or 'basic'")
    if isinstance(reactant_charge, bool) or not isinstance(reactant_charge, int):
        raise TypeError("reactant_charge must be an integer")
    if isinstance(product_charge, bool) or not isinstance(product_charge, int):
        raise TypeError("product_charge must be an integer")

    reactant_atoms = parse_formula(str(reactant_formula))
    product_atoms = parse_formula(str(product_formula))
    if not reactant_atoms or not product_atoms:
        raise ValueError("reactant_formula and product_formula must contain atoms")

    all_elements = set(reactant_atoms) | set(product_atoms)
    core_elements = sorted(all_elements - {"H", "O"})
    if not core_elements:
        core_elements = sorted(all_elements - {"H"}) or sorted(all_elements)
    ratios = []
    for element in core_elements:
        reactant_count = reactant_atoms.get(element, 0)
        product_count = product_atoms.get(element, 0)
        if reactant_count <= 0 or product_count <= 0:
            raise ValueError(
                f"Element {element} must appear in both the reactant and product"
            )
        ratios.append(Fraction(product_count, reactant_count))
    if any(ratio != ratios[0] for ratio in ratios[1:]):
        raise ValueError("Non-H/O atom ratios are inconsistent between species")

    reactant_coeff = ratios[0].numerator
    product_coeff = ratios[0].denominator
    left = {str(reactant_formula): reactant_coeff}
    right = {str(product_formula): product_coeff}

    def atom_total(side, element):
        return sum(
            coefficient * parse_formula(species).get(element, 0)
            for species, coefficient in side.items()
            if species != "e-"
        )

    oxygen_delta = atom_total(left, "O") - atom_total(right, "O")
    if oxygen_delta > 0:
        right["H2O"] = oxygen_delta
    elif oxygen_delta < 0:
        left["H2O"] = -oxygen_delta

    hydrogen_delta = atom_total(left, "H") - atom_total(right, "H")
    if hydrogen_delta > 0:
        right["H+"] = hydrogen_delta
    elif hydrogen_delta < 0:
        left["H+"] = -hydrogen_delta

    charge_map = {
        str(reactant_formula): reactant_charge,
        str(product_formula): product_charge,
        "H+": 1,
        "OH-": -1,
        "H2O": 0,
        "e-": -1,
    }

    def charge_total(side):
        return sum(
            charge_map[species] * coefficient
            for species, coefficient in side.items()
        )

    charge_delta = charge_total(left) - charge_total(right)
    if charge_delta > 0:
        left["e-"] = charge_delta
    elif charge_delta < 0:
        right["e-"] = -charge_delta

    if medium == "basic":
        if "H+" in left:
            count = left.pop("H+")
            left["H2O"] = left.get("H2O", 0) + count
            right["OH-"] = right.get("OH-", 0) + count
        elif "H+" in right:
            count = right.pop("H+")
            right["H2O"] = right.get("H2O", 0) + count
            left["OH-"] = left.get("OH-", 0) + count

        cancel_water = min(left.get("H2O", 0), right.get("H2O", 0))
        if cancel_water:
            left["H2O"] -= cancel_water
            right["H2O"] -= cancel_water
            if left["H2O"] == 0:
                left.pop("H2O")
            if right["H2O"] == 0:
                right.pop("H2O")

    coefficients = list(left.values()) + list(right.values())
    common = reduce(gcd, coefficients)
    if common > 1:
        left = {species: value // common for species, value in left.items()}
        right = {species: value // common for species, value in right.items()}

    atom_audit = {
        element: {
            "reactants": atom_total(left, element),
            "products": atom_total(right, element),
        }
        for element in sorted(all_elements | {"H", "O"})
    }
    atom_balanced = all(
        counts["reactants"] == counts["products"]
        for counts in atom_audit.values()
    )
    left_charge = charge_total(left)
    right_charge = charge_total(right)
    if not atom_balanced or left_charge != right_charge:
        raise ArithmeticError("Internal half-reaction balance audit failed")

    def display_species(species):
        if species == str(reactant_formula) and reactant_charge:
            magnitude = abs(reactant_charge)
            charge = "+" if reactant_charge > 0 else "-"
            return f"{species}^{magnitude if magnitude != 1 else ''}{charge}"
        if species == str(product_formula) and product_charge:
            magnitude = abs(product_charge)
            charge = "+" if product_charge > 0 else "-"
            return f"{species}^{magnitude if magnitude != 1 else ''}{charge}"
        return species

    def formatted(side):
        parts = []
        for species, coefficient in side.items():
            displayed = display_species(species)
            parts.append(
                displayed if coefficient == 1 else f"{coefficient} {displayed}"
            )
        return " + ".join(parts)

    electron_side = "reactants" if "e-" in left else "products"
    electron_count = left.get("e-", right.get("e-", 0))
    return {
        "medium": medium,
        "equation": f"{formatted(left)} -> {formatted(right)}",
        "reactants": left,
        "products": right,
        "electron_side": electron_side,
        "electron_count": electron_count,
        "atom_balance": atom_audit,
        "net_charge": {"reactants": left_charge, "products": right_charge},
        "balanced": True,
    }


if __name__ == "__main__":
    print("Equation balancing tools - implemented")
    
    # Test parse_formula
    print("\n=== parse_formula tests ===")
    print(f"H2O: {parse_formula('H2O')}")
    print(f"Ca(OH)2: {parse_formula('Ca(OH)2')}")
    print(f"Al2(SO4)3: {parse_formula('Al2(SO4)3')}")
    print(f"Fe2O3: {parse_formula('Fe2O3')}")
    
    # Test check_balance
    print("\n=== check_balance tests ===")
    balanced, counts = check_balance([("H2", 2), ("O2", 1)], [("H2O", 2)])
    print(f"2H2 + O2 -> 2H2O: balanced={balanced}, counts={counts}")
    
    balanced, counts = check_balance([("H2", 1), ("O2", 1)], [("H2O", 1)])
    print(f"H2 + O2 -> H2O: balanced={balanced}, counts={counts}")
    
    # Test balance_by_inspection
    print("\n=== balance_by_inspection tests ===")
    result = balance_by_inspection(["H2", "O2"], ["H2O"])
    print(f"H2 + O2 -> H2O: {format_equation(result) if result else 'Failed'}")
    
    result = balance_by_inspection(["Fe", "O2"], ["Fe2O3"])
    print(f"Fe + O2 -> Fe2O3: {format_equation(result) if result else 'Failed'}")
    
    result = balance_by_inspection(["CH4", "O2"], ["CO2", "H2O"])
    print(f"CH4 + O2 -> CO2 + H2O: {format_equation(result) if result else 'Failed'}")


# MCP Tool Declarations
MCP_TOOLS = [
    {
        "name": "balance_redox_half_reaction",
        "description": "Balance a one-reactant/one-product redox half-reaction in acidic or basic medium and audit atom, charge, and electron counts.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "reactant_formula": {"type": "string", "description": "Reactant formula without charge suffix"},
                "reactant_charge": {"type": "integer", "description": "Integer reactant charge"},
                "product_formula": {"type": "string", "description": "Product formula without charge suffix"},
                "product_charge": {"type": "integer", "description": "Integer product charge"},
                "medium": {"type": "string", "description": "acidic or basic", "default": "acidic"},
            },
            "required": ["reactant_formula", "reactant_charge", "product_formula", "product_charge"]
        }
    },
    {
        "name": "balance_by_inspection",
        "description": "Balance equation using systematic coefficient search.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "reactant_formulas": {"type": "string", "description": "Reactant Formulas"},
                "product_formulas": {"type": "string", "description": "Product Formulas"},
                "max_coeff": {"type": "number", "description": "Max Coeff", "default": 20},
            },
            "required": ["reactant_formulas", "product_formulas"]
        }
    },
    {
        "name": "check_balance",
        "description": "Check if equation is balanced.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "reactants": {"type": "number", "description": "Reactants"},
                "products": {"type": "number", "description": "Products"},
            },
            "required": ["reactants", "products"]
        }
    },
    {
        "name": "complete_to_net_ionic",
        "description": "Remove spectator ions from complete ionic equation.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "complete_ionic_eq": {"type": "number", "description": "Complete Ionic Eq"},
            },
            "required": ["complete_ionic_eq"]
        }
    },
    {
        "name": "count_atoms",
        "description": "Count atoms in a chemical formula with coefficient.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "formula": {"type": "string", "description": "Formula"},
                "coefficient": {"type": "number", "description": "Coefficient", "default": 1},
            },
            "required": ["formula"]
        }
    },
    {
        "name": "format_equation",
        "description": "Format a balanced equation dict as a readable string.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "balanced_eq": {"type": "number", "description": "Balanced Eq"},
            },
            "required": ["balanced_eq"]
        }
    },
    {
        "name": "molecular_to_ionic",
        "description": "Convert molecular equation to complete ionic equation.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "molecular_eq": {"type": "number", "description": "Molecular Eq"},
                "solubility_rules": {"type": "number", "description": "Solubility Rules", "default": None},
            },
            "required": ["molecular_eq"]
        }
    },
    {
        "name": "parse_formula",
        "description": "Parse a chemical formula into element counts.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "formula": {"type": "string", "description": "Formula"},
            },
            "required": ["formula"]
        }
    }
]
