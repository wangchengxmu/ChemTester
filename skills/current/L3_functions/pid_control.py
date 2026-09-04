"""
PID Control - L3 Implementation

Proportional-Integral-Derivative controller calculations.
Source: Chemical Process Dynamics and Controls (Woolf), Ch9

## Solver Instructions (for AI Agent)

When you encounter process control problems (PID tuning, controller design), follow this decision tree:

### Step 1: Identify what is given and what is asked
- Given Kp, Ki, Kd -> calculate controller output for error?
- Given ultimate gain and period -> calculate PID gains (Ziegler-Nichols)?
- Given setpoint and measurement -> calculate error and output?
- Given process response -> tune controller?

### Step 2: Choose the correct function
| Task | Function | Key Parameters |
|---|---|---|
| PID update | `PIDController.update(measured_value, dt)` | Returns control output |
| Ziegler-Nichols tuning | `ziegler_nichols_tuning(ku, tu, controller_type)` | Returns (Kp, Ki, Kd) |
| Closed-loop gain | `closed_loop_gain(kp, kc)` | K_cl = Kp x Kc / (1 + Kp x Kc) |
| Controller reset | `PIDController.reset()` | Clear integral and derivative terms |

### Step 3: Handle special cases
- Ziegler-Nichols: P-only uses 0.5Ku; PI uses 0.45Ku; PID uses 0.6Ku
- Integral windup: occurs when error persists; can cause overshoot
- Derivative kick: sudden change in setpoint causes spike; use derivative on measurement instead

### Examples
```python
# Example 1: Ziegler-Nichols PID tuning
ziegler_nichols_tuning(10, 5, 'pid')  # Ku=10, Tu=5
# -> (Kp=6.0, Ki=2.4, Kd=3.75)

# Example 2: PID controller
ctrl = PIDController(kp=1.0, ki=0.1, kd=0.01, setpoint=50)
output = ctrl.update(45, 0.1)  # measured=45, dt=0.1s
# -> control output based on error

# Example 3: P-only controller
ziegler_nichols_tuning(8, 4, 'p')
# -> (Kp=4.0, Ki=0.0, Kd=0.0)

# Example 4: PI controller
ziegler_nichols_tuning(8, 4, 'pi')
# -> (Kp=3.6, Ki=1.08, Kd=0.0)
```
"""

import math
from typing import Tuple


class PIDController:
    """PID Controller implementation."""
    
    def __init__(self, kp: float = 1.0, ki: float = 0.0, kd: float = 0.0, setpoint: float = 0.0):
        """
        Initialize PID controller.
        
        Args:
            kp: Proportional gain
            ki: Integral gain
            kd: Derivative gain
            setpoint: Target setpoint value
        """
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self.integral = 0.0
        self.previous_error = 0.0
    
    def update(self, measured_value: float, dt: float) -> float:
        """
        Calculate PID output.
        
        u(t) = Kp*e(t) + Ki*∫e(τ)dτ + Kd*de/dt
        
        Args:
            measured_value: Current process variable
            dt: Time step
        
        Returns:
            Control output
        """
        error = self.setpoint - measured_value
        
        # Proportional term
        p_term = self.kp * error
        
        # Integral term
        self.integral += error * dt
        i_term = self.ki * self.integral
        
        # Derivative term
        if dt > 0:
            d_term = self.kd * (error - self.previous_error) / dt
        else:
            d_term = 0
        
        self.previous_error = error
        
        return p_term + i_term + d_term
    
    def reset(self):
        """Reset controller state."""
        self.integral = 0.0
        self.previous_error = 0.0


def ziegler_nichols_tuning(ku: float, tu: float, controller_type: str = 'pid') -> Tuple[float, float, float]:
    """
    Calculate PID gains using Ziegler-Nichols method.
    
    Args:
        ku: Ultimate gain (at sustained oscillation)
        tu: Ultimate period (oscillation period)
        controller_type: 'p', 'pi', or 'pid'
    
    Returns:
        (Kp, Ki, Kd) gains
    """
    if controller_type == 'p':
        kp = 0.5 * ku
        ki = 0.0
        kd = 0.0
    elif controller_type == 'pi':
        kp = 0.45 * ku
        ki = 0.54 * ku / tu
        kd = 0.0
    else:  # PID
        kp = 0.6 * ku
        ki = 1.2 * ku / tu
        kd = 0.075 * ku * tu
    
    return kp, ki, kd


def closed_loop_gain(kp: float, kc: float) -> float:
    """
    Calculate closed-loop gain.
    
    Kcl = Kp * Kc / (1 + Kp * Kc)
    
    Args:
        kp: Process gain
        kc: Controller gain
    
    Returns:
        Closed-loop gain
    """
    return kp * kc / (1 + kp * kc)


def settling_time(tau: float, zeta: float) -> float:
    """
    Calculate settling time (2% criterion).
    
    Ts ~ 4*τ / ζ
    
    Args:
        tau: Time constant
        zeta: Damping ratio
    
    Returns:
        Settling time
    """
    if zeta <= 0:
        return float('inf')
    return 4 * tau / zeta


def overshoot_percentage(zeta: float) -> float:
    """
    Calculate overshoot percentage from damping ratio.
    
    %OS = 100 * exp(-pi*ζ/√(1-ζ2))
    
    Args:
        zeta: Damping ratio
    
    Returns:
        Overshoot percentage
    """
    if zeta >= 1:
        return 0.0
    
    sqrt_term = math.sqrt(1 - zeta**2)
    exponent = -math.pi * zeta / sqrt_term
    return 100 * math.exp(exponent)


def damping_from_overshoot(overshoot_percent: float) -> float:
    """
    Estimate damping ratio from overshoot percentage.
    
    ζ = √(ln(%OS/100)2 / (pi2 + ln(%OS/100)2))
    
    Args:
        overshoot_percent: Measured overshoot percentage
    
    Returns:
        Estimated damping ratio
    """
    if overshoot_percent <= 0:
        return 1.0  # Critically damped or overdamped
    
    os_decimal = overshoot_percent / 100
    ln_term = math.log(os_decimal)
    
    return math.sqrt(ln_term**2 / (math.pi**2 + ln_term**2))


# TODO: Implement for Pass-3
# - pid_autotune() - Automatic tuning from step response
# - stability_margins() - Gain and phase margins
# - discrete_pid() - Digital implementation
