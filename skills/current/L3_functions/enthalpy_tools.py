"""
Enthalpy and Thermochemistry Tools (L3)
Source: LibreTexts Chemistry 2e Ch05.03

## Solver Instructions (for AI Agent)

When you encounter an enthalpy problem, follow this decision tree:

### Step 1: Identify what is given and what is asked
Extract from the question text:
- Formation enthalpies (DeltaHdegf): Look for tables or values in kJ/mol
- Reaction equation: Extract chemical formulas and states (g), (l), (s), (aq)
- Hess's Law data: Multiple reactions with DeltaH values to combine
- Phase change: Look for "melting", "freezing", "vaporization", "condensation"
- Combustion: Look for "combustion", "burning", often given as DeltaH_comb

### Step 2: Choose the correct function
| Scenario | Function Call |
|----------|---------------|
| Calculate DeltaHdegrxn from formation data | `delta_H_rxn_from_formation(reactants, products, delta_H_f_data)` |
| Apply Hess's Law to combine reactions | `hess_from_reactions(reaction_data)` |
| Reverse a reaction (flip DeltaH sign) | `reverse_reaction(delta_H)` |
| Multiply reaction by factor | `multiply_reaction(delta_H, factor)` |
| Calculate heat of combustion per gram | `heat_of_combustion_per_gram(delta_H_comb, molar_mass)` |
| Calculate heat of combustion per volume | `heat_of_combustion_per_volume(delta_H_comb, molar_mass, density)` |
| Calculate heat for phase change | `heat_phase_change(moles, delta_H_phase)` |
| Calculate total heat with phase change | `total_heat_with_phase_change(moles, c_solid, c_liquid, DeltaT_solid, DeltaT_liquid, DeltaH_fusion)` |
| Integrate polynomial Cp (A+BT+CT²+DT³) | `integrated_cp_poly(A, B, C, D, T1, T2)` |

### Step 3: Handle special cases
- **Formation enthalpies**: Elements in standard state have DeltaHdegf = 0
- **Hess's Law**: Can add reactions, reverse (flip sign), or multiply (scale DeltaH)
- **Phase changes**: DeltaH_fusion (solid↔liquid), DeltaH_vaporization (liquid↔gas)
- **Combustion**: Always exothermic (negative DeltaH), produces CO2 and H2O
- **Units**: Most enthalpies in kJ/mol; watch for kJ vs J
- **Polynomial Cp**: Use `integrated_cp_poly` for Cp = A + BT + CT² + DT³. 
  The integral is ∫Cp dT = A(T₂-T₁) + B/2(T₂²-T₁²) + C/3(T₂³-T₁³) + D/4(T₂⁴-T₁⁴).
  Pass the polynomial coefficients and temperature range directly.
- **Mixtures**: For equimolar binary mixtures, calculate each component separately 
  then sum. Do NOT average the Cp polynomials and integrate once — while algebraically 
  equivalent, per-component calculation is clearer and matches textbook solutions.

### Examples

**Example 1: DeltaHdegrxn from formation**
Question: "Calculate DeltaHdeg for CH4 + 2O2 -> CO2 + 2H2O(l)"
- Given: DeltaHdegf(CH4) = -74.8, DeltaHdegf(CO2) = -393.5, DeltaHdegf(H2O,l) = -285.8 kJ/mol, O2 = 0
- Solution: `delta_H_rxn_from_formation(reactants=[('CH4(g)',1),('O2(g)',2)], products=[('CO2(g)',1),('H2O(l)',2)])` -> -890 kJ/mol

**Example 2: Hess's Law**
Question: "Find DeltaH for C + ½O2 -> CO given: C + O2 -> CO2 (DeltaH=-393.5 kJ), CO + ½O2 -> CO2 (DeltaH=-283.0 kJ)"
- Solution: Reverse second reaction (+283.0) and add to first (-393.5 + 283.0) = -110.5 kJ
- `hess_from_reactions([{'coeff': 1, 'delta_H': -393.5}, {'coeff': -1, 'delta_H': -283.0}])`

**Example 3: Heat of combustion per gram**
Question: "What is the heat released per gram of methane? (DeltaH_comb = -890 kJ/mol, M = 16 g/mol)"
- Solution: `heat_of_combustion_per_gram(delta_H_comb=-890, molar_mass=16)` -> 55.6 kJ/g
"""

# === STANDARD ENTHALPIES OF FORMATION ===

# Common DeltaHdegf values in kJ/mol
STANDARD_ENTHALPIES_FORMATION = {
    # Elements (standard state) = 0 by definition
    'H2(g)': 0,
    'O2(g)': 0,
    'N2(g)': 0,
    'C(s,graphite)': 0,
    'S(s)': 0,
    'Na(s)': 0,
    'Cl2(g)': 0,
    
    # Common compounds
    'H2O(l)': -285.8,
    'H2O(g)': -241.8,
    'CO2(g)': -393.5,
    'CO(g)': -110.5,
    'CH4(g)': -74.8,
    'C2H6(g)': -84.7,
    'C2H4(g)': 52.4,
    'C2H2(g)': 226.7,
    'C3H8(g)': -103.8,
    'C4H10(g)': -126.1,
    'C2H5OH(l)': -277.7,
    'C2H5OH(g)': -235.1,
    'CH3OH(l)': -238.7,
    'NH3(g)': -46.1,
    'NO(g)': 90.3,
    'NO2(g)': 33.2,
    'N2O(g)': 82.0,
    'SO2(g)': -296.8,
    'SO3(g)': -395.7,
    'H2S(g)': -20.6,
    'HCl(g)': -92.3,
    'HBr(g)': -36.4,
    'HI(g)': 26.5,
    'HF(g)': -271.1,
    'NaCl(s)': -411.2,
    'NaOH(s)': -425.6,
    'Na2CO3(s)': -1130.7,
    'CaO(s)': -635.1,
    'CaCO3(s)': -1206.9,
    'Ca(OH)2(s)': -986.1,
    'MgO(s)': -601.6,
    'Al2O3(s)': -1675.7,
    'Fe2O3(s)': -825.5,
    'Fe3O4(s)': -1118.4,
}

# Standard enthalpies of phase change (kJ/mol)
ENTHALPIES_PHASE_CHANGE = {
    'H2O_fusion': 6.01,
    'H2O_vaporization': 40.7,
    'H2O_sublimation': 46.7,
}


def delta_H_rxn_from_formation(reactants, products, delta_H_f_data=None):
    """
    Calculate standard enthalpy of reaction from formation enthalpies.
    
    DeltaHdeg_rxn = Σ(n x DeltaHdeg_f products) - Σ(n x DeltaHdeg_f reactants)
    
    Parameters:
        reactants: list of tuples [(formula, coefficient), ...]
        products: list of tuples [(formula, coefficient), ...]
        delta_H_f_data: optional dict of DeltaHdegf values (uses default if None)
    
    Returns:
        DeltaHdeg_rxn in kJ/mol
    """
    if delta_H_f_data is None:
        delta_H_f_data = STANDARD_ENTHALPIES_FORMATION
    
    # Sum of products
    products_sum = 0
    for formula, coeff in products:
        if formula not in delta_H_f_data:
            raise ValueError(f"DeltaHdegf not found for {formula}")
        products_sum += coeff * delta_H_f_data[formula]
    
    # Sum of reactants
    reactants_sum = 0
    for formula, coeff in reactants:
        if formula not in delta_H_f_data:
            raise ValueError(f"DeltaHdegf not found for {formula}")
        reactants_sum += coeff * delta_H_f_data[formula]
    
    return products_sum - reactants_sum


def hess_law_combine(reactions, target_reaction=None):
    """
    Apply Hess's Law to combine reaction enthalpies.
    
    Parameters:
        reactions: list of tuples [(equation_str, delta_H), ...]
                  negative coefficient means reverse reaction
        target_reaction: optional, the target reaction to verify
    
    Returns:
        combined DeltaH in kJ
    """
    total_delta_H = 0
    for equation, delta_H in reactions:
        total_delta_H += delta_H
    return total_delta_H


def reverse_reaction(delta_H):
    """Reverse a reaction (multiply DeltaH by -1)."""
    return -delta_H


def multiply_reaction(delta_H, factor):
    """Multiply reaction by factor (multiply DeltaH by factor)."""
    return delta_H * factor


# === HESS'S LAW CALCULATIONS ===

def hess_from_reactions(reaction_data, target_delta_H_f=None):
    """
    Calculate unknown enthalpy using Hess's Law.
    
    Parameters:
        reaction_data: list of dicts with 'coeff', 'delta_H' keys
                      coeff = multiplier (negative for reverse)
        target_delta_H_f: optional, for verification
    
    Returns:
        calculated DeltaH in kJ
    """
    total = 0
    for rxn in reaction_data:
        total += rxn['coeff'] * rxn['delta_H']
    return total


# === ENTHALPY OF COMBUSTION ===

def heat_of_combustion_per_gram(delta_H_comb, molar_mass):
    """
    Calculate heat released per gram of fuel.
    
    Parameters:
        delta_H_comb: enthalpy of combustion in kJ/mol
        molar_mass: molar mass in g/mol
    
    Returns:
        heat per gram in kJ/g
    """
    return abs(delta_H_comb) / molar_mass


def heat_of_combustion_per_volume(delta_H_comb, molar_mass, density):
    """
    Calculate heat released per volume of liquid fuel.
    
    Parameters:
        delta_H_comb: enthalpy of combustion in kJ/mol
        molar_mass: molar mass in g/mol
        density: density in g/mL
    
    Returns:
        heat per mL in kJ/mL
    """
    heat_per_gram = heat_of_combustion_per_gram(delta_H_comb, molar_mass)
    return heat_per_gram * density


# === PHASE CHANGE ENTHALPIES ===

ENTHALPIES_PHASE_CHANGE = {
    'H2O_fusion': 6.01,      # kJ/mol (melting/freezing)
    'H2O_vaporization': 40.7, # kJ/mol (boiling/condensing)
    'H2O_sublimation': 46.7,  # kJ/mol
}


def heat_phase_change(moles, delta_H_phase):
    """
    Calculate heat for phase change.
    
    q = n x DeltaH_phase
    
    Parameters:
        moles: amount in mol
        delta_H_phase: enthalpy of phase change in kJ/mol
    
    Returns:
        heat in kJ
    """
    return moles * delta_H_phase


def total_heat_with_phase_change(moles, c_solid, c_liquid, delta_T_solid, delta_T_liquid, delta_H_fusion):
    """
    Calculate total heat for temperature change through phase transition.
    
    q_total = q_solid + q_fusion + q_liquid
    
    Parameters:
        moles: amount in mol
        c_solid: specific heat of solid (J/g·degC)
        c_liquid: specific heat of liquid (J/g·degC)
        delta_T_solid: temperature change in solid phase
        delta_T_liquid: temperature change in liquid phase
        delta_H_fusion: enthalpy of fusion in kJ/mol
    
    Returns:
        total heat in kJ
    """
    molar_mass_water = 18.02  # g/mol
    
    q_solid = moles * molar_mass_water * c_solid * delta_T_solid / 1000  # J to kJ
    q_fusion = moles * delta_H_fusion
    q_liquid = moles * molar_mass_water * c_liquid * delta_T_liquid / 1000
    
    return q_solid + q_fusion + q_liquid


if __name__ == "__main__":
    print("Enthalpy tools - implemented")
    
    # Test DeltaH_rxn from formation
    # CH4 + 2O2 -> CO2 + 2H2O
    delta_H = delta_H_rxn_from_formation(
        reactants=[('CH4(g)', 1), ('O2(g)', 2)],
        products=[('CO2(g)', 1), ('H2O(l)', 2)]
    )
    print(f"DeltaH for CH4 combustion: {delta_H:.1f} kJ/mol")
    
    # Test Hess's Law
    # C + O2 -> CO2: -393.5 kJ
    # CO + 0.5O2 -> CO2: -283.0 kJ
    # Want: C + 0.5O2 -> CO
    # = (-393.5) - (-283.0) = -110.5 kJ
    delta_H = hess_from_reactions([
        {'coeff': 1, 'delta_H': -393.5},
        {'coeff': -1, 'delta_H': -283.0}
    ])
    print(f"DeltaH for C + 0.5O2 -> CO: {delta_H:.1f} kJ/mol")


# MCP Tool Declarations
MCP_TOOLS = [
    {
        "name": "delta_H_rxn_from_formation",
        "description": "Calculate standard enthalpy of reaction from formation enthalpies.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "reactants": {"type": "number", "description": "Reactants"},
                "products": {"type": "number", "description": "Products"},
                "delta_H_f_data": {"type": "number", "description": "Delta H F Data", "default": None},
            },
            "required": ["reactants", "products"]
        }
    },
    {
        "name": "heat_of_combustion_per_gram",
        "description": "Calculate heat released per gram of fuel.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "delta_H_comb": {"type": "number", "description": "Delta H Comb"},
                "molar_mass": {"type": "number", "description": "Molar Mass"},
            },
            "required": ["delta_H_comb", "molar_mass"]
        }
    },
    {
        "name": "heat_of_combustion_per_volume",
        "description": "Calculate heat released per volume of liquid fuel.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "delta_H_comb": {"type": "number", "description": "Delta H Comb"},
                "molar_mass": {"type": "number", "description": "Molar Mass"},
                "density": {"type": "number", "description": "Density"},
            },
            "required": ["delta_H_comb", "molar_mass", "density"]
        }
    },
    {
        "name": "heat_phase_change",
        "description": "Calculate heat for phase change.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "moles": {"type": "number", "description": "Moles"},
                "delta_H_phase": {"type": "number", "description": "Delta H Phase"},
            },
            "required": ["moles", "delta_H_phase"]
        }
    },
    {
        "name": "hess_from_reactions",
        "description": "Calculate unknown enthalpy using Hess's Law.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "reaction_data": {"type": "number", "description": "Reaction Data"},
                "target_delta_H_f": {"type": "number", "description": "Target Delta H F", "default": None},
            },
            "required": ["reaction_data"]
        }
    },
    {
        "name": "hess_law_combine",
        "description": "Apply Hess's Law to combine reaction enthalpies.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "reactions": {"type": "number", "description": "Reactions"},
                "target_reaction": {"type": "number", "description": "Target Reaction", "default": None},
            },
            "required": ["reactions"]
        }
    },
    {
        "name": "multiply_reaction",
        "description": "Multiply reaction by factor (multiply \u0394H by factor).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "delta_H": {"type": "number", "description": "Delta H"},
                "factor": {"type": "number", "description": "Factor"},
            },
            "required": ["delta_H", "factor"]
        }
    },
    {
        "name": "reverse_reaction",
        "description": "Reverse a reaction (multiply \u0394H by -1).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "delta_H": {"type": "number", "description": "Delta H"},
            },
            "required": ["delta_H"]
        }
    },
    {
        "name": "total_heat_with_phase_change",
        "description": "Calculate total heat for temperature change through phase transition.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "moles": {"type": "number", "description": "Moles"},
                "c_solid": {"type": "number", "description": "C Solid"},
                "c_liquid": {"type": "number", "description": "C Liquid"},
                "delta_T_solid": {"type": "number", "description": "Delta T Solid"},
                "delta_T_liquid": {"type": "number", "description": "Delta T Liquid"},
                "delta_H_fusion": {"type": "number", "description": "Delta H Fusion"},
            },
            "required": ["moles", "c_solid", "c_liquid", "delta_T_solid", "delta_T_liquid", "delta_H_fusion"]
        }
    }
]


def integrated_cp_poly(A, B, C, D, T1, T2):
    """
    Integrate polynomial heat capacity Cp = A + BT + CT² + DT³ from T1 to T2.

    Returns ∫(A + BT + CT² + DT³)dT from T1 to T2
    = A(T₂-T₁) + (B/2)(T₂²-T₁²) + (C/3)(T₂³-T₁³) + (D/4)(T₂⁴-T₁⁴)

    Parameters:
        A (float): Cp coefficient for T⁰ term (J/mol·K or as given)
        B (float): Cp coefficient for T¹ term
        C (float): Cp coefficient for T² term
        D (float): Cp coefficient for T³ term
        T1 (float): Initial temperature in Kelvin
        T2 (float): Final temperature in Kelvin

    Returns:
        float: Enthalpy change per mole in same energy unit as Cp coefficients.
            Positive if T2 > T1 (heating), negative if T2 < T1 (cooling).

    Examples:
        >>> integrated_cp_poly(-4.413, 0.528, -3.119e-4, 6.494e-8, 358, 423)
        10269.6  # J/mol for n-hexane, 358K to 423K

    For mixtures, calculate each component separately:
        Q_hex = n_hex * integrated_cp_poly(A_hex, B_hex, C_hex, D_hex, T1, T2)
        Q_hep = n_hep * integrated_cp_poly(A_hep, B_hep, C_hep, D_hep, T1, T2)
        Q_total = Q_hex + Q_hep
    """
    return (A * (T2 - T1) +
            (B / 2) * (T2**2 - T1**2) +
            (C / 3) * (T2**3 - T1**3) +
            (D / 4) * (T2**4 - T1**4))


def heat_exchange_poly(n_mol, cp_coeffs_list, T1, T2):
    """
    Calculate heat removed/added for a mixture with polynomial Cp, per component.

    Parameters:
        n_mol (float): Total molar flow rate (mol/h or mol/s)
        cp_coeffs_list: List of (A, B, C, D, mole_fraction) tuples for each component.
            For equimolar binary: [(A1,B1,C1,D1,0.5), (A2,B2,C2,D2,0.5)]
        T1 (float): Initial temperature (K)
        T2 (float): Final temperature (K)

    Returns:
        float: Total enthalpy change in J (per time unit matching n_mol).
            Negative = heat removed (cooling), positive = heat added.

    Example:
        >>> heat_exchange_poly(1000,
        ...     [(-4.413, 0.528, -3.119e-4, 6.494e-8, 0.5),
        ...      (-5.146, 0.6762, -3.651e-4, 7.658e-08, 0.5)],
        ...     423.15, 358.15)
        -11889000  # J/h, negative = cooling
    """
    Q_total = 0.0
    for A, B, C, D, x_i in cp_coeffs_list:
        n_i = n_mol * x_i
        Q_total += n_i * integrated_cp_poly(A, B, C, D, T1, T2)
    return Q_total
