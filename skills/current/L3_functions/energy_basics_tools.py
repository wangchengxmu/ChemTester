"""
Energy Basics Tools (L3)
Source: LibreTexts Chemistry 2e Ch05.01
## Solver Instructions (for AI Agent)

When you encounter thermochemistry heat/energy problems, follow this decision tree:

### Step 1: Identify what is given and what is asked
- Given mass, specific heat, DeltaT -> Calculate heat? Use `heat_transfer(mass, specific_heat, delta_T)`
- Given heat, mass, specific heat -> Find final temperature? Use `final_temperature(initial_T, heat, mass, specific_heat)`
- Given heat, mass, DeltaT -> Find specific heat? Use `specific_heat_from_heat(mass, heat, delta_T)`
- Need unit conversion (J↔cal↔Cal)? Use `joules_to_calories`, `calories_to_joules`, `joules_to_nutritional_cal`, `nutritional_cal_to_joules`
- Given P, DeltaV -> Calculate PV work? Use `pressure_volume_work(pressure_atm, delta_V_L)`
- Given mass, specific heat -> Calculate heat capacity? Use `heat_capacity(mass, specific_heat)`
- Given C, DeltaT -> Calculate heat? Use `heat_from_heat_capacity(C, delta_T)`
- Need specific heat lookup? Check `SPECIFIC_HEATS` dict (water_liquid=4.184, aluminum=0.897, iron=0.449, etc.)

### Step 2: Choose the correct function
| Scenario | Function | Formula |
|----------|----------|---------|
| Heat from q=mcDeltaT | `heat_transfer(mass, c, delta_T)` | q = m x c x DeltaT (J) |
| Final temperature | `final_temperature(T_i, q, m, c)` | T_f = T_i + q/(mc) |
| Specific heat | `specific_heat_from_heat(m, q, DeltaT)` | c = q/(mxDeltaT) |
| PV work | `pressure_volume_work(P_atm, DeltaV_L)` | w = -PxDeltaV (J) |
| Heat capacity | `heat_capacity(mass, c)` | C = mxc (J/degC) |
| Heat from C | `heat_from_heat_capacity(C, DeltaT)` | q = CxDeltaT |

### Step 3: Handle special cases
- **Sign convention**: q > 0 = absorbed (endothermic), q < 0 = released (exothermic)
- **PV work sign**: Expansion (DeltaV > 0) gives negative work (system does work on surroundings)
- **Unit conversions**: 1 cal = 4.184 J; 1 Cal (nutritional) = 1 kcal = 4184 J
- **SPECIFIC_HEATS dict**: Common values embedded - use for lookups when specific heat not given

### Examples
```python
# Example 1: Heat to raise 100g water by 10degC
heat_transfer(100, 4.184, 10)  # -> 4184 J

# Example 2: Convert 500 Cal to joules
nutritional_cal_to_joules(500)  # -> 2,092,000 J

# Example 3: PV work for gas expansion
pressure_volume_work(1.0, 2.0)  # -> -202.65 J (2L expansion at 1 atm)
```
"""

# === HEAT CALCULATIONS ===

def heat_transfer(mass, specific_heat, delta_T):
    """
    Calculate heat transfer using q = m x c x DeltaT.
    
    Parameters:
        mass: mass in grams
        specific_heat: specific heat capacity in J/(g·degC)
        delta_T: temperature change in degC or K
    
    Returns:
        q: heat in joules (positive = absorbed, negative = released)
    """
    return mass * specific_heat * delta_T


def final_temperature(initial_T, heat, mass, specific_heat):
    """
    Calculate final temperature from heat addition.
    
    DeltaT = q / (m x c)
    
    Parameters:
        initial_T: initial temperature in degC
        heat: heat added in J
        mass: mass in g
        specific_heat: specific heat in J/(g·degC)
    
    Returns:
        final temperature in degC
    """
    delta_T = heat / (mass * specific_heat)
    return initial_T + delta_T


def specific_heat_from_heat(mass, heat, delta_T):
    """
    Calculate specific heat capacity from heat data.
    
    c = q / (m x DeltaT)
    
    Parameters:
        mass: mass in grams
        heat: heat in joules
        delta_T: temperature change in degC
    
    Returns:
        specific heat in J/(g·degC)
    """
    if delta_T == 0:
        raise ValueError("Temperature change cannot be zero")
    return heat / (mass * delta_T)


# === UNIT CONVERSIONS ===

def joules_to_calories(joules):
    """Convert joules to calories."""
    return joules / 4.184


def calories_to_joules(calories):
    """Convert calories to joules."""
    return calories * 4.184


def joules_to_nutritional_cal(joules):
    """Convert joules to nutritional Calories (kcal)."""
    return joules / 4184


def nutritional_cal_to_joules(Cal):
    """Convert nutritional Calories to joules."""
    return Cal * 4184


# === WORK CALCULATIONS ===

def pressure_volume_work(pressure_atm, delta_V_L):
    """
    Calculate pressure-volume work.
    
    w = -P x DeltaV
    
    Parameters:
        pressure_atm: pressure in atm
        delta_V_L: volume change in liters
    
    Returns:
        work in joules
    """
    # 1 L·atm = 101.325 J
    L_atm_to_J = 101.325
    return -pressure_atm * delta_V_L * L_atm_to_J


# === HEAT CAPACITY ===

def heat_capacity(mass, specific_heat):
    """
    Calculate total heat capacity.
    
    C = m x c
    
    Parameters:
        mass: mass in grams
        specific_heat: specific heat in J/(g·degC)
    
    Returns:
        heat capacity in J/degC
    """
    return mass * specific_heat


def heat_from_heat_capacity(C, delta_T):
    """
    Calculate heat from heat capacity.
    
    q = C x DeltaT
    
    Parameters:
        C: heat capacity in J/degC
        delta_T: temperature change in degC
    
    Returns:
        heat in joules
    """
    return C * delta_T


# === COMMON SPECIFIC HEATS ===

SPECIFIC_HEATS = {
    'water_liquid': 4.184,
    'water_solid': 2.09,
    'water_gas': 2.01,
    'ice': 2.03,
    'aluminum': 0.897,
    'iron': 0.449,
    'copper': 0.385,
    'gold': 0.129,
    'silver': 0.235,
    'lead': 0.129,
}


if __name__ == "__main__":
    print("Energy basics tools - implemented")
    
    # Test heat transfer
    q = heat_transfer(100.0, 4.184, 10.0)
    print(f"Heat to raise 100 g water by 10degC: {q:.1f} J")
    
    # Test unit conversion
    cal = joules_to_calories(1000)
    print(f"1000 J = {cal:.1f} cal")
    
    # Test PV work
    w = pressure_volume_work(1.0, 2.0)
    print(f"Work for expansion by 2 L at 1 atm: {w:.1f} J")


# MCP Tool Declarations
MCP_TOOLS = [
    {
        "name": "calories_to_joules",
        "description": "Convert calories to joules.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "calories": {"type": "number", "description": "Calories"},
            },
            "required": ["calories"]
        }
    },
    {
        "name": "final_temperature",
        "description": "Calculate final temperature from heat addition.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "initial_T": {"type": "number", "description": "Initial T"},
                "heat": {"type": "number", "description": "Heat"},
                "mass": {"type": "number", "description": "Mass"},
                "specific_heat": {"type": "number", "description": "Specific Heat"},
            },
            "required": ["initial_T", "heat", "mass", "specific_heat"]
        }
    },
    {
        "name": "heat_capacity",
        "description": "Calculate total heat capacity.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "mass": {"type": "number", "description": "Mass"},
                "specific_heat": {"type": "number", "description": "Specific Heat"},
            },
            "required": ["mass", "specific_heat"]
        }
    },
    {
        "name": "heat_from_heat_capacity",
        "description": "Calculate heat from heat capacity.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "C": {"type": "number", "description": "C"},
                "delta_T": {"type": "number", "description": "Delta T"},
            },
            "required": ["C", "delta_T"]
        }
    },
    {
        "name": "heat_transfer",
        "description": "Calculate heat transfer using q = m \u00d7 c \u00d7 \u0394T.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "mass": {"type": "number", "description": "Mass"},
                "specific_heat": {"type": "number", "description": "Specific Heat"},
                "delta_T": {"type": "number", "description": "Delta T"},
            },
            "required": ["mass", "specific_heat", "delta_T"]
        }
    },
    {
        "name": "joules_to_calories",
        "description": "Convert joules to calories.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "joules": {"type": "number", "description": "Joules"},
            },
            "required": ["joules"]
        }
    },
    {
        "name": "joules_to_nutritional_cal",
        "description": "Convert joules to nutritional Calories (kcal).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "joules": {"type": "number", "description": "Joules"},
            },
            "required": ["joules"]
        }
    },
    {
        "name": "nutritional_cal_to_joules",
        "description": "Convert nutritional Calories to joules.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "Cal": {"type": "number", "description": "Cal"},
            },
            "required": ["Cal"]
        }
    },
    {
        "name": "pressure_volume_work",
        "description": "Calculate pressure-volume work.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "pressure_atm": {"type": "number", "description": "Pressure Atm"},
                "delta_V_L": {"type": "number", "description": "Delta V L"},
            },
            "required": ["pressure_atm", "delta_V_L"]
        }
    },
    {
        "name": "specific_heat_from_heat",
        "description": "Calculate specific heat capacity from heat data.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "mass": {"type": "number", "description": "Mass"},
                "heat": {"type": "number", "description": "Heat"},
                "delta_T": {"type": "number", "description": "Delta T"},
            },
            "required": ["mass", "heat", "delta_T"]
        }
    }
]
