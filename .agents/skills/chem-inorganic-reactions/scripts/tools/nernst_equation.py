"""
Nernst Equation Tools - L3 Implementation
Electrochemistry: Cell potential and concentration relationships

Provides core electrochemical calculations including:
- Cell potential under non-standard conditions
- Concentration cell calculations
- Equilibrium constant from cell potential
- Free energy relationships

## Solver Instructions (for AI Agent)

When you encounter a Nernst equation problem, follow this decision tree:

### Step 1: Identify what is given and what is asked
Extract from the question text:
- Standard cell potential Edeg: Usually given or calculated from reduction potentials
- Concentrations: Of products and reactants
- Number of electrons n: From balanced half-reactions
- Temperature T: Default 298.15 K if not given
- Reaction quotient Q: May need to calculate from concentrations

### Step 2: Choose the correct function
| Scenario | Function Call |
|----------|---------------|
| Calculate E under non-standard conditions | `nernst_equation(E0, n, Q, T)` |
| Calculate reaction quotient Q | `reaction_quotient(concentrations_products, concentrations_reactants, stoich_products, stoich_reactants)` |
| Calculate concentration cell potential | `concentration_cell_potential(n, c_anode, c_cathode, T)` |
| Calculate K from Edeg | `equilibrium_constant_from_potential(E0, n, T)` |
| Calculate Edeg from K | `cell_potential_from_K(E0, n, K)` |
| Calculate DeltaG from E | `free_energy_from_potential(E, n)` |
| Calculate E from DeltaG | `potential_from_free_energy(dG, n)` |
| Calculate pH from hydrogen electrode | `ph_from_hydrogen_electrode(E, T)` |
| Calculate E from pH | `potential_from_ph(pH, T)` |
| Get Nernst factor (0.05916 V at 25degC) | `nernst_factor(T)` |

### Step 3: Handle special cases
- **Nernst equation**: E = Edeg - (0.05916/n) x log(Q) at 25degC
- **Q calculation**: Q = [products]^coeff / [reactants]^coeff; omit solids and pure liquids
- **Concentration cell**: Edeg = 0, E = (0.05916/n) x log(c_cathode/c_anode)
- **DeltaG relationship**: DeltaG = -nFE
- **K relationship**: log K = nEdeg/0.05916 at 25degC
- **Temperature**: Default 298.15 K; adjust factor for other temperatures

### Examples

**Example 1: Non-standard cell potential**
Question: "Calculate E for Zn|Zn2+(0.1 M)||Cu2+(1.0 M)|Cu. Edeg = 1.10 V, n = 2."
- Given: Edeg = 1.10 V, Q = [Zn2+]/[Cu2+] = 0.1/1.0 = 0.1, n = 2
- Solution: `nernst_equation(E0=1.10, n=2, Q=0.1, T=298.15)` -> E ~ 1.13 V

**Example 2: Concentration cell**
Question: "What is the potential of a concentration cell with [Cu2+]_anode = 0.01 M and [Cu2+]_cathode = 1.0 M?"
- Solution: `concentration_cell_potential(n=2, c_anode=0.01, c_cathode=1.0)` -> E ~ 0.059 V

**Example 3: K from Edeg**
Question: "Calculate K for a cell with Edeg = 0.46 V, n = 2."
- Solution: `equilibrium_constant_from_potential(E0=0.46, n=2)` -> K ~ 3 x 1015

**Example 4: DeltaG from E**
Question: "Calculate DeltaG for a cell with E = 1.10 V, n = 2."
- Solution: `free_energy_from_potential(E=1.10, n=2)` -> DeltaG ~ -212 kJ/mol
"""

from typing import Tuple, Optional, Dict
from math import log10, log


# Physical constants
F = 96485.3329  # Faraday constant (C/mol)
R = 8.314462618  # Gas constant (J/(mol·K))


def nernst_equation(E0: float, n: float, Q: float, T: float = 298.15) -> float:
    """
    Calculate cell potential using the Nernst equation.
    
    E = Edeg - (RT/nF) ln(Q)
    
    At 25degC (298.15 K), this simplifies to:
    E = Edeg - (0.05916/n) log10(Q)
    
    Args:
        E0: Standard cell potential (V)
        n: Number of electrons transferred
        Q: Reaction quotient (products/reactants)
        T: Temperature (K), default 298.15 K (25degC)
    
    Returns:
        Cell potential (V)
    
    Examples:
        >>> E = nernst_equation(0.76, 2, 0.01)  # Zn/Cu cell
        >>> round(E, 3)
        0.819
        >>> E = nernst_equation(1.10, 2, 1.0)  # Standard conditions
        >>> E
        1.1
    """
    if Q <= 0:
        raise ValueError("Reaction quotient Q must be positive")
    
    # Calculate the Nernst factor at given temperature
    factor = (R * T) / (n * F)
    
    # E = Edeg - (RT/nF) ln(Q)
    E = E0 - factor * log(Q)
    
    return E


def nernst_equation_25C(E0: float, n: float, Q: float) -> float:
    """
    Calculate cell potential at 25degC using simplified Nernst equation.
    
    E = Edeg - (0.05916/n) log10(Q)
    
    Args:
        E0: Standard cell potential (V)
        n: Number of electrons transferred
        Q: Reaction quotient
    
    Returns:
        Cell potential (V)
    
    Examples:
        >>> E = nernst_equation_25C(0.46, 2, 100)
        >>> round(E, 3)
        0.401
    """
    if Q <= 0:
        raise ValueError("Reaction quotient Q must be positive")
    
    return E0 - (0.05916 / n) * log10(Q)


def reaction_quotient(concentrations_products: Dict[str, float],
                       concentrations_reactants: Dict[str, float],
                       stoich_products: Optional[Dict[str, float]] = None,
                       stoich_reactants: Optional[Dict[str, float]] = None) -> float:
    """
    Calculate reaction quotient Q from concentrations.
    
    Q = Π([products]^coefficients) / Π([reactants]^coefficients)
    
    Args:
        concentrations_products: Dict of {species: concentration} for products
        concentrations_reactants: Dict of {species: concentration} for reactants
        stoich_products: Stoichiometric coefficients for products (default 1)
        stoich_reactants: Stoichiometric coefficients for reactants (default 1)
    
    Returns:
        Reaction quotient Q
    
    Examples:
        >>> # For reaction: Zn(s) + Cu2+ -> Zn2+ + Cu(s)
        >>> # Q = [Zn2+] / [Cu2+] (solids have activity = 1)
        >>> Q = reaction_quotient({'Zn2+': 0.1}, {'Cu2+': 1.0})
        >>> Q
        0.1
    """
    # Calculate numerator (products)
    numerator = 1.0
    for species, conc in concentrations_products.items():
        if conc <= 0:
            continue  # Skip species with zero concentration
        coeff = stoich_products.get(species, 1) if stoich_products else 1
        numerator *= conc ** coeff
    
    # Calculate denominator (reactants)
    denominator = 1.0
    for species, conc in concentrations_reactants.items():
        if conc <= 0:
            continue
        coeff = stoich_reactants.get(species, 1) if stoich_reactants else 1
        denominator *= conc ** coeff
    
    return numerator / denominator


def concentration_cell_potential(n: float, 
                                  c_anode: float, 
                                  c_cathode: float,
                                  T: float = 298.15) -> float:
    """
    Calculate potential of a concentration cell.
    
    E = (RT/nF) ln(c_cathode/c_anode)
    
    For a concentration cell, Edeg = 0 (same electrode materials)
    
    Args:
        n: Number of electrons transferred
        c_anode: Concentration at anode (M)
        c_cathode: Concentration at cathode (M)
        T: Temperature (K)
    
    Returns:
        Cell potential (V)
    
    Examples:
        >>> E = concentration_cell_potential(1, 0.01, 0.1)  # 10x difference
        >>> round(E, 4)
        0.0592
        >>> E = concentration_cell_potential(2, 0.01, 0.1)
        >>> round(E, 4)
        0.0296
    """
    if c_anode <= 0 or c_cathode <= 0:
        raise ValueError("Concentrations must be positive")
    
    ratio = c_cathode / c_anode
    factor = (R * T) / (n * F)
    
    return factor * log(ratio)


def cell_potential_from_half_reactions(E0_cathode: float, 
                                        E0_anode: float,
                                        n: float,
                                        Q: float = 1.0,
                                        T: float = 298.15) -> float:
    """
    Calculate cell potential from half-reaction potentials.
    
    Edeg_cell = Edeg_cathode - Edeg_anode
    
    Args:
        E0_cathode: Standard reduction potential of cathode (V)
        E0_anode: Standard reduction potential of anode (V)
        n: Number of electrons transferred
        Q: Reaction quotient (default 1 for standard conditions)
        T: Temperature (K)
    
    Returns:
        Cell potential (V)
    
    Examples:
        >>> # Zn/Cu galvanic cell
        >>> E = cell_potential_from_half_reactions(0.34, -0.76, 2)  # Cu2+/Cu, Zn2+/Zn
        >>> round(E, 2)
        1.1
    """
    E0_cell = E0_cathode - E0_anode
    return nernst_equation(E0_cell, n, Q, T)


def equilibrium_constant_from_potential(E0: float, n: float, T: float = 298.15) -> float:
    """
    Calculate equilibrium constant K from standard cell potential.
    
    K = exp(nFEdeg/RT)
    
    Also: log10(K) = nEdeg/0.05916 at 25degC
    
    Args:
        E0: Standard cell potential (V)
        n: Number of electrons transferred
        T: Temperature (K)
    
    Returns:
        Equilibrium constant K
    
    Examples:
        >>> K = equilibrium_constant_from_potential(0.46, 2)
        >>> round(K, 0)
        3.0e+15
        >>> K = equilibrium_constant_from_potential(1.10, 2)  # Zn/Cu
        >>> K > 1e30
        True
    """
    # K = exp(nFEdeg/RT)
    exponent = (n * F * E0) / (R * T)
    return 10 ** (exponent / log(10))


def cell_potential_from_K(E0: float, n: float, K: float) -> float:
    """
    Calculate standard cell potential from equilibrium constant.
    
    Edeg = (RT/nF) ln(K) = (0.05916/n) log10(K) at 25degC
    
    Args:
        E0: Not used, kept for API consistency
        n: Number of electrons transferred
        K: Equilibrium constant
    
    Returns:
        Standard cell potential (V)
    
    Examples:
        >>> # Reverse calculation
        >>> E0_calc = cell_potential_from_K(0, 2, 3e15)
        >>> round(E0_calc, 2)
        0.46
    """
    if K <= 0:
        raise ValueError("Equilibrium constant must be positive")
    
    return (0.05916 / n) * log10(K)


def free_energy_from_potential(E: float, n: float) -> float:
    """
    Calculate Gibbs free energy change from cell potential.
    
    DeltaG = -nFE
    
    Args:
        E: Cell potential (V)
        n: Number of electrons transferred
    
    Returns:
        DeltaG in Joules per mole
    
    Examples:
        >>> dG = free_energy_from_potential(1.10, 2)  # Zn/Cu cell
        >>> round(dG / 1000, 1)  # kJ/mol
        -212.3
    """
    return -n * F * E


def potential_from_free_energy(dG: float, n: float) -> float:
    """
    Calculate cell potential from Gibbs free energy change.
    
    E = -DeltaG/(nF)
    
    Args:
        dG: Gibbs free energy change (J/mol)
        n: Number of electrons transferred
    
    Returns:
        Cell potential (V)
    
    Examples:
        >>> E = potential_from_free_energy(-212267, 2)
        >>> round(E, 2)
        1.1
    """
    return -dG / (n * F)


def standard_free_energy_from_potential(E0: float, n: float) -> float:
    """
    Calculate standard Gibbs free energy change from standard cell potential.
    
    DeltaGdeg = -nFEdeg
    
    Args:
        E0: Standard cell potential (V)
        n: Number of electrons transferred
    
    Returns:
        DeltaGdeg in Joules per mole
    
    Examples:
        >>> dG0 = standard_free_energy_from_potential(1.10, 2)
        >>> round(dG0 / 1000, 1)  # kJ/mol
        -212.3
    """
    return -n * F * E0


def ph_from_hydrogen_electrode(E: float, T: float = 298.15) -> float:
    """
    Calculate pH from hydrogen electrode potential.
    
    For 2H+ + 2e- -> H2, E = -0.05916 x pH (at 1 atm H2)
    
    pH = -E / 0.05916
    
    Args:
        E: Measured electrode potential vs SHE (V)
        T: Temperature (K)
    
    Returns:
        pH value
    
    Examples:
        >>> ph = ph_from_hydrogen_electrode(-0.30)
        >>> round(ph, 1)
        5.1
    """
    # E = Edeg - (0.05916/2) x log(1/[H+]2) = -0.05916 x pH
    # So pH = -E / 0.05916
    factor = (R * T * log(10)) / F
    return -E / factor


def potential_from_ph(pH: float, T: float = 298.15) -> float:
    """
    Calculate hydrogen electrode potential at given pH.
    
    E = -0.05916 x pH (at 25degC, 1 atm H2)
    
    Args:
        pH: pH value
        T: Temperature (K)
    
    Returns:
        Electrode potential (V)
    
    Examples:
        >>> E = potential_from_ph(7.0)
        >>> round(E, 3)
        -0.414
    """
    factor = (R * T * log(10)) / F
    return -factor * pH


def nernst_factor(T: float = 298.15) -> float:
    """
    Calculate the Nernst factor (RT/F x ln(10) = 0.05916 V at 25degC).
    
    This is the factor for: E = Edeg - (factor/n) x log10(Q)
    
    Args:
        T: Temperature (K)
    
    Returns:
        Nernst factor in Volts
    
    Examples:
        >>> factor = nernst_factor()
        >>> round(factor, 5)
        0.05916
    """
    return (R * T * log(10)) / F


def temperature_correction_factor(T: float) -> float:
    """
    Calculate temperature correction for the Nernst equation.
    
    Returns RT/F in volts.
    
    Args:
        T: Temperature (K)
    
    Returns:
        RT/F in Volts
    
    Examples:
        >>> factor = temperature_correction_factor(298.15)
        >>> round(factor * 1000, 2)  # mV
        25.69
    """
    return (R * T) / F


if __name__ == "__main__":
    """Example usage and simple tests."""
    import math
    
    print("=" * 60)
    print("Nernst Equation Tools - Example Usage")
    print("=" * 60)
    
    # Example 1: Zn/Cu galvanic cell
    print("\n--- Example 1: Zn/Cu Galvanic Cell ---")
    E0_cell = 1.10  # V
    n = 2
    
    # At standard conditions
    E_standard = nernst_equation(E0_cell, n, 1.0)
    print(f"Standard cell potential: {E_standard:.3f} V")
    
    # With [Zn2+] = 0.1 M, [Cu2+] = 1.0 M
    Q = 0.1 / 1.0
    E_nonstandard = nernst_equation(E0_cell, n, Q)
    print(f"With [Zn2+]=0.1 M, [Cu2+]=1.0 M: {E_nonstandard:.3f} V")
    
    # Equilibrium constant
    K = equilibrium_constant_from_potential(E0_cell, n)
    print(f"Equilibrium constant K: {K:.2e}")
    
    # Free energy
    dG = free_energy_from_potential(E0_cell, n)
    print(f"DeltaGdeg = {dG/1000:.1f} kJ/mol")
    
    # Example 2: Concentration cell
    print("\n--- Example 2: Concentration Cell ---")
    E_conc = concentration_cell_potential(2, 0.001, 0.1)
    print(f"Concentration cell (10^3x difference, n=2): {E_conc*1000:.1f} mV")
    
    E_conc2 = concentration_cell_potential(1, 0.001, 0.1)
    print(f"Concentration cell (10^3x difference, n=1): {E_conc2*1000:.1f} mV")
    
    # Example 3: pH from electrode
    print("\n--- Example 3: pH Measurement ---")
    pH = ph_from_hydrogen_electrode(-0.30)
    print(f"pH from E = -0.30 V: {pH:.1f}")
    
    E_pH7 = potential_from_ph(7.0)
    print(f"Potential at pH 7.0: {E_pH7:.3f} V")
    
    # Example 4: Nernst factor at different temperatures
    print("\n--- Example 4: Temperature Effects ---")
    print(f"Nernst factor at 25degC: {nernst_factor(298.15)*1000:.2f} mV")
    print(f"Nernst factor at 37degC: {nernst_factor(310.15)*1000:.2f} mV")
    
    # Verify relationships
    print("\n--- Verification ---")
    # Verify E -> K -> E
    K_calc = equilibrium_constant_from_potential(0.46, 2)
    E_calc = cell_potential_from_K(0, 2, K_calc)
    print(f"Edeg = 0.46 V -> K = {K_calc:.2e} -> Edeg = {E_calc:.3f} V")
    
    # Verify DeltaG -> E -> DeltaG
    dG_test = -100000  # J/mol
    E_test = potential_from_free_energy(dG_test, 2)
    dG_back = free_energy_from_potential(E_test, 2)
    print(f"DeltaG = -100 kJ/mol -> E = {E_test:.3f} V -> DeltaG = {dG_back/1000:.1f} kJ/mol")
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)
