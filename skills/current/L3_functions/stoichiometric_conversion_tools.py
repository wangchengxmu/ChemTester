"""
Stoichiometric Conversion Tools (L3)
Source: LibreTexts Chemistry 2e Ch04.03

## Solver Instructions (for AI Agent)

When you encounter a stoichiometric conversion problem, follow this decision tree:

### Step 1: Identify what is given and what is asked
Extract from the question text:
- Balanced chemical equation: Look for reaction (e.g., "2H2 + O2 -> 2H2O") - extract coefficients
- Mass of substance: Look for "g", "kg", "mg" - convert to grams if needed
- Moles of substance: Look for "mol"
- Molar mass (M): Often need to calculate from chemical formula (e.g., NaCl = 23.0 + 35.5 = 58.5 g/mol)
- Volume of solution: Look for "L", "mL" - convert to L (1 L = 1000 mL)
- Molarity: Look for "M", "mol/L"
- Particles: Look for "molecules", "atoms", "formula units", often with scientific notation

### Step 2: Choose the correct function
| Scenario | Function Call |
|----------|---------------|
| Convert moles A -> moles B (same reaction) | `mole_to_mole(mol_A, coeff_A, coeff_B)` |
| Convert mass -> moles | `mass_to_moles(mass, molar_mass)` |
| Convert moles -> mass | `moles_to_mass(mol, molar_mass)` |
| Convert mass A -> mass B (full stoichiometry) | `mass_to_mass(mass_A, M_A, M_B, coeff_A, coeff_B)` |
| Convert moles -> particles | `moles_to_particles(mol)` |
| Convert particles -> moles | `particles_to_moles(particles)` |
| Find moles from M x V | `solution_moles(molarity, volume_L)` |
| Find molarity from mol/V | `solution_molarity(mol, volume_L)` |

### Step 3: Handle special cases
- **Multi-step conversions**: Often need to chain functions: mass A -> mol A -> mol B -> mass B
  - Step 1: `mol_A = mass_to_moles(mass_A, M_A)`
  - Step 2: `mol_B = mole_to_mole(mol_A, coeff_A, coeff_B)`
  - Step 3: `mass_B = moles_to_mass(mol_B, M_B)`
  - OR use `mass_to_mass()` for one-step calculation
- **Molar mass calculation**: Extract formula from question, calculate M from periodic table
- **Unit conversions**: kg -> g (x1000), mL -> L (/1000), mmol -> mol (/1000)
- **Solution stoichiometry**: First get moles from M x V, then use mole ratios
- **Identify A and B**: A is what you're given, B is what you need to find

### Examples

**Example 1: Mole-to-mole conversion**
Question: "How many moles of I2 are needed to react with 0.429 mol Al? (2Al + 3I2 -> 2AlI3)"
- Given: mol_A = 0.429 mol Al, coeff_A = 2, coeff_B = 3
- Solution: `mole_to_mole(mol_A=0.429, coeff_A=2, coeff_B=3)` -> 0.644 mol I2

**Example 2: Mass-to-mass conversion**
Question: "What mass of NaOH is needed to produce 16.0 g Mg(OH)2? (MgCl2 + 2NaOH -> Mg(OH)2 + 2NaCl)"
- Given: mass_A = 16.0 g Mg(OH)2, M_A = 58.3 g/mol, M_B = 40.0 g/mol, coeff_A = 1, coeff_B = 2
- Solution: `mass_to_mass(mass_A=16.0, molar_mass_A=58.3, molar_mass_B=40.0, coeff_A=1, coeff_B=2)` -> 22 g NaOH

**Example 3: Solution stoichiometry**
Question: "What volume of 0.150 M HCl reacts with 0.0250 mol NaOH? (HCl + NaOH -> NaCl + H2O)"
- Given: mol_NaOH = 0.0250, coeff_HCl = 1, coeff_NaOH = 1, M_HCl = 0.150 mol/L
- Solution: 
  - `mol_HCl = mole_to_mole(mol_A=0.0250, coeff_A=1, coeff_B=1)` -> 0.0250 mol
  - `V = solution_moles(molarity=0.150, volume_L=?)` or solve V = mol/M = 0.167 L

**Example 4: Particles conversion**
Question: "How many molecules are in 2.5 moles of H2O?"
- Given: mol = 2.5
- Solution: `moles_to_particles(mol=2.5)` -> 1.51 x 1024 molecules
"""

AVOGADRO = 6.022e23

def mole_to_mole(mol_A, coeff_A, coeff_B):
    """
    Convert moles of substance A to moles of substance B.
    
    mol_B = mol_A x (coeff_B / coeff_A)
    
    Parameters:
        mol_A: moles of reactant/product A (float)
        coeff_A: coefficient of A in balanced equation (int or float)
        coeff_B: coefficient of B in balanced equation (int or float)
    
    Returns:
        mol_B: moles of reactant/product B (float)
    
    Raises:
        ValueError: if coeff_A is zero
    """
    if coeff_A == 0:
        raise ValueError("Coefficient cannot be zero")
    return mol_A * (coeff_B / coeff_A)


def mass_to_moles(mass, molar_mass):
    """
    Convert mass to moles.
    
    mol = mass / molar_mass
    
    Parameters:
        mass: mass in grams (float)
        molar_mass: molar mass in g/mol (float)
    
    Returns:
        moles (float)
    
    Raises:
        ValueError: if molar_mass is zero or negative
    """
    if molar_mass <= 0:
        raise ValueError("Molar mass must be positive")
    return mass / molar_mass


def moles_to_mass(mol, molar_mass):
    """
    Convert moles to mass.
    
    mass = mol x molar_mass
    
    Parameters:
        mol: amount in moles (float)
        molar_mass: molar mass in g/mol (float)
    
    Returns:
        mass in grams (float)
    """
    return mol * molar_mass


def mass_to_mass(mass_A, molar_mass_A, molar_mass_B, coeff_A, coeff_B):
    """
    Convert mass of substance A to mass of substance B.
    
    mass_B = mass_A x (1/M_A) x (coeff_B/coeff_A) x M_B
    
    Parameters:
        mass_A: mass of A in grams (float)
        molar_mass_A: molar mass of A in g/mol (float)
        molar_mass_B: molar mass of B in g/mol (float)
        coeff_A: coefficient of A in balanced equation
        coeff_B: coefficient of B in balanced equation
    
    Returns:
        mass_B: mass of B in grams (float)
    
    Raises:
        ValueError: if molar_mass_A or coeff_A is zero/negative
    """
    if molar_mass_A <= 0:
        raise ValueError("Molar mass A must be positive")
    if coeff_A == 0:
        raise ValueError("Coefficient A cannot be zero")
    
    mol_A = mass_to_moles(mass_A, molar_mass_A)
    mol_B = mole_to_mole(mol_A, coeff_A, coeff_B)
    mass_B = moles_to_mass(mol_B, molar_mass_B)
    return mass_B


def moles_to_particles(mol):
    """
    Convert moles to number of particles using Avogadro's number.
    
    particles = mol x 6.022 x 10^23
    
    Parameters:
        mol: amount in moles (float)
    
    Returns:
        number of particles (float)
    """
    return mol * AVOGADRO


def particles_to_moles(particles):
    """
    Convert number of particles to moles using Avogadro's number.
    
    mol = particles / 6.022 x 10^23
    
    Parameters:
        particles: number of particles (float)
    
    Returns:
        amount in moles (float)
    """
    return particles / AVOGADRO


def solution_moles(molarity, volume_L):
    """
    Calculate moles from solution molarity and volume.
    
    mol = M x V
    
    Parameters:
        molarity: concentration in mol/L (float)
        volume_L: volume in liters (float)
    
    Returns:
        moles of solute (float)
    
    Raises:
        ValueError: if molarity is negative
    """
    if molarity < 0:
        raise ValueError("Molarity cannot be negative")
    return molarity * volume_L


def solution_molarity(mol, volume_L):
    """
    Calculate molarity from moles and volume.
    
    M = mol / V
    
    Parameters:
        mol: moles of solute (float)
        volume_L: volume in liters (float)
    
    Returns:
        molarity in mol/L (float)
    
    Raises:
        ValueError: if volume is zero or negative
    """
    if volume_L <= 0:
        raise ValueError("Volume must be positive")
    return mol / volume_L


def ideal_gas_moles(P, V, T, R=0.08206):
    """
    Calculate moles from ideal gas law: n = PV/RT
    
    Args:
        P: Pressure (atm)
        V: Volume (L)
        T: Temperature (K)
        R: Gas constant (default 0.08206 L·atm/(mol·K))
    
    Returns:
        moles (float)
    """
    return P * V / (R * T)


def limiting_reactant(reactants_dict, stoichiometry):
    """
    Identify limiting reactant and theoretical yield.
    
    Args:
        reactants_dict: Dict of {species: moles available}
        stoichiometry: Dict of {species: stoichiometric coefficient}
    
    Returns:
        (limiting_species, theoretical_yield_dict) where theoretical_yield_dict
        contains the moles of each product that can be formed
    
    Examples:
        >>> limiting_reactant({'Na': 1.5, 'Cl2': 1.0}, {'Na': 2, 'Cl2': 1, 'NaCl': 2})
        ('Na', {'NaCl': 1.5})
    """
    # Find which reactant produces least product
    # Assume first non-reactant species is the product
    products = {k: v for k, v in stoichiometry.items() if k not in reactants_dict}
    if not products:
        return list(reactants_dict.keys())[0], {}
    
    target = list(products.keys())[0]
    target_coeff = products[target]
    
    limiting = None
    min_moles_product = float('inf')
    
    for species, moles in reactants_dict.items():
        coeff = stoichiometry[species]
        moles_product = moles * (target_coeff / coeff)
        if moles_product < min_moles_product:
            min_moles_product = moles_product
            limiting = species
    
    # Calculate theoretical yield for all products
    limiting_coeff = stoichiometry[limiting]
    limiting_moles = reactants_dict[limiting]
    theoretical = {}
    for prod, prod_coeff in products.items():
        theoretical[prod] = limiting_moles * (prod_coeff / limiting_coeff)
    
    return limiting, theoretical


def percent_yield(actual, theoretical):
    """
    Calculate percent yield.
    
    Args:
        actual: Actual yield (mass or moles)
        theoretical: Theoretical yield (same units)
    
    Returns:
        Percent yield (float)
    """
    if theoretical == 0:
        raise ValueError("Theoretical yield cannot be zero")
    return (actual / theoretical) * 100


def empirical_formula(percent_composition_dict):
    """
    Determine empirical formula from percent composition.
    
    Args:
        percent_composition_dict: Dict of {element: mass_percent}
    
    Returns:
        Empirical formula string (e.g., 'CH2O')
    
    Examples:
        >>> empirical_formula({'C': 40.0, 'H': 6.7, 'O': 53.3})
        'CH2O'
    """
    from math import gcd
    from functools import reduce
    
    # Atomic masses
    atomic_masses = {
        'H': 1.008, 'He': 4.003, 'Li': 6.941, 'Be': 9.012, 'B': 10.81,
        'C': 12.011, 'N': 14.007, 'O': 15.999, 'F': 18.998, 'Ne': 20.180,
        'Na': 22.990, 'Mg': 24.305, 'Al': 26.982, 'Si': 28.086, 'P': 30.974,
        'S': 32.065, 'Cl': 35.453, 'Ar': 39.948, 'K': 39.098, 'Ca': 40.078,
        'Ti': 47.867, 'V': 50.942, 'Cr': 51.996, 'Mn': 54.938, 'Fe': 55.845,
        'Co': 58.933, 'Ni': 58.693, 'Cu': 63.546, 'Zn': 65.380, 'Ga': 69.723,
        'Ge': 72.630, 'As': 74.922, 'Se': 78.960, 'Br': 79.904, 'Kr': 83.798,
        'Rb': 85.468, 'Sr': 87.620, 'Y': 88.906, 'Zr': 91.224, 'Nb': 92.906,
        'Mo': 95.960, 'Ru': 101.07, 'Rh': 102.91, 'Pd': 106.42, 'Ag': 107.87,
        'Sn': 118.71, 'I': 126.90, 'Xe': 131.29, 'Cs': 132.91, 'Ba': 137.33,
        'La': 138.91, 'Ce': 140.12, 'Pr': 140.91, 'Nd': 144.24, 'Sm': 150.36,
        'Eu': 151.96, 'Gd': 157.25, 'Tb': 158.93, 'Dy': 162.50, 'Ho': 164.93,
        'Er': 167.26, 'Tm': 168.93, 'Yb': 173.04, 'Lu': 174.97, 'Hf': 178.49,
        'Ta': 180.95, 'W': 183.84, 'Re': 186.21, 'Os': 190.23, 'Ir': 192.22,
        'Pt': 195.08, 'Au': 196.97, 'Hg': 200.59, 'Tl': 204.38, 'Pb': 207.2,
        'Bi': 208.98, 'U': 238.03,
    }
    
    # Convert to moles
    moles = {}
    for element, percent in percent_composition_dict.items():
        moles[element] = percent / atomic_masses[element]
    
    # Divide by smallest
    min_moles = min(moles.values())
    ratios = {e: m / min_moles for e, m in moles.items()}
    
    # Round to nearest integer (handle near-integers)
    def round_ratio(r):
        r_rounded = round(r)
        if abs(r - r_rounded) < 0.15:
            return r_rounded
        # Try common multipliers
        for mult in [2, 3, 4]:
            val = round(r * mult)
            if abs(r * mult - val) < 0.15:
                return val  # Return unmultiplied; we'll multiply all later
        return r_rounded
    
    int_ratios = {e: round_ratio(r) for e, r in ratios.items()}
    
    # Check if we need to multiply by common factor
    values = list(int_ratios.values())
    all_ints = all(abs(v - round(v)) < 0.01 for v in values)
    
    if not all_ints:
        # Try multiplying to get integers
        for mult in range(2, 10):
            multiplied = {e: round(r * mult) for e, r in ratios.items()}
            if all(abs(r * mult - round(r * mult)) < 0.15 for e, r in ratios.items()):
                int_ratios = multiplied
                break
    
    int_ratios = {e: round(v) for e, v in int_ratios.items()}
    
    # Divide by GCD
    vals = [v for v in int_ratios.values() if v > 0]
    if vals:
        g = reduce(gcd, vals)
        int_ratios = {e: v // g for e, v in int_ratios.items()}
    
    # Build formula string (order: C, H, then alphabetical)
    order = sorted(int_ratios.keys(), key=lambda x: (x != 'C', x != 'H', x))
    parts = []
    for e in order:
        n = int_ratios[e]
        if n == 1:
            parts.append(e)
        else:
            parts.append(f'{e}{n}')
    
    return ''.join(parts)


def stoichiometric_calculation(given_moles, given_coeff, target_coeff, target_molar_mass):
    """
    Full stoichiometric calculation: moles of given → mass of target.
    
    Args:
        given_moles: Moles of given substance
        given_coeff: Stoichiometric coefficient of given substance
        target_coeff: Stoichiometric coefficient of target substance
        target_molar_mass: Molar mass of target substance (g/mol)
    
    Returns:
        Mass of target substance in grams
    """
    target_moles = mole_to_mole(given_moles, given_coeff, target_coeff)
    return moles_to_mass(target_moles, target_molar_mass)


def moles_from_mass(mass_g, molar_mass):
    """Alias for mass_to_moles."""
    return mass_to_moles(mass_g, molar_mass)


def mass_from_moles(moles, molar_mass):
    """Alias for moles_to_mass."""
    return moles_to_mass(moles, molar_mass)


if __name__ == "__main__":
    # Utility check
    print("Stoichiometric conversion tools - implemented")
    
    # Test: How many moles of I2 needed to react with 0.429 mol Al?
    # 2 Al + 3 I2 -> 2 AlI3
    mol_Al = 0.429
    mol_I2 = mole_to_mole(mol_Al, coeff_A=2, coeff_B=3)
    print(f"Test 1: {mol_Al} mol Al needs {mol_I2:.3f} mol I2 (expected: 0.644)")
    
    # Test: Mass of NaOH needed to produce 16 g Mg(OH)2?
    # MgCl2 + 2 NaOH -> Mg(OH)2 + 2 NaCl
    mass_MgOH2 = 16.0
    M_MgOH2 = 58.3  # g/mol
    M_NaOH = 40.0   # g/mol
    mass_NaOH = mass_to_mass(mass_MgOH2, M_MgOH2, M_NaOH, coeff_A=1, coeff_B=2)
    print(f"Test 2: {mass_MgOH2} g Mg(OH)2 needs {mass_NaOH:.1f} g NaOH (expected: 22 g)")


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="mass_to_mass",
            description="Convert mass of substance A to mass of substance B.",
            input_schema=[
            InputSchemaField(name="mass_A", type="number", required=True),
            InputSchemaField(name="molar_mass_A", type="number", required=True),
            InputSchemaField(name="molar_mass_B", type="number", required=True),
            InputSchemaField(name="coeff_A", type="number", required=True),
            InputSchemaField(name="coeff_B", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="mass_to_moles",
            description="Convert mass to moles.",
            input_schema=[
            InputSchemaField(name="mass", type="number", required=True),
            InputSchemaField(name="molar_mass", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="mole_to_mole",
            description="Convert moles of substance A to moles of substance B.",
            input_schema=[
            InputSchemaField(name="mol_A", type="number", required=True),
            InputSchemaField(name="coeff_A", type="number", required=True),
            InputSchemaField(name="coeff_B", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="moles_to_mass",
            description="Convert moles to mass.",
            input_schema=[
            InputSchemaField(name="mol", type="number", required=True),
            InputSchemaField(name="molar_mass", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="moles_to_particles",
            description="Convert moles to number of particles using Avogadro's number.",
            input_schema=[
            InputSchemaField(name="mol", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="particles_to_moles",
            description="Convert number of particles to moles using Avogadro's number.",
            input_schema=[
            InputSchemaField(name="particles", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="solution_molarity",
            description="Calculate molarity from moles and volume.",
            input_schema=[
            InputSchemaField(name="mol", type="number", required=True),
            InputSchemaField(name="volume_L", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="solution_moles",
            description="Calculate moles from solution molarity and volume.",
            input_schema=[
            InputSchemaField(name="molarity", type="number", required=True),
            InputSchemaField(name="volume_L", type="number", required=True)
            ],
            handler="{name}",
        )
    ]
