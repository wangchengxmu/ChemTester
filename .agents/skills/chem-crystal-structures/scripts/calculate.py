"""Standalone, explicit calculator invocation; no model, retrieval, or routing."""

from __future__ import annotations

import argparse
import contextlib
import importlib.util
import inspect
import json
import math
from pathlib import Path
import re
import sys
from typing import Any, get_origin


def finite_json(value: Any) -> Any:
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError("Non-finite numbers are not supported")
    if value is None or isinstance(value, (str, bool, int, float)):
        return value
    if isinstance(value, dict):
        return {str(key): finite_json(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [finite_json(item) for item in value]
    if hasattr(value, "tolist"):
        return finite_json(value.tolist())
    if hasattr(value, "item"):
        return finite_json(value.item())
    raise ValueError(f"Unsupported result type: {type(value).__name__}")


def input_contract(arguments: dict[str, Any], contract: dict[str, Any]) -> None:
    finite_json(arguments)
    for name, allowed in contract.get("allowed_values", {}).items():
        if name in arguments and arguments[name] not in allowed:
            raise ValueError(f"{name} must be one of {allowed}")
    for name in contract.get("positive_parameters", []):
        if name in arguments and (isinstance(arguments[name], bool) or not isinstance(arguments[name], (int, float)) or arguments[name] <= 0):
            raise ValueError(f"{name} must be a positive number")
    limit = contract.get("max_items_combined")
    if limit:
        values = [arguments.get(name, []) for name in limit["parameters"]]
        if any(not isinstance(value, list) for value in values):
            raise ValueError("Bounded formula collections must be JSON arrays")
        if sum(len(value) for value in values) > limit["maximum"]:
            raise ValueError(f"Combined input count exceeds {limit['maximum']}")


def output_contract(result: Any, contract: dict[str, Any]) -> Any:
    result = finite_json(result)
    if result is None:
        raise ValueError("Calculator returned no result")
    if isinstance(result, dict):
        if result.get("error") or result.get("success") is False or result.get("ok") is False:
            raise ValueError(f"Calculator reported failure: {result}")
    if contract.get("result_type") == "object" and not isinstance(result, dict):
        raise ValueError("Calculator must return an object")
    required = contract.get("required_result_keys", [])
    if required and (not isinstance(result, dict) or any(key not in result for key in required)):
        raise ValueError(f"Calculator result is missing required keys: {required}")
    return result


def execute(base: Path, catalog: dict[str, Any], tool_id: str, arguments: Any) -> dict[str, Any]:
    if tool_id not in catalog["tools"] or not re.fullmatch(r"[a-zA-Z_]\w*\.[a-zA-Z_]\w*", tool_id):
        raise ValueError("Unknown or inactive calculator")
    if not isinstance(arguments, dict):
        raise ValueError("Arguments must be a JSON object")
    record = catalog["tools"][tool_id]
    contract = record.get("contract", {})
    input_contract(arguments, contract)
    module_name, function_name = tool_id.split(".")
    module_dir = (base / "tools").resolve()
    module_path = (module_dir / f"{module_name}.py").resolve()
    if module_path.parent != module_dir:
        raise ValueError("Calculator path escapes the bundled tools directory")
    spec = importlib.util.spec_from_file_location(f"native_chem_{module_name}", module_path)
    if spec is None or spec.loader is None:
        raise ValueError("Cannot load calculator")
    module = importlib.util.module_from_spec(spec)
    old_path = list(sys.path)
    try:
        sys.path.insert(0, str(module_dir))
        # Third-party and legacy diagnostic prints must not corrupt the JSON response.
        with contextlib.redirect_stdout(sys.stderr):
            spec.loader.exec_module(module)
            function = getattr(module, function_name)
            inspect.signature(function).bind(**arguments)
            converted = dict(arguments)
            for name, annotation in inspect.get_annotations(function, eval_str=True).items():
                array_type = get_origin(annotation) or annotation
                if name in converted and getattr(array_type, "__module__", "") == "numpy" and getattr(array_type, "__name__", "") == "ndarray":
                    import numpy as np

                    converted[name] = np.asarray(converted[name])
            result = function(**converted)
    finally:
        sys.path[:] = old_path
    return {
        "ok": True,
        "tool_id": tool_id,
        "result": output_contract(result, contract),
        "scientific_validity": "not_independently_verified",
        "note": "Execution and contract checks do not establish empirical or scientific correctness.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--list", action="store_true")
    action.add_argument("--describe", metavar="MODULE.FUNCTION")
    action.add_argument("--call", metavar="MODULE.FUNCTION")
    parser.add_argument("--arguments-json", default="{}")
    args = parser.parse_args()
    try:
        base = Path(__file__).resolve().parent
        catalog = json.loads((base / "catalog.json").read_text(encoding="utf-8"))
        if args.list:
            result = {key: record["summary"] for key, record in catalog["tools"].items()}
        elif args.describe:
            if args.describe not in catalog["tools"]:
                raise ValueError("Unknown or inactive calculator")
            result = catalog["tools"][args.describe]
        else:
            result = execute(base, catalog, args.call, json.loads(args.arguments_json))
        print(json.dumps(result, ensure_ascii=True, allow_nan=False))
        return 0
    except Exception as exc:
        print(json.dumps({"ok": False, "error": f"{type(exc).__name__}: {exc}"}, ensure_ascii=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
