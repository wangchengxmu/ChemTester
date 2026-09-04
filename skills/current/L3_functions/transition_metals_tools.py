"""
Transition Metals Tools - L3 Implementation
Chapter 19.1: Transition Metals and Their Compounds
"""

## Solver Instructions (for AI Agent)

# When you encounter **transition metal** electronic configuration and properties problems, follow this decision tree:

### Step 1: Identify what is given and what is asked
# - Ion electron configuration: `ion_electron_config(element, charge)`
# - Count d electrons: `count_d_electrons(element, charge)`
# - Count unpaired electrons in a geometry: `count_unpaired_electrons(d_count, geometry)`
# - Common oxidation states: `common_oxidation_states(element)`

### Step 2: Choose the correct function
# - Start with `ion_electron_config` to see full configuration
# - Use `count_d_electrons` for the d-electron count
# - Use `count_unpaired_electrons` with geometry ('octahedral', 'tetrahedral', 'square_planar')
# - `common_oxidation_states` for periodic trend information

### Step 3: Handle special cases
# - Elements use standard symbols (e.g., 'Fe', 'Cu', 'Cr')
# - Charge should be the ionic charge (positive integer for cations)
# - Geometry affects crystal field splitting and thus unpaired count
# - Superscript formatting handled internally by `superscript()`

### Examples
# 1. Fe3+ configuration: `ion_electron_config("Fe", 3)` -> [Ar] 3d5
# 2. d-electron count of Cu2+: `count_d_electrons("Cu", 2)` -> 9
# 3. Unpaired electrons for d6 octahedral (low-spin): `count_unpaired_electrons(6, "octahedral")` -> depends on spin state
# 4. Common oxidation states of Mn: `common_oxidation_states("Mn")` -> [+2, +3, +4, +6, +7]



from typing import Dict, Tuple, Optional, List


# Electron configurations for neutral transition metals (first row)
TRANSITION_CONFIGS = {
    'Sc': '3d14s2',
    'Ti': '3d24s2',
    'V': '3d34s2',
    'Cr': '3d54s1',  # Exception
    'Mn': '3d54s2',
    'Fe': '3d64s2',
    'Co': '3d74s2',
    'Ni': '3d84s2',
    'Cu': '3d104s1',  # Exception
    'Zn': '3d104s2'
}


def ion_electron_config(element: str, charge: int) -> str:
    """
    Write electron configuration for transition metal ion.
    
    Remove s electrons before d electrons.
    
    Args:
        element: Element symbol
        charge: Ion charge (positive integer)
    
    Returns:
        Electron configuration string
    
    Examples:
        >>> ion_electron_config('Fe', 2)
        '3d6'
        >>> ion_electron_config('Fe', 3)
        '3d5'
    """
    base_configs = {
        'Sc': ('3d14s2', 3),
        'Ti': ('3d24s2', 4),
        'V': ('3d34s2', 5),
        'Cr': ('3d54s1', 6),
        'Mn': ('3d54s2', 7),
        'Fe': ('3d64s2', 8),
        'Co': ('3d74s2', 9),
        'Ni': ('3d84s2', 10),
        'Cu': ('3d104s1', 11),
        'Zn': ('3d104s2', 12)
    }
    
    if element not in base_configs:
        return 'Unknown element'
    
    # Simplified: return d electron count for common ions
    d_electrons = {
        ('Sc', 3): 0,
        ('Ti', 2): 2, ('Ti', 3): 1, ('Ti', 4): 0,
        ('V', 2): 3, ('V', 3): 2, ('V', 4): 1, ('V', 5): 0,
        ('Cr', 2): 4, ('Cr', 3): 3, ('Cr', 6): 0,
        ('Mn', 2): 5, ('Mn', 3): 4, ('Mn', 4): 3, ('Mn', 7): 0,
        ('Fe', 2): 6, ('Fe', 3): 5,
        ('Co', 2): 7, ('Co', 3): 6,
        ('Ni', 2): 8,
        ('Cu', 1): 10, ('Cu', 2): 9,
        ('Zn', 2): 10
    }
    
    key = (element, charge)
    if key in d_electrons:
        d_count = d_electrons[key]
        if d_count == 0:
            return '[Ar]'
        return f'3d{superscript(d_count)}'
    
    return 'Unknown configuration'


def superscript(n: int) -> str:
    """Convert number to superscript."""
    superscripts = '0123456789'
    return ''.join(superscripts[int(d)] for d in str(n))


def count_d_electrons(element: str, charge: int) -> int:
    """
    Count d electrons in transition metal ion.
    
    Args:
        element: Element symbol
        charge: Ion charge
    
    Returns:
        Number of d electrons
    """
    d_electrons = {
        ('Sc', 3): 0,
        ('Ti', 2): 2, ('Ti', 3): 1, ('Ti', 4): 0,
        ('V', 2): 3, ('V', 3): 2, ('V', 4): 1, ('V', 5): 0,
        ('Cr', 2): 4, ('Cr', 3): 3, ('Cr', 6): 0,
        ('Mn', 2): 5, ('Mn', 3): 4, ('Mn', 4): 3, ('Mn', 7): 0,
        ('Fe', 2): 6, ('Fe', 3): 5,
        ('Co', 2): 7, ('Co', 3): 6,
        ('Ni', 2): 8,
        ('Cu', 1): 10, ('Cu', 2): 9,
        ('Zn', 2): 10
    }
    return d_electrons.get((element, charge), -1)


def count_unpaired_electrons(d_count: int, geometry: str = 'octahedral',
                              high_spin: bool = True) -> int:
    """
    Count unpaired electrons based on d electron count and geometry.
    
    Args:
        d_count: Number of d electrons
        geometry: 'octahedral' or 'tetrahedral'
        high_spin: True for high-spin complexes
    
    Returns:
        Number of unpaired electrons
    """
    # High-spin octahedral unpaired electrons
    unpaired_high_spin_oct = {
        0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5,
        6: 4, 7: 3, 8: 2, 9: 1, 10: 0
    }
    
    # Low-spin octahedral unpaired electrons
    unpaired_low_spin_oct = {
        0: 0, 1: 1, 2: 2, 3: 3, 4: 2, 5: 1,
        6: 0, 7: 1, 8: 2, 9: 1, 10: 0
    }
    
    # Tetrahedral (always high-spin)
    unpaired_tetrahedral = {
        0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5,
        6: 4, 7: 3, 8: 2, 9: 1, 10: 0
    }
    
    if geometry == 'octahedral':
        if high_spin:
            return unpaired_high_spin_oct.get(d_count, 0)
        else:
            return unpaired_low_spin_oct.get(d_count, 0)
    else:
        return unpaired_tetrahedral.get(d_count, 0)


def common_oxidation_states(element: str) -> list:
    """
    Return common oxidation states for transition metal.
    
    Args:
        element: Element symbol
    
    Returns:
        List of common oxidation states
    """
    oxidation_states = {
        'Sc': [3],
        'Ti': [2, 3, 4],
        'V': [2, 3, 4, 5],
        'Cr': [2, 3, 6],
        'Mn': [2, 3, 4, 7],
        'Fe': [2, 3],
        'Co': [2, 3],
        'Ni': [2],
        'Cu': [1, 2],
        'Zn': [2]
    }
    return oxidation_states.get(element, [])


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="common_oxidation_states",
            description="Return common oxidation states for transition metal.",
            input_schema=[
            InputSchemaField(name="element", type="string", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="count_d_electrons",
            description="Count d electrons in transition metal ion.",
            input_schema=[
            InputSchemaField(name="element", type="string", required=True),
            InputSchemaField(name="charge", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="count_unpaired_electrons",
            description="Count unpaired electrons based on d electron count and geometry.",
            input_schema=[
            InputSchemaField(name="d_count", type="number", required=True),
            InputSchemaField(name="geometry", type="number", required=False),
            InputSchemaField(name="high_spin", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="ion_electron_config",
            description="Write electron configuration for transition metal ion.",
            input_schema=[
            InputSchemaField(name="element", type="string", required=True),
            InputSchemaField(name="charge", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="superscript",
            description="Convert number to superscript.",
            input_schema=[
            InputSchemaField(name="n", type="number", required=True)
            ],
            handler="{name}",
        )
    ]
