# L2 Topic: Membrane Structure and Transport

**Source**: Fundamentals of Biochemistry (Jakubowski/Flatt)
**Created**: 2026-03-18
**Status**: Pass-1

---

## Concept Overview

Biological membranes are lipid bilayers with embedded proteins that control molecular traffic and cell signaling. Transport mechanisms maintain cellular homeostasis.

### Key Features
1. **Lipid bilayer**: Phospholipids with hydrophobic core
2. **Membrane proteins**: Integral and peripheral
3. **Selective permeability**: Controlled by transport proteins
4. **Electrochemical gradients**: Drive transport and signaling

---

## Core Principles

### Membrane Composition

| Component | % by Weight | Function |
|-----------|-------------|----------|
| Phospholipids | 40-50% | Structural matrix |
| Cholesterol | 0-50% | Modulates fluidity |
| Proteins | 20-70% | Transport, signaling |
| Carbohydrates | 2-10% | Cell recognition |

### Passive Transport

| Type | Energy | Direction | Examples |
|------|--------|-----------|----------|
| Simple diffusion | None | Down gradient | O₂, CO₂, H₂O |
| Facilitated diffusion | None | Down gradient | Glucose (GLUT), Ions (channels) |

### Active Transport

| Type | Energy | Examples |
|------|--------|----------|
| Primary | ATP hydrolysis | Na⁺/K⁺ ATPase, Ca²⁺ ATPase |
| Secondary | Ion gradient | Na⁺/glucose symport, Na⁺/Ca²⁺ antiport |
| Group translocation | Chemical modification | PEP-dependent PTS |

### Key Transport Proteins

| Transporter | Type | Stoichiometry |
|-------------|------|---------------|
| Na⁺/K⁺ ATPase | Antiport | 3 Na⁺ out / 2 K⁺ in |
| Ca²⁺ ATPase | Uniport | 1 Ca²⁺ out |
| Na⁺/glucose symport | Symport | 2 Na⁺ + 1 glucose in |
| GLUT1 | Facilitated | 1 glucose |

---

## Key Formulas

### Fick's Law (Passive Diffusion)
$$J = -D \frac{dC}{dx}$$

### Flux Equation
$$J = P(C_{out} - C_{in})$$

Where P = permeability coefficient

### Nernst Equation
$$E = \frac{RT}{zF} \ln \frac{[ion]_{out}}{[ion]_{in}} = \frac{61.5}{z} \log \frac{[ion]_{out}}{[ion]_{in}} \text{ mV}$$

### Goldman-Hodgkin-Katz Equation
$$V_m = \frac{RT}{F} \ln \frac{P_K[K^+]_{out} + P_{Na}[Na^+]_{out} + P_{Cl}[Cl^-]_{in}}{P_K[K^+]_{in} + P_{Na}[Na^+]_{in} + P_{Cl}[Cl^-]_{out}}$$

### ATP Cost for Na⁺/K⁺ ATPase
$$\text{1 ATP} \rightarrow \text{3 Na}^+_{out} + \text{2 K}^+_{in}$$

---

## L3 Implementations Needed

| Function | Purpose |
|----------|---------|
| `nernst_potential` | Calculate equilibrium potential |
| `ghk_voltage` | Membrane potential |
| `transport_rate` | Model carrier kinetics |
| `atp_cost_ion_pump` | ATP for ion gradients |

## L4 Data Needed

| Table | Content |
|-------|---------|
| `ion_concentrations.csv` | Intracellular/extracellular [ion] |
| `permeability_coefficients.csv` | P values for various molecules |

## L5 Examples Needed

| Example | Topic |
|---------|-------|
| Resting membrane potential | GHK calculation |
| ATP cost calculation | Ion homeostasis |

---

**Cross-links:**
- lipid_chemistry.md
- bioenergetics.md
- signal_transduction.md
