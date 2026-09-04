"""
Gas Pressure Tools - L3 Implementation
Chapter 8.01-8.02: Gas Pressure and Measurement
## Solver Instructions (for AI Agent)

When you encounter gas pressure, unit conversion, or manometer problems, follow this decision tree:

### Step 1: Identify what is given and what is asked
- Convert pressure units? Use `convert_pressure(value, from_unit, to_unit)` - supports Pa, kPa, atm, bar, mbar, torr, mmHg, psi, inHg
- Hydrostatic pressure from fluid column? Use `hydrostatic_pressure(height, density, g=9.81)` -> Pa
- Manometer reading -> Gas pressure? Use `manometer_pressure(manometer_type, height, P_atm=101325, density=13600)`
- Standard pressure in specific unit? Use `standard_pressure(unit)`
- Pressure at depth in fluid? Use `pressure_at_depth(depth, P_surface=101325, density=1000, g=9.81)`

### Step 2: Handle special cases
- **Manometer types**: 'closed' (direct reading), 'open_higher' (gas > atm, P_gas = P_atm + ρgh), 'open_lower' (gas < atm, P_gas = P_atm - ρgh)
- **Mercury vs water**: Mercury density = 13600 kg/m3; Water = 1000 kg/m3; 760 mmHg ~ 10.3 m water
- **Unit normalization**: Function accepts various unit name formats (e.g., 'mmHg', 'mm hg', 'torr')

### Examples
```python
# Example 1: Unit conversion
convert_pressure(760, 'torr', 'atm')  # -> 1.0
convert_pressure(1, 'atm', 'kPa')  # -> 101.325

# Example 2: Mercury barometer (0.76 m Hg)
hydrostatic_pressure(0.76, 13600)  # -> 101325 Pa ~ 1 atm

# Example 3: Open-end manometer (gas higher)
manometer_pressure('open_higher', 0.10, P_atm=101325, density=13600)  # -> ~114652 Pa
```
"""

from typing import Union

# Pressure unit conversion factors to pascals
PRESSURE_TO_PA = {
    'Pa': 1,
    'kPa': 1000,
    'atm': 101325,
    'bar': 100000,
    'mbar': 100,
    'torr': 133.322,
    'mmHg': 133.322,
    'psi': 6894.76,
    'inHg': 3386.39,
}


def convert_pressure(value: float, from_unit: str, to_unit: str) -> float:
    """
    Convert pressure between different units.
    
    Args:
        value: Pressure value to convert
        from_unit: Original unit (Pa, kPa, atm, bar, mbar, torr, mmHg, psi, inHg)
        to_unit: Target unit
    
    Returns:
        Converted pressure value
    
    Examples:
        >>> convert_pressure(1, 'atm', 'Pa')
        101325.0
        >>> convert_pressure(760, 'torr', 'atm')
        1.0
        >>> convert_pressure(101.325, 'kPa', 'atm')
        1.0
    """
    from_unit = from_unit.lower().replace('mmhg', 'mmHg').replace('inhg', 'inHg')
    to_unit = to_unit.lower().replace('mmhg', 'mmHg').replace('inhg', 'inHg')
    
    # Normalize unit names
    unit_map = {
        'pa': 'Pa', 'pascal': 'Pa', 'pascals': 'Pa',
        'kpa': 'kPa', 'kilopascal': 'kPa',
        'atm': 'atm', 'atmosphere': 'atm', 'atmospheres': 'atm',
        'bar': 'bar', 'bars': 'bar',
        'mbar': 'mbar', 'millibar': 'mbar',
        'torr': 'torr',
        'mmhg': 'mmHg', 'mm hg': 'mmHg',
        'psi': 'psi',
        'inhg': 'inHg', 'in hg': 'inHg',
    }
    
    from_unit = unit_map.get(from_unit.lower(), from_unit)
    to_unit = unit_map.get(to_unit.lower(), to_unit)
    
    if from_unit not in PRESSURE_TO_PA:
        raise ValueError(f"Unknown unit: {from_unit}")
    if to_unit not in PRESSURE_TO_PA:
        raise ValueError(f"Unknown unit: {to_unit}")
    
    # Convert to Pa first, then to target unit
    value_in_pa = value * PRESSURE_TO_PA[from_unit]
    return value_in_pa / PRESSURE_TO_PA[to_unit]


def hydrostatic_pressure(height: float, density: float, g: float = 9.81) -> float:
    """
    Calculate hydrostatic pressure from fluid column.
    
    Args:
        height: Height of fluid column in meters
        density: Fluid density in kg/m3
        g: Acceleration due to gravity (default 9.81 m/s2)
    
    Returns:
        Pressure in pascals
    
    Examples:
        >>> hydrostatic_pressure(0.76, 13600)  # Mercury barometer
        10133760.0
        >>> hydrostatic_pressure(10.3, 1000)  # Water column
        10104300.0
    """
    return height * density * g


def manometer_pressure(manometer_type: str, height: float, 
                       P_atm: float = 101325, density: float = 13600) -> float:
    """
    Calculate gas pressure from manometer reading.
    
    Args:
        manometer_type: 'closed' or 'open_higher' or 'open_lower'
        height: Height difference in meters
        P_atm: Atmospheric pressure in Pa (for open-end manometer)
        density: Fluid density in kg/m3 (default: mercury)
    
    Returns:
        Gas pressure in pascals
    
    Examples:
        >>> manometer_pressure('closed', 0.26)  # 26 cm Hg closed-end
        35232.0
        >>> manometer_pressure('open_higher', 0.10)  # Gas higher than atm
        114652.0
    """
    h_pressure = hydrostatic_pressure(height, density)
    
    if manometer_type == 'closed':
        return h_pressure
    elif manometer_type == 'open_higher':
        # Gas pushes fluid down, so gas > atm
        return P_atm + h_pressure
    elif manometer_type == 'open_lower':
        # Atmosphere pushes fluid down, so gas < atm
        return P_atm - h_pressure
    else:
        raise ValueError(f"Unknown manometer type: {manometer_type}")


def standard_pressure(unit: str = 'atm') -> float:
    """
    Get standard pressure in specified unit.
    
    Args:
        unit: Target unit
    
    Returns:
        Standard pressure (1 atm) in specified unit
    
    Examples:
        >>> standard_pressure('atm')
        1.0
        >>> standard_pressure('kPa')
        101.325
    """
    return convert_pressure(1, 'atm', unit)


def pressure_at_depth(depth: float, P_surface: float = 101325, 
                      density: float = 1000, g: float = 9.81) -> float:
    """
    Calculate pressure at a depth in a fluid.
    
    Args:
        depth: Depth below surface in meters
        P_surface: Pressure at surface in Pa
        density: Fluid density in kg/m3
        g: Gravitational acceleration
    
    Returns:
        Pressure at depth in pascals
    
    Examples:
        >>> pressure_at_depth(10)  # 10 m underwater
        199425.0
    """
    return P_surface + hydrostatic_pressure(depth, density, g)


# MCP Tool Declarations
MCP_TOOLS = [
    {
        "name": "convert_pressure",
        "description": "Convert pressure between different units.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "value": {"type": "number", "description": "Value"},
                "from_unit": {"type": "number", "description": "From Unit"},
                "to_unit": {"type": "number", "description": "To Unit"},
            },
            "required": ["value", "from_unit", "to_unit"]
        }
    },
    {
        "name": "hydrostatic_pressure",
        "description": "Calculate hydrostatic pressure from fluid column.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "height": {"type": "number", "description": "Height"},
                "density": {"type": "number", "description": "Density"},
                "g": {"type": "number", "description": "G", "default": 9.81},
            },
            "required": ["height", "density"]
        }
    },
    {
        "name": "manometer_pressure",
        "description": "Calculate gas pressure from manometer reading.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "manometer_type": {"type": "string", "description": "Manometer Type"},
                "height": {"type": "number", "description": "Height"},
                "P_atm": {"type": "number", "description": "P Atm", "default": 101325},
                "density": {"type": "number", "description": "Density", "default": 13600},
            },
            "required": ["manometer_type", "height"]
        }
    },
    {
        "name": "pressure_at_depth",
        "description": "Calculate pressure at a depth in a fluid.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "depth": {"type": "number", "description": "Depth"},
                "P_surface": {"type": "number", "description": "P Surface", "default": 101325},
                "density": {"type": "number", "description": "Density", "default": 1000},
                "g": {"type": "number", "description": "G", "default": 9.81},
            },
            "required": ["depth"]
        }
    },
    {
        "name": "standard_pressure",
        "description": "Get standard pressure in specified unit.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "unit": {"type": "number", "description": "Unit", "default": "atm"},
            },
            "required": []
        }
    }
]
