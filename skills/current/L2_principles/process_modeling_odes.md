# Process Modeling with ODEs

[Source: Chemical Process Dynamics and Controls (Woolf), Ch2, Ch6]

## Core Concept

Mathematical models describe process dynamics using ordinary differential equations (ODEs) derived from conservation laws (mass, energy, momentum balances).

## General Balance Equation

$$\frac{d(\text{Accumulation})}{dt} = \text{Input} - \text{Output} + \text{Generation} - \text{Consumption}$$

## Stirred Tank Model (CSTR)

### Mass Balance
$$V\frac{dC_A}{dt} = F_{in} C_{A,in} - F_{out} C_A - r_A V$$

### Energy Balance
$$\rho C_p V \frac{dT}{dt} = \rho C_p F_{in} (T_{in} - T) + (-\Delta H_r) r_A V - UA(T - T_c)$$

## Linearization

Nonlinear ODEs are linearized around a steady state using Taylor expansion:

$$\frac{dx}{dt} \approx \left.\frac{\partial f}{\partial x}\right|_{ss} \cdot x' + \left.\frac{\partial f}{\partial u}\right|_{ss} \cdot u'$$

where $x' = x - x_{ss}$ and $u' = u - u_{ss}$.

## State-Space Representation

$$\frac{d\mathbf{x}}{dt} = \mathbf{A}\mathbf{x} + \mathbf{B}\mathbf{u}$$
$$\mathbf{y} = \mathbf{C}\mathbf{x} + \mathbf{D}\mathbf{u}$$

- $\mathbf{x}$ = state variables
- $\mathbf{u}$ = inputs
- $\mathbf{y}$ = outputs
- $\mathbf{A}$ = system matrix (determines stability)

## Deviation Variables

Transform to work around steady state:
$$x' = x - x_{ss}$$

This eliminates constant terms and simplifies to homogeneous form for linear analysis.

## Common Process Models

| Process | ODE | Transfer Function |
|---------|-----|-------------------|
| First-order tank | $\tau \frac{dy}{dt} + y = Ku$ | $\frac{K}{\tau s + 1}$ |
| Non-interacting tanks | $\tau_1\tau_2 \frac{d^2y}{dt^2} + (\tau_1+\tau_2)\frac{dy}{dt} + y = Ku$ | $\frac{K}{(\tau_1 s+1)(\tau_2 s+1)}$ |
| Pure delay | $y(t) = u(t-\theta)$ | $e^{-\theta s}$ |

## Problem Types

1. Derive ODE model from process description
2. Linearize nonlinear models around steady state
3. Convert ODE to transfer function via Laplace transform
4. Solve simple ODE models analytically
5. Identify steady states from ODE models

## Related L2 Nodes

- `transfer_functions.md` — Laplace domain conversion
- `pid_control.md` — Controller design
