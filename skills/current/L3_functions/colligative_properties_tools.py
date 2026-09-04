"""
Colligative Properties Tools - L3 Implementation
Chapter 11.04: Colligative Properties of Solutions

## Solver Instructions (for AI Agent)

When you encounter a colligative properties problem, follow this decision tree:

### Step 1: Identify what is given and what is asked
Extract from the question text:
- Molality (m): mol/kg solvent
- van't Hoff factor (i): Look for electrolyte vs nonelectrolyte (NaCl->i=2, CaCl2->i=3, sugar->i=1)
- Solvent constants: Kb (boiling), Kf (freezing) - water: Kb=0.512, Kf=1.86
- Temperature change: DeltaTb or DeltaTf, or new boiling/freezing point
- Osmotic pressure: Look for Π, M, T
- Molar mass determination: Mass of solute and measured DeltaT

### Step 2: Choose the correct function
| Scenario | Function Call |
|----------|---------------|
| Calculate boiling point elevation | `boiling_point_elevation(m, Kb, i)` |
| Calculate freezing point depression | `freezing_point_depression(m, Kf, i)` |
| Calculate new boiling point | `new_boiling_point(m, Kb, Tb_pure, i)` |
| Calculate new freezing point | `new_freezing_point(m, Kf, Tf_pure, i)` |
| Calculate osmotic pressure | `osmotic_pressure(M, T, i)` |
| Find molar mass from DeltaTf | `molar_mass_from_fp_depression(mass_solute, mass_solvent_kg, delta_T, Kf, i)` |
| Find molar mass from DeltaTb | `molar_mass_from_bp_elevation(mass_solute, mass_solvent_kg, delta_T, Kb, i)` |
| Find molar mass from osmotic pressure | `molar_mass_from_osmotic_pressure(mass_solute, volume_L, Pi, T, i)` |
| Get van't Hoff factor | `vanthoff_factor(formula, actual)` |
| Get solvent constants | `get_solvent_constants(solvent_name)` |
| Calculate vapor pressure lowering | `vapor_pressure_lowering(X_solvent, P0)` |

### Step 3: Handle special cases
- **van't Hoff factor**: Nonelectrolytes i=1; strong electrolytes i = number of ions (ideal)
- **Actual vs ideal i**: Real solutions have i slightly less than ideal (ion pairing)
- **Unit consistency**: Molality in mol/kg, Molarity in mol/L
- **Osmotic pressure**: Π = MRTi, use R = 0.0821 L·atm/(mol·K)
- **Solvent identification**: Water Kb=0.512, Kf=1.86; other solvents have different values

### Examples

**Example 1: Freezing point depression**
Question: "What is the freezing point of a solution with 1.0 m NaCl?"
- Given: m = 1.0 mol/kg, i = 2 (NaCl dissociates), Kf = 1.86 degC·kg/mol
- Solution: `new_freezing_point(m=1.0, Kf=1.86, Tf_pure=0, i=2)` -> -3.72degC

**Example 2: Osmotic pressure**
Question: "Calculate osmotic pressure of 0.10 M glucose at 298 K."
- Given: M = 0.10, T = 298 K, i = 1 (glucose is nonelectrolyte)
- Solution: `osmotic_pressure(M=0.10, T=298, i=1)` -> 2.45 atm

**Example 3: Molar mass from freezing point**
Question: "10.0 g solute in 0.100 kg water causes DeltaTf = 1.86degC. What is the molar mass?"
- Given: mass = 10.0 g, kg_solvent = 0.100, DeltaT = 1.86, Kf = 1.86, i = 1
- Solution: `molar_mass_from_fp_depression(mass_solute=10.0, mass_solvent_kg=0.100, delta_T=1.86, Kf=1.86, i=1)` -> 100 g/mol
"""

from typing import Optional

# Gas constant
R = 0.08206  # L·atm/(mol·K)

# Colligative property constants for common solvents
SOLVENT_CONSTANTS = {
    'water': {'Kb': 0.512, 'Kf': 1.86, 'Tb': 100.0, 'Tf': 0.0},
    'benzene': {'Kb': 2.53, 'Kf': 5.12, 'Tb': 80.1, 'Tf': 5.5},
    'ethanol': {'Kb': 1.22, 'Kf': 1.99, 'Tb': 78.4, 'Tf': -114.1},
    'chloroform': {'Kb': 3.63, 'Kf': 4.68, 'Tb': 61.2, 'Tf': -63.5},
    'acetic_acid': {'Kb': 3.07, 'Kf': 3.90, 'Tb': 118.1, 'Tf': 16.6},
}


def vapor_pressure_lowering(X_solvent: float, P0: float) -> float:
    """
    Calculate vapor pressure of solution using Raoult's Law.
    
    Args:
        X_solvent: Mole fraction of solvent
        P0: Vapor pressure of pure solvent (any unit)
    
    Returns:
        Vapor pressure of solution (same unit)
    
    Examples:
        >>> vapor_pressure_lowering(0.9, 23.8)
        21.42
    """
    return X_solvent * P0


def vapor_pressure_depression(X_solute: float, P0: float) -> float:
    """
    Calculate vapor pressure depression.
    
    Args:
        X_solute: Mole fraction of solute
        P0: Vapor pressure of pure solvent
    
    Returns:
        Vapor pressure depression (DeltaP)
    
    Examples:
        >>> vapor_pressure_depression(0.1, 23.8)
        2.38
    """
    return X_solute * P0


def boiling_point_elevation(m: float, Kb: float = 0.512, i: int = 1) -> float:
    """
    Calculate boiling point elevation.
    
    Args:
        m: Molality (mol/kg)
        Kb: Ebullioscopic constant (degC·kg/mol, default water)
        i: van't Hoff factor (default 1 for nonelectrolytes)
    
    Returns:
        DeltaTb in degC
    
    Examples:
        >>> boiling_point_elevation(1.0)
        0.512
        >>> boiling_point_elevation(1.0, i=2)  # NaCl
        1.024
    """
    return Kb * m * i


def freezing_point_depression(m: float, Kf: float = 1.86, i: int = 1) -> float:
    """
    Calculate freezing point depression.
    
    Args:
        m: Molality (mol/kg)
        Kf: Cryoscopic constant (degC·kg/mol, default water)
        i: van't Hoff factor (default 1 for nonelectrolytes)
    
    Returns:
        DeltaTf in degC
    
    Examples:
        >>> freezing_point_depression(1.0)
        1.86
        >>> freezing_point_depression(1.0, i=3)  # CaCl2
        5.58
    """
    return Kf * m * i


def new_boiling_point(m: float, Kb: float = 0.512, 
                      Tb_pure: float = 100.0, i: int = 1) -> float:
    """
    Calculate new boiling point of solution.
    
    Args:
        m: Molality
        Kb: Ebullioscopic constant
        Tb_pure: Normal boiling point of pure solvent
        i: van't Hoff factor
    
    Returns:
        New boiling point in degC
    
    Examples:
        >>> new_boiling_point(1.0)
        100.512
    """
    return Tb_pure + boiling_point_elevation(m, Kb, i)


def new_freezing_point(m: float, Kf: float = 1.86,
                       Tf_pure: float = 0.0, i: int = 1) -> float:
    """
    Calculate new freezing point of solution.
    
    Args:
        m: Molality
        Kf: Cryoscopic constant
        Tf_pure: Normal freezing point of pure solvent
        i: van't Hoff factor
    
    Returns:
        New freezing point in degC
    
    Examples:
        >>> new_freezing_point(1.0)
        -1.86
    """
    return Tf_pure - freezing_point_depression(m, Kf, i)


def osmotic_pressure(M: float, T: float, i: int = 1) -> float:
    """
    Calculate osmotic pressure.
    
    Args:
        M: Molarity (mol/L)
        T: Temperature in Kelvin
        i: van't Hoff factor
    
    Returns:
        Osmotic pressure in atm
    
    Examples:
        >>> osmotic_pressure(0.1, 298)
        2.44...
    """
    return M * R * T * i


def molar_mass_from_fp_depression(mass_solute: float, mass_solvent_kg: float,
                                   delta_T: float, Kf: float = 1.86,
                                   i: int = 1) -> float:
    """
    Determine molar mass from freezing point depression.
    
    Args:
        mass_solute: Mass of solute in grams
        mass_solvent_kg: Mass of solvent in kilograms
        delta_T: Freezing point depression (degC)
        Kf: Cryoscopic constant
        i: van't Hoff factor
    
    Returns:
        Molar mass in g/mol
    
    Examples:
        >>> molar_mass_from_fp_depression(10, 0.1, 1.86)
        100.0
    """
    m = delta_T / (Kf * i)
    moles = m * mass_solvent_kg
    return mass_solute / moles


def molar_mass_from_bp_elevation(mass_solute: float, mass_solvent_kg: float,
                                  delta_T: float, Kb: float = 0.512,
                                  i: int = 1) -> float:
    """
    Determine molar mass from boiling point elevation.
    
    Args:
        mass_solute: Mass of solute in grams
        mass_solvent_kg: Mass of solvent in kilograms
        delta_T: Boiling point elevation (degC)
        Kb: Ebullioscopic constant
        i: van't Hoff factor
    
    Returns:
        Molar mass in g/mol
    """
    m = delta_T / (Kb * i)
    moles = m * mass_solvent_kg
    return mass_solute / moles


def molar_mass_from_osmotic_pressure(mass_solute: float, volume_L: float,
                                      Pi: float, T: float, i: int = 1) -> float:
    """
    Determine molar mass from osmotic pressure.
    
    Args:
        mass_solute: Mass of solute in grams
        volume_L: Volume of solution in liters
        Pi: Osmotic pressure in atm
        T: Temperature in Kelvin
        i: van't Hoff factor
    
    Returns:
        Molar mass in g/mol
    """
    M = Pi / (R * T * i)
    moles = M * volume_L
    return mass_solute / moles


def vanthoff_factor(formula: str, actual: bool = False) -> float:
    """
    Get van't Hoff factor for a compound.
    
    Args:
        formula: Chemical formula
        actual: If True, return measured value (default ideal)
    
    Returns:
        van't Hoff factor
    
    Examples:
        >>> vanthoff_factor('NaCl')
        2.0
        >>> vanthoff_factor('NaCl', actual=True)
        1.9
    """
    ideal_factors = {
        'C6H12O6': 1, 'C12H22O11': 1,  # Nonelectrolytes
        'NaCl': 2, 'KCl': 2, 'NaOH': 2, 'HCl': 2,
        'CaCl2': 3, 'MgCl2': 3, 'BaCl2': 3,
        'Na2SO4': 3, 'K2SO4': 3,
        'FeCl3': 4, 'AlCl3': 4,
    }
    
    actual_factors = {
        'C6H12O6': 1.0, 'C12H22O11': 1.0,
        'NaCl': 1.9, 'KCl': 1.9, 'HCl': 1.9,
        'CaCl2': 2.7, 'MgCl2': 2.7,
        'MgSO4': 1.3,
        'FeCl3': 3.4,
    }
    
    if actual:
        return actual_factors.get(formula, ideal_factors.get(formula, 1))
    return ideal_factors.get(formula, 1)


def get_solvent_constants(solvent: str) -> dict:
    """
    Get colligative property constants for a solvent.
    
    Args:
        solvent: Solvent name
    
    Returns:
        Dictionary of constants
    """
    solvent_key = solvent.lower().replace(' ', '_')
    return SOLVENT_CONSTANTS.get(solvent_key, SOLVENT_CONSTANTS['water'])


# MCP Tool Declarations
MCP_TOOLS = [
    {'name': 'boiling_point_elevation', 'description': "Calculate boiling point elevation.\n\nArgs:\n    m: Molality (mol/kg)\n    Kb: Ebullioscopic constant (degC·kg/mol, default water)\n    i: van't Hoff factor (default 1 for nonelectrolytes)\n\nReturns:\n    DeltaTb in degC\n\nExamples:\n    >>> boiling_point_elevation(1.0)\n    0.512\n    >>> boiling_point_elevation(1.0, i=2)  # NaCl\n    1.024", 'inputSchema': {'type': 'object', 'properties': {'m': {'type': 'number', 'description': 'M'}, 'Kb': {'type': 'number', 'description': 'Kb', 'default': 0.512}, 'i': {'type': 'number', 'description': 'I', 'default': 1}}, 'required': ['m']}},
    {'name': 'freezing_point_depression', 'description': "Calculate freezing point depression.\n\nArgs:\n    m: Molality (mol/kg)\n    Kf: Cryoscopic constant (degC·kg/mol, default water)\n    i: van't Hoff factor (default 1 for nonelectrolytes)\n\nReturns:\n    DeltaTf in degC\n\nExamples:\n    >>> freezing_point_depression(1.0)\n    1.86\n    >>> freezing_point_depression(1.0, i=3)  # CaCl2\n    5.58", 'inputSchema': {'type': 'object', 'properties': {'m': {'type': 'number', 'description': 'M'}, 'Kf': {'type': 'number', 'description': 'Kf', 'default': 1.86}, 'i': {'type': 'number', 'description': 'I', 'default': 1}}, 'required': ['m']}},
    {'name': 'get_solvent_constants', 'description': 'Get colligative property constants for a solvent.\n\nArgs:\n    solvent: Solvent name\n\nReturns:\n    Dictionary of constants', 'inputSchema': {'type': 'object', 'properties': {'solvent': {'type': 'string', 'description': 'Solvent'}}, 'required': ['solvent']}},
    {'name': 'molar_mass_from_bp_elevation', 'description': "Determine molar mass from boiling point elevation.\n\nArgs:\n    mass_solute: Mass of solute in grams\n    mass_solvent_kg: Mass of solvent in kilograms\n    delta_T: Boiling point elevation (degC)\n    Kb: Ebullioscopic constant\n    i: van't Hoff factor\n\nReturns:\n    Molar mass in g/mol", 'inputSchema': {'type': 'object', 'properties': {'mass_solute': {'type': 'number', 'description': 'Mass Solute'}, 'mass_solvent_kg': {'type': 'string', 'description': 'Mass Solvent Kg'}, 'delta_T': {'type': 'number', 'description': 'Delta T'}, 'Kb': {'type': 'number', 'description': 'Kb', 'default': 0.512}, 'i': {'type': 'number', 'description': 'I', 'default': 1}}, 'required': ['mass_solute', 'mass_solvent_kg', 'delta_T']}},
    {'name': 'molar_mass_from_fp_depression', 'description': "Determine molar mass from freezing point depression.\n\nArgs:\n    mass_solute: Mass of solute in grams\n    mass_solvent_kg: Mass of solvent in kilograms\n    delta_T: Freezing point depression (degC)\n    Kf: Cryoscopic constant\n    i: van't Hoff factor\n\nReturns:\n    Molar mass in g/mol\n\nExamples:\n    >>> molar_mass_from_fp_depression(10, 0.1, 1.86)\n    100.0", 'inputSchema': {'type': 'object', 'properties': {'mass_solute': {'type': 'number', 'description': 'Mass Solute'}, 'mass_solvent_kg': {'type': 'string', 'description': 'Mass Solvent Kg'}, 'delta_T': {'type': 'number', 'description': 'Delta T'}, 'Kf': {'type': 'number', 'description': 'Kf', 'default': 1.86}, 'i': {'type': 'number', 'description': 'I', 'default': 1}}, 'required': ['mass_solute', 'mass_solvent_kg', 'delta_T']}},
    {'name': 'molar_mass_from_osmotic_pressure', 'description': "Determine molar mass from osmotic pressure.\n\nArgs:\n    mass_solute: Mass of solute in grams\n    volume_L: Volume of solution in liters\n    Pi: Osmotic pressure in atm\n    T: Temperature in Kelvin\n    i: van't Hoff factor\n\nReturns:\n    Molar mass in g/mol", 'inputSchema': {'type': 'object', 'properties': {'mass_solute': {'type': 'number', 'description': 'Mass Solute'}, 'volume_L': {'type': 'number', 'description': 'Volume L'}, 'Pi': {'type': 'number', 'description': 'Pi'}, 'T': {'type': 'number', 'description': 'T'}, 'i': {'type': 'number', 'description': 'I', 'default': 1}}, 'required': ['mass_solute', 'volume_L', 'Pi', 'T']}},
    {'name': 'new_boiling_point', 'description': "Calculate new boiling point of solution.\n\nArgs:\n    m: Molality\n    Kb: Ebullioscopic constant\n    Tb_pure: Normal boiling point of pure solvent\n    i: van't Hoff factor\n\nReturns:\n    New boiling point in degC\n\nExamples:\n    >>> new_boiling_point(1.0)\n    100.512", 'inputSchema': {'type': 'object', 'properties': {'m': {'type': 'number', 'description': 'M'}, 'Kb': {'type': 'number', 'description': 'Kb', 'default': 0.512}, 'Tb_pure': {'type': 'number', 'description': 'Tb Pure', 'default': 100.0}, 'i': {'type': 'number', 'description': 'I', 'default': 1}}, 'required': ['m']}},
    {'name': 'new_freezing_point', 'description': "Calculate new freezing point of solution.\n\nArgs:\n    m: Molality\n    Kf: Cryoscopic constant\n    Tf_pure: Normal freezing point of pure solvent\n    i: van't Hoff factor\n\nReturns:\n    New freezing point in degC\n\nExamples:\n    >>> new_freezing_point(1.0)\n    -1.86", 'inputSchema': {'type': 'object', 'properties': {'m': {'type': 'number', 'description': 'M'}, 'Kf': {'type': 'number', 'description': 'Kf', 'default': 1.86}, 'Tf_pure': {'type': 'number', 'description': 'Tf Pure', 'default': 0.0}, 'i': {'type': 'number', 'description': 'I', 'default': 1}}, 'required': ['m']}},
    {'name': 'osmotic_pressure', 'description': "Calculate osmotic pressure.\n\nArgs:\n    M: Molarity (mol/L)\n    T: Temperature in Kelvin\n    i: van't Hoff factor\n\nReturns:\n    Osmotic pressure in atm\n\nExamples:\n    >>> osmotic_pressure(0.1, 298)\n    2.44...", 'inputSchema': {'type': 'object', 'properties': {'M': {'type': 'number', 'description': 'M'}, 'T': {'type': 'number', 'description': 'T'}, 'i': {'type': 'number', 'description': 'I', 'default': 1}}, 'required': ['M', 'T']}},
    {'name': 'vanthoff_factor', 'description': "Get van't Hoff factor for a compound.\n\nArgs:\n    formula: Chemical formula\n    actual: If true, return measured value (default ideal)\n\nReturns:\n    van't Hoff factor\n\nExamples:\n    >>> vanthoff_factor('NaCl')\n    2.0\n    >>> vanthoff_factor('NaCl', actual=true)\n    1.9", 'inputSchema': {'type': 'object', 'properties': {'formula': {'type': 'string', 'description': 'Formula'}, 'actual': {'type': 'number', 'description': 'Actual', 'default': False}}, 'required': ['formula']}},
    {'name': 'vapor_pressure_depression', 'description': 'Calculate vapor pressure depression.\n\nArgs:\n    X_solute: Mole fraction of solute\n    P0: Vapor pressure of pure solvent\n\nReturns:\n    Vapor pressure depression (DeltaP)\n\nExamples:\n    >>> vapor_pressure_depression(0.1, 23.8)\n    2.38', 'inputSchema': {'type': 'object', 'properties': {'X_solute': {'type': 'number', 'description': 'X Solute'}, 'P0': {'type': 'number', 'description': 'P0'}}, 'required': ['X_solute', 'P0']}},
    {'name': 'vapor_pressure_lowering', 'description': "Calculate vapor pressure of solution using Raoult's Law.\n\nArgs:\n    X_solvent: Mole fraction of solvent\n    P0: Vapor pressure of pure solvent (any unit)\n\nReturns:\n    Vapor pressure of solution (same unit)\n\nExamples:\n    >>> vapor_pressure_lowering(0.9, 23.8)\n    21.42", 'inputSchema': {'type': 'object', 'properties': {'X_solvent': {'type': 'string', 'description': 'X Solvent'}, 'P0': {'type': 'number', 'description': 'P0'}}, 'required': ['X_solvent', 'P0']}}
]
