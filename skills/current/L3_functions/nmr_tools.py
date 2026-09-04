"""NMR Tools - 2D NMR, splitting, and analysis helpers.

## Solver Instructions (for AI Agent)

When you encounter basic NMR unit conversion, multiplicity prediction (n+1 rule), or coupling constant questions, follow this decision tree:

### Step 1: Identify what is given and what is asked
- Given chemical shift in ppm and spectrometer frequency -> need frequency offset in Hz?
- Given number of neighboring protons -> predict multiplicity?
- Given a J coupling value -> just need it returned as absolute value?

### Step 2: Choose the correct function
- **Chemical shift to frequency:** `chemical_shift_to_freq(delta_ppm, freq_mhz)` -> Hz. Formula: Hz = ppm x MHz. Example: 2.0 ppm at 400 MHz = 800 Hz
- **Coupling constant (absolute):** `coupling_constant(j_hz)` -> returns |J| in Hz
- **Multiplicity (n+1 rule):** `multiplicity(n_neighbors)` -> 'singlet'(0), 'doublet'(1), 'triplet'(2), 'quartet'(3), 'quintet'(4)

### Step 3: Handle special cases
- Use `nmr_splitting_tools.py` for detailed intensity ratios and coupling analysis
- Chemical shift in Hz depends on spectrometer frequency - always specify MHz
- Coupling constants are always reported as positive (absolute) values

### Examples
```python
# Example 1: Convert 3.5 ppm at 300 MHz to Hz
chemical_shift_to_freq(3.5, 300)  -> 1050.0 Hz

# Example 2: 2 neighboring protons -> what multiplicity?
multiplicity(2)  -> 'triplet'

# Example 3: Coupling constant
coupling_constant(-7.2)  -> 7.2 Hz
```
"""
import math

def chemical_shift_to_freq(delta_ppm: float, freq_mhz: float) -> float:
    """Convert chemical shift (ppm) to frequency offset (Hz)."""
    return delta_ppm * freq_mhz

def coupling_constant(j_hz: float) -> float:
    """Return J coupling constant in Hz (pass-through for unit consistency)."""
    return abs(j_hz)

def multiplicity(n_neighbors: int) -> str:
    """Predict signal multiplicity from n equivalent neighbors (n+1 rule)."""
    names = {0: "singlet", 1: "doublet", 2: "triplet", 3: "quartet", 4: "quintet"}
    return names.get(n_neighbors, f"{n_neighbors+1}-let")


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="chemical_shift_to_freq",
            description="Convert chemical shift (ppm) to frequency offset (Hz).",
            input_schema=[
            InputSchemaField(name="delta_ppm", type="number", required=True),
            InputSchemaField(name="freq_mhz", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="coupling_constant",
            description="Return J coupling constant in Hz (pass-through for unit consistency).",
            input_schema=[
            InputSchemaField(name="j_hz", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="multiplicity",
            description="Predict signal multiplicity from n equivalent neighbors (n+1 rule).",
            input_schema=[
            InputSchemaField(name="n_neighbors", type="number", required=True)
            ],
            handler="{name}",
        )
    ]
