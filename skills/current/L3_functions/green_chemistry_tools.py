"""
L3 Tool: Green Chemistry Tools
Green metrics calculations (E-factor, PMI, atom economy, RME).

Source: Anastas & Warner, Manahan (LibreTexts)
Created: 2026-03-24 (Phase 2)
## Solver Instructions (for AI Agent)

When you encounter green chemistry metrics or sustainability problems, follow this decision tree:

### Step 1: Identify what is given and what is asked
- Molecular weights of reactants and product -> Atom economy? Use `atom_economy(mw_product, mw_reactants)`
- Waste and product mass -> E-factor? Use `e_factor(total_waste_kg, product_kg)`
- Total input mass -> PMI? Use `process_mass_intensity(total_input_mass, product_mass)`
- AE + yield -> RME? Use `reaction_mass_efficiency(mw_product, mw_reactants, yield_pct)`
- Greenhouse gas emissions -> GWP? Use `gwp_calculator(emissions_dict, time_horizon=100)`
- Multi-step synthesis -> Overall yield? Use `overall_yield_multistep(yields_list)` - yields as fractions (0-1)
- Carbon efficiency? Use `carbon_efficiency(carbon_in_product, carbon_in_reactants)`
- Solvent recovery? Use `solvent_recovery_rate(mass_recovered, mass_used)`
- Energy efficiency? Use `energy_efficiency(theoretical_energy, actual_energy)`
- Toxicity reduction? Use `toxicity_reduction(old_toxicity, new_toxicity)`

### Step 2: Handle special cases
- **E-factor**: E = waste/product; PMI = E + 1; pharma E-factor typically 25-100
- **Atom economy**: 100% = all atoms of reactants in product (e.g., H2 + O2 -> H2O = 100%)
- **GWP factors**: CO2=1, CH4=28, N2O=265 (100-yr horizon)
- **Overall yield**: Multiplies step yields; 5 steps at 90% each = 59% overall

### Examples
```python
# Example 1: Atom economy for 2H2 + O2 -> 2H2O
atom_economy(36.03, [4.032, 32.0])  # -> 100%

# Example 2: E-factor for pharma process
e_factor(25, 1)  # -> E=25, PMI=26

# Example 3: Overall yield for 5 steps at 90% each
overall_yield_multistep([0.9]*5)  # -> 59.05%
```
"""

import math


def atom_economy(mw_product: float, mw_reactants: list) -> dict:
    """Calculate atom economy.
    
    AE = MW(product) / Σ MW(reactants) x 100
    """
    total_mw = sum(mw_reactants)
    if total_mw <= 0:
        return {'error': 'Sum of reactant MW must be positive'}
    ae = mw_product / total_mw * 100
    return {
        'atom_economy_pct': round(ae, 2),
        'mw_product': mw_product,
        'total_mw_reactants': total_mw
    }


def e_factor(total_waste_kg: float, product_kg: float) -> dict:
    """Calculate E-factor.
    
    E = total waste / product
    """
    if product_kg <= 0:
        return {'error': 'Product mass must be positive'}
    ef = total_waste_kg / product_kg
    return {
        'e_factor': round(ef, 4),
        'total_waste_kg': total_waste_kg,
        'product_kg': product_kg,
        'pmi': round(ef + 1, 4)
    }


def process_mass_intensity(total_input_mass: float, product_mass: float) -> dict:
    """Calculate PMI and E-factor.
    
    PMI = total input / product = E-factor + 1
    """
    if product_mass <= 0:
        return {'error': 'Product mass must be positive'}
    pmi = total_input_mass / product_mass
    return {
        'pmi': round(pmi, 4),
        'e_factor': round(pmi - 1, 4),
        'total_input': total_input_mass,
        'product': product_mass
    }


def reaction_mass_efficiency(mw_product: float, mw_reactants: list, yield_pct: float) -> dict:
    """Calculate RME = AE x yield.
    
    RME = (actual product mass / total reactant mass) x 100
    """
    if yield_pct < 0 or yield_pct > 100:
        return {'error': 'Yield must be 0-100%'}
    ae = mw_product / sum(mw_reactants)
    rme = ae * yield_pct
    return {
        'rme_pct': round(rme, 2),
        'atom_economy_pct': round(ae * 100, 2),
        'yield_pct': yield_pct
    }


def gwp_calculator(emissions: dict, time_horizon: int = 100) -> dict:
    """Calculate global warming potential.
    
    GWP factors (100-yr): CO2=1, CH4=28, N2O=265
    emissions: dict of gas name -> mass (kg)
    """
    gwp_factors = {
        'CO2': 1, 'CH4': 28, 'N2O': 265,
        'CF4': 6630, 'CFC-11': 4660, 'HFC-134a': 1300
    }
    total_co2eq = 0
    breakdown = {}
    for gas, mass in emissions.items():
        factor = gwp_factors.get(gas.upper(), 1)
        contribution = mass * factor
        total_co2eq += contribution
        breakdown[gas] = {'mass_kg': mass, 'gwp_factor': factor, 'co2_eq': contribution}
    return {'total_co2eq_kg': round(total_co2eq, 2), 'breakdown': breakdown}


def overall_yield_multistep(yields: list) -> dict:
    """Calculate overall yield for multi-step synthesis.
    
    Overall yield = Π(yield_i) for i in steps
    """
    overall = 1.0
    for y in yields:
        if y <= 0 or y > 1:
            return {'error': f'Invalid yield: {y}'}
        overall *= y
    return {
        'overall_yield': round(overall, 6),
        'overall_yield_pct': round(overall * 100, 2),
        'num_steps': len(yields),
        'step_yields': [round(y * 100, 1) for y in yields]
    }


def carbon_efficiency(carbon_in_product: float, carbon_in_reactants: float):
    """Calculate carbon efficiency.

    CE = (carbon in product / carbon in reactants) x 100
    """
    if carbon_in_reactants <= 0:
        return {'error': 'Carbon in reactants must be positive.'}
    ce = carbon_in_product / carbon_in_reactants * 100
    return {
        'carbon_efficiency_pct': round(ce, 2),
        'carbon_in_product': carbon_in_product,
        'carbon_in_reactants': carbon_in_reactants
    }


def solvent_recovery_rate(mass_solvent_recovered: float, mass_solvent_used: float):
    """Calculate solvent recovery rate.

    Rate = (recovered / used) x 100
    """
    if mass_solvent_used <= 0:
        return {'error': 'Mass of solvent used must be positive.'}
    rate = mass_solvent_recovered / mass_solvent_used * 100
    return {
        'recovery_rate_pct': round(rate, 2),
        'mass_recovered': mass_solvent_recovered,
        'mass_used': mass_solvent_used
    }


def energy_efficiency(theoretical_energy: float, actual_energy: float):
    """Calculate energy efficiency.

    Efficiency = (theoretical / actual) x 100
    """
    if actual_energy <= 0:
        return {'error': 'Actual energy must be positive.'}
    eff = theoretical_energy / actual_energy * 100
    return {
        'energy_efficiency_pct': round(eff, 2),
        'theoretical_energy': theoretical_energy,
        'actual_energy': actual_energy
    }


def toxicity_reduction(old_toxicity: float, new_toxicity: float):
    """Calculate percentage toxicity reduction.

    Reduction = (1 - new / old) x 100
    """
    if old_toxicity <= 0:
        return {'error': 'Old toxicity must be positive.'}
    reduction = (1 - new_toxicity / old_toxicity) * 100
    return {
        'toxicity_reduction_pct': round(reduction, 2),
        'old_toxicity': old_toxicity,
        'new_toxicity': new_toxicity
    }


TEXTBOOK_PROBLEMS = {
    "atom_economy_basic": "AE for: 2H2 + O2 -> 2H2O. AE = 36.03 / (4.032 + 32) = 100%",
    "e_factor_pharma": "Typical pharmaceutical: 25 kg waste / 1 kg product -> E=25",
}

MCP_TOOLS = [
    {
        "name": "atom_economy",
        "description": "Calculate atom economy: (MW_product / sum MW_reactants) x 100.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "mw_product": {"type": "number", "description": "Molecular weight of desired product"},
                "mw_reactants": {"type": "array", "items": {"type": "number"}, "description": "List of reactant molecular weights"}
            },
            "required": ["mw_product", "mw_reactants"]
        },
        "returns": {"type": "object", "description": "Dict with atom_economy_pct"}
    },
    {
        "name": "e_factor",
        "description": "Calculate E-factor: mass_waste / mass_product.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "mass_waste": {"type": "number", "description": "Total waste mass (kg)"},
                "mass_product": {"type": "number", "description": "Product mass (kg)"}
            },
            "required": ["mass_waste", "mass_product"]
        },
        "returns": {"type": "object", "description": "Dict with e_factor and pmi"}
    },
    {
        "name": "process_mass_intensity",
        "description": "Calculate PMI: total input mass / product mass. PMI = E-factor + 1.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "mass_total_input": {"type": "number", "description": "Total mass input to process"},
                "mass_product": {"type": "number", "description": "Product mass"}
            },
            "required": ["mass_total_input", "mass_product"]
        },
        "returns": {"type": "object", "description": "Dict with pmi and e_factor"}
    },
    {
        "name": "carbon_efficiency",
        "description": "Calculate carbon efficiency: (carbon in product / carbon in reactants) x 100.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "carbon_in_product": {"type": "number", "description": "Carbon mass in product"},
                "carbon_in_reactants": {"type": "number", "description": "Carbon mass in reactants"}
            },
            "required": ["carbon_in_product", "carbon_in_reactants"]
        },
        "returns": {"type": "object", "description": "Dict with carbon_efficiency_pct"}
    },
    {
        "name": "reaction_mass_efficiency",
        "description": "Calculate RME = atom_economy x yield.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "mw_product": {"type": "number"},
                "mw_reactants": {"type": "array", "items": {"type": "number"}},
                "yield_pct": {"type": "number", "description": "Reaction yield (0-100)"}
            },
            "required": ["mw_product", "mw_reactants", "yield_pct"]
        },
        "returns": {"type": "object", "description": "Dict with rme_pct"}
    },
    {
        "name": "solvent_recovery_rate",
        "description": "Calculate solvent recovery rate: (recovered / used) x 100.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "mass_solvent_recovered": {"type": "number"},
                "mass_solvent_used": {"type": "number"}
            },
            "required": ["mass_solvent_recovered", "mass_solvent_used"]
        },
        "returns": {"type": "object", "description": "Dict with recovery_rate_pct"}
    },
    {
        "name": "energy_efficiency",
        "description": "Calculate energy efficiency: (theoretical / actual) x 100.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "theoretical_energy": {"type": "number"},
                "actual_energy": {"type": "number"}
            },
            "required": ["theoretical_energy", "actual_energy"]
        },
        "returns": {"type": "object", "description": "Dict with energy_efficiency_pct"}
    },
    {
        "name": "toxicity_reduction",
        "description": "Calculate percentage toxicity reduction: (1 - new/old) x 100.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "old_toxicity": {"type": "number"},
                "new_toxicity": {"type": "number"}
            },
            "required": ["old_toxicity", "new_toxicity"]
        },
        "returns": {"type": "object", "description": "Dict with toxicity_reduction_pct"}
    },
]
