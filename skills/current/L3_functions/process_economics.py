"""
Process Economics - L3 Implementation

Economic calculations for chemical processes.
Source: Foundations of Chemical and Biological Engineering I (Verret), Ch6

## Solver Instructions (for AI Agent)

When you encounter chemical process economics problems, follow this decision tree:

### Step 1: Identify what is given and what is asked
- **NPV**: Given cash flows over time and discount rate -> find net present value
- **ROI**: Given annual profit and total investment -> find return on investment (%)
- **Payback period**: Given capital investment and annual cash flow -> find years to payback
- **Cost scaling**: Given reference equipment cost/size -> estimate cost at new size
- **TCO**: Given purchase cost, operating cost, maintenance -> find total cost of ownership
- **MARR**: Given discount rate -> check if NPV > 0 (project viable)

### Step 2: Choose the correct function
- `net_present_value(cash_flows, discount_rate)` -> NPV = Σ CF_t/(1+r)^t
- `return_on_investment(annual_profit, total_investment)` -> ROI as %
- `payback_period(capital_investment, annual_cash_flow)` -> years
- `scale_cost(reference_cost, reference_size, new_size, exponent)` -> six-tenths rule
- `total_cost_of_ownership(purchase_cost, operating_cost, maintenance_cost, years)` -> TCO
- `internal_rate_of_return(cash_flows)` -> IRR (discount rate where NPV=0)

### Step 3: Handle special cases
- cash_flows[0] is typically negative (initial investment)
- Default scaling exponent is 0.6 (six-tenths rule); use 0.7-0.8 for solids processing
- NPV > 0 means project is economically viable
- Payback period is simple (no time value of money); use NPV for rigorous analysis

### Examples
1. **NPV**: Investment $100k, then $30k/yr for 5 years, r=10%
   -> `net_present_value([-100000, 30000, 30000, 30000, 30000, 30000], 0.10)` -> $13,724

2. **Scale cost**: Heat exchanger costs $50,000 for 100 m2, need 200 m2
   -> `scale_cost(50000, 100, 200, 0.6)` -> $50,000 x (200/100)^0.6 = $75,786

3. **ROI**: Annual profit $200k, total investment $1.5M
   -> `return_on_investment(200000, 1500000)` -> 13.3%
"""

from typing import List, Tuple
import math


def net_present_value(cash_flows: List[float], discount_rate: float) -> float:
    """
    Calculate Net Present Value.
    
    NPV = Σ CF_t / (1 + r)^t
    
    Args:
        cash_flows: List of cash flows (CF_0, CF_1, ..., CF_n)
        discount_rate: Annual discount rate (decimal)
    
    Returns:
        NPV in same units as cash flows
    """
    npv = 0.0
    for t, cf in enumerate(cash_flows):
        npv += cf / (1 + discount_rate) ** t
    return npv


def return_on_investment(annual_profit: float, total_investment: float) -> float:
    """
    Calculate Return on Investment.
    
    ROI = (Annual Profit / Total Investment) x 100%
    
    Args:
        annual_profit: Annual profit
        total_investment: Total capital investment
    
    Returns:
        ROI as percentage
    """
    return (annual_profit / total_investment) * 100


def payback_period(capital_investment: float, annual_cash_flow: float) -> float:
    """
    Calculate simple payback period.
    
    Payback = Capital Investment / Annual Cash Flow
    
    Args:
        capital_investment: Initial investment
        annual_cash_flow: Annual cash inflow
    
    Returns:
        Payback period in years
    """
    return capital_investment / annual_cash_flow


def scale_cost(reference_cost: float, reference_size: float, 
               new_size: float, exponent: float = 0.6) -> float:
    """
    Scale equipment cost using six-tenths rule.
    
    C_new = C_ref x (S_new / S_ref)^n
    
    Args:
        reference_cost: Cost of reference equipment
        reference_size: Size/capacity of reference equipment
        new_size: Size/capacity of new equipment
        exponent: Scaling exponent (default 0.6)
    
    Returns:
        Estimated cost of new equipment
    """
    return reference_cost * (new_size / reference_size) ** exponent


def annualized_cost(capital_cost: float, lifetime_years: int, 
                    discount_rate: float) -> float:
    """
    Calculate annualized capital cost.
    
    AC = C x [r(1+r)^n] / [(1+r)^n - 1]
    
    Args:
        capital_cost: Initial capital cost
        lifetime_years: Equipment lifetime in years
        discount_rate: Annual discount rate
    
    Returns:
        Annualized cost
    """
    r = discount_rate
    n = lifetime_years
    factor = (r * (1 + r) ** n) / ((1 + r) ** n - 1)
    return capital_cost * factor


def break_even_analysis(fixed_cost: float, variable_cost: float,
                        selling_price: float) -> float:
    """
    Calculate break-even production quantity.
    
    Q_BE = FC / (P - VC)
    
    Args:
        fixed_cost: Total fixed costs
        variable_cost: Variable cost per unit
        selling_price: Selling price per unit
    
    Returns:
        Break-even quantity
    """
    return fixed_cost / (selling_price - variable_cost)


def compare_alternatives(npv_list: List[Tuple[str, float]]) -> dict:
    """
    Compare multiple investment alternatives.
    
    Args:
        npv_list: List of (alternative_name, npv) tuples
    
    Returns:
        Dictionary with best alternative
    """
    sorted_alternatives = sorted(npv_list, key=lambda x: x[1], reverse=True)
    
    return {
        "best_alternative": sorted_alternatives[0][0],
        "best_npv": sorted_alternatives[0][1],
        "ranking": sorted_alternatives
    }


# Aliases for solver compatibility
def npv(cash_flows: list, discount_rate: float) -> float:
    """Alias for net_present_value."""
    return net_present_value(cash_flows, discount_rate)


def roi(annual_profit: float, total_investment: float) -> float:
    """Alias for return_on_investment."""
    return return_on_investment(annual_profit, total_investment)


def payback(capital_investment: float, annual_cash_flow: float) -> float:
    """Alias for payback_period."""
    return payback_period(capital_investment, annual_cash_flow)


def break_even(fixed_cost: float, variable_cost: float,
               selling_price: float) -> float:
    """Alias for break_even_analysis."""
    return break_even_analysis(fixed_cost, variable_cost, selling_price)


# TODO: Implement for Pass-3
# - depreciation_calculation() - MACRS, straight-line
# - sensitivity_analysis() - Vary inputs, see NPV change
# - irr_calculation() - Internal rate of return
