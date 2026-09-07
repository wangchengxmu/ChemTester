from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import pytest

from scripts.chemistry_expert import native_skill_calculate as calculator


def write_synthetic_bundle(tmp_path: Path) -> tuple[Path, dict[str, object]]:
    tools = tmp_path / "tools"
    tools.mkdir(parents=True, exist_ok=True)
    (tools / "demo.py").write_text(
        "print('diagnostic from synthetic module')\n"
        "def success(value):\n"
        "    print('diagnostic from synthetic call')\n"
        "    return {'value': value}\n"
        "\n"
        "def add(left, right):\n"
        "    return {'value': left + right}\n",
        encoding="utf-8",
    )
    catalog: dict[str, object] = {
        "tools": {
            "demo.success": {
                "summary": "Synthetic successful calculator",
                "contract": {
                    "result_type": "object",
                    "required_result_keys": ["value"],
                },
            },
            "demo.add": {
                "summary": "Synthetic addition calculator",
                "contract": {
                    "result_type": "object",
                    "required_result_keys": ["value"],
                },
            },
        }
    }
    (tmp_path / "catalog.json").write_text(
        json.dumps(catalog),
        encoding="utf-8",
    )
    return tools, catalog


def test_finite_json_rejects_nested_nan_and_infinity():
    assert calculator.finite_json({"nested": [1, {"value": 2.5}]}) == {
        "nested": [1, {"value": 2.5}]
    }

    for value in (math.nan, math.inf, -math.inf):
        with pytest.raises(ValueError, match="Non-finite"):
            calculator.finite_json({"nested": [{"value": value}]})


def test_input_contract_enforces_combined_array_cap_of_six():
    contract = {
        "max_items_combined": {
            "parameters": ["reactants", "products"],
            "maximum": 6,
        }
    }

    calculator.input_contract(
        {"reactants": ["A"] * 3, "products": ["B"] * 3},
        contract,
    )
    with pytest.raises(ValueError, match="exceeds 6"):
        calculator.input_contract(
            {"reactants": ["A"] * 4, "products": ["B"] * 3},
            contract,
        )
    with pytest.raises(ValueError, match="JSON arrays"):
        calculator.input_contract(
            {"reactants": ("A",), "products": []},
            contract,
        )


def test_input_contract_accepts_allowed_values_and_positive_parameters():
    contract = {
        "allowed_values": {"crystal_system": ["cubic", "hexagonal"]},
        "positive_parameters": ["edge_length", "replicates"],
    }

    calculator.input_contract(
        {
            "crystal_system": "cubic",
            "edge_length": 4.2,
            "replicates": 1,
        },
        contract,
    )


def test_input_contract_rejects_invalid_enum():
    contract = {
        "allowed_values": {"crystal_system": ["cubic", "hexagonal"]},
        "positive_parameters": ["edge_length"],
    }

    with pytest.raises(ValueError, match="must be one of"):
        calculator.input_contract(
            {"crystal_system": "triclinic", "edge_length": 1},
            contract,
        )


@pytest.mark.parametrize("value", [0, -1, -0.5, "4.2", True, False])
def test_input_contract_rejects_nonpositive_nonnumeric_or_bool(value):
    contract = {"positive_parameters": ["edge_length"]}

    with pytest.raises(ValueError, match="positive number"):
        calculator.input_contract(
            {"edge_length": value},
            contract,
        )


@pytest.mark.parametrize(
    ("result", "message"),
    [
        (None, "no result"),
        ({"error": "failed"}, "reported failure"),
        ({"success": False}, "reported failure"),
        ({"ok": False}, "reported failure"),
        ({"value": math.inf}, "Non-finite"),
        ({"other": 1}, "missing required keys"),
    ],
)
def test_output_contract_rejects_invalid_results(result, message):
    contract = {"result_type": "object", "required_result_keys": ["value"]}

    with pytest.raises(ValueError, match=message):
        calculator.output_contract(result, contract)


def test_execute_rejects_unknown_and_inactive_calculator_ids(tmp_path):
    catalog = {"tools": {"demo.active": {"contract": {}}}}

    for tool_id in ("demo.unknown", "demo.inactive"):
        with pytest.raises(ValueError, match="Unknown or inactive"):
            calculator.execute(tmp_path, catalog, tool_id, {})


def test_execute_rejects_missing_and_unexpected_kwargs(tmp_path):
    _tools, catalog = write_synthetic_bundle(tmp_path)

    with pytest.raises(TypeError, match="missing a required argument"):
        calculator.execute(tmp_path, catalog, "demo.add", {"left": 2})
    with pytest.raises(TypeError, match="unexpected keyword argument"):
        calculator.execute(
            tmp_path,
            catalog,
            "demo.add",
            {"left": 2, "right": 3, "extra": 4},
        )


def test_execute_synthetic_module_is_standalone_and_redirects_diagnostics(
    tmp_path,
    capsys,
):
    _tools, catalog = write_synthetic_bundle(tmp_path)

    response = calculator.execute(
        tmp_path,
        catalog,
        "demo.success",
        {"value": 7},
    )
    captured = capsys.readouterr()

    assert response["ok"] is True
    assert response["tool_id"] == "demo.success"
    assert response["result"] == {"value": 7}
    assert captured.out == ""
    assert "diagnostic from synthetic module" in captured.err
    assert "diagnostic from synthetic call" in captured.err


def test_execute_converts_json_lists_for_ndarray_annotation_and_serializes_result(
    tmp_path,
    capsys,
):
    tools = tmp_path / "tools"
    tools.mkdir(parents=True, exist_ok=True)
    (tools / "matrix.py").write_text(
        "from __future__ import annotations\n"
        "import numpy as np\n"
        "\n"
        "def gram(matrix: np.ndarray) -> dict[str, np.ndarray]:\n"
        "    print('diagnostic from ndarray call')\n"
        "    return {'value': matrix.T @ matrix}\n",
        encoding="utf-8",
    )
    catalog = {
        "tools": {
            "matrix.gram": {
                "contract": {
                    "result_type": "object",
                    "required_result_keys": ["value"],
                }
            }
        }
    }

    response = calculator.execute(
        tmp_path,
        catalog,
        "matrix.gram",
        {"matrix": [[1, 2], [3, 4]]},
    )
    captured = capsys.readouterr()

    assert response["ok"] is True
    assert response["result"] == {"value": [[10, 14], [14, 20]]}
    assert captured.out == ""
    assert "diagnostic from ndarray call" in captured.err


def test_cli_list_describe_call_and_error_are_json_with_expected_exit_codes(
    tmp_path,
    monkeypatch,
    capsys,
):
    _tools, catalog = write_synthetic_bundle(tmp_path)
    monkeypatch.setattr(
        calculator,
        "__file__",
        str(tmp_path / "native_skill_calculate.py"),
    )

    monkeypatch.setattr(sys, "argv", ["native_skill_calculate.py", "--list"])
    assert calculator.main() == 0
    listed = json.loads(capsys.readouterr().out)
    assert listed == {
        "demo.success": "Synthetic successful calculator",
        "demo.add": "Synthetic addition calculator",
    }

    monkeypatch.setattr(
        sys,
        "argv",
        ["native_skill_calculate.py", "--describe", "demo.success"],
    )
    assert calculator.main() == 0
    described = json.loads(capsys.readouterr().out)
    assert described == catalog["tools"]["demo.success"]

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "native_skill_calculate.py",
            "--call",
            "demo.success",
            "--arguments-json",
            '{"value": 9}',
        ],
    )
    assert calculator.main() == 0
    called_capture = capsys.readouterr()
    called = json.loads(called_capture.out)
    assert called["ok"] is True
    assert called["result"] == {"value": 9}
    assert "diagnostic from synthetic module" in called_capture.err
    assert "diagnostic from synthetic call" in called_capture.err

    monkeypatch.setattr(
        sys,
        "argv",
        ["native_skill_calculate.py", "--describe", "demo.unknown"],
    )
    assert calculator.main() == 1
    failed = json.loads(capsys.readouterr().out)
    assert failed["ok"] is False
    assert "Unknown or inactive calculator" in failed["error"]
