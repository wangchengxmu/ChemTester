from __future__ import annotations

import json
from pathlib import Path
import shutil
import uuid

import pytest

from scripts.chemistry_expert.curated_support import (
    CuratedMemoryIndex,
    CuratedToolCatalog,
    load_support_policy,
)
from scripts.chemistry_expert.chemistry_tool_skill import ChemistryToolSkill
from scripts.design.generated_runtime_support import GenericProblem


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "configs" / "examples" / "self_evolving_chemistry_expert.json"


@pytest.fixture
def synthetic_tool_catalog():
    tmp_path = ROOT / f".pytest_curated_support_{uuid.uuid4().hex}"
    tmp_path.mkdir()
    module_path = tmp_path / "contract_tools.py"
    try:
        module_path.write_text(
            '''
EXECUTIONS = 0


def returns_none(value):
    \"\"\"Return no evidence.\"\"\"
    return None


def returns_nested_nan(value):
    \"\"\"Return a nested non-finite value.\"\"\"
    return {\"payload\": [{\"value\": float(\"nan\")}]}


def returns_zero_false(value):
    \"\"\"Return finite zero and false values.\"\"\"
    return {\"value\": 0, \"flag\": False}


def returns_number(value):
    \"\"\"Return a finite number.\"\"\"
    return 0


def returns_array(value):
    \"\"\"Return a finite array containing zero and false.\"\"\"
    return [0, False]


def bounded(left, right):
    \"\"\"Return the combined input size.\"\"\"
    global EXECUTIONS
    EXECUTIONS += 1
    return {\"count\": len(left) + len(right)}


def returns_missing_key(value):
    \"\"\"Return an object missing a required output key.\"\"\"
    return {\"value\": value}


def returns_error(value):
    \"\"\"Return a legacy error payload.\"\"\"
    return {\"error\": \"synthetic failure\"}


def returns_success_false(value):
    \"\"\"Return a legacy unsuccessful payload.\"\"\"
    return {\"success\": False}


def returns_ok_false(value):
    \"\"\"Return a legacy not-ok payload.\"\"\"
    return {\"ok\": False}


def raises_error(value):
    \"\"\"Raise an execution error.\"\"\"
    raise RuntimeError(\"synthetic execution failure\")
        '''.strip()
            + "\n",
            encoding="utf-8",
        )
        policy = {
            "tools": {
                "active_tiers": ["core"],
                "core_modules": ["contract_tools"],
                "quarantine_patterns": [],
                "contracts": {
                    "contract_tools.returns_none": {"result_type": "number"},
                    "contract_tools.returns_nested_nan": {"result_type": "object"},
                    "contract_tools.returns_zero_false": {
                        "result_type": "object",
                        "required_result_keys": ["value", "flag"],
                    },
                    "contract_tools.returns_number": {"result_type": "number"},
                    "contract_tools.returns_array": {"result_type": "array"},
                    "contract_tools.bounded": {
                        "max_items_combined": {
                            "parameters": ["left", "right"],
                            "maximum": 6,
                        },
                        "result_type": "object",
                        "required_result_keys": ["count"],
                    },
                    "contract_tools.returns_missing_key": {
                        "result_type": "object",
                        "required_result_keys": ["value", "detail"],
                    },
                    "contract_tools.returns_error": {"result_type": "object"},
                    "contract_tools.returns_success_false": {"result_type": "object"},
                    "contract_tools.returns_ok_false": {"result_type": "object"},
                    "contract_tools.raises_error": {"result_type": "object"},
                },
            }
        }
        yield CuratedToolCatalog(tmp_path, policy=policy).build()
    finally:
        shutil.rmtree(tmp_path, ignore_errors=True)


@pytest.fixture(scope="module")
def curated_support() -> tuple[dict, CuratedMemoryIndex, CuratedToolCatalog]:
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    policy = load_support_policy(repo_root=ROOT, config=config)
    memory = CuratedMemoryIndex(
        ROOT / config.get("memory_root", "chem-memory"),
        policy=policy,
    ).build()
    tools = CuratedToolCatalog(
        ROOT / config.get("tool_root", "chem-memory/L3_functions"),
        policy=policy,
    ).build()
    return policy, memory, tools


def test_policy_removes_automatic_support_injection(curated_support) -> None:
    policy, _, _ = curated_support
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))

    assert policy["model_decides_retrieval"] is True
    assert policy["promote_model_tool_result_to_direct_payload"] is False
    assert config["retrieval_top_k"] == 0
    assert config["tool_skill"]["initial_tool_count"] == 0


def test_tool_catalog_is_small_and_excludes_retired_benchmark_helpers(
    curated_support,
) -> None:
    _, _, tools = curated_support

    assert 0 < len(tools.tools) < 500
    assert tools.quarantined_tool_count == 0
    assert tools.retired_tool_count == 36
    assert tools.find(
        "inorganic_benchmark_support_tools",
        "analyze_inorganic_benchmark_mcq",
    ) is None


def test_curated_search_preserves_obvious_calculation_tools(curated_support) -> None:
    _, _, tools = curated_support

    gibbs_ids = [
        tool.id
        for tool in tools.search(
            "calculate Gibbs free energy from enthalpy entropy and temperature",
            top_k=4,
        )
    ]
    gas_ids = [
        tool.id
        for tool in tools.search(
            "ideal gas pressure from volume moles and temperature",
            top_k=4,
        )
    ]

    assert gibbs_ids[0] == "gibbs_free_energy_tools.gibbs_free_energy"
    assert "ideal_gas_law_tools.ideal_gas_law" in gas_ids


def test_curated_search_exposes_general_linear_regression(curated_support) -> None:
    _, _, tools = curated_support

    regression_ids = [
        tool.id
        for tool in tools.search(
            "ordinary least squares linear regression paired measurements "
            "intercept slope r squared",
            top_k=4,
        )
    ]

    assert regression_ids[0] == "chemometrics_tools.linear_regression"


def test_compatibility_support_is_retrievable_from_storage_table_wording(
    curated_support,
) -> None:
    _, memory, tools = curated_support
    query = (
        "chemical storage compatibility table combustible flammable miscellaneous "
        "materials alkali alkaline earth metals"
    )

    tool_ids = [tool.id for tool in tools.search(query, top_k=4)]
    knowledge_paths = [item.path for item in memory.search(query, top_k=4)]

    assert (
        "hazardous_waste_compatibility.lookup_chemical_storage_compatibility"
        in tool_ids
    )
    assert "L2_principles/epa_hazardous_waste_compatibility_lookup.md" in (
        knowledge_paths
    )

    epa_query = (
        "lookup EPA hazardous-waste compatibility for combustible and flammable "
        "miscellaneous materials paired with alkali and alkaline-earth metals"
    )
    assert (
        "hazardous_waste_compatibility.lookup_chemical_storage_compatibility"
        in [tool.id for tool in tools.search(epa_query, top_k=4)]
    )

    literal_id_query = (
        "hazardous_waste_compatibility.lookup_chemical_storage_compatibility "
        "combustible and flammable miscellaneous materials alkali and "
        "alkaline-earth metals published hazard codes"
    )
    assert (
        "hazardous_waste_compatibility.lookup_chemical_storage_compatibility"
        in [tool.id for tool in tools.search(literal_id_query, top_k=4)]
    )

    strong_identifier_query = (
        "hazardous_waste_compatibility lookup organic phosphates "
        "phosphothioates phosphodithioates with metals alkali metals "
        "alkaline-earth metals published hazard codes"
    )
    assert (
        "hazardous_waste_compatibility.lookup_chemical_storage_compatibility"
        in [tool.id for tool in tools.search(strong_identifier_query, top_k=4)]
    )


def test_knowledge_search_uses_canonical_notes_and_can_abstain(
    curated_support,
) -> None:
    _, memory, _ = curated_support

    synthesis = memory.search(
        "natural product total synthesis retrosynthesis protecting group strategy",
        top_k=2,
    )
    unsupported = memory.search(
        "inorganic oxide crystal structure coordination geometry",
        top_k=2,
    )

    # Complete sections replace clipped excerpts; ranking now favors substantive
    # planning evidence over the old source-context/cross-reference excerpt.
    assert [item.path for item in synthesis] == [
        "L2_principles/protecting_group_strategies.md",
        "L2_principles/retrosynthesis_advanced.md",
    ]
    assert all(len(item.snippet) <= 3200 for item in synthesis)
    assert "Deprotection sequence" in synthesis[0].snippet
    assert "Synthetic Route Evaluation Checklist" in synthesis[1].snippet
    assert all(item.snippet.count("```") % 2 == 0 for item in synthesis)
    assert unsupported == []


def test_v2_router_exact_loads_reference_without_duplicate_managed_topic(
    curated_support,
) -> None:
    _, memory, tools = curated_support
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    question = "Determine the Diels-Alder absolute stereochemistry of the bridged adduct."
    problem = GenericProblem(problem_id="diels-alder-routing", question=question)
    skill = ChemistryToolSkill(
        memory_index=memory,
        tool_catalog=tools,
        policy=config["tool_skill"],
    )
    decision = skill.route_question(question=question, problem=problem)
    paths = [
        item.path
        for item in skill.linked_documents_for_question(
            question=question,
            problem=problem,
        )
    ]

    assert decision["route"] == "skill"
    assert decision["selected_capability_ids"] == [
        "diels_alder_bridged_stereochemistry"
    ]
    assert (
        "L2_principles/chemtester_gap_skills/"
        "diels_alder_bridged_stereochemistry.md"
    ) not in paths
    assert paths == ["L2_principles/openstax_organic_ch30_pericyclic_reactions.md"]
    procedure = skill.compact_skill_for_question(question=question, problem=problem)
    assert "Procedure:" in procedure and "Guards:" in procedure
    assert "L2_principles/chemtester_compact_problem_solving_skill.md" not in paths


def test_peroxide_former_visual_hazard_note_matches_gap_queries(
    curated_support,
) -> None:
    _, memory, _ = curated_support
    expected = "L2_principles/peroxide_former_visual_hazard_response.md"
    queries = [
        (
            "ether peroxide crystals around container cap immediate handling "
            "expert hazardous waste disposal"
        ),
        (
            "peroxide-forming ether visible crystals cap do not move open or "
            "handle contact hazardous materials disposal"
        ),
    ]

    for query in queries:
        paths = [item.path for item in memory.search(query, top_k=4)]
        assert expected in paths


def test_tool_result_validation_rejects_none_and_nested_non_finite_values(
    synthetic_tool_catalog,
) -> None:
    tools = synthetic_tool_catalog

    none_result = tools.execute(
        tools.find("contract_tools", "returns_none"),
        {"value": 1},
    )
    assert none_result.error is not None
    assert "None" in none_result.error
    assert "evidence-invalid" in none_result.error
    assert none_result.metadata["classification"] == "evidence_invalid"
    assert none_result.metadata["evidence_valid"] is False
    assert none_result.metadata["usable"] is False
    assert none_result.metadata["execution_succeeded"] is True
    assert none_result.metadata["result_contract_valid"] is False

    nan_result = tools.execute(
        tools.find("contract_tools", "returns_nested_nan"),
        {"value": 1},
    )
    assert nan_result.error is not None
    assert "non-finite" in nan_result.error
    assert "result.payload" in nan_result.error
    assert nan_result.metadata["classification"] == "evidence_invalid"
    assert nan_result.metadata["usable"] is False
    assert nan_result.metadata["execution_succeeded"] is True
    assert nan_result.metadata["result_contract_valid"] is False


def test_tool_result_validation_preserves_zero_false_and_dict_failure_handling(
    synthetic_tool_catalog,
) -> None:
    tools = synthetic_tool_catalog

    finite_result = tools.execute(
        tools.find("contract_tools", "returns_zero_false"),
        {"value": 0},
    )
    assert finite_result.error is None
    assert finite_result.result == {"value": 0, "flag": False}
    assert finite_result.metadata["classification"] == "usable"
    assert finite_result.metadata["evidence_valid"] is None
    assert finite_result.metadata["usable"] is True
    assert finite_result.metadata["scientific_validity"] == (
        "not_independently_verified"
    )
    assert finite_result.metadata["execution_succeeded"] is True
    assert finite_result.metadata["result_contract_valid"] is True

    number_result = tools.execute(
        tools.find("contract_tools", "returns_number"),
        {"value": False},
    )
    assert number_result.error is None
    assert number_result.result == 0
    assert number_result.metadata["evidence_valid"] is None
    assert number_result.metadata["usable"] is True

    array_result = tools.execute(
        tools.find("contract_tools", "returns_array"),
        {"value": 0},
    )
    assert array_result.error is None
    assert array_result.result == [0, False]
    assert array_result.metadata["evidence_valid"] is None
    assert array_result.metadata["usable"] is True

    for function_name in (
        "returns_error",
        "returns_success_false",
        "returns_ok_false",
    ):
        result = tools.execute(
            tools.find("contract_tools", function_name),
            {"value": 1},
        )
        assert result.error is not None
        assert result.metadata["classification"] == "evidence_invalid"
        assert result.metadata["evidence_valid"] is False
        assert result.metadata["usable"] is False
        assert result.metadata["execution_succeeded"] is True
        assert result.metadata["result_contract_valid"] is False


def test_tool_metadata_distinguishes_execution_and_input_failures(
    synthetic_tool_catalog,
) -> None:
    tools = synthetic_tool_catalog

    execution_error = tools.execute(
        tools.find("contract_tools", "raises_error"),
        {"value": 1},
    )
    assert execution_error.error == "synthetic execution failure"
    assert execution_error.metadata["classification"] == "tool_error"
    assert execution_error.metadata["evidence_valid"] is False
    assert execution_error.metadata["usable"] is False
    assert execution_error.metadata["execution_succeeded"] is False
    assert execution_error.metadata["result_contract_valid"] is None

    missing_input = tools.execute(
        tools.find("contract_tools", "bounded"),
        {"left": []},
    )
    assert missing_input.error is not None
    assert missing_input.metadata["classification"] == "invalid_input"
    assert missing_input.metadata["evidence_valid"] is False
    assert missing_input.metadata["usable"] is False
    assert missing_input.metadata["execution_succeeded"] is False
    assert missing_input.metadata["result_contract_valid"] is None


def test_tool_contract_limits_inputs_before_execution_and_exposes_metadata(
    synthetic_tool_catalog,
) -> None:
    tools = synthetic_tool_catalog
    tool = tools.find("contract_tools", "bounded")
    metadata = tools.metadata_for(tool)

    assert metadata["contract"] == {
        "max_items_combined": {
            "parameters": ["left", "right"],
            "maximum": 6,
        },
        "result_type": "object",
        "required_result_keys": ["count"],
    }

    supported = tools.execute(
        tool,
        {"left": [0, False, 2], "right": [3, 4, 5]},
    )
    assert supported.error is None
    assert supported.result == {"count": 6}

    module = tools.base_catalog._module_cache["generated_tool_contract_tools"]
    assert module.EXECUTIONS == 1

    unsupported = tools.execute(
        tool,
        {"left": [0, False, 2, 3], "right": [4, 5, 6]},
    )
    assert unsupported.error is not None
    assert "max_items_combined" in unsupported.error
    assert "maximum 6" in unsupported.error
    assert unsupported.metadata["classification"] == "invalid_input"
    assert unsupported.metadata["usable"] is False
    assert module.EXECUTIONS == 1

    non_finite_input = tools.execute(
        tool,
        {"left": [{"nested": float("inf")}], "right": []},
    )
    assert non_finite_input.error is not None
    assert "non-finite" in non_finite_input.error
    assert module.EXECUTIONS == 1


def test_tool_contract_validates_required_output_keys(
    synthetic_tool_catalog,
) -> None:
    tools = synthetic_tool_catalog
    result = tools.execute(
        tools.find("contract_tools", "returns_missing_key"),
        {"value": 0},
    )

    assert result.error is not None
    assert "missing required output key(s)" in result.error
    assert "detail" in result.error
    assert result.metadata["classification"] == "evidence_invalid"
    assert result.metadata["evidence_valid"] is False
    assert result.metadata["execution_succeeded"] is True
    assert result.metadata["result_contract_valid"] is False
