# Periodic Trends

## Concept Overview

Periodic trends describe how element properties vary systematically across periods and groups.

## Key Principles

### Major Trends
| Trend | Across Period | Down Group |
|-------|---------------|------------|
| Atomic radius | Decreases | Increases |
| Ionization energy | Increases | Decreases |
| Electronegativity | Increases | Decreases |
| Electron affinity | Increases | Decreases |

### Element Classifications
- **Metals**: Low IE, low EN, form cations
- **Nonmetals**: High IE, high EN, form anions
- **Metalloids**: Intermediate, semiconductors

## Links

- **L3 Tools**: `../L3_functions/periodic_trends_tools.py`
- **L4 Reference**: Element property tables
- **L5 Examples**: Trend predictions

## L3 Tool Call Directives

**Source:** `periodic_trends_tools.py`
Atomic radius, ionization energy, electronegativity comparisons and element classification.

### Available functions:
- `predict_atomic_radius_trend(element1, element2)` → str — Which has larger radius
- `predict_ionization_energy_trend(element1, element2)` → str — Which has higher IE
- `compare_electronegativity(element1, element2)` → dict — EN values + difference + more electronegative
- `classify_element(element)` → str — metal/metalloid/nonmetal
- `oxide_type(element)` → str — acidic/basic/amphoteric oxide prediction
- `bond_type_prediction(element1, element2)` → str — nonpolar covalent (<0.4ΔEN), polar covalent (<1.7), ionic

### Common errors:
- ❌ Using lowercase element symbols — must match database keys exactly (e.g., 'Na' not 'na')
- ❌ Forgetting IE exceptions: Be > B, N > O, Ga < Al (d-block contraction)
- ❌ Requesting elements not in database — only periods 1–4 covered
