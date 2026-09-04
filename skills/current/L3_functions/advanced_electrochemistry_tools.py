"""
L3 Tool: Advanced Electrochemistry Tools
Nernst equation, electrolysis calculations, and thermodynamic relationships.

Source: Physical Chemistry (LibreTexts)
Created: 2026-03-13

## Solver Instructions (for AI Agent)

When you encounter electrochemistry problems (Nernst equation, electrolysis, Faraday's law, cell potentials):

### Step 1: Identify what is given and what is asked
- Given: standard potentials, concentrations, current, time, masses, temperature
- Asked: cell potential, mass deposited, time required, spontaneity, DeltaG, K

### Step 2: Choose the correct function
- `nernst_equation(E0, n, Q, T)`: E = Edeg - (RT/nF)ln(Q)
- `nernst_equation_25C(E0, n, Q)`: At 25degC using 0.0592/n x log10(Q)
- `reaction_quotient(...)`: Calculate Q from concentrations and coefficients
- `cell_potential_from_half_reactions(E0_cathode, E0_anode, n, Q, T)`: Full cell E
- `equilibrium_constant_from_potential(E0, n, T)`: K from Edeg
- `cell_potential_from_K(E0, n, K)`: E from K
- `free_energy_from_potential(E, n)`: DeltaG = -nFE
- `potential_from_free_energy(dG, n)`: E = -DeltaG/(nF)
- `mass_from_electrolysis(current, time, molar_mass, n_electrons)`: Faraday's law
- `moles_from_electrolysis(current, time, n_electrons)`: Moles from Q = It
- `time_for_mass(mass, current, molar_mass, n_electrons)`: Time for electrolysis
- `minimum_voltage(E_cell)`: |E_cell| thermodynamic minimum

### Step 3: Handle special cases
- Edeg_cell = Edeg_cathode - Edeg_anode (always subtract anode reduction potential)
- At 25degC: nernst factor = 0.0592/n per electron transferred
- Balance half-reactions before determining n (electrons transferred)

### Examples
```python
E0 = 0.337 - (-0.763)  # Cu/Zn cell = 1.100V
E = nernst_equation_25C(1.100, 2, 0.1/1.0)  # -> ~1.070V
mass = mass_from_electrolysis(2.0, 1800, 63.55, 2)  # Cu, 2A, 30min -> ~1.185g
```
"""

import math

# Constants
R = 8.314  # J/(mol·K)
F = 96485  # C/mol


def nernst_potential(e0: float, n: int, q: float, t: float = 298.15) -> dict:
    """
    Calculate cell potential at non-standard conditions.
    
    E = Edeg - (RT/nF) ln Q
    
    Args:
        e0: Standard cell potential (V)
        n: Moles of electrons transferred
        q: Reaction quotient
        t: Temperature (K), default 298.15 K (25degC)
    
    Returns:
        Dictionary with cell potential
    
    Example:
        >>> nernst_potential(1.10, 2, 0.1)
        {'e': 1.13, 'e0': 1.10, 'n': 2, 'q': 0.1}
    """
    if q <= 0:
        return {'error': 'Q must be positive'}
    
    # E = Edeg - (RT/nF) ln Q
    rt_nf = (R * t) / (n * F)
    e = e0 - rt_nf * math.log(q)
    
    return {
        'e': round(e, 4),
        'e0': e0,
        'n': n,
        'q': q,
        'temperature_k': t,
        'formula': 'E = Edeg - (RT/nF) ln Q'
    }


def nernst_25c(e0: float, n: int, q: float) -> dict:
    """
    Calculate cell potential at 25degC using simplified Nernst equation.
    
    E = Edeg - (0.0592/n) log Q
    
    Args:
        e0: Standard cell potential (V)
        n: Moles of electrons transferred
        q: Reaction quotient
    
    Returns:
        Dictionary with cell potential
    
    Example:
        >>> nernst_25c(1.10, 2, 0.1)
        {'e': 1.129, 'e0': 1.10, 'n': 2, 'q': 0.1}
    """
    if q <= 0:
        return {'error': 'Q must be positive'}
    
    e = e0 - (0.0592 / n) * math.log10(q)
    
    return {
        'e': round(e, 4),
        'e0': e0,
        'n': n,
        'q': q,
        'temperature': '25degC',
        'formula': 'E = Edeg - (0.0592/n) log Q'
    }


def electrolysis_mass(current: float, time_s: float, 
                      molar_mass: float, n: int) -> dict:
    """
    Calculate mass produced in electrolysis.
    
    m = (M x I x t) / (n x F)
    
    Args:
        current: Current (A)
        time_s: Time (seconds)
        molar_mass: Molar mass (g/mol)
        n: Moles of electrons per mole of product
    
    Returns:
        Dictionary with mass produced
    
    Example:
        >>> electrolysis_mass(2.0, 3600, 63.55, 2)
        {'mass_g': 2.37, 'current_a': 2.0, 'time_s': 3600}
    """
    charge = current * time_s  # Coulombs
    moles_electrons = charge / F
    moles_product = moles_electrons / n
    mass = molar_mass * moles_product
    
    return {
        'mass_g': round(mass, 4),
        'current_a': current,
        'time_s': time_s,
        'time_h': round(time_s / 3600, 3),
        'charge_c': round(charge, 1),
        'moles_electrons': round(moles_electrons, 4),
        'moles_product': round(moles_product, 4),
        'molar_mass': molar_mass,
        'n': n,
        'formula': 'm = (M x I x t) / (n x F)'
    }


def electrolysis_charge(mass: float, molar_mass: float, n: int) -> dict:
    """
    Calculate charge needed to produce a given mass.
    
    Q = (m x n x F) / M
    
    Args:
        mass: Mass of product (g)
        molar_mass: Molar mass (g/mol)
        n: Moles of electrons per mole of product
    
    Returns:
        Dictionary with charge required
    """
    moles_product = mass / molar_mass
    moles_electrons = moles_product * n
    charge = moles_electrons * F
    
    return {
        'charge_c': round(charge, 1),
        'charge_ah': round(charge / 3600, 3),
        'moles_electrons': round(moles_electrons, 4),
        'moles_product': round(moles_product, 4)
    }


def equilibrium_constant_from_e0(e0: float, n: int, t: float = 298.15) -> dict:
    """
    Calculate equilibrium constant from standard cell potential.
    
    K = exp(nFEdeg/RT)
    
    At 25degC: log K = nEdeg/0.0592
    
    Args:
        e0: Standard cell potential (V)
        n: Moles of electrons
        t: Temperature (K)
    
    Returns:
        Dictionary with equilibrium constant
    
    Example:
        >>> equilibrium_constant_from_e0(0.46, 2)
        {'k': 3.2e+15, 'log_k': 15.5}
    """
    # K = exp(nFEdeg/RT)
    exponent = (n * F * e0) / (R * t)
    k = math.exp(exponent)
    
    return {
        'k': k if k < 1e50 else f'{k:.2e}',
        'log_k': round(math.log10(k), 2),
        'ln_k': round(exponent, 2),
        'e0': e0,
        'n': n,
        'temperature_k': t,
        'formula': 'K = exp(nFEdeg/RT)'
    }


def gibbs_from_cell_potential(e: float, n: int) -> dict:
    """
    Calculate Gibbs free energy from cell potential.
    
    DeltaG = -nFE
    
    Args:
        e: Cell potential (V)
        n: Moles of electrons
    
    Returns:
        Dictionary with Gibbs free energy
    
    Example:
        >>> gibbs_from_cell_potential(1.10, 2)
        {'delta_g_j': -212267, 'delta_g_kj': -212.3}
    """
    delta_g = -n * F * e  # Joules
    
    return {
        'delta_g_j': round(delta_g, 1),
        'delta_g_kj': round(delta_g / 1000, 2),
        'e': e,
        'n': n,
        'formula': 'DeltaG = -nFE'
    }


def cell_potential_from_gibbs(delta_g: float, n: int) -> dict:
    """
    Calculate cell potential from Gibbs free energy.
    
    E = -DeltaG / (nF)
    
    Args:
        delta_g: Gibbs free energy (J/mol)
        n: Moles of electrons
    
    Returns:
        Dictionary with cell potential
    """
    e = -delta_g / (n * F)
    
    return {
        'e': round(e, 4),
        'delta_g_j': delta_g,
        'delta_g_kj': round(delta_g / 1000, 2),
        'n': n
    }


def concentration_cell_potential(c_dilute: float, c_concentrated: float, 
                                  n: int = 1, t: float = 298.15) -> dict:
    """
    Calculate potential of a concentration cell.
    
    E = -(RT/nF) ln([dilute]/[concentrated])
    
    At 25degC: E = -(0.0592/n) log([dilute]/[concentrated])
    
    Args:
        c_dilute: Concentration of dilute solution (M)
        c_concentrated: Concentration of concentrated solution (M)
        n: Moles of electrons
        t: Temperature (K)
    
    Returns:
        Dictionary with concentration cell potential
    """
    if c_dilute <= 0 or c_concentrated <= 0:
        return {'error': 'Concentrations must be positive'}
    
    ratio = c_dilute / c_concentrated
    e = -(R * t / (n * F)) * math.log(ratio)
    
    return {
        'e': round(e, 4),
        'c_dilute': c_dilute,
        'c_concentrated': c_concentrated,
        'ratio': round(ratio, 4),
        'n': n,
        'note': 'Concentration cell: Edeg = 0, potential from concentration gradient'
    }


# Problem set for testing
TEXTBOOK_PROBLEMS = [
    {
        "id": "EC-01",
        "question": "Nernst for Zn-Cu cell (Q=0.1)",
        "e0": 1.10,
        "n": 2,
        "q": 0.1,
        "expected_e_approx": 1.13
    },
    {
        "id": "EC-02",
        "question": "Electrolysis of Cu (2A, 1h)",
        "current": 2.0,
        "time": 3600,
        "mm": 63.55,
        "n": 2,
        "expected_mass_approx": 2.37
    },
    {
        "id": "EC-03",
        "question": "K from Edeg=0.46V, n=2",
        "e0": 0.46,
        "n": 2,
        "expected_log_k_approx": 15.5
    },
    {
        "id": "EC-04",
        "question": "Concentration cell 0.1M vs 1.0M",
        "c_dilute": 0.1,
        "c_concentrated": 1.0,
        "n": 1,
        "expected_e_approx": 0.059
    },
]


if __name__ == "__main__":
    print("Advanced Electrochemistry Tools")
    print("=" * 40)
    
    # Test Nernst
    print("\nNernst Equation:")
    result = nernst_potential(1.10, 2, 0.1)
    print(f"  Zn-Cu cell, Q=0.1: E = {result['e']} V")
    
    # Test electrolysis
    print("\nElectrolysis:")
    result = electrolysis_mass(2.0, 3600, 63.55, 2)
    print(f"  Cu from 2A for 1h: {result['mass_g']} g")
    
    # Test equilibrium constant
    print("\nEquilibrium Constant:")
    result = equilibrium_constant_from_e0(0.46, 2)
    print(f"  Edeg=0.46V, n=2: log K = {result['log_k']}")
    
    # Test concentration cell
    print("\nConcentration Cell:")
    result = concentration_cell_potential(0.1, 1.0, 1)
    print(f"  0.1M vs 1.0M: E = {result['e']} V")


# MCP Tool Declarations
MCP_TOOLS = [
    {
        "name": "cell_potential_from_gibbs",
        "description": "Calculate cell potential from Gibbs free energy.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "delta_g": {
                    "type": "number",
                    "description": "Delta G"
                },
                "n": {
                    "type": "number",
                    "description": "N"
                }
            },
            "required": [
                "delta_g",
                "n"
            ]
        }
    },
    {
        "name": "concentration_cell_potential",
        "description": "Calculate potential of a concentration cell.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "c_dilute": {
                    "type": "number",
                    "description": "C Dilute"
                },
                "c_concentrated": {
                    "type": "number",
                    "description": "C Concentrated"
                },
                "n": {
                    "type": "number",
                    "description": "N",
                    "default": 1
                },
                "t": {
                    "type": "number",
                    "description": "T",
                    "default": 298.15
                }
            },
            "required": [
                "c_dilute",
                "c_concentrated"
            ]
        }
    },
    {
        "name": "electrolysis_charge",
        "description": "Calculate charge needed to produce a given mass.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "mass": {
                    "type": "number",
                    "description": "Mass"
                },
                "molar_mass": {
                    "type": "number",
                    "description": "Molar Mass"
                },
                "n": {
                    "type": "number",
                    "description": "N"
                }
            },
            "required": [
                "mass",
                "molar_mass",
                "n"
            ]
        }
    },
    {
        "name": "electrolysis_mass",
        "description": "Calculate mass produced in electrolysis.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "current": {
                    "type": "number",
                    "description": "Current"
                },
                "time_s": {
                    "type": "number",
                    "description": "Time S"
                },
                "molar_mass": {
                    "type": "number",
                    "description": "Molar Mass"
                },
                "n": {
                    "type": "number",
                    "description": "N"
                }
            },
            "required": [
                "current",
                "time_s",
                "molar_mass",
                "n"
            ]
        }
    },
    {
        "name": "equilibrium_constant_from_e0",
        "description": "Calculate equilibrium constant from standard cell potential.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "e0": {
                    "type": "number",
                    "description": "E0"
                },
                "n": {
                    "type": "number",
                    "description": "N"
                },
                "t": {
                    "type": "number",
                    "description": "T",
                    "default": 298.15
                }
            },
            "required": [
                "e0",
                "n"
            ]
        }
    },
    {
        "name": "gibbs_from_cell_potential",
        "description": "Calculate Gibbs free energy from cell potential.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "e": {
                    "type": "number",
                    "description": "E"
                },
                "n": {
                    "type": "number",
                    "description": "N"
                }
            },
            "required": [
                "e",
                "n"
            ]
        }
    },
    {
        "name": "nernst_25c",
        "description": "Calculate cell potential at 25degC using simplified Nernst equation.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "e0": {
                    "type": "number",
                    "description": "E0"
                },
                "n": {
                    "type": "number",
                    "description": "N"
                },
                "q": {
                    "type": "number",
                    "description": "Q"
                }
            },
            "required": [
                "e0",
                "n",
                "q"
            ]
        }
    },
    {
        "name": "nernst_potential",
        "description": "Calculate cell potential at non-standard conditions.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "e0": {
                    "type": "number",
                    "description": "E0"
                },
                "n": {
                    "type": "number",
                    "description": "N"
                },
                "q": {
                    "type": "number",
                    "description": "Q"
                },
                "t": {
                    "type": "number",
                    "description": "T",
                    "default": 298.15
                }
            },
            "required": [
                "e0",
                "n",
                "q"
            ]
        }
    }
]