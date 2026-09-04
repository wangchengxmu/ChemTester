"""
Limiting Reactant and Yield Tools (L3)
Source: LibreTexts Chemistry 2e Ch04.04

## Solver Instructions (for AI Agent)

When you encounter a limiting reactant or yield problem, follow this decision tree:

### Step 1: Identify what is given and what is asked
Extract from the question text:
- Amounts of reactants: Look for masses or moles of each reactant given
- Balanced equation: Extract coefficients for all reactants and products
- What's asked: "limiting reactant", "theoretical yield", "percent yield", "excess remaining", "atom economy"
- Actual yield: Given if calculating percent yield

### Step 2: Choose the correct function
| Scenario | Function Call |
|----------|---------------|
| Identify limiting reactant (two reactants) | `identify_limiting_by_ratio(mol_A, mol_B, coeff_A, coeff_B)` |
| Identify limiting by product comparison | `identify_limiting_by_product(mol_A, mol_B, coeff_A, coeff_B, coeff_product)` |
| Calculate theoretical yield (moles) | `theoretical_yield_moles(mol_limiting, coeff_limiting, coeff_product)` |
| Calculate theoretical yield (grams) | `theoretical_yield_mass(mol_limiting, coeff_limiting, coeff_product, M_product)` |
| Calculate percent yield | `percent_yield(actual_yield, theoretical_yield)` |
| Find excess reactant remaining | `excess_remaining_moles(mol_excess_init, mol_limiting, coeff_excess, coeff_limiting)` |
| Calculate atom economy | `atom_economy(M_product, [M_reactant1, M_reactant2, ...])` |

### Step 3: Handle special cases
- **Convert mass to moles first**: If masses given, calculate moles using M = mass/molar_mass before using limiting reactant functions
- **Identifying A vs B**: Assign reactants as A and B consistently; function returns 'A' or 'B'
- **Theoretical yield**: Always based on limiting reactant - identify it first!
- **Percent yield**: Both actual and theoretical must be in same units (both in g or both in mol)
- **Excess remaining**: First identify which reactant is in excess (not the limiting one)
- **Multi-reactant problems**: For 3+ reactants, compare each pair or use product method

### Examples

**Example 1: Identify limiting reactant**
Question: "For 3Si + 2N2 -> Si3N4, if you have 2.00 g Si (28.09 g/mol) and 1.50 g N2 (28.02 g/mol), which is limiting?"
- Step 1: Convert to moles: mol_Si = 2.00/28.09 = 0.0712 mol, mol_N2 = 1.50/28.02 = 0.0535 mol
- Solution: `identify_limiting_by_ratio(mol_A=0.0712, mol_B=0.0535, coeff_A=3, coeff_B=2)` -> 'A' (Si is limiting)

**Example 2: Theoretical yield**
Question: "What mass of Si3N4 forms if Si is limiting? (M = 140.3 g/mol)"
- Given: mol_limiting = 0.0712 mol Si, coeff_Si = 3, coeff_product = 1
- Solution: `theoretical_yield_mass(mol_limiting=0.0712, coeff_limiting=3, coeff_product=1, molar_mass_product=140.3)` -> 3.33 g

**Example 3: Percent yield**
Question: "If 2.58 g of product was actually obtained, what is the percent yield?"
- Given: actual = 2.58 g, theoretical = 3.33 g
- Solution: `percent_yield(actual_yield=2.58, theoretical_yield=3.33)` -> 77.5%

**Example 4: Excess remaining**
Question: "How much N2 remains after the reaction?"
- Given: mol_N2_initial = 0.0535 mol, mol_Si_limiting = 0.0712 mol, coeff_N2 = 2, coeff_Si = 3
- Solution: `excess_remaining_moles(mol_excess_initial=0.0535, mol_limiting=0.0712, coeff_excess=2, coeff_limiting=3)` -> 0.0061 mol N2 remaining
"""


def identify_limiting_by_ratio(mol_A, mol_B, coeff_A, coeff_B):
    """
    Identify limiting reactant using ratio comparison method.
    
    provided_ratio = mol_A / mol_B
    stoichiometric_ratio = coeff_A / coeff_B
    
    If provided_ratio < stoichiometric_ratio -> A is limiting
    If provided_ratio > stoichiometric_ratio -> B is limiting
    
    Parameters:
        mol_A: moles of reactant A (float)
        mol_B: moles of reactant B (float)
        coeff_A: coefficient of A in balanced equation
        coeff_B: coefficient of B in balanced equation
    
    Returns:
        str: 'A' if A is limiting, 'B' if B is limiting
    
    Raises:
        ValueError: if mol_B or coeff_B is zero
    """
    if mol_B == 0:
        raise ValueError("Moles of B cannot be zero for ratio comparison")
    if coeff_B == 0:
        raise ValueError("Coefficient B cannot be zero")
    
    provided_ratio = mol_A / mol_B
    stoichiometric_ratio = coeff_A / coeff_B
    
    if provided_ratio < stoichiometric_ratio:
        return 'A'
    else:
        return 'B'


def identify_limiting_by_product(mol_A, mol_B, coeff_A, coeff_B, coeff_product):
    """
    Identify limiting reactant by comparing product amounts.
    
    mol_product_from_A = mol_A x (coeff_product / coeff_A)
    mol_product_from_B = mol_B x (coeff_product / coeff_B)
    
    Limiting = reactant giving lesser product amount
    
    Parameters:
        mol_A: moles of reactant A (float)
        mol_B: moles of reactant B (float)
        coeff_A: coefficient of A in balanced equation
        coeff_B: coefficient of B in balanced equation
        coeff_product: coefficient of product in balanced equation
    
    Returns:
        str: 'A' or 'B' (whichever gives lesser product)
    
    Raises:
        ValueError: if coefficients are zero
    """
    if coeff_A == 0 or coeff_B == 0:
        raise ValueError("Coefficients cannot be zero")
    
    mol_product_from_A = mol_A * (coeff_product / coeff_A)
    mol_product_from_B = mol_B * (coeff_product / coeff_B)
    
    if mol_product_from_A < mol_product_from_B:
        return 'A'
    else:
        return 'B'


def theoretical_yield_moles(mol_limiting, coeff_limiting, coeff_product):
    """
    Calculate theoretical yield in moles.
    
    mol_product = mol_limiting x (coeff_product / coeff_limiting)
    
    Parameters:
        mol_limiting: moles of limiting reactant
        coeff_limiting: coefficient of limiting reactant
        coeff_product: coefficient of product
    
    Returns:
        theoretical yield in moles (float)
    """
    if coeff_limiting == 0:
        raise ValueError("Coefficient cannot be zero")
    return mol_limiting * (coeff_product / coeff_limiting)


def theoretical_yield_mass(mol_limiting, coeff_limiting, coeff_product, molar_mass_product):
    """
    Calculate theoretical yield in grams.
    
    theoretical = mol_limiting x (coeff_product/coeff_limiting) x M_product
    
    Parameters:
        mol_limiting: moles of limiting reactant
        coeff_limiting: coefficient of limiting reactant
        coeff_product: coefficient of product
        molar_mass_product: molar mass of product in g/mol
    
    Returns:
        theoretical yield in grams (float)
    """
    mol_product = theoretical_yield_moles(mol_limiting, coeff_limiting, coeff_product)
    return mol_product * molar_mass_product


def percent_yield(actual_yield, theoretical_yield):
    """
    Calculate percent yield.
    
    percent = (actual / theoretical) x 100%
    
    Parameters:
        actual_yield: actual amount obtained (any unit)
        theoretical_yield: theoretical maximum (same unit)
    
    Returns:
        percent yield (float, 0-100+)
    
    Raises:
        ValueError: if theoretical_yield is zero or negative
    """
    if theoretical_yield <= 0:
        raise ValueError("Theoretical yield must be positive")
    return (actual_yield / theoretical_yield) * 100.0


def excess_remaining_moles(mol_excess_initial, mol_limiting, coeff_excess, coeff_limiting):
    """
    Calculate amount of excess reactant remaining (in moles).
    
    consumed = mol_limiting x (coeff_excess / coeff_limiting)
    remaining = initial - consumed
    
    Parameters:
        mol_excess_initial: initial moles of excess reactant
        mol_limiting: moles of limiting reactant
        coeff_excess: coefficient of excess reactant
        coeff_limiting: coefficient of limiting reactant
    
    Returns:
        moles of excess reactant remaining (float)
    """
    if coeff_limiting == 0:
        raise ValueError("Coefficient of limiting reactant cannot be zero")
    
    consumed = mol_limiting * (coeff_excess / coeff_limiting)
    return mol_excess_initial - consumed


def atom_economy(molar_mass_product, molar_masses_reactants):
    """
    Calculate atom economy (green chemistry metric).
    
    atom_economy = (M_product / sum(M_reactants)) x 100%
    
    Parameters:
        molar_mass_product: molar mass of desired product (g/mol)
        molar_masses_reactants: list of molar masses of all reactants (g/mol)
    
    Returns:
        atom economy percentage (float, 0-100)
    
    Raises:
        ValueError: if sum of reactant masses is zero
    """
    total_reactants = sum(molar_masses_reactants)
    if total_reactants <= 0:
        raise ValueError("Total reactant mass must be positive")
    return (molar_mass_product / total_reactants) * 100.0


if __name__ == "__main__":
    print("Limiting reactant tools - implemented")
    
    # Test: Si + N2 -> Si3N4
    # 3 Si + 2 N2 -> Si3N4
    # 2.00 g Si (28.09 g/mol) and 1.50 g N2 (28.02 g/mol)
    mol_Si = 2.00 / 28.09  # 0.0712 mol
    mol_N2 = 1.50 / 28.02  # 0.0535 mol
    
    limiting = identify_limiting_by_ratio(mol_Si, mol_N2, coeff_A=3, coeff_B=2)
    print(f"Test 1: Limiting reactant is {limiting} (expected: A/Si)")
    
    limiting2 = identify_limiting_by_product(mol_Si, mol_N2, coeff_A=3, coeff_B=2, coeff_product=1)
    print(f"Test 2 (product method): Limiting reactant is {limiting2} (expected: A/Si)")
    
    # Test: Percent yield
    # 1.274 g CuSO4 -> 0.392 g Cu actual, theoretical 0.5072 g
    percent = percent_yield(0.392, 0.5072)
    print(f"Test 3: Percent yield = {percent:.1f}% (expected: 77.3%)")

MCP_TOOLS = [
    {
        "name": "atom_economy",
        "description": "Calculate atom economy (green chemistry metric).",
        "parameters": [
            {
                "name": "molar_mass_product",
                "type": "number"
            },
            {
                "name": "molar_masses_reactants",
                "type": "number"
            }
        ]
    },
    {
        "name": "excess_remaining_moles",
        "description": "Calculate amount of excess reactant remaining (in moles).",
        "parameters": [
            {
                "name": "mol_excess_initial",
                "type": "number"
            },
            {
                "name": "mol_limiting",
                "type": "number"
            },
            {
                "name": "coeff_excess",
                "type": "number"
            },
            {
                "name": "coeff_limiting",
                "type": "number"
            }
        ]
    },
    {
        "name": "identify_limiting_by_product",
        "description": "Identify limiting reactant by comparing product amounts.",
        "parameters": [
            {
                "name": "mol_A",
                "type": "number"
            },
            {
                "name": "mol_B",
                "type": "number"
            },
            {
                "name": "coeff_A",
                "type": "number"
            },
            {
                "name": "coeff_B",
                "type": "number"
            },
            {
                "name": "coeff_product",
                "type": "number"
            }
        ]
    },
    {
        "name": "identify_limiting_by_ratio",
        "description": "Identify limiting reactant using ratio comparison method.",
        "parameters": [
            {
                "name": "mol_A",
                "type": "number"
            },
            {
                "name": "mol_B",
                "type": "number"
            },
            {
                "name": "coeff_A",
                "type": "number"
            },
            {
                "name": "coeff_B",
                "type": "number"
            }
        ]
    },
    {
        "name": "percent_yield",
        "description": "Calculate percent yield.",
        "parameters": [
            {
                "name": "actual_yield",
                "type": "number"
            },
            {
                "name": "theoretical_yield",
                "type": "number"
            }
        ]
    },
    {
        "name": "theoretical_yield_mass",
        "description": "Calculate theoretical yield in grams.",
        "parameters": [
            {
                "name": "mol_limiting",
                "type": "number"
            },
            {
                "name": "coeff_limiting",
                "type": "number"
            },
            {
                "name": "coeff_product",
                "type": "number"
            },
            {
                "name": "molar_mass_product",
                "type": "number"
            }
        ]
    },
    {
        "name": "theoretical_yield_moles",
        "description": "Calculate theoretical yield in moles.",
        "parameters": [
            {
                "name": "mol_limiting",
                "type": "number"
            },
            {
                "name": "coeff_limiting",
                "type": "number"
            },
            {
                "name": "coeff_product",
                "type": "number"
            }
        ]
    }
]
