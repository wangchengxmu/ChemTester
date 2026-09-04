"""
Reaction Rate Tools - L3 Implementation
Chapter 12.01: Chemical Reaction Rates

## Solver Instructions (for AI Agent)

When you encounter reaction rate problems (average rate, instantaneous rate, relative rates, stoichiometric relationships), follow this decision tree:

### Step 1: Identify what is given and what is asked
- **Average rate**: Given concentrations at two times -> find average rate of reaction
- **Relative rates**: Given stoichiometric coefficients -> relate rates of different species
- **Rate conversion**: Given rate in terms of one species -> convert to rate for another species
- **Instantaneous rate**: Given concentration vs time data and specific time -> estimate instantaneous rate

### Step 2: Choose the correct function
- `average_rate(C1, C2, t1, t2, reactant=True)` -> |DeltaC|/Deltat (positive for disappearance)
- `relative_rate_expression(coefficients)` -> dict of rate expressions per species
  - coefficients: negative for reactants, positive for products
- `convert_rate(rate, species1, coeff1, species2, coeff2)` -> rate for species2
- `instantaneous_rate(times, concentrations, target_time, species_coeff=1)` -> estimated d[A]/dt

### Step 3: Handle special cases
- `reactant=True` (default) makes the rate positive for disappearance (adds negative sign)
- Stoichiometric coefficients must include sign: reactants negative, products positive
- Rate of reaction is unique (independent of which species you track) when divided by |coefficient|

### Examples
1. **Average rate**: [A] drops from 1.0 M to 0.5 M over 6 seconds
   -> `average_rate(1.0, 0.5, 0, 6, reactant=True)` -> 0.0833 M/s

2. **Relative rates**: 2NH3 -> N2 + 3H2
   -> `relative_rate_expression({'NH3': -2, 'N2': 1, 'H2': 3})`
   -> rate = -½d[NH3]/dt = d[N2]/dt = ⅓d[H2]/dt

3. **Rate conversion**: If d[NH3]/dt = -0.4 M/s in above reaction, find d[N2]/dt
   -> `convert_rate(0.4, 'NH3', -2, 'N2', 1)` -> 0.2 M/s
"""

from typing import Dict, List, Tuple, Optional


def average_rate(C1: float, C2: float, t1: float, t2: float, 
                 reactant: bool = True) -> float:
    """
    Calculate average reaction rate.
    
    Args:
        C1: Initial concentration (M)
        C2: Final concentration (M)
        t1: Initial time
        t2: Final time
        reactant: True if measuring reactant (rate negative)
    
    Returns:
        Average rate (M/time unit)
    
    Examples:
        >>> average_rate(1.0, 0.5, 0, 6)
        0.0833
    """
    delta_C = C2 - C1
    delta_t = t2 - t1
    
    if reactant:
        return -delta_C / delta_t
    else:
        return delta_C / delta_t


def relative_rate_expression(coefficients: Dict[str, int]) -> Dict[str, str]:
    """
    Generate relative rate expressions from stoichiometric coefficients.
    
    Args:
        coefficients: Dict of {species: coefficient}
                     Negative for reactants, positive for products
    
    Returns:
        Dict of rate expressions for each species
    
    Examples:
        >>> relative_rate_expression({'NH3': -2, 'N2': 1, 'H2': 3})
        {'NH3': '-1/2 x d[NH3]/dt', 'N2': 'd[N2]/dt', 'H2': '1/3 x d[H2]/dt'}
    """
    expressions = {}
    
    for species, coeff in coefficients.items():
        abs_coeff = abs(coeff)
        
        if coeff < 0:  # Reactant
            if abs_coeff == 1:
                expressions[species] = f'-d[{species}]/dt'
            else:
                expressions[species] = f'-1/{abs_coeff} x d[{species}]/dt'
        else:  # Product
            if abs_coeff == 1:
                expressions[species] = f'd[{species}]/dt'
            else:
                expressions[species] = f'1/{abs_coeff} x d[{species}]/dt'
    
    return expressions


def convert_rate(rate: float, species1: str, coeff1: int, 
                 species2: str, coeff2: int) -> float:
    """
    Convert rate from one species to another using stoichiometry.
    
    Args:
        rate: Rate in terms of species1
        species1: First species name
        coeff1: Coefficient of species1 (with sign)
        species2: Second species name
        coeff2: Coefficient of species2 (with sign)
    
    Returns:
        Rate in terms of species2
    
    Examples:
        >>> convert_rate(1.0, 'NH3', -2, 'N2', 1)
        0.5
    """
    return rate * abs(coeff2) / abs(coeff1)


def instantaneous_rate(concentrations: List[float], times: List[float], 
                        t_target: float) -> float:
    """
    Estimate instantaneous rate at a specific time using slope.
    
    Args:
        concentrations: List of concentration values
        times: List of time values
        t_target: Time at which to estimate rate
    
    Returns:
        Estimated instantaneous rate
    
    Examples:
        >>> instantaneous_rate([1.0, 0.5, 0.25], [0, 6, 12], 6)
        0.083
    """
    # Simple linear interpolation around target time
    for i in range(len(times) - 1):
        if times[i] <= t_target <= times[i + 1]:
            # Use slope of this segment
            return -(concentrations[i] - concentrations[i + 1]) / (times[i + 1] - times[i])
    
    return 0.0


def rate_from_stoichiometry(rate_known: float, coeff_known: int, 
                             coeff_unknown: int) -> float:
    """
    Calculate rate of one species from rate of another.
    
    Args:
        rate_known: Known rate value
        coeff_known: Stoichiometric coefficient of known species
        coeff_unknown: Stoichiometric coefficient of unknown species
    
    Returns:
        Rate of unknown species
    
    Examples:
        >>> rate_from_stoichiometry(2.0, -2, 1)  # NH3 to N2
        1.0
    """
    return rate_known * abs(coeff_unknown) / abs(coeff_known)


def initial_rate_method(rates: List[float], concentrations: List[float]) -> float:
    """
    Estimate initial rate from early time data.
    
    Args:
        rates: List of rate values
        concentrations: List of concentration values
    
    Returns:
        Estimated initial rate
    """
    # Initial rate is typically the first measured rate
    return rates[0] if rates else 0.0


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="average_rate",
            description="Calculate average reaction rate.",
            input_schema=[
            InputSchemaField(name="C1", type="number", required=True),
            InputSchemaField(name="C2", type="number", required=True),
            InputSchemaField(name="t1", type="number", required=True),
            InputSchemaField(name="t2", type="number", required=True),
            InputSchemaField(name="reactant", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="convert_rate",
            description="Convert rate from one species to another using stoichiometry.",
            input_schema=[
            InputSchemaField(name="rate", type="number", required=True),
            InputSchemaField(name="species1", type="number", required=True),
            InputSchemaField(name="coeff1", type="number", required=True),
            InputSchemaField(name="species2", type="number", required=True),
            InputSchemaField(name="coeff2", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="initial_rate_method",
            description="Estimate initial rate from early time data.",
            input_schema=[
            InputSchemaField(name="rates", type="number", required=True),
            InputSchemaField(name="concentrations", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="instantaneous_rate",
            description="Estimate instantaneous rate at a specific time using slope.",
            input_schema=[
            InputSchemaField(name="concentrations", type="number", required=True),
            InputSchemaField(name="times", type="number", required=True),
            InputSchemaField(name="t_target", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="rate_from_stoichiometry",
            description="Calculate rate of one species from rate of another.",
            input_schema=[
            InputSchemaField(name="rate_known", type="number", required=True),
            InputSchemaField(name="coeff_known", type="number", required=True),
            InputSchemaField(name="coeff_unknown", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="relative_rate_expression",
            description="Generate relative rate expressions from stoichiometric coefficients.",
            input_schema=[
            InputSchemaField(name="coefficients", type="number", required=True)
            ],
            handler="{name}",
        )
    ]
