# Temperature-shifted carbonate alkalinity and scale limits

**Retrieve with:** boiler hardness carbonate scale, temperature dependent Ksp alkalinity, open carbon dioxide carbonate speciation, calcium magnesium scale limit

**Use when:** A water-scaling or hardness problem changes temperature and couples gas-buffered carbonate speciation to saturation of more than one calcium, magnesium, carbonate, or hydroxide solid.

## Procedure

1. From the stated formation enthalpies and entropies, form each required reaction and compute its equilibrium constant at the target temperature from reaction Gibbs energy; keep the reaction direction explicit.
2. Use the initial pH, gas partial pressure, and carbonate equilibria to establish the conserved analytical alkalinity or other conserved inventory before heating rather than carrying the initial pH forward.
3. At the target temperature and stated gas boundary condition, solve charge or alkalinity balance together with carbonate acid-base equilibria to obtain free hydroxide, bicarbonate, and carbonate concentrations.
4. Apply each candidate solid's solubility product independently to the target free-ion concentrations, sum the allowed dissolved metal concentrations requested by the problem, and convert the total once to the specified hardness basis.
5. Check reaction signs, concentration units, omitted scale formers, and whether the gas boundary is open or closed before comparing with numerical choices.

## Preferred Support

- chem-memory/L2_principles/thermodynamics_vant_hoff_equilibrium_tables.md
- chem-memory/L2_principles/coupled_equilibria.md
- chem-memory/L2_principles/solubility_equilibria.md
- chem-memory/L2_principles/ph_calculations.md

## Guards

- Do not hold pH fixed across a temperature change unless the problem explicitly imposes it.
- Distinguish conserved alkalinity from temperature-dependent species concentrations.
- Use free-ion activities or stated concentration approximations in each solubility product.
- Include every independently limiting scale former before converting the summed hardness.
