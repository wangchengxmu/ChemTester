# Control Architectures

[Source: Chemical Process Dynamics and Controls (Woolf), Ch11]

## Core Concept

Control architectures define how controllers are organized to manage process variables. Beyond single-loop PID, more sophisticated architectures handle multivariable interactions and disturbances.

## Feedback Control (Single Loop)

The standard architecture: controller adjusts manipulated variable based on measured error.

**Advantages**: Simple, handles unknown disturbances
**Disadvantages**: Reacts only after error occurs; poor for slow processes or large disturbances

## Feedforward Control

Measures disturbance directly and adjusts manipulated variable before the process is affected.

$$U_{ff}(s) = -\frac{G_d(s)}{G_p(s)} D(s)$$

where $G_d(s)$ is the disturbance transfer function and $G_p(s)$ is the process transfer function.

**Advantages**: Acts before error develops
**Disadvantages**: Requires disturbance measurement; model-dependent; cannot handle unmeasured disturbances

## Feedforward + Feedback (Combined)

Best of both worlds: feedforward handles major measured disturbances, feedback corrects residual error.

$$U(s) = U_{ff}(s) + U_{fb}(s)$$

## Cascade Control

Two controllers in series: secondary (inner) loop controls a fast-responding variable, primary (outer) loop controls the main process variable.

**Requirements for cascade:**
1. Secondary variable must respond faster than primary
2. Secondary loop must significantly affect the primary variable
3. Secondary variable must be measurable

**Common applications:**
- Temperature control via flow (inner) → temperature (outer)
- Composition control via flow (inner) → composition (outer)

## Ratio Control

Maintains a fixed ratio between two flow rates:

$$u_2 = K_r \cdot u_1$$

**Applications**: Reactant feed ratios, fuel/air ratio, blending operations.

## Split-Range Control

One controller output drives two (or more) manipulated variables, each operating over a different output range.

**Example**: Temperature control where both heating and cooling valves share one controller output (0-50% → cooling, 50-100% → heating).

## Override (Selective) Control

Multiple controllers compete; the one demanding the lowest (or highest) output wins. Protects equipment from constraints.

**Applications**: Preventing high pressure, low level, high temperature.

## Inferential Control

Uses easily measurable secondary variables to estimate the primary variable when direct measurement is difficult or slow.

**Example**: Using tray temperatures to estimate distillation composition.

## MIMO Control (Book Ch12)

For processes with multiple inputs and multiple outputs where loops interact.

### Pairing: Relative Gain Array (RGA)

$$\lambda_{ij} = \frac{(\partial y_i / \partial u_j)|_{u_k=const}}{(\partial y_i / \partial u_j)|_{y_k=const}}$$

**Niederlinski Index** for stability:
$$N = \frac{|K|}{\prod_{i=1}^n K_{ii}}$$

Stable if $N > 0$ and $\lambda_{ii} > 0$ for all pairs.

### Decoupling

Add cross-controllers to eliminate loop interactions.

## Problem Types

1. Select appropriate control architecture for a given process
2. Design feedforward controller from process/disturbance models
3. Determine cascade controller pairing
4. Calculate RGA for MIMO pairing decisions
5. Analyze stability of multiloop systems

## Related L2 Nodes

- `pid_control.md` — Single-loop PID
- `transfer_functions.md` — Laplace domain analysis
