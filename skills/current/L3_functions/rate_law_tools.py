"""
Rate Law Tools - L3 Implementation
Chapter 12.03: Rate Laws and Reaction Orders

## Solver Instructions (for AI Agent)

When you encounter a rate law problem, follow this decision tree:

### Step 1: Identify what is given and what is asked
Extract from the question text:
- Rate law: rate = k[A]^m[B]^n
- Rate constant k: With appropriate units
- Reaction orders: m, n for each reactant
- Initial rates data: Multiple experiments with varying concentrations
- Overall order: Sum of individual orders

### Step 2: Choose the correct function
| Scenario | Function Call |
|----------|---------------|
| Calculate rate from rate law | `calculate_rate(k, concentrations, orders)` |
| Generate rate law expression string | `rate_law_from_orders(k, orders)` |
| Determine order from two rate experiments | `determine_order_initial_rates(conc1, rate1, conc2, rate2)` |
| Determine orders from multiple experiments | `method_of_initial_rates(data)` |
| Calculate rate constant from rate and concentrations | `determine_rate_constant(rate, concentrations, orders)` |
| Calculate overall order | `overall_order(orders)` |
| Get units for rate constant | `rate_constant_units(overall_order)` |

### Step 3: Handle special cases
- **Method of initial rates**: Find pairs where only one reactant changes
- **Order determination**: rate = k[A]^m -> m = log(rate2/rate1) / log(conc2/conc1)
- **Units of k**: Depend on overall order (0th: M·s-1, 1st: s-1, 2nd: M-1·s-1, 3rd: M-2·s-1)
- **Overall order**: Sum of all individual orders

### Examples

**Example 1: Calculate rate**
Question: "Calculate the rate if k = 0.1, [A] = 0.5 M, [B] = 0.2 M, with orders {A:1, B:2}."
- Solution: `calculate_rate(k=0.1, concentrations={'A': 0.5, 'B': 0.2}, orders={'A': 1, 'B': 2})` -> 0.002 M/s

**Example 2: Determine order from rates**
Question: "When [A] doubles from 0.1 to 0.2 M, rate doubles from 0.001 to 0.002 M/s. What is the order in A?"
- Solution: `determine_order_initial_rates(conc1=0.1, rate1=0.001, conc2=0.2, rate2=0.002)` -> 1 (first order)

**Example 3: Method of initial rates**
Question: "Expt1: [A]=0.1, [B]=0.1, rate=0.001; Expt2: [A]=0.2, [B]=0.1, rate=0.002; Expt3: [A]=0.1, [B]=0.2, rate=0.004. Find orders."
- Solution: `method_of_initial_rates([{'concentrations':{'A':0.1,'B':0.1},'rate':0.001}, {'concentrations':{'A':0.2,'B':0.1},'rate':0.002}, {'concentrations':{'A':0.1,'B':0.2},'rate':0.004}])` -> {'A': 1, 'B': 2}

**Example 4: Rate constant units**
Question: "What are the units of k for a second-order reaction?"
- Solution: `rate_constant_units(overall_order=2)` -> 'M-1·s-1'
"""

from typing import Dict, List, Tuple, Optional
from math import log


def rate_law_from_orders(k: float, orders: Dict[str, int]) -> str:
    """
    Generate rate law expression string.
    
    Args:
        k: Rate constant
        orders: Dict of {species: order}
    
    Returns:
        Rate law string
    
    Examples:
        >>> rate_law_from_orders(0.1, {'A': 1, 'B': 2})
        'rate = 0.1 [A]^1[B]^2'
    """
    terms = [f'[{sp}]^{order}' if order != 1 else f'[{sp}]' 
             for sp, order in orders.items() if order != 0]
    
    if not terms:
        return f'rate = {k}'
    
    return f'rate = {k} ' + ''.join(terms)


def calculate_rate(k: float, concentrations: Dict[str, float], 
                   orders: Dict[str, int]) -> float:
    """
    Calculate rate from rate law.
    
    Args:
        k: Rate constant
        concentrations: Dict of {species: concentration}
        orders: Dict of {species: order}
    
    Returns:
        Reaction rate
    
    Examples:
        >>> calculate_rate(0.1, {'A': 0.5, 'B': 0.2}, {'A': 1, 'B': 2})
        0.002
    """
    rate = k
    for species, order in orders.items():
        if species in concentrations:
            rate *= concentrations[species] ** order
    return rate


def determine_order_initial_rates(conc1: float, rate1: float, 
                                   conc2: float, rate2: float,
                                   other_constant: bool = True) -> int:
    """
    Determine reaction order from two initial rate measurements.
    
    Args:
        conc1, rate1: First concentration and rate
        conc2, rate2: Second concentration and rate
        other_constant: Whether other reactants held constant
    
    Returns:
        Reaction order
    
    Examples:
        >>> determine_order_initial_rates(0.1, 0.01, 0.2, 0.02)
        1
        >>> determine_order_initial_rates(0.1, 0.01, 0.2, 0.04)
        2
    """
    # rate2/rate1 = (conc2/conc1)^order
    # So: order = log(rate2/rate1) / log(conc2/conc1)
    
    from math import log
    
    rate_ratio = rate2 / rate1
    conc_ratio = conc2 / conc1
    
    if conc_ratio == 1:
        return 0  # No change in concentration
    
    order_float = log(rate_ratio) / log(conc_ratio)
    
    # Round to nearest integer
    return round(order_float)


def rate_constant_units(overall_order: int) -> str:
    """
    Get units for rate constant based on overall order.
    
    Args:
        overall_order: Overall reaction order
    
    Returns:
        Units string
    
    Examples:
        >>> rate_constant_units(0)
        'M·s-1'
        >>> rate_constant_units(1)
        's-1'
        >>> rate_constant_units(2)
        'M-1·s-1'
    """
    units = {
        0: 'M·s⁻¹',
        1: 's⁻¹',
        2: 'M⁻¹·s⁻¹',
        3: 'M⁻²·s⁻¹',
    }
    return units.get(overall_order, f'M^{1-overall_order}·s⁻¹')


def determine_rate_constant(rate: float, concentrations: Dict[str, float],
                             orders: Dict[str, int]) -> float:
    """
    Calculate rate constant from rate and concentrations.
    
    Args:
        rate: Measured rate
        concentrations: Dict of {species: concentration}
        orders: Dict of {species: order}
    
    Returns:
        Rate constant k
    
    Examples:
        >>> determine_rate_constant(0.002, {'A': 0.5, 'B': 0.2}, {'A': 1, 'B': 2})
        0.1
    """
    denominator = 1.0
    for species, order in orders.items():
        if species in concentrations:
            denominator *= concentrations[species] ** order
    
    return rate / denominator


def overall_order(orders: Dict[str, int]) -> int:
    """
    Calculate overall reaction order.
    
    Args:
        orders: Dict of {species: order}
    
    Returns:
        Overall order
    
    Examples:
        >>> overall_order({'A': 1, 'B': 2})
        3
    """
    return sum(orders.values())


def method_of_initial_rates(data: List[Dict]) -> Dict[str, int]:
    """
    Determine reaction orders from multiple initial rate experiments.
    
    Args:
        data: List of dicts with 'concentrations' and 'rate' keys
    
    Returns:
        Dict of {species: order}
    
    Examples:
        >>> data = [
        ...     {'concentrations': {'A': 0.1, 'B': 0.1}, 'rate': 0.001},
        ...     {'concentrations': {'A': 0.2, 'B': 0.1}, 'rate': 0.002},
        ...     {'concentrations': {'A': 0.1, 'B': 0.2}, 'rate': 0.004},
        ... ]
        >>> method_of_initial_rates(data)
        {'A': 1, 'B': 2}
    """
    if len(data) < 2:
        return {}
    
    species = list(data[0]['concentrations'].keys())
    orders = {}
    
    for sp in species:
        # Find two experiments where only this species varies
        for i, exp1 in enumerate(data):
            for exp2 in data[i+1:]:
                other_same = all(
                    exp1['concentrations'].get(s, 0) == exp2['concentrations'].get(s, 0)
                    for s in species if s != sp
                )
                if other_same and exp1['concentrations'][sp] != exp2['concentrations'][sp]:
                    orders[sp] = determine_order_initial_rates(
                        exp1['concentrations'][sp], exp1['rate'],
                        exp2['concentrations'][sp], exp2['rate']
                    )
                    break
            if sp in orders:
                break
    
    return orders


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="calculate_rate",
            description="Calculate rate from rate law.",
            input_schema=[
            InputSchemaField(name="k", type="number", required=True),
            InputSchemaField(name="concentrations", type="number", required=True),
            InputSchemaField(name="orders", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="determine_order_initial_rates",
            description="Determine reaction order from two initial rate measurements.",
            input_schema=[
            InputSchemaField(name="conc1", type="number", required=True),
            InputSchemaField(name="rate1", type="number", required=True),
            InputSchemaField(name="conc2", type="number", required=True),
            InputSchemaField(name="rate2", type="number", required=True),
            InputSchemaField(name="other_constant", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="determine_rate_constant",
            description="Calculate rate constant from rate and concentrations.",
            input_schema=[
            InputSchemaField(name="rate", type="number", required=True),
            InputSchemaField(name="concentrations", type="number", required=True),
            InputSchemaField(name="orders", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="method_of_initial_rates",
            description="Determine reaction orders from multiple initial rate experiments.",
            input_schema=[
            InputSchemaField(name="data", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="overall_order",
            description="Calculate overall reaction order.",
            input_schema=[
            InputSchemaField(name="orders", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="rate_constant_units",
            description="Get units for rate constant based on overall order.",
            input_schema=[
            InputSchemaField(name="overall_order", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="rate_law_from_orders",
            description="Generate rate law expression string.",
            input_schema=[
            InputSchemaField(name="k", type="number", required=True),
            InputSchemaField(name="orders", type="number", required=True)
            ],
            handler="{name}",
        )
    ]
