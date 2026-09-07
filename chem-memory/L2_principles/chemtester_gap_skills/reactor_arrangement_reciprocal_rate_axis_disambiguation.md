# Reciprocal-rate axis choice for reactor arrangements

**Retrieve with:** reactor arrangement reciprocal rate concentration, ideal reactor sequence rate concentration curve, Levenspiel plot concentration conversion, reactors in series arrangement

**Use when:** Use when selecting or comparing an arrangement of ideal reactor units from rate plots, especially when candidate methods differ by concentration versus conversion axes or by sizing versus sequencing purpose.

## Procedure

1. Classify the task first: sizing a reactor at a target conversion and sequencing a fixed set of reactor units are related but distinct design questions.
2. For the classic single-reaction sequencing heuristic, express the positive reciprocal disappearance rate as a function of reactant concentration and use the curve shape to identify orderings that retain favorable-rate concentration regions.
3. Use a conversion-axis plot only after deriving the concentration-conversion mapping from the material balance and accounting for volumetric-flow or density changes; preserve axis direction and any Jacobian needed for area arguments.
4. Match each proposed method to the requested design purpose and stated assumptions instead of selecting a plot solely from its familiar name.
5. Check the sequence qualitatively against the rate curve: it should avoid unnecessary reactor volume in high reciprocal-rate regions.

## Guards

- Do not treat a conversion-based sizing plot as automatically interchangeable with a concentration-state arrangement plot.
- Do not assume C_A = C_A0(1-X_A) unless constant volumetric flow is justified.
- Use -r_A as a positive disappearance rate and keep concentration and conversion axis directions distinct.
- A temperature profile is not a universal sequencing criterion unless nonisothermal effects are explicitly part of the design.
