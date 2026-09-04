"""
Calorimetry Tools (L3)
Source: LibreTexts Chemistry 2e Ch05.02

## Solver Instructions (for AI Agent)

When you encounter a calorimetry problem, follow this decision tree:

### Step 1: Identify what is given and what is asked
Extract from the question text:
- Type of calorimeter: "coffee cup" (constant P) vs "bomb calorimeter" (constant V)
- Mass or volume of solution: Look for "g", "mL", "L"
- Specific heat capacity: Often 4.184 J/g·degC for water-based solutions
- Temperature change: DeltaT = T_final - T_initial, often given as "temperature rose by XdegC"
- Calorimeter constant: C_cal in J/degC (for bomb calorimeter)
- Moles of reactant: May need to calculate from mass or MxV

### Step 2: Choose the correct function
| Scenario | Function Call |
|----------|---------------|
| Coffee cup calorimetry (q_rxn) | `coffee_cup_heat_rxn(mass, specific_heat, delta_T)` |
| Calculate molar enthalpy | `enthalpy_per_mole(q_rxn, moles)` |
| Bomb calorimetry (q_rxn) | `bomb_calorimeter_heat(C_cal, delta_T)` |
| Calculate calorimeter constant | `calorimeter_constant(q_known, delta_T)` |
| Convert DeltaU to DeltaH (gases) | `delta_H_from_delta_U(delta_U, delta_n_gas, T)` |
| Convert DeltaH to DeltaU (gases) | `delta_U_from_delta_H(delta_H, delta_n_gas, T)` |
| Mixing final temperature | `mixing_final_T(m1, c1, T1, m2, c2, T2)` |

### Step 3: Handle special cases
- **Sign convention**: q_rxn is negative for exothermic, positive for endothermic
- **Coffee cup vs bomb**: Coffee cup gives DeltaH (constant P), bomb gives DeltaU (constant V)
- **DeltaU vs DeltaH**: For reactions with gas, DeltaH = DeltaU + Deltan_gas x R x T
- **Moles calculation**: moles = mass/M, or moles = Molarity x Volume(L)
- **Specific heat**: Default 4.184 J/g·degC for water; may differ for other solutions

### Examples

**Example 1: Coffee cup calorimetry**
Question: "When 0.050 mol HCl reacts with excess NaOH in 100 g solution, temperature rises by 2.5degC. Calculate DeltaH per mole."
- Given: mass = 100 g, c = 4.184 J/g·degC, DeltaT = 2.5degC, n = 0.050 mol
- Solution:
  - `q_rxn = coffee_cup_heat_rxn(mass=100, specific_heat=4.184, delta_T=2.5)` -> -1046 J
  - `enthalpy_per_mole(q_rxn=-1046, moles=0.050)` -> -20.9 kJ/mol

**Example 2: Bomb calorimetry**
Question: "A reaction in a bomb calorimeter (C_cal = 7.85 kJ/degC) causes DeltaT = 2.17degC. What is q_rxn?"
- Given: C_cal = 7850 J/degC, DeltaT = 2.17degC
- Solution: `bomb_calorimeter_heat(C_cal=7850, delta_T=2.17)` -> -17.0 kJ

**Example 3: Mixing problem**
Question: "What is the final temperature when 50 g of water at 80degC mixes with 100 g at 20degC?"
- Given: m1=50, c1=4.184, T1=80, m2=100, c2=4.184, T2=20
- Solution: `mixing_final_T(m1=50, c1=4.184, T1=80, m2=100, c2=4.184, T2=20)` -> 40degC
"""

# === COFFEE CUP CALORIMETRY (constant pressure) ===

def coffee_cup_heat_rxn(specific_heat, delta_T, mass_solution=None, density=1.0, volume_mL=None):
    """
    Calculate heat of reaction from coffee cup calorimetry.
    
    q_rxn = -m x c x DeltaT
    
    Parameters:
        specific_heat: specific heat of solution (e.g., 4.184 J/g·degC for water)
        delta_T: temperature change (T_final - T_initial)
        mass_solution: mass of solution in grams. Provide this OR volume_mL.
        density: solution density in g/mL (default 1.0)
        volume_mL: volume in mL (alternative to mass; mass = volume_mL * density)
    
    Returns:
        q_rxn: heat of reaction in joules
    
    Examples:
        >>> coffee_cup_heat_rxn(4.184, 6.7, volume_mL=100.0)
        -2803.28
    """
    if mass_solution is None:
        if volume_mL is None:
            raise ValueError("Provide either mass_solution or volume_mL")
        mass_solution = volume_mL * density
    elif volume_mL is not None:
        mass_solution = volume_mL * density
    
    q_solution = mass_solution * specific_heat * delta_T
    return -q_solution


def enthalpy_per_mole(q_rxn, moles):
    """
    Calculate molar enthalpy change.
    
    DeltaH = q_rxn / n
    
    Parameters:
        q_rxn: heat of reaction in J
        moles: moles of limiting reactant (NOT volume!)
    
    Returns:
        DeltaH in kJ/mol
    """
    if moles <= 0:
        raise ValueError("Moles must be positive. "
                         "Pass moles of limiting reactant (mol), NOT volume (mL/L). "
                         "Use moles_from_molarity(M, V_L) to convert first.")
    return q_rxn / moles / 1000  # Convert J to kJ


def coffee_cup_delta_H(volume_mL, molarity, specific_heat, delta_T, density=1.0):
    """
    Complete coffee cup calorimetry: calculate DeltaH per mole of reaction.
    
    Correctly computes:
    1. q = -mass * c * delta_T  (heat absorbed by solution)
    2. n = M * V  (moles of limiting reactant)
    3. DeltaH = q / n  (per mole)
    
    Parameters:
        volume_mL: total solution volume in mL
        molarity: molarity of limiting reactant in mol/L
        specific_heat: specific heat in J/(g·°C) (water = 4.184)
        delta_T: temperature change (T_final - T_initial) in °C
        density: solution density in g/mL (default 1.0)
    
    Returns:
        DeltaH in kJ/mol
    
    Note:
        DeltaH is per MOLE of limiting reactant, NOT per mL of solution.
        Common mistake: dividing by volume instead of moles.
    """
    q = coffee_cup_heat_rxn(0, specific_heat, delta_T, density, volume_mL)
    moles = moles_from_molarity(molarity, volume_mL / 1000.0)
    return enthalpy_per_mole(q, moles)


def moles_from_molarity(M, V_L):
    """
    Calculate moles from molarity and volume.
    
    n = M x V
    
    Parameters:
        M: molarity in mol/L
        V_L: volume in liters
    
    Returns:
        moles
    """
    return M * V_L


# === BOMB CALORIMETRY (constant volume) ===

def bomb_calorimeter_heat(C_cal, delta_T):
    """
    Calculate heat from bomb calorimeter data.
    
    q_cal = C_cal x DeltaT
    q_rxn = -q_cal
    
    Parameters:
        C_cal: calorimeter constant in J/degC
        delta_T: temperature change in degC
    
    Returns:
        q_rxn: heat of reaction in joules
    """
    q_cal = C_cal * delta_T
    return -q_cal


def calorimeter_constant(q_known, delta_T):
    """
    Calculate calorimeter constant from known reaction.
    
    C_cal = q_known / DeltaT
    
    Parameters:
        q_known: known heat of reaction in J
        delta_T: measured temperature change in degC
    
    Returns:
        C_cal: calorimeter constant in J/degC
    """
    if delta_T == 0:
        raise ValueError("Temperature change cannot be zero")
    return abs(q_known) / abs(delta_T)


# === DeltaH vs DeltaU RELATIONSHIP ===

def delta_H_from_delta_U(delta_U, delta_n_gas, T=298):
    """
    Convert internal energy change to enthalpy change.
    
    DeltaH = DeltaU + Deltan_gas x R x T
    
    Parameters:
        delta_U: internal energy change in J
        delta_n_gas: change in moles of gas (products - reactants)
        T: temperature in K (default 298 K)
    
    Returns:
        DeltaH in joules
    """
    R = 8.314  # J/(mol·K)
    return delta_U + delta_n_gas * R * T


def delta_U_from_delta_H(delta_H, delta_n_gas, T=298):
    """
    Convert enthalpy change to internal energy change.
    
    DeltaU = DeltaH - Deltan_gas x R x T
    
    Parameters:
        delta_H: enthalpy change in J
        delta_n_gas: change in moles of gas
        T: temperature in K
    
    Returns:
        DeltaU in joules
    """
    R = 8.314
    return delta_H - delta_n_gas * R * T


# === MIXING PROBLEMS ===

def mixing_final_T(m1, c1, T1, m2, c2, T2):
    """
    Calculate final temperature when mixing two substances.
    
    Heat lost = Heat gained
    m1 x c1 x (T_final - T1) + m2 x c2 x (T_final - T2) = 0
    
    Parameters:
        m1, c1, T1: mass, specific heat, initial temp of substance 1
        m2, c2, T2: mass, specific heat, initial temp of substance 2
    
    Returns:
        final temperature in same units as T1, T2
    """
    # Solve: (m1*c1 + m2*c2)*T_f = m1*c1*T1 + m2*c2*T2
    numerator = m1 * c1 * T1 + m2 * c2 * T2
    denominator = m1 * c1 + m2 * c2
    return numerator / denominator


if __name__ == "__main__":
    print("Calorimetry tools - implemented")
    
    # Test coffee cup calorimetry
    q = coffee_cup_heat_rxn(100.0, 4.184, 2.5)
    print(f"Heat of reaction (100g water, DeltaT=2.5degC): {q:.1f} J")
    
    # Test enthalpy per mole
    delta_H = enthalpy_per_mole(-1046, 0.0050)
    print(f"DeltaH per mole: {delta_H:.1f} kJ/mol")
    
    # Test mixing problem
    T_final = mixing_final_T(50, 4.184, 80, 100, 4.184, 20)
    print(f"Final temp (mixing 50g at 80degC with 100g at 20degC): {T_final:.1f}degC")


# MCP Tool Declarations
MCP_TOOLS = [
    {'name': 'bomb_calorimeter_heat', 'description': 'Calculate heat from bomb calorimeter data.\n\nq_cal = C_cal x DeltaT\nq_rxn = -q_cal\n\nParameters:\n    C_cal: calorimeter constant in J/degC\n    delta_T: temperature change in degC\n\nReturns:\n    q_rxn: heat of reaction in joules', 'inputSchema': {'type': 'object', 'properties': {'C_cal': {'type': 'number', 'description': 'C Cal'}, 'delta_T': {'type': 'number', 'description': 'Delta T'}}, 'required': ['C_cal', 'delta_T']}},
    {'name': 'calorimeter_constant', 'description': 'Calculate calorimeter constant from known reaction.\n\nC_cal = q_known / DeltaT\n\nParameters:\n    q_known: known heat of reaction in J\n    delta_T: measured temperature change in degC\n\nReturns:\n    C_cal: calorimeter constant in J/degC', 'inputSchema': {'type': 'object', 'properties': {'q_known': {'type': 'number', 'description': 'Q Known'}, 'delta_T': {'type': 'number', 'description': 'Delta T'}}, 'required': ['q_known', 'delta_T']}},
    {'name': 'coffee_cup_heat_rxn', 'description': 'Calculate heat of reaction from coffee cup calorimetry.\n\nq_rxn = -m x c x DeltaT\n\nParameters:\n    mass_solution: mass of solution in grams (or use volume + density)\n    specific_heat: specific heat of solution (default water: 4.184 J/g·degC)\n    delta_T: temperature change (T_final - T_initial)\n    density: solution density in g/mL (default 1.0)\n    volume_mL: volume in mL (alternative to mass)\n\nReturns:\n    q_rxn: heat of reaction in joules', 'inputSchema': {'type': 'object', 'properties': {'mass_solution': {'type': 'string', 'description': 'Mass Solution'}, 'specific_heat': {'type': 'number', 'description': 'Specific Heat'}, 'delta_T': {'type': 'number', 'description': 'Delta T'}, 'density': {'type': 'number', 'description': 'Density', 'default': 1.0}, 'volume_mL': {'type': 'number', 'description': 'Volume Ml', 'default': None}}, 'required': ['mass_solution', 'specific_heat', 'delta_T']}},
    {'name': 'delta_H_from_delta_U', 'description': 'Convert internal energy change to enthalpy change.\n\nDeltaH = DeltaU + Deltan_gas x R x T\n\nParameters:\n    delta_U: internal energy change in J\n    delta_n_gas: change in moles of gas (products - reactants)\n    T: temperature in K (default 298 K)\n\nReturns:\n    DeltaH in joules', 'inputSchema': {'type': 'object', 'properties': {'delta_U': {'type': 'number', 'description': 'Delta U'}, 'delta_n_gas': {'type': 'number', 'description': 'Delta N Gas'}, 'T': {'type': 'number', 'description': 'T', 'default': 298}}, 'required': ['delta_U', 'delta_n_gas']}},
    {'name': 'delta_U_from_delta_H', 'description': 'Convert enthalpy change to internal energy change.\n\nDeltaU = DeltaH - Deltan_gas x R x T\n\nParameters:\n    delta_H: enthalpy change in J\n    delta_n_gas: change in moles of gas\n    T: temperature in K\n\nReturns:\n    DeltaU in joules', 'inputSchema': {'type': 'object', 'properties': {'delta_H': {'type': 'number', 'description': 'Delta H'}, 'delta_n_gas': {'type': 'number', 'description': 'Delta N Gas'}, 'T': {'type': 'number', 'description': 'T', 'default': 298}}, 'required': ['delta_H', 'delta_n_gas']}},
    {'name': 'enthalpy_per_mole', 'description': 'Calculate molar enthalpy change.\n\nDeltaH = q_rxn / n\n\nParameters:\n    q_rxn: heat of reaction in J\n    moles: moles of limiting reactant\n\nReturns:\n    DeltaH in kJ/mol', 'inputSchema': {'type': 'object', 'properties': {'q_rxn': {'type': 'number', 'description': 'Q Rxn'}, 'moles': {'type': 'number', 'description': 'Moles'}}, 'required': ['q_rxn', 'moles']}},
    {'name': 'mixing_final_T', 'description': 'Calculate final temperature when mixing two substances.\n\nHeat lost = Heat gained\nm1 x c1 x (T_final - T1) + m2 x c2 x (T_final - T2) = 0\n\nParameters:\n    m1, c1, T1: mass, specific heat, initial temp of substance 1\n    m2, c2, T2: mass, specific heat, initial temp of substance 2\n\nReturns:\n    final temperature in same units as T1, T2', 'inputSchema': {'type': 'object', 'properties': {'m1': {'type': 'number', 'description': 'M1'}, 'c1': {'type': 'number', 'description': 'C1'}, 'T1': {'type': 'number', 'description': 'T1'}, 'm2': {'type': 'number', 'description': 'M2'}, 'c2': {'type': 'number', 'description': 'C2'}, 'T2': {'type': 'number', 'description': 'T2'}}, 'required': ['m1', 'c1', 'T1', 'm2', 'c2', 'T2']}},
    {'name': 'moles_from_molarity', 'description': 'Calculate moles from molarity and volume.\n\nn = M x V\n\nParameters:\n    M: molarity in mol/L\n    V_L: volume in liters\n\nReturns:\n    moles', 'inputSchema': {'type': 'object', 'properties': {'M': {'type': 'number', 'description': 'M'}, 'V_L': {'type': 'number', 'description': 'V L'}}, 'required': ['M', 'V_L']}}
]
