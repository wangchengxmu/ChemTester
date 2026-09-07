# Fractional-coordinate polyhedron metric reconstruction

**Retrieve with:** fractional coordinate bond angle, tetragonal disphenoid geometry, crystal lattice Cartesian metric, periodic symmetry equivalent positions

**Use when:** A crystal-structure problem gives fractional coordinates or layered symmetry, a distorted-polyhedron angle, and asks for a lattice parameter or local geometry.

## Procedure

1. Enumerate the symmetry-related and periodic-image vertices that actually form the stated polyhedron, using nearest-image fractional differences.
2. Convert every fractional difference with the lattice matrix. For tetragonal vertices (±a/2,0,zc) and (0,±a/2,(1-z)c), define Δ=|1-2z|c and construct the edge vectors explicitly.
3. Compute all unique angle classes from cos θ=(u·v)/(|u||v|). For this disphenoid, the classes obey cos θ1=a/[2√(a²/2+Δ²)] and cos θ2=Δ²/(a²/2+Δ²).
4. Match the stated larger or smaller angle before solving. For the θ2 class, use c=a√[cos θ/(2(1-cos θ))]/|1-2z|; otherwise solve the corresponding dot-product equation.
5. Back-substitute the result to reproduce every angle class and check periodic images, units, and option rounding.

## Guards

- Never treat one fractional-axis component as a complete Cartesian edge length.
- Do not choose an angle equation until all unique angle classes have been calculated and ordered.
- Apply symmetry and minimum-image conventions before computing distances or angles.
- Reject a solution that fails back-substitution into the reported angle class.
