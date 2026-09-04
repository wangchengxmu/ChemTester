"""
Process Engineering Tools (MCP-style)

Core chemical engineering calculations: conversion, yield, selectivity,
material balance, atom economy, E-factor, PMI, STY, TOF, TON.

## Solver Instructions (for AI Agent)

When you encounter process engineering calculation problems (conversion, yield, selectivity, material balance, green chemistry metrics), follow this decision tree:

### Step 1: Identify what is given and what is asked
- **Conversion**: Given initial and final moles of reactant -> find fractional conversion
- **Yield**: Given product moles and limiting reactant moles -> find yield
- **Selectivity**: Given desired product vs byproduct moles -> find selectivity
- **Material balance**: Given inputs and outputs -> check mass/mole balance closure
- **Atom economy**: Given MW of products vs reactants -> find atom economy %
- **Green metrics**: Given masses -> find E-factor, PMI, STY, TOF, TON

### Step 2: Choose the correct function
- `conversion(reactant_in, reactant_out)` -> X = (in - out)/in
- `yield_calc(product_moles, limiting_reactant_moles)` -> Y = product/limiting
- `selectivity(product_moles, byproduct_moles)` -> S = desired/(desired + byproducts)
- `material_balance(inputs, outputs)` -> total_in, total_out, difference, closure_pct
- `atom_economy(mw_products, mw_reactants)` -> % = (MW_products/MW_reactants)x100
- `e_factor(mass_waste, mass_product)` -> E = waste/product
- `pmi(total_mass_input, mass_product)` -> PMI = total_input/product
- `sty(mass_product, reactor_volume, time)` -> kg/(L·h) or similar
- `tof(moles_product, moles_catalyst, time)` -> turnover frequency
- `ton_calc(moles_product, moles_catalyst)` -> turnover number

### Step 3: Handle special cases
- Conversion is always ≤ 1 (fractional); multiply by 100 for percentage
- Yield ≤ conversion (can't exceed conversion)
- Selectivity = 1.0 means no byproducts formed
- E-factor of 1 means equal waste and product mass; ideal is < 1
- For atom economy, use MW of desired product(s) only, not all products

### Examples
1. **Conversion**: 10 mol A fed, 2 mol A remaining
   -> `conversion(10.0, 2.0)` -> 0.8 (80% conversion)

2. **Atom economy**: C2H4 + H2O -> C2H5OH; MW products=46, MW reactants=30+18=46
   -> `atom_economy(46, 48)` -> 95.8%

3. **E-factor**: 50 kg product, 200 kg waste
   -> `e_factor(200, 50)` -> 4.0 (poor; pharmaceutical industry average ~25-100)
"""

from typing import Dict, List, Tuple

MCP_TOOLS = [
    {
        "name": "conversion",
        "description": "Calculate fractional conversion of a reactant.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "reactant_in": {"type": "number", "description": "Initial moles (or mass/flow) of reactant"},
                "reactant_out": {"type": "number", "description": "Final moles (or mass/flow) of reactant"}
            },
            "required": ["reactant_in", "reactant_out"]
        },
        "returns": {"type": "number", "description": "Fractional conversion (0 to 1)"},
        "examples": [
            {"input": {"reactant_in": 10.0, "reactant_out": 2.0}, "output": 0.8}
        ]
    },
    {
        "name": "yield_calc",
        "description": "Calculate reaction yield based on product formed vs limiting reactant.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "product_moles": {"type": "number", "description": "Moles of product formed"},
                "limiting_reactant_moles": {"type": "number", "description": "Initial moles of limiting reactant"}
            },
            "required": ["product_moles", "limiting_reactant_moles"]
        },
        "returns": {"type": "number", "description": "Yield as fraction (0 to 1)"}
    },
    {
        "name": "selectivity",
        "description": "Calculate product selectivity (product moles / total product moles including byproducts).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "product_moles": {"type": "number", "description": "Moles of desired product"},
                "byproduct_moles": {"type": "number", "description": "Moles of byproduct(s)"}
            },
            "required": ["product_moles", "byproduct_moles"]
        },
        "returns": {"type": "number", "description": "Selectivity as fraction (0 to 1)"},
        "examples": [
            {"input": {"product_moles": 8.0, "byproduct_moles": 2.0}, "output": 0.8}
        ]
    },
    {
        "name": "material_balance",
        "description": "Check material balance closure: sum of inputs vs sum of outputs.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "inputs": {"type": "array", "items": {"type": "number"}, "description": "List of input masses or moles"},
                "outputs": {"type": "array", "items": {"type": "number"}, "description": "List of output masses or moles"}
            },
            "required": ["inputs", "outputs"]
        },
        "returns": {"type": "object", "description": "Dict with total_in, total_out, difference, closure_pct"}
    },
    {
        "name": "atom_economy",
        "description": "Calculate atom economy percentage.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "mw_products": {"type": "number", "description": "Molecular weight of desired product(s)"},
                "mw_reactants": {"type": "number", "description": "Total molecular weight of all reactants"}
            },
            "required": ["mw_products", "mw_reactants"]
        },
        "returns": {"type": "number", "description": "Atom economy as percentage (%)"},
        "examples": [
            {"input": {"mw_products": 104.15, "mw_reactants": 212.26}, "output": 49.07, "note": "~49% atom economy"}
        ]
    },
    {
        "name": "e_factor",
        "description": "Calculate E-factor (mass waste / mass product). Lower is greener.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "mass_waste": {"type": "number", "description": "Total mass of waste generated (kg)"},
                "mass_product": {"type": "number", "description": "Mass of product obtained (kg)"}
            },
            "required": ["mass_waste", "mass_product"]
        },
        "returns": {"type": "number", "description": "E-factor (dimensionless)"}
    },
    {
        "name": "pmi",
        "description": "Calculate Process Mass Intensity (total input mass / product mass).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "mass_total_input": {"type": "number", "description": "Total mass of all inputs including solvents, reagents (kg)"},
                "mass_product": {"type": "number", "description": "Mass of product (kg)"}
            },
            "required": ["mass_total_input", "mass_product"]
        },
        "returns": {"type": "number", "description": "PMI (dimensionless, lower is better)"}
    },
    {
        "name": "space_time_yield",
        "description": "Calculate Space-Time Yield (STY) in kg/(L·h).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "mass_product": {"type": "number", "description": "Mass of product (kg)"},
                "reactor_volume": {"type": "number", "description": "Reactor volume (L)"},
                "time_hours": {"type": "number", "description": "Reaction time (hours)"}
            },
            "required": ["mass_product", "reactor_volume", "time_hours"]
        },
        "returns": {"type": "number", "description": "STY in kg/(L·h)"}
    },
    {
        "name": "turnover_frequency",
        "description": "Calculate Turnover Frequency (TOF) in h-1.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "moles_product": {"type": "number", "description": "Moles of product formed"},
                "moles_catalyst": {"type": "number", "description": "Moles of catalyst used"},
                "time_hours": {"type": "number", "description": "Reaction time (hours)"}
            },
            "required": ["moles_product", "moles_catalyst", "time_hours"]
        },
        "returns": {"type": "number", "description": "TOF in h-1"}
    },
    {
        "name": "turnover_number",
        "description": "Calculate Turnover Number (TON).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "moles_product": {"type": "number", "description": "Moles of product formed"},
                "moles_catalyst": {"type": "number", "description": "Moles of catalyst used"}
            },
            "required": ["moles_product", "moles_catalyst"]
        },
        "returns": {"type": "number", "description": "TON (dimensionless)"},
        "examples": [
            {"input": {"moles_product": 100.0, "moles_catalyst": 0.01}, "output": 10000}
        ]
    }
]


def conversion(reactant_in: float, reactant_out: float) -> float:
    """
    Calculate fractional conversion.
    
    X = (reactant_in - reactant_out) / reactant_in
    
    Args:
        reactant_in: Initial amount of reactant
        reactant_out: Final amount of reactant
    
    Returns:
        Fractional conversion (0 to 1)
    """
    if reactant_in <= 0:
        raise ValueError("reactant_in must be positive")
    return (reactant_in - reactant_out) / reactant_in


def yield_calc(product_moles: float, limiting_reactant_moles: float) -> float:
    """
    Calculate reaction yield.
    
    Y = product_moles / limiting_reactant_moles
    
    Args:
        product_moles: Moles of product formed
        limiting_reactant_moles: Initial moles of limiting reactant
    
    Returns:
        Yield as fraction
    """
    if limiting_reactant_moles <= 0:
        raise ValueError("limiting_reactant_moles must be positive")
    return product_moles / limiting_reactant_moles


def selectivity(product_moles: float, byproduct_moles: float) -> float:
    """
    Calculate product selectivity.
    
    S = product_moles / (product_moles + byproduct_moles)
    
    Args:
        product_moles: Moles of desired product
        byproduct_moles: Moles of byproduct(s)
    
    Returns:
        Selectivity as fraction (0 to 1)
    """
    total = product_moles + byproduct_moles
    if total <= 0:
        raise ValueError("Sum of product and byproduct moles must be positive")
    return product_moles / total


def material_balance(inputs: List[float], outputs: List[float]) -> Dict:
    """
    Check material balance closure.
    
    Args:
        inputs: List of input masses/moles
        outputs: List of output masses/moles
    
    Returns:
        Dict with total_in, total_out, difference, closure_pct
    """
    total_in = sum(inputs)
    total_out = sum(outputs)
    difference = total_in - total_out
    closure_pct = (total_out / total_in * 100) if total_in > 0 else float('inf')
    return {
        "total_in": total_in,
        "total_out": total_out,
        "difference": difference,
        "closure_pct": round(closure_pct, 4)
    }


def atom_economy(mw_products: float, mw_reactants: float) -> float:
    """
    Calculate atom economy percentage.
    
    AE = (MW_products / MW_reactants) x 100%
    
    Args:
        mw_products: Molecular weight of desired product(s)
        mw_reactants: Total MW of all reactants
    
    Returns:
        Atom economy as percentage
    """
    if mw_reactants <= 0:
        raise ValueError("mw_reactants must be positive")
    return (mw_products / mw_reactants) * 100


def e_factor(mass_waste: float, mass_product: float) -> float:
    """
    Calculate E-factor.
    
    E = mass_waste / mass_product
    
    Args:
        mass_waste: Total waste mass (kg)
        mass_product: Product mass (kg)
    
    Returns:
        E-factor (dimensionless)
    """
    if mass_product <= 0:
        raise ValueError("mass_product must be positive")
    return mass_waste / mass_product


def pmi(mass_total_input: float, mass_product: float) -> float:
    """
    Calculate Process Mass Intensity.
    
    PMI = mass_total_input / mass_product
    
    Args:
        mass_total_input: Total input mass (kg)
        mass_product: Product mass (kg)
    
    Returns:
        PMI (dimensionless)
    """
    if mass_product <= 0:
        raise ValueError("mass_product must be positive")
    return mass_total_input / mass_product


def space_time_yield(mass_product: float, reactor_volume: float, time_hours: float) -> float:
    """
    Calculate Space-Time Yield.
    
    STY = mass_product / (reactor_volume x time_hours)
    
    Args:
        mass_product: Product mass (kg)
        reactor_volume: Reactor volume (L)
        time_hours: Reaction time (h)
    
    Returns:
        STY in kg/(L·h)
    """
    if reactor_volume <= 0:
        raise ValueError("reactor_volume must be positive")
    if time_hours <= 0:
        raise ValueError("time_hours must be positive")
    return mass_product / (reactor_volume * time_hours)


def turnover_frequency(moles_product: float, moles_catalyst: float, time_hours: float) -> float:
    """
    Calculate Turnover Frequency.
    
    TOF = moles_product / (moles_catalyst x time_hours)
    
    Args:
        moles_product: Moles of product
        moles_catalyst: Moles of catalyst
        time_hours: Time (h)
    
    Returns:
        TOF in h-1
    """
    if moles_catalyst <= 0:
        raise ValueError("moles_catalyst must be positive")
    if time_hours <= 0:
        raise ValueError("time_hours must be positive")
    return moles_product / (moles_catalyst * time_hours)


def turnover_number(moles_product: float, moles_catalyst: float) -> float:
    """
    Calculate Turnover Number.
    
    TON = moles_product / moles_catalyst
    
    Args:
        moles_product: Moles of product
        moles_catalyst: Moles of catalyst
    
    Returns:
        TON (dimensionless)
    """
    if moles_catalyst <= 0:
        raise ValueError("moles_catalyst must be positive")
    return moles_product / moles_catalyst
