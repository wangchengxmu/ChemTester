"""DFT Tools - Density Functional Theory helper functions.
## Solver Instructions (for AI Agent)

When you encounter DFT (Density Functional Theory) calculation problems:

### Step 1: Identify what is given and what is asked
- Given: electron density n, Wigner-Seitz radius rs, functional name, Kohn-Sham orbital energies
- Asked: exchange-correlation energy, Kohn-Sham total energy, screening length

### Step 2: Choose the correct function
- `exchange_correlation_energy(n, rs, functional)`: Exc for LDA (Dirac exchange)
- `kohn_sham_energy(ekin, vh, vxc, exc)`: E_KS = T_s + V_H + V_xc + E_xc

### Step 3: Handle special cases
- LDA: Exc(n) ~ -0.7386 x n x (3n/(4pi))^(1/3) (Dirac exchange only)
- rs = (3/(4pin))^(1/3) in atomic units

### Examples
```python
exc = exchange_correlation_energy(0.03, 4.0, "LDA")  # -> LDA exchange energy
```
"""
import math

def exchange_correlation_energy(n: float, rs: float, functional: str = "LDA") -> float:
    """Approximate XC energy per particle. LDA: Dirac exchange + Wigner correlation."""
    if functional == "LDA":
        ex = -0.7386 / rs
        ec = -0.44 / (rs + 7.8)
        return ex + ec
    raise ValueError(f"Unknown functional: {functional}")

def kohn_sham_energy(ekin: float, vh: float, vxc: float, exc: float) -> float:
    """Total Kohn-Sham energy: E = T_s + V_H + V_xc + E_xc."""
    return ekin + vh + vxc + exc

def screening_length(fermi_wavenumber: float) -> float:
    """Thomas-Fermi screening length."""
    return 1.0 / (2.0 * fermi_wavenumber)


# MCP Tool Declarations
MCP_TOOLS = [
    {'name': 'exchange_correlation_energy', 'description': 'Approximate XC energy per particle. LDA: Dirac exchange + Wigner correlation.', 'inputSchema': {'type': 'object', 'properties': {'n': {'type': 'number', 'description': 'N'}, 'rs': {'type': 'number', 'description': 'Rs'}, 'functional': {'type': 'string', 'description': 'Functional', 'default': 'LDA'}}, 'required': ['n', 'rs']}},
    {'name': 'kohn_sham_energy', 'description': 'Total Kohn-Sham energy: E = T_s + V_H + V_xc + E_xc.', 'inputSchema': {'type': 'object', 'properties': {'ekin': {'type': 'number', 'description': 'Ekin'}, 'vh': {'type': 'number', 'description': 'Vh'}, 'vxc': {'type': 'string', 'description': 'Vxc'}, 'exc': {'type': 'string', 'description': 'Exc'}}, 'required': ['ekin', 'vh', 'vxc', 'exc']}},
    {'name': 'screening_length', 'description': 'Thomas-Fermi screening length.', 'inputSchema': {'type': 'object', 'properties': {'fermi_wavenumber': {'type': 'number', 'description': 'Fermi Wavenumber'}}, 'required': ['fermi_wavenumber']}}
]
