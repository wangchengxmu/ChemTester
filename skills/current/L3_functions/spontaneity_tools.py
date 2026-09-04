"""
Spontaneity Tools - L3 Implementation
Chapter 16.1: Spontaneity

## Solver Instructions (for AI Agent)

When you encounter spontaneity problems (Gibbs free energy, entropy, predicting reaction direction), follow this decision tree:

### Step 1: Identify what is given and what is asked
- **Spontaneity from DeltaG**: Given DeltaG value -> determine if process is spontaneous
- **Entropy prediction**: Given initial/final state (volume, temperature, phase) -> predict DeltaS
- **Matter dispersal**: Given volume change -> predict if expansion is spontaneous
- **Energy dispersal**: Given temperature difference -> predict heat flow direction
- **Temperature dependence**: Given DeltaH, DeltaS -> find temperature where DeltaG = 0 (equilibrium T)

### Step 2: Choose the correct function
- `is_spontaneous(delta_G)` -> bool (True if DeltaG < 0)
- `spontaneity_direction(delta_G)` -> 'forward (spontaneous)', 'reverse (spontaneous)', or 'equilibrium'
- `predict_matter_dispersal(initial_volume, final_volume)` -> expansion description
- `predict_energy_dispersal(T_hot, T_cold)` -> heat flow direction
- `predict_entropy_change(phase, direction)` -> entropy increase/decrease
- `equilibrium_temperature(delta_H, delta_S)` -> T = DeltaH/DeltaS where DeltaG=0

### Step 3: Handle special cases
- DeltaG < 0 -> spontaneous forward; DeltaG > 0 -> spontaneous reverse; DeltaG = 0 -> equilibrium
- Phase changes: solid->liquid->gas always increase entropy
- Dissolving: entropy can increase or decrease depending on solvation
- At equilibrium temperature: DeltaG = 0, reaction is at equilibrium

### Examples
1. **Spontaneity check**: DeltaG = -45 kJ/mol
   -> `is_spontaneous(-45)` -> True
   -> `spontaneity_direction(-45)` -> 'forward (spontaneous)'

2. **Equilibrium temperature**: DeltaH = +50 kJ/mol, DeltaS = +150 J/(mol·K)
   -> `equilibrium_temperature(50, 150)` -> T = 50000/150 = 333 K
   -> Below 333 K: DeltaG > 0 (non-spontaneous); Above 333 K: DeltaG < 0 (spontaneous)

3. **Matter dispersal**: Gas expands from 1 L to 5 L
   -> `predict_matter_dispersal(1.0, 5.0)` -> 'increased dispersal (spontaneous expansion)'
"""

from typing import Dict, Tuple, Optional


def is_spontaneous(delta_G: float) -> bool:
    """
    Determine if a process is spontaneous based on DeltaG.
    
    Args:
        delta_G: Gibbs free energy change (kJ/mol)
    
    Returns:
        True if spontaneous (DeltaG < 0)
    
    Examples:
        >>> is_spontaneous(-50.0)
        True
        >>> is_spontaneous(50.0)
        False
    """
    return delta_G < 0


def spontaneity_direction(delta_G: float) -> str:
    """
    Determine direction of spontaneity from DeltaG.
    
    Args:
        delta_G: Gibbs free energy change (kJ/mol)
    
    Returns:
        Direction string
    
    Examples:
        >>> spontaneity_direction(-10.0)
        'forward (spontaneous)'
        >>> spontaneity_direction(10.0)
        'reverse (spontaneous)'
        >>> spontaneity_direction(0.0)
        'equilibrium'
    """
    if delta_G < 0:
        return 'forward (spontaneous)'
    elif delta_G > 0:
        return 'reverse (spontaneous)'
    else:
        return 'equilibrium'


def predict_matter_dispersal(initial_volume: float, final_volume: float) -> str:
    """
    Predict if matter dispersal increases.
    
    Args:
        initial_volume: Initial volume (L)
        final_volume: Final volume (L)
    
    Returns:
        Dispersal change description
    
    Examples:
        >>> predict_matter_dispersal(1.0, 2.0)
        'increased dispersal (spontaneous expansion)'
    """
    if final_volume > initial_volume:
        return 'increased dispersal (spontaneous expansion)'
    elif final_volume < initial_volume:
        return 'decreased dispersal (requires work)'
    else:
        return 'no change in dispersal'


def predict_energy_dispersal(T_hot: float, T_cold: float) -> str:
    """
    Predict direction of heat flow based on temperatures.
    
    Args:
        T_hot: Temperature of hot object (K)
        T_cold: Temperature of cold object (K)
    
    Returns:
        Heat flow prediction
    
    Examples:
        >>> predict_energy_dispersal(373, 298)
        'heat flows from hot to cold (spontaneous)'
    """
    if T_hot > T_cold:
        return 'heat flows from hot to cold (spontaneous)'
    elif T_hot < T_cold:
        return 'heat would flow from cold to hot (nonspontaneous)'
    else:
        return 'at thermal equilibrium'


def distinguish_spontaneity_from_rate(is_spontaneous_process: bool,
                                       observed_rate: str = 'slow') -> Dict:
    """
    Clarify that spontaneity does not indicate rate.
    
    Args:
        is_spontaneous_process: Whether process is thermodynamically spontaneous
        observed_rate: 'fast', 'slow', or 'immeasurable'
    
    Returns:
        Dict with spontaneity and rate info
    
    Examples:
        >>> distinguish_spontaneity_from_rate(True, 'slow')
        {'spontaneous': True, 'rate': 'slow', 'note': 'spontaneous but may be kinetically slow'}
    """
    return {
        'spontaneous': is_spontaneous_process,
        'rate': observed_rate,
        'note': 'spontaneous but may be kinetically slow' if is_spontaneous_process and observed_rate == 'slow' else 'process proceeds'
    }


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="distinguish_spontaneity_from_rate",
            description="Clarify that spontaneity does not indicate rate.",
            input_schema=[
            InputSchemaField(name="is_spontaneous_process", type="boolean", required=True),
            InputSchemaField(name="observed_rate", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="is_spontaneous",
            description="Determine if a process is spontaneous based on DeltaG.",
            input_schema=[
            InputSchemaField(name="delta_G", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="predict_energy_dispersal",
            description="Predict direction of heat flow based on temperatures.",
            input_schema=[
            InputSchemaField(name="T_hot", type="number", required=True),
            InputSchemaField(name="T_cold", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="predict_matter_dispersal",
            description="Predict if matter dispersal increases.",
            input_schema=[
            InputSchemaField(name="initial_volume", type="number", required=True),
            InputSchemaField(name="final_volume", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="spontaneity_direction",
            description="Determine direction of spontaneity from DeltaG.",
            input_schema=[
            InputSchemaField(name="delta_G", type="number", required=True)
            ],
            handler="{name}",
        )
    ]
