"""
Measurement and Quantitative Tools - L3 Implementation

## Solver Instructions (for AI Agent)

When you encounter measurement, unit conversion, or significant figures problems, follow this decision tree:

### Step 1: Identify what is given and what is asked
- Given value with units -> convert to different units?
- Given measurement description -> classify as physical or chemical change?
- Given value with sig figs -> round to correct precision?
- Given value with uncertainty -> format for reporting?

### Step 2: Choose the correct function
| Task | Function | Key Parameters |
|---|---|---|
| Unit conversion | `unit_convert(value, from_unit, to_unit)` | supported: m↔cm, kg↔g, L↔mL |
| Classify change | `classify_change(description)` | returns "chemical" or "physical" |
| Significant figures | `sigfig_round(value, sigfigs)` | rounds to N significant figures |
| Uncertainty report | `uncertainty_report(value, uncertainty)` | returns "value ± uncertainty" string |

### Step 3: Handle special cases
- Only specific unit conversions are supported (m↔cm, kg↔g, L↔mL)
- Chemical change keywords: burn, rust, react, oxid, acid, base, precip
- sigfig_round(0, n) returns 0.0 (special case for zero)

### Examples
```python
# Example 1: Unit conversion
unit_convert(2.5, "L", "mL")
# -> 2500.0

# Example 2: Classify change
classify_change("Iron rusts in humid air")
# -> "chemical"

# Example 3: Significant figures
sigfig_round(12.3456, 3)
# -> 12.3

# Example 4: Uncertainty reporting
uncertainty_report(7.20, 0.05)
# -> "7.2 ± 0.05"
```
"""
UNIT_FACTORS = {
    ("m", "cm"): 100.0,
    ("cm", "m"): 0.01,
    ("kg", "g"): 1000.0,
    ("g", "kg"): 0.001,
    ("L", "mL"): 1000.0,
    ("mL", "L"): 0.001,
}


def unit_convert(value: float, from_unit: str, to_unit: str) -> float:
    if from_unit == to_unit:
        return value
    key = (from_unit, to_unit)
    if key not in UNIT_FACTORS:
        raise ValueError(f"Unsupported conversion: {from_unit} -> {to_unit}")
    return value * UNIT_FACTORS[key]


def classify_change(description: str) -> str:
    d = description.lower()
    chem_words = ["burn", "rust", "react", "oxid", "acid", "base", "precip"]
    if any(w in d for w in chem_words):
        return "chemical"
    return "physical"


def sigfig_round(value: float, sigfigs: int) -> float:
    if value == 0:
        return 0.0
    import math
    return round(value, sigfigs - int(math.floor(math.log10(abs(value)))) - 1)


def uncertainty_report(value: float, uncertainty: float) -> str:
    return f"{value} ± {uncertainty}"


if __name__ == "__main__":
    print(unit_convert(2.5, "L", "mL"))
    print(classify_change("Iron rusts in humid air"))
    print(sigfig_round(12.3456, 3))
    print(uncertainty_report(7.20, 0.05))

MCP_TOOLS = [
    {
        "name": "classify_change",
        "description": "classify_change",
        "parameters": [
            {
                "name": "description",
                "type": "number"
            }
        ]
    },
    {
        "name": "sigfig_round",
        "description": "sigfig_round",
        "parameters": [
            {
                "name": "value",
                "type": "number"
            },
            {
                "name": "sigfigs",
                "type": "number"
            }
        ]
    },
    {
        "name": "uncertainty_report",
        "description": "uncertainty_report",
        "parameters": [
            {
                "name": "value",
                "type": "number"
            },
            {
                "name": "uncertainty",
                "type": "number"
            }
        ]
    },
    {
        "name": "unit_convert",
        "description": "unit_convert",
        "parameters": [
            {
                "name": "value",
                "type": "number"
            },
            {
                "name": "from_unit",
                "type": "number"
            },
            {
                "name": "to_unit",
                "type": "number"
            }
        ]
    }
]
