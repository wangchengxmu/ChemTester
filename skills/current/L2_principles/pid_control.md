# PID Control

[Source: Chemical Process Dynamics and Controls (Woolf), Ch9]

## Core Concept

Proportional-Integral-Derivative (PID) control is the most common control algorithm in industrial process control. It combines three control actions to maintain a process variable at setpoint.

## Control Equation

$$u(t) = K_p e(t) + K_i \int_0^t e(\tau) d\tau + K_d \frac{de(t)}{dt}$$

where:
- $u(t)$ = Control output
- $e(t)$ = Error = Setpoint - Process Variable
- $K_p$ = Proportional gain
- $K_i$ = Integral gain
- $K_d$ = Derivative gain

## Control Actions

| Action | Term | Effect |
|--------|------|--------|
| Proportional (P) | $K_p e(t)$ | Immediate response to error |
| Integral (I) | $K_i \int e \, dt$ | Eliminates steady-state error |
| Derivative (D) | $K_d \frac{de}{dt}$ | Anticipates future error |

## Controller Tuning

### Ziegler-Nichols Method

1. Set $K_i = K_d = 0$
2. Increase $K_p$ until system oscillates (ultimate gain $K_u$)
3. Measure oscillation period $T_u$
4. Calculate gains:
   - P: $K_p = 0.5 K_u$
   - PI: $K_p = 0.45 K_u$, $K_i = 0.54 K_u / T_u$
   - PID: $K_p = 0.6 K_u$, $K_i = 1.2 K_u / T_u$, $K_d = 0.075 K_u T_u$

## Problem Types

1. **Calculate controller output** given error and gains
2. **Tune controller** using Ziegler-Nichols
3. **Analyze closed-loop response** stability
4. **Select control mode** (P, PI, PID) for application

## Related Topics

- â?`process_safety_analysis.md` for safety systems
- â?`process_economics.md` for economic impact


## Implementations

- Implementation: `../L3_functions/pid_control.py`

## L3 Tool Call Directives

**Source:** pid_control.py
PID Control - L3 Implementation

### Available functions:
- ziegler_nichols_tuning(ku, tu, controller_type) →  — Calculate PID gains using Ziegler-Nichols method.
- closed_loop_gain(kp, kc) → float — Calculate closed-loop gain.
- settling_time(tau, zeta) → float — Calculate settling time (2% criterion).
- overshoot_percentage(zeta) → float — Calculate overshoot percentage from damping ratio.
- damping_from_overshoot(overshoot_percent) → float — Estimate damping ratio from overshoot percentage.
- update(self, measured_value, dt) → float — Calculate PID output.
- reset(self) →  — Reset controller state.

### Common errors:
- ❌ Passing wrong parameter types or missing required arguments
