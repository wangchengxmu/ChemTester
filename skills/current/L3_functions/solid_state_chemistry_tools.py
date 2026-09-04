"""
Solid State Chemistry Tools - L3 Implementation
Source: Averill, Ch12

## Solver Instructions (for AI Agent)

When you encounter solid state chemistry problems (crystal structures, band theory, conductivity, defect chemistry), follow this decision tree:

### Step 1: Identify what is given and what is asked
- **Solid classification**: Given bonding type -> predict properties (mp, conductivity, solubility)
- **Band gap classification**: Given band gap in eV -> classify as metal/semiconductor/insulator
- **Unit cell calculations**: Given lattice type and parameters -> find atoms per cell, density, packing efficiency
- **Defect calculations**: Given defect type and concentration -> find properties (color, conductivity)
- **Conductivity prediction**: Given material type and temperature -> predict conductivity behavior

### Step 2: Choose the correct function
- `classify_solid(bonding_type)` -> dict with mp, conductivity, solubility, examples
- `predict_conductivity(material_type, temperature)` -> conductivity description
- `band_gap_classification(band_gap_ev)` -> 'metal' (<0), 'semiconductor' (0-3 eV), 'insulator' (>3 eV)
- `atoms_per_unit_cell(lattice_type)` -> number of atoms (SC=1, BCC=2, FCC=4)
- `packing_efficiency(lattice_type)` -> % of space filled (SC=52%, BCC=68%, FCC=74%)
- `density_from_cell(parameters)` -> ρ = Z·M/(N_A·a3)
- `schottky_defect_concentration(Ef, T, N)` -> n_s = N·exp(-Ef/2kT)
- `frenkel_defect_concentration(Ef, T, N)` -> n_f = √(N·N_i)·exp(-Ef/2kT)

### Step 3: Handle special cases
- Metals have no band gap (overlapping bands); insulators have >3-4 eV gap
- Semiconductors: conductivity increases with T (thermal excitation); metals decrease
- FCC has highest packing efficiency (74%); SC lowest (52%)
- Schottky defects: paired vacancy; Frenkel: cation displaced to interstitial site
- n-type doping: group 15 in group 14 lattice; p-type: group 13 in group 14

### Examples
1. **Band gap classification**: Si has band gap 1.1 eV; diamond has 5.5 eV
   -> `band_gap_classification(1.1)` -> 'semiconductor'
   -> `band_gap_classification(5.5)` -> 'insulator'

2. **Packing efficiency**: FCC copper
   -> `packing_efficiency('fcc')` -> 74% (highest for pure metals)

3. **Solid classification**: NaCl
   -> `classify_solid('ionic')` -> {'melting_point': 'high', 'conductivity': 'low (solid), high (molten)', ...}
"""

from typing import Dict, List, Tuple


def classify_solid(bonding_type: str) -> Dict:
    """
    Classify solid type and predict properties.
    
    Args:
        bonding_type: 'ionic', 'molecular', 'covalent_network', 'metallic'
    
    Returns:
        Dict with properties
    
    Examples:
        >>> classify_solid('ionic')
        {'type': 'ionic', 'melting_point': 'high', 'conductivity': 'low (solid)'}
    """
    properties = {
        'ionic': {
            'type': 'ionic',
            'melting_point': 'high',
            'conductivity': 'low (solid), high (molten)',
            'solubility': 'often water soluble',
            'examples': ['NaCl', 'MgO', 'CaF2']
        },
        'molecular': {
            'type': 'molecular',
            'melting_point': 'low',
            'conductivity': 'none',
            'solubility': 'varies by polarity',
            'examples': ['ice', 'dry ice', 'sucrose']
        },
        'covalent_network': {
            'type': 'covalent_network',
            'melting_point': 'very high',
            'conductivity': 'diamond: none, graphite: moderate',
            'solubility': 'insoluble',
            'examples': ['diamond', 'silicon', 'SiO2']
        },
        'metallic': {
            'type': 'metallic',
            'melting_point': 'varies',
            'conductivity': 'high',
            'solubility': 'insoluble in common solvents',
            'examples': ['Fe', 'Cu', 'Al']
        }
    }
    return properties.get(bonding_type, {})


def predict_conductivity(material_type: str, temperature: float = 298) -> str:
    """
    Predict electrical conductivity of a solid.
    
    Args:
        material_type: 'metal', 'semiconductor', 'insulator'
        temperature: Temperature in K
    
    Returns:
        Conductivity description
    """
    if material_type == 'metal':
        return 'High conductivity, decreases slightly with temperature'
    elif material_type == 'semiconductor':
        return 'Moderate conductivity, increases with temperature'
    elif material_type == 'insulator':
        return 'Very low conductivity'
    else:
        return 'Unknown material type'


def band_gap_classification(band_gap_ev: float) -> str:
    """
    Classify material based on band gap energy.
    
    Args:
        band_gap_ev: Band gap in electron volts
    
    Returns:
        Material classification
    
    Examples:
        >>> band_gap_classification(0.5)
        'metal/poor semiconductor'
        >>> band_gap_classification(5.0)
        'insulator'
    """
    if band_gap_ev < 0.1:
        return 'metal'
    elif band_gap_ev < 3.0:
        return 'semiconductor'
    else:
        return 'insulator'


def unit_cell_atoms(cell_type: str) -> int:
    """
    Return number of atoms per unit cell.
    
    Args:
        cell_type: 'simple_cubic', 'bcc', 'fcc', 'hcp'
    
    Returns:
        Number of atoms
    
    Examples:
        >>> unit_cell_atoms('simple_cubic')
        1
        >>> unit_cell_atoms('fcc')
        4
    """
    atoms = {
        'simple_cubic': 1,
        'bcc': 2,
        'fcc': 4,
        'hcp': 2
    }
    return atoms.get(cell_type, 0)


def coordination_number(cell_type: str) -> int:
    """
    Return coordination number for crystal structure.
    
    Args:
        cell_type: Crystal structure type
    
    Returns:
        Coordination number
    """
    cn = {
        'simple_cubic': 6,
        'bcc': 8,
        'fcc': 12,
        'hcp': 12,
        'diamond': 4,
        'nacl': 6
    }
    return cn.get(cell_type, 0)


def packing_efficiency(cell_type: str) -> float:
    """
    Return packing efficiency (fraction of space filled).
    
    Args:
        cell_type: Crystal structure type
    
    Returns:
        Packing efficiency as decimal
    
    Examples:
        >>> packing_efficiency('fcc')
        0.74
    """
    efficiency = {
        'simple_cubic': 0.52,
        'bcc': 0.68,
        'fcc': 0.74,
        'hcp': 0.74
    }
    return efficiency.get(cell_type, 0.0)


def density_from_cell(cell_type: str, atomic_mass: float,
                       edge_length: float) -> float:
    """
    Calculate density from unit cell parameters.
    
    ρ = (n x M) / (a3 x N_A)
    
    Args:
        cell_type: Crystal structure type
        atomic_mass: Atomic mass in g/mol
        edge_length: Unit cell edge in cm
    
    Returns:
        Density in g/cm3
    """
    n = unit_cell_atoms(cell_type)
    N_A = 6.022e23
    
    if edge_length == 0 or n == 0:
        return 0.0
    
    volume = edge_length ** 3
    density = (n * atomic_mass) / (volume * N_A)
    return density


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="band_gap_classification",
            description="Classify material based on band gap energy.",
            input_schema=[
            InputSchemaField(name="band_gap_ev", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="classify_solid",
            description="Classify solid type and predict properties.",
            input_schema=[
            InputSchemaField(name="bonding_type", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="coordination_number",
            description="Return coordination number for crystal structure.",
            input_schema=[
            InputSchemaField(name="cell_type", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="density_from_cell",
            description="Calculate density from unit cell parameters.",
            input_schema=[
            InputSchemaField(name="cell_type", type="number", required=True),
            InputSchemaField(name="atomic_mass", type="number", required=True),
            InputSchemaField(name="edge_length", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="packing_efficiency",
            description="Return packing efficiency (fraction of space filled).",
            input_schema=[
            InputSchemaField(name="cell_type", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="predict_conductivity",
            description="Predict electrical conductivity of a solid.",
            input_schema=[
            InputSchemaField(name="material_type", type="number", required=True),
            InputSchemaField(name="temperature", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="unit_cell_atoms",
            description="Return number of atoms per unit cell.",
            input_schema=[
            InputSchemaField(name="cell_type", type="number", required=True)
            ],
            handler="{name}",
        )
    ]
