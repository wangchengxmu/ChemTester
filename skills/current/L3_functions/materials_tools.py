"""
Materials Tools - General materials science calculations.

## Solver Instructions (for AI Agent)

When you encounter materials science problems (packing, density, band gaps), follow this decision tree:

### Step 1: Identify what is given and what is asked
- Given crystal structure data -> calculate packing efficiency or density?
- Given absorption wavelength -> calculate band gap?
- Given cell parameters -> calculate material properties?

### Step 2: Choose the correct function
| Task | Function | Key Parameters |
|---|---|---|
| Packing efficiency | `packing_efficiency(n_atoms, atom_volume, cell_volume)` | n atoms per cell, atomic volume, cell volume |
| Crystal density | `density_from_cell(Z, M, V_cell, na=6.022e23)` | Z=atoms/cell, M=molar mass, V_cell in m3 |
| Band gap from lambda | `band_gap_from_wavelength(wavelength_nm)` | absorption edge in nm -> returns eV |

### Step 3: Handle special cases
- Packing efficiency: FCC = 74%, BCC = 68%, HCP = 74%, SC = 52%
- Band gap: E(eV) = 1240 / lambda(nm) - semiconductor property
- Density: ρ = Z·M/(N_A·V_cell) - standard crystallography formula

### Examples
```python
# Example 1: FCC packing efficiency
packing_efficiency(4, 0.0187, 0.0512)  # 4 atoms, atom vol, cell vol
# -> 1.46 (fraction, may exceed 1 if atom_volume includes void space)

# Example 2: Crystal density
density_from_cell(4, 58.44, 1.8e-28)  # NaCl: 4 formula units, M=58.44 g/mol
# -> ~2100 kg/m3

# Example 3: Band gap from absorption edge
band_gap_from_wavelength(500)  # 500 nm absorption edge
# -> 2.48 eV
```
"""
import math

def packing_efficiency(n_atoms: int, atom_volume: float, cell_volume: float) -> float:
    """Packing efficiency = (n x V_atom) / V_cell."""
    if cell_volume == 0:
        raise ValueError("Cell volume cannot be zero")
    return n_atoms * atom_volume / cell_volume

def density_from_cell(Z: float, M: float, V_cell: float, na: float = 6.022e23) -> float:
    """Crystal density: ρ = Z·M/(N_A·V_cell)."""
    return Z * M / (na * V_cell)

def band_gap_from_wavelength(wavelength_nm: float) -> float:
    """Band gap in eV from absorption edge wavelength: E = hc/lambda."""
    hc = 1240.0  # eV·nm
    return hc / wavelength_nm

MCP_TOOLS = [
    {
        "name": "band_gap_from_wavelength",
        "description": "Band gap in eV from absorption edge wavelength: E = hc/lambda.",
        "parameters": [
            {
                "name": "wavelength_nm",
                "type": "number"
            }
        ]
    },
    {
        "name": "density_from_cell",
        "description": "Crystal density: ρ = Z·M/(N_A·V_cell).",
        "parameters": [
            {
                "name": "Z",
                "type": "number"
            },
            {
                "name": "M",
                "type": "number"
            },
            {
                "name": "V_cell",
                "type": "number"
            },
            {
                "name": "na",
                "type": "number"
            }
        ]
    },
    {
        "name": "packing_efficiency",
        "description": "Packing efficiency = (n x V_atom) / V_cell.",
        "parameters": [
            {
                "name": "n_atoms",
                "type": "number"
            },
            {
                "name": "atom_volume",
                "type": "number"
            },
            {
                "name": "cell_volume",
                "type": "number"
            }
        ]
    }
]
