# Competitive ITC affinity identifiability

**Retrieve with:** competitive ITC apparent affinity, displacement calorimetry mass balance, free competitor concentration, binding model identifiability

**Use when:** An ITC displacement or competition problem asks for an intrinsic binding constant from a fitted affinity measured in the presence of another ligand.

## Procedure

1. Label every reported constant by experiment and fit model: intrinsic single-ligand constant, conditional apparent constant, or parameter from a competitive global fit.
2. Require mutually exclusive binding at the same independent sites; shared inhibition and near-unity stoichiometry alone do not establish competition.
3. Only for a fixed-free-competitor one-site model use Kd,app,A = Kd,A(1 + [B]free/Kd,B), equivalently Ka,A = (1 + [B]free/Kd,B)/Kd,app,A.
4. Derive free competitor by mass balance rather than using nominal excess; if concentrations change during injections, use the full conservation and heat model.
5. If the binding model, free-concentration trajectory, or fitted-parameter meaning is unspecified, report the intrinsic affinity as non-identifiable instead of forcing a numerical conversion.

## Guards

- Do not infer a shared binding site merely because both ligands bind one target with similar stoichiometry.
- Do not assume a displacement-run fitted Kd is an apparent or intrinsic Kd without the stated fitting model.
- Do not substitute total competitor for free competitor when binding depletion can be material.
- Do not add a deterministic calculator when missing model assumptions, rather than arithmetic, prevent a unique result.
