"""Deterministic audits for verbal product constraints in reaction problems."""

from __future__ import annotations

import re


_ELEMENT_TOKEN = re.compile(r"[A-Z][a-z]?")


def audit_gas_product_constraints(
    gas_formulas,
    expected_gas_count=None,
    require_elemental_gases=False,
):
    """Audit gas count and elemental gas-composition constraints.

    Args:
        gas_formulas: Product gas formulas selected for a candidate equation.
        expected_gas_count: Required number of distinct gaseous products, if stated.
        require_elemental_gases: True when every released gas must be a simple
            substance made from only one chemical element.

    Returns:
        A structured audit with per-gas elements, count and elementality checks,
        violations, and an overall accepted flag.
    """
    if isinstance(gas_formulas, (str, bytes)) or not isinstance(
        gas_formulas, (list, tuple)
    ):
        raise TypeError("gas_formulas must be a list or tuple of formulas")
    if expected_gas_count is not None:
        if isinstance(expected_gas_count, bool) or not isinstance(
            expected_gas_count, int
        ):
            raise TypeError("expected_gas_count must be an integer or None")
        if expected_gas_count < 0:
            raise ValueError("expected_gas_count must be nonnegative")
    if not isinstance(require_elemental_gases, bool):
        raise TypeError("require_elemental_gases must be a boolean")

    normalized = []
    for value in gas_formulas:
        formula = str(value).strip()
        if not formula:
            raise ValueError("gas formulas must be nonempty")
        elements = sorted(set(_ELEMENT_TOKEN.findall(formula)))
        if not elements:
            raise ValueError(f"Gas formula contains no element symbols: {formula}")
        normalized.append(
            {
                "formula": formula,
                "elements": elements,
                "elemental": len(elements) == 1,
            }
        )

    count_matches = (
        expected_gas_count is None or len(normalized) == expected_gas_count
    )
    elemental_matches = not require_elemental_gases or all(
        item["elemental"] for item in normalized
    )
    violations = []
    if not count_matches:
        violations.append(
            f"expected {expected_gas_count} gaseous product(s), found {len(normalized)}"
        )
    if not elemental_matches:
        compound_gases = [
            item["formula"] for item in normalized if not item["elemental"]
        ]
        violations.append(
            "non-elemental gas products: " + ", ".join(compound_gases)
        )

    return {
        "gas_count": len(normalized),
        "gas_audit": normalized,
        "expected_gas_count": expected_gas_count,
        "require_elemental_gases": require_elemental_gases,
        "count_matches": count_matches,
        "elemental_matches": elemental_matches,
        "violations": violations,
        "accepted": count_matches and elemental_matches,
    }


MCP_TOOLS = [
    {
        "name": "audit_gas_product_constraints",
        "description": (
            "Audit the number of gaseous products and whether each gas is an "
            "elemental simple substance rather than a compound."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "gas_formulas": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Distinct gaseous product formulas",
                },
                "expected_gas_count": {
                    "type": ["integer", "null"],
                    "description": "Required number of gas products, if stated",
                },
                "require_elemental_gases": {
                    "type": "boolean",
                    "description": "Require each gas to contain only one element",
                    "default": False,
                },
            },
            "required": ["gas_formulas"],
        },
    }
]
