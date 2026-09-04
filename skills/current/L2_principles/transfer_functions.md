# Transfer Functions

[Source: Chemical Process Dynamics and Controls (Woolf), Ch7]

## Core Concept

Transfer functions model the input-output relationship of linear time-invariant (LTI) systems in the Laplace domain. They are fundamental to process control analysis.

## Definition

For a linear ODE system with zero initial conditions:

$$Y(s) = G(s) \cdot U(s)$$

where $G(s)$ is the transfer function, $Y(s)$ is the output, and $U(s)$ is the input.

$$G(s) = \frac{Y(s)}{U(s)}$$

## Common Transfer Function Models

### First-Order System
$$G(s) = \frac{K}{\tau s + 1}$$

- $K$ = steady-state gain (process gain)
- $\tau$ = time constant (response speed)
- Step response: reaches 63.2% of final value at $t = \tau$

### Second-Order System
$$G(s) = \frac{K}{\tau^2 s^2 + 2\zeta\tau s + 1}$$

- $\zeta$ = damping ratio (underdamped: $\zeta < 1$, overdamped: $\zeta > 1$, critically damped: $\zeta = 1$)
- $\omega_n = 1/\tau$ = natural frequency

### Integrating Process
$$G(s) = \frac{K}{s}$$

### Time Delay (Dead Time)
$$G(s) = e^{-\theta s}$$

### First-Order Plus Dead Time (FOPDT)
$$G(s) = \frac{K e^{-\theta s}}{\tau s + 1}$$

This is the most common process model for controller tuning.

## Block Diagram Algebra

### Series (Cascade)
$$G_{total} = G_1(s) \cdot G_2(s)$$

### Parallel
$$G_{total} = G_1(s) + G_2(s)$$

### Feedback (Negative)
$$G_{closed} = \frac{G(s)}{1 + G(s)H(s)}$$

where $H(s)$ is the feedback transfer function.

## Stability Criterion

A system is stable if all poles of $G(s)$ have negative real parts (lie in the left half of the s-plane).

### Routh-Hurwitz Criterion
For characteristic equation $a_n s^n + a_{n-1} s^{n-1} + \cdots + a_0 = 0$, construct the Routh array. System is stable if all elements in the first column have the same sign.

## Step Response Characteristics

| Parameter | Definition |
|-----------|-----------|
| Rise time $t_r$ | Time from 10% to 90% of final value |
| Settling time $t_s$ | Time to reach within ±2% of final value ($\approx 4\tau$ for first-order) |
| Overshoot | Maximum value minus final value (for underdamped systems) |
| Steady-state error | $e_{ss} = 1 - K$ (for unit step with $K$ as gain) |

## Frequency Response

Substituting $s = j\omega$:

$$G(j\omega) = |G(j\omega)| e^{j\phi(\omega)}$$

- Bode plot: $|G(j\omega)|$ and $\phi(\omega)$ vs $\omega$
- Gain margin: gain at phase crossover ($\phi = -180°$)
- Phase margin: phase at gain crossover ($|G| = 1$, i.e., 0 dB)

## Problem Types

1. Derive transfer function from ODE
2. Convert between time domain and Laplace domain
3. Analyze stability using poles or Routh-Hurwitz
4. Calculate step response parameters
5. Construct Bode plots and determine margins

## L3 Tools

- `pid_control.py` — PID simulation and tuning (includes transfer function response)

## Related L2 Nodes

- `pid_control.md` — PID controller design
