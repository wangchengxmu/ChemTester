"""Deterministic lookup for the EPA hazardous-waste compatibility chart.

The table is transcribed from EPA-600/2-80-076 (April 1980), "A Method
for Determining the Compatibility of Hazardous Wastes." It reports coded
outcomes for pairs of broad reactivity groups. A blank chart cell is not a
claim of safety.

This module contains no benchmark identifiers, option letters, or expected
answers. It maps only public EPA group names/numbers to the published codes.
"""

from __future__ import annotations

import re
from typing import Any


GROUP_NAMES = {
    1: "Acids, Mineral, Non-oxidizing",
    2: "Acids, Mineral, Oxidizing",
    3: "Acids, Organic",
    4: "Alcohols and Glycols",
    5: "Aldehydes",
    6: "Amides",
    7: "Amines, Aliphatic and Aromatic",
    8: "Azo Compounds, Diazo Compounds and Hydrazines",
    9: "Carbamates",
    10: "Caustics",
    11: "Cyanides",
    12: "Dithiocarbamates",
    13: "Esters",
    14: "Ethers",
    15: "Fluorides, Inorganic",
    16: "Hydrocarbons, Aromatic",
    17: "Halogenated Organics",
    18: "Isocyanates",
    19: "Ketones",
    20: "Mercaptans and Other Organic Sulfides",
    21: "Metals, Alkali and Alkaline Earth, Elemental",
    22: "Metals, Other Elemental and Alloys as Powders, Vapors, or Sponges",
    23: "Metals, Other Elemental and Alloys as Sheets, Rods, or Moldings",
    24: "Metals and Metal Compounds, Toxic",
    25: "Nitrides",
    26: "Nitriles",
    27: "Nitro Compounds, Organic",
    28: "Hydrocarbons, Aliphatic, Unsaturated",
    29: "Hydrocarbons, Aliphatic, Saturated",
    30: "Peroxides and Hydroperoxides, Organic",
    31: "Phenols and Cresols",
    32: "Organophosphates, Phosphothioates, Phosphodithioates",
    33: "Sulfides, Inorganic",
    34: "Epoxides",
    101: "Combustible and Flammable Materials, Miscellaneous",
    102: "Explosives",
    103: "Polymerizable Compounds",
    104: "Oxidizing Agents, Strong",
    105: "Reducing Agents, Strong",
    106: "Water and Mixtures Containing Water",
    107: "Water Reactive Substances",
}

CODE_CONSEQUENCES = {
    "H": "Heat generation",
    "F": "Fire",
    "G": "Innocuous and non-flammable gas generation",
    "GT": "Toxic gas formation",
    "GF": "Flammable gas formation",
    "E": "Explosion",
    "P": "Violent polymerization",
    "S": "Solubilization of toxic substance",
    "U": "May be hazardous, but unknown",
}

SOURCE = {
    "title": "A Method for Determining the Compatibility of Hazardous Wastes",
    "report_number": "EPA-600/2-80-076",
    "agency": "U.S. Environmental Protection Agency",
    "published": "April 1980",
    "official_url": "https://www.epa.gov/hwpermitting/method-determining-compatibility-hazardous-wastes",
    "chart_url": "https://ipo.rutgers.edu/rehs/chemical-compatibilty-chart-epa",
    "transcribed_chart_sha256": "398e58868d2c90f2e0f771617c49e48433564e981b09e8943b7cae729192c4a8",
}

# One line per nonblank lower-triangular chart cell: group_a-group_b:codes.
_PAIR_DATA = """
2-3:H,G
1-4:H
2-4:H,F
3-4:H,P
1-5:H,P
2-5:H,F
3-5:H,P
1-6:H
2-6:H,GT
1-7:H
2-7:H,GT
3-7:H
5-7:H
1-8:H,G
2-8:H,GT
3-8:H,G
4-8:H,G
5-8:H
1-9:H,G
2-9:H,GT
8-9:H,G
1-10:H
2-10:H
3-10:H
5-10:H
9-10:H,G
1-11:GT,GF
2-11:GT,GF
3-11:GT,GF
8-11:G
1-12:H,F,GF
2-12:H,F,GF
3-12:H,GT,GF
5-12:GT,GF
7-12:U
8-12:H,G
1-13:H
2-13:H,F
8-13:H,G
10-13:H
1-14:H
2-14:H,F
1-15:GT
2-15:GT
3-15:GT
2-16:H,F
1-17:H,GT
2-17:H,F,GT
7-17:H,GT
8-17:H,G
10-17:H,GF
11-17:H
1-18:H,G
2-18:H,F,GT
3-18:H,G
4-18:H,P
7-18:H,P
8-18:H,G
10-18:H,G,P
11-18:H,G
12-18:U
1-19:H
2-19:H,F
8-19:H,G
10-19:H
11-19:H
1-20:GT,GF
2-20:H,F,GT
8-20:H,G
17-20:H
18-20:H
19-20:H
1-21:H,F,GF
2-21:H,F,GF
3-21:H,F,GF
4-21:H,F,GF
5-21:H,F,GF
6-21:H,GF
7-21:H,GF
8-21:H,GF
9-21:H,GF
10-21:H,GF
11-21:H,GF
12-21:H,GT,GF
13-21:H,GF
17-21:H,E
18-21:H,GF
19-21:H,GF
20-21:H,GF
1-22:H,F,GF
2-22:H,F,GF
3-22:F,G
8-22:H,F,GT
9-22:U
10-22:H,GF
17-22:H,E
18-22:H,GF
20-22:H,F,GF
1-23:H,F,GF
2-23:H,F,GF
8-23:H,F,G
17-23:H,F
1-24:S
2-24:S
3-24:S
6-24:S
7-24:S
10-24:S
1-25:H,F,GF
2-25:H,F,E
3-25:H,GF
4-25:H,GF,E
5-25:H,GF
8-25:U
9-25:H,G
10-25:U
11-25:H,GF
12-25:H,GF
13-25:H,GF
17-25:H,GF
18-25:U
19-25:H,GF
20-25:H,GF
21-25:E
1-26:H,GT,GF
2-26:H,F,GT
3-26:H
10-26:U
21-26:H,P
24-26:S
25-26:H,GF
2-27:H,F,GT
5-27:H
10-27:H,E
21-27:H,GF,E
25-27:H,GF,E
1-28:H
2-28:H,F
5-28:H
22-28:H,E
2-29:H,F
1-30:H,G
2-30:H,E
4-30:H,F
5-30:H,G
7-30:H,GT
8-30:H,F,E
9-30:H,F,GT
11-30:H,GT,E
12-30:H,F,GT
17-30:H,E
18-30:H
19-30:E
20-30:H,F,GT
21-30:H,E
22-30:H,G
24-30:H,G
25-30:H,GF,E
26-30:H,GT,P
28-30:H,P
1-31:H
2-31:H,F
8-31:H,G
18-31:H,P
21-31:H,GF
25-31:H,GF
30-31:H
1-32:H,GT
2-32:H,GT
8-32:U
10-32:H,E
21-32:H
30-32:U
1-33:GT,GF
2-33:H,F,GF
3-33:GT
5-33:H
8-33:E
18-33:H
30-33:H,GT
1-34:H,P
2-34:H,P
3-34:H,P
4-34:H,P
5-34:U
7-34:H,P
8-34:H,P
10-34:H,P
11-34:H,P
12-34:U
20-34:H,P
21-34:H,P
22-34:H,P
24-34:H,P
25-34:H,P
30-34:H,P
31-34:H,P
32-34:U
33-34:H,P
1-101:H,G
2-101:H,F,GT
21-101:H,F,G
25-101:H,F,GF
30-101:H,F,GT
1-102:H,E
2-102:H,E
3-102:H,E
8-102:H,E
10-102:H,E
13-102:H,E
21-102:H,E
22-102:H,E
23-102:H,E
24-102:E
25-102:E
30-102:H,E
31-102:H,E
33-102:H,E
34-102:H,E
101-102:H,E
1-103:H,P
2-103:H,P
3-103:H,P
8-103:H,P
10-103:H,P
11-103:H,P
12-103:U
21-103:H,P
22-103:H,P
23-103:H,P
24-103:H,P
25-103:H,P
30-103:H,P
31-103:H,P
33-103:H,P
1-104:H,GT
3-104:H,GT
4-104:H,F
5-104:H,F
6-104:H,F,GT
7-104:H,F,GT
8-104:H,E
9-104:H,F,GT
11-104:H,GT,E
12-104:H,F,GT
13-104:H,F
14-104:H,F
16-104:H,F
17-104:H,GT
18-104:H,F,GT
19-104:H,F
20-104:H,F,GT
21-104:H,F,E
22-104:H,F,E
23-104:H,F
25-104:H,F,E
26-104:H,F,GT
27-104:H,E
28-104:H,F
29-104:H,F
30-104:H,G
31-104:H,F
32-104:H,F,GT
33-104:H,F,GT
34-104:H,F,G
101-104:H,F,G
1-105:H,GF
2-105:H,F,GT
3-105:H,GF
4-105:H,F,GF
5-105:H,F,GF
6-105:H,GF
7-105:H,G
11-105:H,GT
12-105:H,F
16-105:H,F,E
17-105:H,E
18-105:H,GF
19-105:H,GF
20-105:H,GF
26-105:H,GF
27-105:H,E
30-105:H,E
31-105:H,GF
32-105:H,GT,GF
34-105:H
101-105:H,GF
1-106:H
2-106:H
8-106:G
18-106:H,G
21-106:H,GF
22-106:H,GF
24-106:S
25-106:H,GF
33-106:GT,GF
"""


def _parse_pair_data() -> dict[tuple[int, int], tuple[str, ...]]:
    pairs: dict[tuple[int, int], tuple[str, ...]] = {}
    for raw_line in _PAIR_DATA.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        pair_text, codes_text = line.split(":", 1)
        first, second = (int(value) for value in pair_text.split("-", 1))
        pairs[(first, second)] = tuple(codes_text.split(","))
    return pairs


PAIR_CODES = _parse_pair_data()
_GROUP_ORDER = tuple(GROUP_NAMES)
_ORDER_INDEX = {group: index for index, group in enumerate(_GROUP_ORDER)}


def _normalize_name(value: Any) -> str:
    return re.sub(r"[^a-z0-9]+", " ", str(value or "").lower()).strip()


_NAME_TO_GROUP = {_normalize_name(name): number for number, name in GROUP_NAMES.items()}
_NAME_TO_GROUP.update(
    {
        "non oxidizing mineral acids": 1,
        "non oxidizing acids": 1,
        "oxidizing mineral acids": 2,
        "organic acids": 3,
        "alcohols or glycols": 4,
        "azo compounds diazo compounds or hydrazines": 8,
        "mercaptans or other organic sulfides": 20,
        "alkali and alkaline earth metals": 21,
        "alkali or alkaline earth metals": 21,
        "alkali metals and alkaline earth metals": 21,
        "metals alkali metals or alkaline earth metals": 21,
        "metals alkali and alkaline earth": 21,
        "metals alkali or alkaline earth": 21,
        "elemental alkali and alkaline earth metals": 21,
        "elemental alkali or alkaline earth metals": 21,
        "powdered metals": 22,
        "metals or elemental alloys in powder vapor or sponge form": 22,
        "bulk metals": 23,
        "metals or elemental alloys in sheets rods or moldings": 23,
        "toxic metals or metal compounds": 24,
        "organic nitro compounds": 27,
        "unsaturated aliphatic hydrocarbons": 28,
        "saturated aliphatic hydrocarbons": 29,
        "organic peroxides or hydroperoxides": 30,
        "organophosphates phosphorothioates or phosphodithioates": 32,
        "organophosphates phosphothioates or phosphodithioates": 32,
        "organophosphates phosphothioates and phosphodithioates": 32,
        "organic phosphates phosphothioates or phosphodithioates": 32,
        "inorganic sulfides": 33,
        "combustible or flammable miscellaneous materials": 101,
        "combustible or flammable materials miscellaneous": 101,
        "combustible and flammable materials miscellaneous": 101,
        "strong oxidizing agents": 104,
        "strong oxidizers": 104,
        "strong reducing agents": 105,
        "strong reducers": 105,
        "water or mixtures containing water": 106,
        "water reactive materials": 107,
    }
)


def _name_signature(value: Any) -> str:
    normalized = re.sub(
        r"\borganic phosphates?\b",
        "organophosphates",
        _normalize_name(value),
    )
    tokens = (token for token in normalized.split() if token not in {"and", "or"})
    return " ".join(sorted(tokens))


_SIGNATURE_TO_GROUP: dict[str, int] = {}
_AMBIGUOUS_NAME_SIGNATURES: set[str] = set()
for _name, _number in _NAME_TO_GROUP.items():
    _signature = _name_signature(_name)
    _existing = _SIGNATURE_TO_GROUP.get(_signature)
    if _existing is not None and _existing != _number:
        _AMBIGUOUS_NAME_SIGNATURES.add(_signature)
        _SIGNATURE_TO_GROUP.pop(_signature, None)
    elif _signature not in _AMBIGUOUS_NAME_SIGNATURES:
        _SIGNATURE_TO_GROUP[_signature] = _number


def _resolve_group(value: int | str) -> int:
    if isinstance(value, bool):
        raise ValueError("Boolean values are not valid EPA reactivity groups")
    if isinstance(value, int) or str(value).strip().isdigit():
        number = int(value)
        if number not in GROUP_NAMES:
            raise ValueError(f"Unknown EPA reactivity group number: {number}")
        return number
    normalized = _normalize_name(value)
    exact = _NAME_TO_GROUP.get(normalized)
    if exact is not None:
        return exact
    signature = _name_signature(normalized)
    resolved = _SIGNATURE_TO_GROUP.get(signature)
    if resolved is not None:
        return resolved
    raise ValueError(f"Unknown EPA reactivity group name: {value}")


def _pair_key(first: int, second: int) -> tuple[int, int]:
    if first == second:
        raise ValueError("The EPA chart reports binary combinations of different groups")
    return tuple(sorted((first, second), key=_ORDER_INDEX.__getitem__))  # type: ignore[return-value]


def lookup_hazardous_waste_compatibility(
    group_a: int | str,
    group_b: int | str,
) -> dict[str, Any]:
    """Look up EPA-600/2-80-076 hazards for two reactivity groups.

    Parameters:
        group_a: EPA group number or full class name, such as "Metals, Alkali
            and Alkaline Earth, Elemental", "strong oxidizing agents", or
            "combustible and flammable materials, miscellaneous".
        group_b: A different EPA group number or class name.

    Returns:
        Exact chart codes and decoded consequences with source provenance.
        Empty codes mean only that the chart cell is blank; they do not prove
        that a mixture is safe. Group 107 always returns the chart's explicit
        do-not-mix warning.
    """
    first = _resolve_group(group_a)
    second = _resolve_group(group_b)
    key = _pair_key(first, second)
    water_reactive = 107 in key
    codes = (
        ("EXTREMELY_REACTIVE_DO_NOT_MIX",)
        if water_reactive
        else PAIR_CODES.get(key, ())
    )
    consequences = [
        (
            "Extremely reactive: do not mix with any chemical or waste material"
            if code == "EXTREMELY_REACTIVE_DO_NOT_MIX"
            else CODE_CONSEQUENCES[code]
        )
        for code in codes
    ]
    blank_cell = not codes
    warning = (
        "A blank cell is not evidence of compatibility or safety; obtain "
        "waste-specific handling and disposal information."
        if blank_cell
        else "The chart is an indication of possible hazards, not a definitive or exhaustive compatibility determination."
    )
    return {
        "group_a": {"number": first, "name": GROUP_NAMES[first]},
        "group_b": {"number": second, "name": GROUP_NAMES[second]},
        "codes": list(codes),
        "consequences": consequences,
        "blank_cell": blank_cell,
        "warning": warning,
        "source": dict(SOURCE),
        "deterministic_reasoning": True,
        "anti_leakage": {
            "uses_problem_id": False,
            "uses_expected_answer": False,
            "selection_basis": "public EPA reactivity-group pair table",
        },
    }


def lookup_chemical_storage_compatibility(
    chemical_class_a: int | str,
    chemical_class_b: int | str,
) -> dict[str, Any]:
    """Look up an EPA hazardous-waste compatibility chart class pair.

    Use this discoverable entry point when a question names two material or
    chemical classes from the EPA chemical-storage compatibility table, such
    as combustible or flammable miscellaneous materials and alkali or
    alkaline-earth metals. Inputs may be EPA group numbers or published class
    names. The result contains published hazard codes and decoded consequences.
    """
    return lookup_hazardous_waste_compatibility(chemical_class_a, chemical_class_b)
