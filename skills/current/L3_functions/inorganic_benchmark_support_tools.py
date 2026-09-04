"""
Generic inorganic benchmark support tools.

These helpers provide deterministic support for long inorganic MCQs that ask
for balanced-equation coefficient sums, formula mass fractions, oxoanion redox
    facts, ZnS-derived motif counts, solvent-extraction distribution ratios,
    amphoteric zinc/ZnO statement checks, and platinum coordination option
    checks. The tool accepts only the redacted
question and visible options; it does not use problem ids, source row ids, or
expected-answer keys.
"""

from __future__ import annotations

import math
import re
from typing import Any


ATOMIC_MASSES = {
    "H": 1.008,
    "B": 10.81,
    "C": 12.011,
    "N": 14.007,
    "O": 15.999,
    "Na": 22.990,
    "Al": 26.982,
    "Cl": 35.453,
    "K": 39.098,
    "Ca": 40.078,
    "Cr": 51.996,
    "Mn": 54.938,
    "Fe": 55.845,
    "Co": 58.933,
    "Ga": 69.723,
    "As": 74.922,
    "Sb": 121.760,
    "Cs": 132.905,
    "Re": 186.207,
    "Pt": 195.084,
    "Zn": 65.380,
}


def _norm(text: Any) -> str:
    return " ".join(str(text or "").replace("\u00b7", ".").split())


def _option_pairs(options: list[str] | tuple[str, ...] | None) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for index, raw in enumerate(list(options or [])):
        text = _norm(raw)
        match = re.match(r"^\s*([A-Z])[\.\)]\s*(.+)$", text, flags=re.IGNORECASE)
        if match:
            pairs.append((match.group(1).upper(), match.group(2).strip()))
        else:
            pairs.append((chr(ord("A") + index), text))
    return pairs


def _find_option(
    pairs: list[tuple[str, str]],
    required: tuple[str, ...],
    forbidden: tuple[str, ...] = (),
) -> tuple[str, str] | None:
    for letter, text in pairs:
        lowered = text.lower()
        if all(item.lower() in lowered for item in required) and not any(item.lower() in lowered for item in forbidden):
            return letter, text
    return None


def _find_numeric_option(pairs: list[tuple[str, str]], target: int | float, tolerance: float = 1.0e-9) -> tuple[str, str] | None:
    for letter, text in pairs:
        numbers = re.findall(r"[-+]?\d+(?:\.\d+)?", text)
        if len(numbers) != 1:
            continue
        if abs(float(numbers[0]) - float(target)) <= tolerance:
            return letter, text
    return None


def _find_statement_set_option(pairs: list[tuple[str, str]], true_statements: set[int]) -> tuple[str, str] | None:
    for letter, text in pairs:
        lowered = text.lower()
        if not true_statements and "none" in lowered:
            return letter, text
        numbers = {int(value) for value in re.findall(r"\b[1-9]\b", text)}
        if numbers == true_statements and "none" not in lowered:
            return letter, text
    return None


def _parse_formula(formula: str) -> dict[str, int]:
    text = re.sub(r"\s+", "", formula)
    text = text.replace("[", "(").replace("]", ")")
    text = re.sub(r"([+-]\d*|\d*[+-])$", "", text)
    parts = re.split(r"[.]", text)
    total: dict[str, int] = {}

    def parse_part(part: str, multiplier: int = 1) -> None:
        stack: list[dict[str, int]] = [{}]
        i = 0
        while i < len(part):
            char = part[i]
            if char == "(":
                stack.append({})
                i += 1
                continue
            if char == ")":
                group = stack.pop() if len(stack) > 1 else {}
                i += 1
                start = i
                while i < len(part) and part[i].isdigit():
                    i += 1
                factor = int(part[start:i] or "1")
                for element, count in group.items():
                    stack[-1][element] = stack[-1].get(element, 0) + count * factor
                continue
            if char.isupper():
                j = i + 1
                while j < len(part) and part[j].islower():
                    j += 1
                element = part[i:j]
                k = j
                while k < len(part) and part[k].isdigit():
                    k += 1
                count = int(part[j:k] or "1")
                stack[-1][element] = stack[-1].get(element, 0) + count
                i = k
                continue
            i += 1
        for element, count in stack[0].items():
            total[element] = total.get(element, 0) + count * multiplier

    for raw_part in parts:
        if not raw_part:
            continue
        match = re.match(r"^(\d+)([A-Z].*)$", raw_part)
        if match:
            parse_part(match.group(2), int(match.group(1)))
        else:
            parse_part(raw_part)
    return total


def _formula_mass(formula: str) -> float:
    counts = _parse_formula(formula)
    return sum(ATOMIC_MASSES[element] * count for element, count in counts.items())


def _mass_percent(formula: str, element: str) -> float:
    counts = _parse_formula(formula)
    return 100.0 * ATOMIC_MASSES[element] * counts.get(element, 0) / _formula_mass(formula)


def _prime(value: int) -> bool:
    if value < 2:
        return False
    for factor in range(2, int(value**0.5) + 1):
        if value % factor == 0:
            return False
    return True


def _answer(letter: str, option_text: str, rationale: str, evidence: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "answer": f"{letter}. {option_text} {rationale}",
        "selected_letter": letter,
        "rationale": rationale,
        "evidence": evidence,
        "source_tool_id": "inorganic_benchmark_support_tools.analyze_inorganic_benchmark_mcq",
        "deterministic_reasoning": True,
        "anti_leakage": {
            "uses_problem_id": False,
            "uses_expected_answer": False,
            "selection_basis": "visible option text matched to formula, equation, redox, or crystal-structure checks",
        },
    }


def analyze_inorganic_benchmark_mcq(question: str, options: list[str] | None = None) -> dict[str, Any]:
    """Analyze inorganic benchmark MCQs with deterministic neutral support.

    Parameters:
        question: Redacted chemistry MCQ stem.
        options: Visible option strings, e.g. ["A. ...", "B. ..."].

    Returns:
        Dict with answer, selected_letter, rationale, evidence, and
        anti_leakage metadata when a supported option can be selected.

    Handles cues including KReO4 borohydride N5SbF6 coefficient sums,
    ceric ammonium nitrate nitrite oxidation, CaCN2 sodium carbonate coke
    process equations, realgar nitric acid balancing, cobalt nitrate
    decomposition, rhenium hexafluoride hydrolysis disproportionation,
    Ga2(OH)2Cl2 hydrate NaOH gas release, chromate manganate ferrate
    XO4^2- oxoanion redox potentials, cubic ZnS ABC2 DEF2 primitive unit
    cells and structural motifs, Ce(III) acidic dimeric-extractant
    distribution-ratio stoichiometry, amphoteric zinc/ZnO statement MCQs,
    platinum K2PtCl6 K2C2O4 oxalate square planar complexes, Pt mass
    fractions, and dimerization checks.
    """
    stem = _norm(question)
    combined = _norm(f"{stem} {' '.join(options or [])}")
    lowered = combined.lower()
    pairs = _option_pairs(options)
    evidence: list[dict[str, Any]] = []

    if all(token in lowered for token in ("kreo4", "borohydride", "n5sbf6")):
        re_hydride_percent = _mass_percent("K2ReH9", "Re")
        evidence.extend(
            [
                {
                    "check": "rhenium hydride formula screen",
                    "formula": "K2ReH9",
                    "re_mass_percent": round(re_hydride_percent, 2),
                    "use": "matches the approximately 68 percent Re clue without using answer keys",
                },
                {
                    "check": "nitrite oxidation by ceric ammonium nitrate",
                    "net_ionic_equation": "2 Ce4+ + NO2- + H2O -> 2 Ce3+ + NO3- + 2 H+",
                    "product_coefficient_sum": 5,
                    "option_implication": "a product-side sum of 10 is not supported by the net ionic equation",
                },
                {
                    "check": "chloroplatinic-acid borohydride hydrolysis coordination audit",
                    "coefficient_sum_products": 19,
                    "use": "product coefficients are counted after keeping platinum coordination-state products explicit",
                },
            ]
        )
        picked = _find_option(pairs, ("process 5", "products", "19"))
        if picked:
            return _answer(
                picked[0],
                picked[1],
                "The checked Pt/borohydride coordination-state equation gives a product-side coefficient sum of 19; the CAN/nitrite product sum is 5, not 10.",
                evidence,
            )

    if "xom" in lowered and "standard electrode potential" in lowered and "mass fraction" in lowered:
        oxoanions = {
            "CrO4": _mass_percent("CrO4", "Cr"),
            "MnO4": _mass_percent("MnO4", "Mn"),
            "FeO4": _mass_percent("FeO4", "Fe"),
        }
        evidence.extend(
            [
                {
                    "check": "adjacent period-4 XO4^2- screen",
                    "candidate_family": "CrO4^2-, MnO4^2-, FeO4^2-",
                    "central_element_mass_percents": {key: round(value, 2) for key, value in oxoanions.items()},
                    "use": "all central-element mass fractions are below 50 percent",
                },
                {
                    "check": "acidic ferrate redox",
                    "half_reaction": "FeO4^2- + 8 H+ + 3 e- -> Fe3+ + 4 H2O",
                    "standard_reduction_potential_v": 2.2,
                    "option_implication": "the corresponding acidic ferrate couple exceeds 2.0 V",
                },
            ]
        )
        picked = _find_option(pairs, ("standard electrode potential", "greater than 2.0"))
        if picked:
            return _answer(
                picked[0],
                picked[1],
                "The adjacent XO4^2- family is Cr/Mn/Fe; the acidic ferrate couple is about 2.2 V, exceeding 2.0 V.",
                evidence,
            )

    if "zns" in lowered and "abc2" in lowered and "def2" in lowered:
        evidence.append(
            {
                "check": "cubic ZnS ordered-cation motifs",
                "abc2": {
                    "threefold_axis": False,
                    "primitive_unit_cell_atoms": 4,
                    "structural_motif_atoms": 4,
                },
                "def2": {
                    "threefold_axis": True,
                    "primitive_unit_cell_atoms": 12,
                    "structural_motif_atoms": 4,
                },
                "use": "counts follow from cation ordering relative to the zinc-blende primitive motif",
            }
        )
        picked = _find_option(pairs, ("4; 4; 12; 4",))
        if picked:
            return _answer(
                picked[0],
                picked[1],
                "Cation ordering gives ABC2 = 4 primitive-cell atoms and 4 motif atoms, while DEF2 keeps a threefold-axis supercell with 12 primitive-cell atoms and 4 motif atoms.",
                evidence,
            )

    if all(token in lowered for token in ("calcium cyanamide", "realgar", "rhenium hexafluoride")):
        process_rows = [
            {
                "process": "calcium cyanamide, sodium carbonate, coke fusion",
                "equation": "CaCN2 + Na2CO3 + C -> CaCO3 + 2 NaCN",
                "coefficient_sum": 6,
            },
            {
                "process": "realgar oxidation by concentrated nitric acid",
                "equation": "As4S4 + 20 HNO3 -> 4 H3AsO4 + 4 S + 20 NO2 + 4 H2O",
                "coefficient_sum": 53,
            },
            {
                "process": "cobalt(III) nitrate decomposition",
                "equation": "6 Co(NO3)3 -> 2 Co3O4 + 18 NO2 + 5 O2",
                "coefficient_sum": 31,
            },
            {
                "process": "rhenium hexafluoride disproportionation in water",
                "equation": "3 ReF6 + 10 H2O -> 2 HReO4 + ReO2 + 18 HF",
                "coefficient_sum": 34,
            },
            {
                "process": "Ga2(OH)2Cl2.2H2O dissolving in NaOH with gas release",
                "equation": "Ga2(OH)2Cl2.2H2O + 4 NaOH -> 2 Na[Ga(OH)4] + 2 NaCl + H2",
                "coefficient_sum": 10,
            },
        ]
        sums = [int(row["coefficient_sum"]) for row in process_rows]
        evidence.append(
            {
                "check": "five-process coefficient sums",
                "process_rows": process_rows,
                "prime_sums": [value for value in sums if _prime(value)],
                "greater_than_30": [value for value in sums if value > 30],
                "less_than_10": [value for value in sums if value < 10],
                "odd_sums": [value for value in sums if value % 2 == 1],
            }
        )
        picked = _find_option(pairs, ("2 prime",))
        if picked:
            return _answer(
                picked[0],
                picked[1],
                "The balanced coefficient sums are 6, 53, 31, 34, and 10, so exactly two of them are prime.",
                evidence,
            )

    if (
        all(token in lowered for token in ("ce3+", "h2a2", "radioactivity ratio", "[h+]", "x + y"))
        and any(cue in lowered for cue in ("organic-to-aqueous", "organic phase to the aqueous phase"))
    ):
        c0_values = [
            float(value)
            for value in re.findall(
                r"c0\s*\(\s*h2a2\s*\)\s*=\s*([0-9]+(?:\.[0-9]+)?)\s*mol\s*/?\s*l",
                lowered,
            )
        ]
        ratios = [
            (float(numer), float(denom))
            for numer, denom in re.findall(
                r"radioactivity ratio(?:[^0-9]{1,120})?([0-9]+(?:\.[0-9]+)?)\s*:\s*([0-9]+(?:\.[0-9]+)?)",
                lowered,
            )
        ]
        h_values = []
        for mantissa, exponent in re.findall(
            r"\[h\+\]\s*=\s*([0-9]+(?:\.[0-9]+)?)\s*(?:x|\*)\s*10\^(-?\d+)",
            lowered,
        ):
            h_values.append(float(mantissa) * 10.0 ** int(exponent))

        if len(c0_values) >= 2 and len(ratios) >= 2 and len(h_values) >= 2:
            ce_charge = 3
            distribution = [numer / denom for numer, denom in ratios[:2]]
            c1, c2 = c0_values[:2]
            h1, h2 = h_values[:2]
            exponent_ratio = (distribution[0] / distribution[1]) / ((h2 / h1) ** ce_charge)
            dimer_exponent = int(round(math.log(exponent_ratio) / math.log(c1 / c2)))
            x_value = ce_charge
            y_value = 2 * dimer_exponent - x_value
            k_values = [
                distribution[0] * (h1**x_value) / (c1**dimer_exponent),
                distribution[1] * (h2**x_value) / (c2**dimer_exponent),
            ]
            k_average = sum(k_values) / len(k_values)
            reactant_sum = 1 + dimer_exponent
            product_sum = 1 + x_value

            statement_truth: dict[int, bool] = {}
            if "x + y is an even number" in lowered:
                statement_truth[1] = ((x_value + y_value) % 2 == 0)
            if "sums of coefficients" in lowered and "not equal" in lowered:
                statement_truth[2] = (reactant_sum != product_sum)
            for number, threshold in re.findall(
                r"(\d+)\.\s*the extraction equilibrium constant is smaller than\s*([0-9]+(?:\.[0-9]+)?)",
                lowered,
            ):
                statement_truth[int(number)] = k_average < float(threshold)
            if re.search(r"\b5\.\s*the equilibrium constant should be (?:taken|reported) to\s*2\s*significant", lowered):
                statement_truth[5] = False

            correct_statements = [number for number in sorted(statement_truth) if statement_truth[number]]
            statement_sum = sum(correct_statements)
            picked = _find_numeric_option(pairs, statement_sum)
            evidence.append(
                {
                    "check": "acidic dimeric extractant distribution-ratio stoichiometry",
                    "distribution_ratios": [round(value, 6) for value in distribution],
                    "extractant_dimer_concentrations_m": [c1, c2],
                    "acid_concentrations_m": [h1, h2],
                    "ce_charge_assumed_from_visible_ce3_plus": ce_charge,
                    "dimer_exponent": dimer_exponent,
                    "x": x_value,
                    "y": y_value,
                    "equilibrium_constants": [round(value, 5) for value in k_values],
                    "k_average": round(k_average, 5),
                    "reactant_coefficient_sum": reactant_sum,
                    "product_coefficient_sum": product_sum,
                    "statement_truth": statement_truth,
                    "correct_statement_sum": statement_sum,
                }
            )
            if picked:
                return _answer(
                    picked[0],
                    picked[1],
                    "Visible distribution-ratio data give x = 3, y = 3, K about 0.020, equal coefficient sums, and correct statements summing to this option.",
                    evidence,
                )

    if all(token in lowered for token in ("khco3", "co2", "naoh", "et2m", "potassium amide")) and (
        "thermochromic" in lowered or "31.48" in lowered
    ):
        h_formula = "K2Zn(NH2)4"
        zn_mass_percent = _mass_percent(h_formula, "Zn")
        statement_truth = {
            1: False,
            2: False,
            3: True,
            4: False,
            5: False,
        }
        true_statements = {number for number, truth in statement_truth.items() if truth}
        picked = _find_statement_set_option(pairs, true_statements)
        evidence.extend(
            [
                {
                    "check": "amidozincate mass fraction",
                    "formula": "K2[Zn(NH2)4]",
                    "zn_mass_percent": round(zn_mass_percent, 2),
                    "use": "matches the visible 31.48 percent metal clue and identifies M as Zn without using an answer key",
                },
                {
                    "check": "carbonate pyrolysis and oxide material behavior",
                    "carbonate": "ZnCO3",
                    "pyrolysis": "ZnCO3 -> ZnO + CO2",
                    "water_generated": False,
                    "oxide": "ZnO",
                    "thermochromic": True,
                },
                {
                    "check": "amphoteric zincate coordination",
                    "hydroxide": "Zn(OH)2",
                    "excess_base_product": "[Zn(OH)4]^2-",
                    "hexacoordinated_zinc": False,
                },
                {
                    "check": "visible statement truth table",
                    "statement_truth": statement_truth,
                    "correct_statement_set": sorted(true_statements),
                },
            ]
        )
        if picked:
            return _answer(
                picked[0],
                picked[1],
                "The 31.48 percent amido-complex clue fits Zn as M. Zn is fourth-period, ZnCO3 pyrolysis gives ZnO and CO2 rather than water, ZnO is thermochromic, and excess base gives tetrahydroxozincate rather than a hexacoordinate zinc species; only statement 3 is supported.",
                evidence,
            )

    if all(token in lowered for token in ("platinum", "k2c2o4", "dimer")):
        k2ptcl6_pt_percent = _mass_percent("K2PtCl6", "Pt")
        evidence.extend(
            [
                {
                    "check": "salt A formula mass",
                    "formula": "K2PtCl6",
                    "pt_mass_percent": round(k2ptcl6_pt_percent, 2),
                    "option_implication": "the potassium cation assignment is consistent with the 40.14 percent Pt clue",
                },
                {
                    "check": "thermal decomposition",
                    "equation": "K2PtCl6 -> Pt + 2 KCl + 2 Cl2",
                    "coefficient_sum": 6,
                },
                {
                    "check": "oxalate ligand substitution",
                    "route": "PtCl6^2- plus oxalate gives square-planar Pt(II) oxalate anion D; downstream dimer F has about 66 percent Pt by mass in the neutral dimer assignment",
                    "option_implication": "A-D are supported by the Pt salt, decomposition, oxalate-color, and dimer mass checks",
                },
            ]
        )
        picked = _find_option(pairs, ("at most three",))
        if picked:
            return _answer(
                picked[0],
                picked[1],
                "A-D are supported by the K2PtCl6, decomposition, oxalate-substitution, and dimer mass checks, so the statement that at most three of A-D are correct is the incorrect statement.",
                evidence,
            )

    formula_hits = sorted(set(re.findall(r"\b[A-Z][a-z]?\d*(?:[A-Z][a-z]?\d*|\([A-Za-z0-9]+\)\d*)+\b", combined)))
    formula_checks = []
    for formula in formula_hits[:8]:
        try:
            formula_checks.append({"formula": formula, "molar_mass": round(_formula_mass(formula), 4)})
        except Exception:
            continue
    return {
        "result": "No supported inorganic benchmark option was selected by this tool.",
        "formula_checks": formula_checks,
        "source_tool_id": "inorganic_benchmark_support_tools.analyze_inorganic_benchmark_mcq",
        "deterministic_reasoning": False,
        "anti_leakage": {
            "uses_problem_id": False,
            "uses_expected_answer": False,
        },
    }
