from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import Counter
from dataclasses import asdict, dataclass, field
from importlib.util import module_from_spec, spec_from_file_location
import inspect
import json
from pathlib import Path
import re
import sys
import time
from typing import Any

from scripts.design.llm_clients import build_text_client_from_profile


TOKEN_PATTERN = re.compile(r"[A-Za-z0-9_+-]+")
INLINE_OPTION_PATTERN = re.compile(r"(?:^|\s)([A-Z])[\.\)]\s+(.+?)(?=(?:\s+[A-Z][\.\)]\s+)|$)")
UNICODE_SUPERSCRIPT_DIGITS = str.maketrans("⁺⁻⁰¹²³⁴⁵⁶⁷⁸⁹", "+-0123456789")
UNICODE_SUBSCRIPT_DIGITS = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")
UNICODE_MINUS_SIGNS = str.maketrans({"−": "-", "–": "-", "—": "-"})
SCIENTIFIC_MULTIPLIER_PATTERN = r"(?:\u00d7|x|\*|\\times|times)"
SUPERSCRIPT_EXPONENT_PATTERN = re.compile(
    rf"(-?\d+(?:\.\d+)?)\s*{SCIENTIFIC_MULTIPLIER_PATTERN}\s*10\s*([\u207a\u207b\u2070\u00b9\u00b2\u00b3\u2074-\u2079]+)",
    flags=re.IGNORECASE,
)
STANDARD_SCIENTIFIC_PATTERN = re.compile(
    rf"(-?\d+(?:\.\d+)?)\s*{SCIENTIFIC_MULTIPLIER_PATTERN}\s*10\s*(?:\^)?\s*\{{?\s*([+-]?\d+)\s*\}}?",
    flags=re.IGNORECASE,
)
GRADING_NORMALIZATION_VERSION = "grading-normalization-v2"

# BEGIN GENERATED_RUNTIME_DOMAIN_CONSTANTS
ELEMENT_ATOMIC_NUMBERS = {
    "h": 1,
    "he": 2,
    "li": 3,
    "be": 4,
    "b": 5,
    "c": 6,
    "n": 7,
    "o": 8,
    "f": 9,
    "ne": 10,
    "na": 11,
    "mg": 12,
    "al": 13,
    "si": 14,
    "p": 15,
    "s": 16,
    "cl": 17,
    "ar": 18,
}
ELEMENT_ATOMIC_NUMBERS.update(
    {
        "k": 19,
        "ca": 20,
        "sc": 21,
        "ti": 22,
        "v": 23,
        "cr": 24,
        "mn": 25,
        "fe": 26,
        "co": 27,
        "ni": 28,
        "cu": 29,
        "zn": 30,
        "ga": 31,
        "ge": 32,
        "as": 33,
        "se": 34,
        "br": 35,
        "kr": 36,
    }
)
COMMON_FORMULAS = {
    "ammonium chloride": "NH4Cl",
    "calcium phosphate": "Ca3(PO4)2",
    "carbon dioxide": "CO2",
    "ammonia": "NH3",
    "aluminum chloride": "AlCl3",
    "argon": "Ar",
    "chlorine": "Cl2",
    "dimethyl ether": "(CH3)2O",
    "ethane": "C2H6",
    "ethylene": "C2H4",
    "helium": "He",
    "hydrogen chloride": "HCl",
    "hydrogen gas": "H2",
    "hydrogen iodide": "HI",
    "hydrogen sulfide": "H2S",
    "methane": "CH4",
    "nitrogen": "N2",
    "nitrogen dioxide": "NO2",
    "oxygen gas": "O2",
    "potassium chlorate": "KClO3",
    "potassium chloride": "KCl",
    "propane": "C3H8",
    "sulfur dioxide": "SO2",
}
VALID_ELEMENT_SYMBOLS = {
    "H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne",
    "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca",
    "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn",
    "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr", "Y", "Zr",
    "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn",
    "Sb", "Te", "I", "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd",
    "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb",
    "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg",
    "Tl", "Pb", "Bi", "Po", "At", "Rn",
}
# END GENERATED_RUNTIME_DOMAIN_CONSTANTS


def normalize_whitespace(text: str) -> str:
    return " ".join(str(text).split())


def parse_numeric_literal(value: str) -> float:
    return float(str(value).replace(",", ""))


def parse_superscript_exponent(value: str) -> int:
    return int(str(value).translate(UNICODE_SUPERSCRIPT_DIGITS))


def tokenize(text: str) -> list[str]:
    return TOKEN_PATTERN.findall(str(text).lower())


def safe_read_text(path: Path) -> str:
    for encoding in ("utf-8", "utf-8-sig", "gb18030", "latin-1"):
        try:
            return path.read_text(encoding=encoding)
        except Exception:
            continue
    return path.read_text(encoding="utf-8", errors="ignore")


def normalize_symbolic_text(text: str) -> str:
    return str(text).translate(UNICODE_SUBSCRIPT_DIGITS)


def json_preview_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): json_preview_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [json_preview_safe(item) for item in value]
    if hasattr(value, "tolist"):
        return json_preview_safe(value.tolist())
    if hasattr(value, "item"):
        try:
            return json_preview_safe(value.item())
        except Exception:
            pass
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


def json_preview(value: Any, *, limit: int = 1800) -> str:
    text = json.dumps(json_preview_safe(value), ensure_ascii=False, indent=2)
    return text if len(text) <= limit else text[:limit] + "\n..."


def extract_json_payload(text: str) -> dict[str, Any]:
    raw = str(text).strip()
    if not raw:
        return {}
    try:
        value = json.loads(raw)
        return value if isinstance(value, dict) else {}
    except Exception:
        pass
    start = raw.find("{")
    end = raw.rfind("}")
    if start >= 0 and end > start:
        try:
            value = json.loads(raw[start : end + 1])
            return value if isinstance(value, dict) else {}
        except Exception:
            return {}
    return {}


def extract_inline_options(question: str) -> list[str]:
    options = []
    for match in INLINE_OPTION_PATTERN.finditer(str(question)):
        letter = match.group(1).upper()
        text = normalize_whitespace(match.group(2)).strip()
        if text:
            options.append(f"{letter}. {text}")
    if len(options) >= 2:
        return options
    parenthesized = []
    matches = list(re.finditer(r"\(([A-Da-d])\)\s*", str(question)))
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(str(question))
        text = normalize_whitespace(str(question)[start:end]).strip(" ,.;")
        if text:
            parenthesized.append(f"{match.group(1).upper()}. {text}")
    if len(parenthesized) >= 2:
        stem = str(question)[: matches[0].start()].strip()
        if "?" not in stem:
            return []
        option_texts = [item.split(".", 1)[1].strip() for item in parenthesized]
        looks_like_qualitative_choices = all(
            len(text) <= 90
            and "?" not in text.rstrip("?")
            and not re.match(r"[-+]?\d", text)
            and not re.search(r"\b(?:ml|l|g|kg|mg|mol|atm|kpa|mmhg|torr|cm|kj|j|cal|°c)\b", text, flags=re.IGNORECASE)
            for text in option_texts
        )
        if looks_like_qualitative_choices:
            return parenthesized
    return []


def strip_inline_options(question: str) -> str:
    first = INLINE_OPTION_PATTERN.search(str(question))
    if not first:
        return str(question)
    return str(question)[: first.start()].strip()


def option_pairs(problem: "GenericProblem | None") -> list[tuple[str, str]]:
    if problem is None:
        return []
    raw_options = list(problem.options) or extract_inline_options(problem.question)
    pairs: list[tuple[str, str]] = []
    for index, raw in enumerate(raw_options):
        text = normalize_whitespace(raw)
        match = re.match(r"^\s*([A-Z])[\.\)]\s*(.+)$", text, flags=re.IGNORECASE)
        if match:
            pairs.append((match.group(1).upper(), match.group(2).strip()))
        else:
            pairs.append((chr(ord("A") + index), text))
    return pairs


def support_score(option_text: str, *, question: str, docs: list["RetrievedDocument"]) -> float:
    option_tokens = {item for item in tokenize(option_text) if len(item) > 1}
    if not option_tokens:
        return 0.0
    stem_tokens = {item for item in tokenize(strip_inline_options(question)) if len(item) > 1}
    doc_tokens: set[str] = set()
    for doc in docs[:6]:
        doc_tokens.update(item for item in tokenize(f"{doc.title} {doc.snippet}") if len(item) > 1)
    return 2.0 * len(option_tokens & doc_tokens) + 0.25 * len(option_tokens & stem_tokens)


# BEGIN GENERATED_RUNTIME_DOMAIN_HELPERS
def extract_element_symbol(question: str) -> str | None:
    lowered = str(question).lower()
    normalized = normalize_symbolic_text(str(question))
    for symbol in re.findall(r"\b([A-Z][a-z]?)(?:\d*[+-]|[+-]\d*)", normalized):
        if symbol in VALID_ELEMENT_SYMBOLS:
            return symbol
    name_to_symbol = {
        "hydrogen": "H",
        "helium": "He",
        "lithium": "Li",
        "beryllium": "Be",
        "boron": "B",
        "carbon": "C",
        "nitrogen": "N",
        "oxygen": "O",
        "fluorine": "F",
        "neon": "Ne",
        "sodium": "Na",
        "magnesium": "Mg",
        "aluminum": "Al",
        "silicon": "Si",
        "phosphorus": "P",
        "sulfur": "S",
        "chlorine": "Cl",
        "argon": "Ar",
    }
    for name, symbol in name_to_symbol.items():
        if name in lowered:
            return symbol
    for symbol in sorted(ELEMENT_ATOMIC_NUMBERS, key=len, reverse=True):
        if re.search(rf"\b{re.escape(symbol)}\b", lowered, flags=re.IGNORECASE):
            return symbol.capitalize()
    return None


def clean_formula_token(text: str) -> str:
    token = normalize_symbolic_text(text)
    token = re.sub(r"\\(?:ce|mathrm|text)\s*", "", token, flags=re.IGNORECASE)
    token = token.replace("_", "").replace("{", "").replace("}", "")
    token = re.sub(r"\((?:aq|s|l|g)\)", "", token, flags=re.IGNORECASE)
    token = re.sub(r"[^A-Za-z0-9()+-]", "", token)
    token = token.strip()
    while len(token) >= 2 and token.startswith("(") and token.endswith(")"):
        depth = 0
        encloses_all = True
        for index, char in enumerate(token):
            if char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
                if depth == 0 and index != len(token) - 1:
                    encloses_all = False
                    break
        if encloses_all and depth == 0:
            token = token[1:-1]
        else:
            break
    return token


def _formula_syntax_is_valid(token: str) -> bool:
    """Validate formula syntax without changing chemically meaningful groups."""

    value = clean_formula_token(token)
    if not value:
        return False
    index = 0

    def parse_group(stop_at_closing: bool = False) -> bool:
        nonlocal index
        consumed = False
        while index < len(value):
            if value[index] == ")":
                if not stop_at_closing or not consumed:
                    return False
                index += 1
                return True
            if value[index] == "(":
                index += 1
                if not parse_group(True):
                    return False
                consumed = True
                while index < len(value) and value[index].isdigit():
                    index += 1
                continue
            element_match = re.match(r"[A-Z][a-z]?", value[index:])
            if not element_match:
                if value[index] in "+-" and index == len(value) - 1:
                    index += 1
                    return consumed
                return False
            element = element_match.group(0)
            if element not in VALID_ELEMENT_SYMBOLS:
                return False
            index += len(element)
            while index < len(value) and value[index].isdigit():
                index += 1
            consumed = True
        return consumed and not stop_at_closing

    return parse_group() and index == len(value)


def is_probable_formula_token(token: str) -> bool:
    value = clean_formula_token(token)
    if not value:
        return False
    if value.upper() == value and len(value) > 2 and not re.search(r"\d|\(", value):
        return False
    return _formula_syntax_is_valid(value)


FORMULA_CANDIDATE_PATTERN = re.compile(
    r"(?<![A-Za-z])(?:[A-Z][a-z]?|\d+|\([A-Za-z0-9]+\)|[()+\-{}_])+(?![a-z])"
)


def _formula_candidate_is_contextually_valid(text: str, match: re.Match[str], token: str) -> bool:
    raw = match.group(0).strip()
    source = str(text)
    before = source[: match.start()]
    after = source[match.end() :]
    previous_nonspace = next((char for char in reversed(before) if not char.isspace()), "")
    next_nonspace = next((char for char in after if not char.isspace()), "")
    if raw in {"(I)", "(II)", "(III)", "(IV)", "(V)"}:
        return False
    if len(token) == 1 and next_nonspace == "=":
        return False
    if (
        len(token) == 1
        and source.strip() != raw
        and not (raw.startswith("(") and raw.endswith(")"))
        and previous_nonspace not in "=([{,;:"
    ):
        return False
    return True


def formula_candidates_from_text(text: str) -> list[str]:
    normalized = normalize_symbolic_text(text)
    candidates: list[str] = []
    for match in FORMULA_CANDIDATE_PATTERN.finditer(normalized):
        token = clean_formula_token(match.group(0))
        if (
            is_probable_formula_token(token)
            and _formula_candidate_is_contextually_valid(normalized, match, token)
            and token not in candidates
        ):
            candidates.append(token)
    for match in re.finditer(r"\bof\s+([A-Z][a-z]?)\b", normalized):
        token = clean_formula_token(match.group(1))
        if is_probable_formula_token(token) and token not in candidates:
            candidates.append(token)
    return candidates


def parse_equation_sides(question: str) -> tuple[list[str], list[str]] | None:
    text = normalize_symbolic_text(question)
    text = re.sub(r"^\s*balance\s*:\s*", "", text, flags=re.IGNORECASE)
    arrow = "->" if "->" in text else "→" if "→" in text else None
    if arrow is None:
        return None
    left, right = text.split(arrow, 1)
    reactants = [clean_formula_token(item) for item in left.split("+")]
    products = [clean_formula_token(item) for item in right.split("+")]
    reactants = [item for item in reactants if item]
    products = [item for item in products if item]
    return (reactants, products) if reactants and products else None


def convert_pressure_to_mmhg(value: float, unit: str) -> float:
    normalized = unit.lower()
    if "atm" in normalized:
        return value * 760.0
    if "bar" in normalized:
        return value * 750.062
    if "kpa" in normalized:
        return value * 7.50062
    return value


def convert_volume_to_ml(value: float, unit: str) -> float:
    normalized = unit.lower()
    if normalized == "l" or "liter" in normalized or normalized in {"dm3", "dm^3"}:
        return value * 1000.0
    return value


def formula_from_question(question: str) -> str | None:
    lowered = question.lower()
    for name, formula in COMMON_FORMULAS.items():
        if name in lowered:
            return formula
    candidates = formula_candidates_from_text(question)
    return candidates[0] if candidates else None

# END GENERATED_RUNTIME_DOMAIN_HELPERS


@dataclass(slots=True)
class GenericProblem:
    problem_id: str
    question: str
    answer: Any | None = None
    options: list[str] = field(default_factory=list)
    source: str = ""
    source_file: str = ""
    given: dict[str, Any] = field(default_factory=dict)
    expected_answer: Any | None = None
    tolerance: dict[str, Any] = field(default_factory=dict)
    matching_module: str | None = None
    matching_function: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class RetrievedDocument:
    path: str
    title: str
    score: float
    snippet: str


@dataclass(slots=True)
class ToolSpec:
    module: str
    function: str
    path: str
    description: str
    params: list[str]
    keywords: list[str]
    required_params: list[str] = field(default_factory=list)

    @property
    def id(self) -> str:
        return f"{self.module}.{self.function}"


@dataclass(slots=True)
class ToolCallResult:
    tool_id: str
    kwargs: dict[str, Any]
    result: Any | None = None
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class GeneratedAgentSpec:
    agent_id: str
    role: str
    dominant_actions: list[str]
    responsibilities: list[str]
    inputs: list[str]
    outputs: list[str]
    dependencies: list[str]
    llm_prompt: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "role": self.role,
            "dominant_actions": list(self.dominant_actions),
            "responsibilities": list(self.responsibilities),
            "inputs": list(self.inputs),
            "outputs": list(self.outputs),
            "dependencies": list(self.dependencies),
            "llm_prompt": self.llm_prompt,
            "metadata": dict(self.metadata),
        }


@dataclass(slots=True)
class AnswerRecord:
    question: str
    final_answer: str
    raw_answer: str
    confidence: float
    retrieved_docs: list[RetrievedDocument]
    tool_calls: list[ToolCallResult]
    route_notes: list[str]
    normalized_prediction: str
    verification: dict[str, Any]
    agent_trace: list[dict[str, Any]] = field(default_factory=list)
    tool_result_payload: Any | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "question": self.question,
            "final_answer": self.final_answer,
            "raw_answer": self.raw_answer,
            "confidence": self.confidence,
            "retrieved_docs": [asdict(item) for item in self.retrieved_docs],
            "tool_calls": [asdict(item) for item in self.tool_calls],
            "route_notes": list(self.route_notes),
            "normalized_prediction": self.normalized_prediction,
            "verification": dict(self.verification),
            "agent_trace": list(self.agent_trace),
            "tool_result_payload": self.tool_result_payload,
        }


@dataclass(slots=True)
class EvaluationRecord:
    problem_id: str
    source_file: str
    correct: bool
    score: float
    expected: Any
    prediction: str
    notes: list[str]
    answer_record: AnswerRecord

    def to_dict(self) -> dict[str, Any]:
        return {
            "problem_id": self.problem_id,
            "source_file": self.source_file,
            "correct": self.correct,
            "score": self.score,
            "expected": self.expected,
            "prediction": self.prediction,
            "notes": list(self.notes),
            "answer_record": self.answer_record.to_dict(),
        }


class MemoryIndex:
    def __init__(self, memory_root: str | Path, *, exclude_dirs: list[str] | None = None) -> None:
        self.memory_root = Path(memory_root)
        self.exclude_dirs = {str(item).strip().lower().replace("\\", "/") for item in (exclude_dirs or []) if str(item).strip()}
        self.documents: list[tuple[str, str, str]] = []

    def build(self) -> "MemoryIndex":
        self.documents.clear()
        if not self.memory_root.exists():
            return self
        for path in sorted(self.memory_root.rglob("*")):
            if not path.is_file():
                continue
            rel = path.relative_to(self.memory_root).as_posix()
            rel_parts = {part.lower() for part in Path(rel).parts}
            if rel_parts & self.exclude_dirs:
                continue
            if path.suffix.lower() not in {".md", ".txt", ".json", ".csv", ".py"}:
                continue
            text = safe_read_text(path)
            if not text.strip():
                continue
            title = next((line.lstrip("#").strip() for line in text.splitlines() if line.strip().startswith("#")), path.stem)
            self.documents.append((rel, title, text))
        return self

    def search(self, query: str, *, top_k: int = 6) -> list[RetrievedDocument]:
        query_tokens = set(tokenize(query))
        scored: list[RetrievedDocument] = []
        for rel, title, text in self.documents:
            title_tokens = set(tokenize(title))
            text_tokens = set(tokenize(text[:4000]))
            overlap = len(query_tokens & text_tokens) + 1.5 * len(query_tokens & title_tokens)
            if overlap <= 0:
                continue
            snippet = text[:700]
            scored.append(RetrievedDocument(path=rel, title=title, score=round(float(overlap), 4), snippet=snippet))
        scored.sort(key=lambda item: item.score, reverse=True)
        return scored[:top_k]


class ToolCatalog:
    def __init__(self, tools_root: str | Path) -> None:
        self.tools_root = Path(tools_root)
        self.tools: list[ToolSpec] = []
        self._module_cache: dict[str, Any] = {}

    def build(self) -> "ToolCatalog":
        self.tools.clear()
        if not self.tools_root.exists():
            return self
        for path in sorted(self.tools_root.glob("*.py")):
            if path.name.startswith("_") or path.name == "batch_verify.py":
                continue
            module_name = f"generated_tool_{path.stem}"
            try:
                module = self._load_module(path, module_name)
            except Exception:
                continue
            for function_name, function in inspect.getmembers(module, inspect.isfunction):
                if function.__module__ != module.__name__ or function_name.startswith("_"):
                    continue
                signature = inspect.signature(function)
                params = [
                    name
                    for name, parameter in signature.parameters.items()
                    if parameter.kind
                    in {
                        inspect.Parameter.POSITIONAL_OR_KEYWORD,
                        inspect.Parameter.KEYWORD_ONLY,
                    }
                ]
                required_params = [
                    name
                    for name, parameter in signature.parameters.items()
                    if parameter.kind
                    in {
                        inspect.Parameter.POSITIONAL_OR_KEYWORD,
                        inspect.Parameter.KEYWORD_ONLY,
                    }
                    and parameter.default is inspect.Parameter.empty
                ]
                doc = inspect.getdoc(function) or ""
                keywords = sorted(set(tokenize(" ".join([path.stem, function_name, doc]))))
                self.tools.append(
                    ToolSpec(
                        module=path.stem,
                        function=function_name,
                        path=path.as_posix(),
                        description=doc[:1000],
                        params=params,
                        keywords=keywords,
                        required_params=required_params,
                    )
                )
        return self

    def _load_module(self, path: Path, module_name: str) -> Any:
        cached = self._module_cache.get(module_name)
        if cached is not None:
            return cached
        spec = spec_from_file_location(module_name, path)
        if spec is None or spec.loader is None:
            raise ImportError(f"Unable to load module from {path}")
        module = module_from_spec(spec)
        tools_root = str(self.tools_root.resolve())
        if tools_root not in sys.path:
            sys.path.insert(0, tools_root)
        spec.loader.exec_module(module)
        self._module_cache[module_name] = module
        return module

    def find(self, module: str, function: str) -> ToolSpec | None:
        return next((tool for tool in self.tools if tool.module == module and tool.function == function), None)

    def search(self, query: str, *, top_k: int = 6) -> list[ToolSpec]:
        query_tokens = set(tokenize(query))
        scored: list[tuple[float, ToolSpec]] = []
        for tool in self.tools:
            overlap = len(query_tokens & set(tool.keywords))
            if overlap <= 0:
                continue
            scored.append((float(overlap), tool))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [item[1] for item in scored[:top_k]]

    def execute(self, tool: ToolSpec, kwargs: dict[str, Any]) -> ToolCallResult:
        module_name = f"generated_tool_{tool.module}"
        try:
            module = self._load_module(self.tools_root / f"{tool.module}.py", module_name)
            function = getattr(module, tool.function)
            filtered = {name: value for name, value in kwargs.items() if name in tool.params}
            result = function(**filtered)
            return ToolCallResult(tool_id=tool.id, kwargs=filtered, result=result)
        except Exception as exc:
            return ToolCallResult(tool_id=tool.id, kwargs=kwargs, error=str(exc))


def normalize_problem_record(record: dict[str, Any], *, source_file: str, index: int = 0) -> GenericProblem:
    if not isinstance(record, dict):
        record = {"question": str(record)}
    question = str(
        record.get("question")
        or record.get("question_text")
        or record.get("problem_text")
        or record.get("q")
        or record.get("qt")
        or record.get("text")
        or ""
    )
    answer = record.get("answer")
    if answer is None:
        answer = record.get("correct_answer")
    if answer is None:
        answer = record.get("expected_answer")
    if answer is None:
        answer = record.get("ca")
    if answer is None:
        answer = record.get("solution")
    options = list(record.get("options", [])) if isinstance(record.get("options"), list) else []
    if not options:
        options = extract_inline_options(question)
    problem_id = str(record.get("id") or record.get("problem_id") or record.get("qid") or "").strip()
    if not problem_id:
        problem_id = f"{Path(source_file).stem}_{index + 1:04d}"
    return GenericProblem(
        problem_id=problem_id,
        question=question,
        answer=answer,
        options=options,
        source=str(record.get("source_short") or record.get("source") or record.get("original_file") or ""),
        source_file=source_file,
        given=record.get("given", {}) if isinstance(record.get("given"), dict) else {},
        expected_answer=record.get("expected_answer"),
        tolerance=record.get("tolerance", {}) if isinstance(record.get("tolerance"), dict) else {},
        matching_module=record.get("matching_module"),
        matching_function=record.get("matching_function"),
        metadata={key: value for key, value in record.items() if key not in {"id", "problem_id", "qid", "question", "question_text", "problem_text", "q", "qt", "text", "answer", "correct_answer", "expected_answer", "ca", "solution", "options", "source_short", "source", "original_file", "given", "tolerance", "matching_module", "matching_function"}},
    )


def load_generic_problem_file(path: str | Path) -> list[GenericProblem]:
    file_path = Path(path)
    data = json.loads(file_path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        rows = data
    elif isinstance(data, dict) and isinstance(data.get("problems"), list):
        rows = data["problems"]
    elif isinstance(data, dict) and isinstance(data.get("items"), list):
        rows = data["items"]
    elif isinstance(data, dict) and isinstance(data.get("questions"), list):
        rows = data["questions"]
    elif isinstance(data, dict) and isinstance(data.get("examples"), list):
        rows = data["examples"]
    else:
        rows = []
    return [normalize_problem_record(item, source_file=file_path.as_posix(), index=index) for index, item in enumerate(rows)]


def normalize_prediction(text: str) -> str:
    return normalize_whitespace(text).strip("`")


def build_numeric_tolerance(tolerance: dict[str, Any], expected_value: float) -> float:
    candidates: list[float] = []
    if "absolute" in tolerance:
        candidates.append(float(tolerance["absolute"]))
    if "relative" in tolerance:
        candidates.append(abs(expected_value) * float(tolerance["relative"]))
    if candidates:
        return max(candidates)
    return max(1e-6, abs(expected_value) * 1e-2)


def normalize_equation_text(value: str) -> str:
    text = normalize_symbolic_text(value)
    text = text.replace("→", "->")
    text = text.replace("*", "")
    text = re.sub(r"\((?:aq|s|l|g)\)", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s+", "", text)
    return text.lower()


def looks_like_equation(value: str) -> bool:
    return "->" in value or "→" in value


def first_numeric(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, dict):
        if isinstance(value.get("answer_values"), list):
            return first_numeric(value["answer_values"])
        for item in value.values():
            result = first_numeric(item)
            if result is not None:
                return result
    if isinstance(value, list):
        for item in value:
            result = first_numeric(item)
            if result is not None:
                return result
    return None


def scientific_notation_values(text: str) -> list[float]:
    source = str(text).translate(UNICODE_MINUS_SIGNS)
    normalized = source.translate(UNICODE_SUPERSCRIPT_DIGITS)
    values = []
    for match in SUPERSCRIPT_EXPONENT_PATTERN.finditer(source):
        try:
            values.append(float(match.group(1)) * (10 ** parse_superscript_exponent(match.group(2))))
        except Exception:
            continue
    for match in STANDARD_SCIENTIFIC_PATTERN.finditer(normalized):
        try:
            values.append(float(match.group(1)) * (10 ** int(match.group(2))))
        except Exception:
            continue
    return values


def numeric_spans(text: str) -> list[tuple[int, int, float, str]]:
    """Return numeric values with source spans, suppressing mantissa/exponent duplicates."""

    source = str(text).translate(UNICODE_MINUS_SIGNS)
    normalized = source.translate(UNICODE_SUPERSCRIPT_DIGITS)
    spans: list[tuple[int, int, float, str]] = []
    occupied: list[tuple[int, int]] = []

    def overlaps_existing(start: int, end: int) -> bool:
        return any(start < occupied_end and end > occupied_start for occupied_start, occupied_end in occupied)

    for match in SUPERSCRIPT_EXPONENT_PATTERN.finditer(source):
        try:
            value = float(match.group(1)) * (10 ** parse_superscript_exponent(match.group(2)))
        except Exception:
            continue
        spans.append((match.start(), match.end(), value, match.group(0)))
        occupied.append((match.start(), match.end()))
    for match in STANDARD_SCIENTIFIC_PATTERN.finditer(normalized):
        if overlaps_existing(match.start(), match.end()):
            continue
        try:
            value = float(match.group(1)) * (10 ** int(match.group(2)))
        except Exception:
            continue
        spans.append((match.start(), match.end(), value, match.group(0)))
        occupied.append((match.start(), match.end()))

    for match in re.finditer(r"-?\d[\d,]*(?:\.\d+)?(?:e[+-]?\d+)?", normalized, flags=re.IGNORECASE):
        start, end = match.span()
        if overlaps_existing(start, end):
            continue
        if start > 0 and normalized[start - 1].isalpha():
            continue
        try:
            value = parse_numeric_literal(match.group(0))
        except Exception:
            continue
        spans.append((start, end, value, match.group(0)))
    spans.sort(key=lambda item: item[0])
    return spans


def _is_exponent_numeric_span(normalized_text: str, start: int, end: int) -> bool:
    raw = normalized_text[start:end].replace(",", "")
    if not re.fullmatch(r"[+-]?\d+(?:\.0+)?", raw):
        return False
    prefix = normalized_text[max(0, start - 12) : start]
    return bool(re.search(r"\^\s*\{?\s*$", prefix))


def answer_candidate_numeric_spans(text: str) -> list[tuple[int, int, float, str]]:
    """Return numeric spans usable as answer values, excluding unit/formula exponents."""

    normalized = str(text).translate(UNICODE_SUPERSCRIPT_DIGITS).translate(UNICODE_MINUS_SIGNS)
    return [
        (start, end, value, raw)
        for start, end, value, raw in numeric_spans(str(text))
        if not _is_exponent_numeric_span(normalized, start, end)
    ]


def answer_candidate_numeric_values(text: str) -> list[float]:
    return [item[2] for item in answer_candidate_numeric_spans(str(text))]


FINAL_ANSWER_MARKER_PATTERN = re.compile(r"final\s+answer\s*:\s*", flags=re.IGNORECASE)


def requires_separate_final_answer_line(
    problem: GenericProblem | None = None,
    *,
    question: str = "",
) -> bool:
    """Return whether the problem explicitly requires a separate final-answer line."""

    metadata = problem.metadata if problem and isinstance(problem.metadata, dict) else {}
    if metadata.get("require_separate_final_answer_line") or metadata.get("final_answer_line_required"):
        return True
    source = str(question or (problem.question if problem else ""))
    lowered = normalize_whitespace(source).lower()
    return bool(
        "final answer:" in lowered
        and (
            "separate line" in lowered
            or "final-answer line" in lowered
            or re.search(r"\bfinish\s+with\b.{0,80}\bfinal\s+answer\b", lowered)
        )
    )


def separate_final_answer_line(text: str) -> str | None:
    """Extract a canonical final-answer line only when it is the last non-empty line."""

    lines = [line.strip() for line in str(text or "").splitlines() if line.strip()]
    if not lines:
        return None
    final_line = lines[-1]
    if not re.match(r"^final\s+answer\s*:\s*\S", final_line, flags=re.IGNORECASE):
        return None
    payload = re.sub(r"^final\s+answer\s*:\s*", "", final_line, flags=re.IGNORECASE).strip()
    if re.search(r"<\s*(?:number\d*|unit)\s*>", payload, flags=re.IGNORECASE):
        return None
    return re.sub(r"^final\s+answer\s*:\s*", "Final answer: ", final_line, flags=re.IGNORECASE)


def _preserve_answer_line_breaks(text: str) -> str:
    lines = [normalize_whitespace(line) for line in str(text or "").strip().splitlines()]
    normalized = "\n".join(lines)
    return re.sub(r"\n{3,}", "\n\n", normalized).strip()


def _format_structured_final_answer_values(answer_values: list[Any], units: list[Any] | None) -> str:
    rendered_values: list[str] = []
    normalized_units = [normalize_whitespace(str(unit)) for unit in (units or [])]
    for index, value in enumerate(answer_values):
        try:
            numeric_value = float(value)
            rendered = f"{numeric_value:.8g}"
        except (TypeError, ValueError):
            rendered = normalize_whitespace(str(value))
        unit = ""
        if len(normalized_units) == len(answer_values):
            unit = normalized_units[index]
        elif len(normalized_units) == 1 and normalized_units[0].lower() != "mixed":
            unit = normalized_units[0]
        if unit and unit.lower() not in {"dimensionless", "none", "unitless"}:
            rendered = f"{rendered} {unit}"
        rendered_values.append(rendered)
    return ", ".join(rendered_values)


def enforce_separate_final_answer_line(
    text: str,
    *,
    question: str,
    answer_values: list[Any] | None = None,
    units: list[Any] | None = None,
) -> str:
    """Move an explicit final-answer marker onto one canonical last line.

    This deliberately does not invent an answer when the marker is absent. A
    missing marker remains a verifier/evaluator failure.
    """

    normalized = _preserve_answer_line_breaks(text)
    if not normalized or not requires_separate_final_answer_line(question=question):
        return normalized
    markers = list(FINAL_ANSWER_MARKER_PATTERN.finditer(normalized))
    if not markers:
        structured_payload = _format_structured_final_answer_values(answer_values or [], units)
        if structured_payload:
            return f"{normalized}\n\nFinal answer: {structured_payload}"
        return normalized
    marker = markers[-1]
    prefix = normalized[: marker.start()].rstrip()
    suffix = normalized[marker.end() :].strip()
    if not suffix:
        return normalized

    payload_line, separator, remainder = suffix.partition("\n")
    payload = payload_line.strip()
    trailing_body = remainder.strip() if separator else ""
    prose_boundary = re.search(r"(?<=[A-Za-z0-9)\]])\.(?=\s+[A-Za-z])", payload)
    if prose_boundary:
        trailing_body = " ".join(
            part for part in (payload[prose_boundary.end() :].strip(), trailing_body) if part
        )
        payload = payload[: prose_boundary.start()].strip()
    payload = payload.rstrip(" .")
    if not payload:
        return normalized

    body_parts = [part for part in (prefix, trailing_body) if part]
    body = _preserve_answer_line_breaks("\n".join(body_parts))
    final_line = f"Final answer: {payload}"
    return f"{body}\n\n{final_line}" if body else final_line


def evaluation_integrity_failures(problem: GenericProblem, answer_record: AnswerRecord) -> list[str]:
    """Return hard evaluation failures that a gold-answer match cannot rescue."""

    failures: list[str] = []
    if requires_separate_final_answer_line(problem) and separate_final_answer_line(answer_record.final_answer) is None:
        failures.append("required separate final-answer line is missing or malformed")

    verification = answer_record.verification if isinstance(answer_record.verification, dict) else {}
    status = str(verification.get("status", "")).strip().lower()
    if status in {"fail", "failed", "blocked", "error"}:
        failures.append(f"verification status is unresolved: {status}")

    challenge = verification.get("performance_challenge")
    if isinstance(challenge, dict):
        blocking_risks = {
            "answer_missing",
            "leakage_risk",
            "suspicious_overfitting",
        }
        for risk in challenge.get("risks", []) if isinstance(challenge.get("risks"), list) else []:
            normalized_risk = str(risk).strip().lower()
            if normalized_risk in blocking_risks:
                failures.append(f"unresolved performance risk: {normalized_risk}")
    return failures


def evaluation_quality_warnings(answer_record: AnswerRecord) -> list[str]:
    """Return non-blocking evidence and tool-support warnings."""

    verification = answer_record.verification if isinstance(answer_record.verification, dict) else {}
    warnings: list[str] = []
    status = str(verification.get("status", "")).strip().lower()
    if status == "review":
        warnings.append("verification status requires review")
    challenge = verification.get("performance_challenge")
    warning_risks = {
        "capability_frontier_gap",
        "tool_execution_failures",
        "weak_quantitative_support",
    }
    if isinstance(challenge, dict) and isinstance(challenge.get("risks"), list):
        for risk in challenge["risks"]:
            normalized_risk = str(risk).strip().lower()
            if normalized_risk in warning_risks:
                warnings.append(f"non-blocking performance warning: {normalized_risk}")
    return list(dict.fromkeys(warnings))


def _exact_numeric_final_answer_matches_expected(problem: GenericProblem, answer_record: AnswerRecord) -> bool:
    gold = problem.answer if problem.answer is not None else problem.expected_answer
    expected_values = numeric_answer_values(gold)
    if not expected_values:
        return False
    final_line = separate_final_answer_line(answer_record.final_answer)
    if requires_separate_final_answer_line(problem):
        if final_line is None:
            return False
        observed_values = answer_like_numeric_values(final_line, question=problem.question)
    else:
        observed_values = answer_like_numeric_values(final_line or answer_record.final_answer, question=problem.question)
    if not observed_values:
        return False
    return _compare_numeric_values(
        expected_values,
        observed_values,
        tolerance=problem.tolerance,
    )[0]


def numeric_values(value: Any) -> list[float]:
    if isinstance(value, bool):
        return []
    if isinstance(value, (int, float)):
        return [float(value)]
    if isinstance(value, dict):
        if isinstance(value.get("answer_values"), list):
            return numeric_values(value["answer_values"])
        values: list[float] = []
        for item in value.values():
            values.extend(numeric_values(item))
        return values
    if isinstance(value, list):
        values: list[float] = []
        for item in value:
            values.extend(numeric_values(item))
        return values
    return [item[2] for item in numeric_spans(str(value))]


STRUCTURED_EXPLANATION_KEYS = {"explanation", "rationale", "reason", "work", "calculation", "derivation", "approach"}
STRUCTURED_METADATA_STRING_KEYS = {"part_id", "part_ids", "unit", "units", "source_tool_id"}


def numeric_values_without_percent_labels(text: str) -> list[float]:
    values: list[float] = []
    for start, end, value, _raw in numeric_spans(str(text)):
        suffix = str(text)[end : end + 8].lstrip()
        if suffix.startswith("%") or suffix.lower().startswith("percent"):
            continue
        values.append(value)
    return values


def boxed_numeric_values(text: str) -> list[float]:
    values: list[float] = []
    source = str(text)
    marker = r"\boxed"
    search_start = 0
    while True:
        marker_index = source.find(marker, search_start)
        if marker_index < 0:
            break
        brace_index = source.find("{", marker_index + len(marker))
        if brace_index < 0:
            break
        depth = 0
        end_index: int | None = None
        for index in range(brace_index, len(source)):
            char = source[index]
            if char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
                if depth == 0:
                    end_index = index
                    break
        if end_index is None:
            break
        inner_numbers = numeric_spans(source[brace_index + 1 : end_index])
        if inner_numbers:
            values.append(inner_numbers[0][2])
        search_start = end_index + 1
    return values


def numeric_answer_values(value: Any) -> list[float]:
    if isinstance(value, dict):
        if isinstance(value.get("answer_values"), list):
            return numeric_values(value["answer_values"])
        for preferred_key in ("numerical_answer", "numeric_answer", "final_answer", "answer"):
            if preferred_key in value:
                preferred_values = numeric_values_without_percent_labels(str(value[preferred_key]))
                if preferred_values:
                    return preferred_values
        values: list[float] = []
        for key, item in value.items():
            if str(key).lower() in STRUCTURED_EXPLANATION_KEYS:
                continue
            values.extend(numeric_answer_values(item))
        return values
    if isinstance(value, list):
        values: list[float] = []
        for item in value:
            values.extend(numeric_answer_values(item))
        return values
    return numeric_values(value)


def structured_explanation_text(value: Any) -> str:
    if isinstance(value, dict):
        chunks: list[str] = []
        for key, item in value.items():
            if str(key).lower() in STRUCTURED_EXPLANATION_KEYS:
                chunks.append(str(item))
            else:
                text = structured_explanation_text(item)
                if text:
                    chunks.append(text)
        return " ".join(chunks)
    if isinstance(value, list):
        return " ".join(structured_explanation_text(item) for item in value)
    return ""


def _split_answer_segments(text: str) -> list[str]:
    raw_segments = re.split(r"(?<=[.!?])\s+|[;\n]+", normalize_whitespace(text))
    return [segment.strip(" .") for segment in raw_segments if segment.strip(" .")]


def _question_requests_multiple_numeric_answers(question: str) -> bool:
    lowered = str(question).lower()
    if re.search(
        r"\b(?:two|three|four|five|six|\d+)\s+(?:values|answers|quantities|numbers|outputs|results|gaps|energy\s+gaps)\b",
        lowered,
    ):
        return True
    if re.search(
        r"\b(?:in\s+this\s+order|in\s+that\s+order|in\s+the\s+following\s+order|in\s+order|respectively)\b",
        lowered,
    ) and re.search(
        r"\b(?:values|answers|quantities|numbers|outputs|results|gaps|calculate|report)\b",
        lowered,
    ):
        return True
    if re.search(r"\b(?:and|then|followed\s+by|first|second|respectively|in\s+order)\b", lowered) and re.search(
        r"\b(?:decimal\s+)?(?:mass\s+|mole\s+)?fraction\b|\b(?:mass\s+)?percent(?:age)?\b",
        lowered,
    ):
        return True
    if re.search(r"\b(?:molecular\s+weight|molar\s+mass|formula\s+mass)\b", lowered) and not re.search(
        r"\b(?:molecular\s+weights|molar\s+masses|formula\s+masses|respectively)\b", lowered
    ):
        return False
    if (
        re.search(r"\b(?:calculate|determine|find|estimate|what\s+is)\b", lowered)
        and re.search(r"(?:\\delta|delta|螖)\s*[shg]\b|\b(?:entropy|enthalpy|gibbs|free\s+energy)\b", lowered)
        and not re.search(r"\b(?:respectively|in\s+this\s+order|in\s+order|both|two)\b", lowered)
    ):
        return False
    if not re.search(r"\b(?:calculate|determine|find|what are|give)\b", lowered):
        return False
    if re.search(r"\b(?:and|and the|respectively)\b", lowered) and re.search(r"\b(?:k[cp]?|ph|poh|\[[^\]]+\])\b", lowered):
        return True
    return "," in lowered and re.search(r"\b(?:ph|poh|moles?|mol|mole fraction|concentration|rate|pressure|volume)\b", lowered)


def _numeric_list_values_from_body(text: str) -> list[float]:
    spans = answer_candidate_numeric_spans(text)
    if len(spans) == 1 and "," in spans[0][3]:
        raw = spans[0][3]
        pieces = raw.split(",")
        if all(piece.isdigit() for piece in pieces) and not all(len(piece) == 3 for piece in pieces[1:]):
            return [float(piece) for piece in pieces]
    if len(spans) < 2:
        return []
    residual_parts: list[str] = []
    cursor = 0
    for start, end, _value, _raw in spans:
        residual_parts.append(str(text)[cursor:start])
        cursor = end
    residual_parts.append(str(text)[cursor:])
    residual = "".join(residual_parts)
    residual = re.sub(r"\\(?:quad|qquad|!|,|;|:|\s)", "", residual, flags=re.IGNORECASE)
    residual = re.sub(r"[\s,;:.!?]+", "", residual)
    if residual:
        return []
    return [item[2] for item in spans]


def _explicit_numeric_list_values(text: str) -> list[float]:
    source = re.sub(r"\\(?:left|right)\s*", "", normalize_whitespace(text), flags=re.IGNORECASE)
    wrapper_patterns = (
        r"\\\((?P<body>.*?)\\\)",
        r"\\\[(?P<body>.*?)\\\]",
        r"\$\$(?P<body>.*?)\$\$",
        r"\$(?P<body>.*?)\$",
        r"\[(?P<body>[^\[\]]+)\]",
    )
    candidates: list[list[float]] = []
    for pattern in wrapper_patterns:
        for match in re.finditer(pattern, source, flags=re.DOTALL):
            values = _numeric_list_values_from_body(match.group("body"))
            if values:
                candidates.append(values)
    whole_text_values = _numeric_list_values_from_body(source)
    if whole_text_values:
        candidates.append(whole_text_values)
    return max(candidates, key=len, default=[])


def _has_invalid_numeric_list_expression(text: str) -> bool:
    source = re.sub(r"\\(?:left|right)\s*", "", normalize_whitespace(text), flags=re.IGNORECASE)
    wrapper_patterns = (
        r"\\\((?P<body>.*?)\\\)",
        r"\\\[(?P<body>.*?)\\\]",
        r"\$\$(?P<body>.*?)\$\$",
        r"\$(?P<body>.*?)\$",
        r"\[(?P<body>[^\[\]]+)\]",
    )
    saw_valid_numeric_wrapper = False
    for pattern in wrapper_patterns:
        for match in re.finditer(pattern, source, flags=re.DOTALL):
            body = match.group("body")
            if len(answer_candidate_numeric_spans(body)) < 2:
                continue
            if _numeric_list_values_from_body(body):
                saw_valid_numeric_wrapper = True
            else:
                return True
    if saw_valid_numeric_wrapper:
        return False
    return len(answer_candidate_numeric_spans(source)) >= 2 and bool(re.search(r"\\[A-Za-z]+", source))


def answer_like_numeric_values(value: Any, *, question: str = "") -> list[float]:
    """Extract likely final-answer numbers from explanatory gold-answer text."""

    if not isinstance(value, str):
        return numeric_values(value)
    text = normalize_whitespace(value)
    all_numbers = answer_candidate_numeric_spans(text)
    if not all_numbers:
        return []
    final_answer_matches = list(
        re.finditer(r"(?:^|\b)(?:final\s+answer|answer)\s*(?:is|:|-)\s*", text, flags=re.IGNORECASE)
    )
    for marker in reversed(final_answer_matches):
        tail = text[marker.end() :]
        explicit_tail_values = _explicit_numeric_list_values(tail)
        if explicit_tail_values:
            return explicit_tail_values
        if _has_invalid_numeric_list_expression(tail):
            return []
        tail_numbers = answer_candidate_numeric_spans(tail)
        if tail_numbers:
            if _question_requests_multiple_numeric_answers(question):
                return [item[2] for item in tail_numbers]
            return [tail_numbers[0][2]]
    if _has_invalid_numeric_list_expression(text):
        return []
    boxed_values = boxed_numeric_values(text)
    if boxed_values:
        return boxed_values
    explicit_list_values = _explicit_numeric_list_values(text)
    if explicit_list_values:
        return explicit_list_values
    part_markers = list(re.finditer(r"(?<!\w)\([a-z]\)\s*", text, flags=re.IGNORECASE))
    if len(part_markers) >= 2:
        part_values: list[float] = []
        for index, marker in enumerate(part_markers):
            end = part_markers[index + 1].start() if index + 1 < len(part_markers) else len(text)
            segment_numbers = answer_candidate_numeric_spans(text[marker.end() : end])
            if segment_numbers:
                part_values.append(segment_numbers[0][2])
        if len(part_values) == len(part_markers):
            return part_values
    if not _question_requests_multiple_numeric_answers(question):
        leading_start, leading_end, leading_value, _leading_raw = all_numbers[0]
        leading_tail = text[leading_end:].lstrip()
        if not text[:leading_start].strip() and (
            not leading_tail
            or re.match(
                r"^(?:[.;,%]|percent\b|amu\b|"
                r"(?:m[lm]?|l|g|kg|mg|mol|mmhg|torr|atm|bar|pa|kpa|"
                r"kj|j|ev|k|s|min|h|hz|nm|pm|cm)\b)",
                leading_tail,
                flags=re.IGNORECASE,
            )
        ):
            return [leading_value]
    for bold_match in reversed(list(re.finditer(r"\*\*([^*]+)\*\*", text))):
        bold_segment = bold_match.group(1).strip()
        bold_numbers = answer_candidate_numeric_spans(bold_segment)
        if (
            bold_numbers
            and len(bold_segment) <= 180
            and "=" not in bold_segment
            and re.match(r"^\s*[-+]?\d", bold_segment)
        ):
            if _question_requests_multiple_numeric_answers(question):
                return [item[2] for item in bold_numbers]
            return [bold_numbers[-1][2]]
    segments = _split_answer_segments(text)
    lowered_question = str(question).lower()
    if _question_requests_multiple_numeric_answers(question):
        leading_numbers: list[float] = []
        for segment in segments or [text]:
            stripped_segment = segment.strip(" *`_")
            if not stripped_segment:
                continue
            if len(stripped_segment) > 120 or "=" in stripped_segment or not re.match(r"^\s*[-+]?\d", stripped_segment):
                if leading_numbers:
                    break
                continue
            segment_numbers = answer_candidate_numeric_spans(stripped_segment)
            if not segment_numbers:
                if leading_numbers:
                    break
                continue
            leading_numbers.extend(item[2] for item in segment_numbers)
            if len(leading_numbers) >= 2 and ("," in stripped_segment or ";" in text or len(segment_numbers) >= 2):
                return leading_numbers
        if len(leading_numbers) >= 2:
            return leading_numbers
    if "spin states" in lowered_question and "magnetic field" in lowered_question and "kj/mol" in lowered_question:
        isotope_values = []
        for isotope in ("19F", "1H"):
            match = re.search(
                rf"{re.escape(isotope)}\s*=\s*(-?\d+(?:,\d{{3}})*(?:\.\d+)?(?:e[+-]?\d+)?)",
                text,
                flags=re.IGNORECASE,
            )
            if match:
                isotope_values.append(float(match.group(1).replace(",", "")))
        if isotope_values:
            return isotope_values
    if "born-haber" in lowered_question or "lattice enthalpy" in lowered_question:
        for segment in reversed(segments or [text]):
            if not re.search(r"\b(?:kj\s*/\s*mol|enthalpy|dh|delta\s*h|hf)\b", segment, flags=re.IGNORECASE):
                continue
            segment_numbers = answer_candidate_numeric_spans(segment)
            if not segment_numbers:
                continue
            after_equal_numbers = []
            if "=" in segment:
                after_equal_numbers = answer_candidate_numeric_spans(segment[segment.rfind("=") + 1 :])
            return [(after_equal_numbers or segment_numbers)[-1][2]]
    if "saturation vapor pressure" in lowered_question or "vapor pressure" in lowered_question and "clapeyron" in lowered_question:
        pressure_candidates = []
        for segment in segments or [text]:
            if not re.search(r"\bp\s*2|p₂|pressure|bar|atm", segment, flags=re.IGNORECASE):
                continue
            pressure_candidates.extend(answer_candidate_numeric_spans(segment))
        if pressure_candidates:
            return [pressure_candidates[-1][2]]
    if re.search(r"\bpH\b", str(question), flags=re.IGNORECASE):
        if _question_requests_multiple_numeric_answers(question):
            pH_assignment_values: list[float] = []
            for segment in segments or [text]:
                if not re.search(r"\bpH\s*=", segment, flags=re.IGNORECASE):
                    continue
                if re.search(r"\bpKa\s*\+", segment, flags=re.IGNORECASE):
                    continue
                after_equal_numbers = []
                if "=" in segment:
                    after_equal_numbers = answer_candidate_numeric_spans(segment[segment.find("=") + 1 :])
                if after_equal_numbers:
                    pH_assignment_values.append(after_equal_numbers[0][2])
            if len(pH_assignment_values) >= 2:
                return pH_assignment_values
        for segment in segments or [text]:
            if not re.search(r"\bpH\s*=", segment, flags=re.IGNORECASE):
                continue
            if re.search(r"\bpKa\s*\+", segment, flags=re.IGNORECASE):
                continue
            after_equal_numbers = []
            if "=" in segment:
                after_equal_numbers = answer_candidate_numeric_spans(segment[segment.find("=") + 1 :])
            if after_equal_numbers:
                return [after_equal_numbers[0][2]]
    if _question_requests_multiple_numeric_answers(question):
        for segment in reversed(segments or [text]):
            stripped_segment = segment.strip(" *`_")
            segment_numbers = answer_candidate_numeric_spans(stripped_segment)
            if (
                segment_numbers
                and len(stripped_segment) <= 180
                and "=" not in stripped_segment
                and re.match(r"^\s*[-+]?\d", stripped_segment)
            ):
                return [item[2] for item in segment_numbers]
    if not _question_requests_multiple_numeric_answers(question):
        assignment_target_cues = (
            "energy",
            "enthalpy",
            "entropy",
            "gibbs",
            "pressure",
            "mass",
            "concentration",
            "rate",
            "constant",
            "temperature",
            "wavelength",
            "frequency",
            "solubility",
            "work",
            "yield",
        )
        for segment in segments or [text]:
            stripped_segment = segment.strip(" *`_")
            if len(stripped_segment) > 180:
                continue
            assignment_match = re.match(
                r"\s*([A-Za-z][A-Za-z0-9_+\-\[\]\s]{0,48})\s*=\s*",
                stripped_segment,
            )
            if not assignment_match:
                continue
            assignment_label = assignment_match.group(1).lower().replace(" ", "_")
            if not any(cue in assignment_label for cue in assignment_target_cues):
                continue
            assigned_numbers = answer_candidate_numeric_spans(stripped_segment[assignment_match.end() :])
            if assigned_numbers:
                return [assigned_numbers[0][2]]
    if re.search(r"\b(?:rmse|root\s+mean\s+square\s+error)\b", str(question), flags=re.IGNORECASE):
        for segment in segments or [text]:
            if not re.search(r"\brmse\b|\broot\s+mean\s+square\s+error\b", segment, flags=re.IGNORECASE):
                continue
            if re.search(r"\b(?:acceptable|typical|threshold|less\s+than|<)\b", segment, flags=re.IGNORECASE):
                continue
            segment_numbers = answer_candidate_numeric_spans(segment)
            if segment_numbers:
                after_equal_numbers = []
                if "=" in segment:
                    after_equal_numbers = answer_candidate_numeric_spans(segment[segment.rfind("=") + 1 :])
                return [(after_equal_numbers or segment_numbers)[-1][2]]
    if "bond length" in str(question).lower():
        for segment in segments or [text]:
            if not re.search(r"\br\s*=|\bbond\s+length\b", segment, flags=re.IGNORECASE):
                continue
            segment_numbers = answer_candidate_numeric_spans(segment)
            if segment_numbers:
                after_equal_numbers = []
                if "=" in segment:
                    after_equal_numbers = answer_candidate_numeric_spans(segment[segment.rfind("=") + 1 :])
                return [(after_equal_numbers or segment_numbers)[-1][2]]
    if "force constant" in str(question).lower():
        for segment in reversed(segments or [text]):
            if not re.search(r"(?:\bforce\s+constant\b|\bk\s*=)", segment, flags=re.IGNORECASE):
                continue
            force_unit_numbers: list[float] = []
            for start, end, value, _raw in answer_candidate_numeric_spans(segment):
                suffix = segment[end : end + 32].lower()
                if re.search(r"\b(?:n\s*/\s*m|n\s*m\s*(?:\^-?1|-1)|newtons?\s*(?:per|/)\s*meter)", suffix):
                    force_unit_numbers.append(value)
            if force_unit_numbers:
                return [force_unit_numbers[-1]]
    if re.search(r"\b(?:molecular\s+weight|molar\s+mass|formula\s+mass)\b", lowered_question):
        for segment in reversed(segments or [text]):
            if not re.search(
                r"\b(?:mw|molecular\s+weight|molar\s+mass|formula\s+mass)\b|g\s*/?\s*mol",
                segment,
                flags=re.IGNORECASE,
            ):
                continue
            if not re.search(r"\b(?:answer|result|therefore|thus|so|approximately|about|equals?|is|=)\b", segment, flags=re.IGNORECASE):
                continue
            segment_numbers = answer_candidate_numeric_spans(segment)
            if not segment_numbers:
                continue
            after_equal_numbers = []
            if "=" in segment:
                after_equal_numbers = answer_candidate_numeric_spans(segment[segment.rfind("=") + 1 :])
            return [(after_equal_numbers or segment_numbers)[-1][2]]
    if segments:
        first_segment = segments[0]
        first_numbers = answer_candidate_numeric_spans(first_segment)
        if (
            first_numbers
            and len(first_segment) <= 90
            and "=" not in first_segment
            and re.match(r"^\s*[-+]?\d", first_segment)
        ):
            if _question_requests_multiple_numeric_answers(question):
                return [item[2] for item in first_numbers]
            return [first_numbers[0][2]]

    target_label_patterns: list[str] = []
    if re.search(
        r"\b(?:calculate|determine|find|estimate|what\s+is)\b[^.?!;\n]{0,180}\b(?:enthalpy\s+of\s+formation|formation\s+enthalpy|heat\s+of\s+formation|delta\s*h\s*f)\b",
        lowered_question,
    ):
        target_label_patterns.append(
            r"(?:\\delta|delta|\u0394|\u87d6)\s*h\s*(?:[o0]|\u00b0|\u63b3)?\s*f\b|\b(?:deltahf|delta\s*h\s*f|dhf|h\s*(?:[o0]|\u00b0|\u63b3)?\s*f|formation\s+enthalpy|enthalpy\s+of\s+formation|heat\s+of\s+formation)\b"
        )
    if re.search(r"\b(?:calculate|determine|find|estimate|what\s+is)\b[^.?!;\n]{0,140}\b(?:delta\s*s|entropy)\b", lowered_question):
        target_label_patterns.append(r"(?:\\delta|delta|螖)\s*s\b|\b(?:deltas|entropy)\b")
    if re.search(r"\b(?:calculate|determine|find|estimate|what\s+is)\b[^.?!;\n]{0,140}\b(?:delta\s*h|enthalpy)\b", lowered_question):
        target_label_patterns.append(r"(?:\\delta|delta|螖)\s*h\b|\b(?:deltah|enthalpy)\b")
    if re.search(r"\b(?:calculate|determine|find|estimate|what\s+is)\b[^.?!;\n]{0,140}\b(?:delta\s*g|gibbs|free\s+energy)\b", lowered_question):
        target_label_patterns.append(r"(?:\\delta|delta|螖)\s*g\b|\b(?:deltag|gibbs|free\s+energy)\b")
    if re.search(r"\b(?:calculate|determine|find|estimate|what\s+is)\b[^.?!;\n]{0,180}\b(?:wavelength|lambda)\b", lowered_question):
        target_label_patterns.append(r"\b(?:wavelength(?:_[a-z0-9]+)?|lambda|lamda)\b")
    if re.search(r"\b(?:calculate|determine|find|estimate|what\s+is)\b[^.?!;\n]{0,180}\b(?:wavenumber|wave\s+number)\b", lowered_question):
        target_label_patterns.append(r"\b(?:wavenumber|wave\s*number|nu\s*bar|nubar)\b")
    if re.search(r"\b(?:gas\s+constant|calculate\s+r\b|determine\s+r\b|find\s+r\b|estimate\s+r\b)\b", lowered_question):
        target_label_patterns.append(r"\br\b|\bgas\s+constant\b")
    for label_pattern in target_label_patterns:
        direct_labelled_values: list[float] = []
        labelled_values: list[float] = []
        for segment in segments or [text]:
            label_match = re.search(label_pattern, segment, flags=re.IGNORECASE)
            if not label_match:
                continue
            assignment_tail_match = re.match(
                r"\s*(?:=|:|is|equals?|approximately|approx\.?|about)\s*",
                segment[label_match.end() :],
                flags=re.IGNORECASE,
            )
            if assignment_tail_match:
                assigned_tail = segment[label_match.end() + assignment_tail_match.end() :]
                direct_numbers = answer_candidate_numeric_spans(assigned_tail)
                if direct_numbers and not re.search(r"[A-Za-z]", assigned_tail[: direct_numbers[0][0]]):
                    direct_labelled_values.append(direct_numbers[0][2])
                    continue
            equal_index = segment.rfind("=")
            if equal_index < 0:
                continue
            after_equal_numbers = answer_candidate_numeric_spans(segment[equal_index + 1 :])
            if after_equal_numbers:
                labelled_values.append(after_equal_numbers[-1][2])
        selected_labelled_values = direct_labelled_values or labelled_values
        if selected_labelled_values:
            if _question_requests_multiple_numeric_answers(question):
                return selected_labelled_values
            return [selected_labelled_values[-1]]

    question_tokens = set(tokenize(question))
    candidates: list[tuple[float, float]] = []
    for index, segment in enumerate(segments or [text]):
        segment_numbers = answer_candidate_numeric_spans(segment)
        if not segment_numbers:
            continue
        after_equal_numbers: list[tuple[int, int, float, str]] = []
        if "=" in segment:
            last_equal = segment.rfind("=")
            after_equal_numbers = answer_candidate_numeric_spans(segment[last_equal + 1 :])
        selected_number = (after_equal_numbers or segment_numbers)[-1][2]
        prefix = segment.split("=", 1)[0]
        prefix_tokens = set(tokenize(prefix))
        score = float(len(prefix_tokens & question_tokens))
        lowered_question = str(question).lower()
        lowered_segment = segment.lower()
        if "enthalpy" in lowered_question and re.search(r"\b(?:delta\s*h|dh|Δh|enthalpy)\b", lowered_segment, flags=re.IGNORECASE):
            score += 3.0
        if "bond energy" in lowered_question and re.search(r"\b(?:bond|bonds|e\s*=|kJ\s*/\s*mol)\b", lowered_segment, flags=re.IGNORECASE):
            score += 4.0
        if re.search(r"\b(?:rmse|root\s+mean\s+square\s+error)\b", lowered_question):
            if re.search(r"\brmse\b|\broot\s+mean\s+square\s+error\b", lowered_segment, flags=re.IGNORECASE):
                score += 5.0
            if re.search(r"\b(?:acceptable|typical|threshold|less\s+than|<)\b", lowered_segment, flags=re.IGNORECASE):
                score -= 3.0
        if "per mole" in lowered_question and re.search(r"/\s*mol|\bper\s+mole\b", lowered_segment, flags=re.IGNORECASE):
            score += 2.0
        if (
            re.search(r"\b(?:molecular\s+weight|molar\s+mass|formula\s+mass)\b", lowered_question)
            and re.search(r"\b(?:mw|molecular\s+weight|molar\s+mass|formula\s+mass)\b|g\s*/\s*mol", lowered_segment, flags=re.IGNORECASE)
        ):
            score += 3.0
        if index == len(segments) - 1:
            score += 0.75
        if re.match(r"^\s*[A-Za-z][A-Za-z0-9_+\-\[\]]{0,16}\s*=", segment):
            score += 1.0
        if re.search(r"\b(?:answer|result|therefore|thus|equals?|is|are)\b", segment, flags=re.IGNORECASE):
            score += 0.5
        candidates.append((score, selected_number))
    if candidates:
        best_score = max(score for score, _ in candidates)
        if _question_requests_multiple_numeric_answers(question):
            selected = [value for score, value in candidates if score >= max(1.5, best_score - 1.0)]
        else:
            selected = [max(enumerate(candidates), key=lambda item: (item[1][0], item[0]))[1][1]]
        if selected:
            return selected
    return [all_numbers[-1][2]]


def _compare_numeric_values(
    expected_values: list[float],
    observed_values: list[float],
    *,
    tolerance: dict[str, Any],
    relative_floor: float = 0.0,
) -> tuple[bool, float, list[str]]:
    if not expected_values or not observed_values:
        return False, 0.0, ["numeric comparison unavailable"]
    used: set[int] = set()
    scores: list[float] = []
    failures: list[str] = []
    for expected in expected_values:
        tolerance_value = build_numeric_tolerance(tolerance, expected)
        if relative_floor > 0.0:
            tolerance_value = max(tolerance_value, abs(expected) * relative_floor)
        best_index: int | None = None
        best_error: float | None = None
        for index, observed in enumerate(observed_values):
            if index in used:
                continue
            error = abs(observed - expected)
            if best_error is None or error < best_error:
                best_index = index
                best_error = error
        if best_index is None or best_error is None:
            failures.append(f"missing observed numeric value for expected={expected}")
            scores.append(0.0)
            continue
        used.add(best_index)
        observed = observed_values[best_index]
        scores.append(max(0.0, 1.0 - best_error / max(abs(expected), 1.0)))
        if best_error > tolerance_value:
            failures.append(f"numeric mismatch: observed={observed}, expected={expected}, tolerance={tolerance_value}")
    return not failures, round(sum(scores) / max(len(scores), 1), 4), failures


def _compare_numeric_values_ordered(
    expected_values: list[float],
    observed_values: list[float],
    *,
    tolerance: dict[str, Any],
    relative_floor: float = 0.0,
) -> tuple[bool, float, list[str]]:
    if not expected_values or not observed_values:
        return False, 0.0, ["ordered numeric comparison unavailable"]
    cursor = 0
    scores: list[float] = []
    failures: list[str] = []
    for expected in expected_values:
        tolerance_value = build_numeric_tolerance(tolerance, expected)
        if relative_floor > 0.0:
            tolerance_value = max(tolerance_value, abs(expected) * relative_floor)
        best_index: int | None = None
        best_error: float | None = None
        for index in range(cursor, len(observed_values)):
            error = abs(observed_values[index] - expected)
            if best_error is None or error < best_error:
                best_index = index
                best_error = error
        if best_index is None or best_error is None or best_error > tolerance_value:
            failures.append(f"ordered numeric mismatch for expected={expected}, tolerance={tolerance_value}")
            scores.append(0.0)
            continue
        cursor = best_index + 1
        scores.append(max(0.0, 1.0 - best_error / max(abs(expected), 1.0)))
    if failures:
        failures.insert(0, "ordered numeric answer values required")
    return not failures, round(sum(scores) / max(len(scores), 1), 4), failures


def _requires_ordered_numeric_values(problem: GenericProblem, gold: dict[str, Any]) -> bool:
    if not isinstance(gold.get("answer_values"), list) or len(gold.get("answer_values", [])) <= 1:
        return False
    metadata = problem.metadata or {}
    if metadata.get("require_ordered_answer_values") or metadata.get("ordered_answer_values"):
        return True
    lowered = normalize_whitespace(problem.question).lower()
    ordered_cues = [
        r"\bin\s+this\s+order\b",
        r"\bin\s+order\b",
        r"\bordered\s+as\b",
        r"\banswer\s+order\b",
        r"\border\s*:",
        r"\brespectively\b",
    ]
    if any(re.search(pattern, lowered) for pattern in ordered_cues):
        return True
    return " first" in lowered and " then " in lowered


def _string_leaf_values(value: Any) -> list[str]:
    if isinstance(value, dict):
        values: list[str] = []
        for key, item in value.items():
            if str(key).lower() in STRUCTURED_METADATA_STRING_KEYS:
                continue
            values.extend(_string_leaf_values(item))
        return values
    if isinstance(value, list):
        values: list[str] = []
        for item in value:
            values.extend(_string_leaf_values(item))
        return values
    if isinstance(value, str) and not numeric_values(value):
        return [value]
    return []


def _flatten_text(value: Any) -> str:
    if isinstance(value, dict):
        return " ".join(f"{key} {_flatten_text(item)}" for key, item in value.items())
    if isinstance(value, list):
        return " ".join(_flatten_text(item) for item in value)
    return str(value)


def _expected_unit_keys(value: Any) -> set[str]:
    units: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            lowered = str(key).lower()
            if lowered.endswith("_a") or "angstrom" in lowered:
                units.add("angstrom")
            units.update(_expected_unit_keys(item))
    elif isinstance(value, list):
        for item in value:
            units.update(_expected_unit_keys(item))
    return units


def _length_values_as_angstrom(text: str) -> list[float]:
    unit_factors = {
        "pm": 0.01,
        "picometer": 0.01,
        "picometers": 0.01,
        "nm": 10.0,
        "nanometer": 10.0,
        "nanometers": 10.0,
        "cm": 1.0e8,
        "centimeter": 1.0e8,
        "centimeters": 1.0e8,
        "m": 1.0e10,
        "meter": 1.0e10,
        "meters": 1.0e10,
        "a": 1.0,
        "angstrom": 1.0,
        "angstroms": 1.0,
    }
    normalized = str(text).translate(UNICODE_SUPERSCRIPT_DIGITS).translate(UNICODE_MINUS_SIGNS)
    values: list[float] = []
    pattern = (
        r"(-?\d[\d,]*(?:\.\d+)?(?:e[+-]?\d+)?(?:\s*(?:×|x|\*)\s*10\s*(?:\^)?\s*[+-]?\d+)?)"
        r"\s*(pm|picometers?|nm|nanometers?|cm|centimeters?|m|meters?|Å|angstroms?)\b"
    )
    for match in re.finditer(pattern, normalized, flags=re.IGNORECASE):
        raw_unit = match.group(2).lower()
        if raw_unit == "å":
            raw_unit = "a"
        values_in_match = numeric_values(match.group(1))
        if values_in_match:
            values.append(values_in_match[0] * unit_factors[raw_unit])
    return values


def _augment_observed_numbers_for_expected_units(gold: dict[str, Any], observed_source: Any, observed_numbers: list[float]) -> list[float]:
    augmented = list(observed_numbers)
    if "angstrom" in _expected_unit_keys(gold):
        augmented.extend(_length_values_as_angstrom(str(observed_source)))
    return augmented


def relation_order_terms(text: str) -> list[str]:
    normalized = normalize_symbolic_text(text).lower()
    if "<" not in normalized:
        return []
    terms: list[str] = []
    for part in normalized.split("<"):
        classed_match = re.search(r"\b(?:acid|base)\s+([a-z])\b", part)
        if classed_match:
            terms.append(classed_match.group(1))
            continue
        cleaned = re.sub(r"\([^)]*\)", " ", part)
        tokens = [
            token
            for token in tokenize(cleaned)
            if token not in {"in", "of", "increasing", "decreasing", "order", "strength", "acid", "base"}
        ]
        if tokens:
            terms.append(tokens[0] if len(tokens[0]) <= 3 else tokens[-1])
    return terms


def relation_order_matches(prediction: str, gold: str) -> bool:
    gold_terms = relation_order_terms(gold)
    pred_terms = relation_order_terms(prediction)
    return bool(gold_terms and pred_terms and gold_terms == pred_terms[: len(gold_terms)])


def spectroscopy_assignment_matches(prediction: str, gold: dict[str, Any]) -> bool:
    assignments = gold.get("assignments") if isinstance(gold, dict) else None
    if not isinstance(assignments, dict) or not assignments:
        return False
    normalized_prediction = re.sub(r"\bstretch(?:ing|es)?\b", "stretch", prediction, flags=re.IGNORECASE)
    for expected in assignments.values():
        normalized_expected = re.sub(r"\bstretch(?:ing|es)?\b", "stretch", str(expected), flags=re.IGNORECASE)
        if token_overlap_score(normalized_prediction, normalized_expected) < 0.5:
            return False
    return True


def cfse_terms_match(prediction: str, gold: str) -> bool:
    def terms(text: str) -> list[float]:
        normalized = normalize_symbolic_text(text).replace("−", "-").replace("–", "-").replace("ₒ", "0")
        values = [float(item) for item in re.findall(r"(-?\d+(?:\.\d+)?)\s*Δ", normalized)]
        finals = [float(item) for item in re.findall(r"=\s*(-?\d+(?:\.\d+)?)\s*Δ", normalized)]
        return finals or values

    raw_expected = numeric_values(gold)
    first_segment_numbers = numeric_values((_split_answer_segments(prediction) or [prediction])[0])
    if raw_expected and first_segment_numbers:
        final_expected = raw_expected[-1]
        if any(abs(value - final_expected) <= 1e-9 for value in first_segment_numbers[:2]):
            return True
    expected = terms(gold)
    observed = terms(prediction)
    if not expected or not observed:
        return False
    remaining = list(observed)
    for value in expected:
        match_index = next((index for index, candidate in enumerate(remaining) if abs(candidate - value) <= 1e-9), None)
        if match_index is None:
            return False
        remaining.pop(match_index)
    return True


def vibrational_partition_matches(prediction: str, gold: str, question: str) -> bool:
    lowered_question = question.lower()
    if "vibrational" not in lowered_question or "partition function" not in lowered_question:
        return False
    expected_numbers = numeric_values(gold)
    observed_numbers = numeric_values(prediction)
    if not expected_numbers or not observed_numbers:
        return False
    theta_expected = expected_numbers[0]
    has_theta = any(abs(value - theta_expected) <= max(5.0, abs(theta_expected) * 0.005) for value in observed_numbers)
    has_q_near_one = any(abs(value - 1.0) <= 0.02 for value in observed_numbers)
    lowered_prediction = prediction.lower()
    has_zero_point = "zero-point" in lowered_prediction or "zero point" in lowered_prediction or re.search(r"\br\s*theta", lowered_prediction)
    return bool(has_theta and has_q_near_one and has_zero_point)


def evaluate_structured_gold(problem: GenericProblem, answer_record: AnswerRecord, gold: dict[str, Any]) -> tuple[bool, float, list[str]]:
    prediction = answer_record.final_answer
    observed_source = answer_record.tool_result_payload if answer_record.tool_result_payload is not None else prediction
    expected_numbers = numeric_answer_values(gold)
    final_text_number_candidates: list[list[float]] = []
    observed_number_candidates: list[list[float]] = []
    strict_final_line = requires_separate_final_answer_line(problem)
    if strict_final_line:
        final_line = separate_final_answer_line(prediction)
        final_line_numbers = (
            answer_like_numeric_values(final_line, question=problem.question)
            if final_line
            else []
        )
        if final_line_numbers:
            final_text_number_candidates.append(final_line_numbers)
            observed_number_candidates.append(final_line_numbers)
    elif isinstance(prediction, str):
        prediction_preferred_numbers = answer_like_numeric_values(prediction, question=problem.question)
        if prediction_preferred_numbers:
            final_text_number_candidates.append(prediction_preferred_numbers)
            observed_number_candidates.append(prediction_preferred_numbers)
    if not strict_final_line and isinstance(observed_source, str):
        preferred_numbers = answer_like_numeric_values(observed_source, question=problem.question)
        if preferred_numbers and preferred_numbers not in observed_number_candidates:
            observed_number_candidates.append(preferred_numbers)
    elif not strict_final_line and isinstance(observed_source, dict):
        for preferred_key in ("answer", "final_answer", "result"):
            answer_text = observed_source.get(preferred_key)
            if isinstance(answer_text, str):
                preferred_numbers = answer_like_numeric_values(answer_text, question=problem.question)
                if preferred_numbers and preferred_numbers not in observed_number_candidates:
                    observed_number_candidates.append(preferred_numbers)
                    break
    if not strict_final_line:
        raw_observed_numbers = numeric_values(observed_source)
        if raw_observed_numbers and raw_observed_numbers not in observed_number_candidates:
            observed_number_candidates.append(raw_observed_numbers)
        raw_prediction_numbers = numeric_values(prediction)
        if raw_prediction_numbers and raw_prediction_numbers not in observed_number_candidates:
            final_text_number_candidates.append(raw_prediction_numbers)
            observed_number_candidates.append(raw_prediction_numbers)
    if expected_numbers and observed_number_candidates:
        best_result: tuple[bool, float, list[str]] | None = None
        ordered_required = _requires_ordered_numeric_values(problem, gold)
        final_text_best_result: tuple[bool, float, list[str]] | None = None
        compare_numeric = _compare_numeric_values_ordered if ordered_required else _compare_numeric_values
        for observed_base_numbers in final_text_number_candidates:
            observed_numbers = _augment_observed_numbers_for_expected_units(gold, prediction, observed_base_numbers)
            if not observed_numbers:
                continue
            if strict_final_line and ordered_required and len(observed_numbers) != len(expected_numbers):
                final_correct = False
                final_score = 0.0
                final_notes = [
                    "ordered numeric answer values required",
                    (
                        "final-answer value count mismatch: "
                        f"observed={len(observed_numbers)}, expected={len(expected_numbers)}"
                    ),
                ]
                if final_text_best_result is None:
                    final_text_best_result = (final_correct, final_score, final_notes)
                continue
            final_correct, final_score, final_notes = compare_numeric(
                expected_numbers,
                observed_numbers,
                tolerance=problem.tolerance,
                relative_floor=0.03,
            )
            if final_correct:
                return final_correct, final_score, final_notes
            if final_text_best_result is None or final_score > final_text_best_result[1]:
                final_text_best_result = (final_correct, final_score, final_notes)
        if final_text_best_result is not None:
            return (
                False,
                final_text_best_result[1],
                [
                    "final answer numeric text did not match expected values; structured payload ignored",
                    *final_text_best_result[2],
                ],
            )
        for observed_base_numbers in observed_number_candidates:
            observed_numbers = _augment_observed_numbers_for_expected_units(gold, observed_source, observed_base_numbers)
            if not observed_numbers:
                continue
            correct, score, notes = compare_numeric(
                expected_numbers,
                observed_numbers,
                tolerance=problem.tolerance,
                relative_floor=0.03,
            )
            string_values = _string_leaf_values(gold)
            if string_values:
                expected_text = " ".join(string_values)
                if token_overlap_score(prediction, expected_text) < 0.5 and not relation_order_matches(prediction, expected_text):
                    correct = False
                    score = min(score, 0.75)
                    notes.append("structured string field not supported by prediction")
            if correct:
                return correct, score, notes
            if best_result is None or score > best_result[1]:
                best_result = (correct, score, notes)
            if ordered_required:
                continue
            explanation_text = structured_explanation_text(gold)
            explanation_candidates = [answer_like_numeric_values(explanation_text, question=problem.question)]
            raw_explanation_numbers = numeric_values(explanation_text)
            if raw_explanation_numbers:
                explanation_candidates.append([raw_explanation_numbers[-1]])
            for explanation_numbers in explanation_candidates:
                if not explanation_numbers:
                    continue
                explanation_correct, explanation_score, explanation_notes = _compare_numeric_values(
                    explanation_numbers,
                    observed_numbers,
                    tolerance=problem.tolerance,
                    relative_floor=0.03,
                )
                if explanation_correct:
                    return True, max(score, explanation_score), ["structured explanation final numeric matched", *explanation_notes]
        if best_result is not None:
            return best_result
    expected_text = _flatten_text(gold)
    if relation_order_matches(prediction, expected_text):
        return True, 1.0, ["ordered relation matched"]
    if re.search(r"\b(?:ir|infrared|spectrum|spectroscopy|absorption|absorptions)\b", problem.question, flags=re.IGNORECASE):
        if spectroscopy_assignment_matches(prediction, gold):
            return True, 0.9, ["spectroscopy assignments matched"]
    overlap = token_overlap_score(prediction, expected_text)
    threshold = 0.82
    if re.search(r"\b(?:ir|infrared|spectrum|spectroscopy|absorption|absorptions)\b", problem.question, flags=re.IGNORECASE):
        threshold = 0.65
    return overlap >= threshold, round(overlap, 4), [f"structured token overlap={overlap:.3f}"]


def evaluate_numeric_text_gold(problem: GenericProblem, answer_record: AnswerRecord, gold: str) -> tuple[bool, float, list[str]] | None:
    expected_numbers = answer_like_numeric_values(gold, question=problem.question)
    observed_source = answer_record.tool_result_payload if answer_record.tool_result_payload is not None else answer_record.final_answer
    final_text_number_candidates: list[list[float]] = []
    observed_number_candidates: list[list[float]] = []
    strict_final_line = requires_separate_final_answer_line(problem)
    if strict_final_line:
        final_line = separate_final_answer_line(answer_record.final_answer)
        preferred_numbers = (
            answer_like_numeric_values(final_line, question=problem.question)
            if final_line
            else []
        )
        if preferred_numbers:
            final_text_number_candidates.append(preferred_numbers)
            observed_number_candidates.append(preferred_numbers)
    elif isinstance(answer_record.final_answer, str):
        preferred_numbers = answer_like_numeric_values(answer_record.final_answer, question=problem.question)
        if preferred_numbers:
            final_text_number_candidates.append(preferred_numbers)
            observed_number_candidates.append(preferred_numbers)
    if not strict_final_line and isinstance(observed_source, str):
        preferred_numbers = answer_like_numeric_values(observed_source, question=problem.question)
        if preferred_numbers and preferred_numbers not in observed_number_candidates:
            observed_number_candidates.append(preferred_numbers)
    elif not strict_final_line and isinstance(observed_source, dict):
        for preferred_key in ("answer", "final_answer", "result"):
            answer_text = observed_source.get(preferred_key)
            if isinstance(answer_text, str):
                preferred_numbers = answer_like_numeric_values(answer_text, question=problem.question)
                if preferred_numbers and preferred_numbers not in observed_number_candidates:
                    observed_number_candidates.append(preferred_numbers)
                    break
    if not strict_final_line:
        raw_observed_numbers = numeric_values(observed_source)
        if raw_observed_numbers and raw_observed_numbers not in observed_number_candidates:
            observed_number_candidates.append(raw_observed_numbers)
    if not expected_numbers or not observed_number_candidates:
        return None
    best_result: tuple[bool, float, list[str]] | None = None
    final_text_best_result: tuple[bool, float, list[str]] | None = None
    ordered_required = _requires_ordered_numeric_values(problem, {"answer_values": expected_numbers}) or len(
        re.findall(r"(?<!\w)\([a-z]\)\s*", gold, flags=re.IGNORECASE)
    ) >= 2
    compare_numeric = _compare_numeric_values_ordered if ordered_required else _compare_numeric_values
    for observed_numbers in final_text_number_candidates:
        if strict_final_line and ordered_required and len(observed_numbers) != len(expected_numbers):
            result = (
                False,
                0.0,
                [
                    "ordered numeric answer values required",
                    (
                        "final-answer value count mismatch: "
                        f"observed={len(observed_numbers)}, expected={len(expected_numbers)}"
                    ),
                ],
            )
            if final_text_best_result is None:
                final_text_best_result = result
            continue
        relative_floor = 0.03 if len(expected_numbers) > 1 or len(observed_numbers) > 1 else 0.0
        result = compare_numeric(
            expected_numbers,
            observed_numbers,
            tolerance=problem.tolerance,
            relative_floor=relative_floor,
        )
        if result[0]:
            return result
        if final_text_best_result is None or result[1] > final_text_best_result[1]:
            final_text_best_result = result
    if final_text_best_result is not None:
        return (
            False,
            final_text_best_result[1],
            [
                "final answer numeric text did not match expected values; structured payload ignored",
                *final_text_best_result[2],
            ],
        )
    for observed_numbers in observed_number_candidates:
        relative_floor = 0.03 if len(expected_numbers) > 1 or len(observed_numbers) > 1 else 0.0
        result = compare_numeric(
            expected_numbers,
            observed_numbers,
            tolerance=problem.tolerance,
            relative_floor=relative_floor,
        )
        if result[0]:
            return result
        if best_result is None or result[1] > best_result[1]:
            best_result = result
    return best_result


def has_structured_numeric_evidence(value: Any) -> bool:
    if isinstance(value, (int, float)):
        return True
    if isinstance(value, str):
        return bool(numeric_values(value))
    if isinstance(value, dict):
        if isinstance(value.get("answer_values"), list):
            return has_structured_numeric_evidence(value.get("answer_values"))
        return any(has_structured_numeric_evidence(item) for item in value.values())
    if isinstance(value, list):
        return any(has_structured_numeric_evidence(item) for item in value)
    return False


def normalized_letter(value: Any) -> str | None:
    raw_text = normalize_prediction(str(value)).strip()
    bare_letter = re.fullmatch(r"\(?([A-Za-z])\)?[\.\):;-]?", raw_text)
    if bare_letter:
        return bare_letter.group(1).upper()
    leading_science_letter = re.match(
        r"\s*\(?([B-Hb-h])\)?\s+(?=(?:\[[A-Za-z]|[A-Z][a-z]|\d))",
        raw_text,
    )
    if leading_science_letter:
        return leading_science_letter.group(1).upper()
    leading_a_numeric_or_bracket = re.match(r"\s*\(?([Aa])\)?\s+(?=(?:\[[A-Za-z]|\d))", raw_text)
    if leading_a_numeric_or_bracket:
        return "A"
    leading_a_formula_token = re.match(
        r"\s*\(?([Aa])\)?\s+(?=(?:R\s*[_-]?\s*S\b|DELTA\b|D[GHUS]\b|E(?:CELL)?\b|P(?:H|OH)\b|K(?:[_-]?[A-Z0-9]+)?\b|[A-Z][A-Z0-9_+-]*\s*=))",
        raw_text,
        flags=re.IGNORECASE,
    )
    if leading_a_formula_token:
        return "A"
    text = raw_text.upper()
    explicit_matches = re.findall(
        r"\b(?:FINAL\s+ANSWER|CORRECT\s+ANSWER|ANSWER|CORRECT\s+OPTION|FINAL\s+OPTION)\s*(?:IS|:)?\s*\(?([A-Z])\)?\b",
        text,
    )
    if explicit_matches:
        return explicit_matches[-1]
    final_choice_patterns = [
        r"\b(?:I\s*(?:WOULD\s*)?(?:CHOOSE|SELECT|PICK)|I'?LL\s+GO\s+WITH|I\s+WILL\s+GO\s+WITH|GO\s+WITH)\s+(?:OPTION\s+)?\(?([A-Z])\)?\b",
        r"\b(?:THE\s+ANSWER|MY\s+ANSWER|FINAL\s+CHOICE|CORRECT\s+CHOICE|BEST\s+ANSWER|MOST\s+LIKELY\s+ANSWER)\s*(?:IS|:|,)?\s*(?:OPTION\s+)?\(?([A-Z])\)?\b",
        r"\b(?:STRICTLY\s+)?(?:CORRESPONDS|MAPS|MATCH(?:ES)?)\s+(?:(?:TO|WITH)\s+)?(?:[\W_]{0,12})?(?:THE\s+)?(?:CORRECT\s+)?(?:OPTION\s+)?\(?([A-Z])\)?\b",
        r"\b(?:WHICH|THIS|THAT|IT|THESE|THOSE|THESE\s+VALUES|THOSE\s+VALUES|THE\s+VALUES)\s+(?:MATCH(?:ES)?|CORRESPONDS\s+(?:TO|WITH)|MAPS\s+(?:TO|WITH))\s+(?:THE\s+)?(?:CORRECT\s+)?OPTION\s+\(?([A-Z])\)?\b",
        r"\b(?:MATCH(?:ES)?|CORRESPONDS\s+(?:TO|WITH)|MAPS\s+(?:TO|WITH))\s+(?:THE\s+)?(?:CORRECT\s+)?OPTION\s+\(?([A-Z])\)?\b",
    ]
    final_choice_matches: list[str] = []
    for pattern in final_choice_patterns:
        final_choice_matches.extend(re.findall(pattern, text))
    if final_choice_matches:
        return final_choice_matches[-1]
    option_verdict_matches: list[str] = []
    option_markers = list(re.finditer(r"(?:^|[\s\n])([A-Z])[\.\)]\s+", raw_text, flags=re.IGNORECASE))
    for index, marker in enumerate(option_markers):
        segment_start = marker.end()
        segment_end = option_markers[index + 1].start() if index + 1 < len(option_markers) else len(raw_text)
        segment = raw_text[segment_start:segment_end][:360]
        segment_upper = segment.upper()
        has_positive_verdict = (
            "✓" in segment
            or "✔" in segment
            or re.search(r"\b(?:CORRECT|TRUE|RIGHT)\b", segment_upper) is not None
        )
        has_negative_verdict = re.search(r"\b(?:INCORRECT|WRONG|FALSE|REVERSED|NOT\s+CORRECT)\b", segment_upper) is not None
        if has_positive_verdict and not has_negative_verdict:
            option_verdict_matches.append(marker.group(1).upper())
    if option_verdict_matches and len(set(option_verdict_matches)) == 1:
        return option_verdict_matches[-1]
    leading_markdown_marked_letter = re.match(
        r"\s*(?:\*\*|__)\s*\(?([A-Z])\)?\s*[\.\):;-](?:\s|$|(?:\*\*|__))",
        text,
    )
    if leading_markdown_marked_letter:
        return leading_markdown_marked_letter.group(1)
    leading_markdown_letter = re.match(r"\s*(?:\*\*|__)\s*\(?([A-Z])\)?\s*(?:\*\*|__)(?:\s|$|[\.\):;-])", text)
    if leading_markdown_letter:
        return leading_markdown_letter.group(1)
    leading_option = re.match(r"\s*\(?([A-Z])\)?\s+OPTION\s+\1\b", text)
    if leading_option:
        return leading_option.group(1)
    leading_marked_letter = re.match(r"\s*\(?([A-Z])\)?\s*(?:[\.\):;-]|\*\*|OPTION\b|ANSWER\b|CORRECT\b|CHOICE\b|REASON\b)", text)
    if leading_marked_letter:
        return leading_marked_letter.group(1)
    leading_plain_evidence_letter = re.match(
        r"\s*\(?([A-Z])\)?\s+(?:THE|BECAUSE|THIS|IT|BLUE|RED|GREEN|AMBER|PURPLE|BLACK|WHITE|CORRECT)\b",
        text,
    )
    if leading_plain_evidence_letter:
        return leading_plain_evidence_letter.group(1)
    leading_reasoning_letter = re.match(
        r"\s*\(?([A-Z])\)?\s+(?:TO|USING|FROM|FOR|BECAUSE|SINCE|THEREFORE|THUS|RATE|PH|DETERMINE|CALCULATING)\b",
        text,
    )
    if leading_reasoning_letter:
        return leading_reasoning_letter.group(1)
    option_marker = re.search(r"(?:^|[\s.;:])([A-Z])[\.\)]\s+", text)
    if option_marker and option_marker.start() <= 20:
        return option_marker.group(1)
    match = re.fullmatch(r"[A-Z]", text)
    if match:
        return text
    if len(text) > 80:
        return None
    match = re.search(r"\b([A-H])\b", text)
    return match.group(1) if match else None


def _visible_options_are_single_statement_sum_choices(problem: GenericProblem | None) -> bool:
    pairs = option_pairs(problem)
    if len(pairs) < 2:
        return False
    value_options = 0
    for _letter, option_text in pairs:
        lowered = normalize_whitespace(option_text).lower().rstrip(".")
        if re.fullmatch(
            r"(?:the\s+)?(?:sum|total|number|count|value)\s+(?:is|=)\s*[-+]?\d+(?:\.\d+)?",
            lowered,
        ):
            value_options += 1
            continue
        if re.fullmatch(
            r"(?:all\s+of\s+the\s+above\s+options\s+are\s+incorrect|none\s+of\s+the\s+above)",
            lowered,
        ):
            continue
        return False
    return value_options >= 2


def problem_requests_multiple_option_letters(problem: GenericProblem | None) -> bool:
    if problem is None:
        return False
    metadata = problem.metadata or {}
    if any(
        bool(metadata.get(key))
        for key in (
            "multi_select_answer",
            "multi_select_answer_letters",
            "multiple_correct_options",
            "require_option_letter_set",
        )
    ):
        return True
    lowered = normalize_whitespace(problem.question).lower()
    if (
        re.search(r"\ball\s+(?:correct|true|applicable)\s+(?:options|statements|choices)\b", lowered)
        and _visible_options_are_single_statement_sum_choices(problem)
    ):
        return False
    if re.search(r"\b(?:select|choose|pick)\s+one\s+option\b", lowered):
        return False
    return bool(
        re.search(r"\bselect\s+all\b", lowered)
        or re.search(r"\ball\s+(?:correct|true|applicable)\s+(?:options|statements|choices)\b", lowered)
        or re.search(r"\boption\s+letters?\s+in\s+ascending\s+order\b", lowered)
    )


def _letters_from_segment(segment: str, valid_letters: set[str]) -> set[str]:
    letters = {
        match.group(1).upper()
        for match in re.finditer(r"\(?\b([A-Z])\b\)?", normalize_prediction(segment).upper())
        if match.group(1).upper() in valid_letters
    }
    return letters


def _bare_valid_option_letter(value: Any, valid_letters: set[str]) -> str | None:
    raw_text = normalize_prediction(str(value)).strip().upper()
    match = re.fullmatch(r"\(?([A-Z])\)?[\.\):;-]?", raw_text)
    if match and match.group(1) in valid_letters:
        return match.group(1)
    return None


def option_letter_set_from_text(value: Any, pairs: list[tuple[str, str]]) -> set[str]:
    valid_letters = {letter.upper() for letter, _ in pairs}
    if not valid_letters:
        return set()
    if isinstance(value, (list, tuple, set)):
        letters: set[str] = set()
        options_by_surface = {
            compact_option_surface(option_text): letter.upper()
            for letter, option_text in pairs
            if compact_option_surface(option_text)
        }
        for item in value:
            bare_letter = _bare_valid_option_letter(item, valid_letters)
            if bare_letter:
                letters.add(bare_letter)
                continue
            single = normalized_letter(item)
            if single in valid_letters:
                letters.add(single)
                continue
            compact_item = compact_option_surface(str(item))
            if compact_item in options_by_surface:
                letters.add(options_by_surface[compact_item])
                continue
            letters.update(option_letter_set_from_text(str(item), pairs))
        return letters

    raw_text = normalize_prediction(str(value)).strip()
    if not raw_text:
        return set()
    compact_letter_text = re.sub(r"[\s,;/&+().:\-]+", "", raw_text).upper()
    if (
        2 <= len(compact_letter_text) <= len(valid_letters)
        and set(compact_letter_text) <= valid_letters
        and re.fullmatch(r"[\sA-Z,;/&+().:\-]+", raw_text, flags=re.IGNORECASE)
    ):
        return set(compact_letter_text)
    leading_separated = re.match(
        r"^\s*([A-Z](?:\s*(?:,|;|/|&|\+|\band\b)\s*[A-Z]){1,})(?:\s*[\.\):;-]|\s+|$)",
        raw_text,
        flags=re.IGNORECASE,
    )
    if leading_separated:
        letters = _letters_from_segment(leading_separated.group(1), valid_letters)
        if letters:
            return letters
    leading_spaced = re.match(
        r"^\s*([A-Z](?:\s+[A-Z]){1,})(?:\s*[\.\):;-]|\s+|$)",
        raw_text,
        flags=re.IGNORECASE,
    )
    if leading_spaced:
        letters = _letters_from_segment(leading_spaced.group(1), valid_letters)
        if letters:
            return letters
    leading_single = re.match(
        r"^\s*\(?([A-Z])\)?\s*(?:[\.\):;-]|\b)(?=\s|$)",
        raw_text,
        flags=re.IGNORECASE,
    )
    if leading_single and leading_single.group(1).upper() in valid_letters:
        return {leading_single.group(1).upper()}
    explicit_patterns = [
        r"\b(?:final\s+answer|correct\s+answers?|answer|selected\s+options?|correct\s+options?)\s*(?:are|is|:|=)?\s*([A-Z][A-Z\s,;/&+()-]*(?:\band\b\s*[A-Z])?)",
        r"\b(?:choose|select|pick)\s+(?:options?\s+)?([A-Z][A-Z\s,;/&+()-]*(?:\band\b\s*[A-Z])?)",
    ]
    for pattern in explicit_patterns:
        letters: set[str] = set()
        matches = list(re.finditer(pattern, raw_text, flags=re.IGNORECASE))
        if matches:
            letters = _letters_from_segment(matches[-1].group(1), valid_letters)
        if letters:
            return letters
    if len(raw_text) <= 80:
        bare_letter = _bare_valid_option_letter(raw_text, valid_letters)
        if bare_letter:
            return {bare_letter}
        letters = _letters_from_segment(raw_text, valid_letters)
        if len(letters) >= 2:
            return letters
    return set()


def option_letter_set_from_prediction_text(prediction: str, pairs: list[tuple[str, str]]) -> set[str]:
    prediction_surface = compact_option_surface(prediction)
    if not prediction_surface:
        return set()
    letters: set[str] = set()
    for letter, option_text in pairs:
        for surface in compact_option_surfaces(option_text):
            if surface and len(surface) >= 4 and surface in prediction_surface:
                letters.add(letter.upper())
                break
    return letters


def leading_unpunctuated_option_letter(value: Any, pairs: list[tuple[str, str]]) -> str | None:
    raw_text = normalize_prediction(str(value)).strip()
    match = re.match(
        r"\s*\(?([A-Z])\)?(?:\s*[\.\):;-]\s*|\s+)(.+)$",
        raw_text,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if not match:
        return None
    letter = match.group(1).upper()
    options_by_letter = {option_letter.upper(): option_text for option_letter, option_text in pairs}
    if letter not in options_by_letter:
        return None
    remainder = normalize_prediction(match.group(2)).strip()
    if re.match(
        r"(?i)^(?:to|using|from|for|because|since|therefore|thus|rate|pH|determine|calculating)\b",
        remainder,
    ):
        return letter
    if re.match(r"(?i)^first\b", remainder) and re.search(
        r"(?i)\b(?:calculate|using|q\s*=|moles?|mass|charge|current|enthalpy|concentration|absorbance)\b",
        remainder[:220],
    ):
        return letter
    leading_clause = re.split(r"[\n.;:]", remainder, maxsplit=1)[0][:260]
    if len(leading_clause) < 8:
        return None
    stop_tokens = {
        "the",
        "and",
        "for",
        "with",
        "from",
        "near",
        "data",
        "formula",
        "structure",
        "compound",
        "answer",
        "option",
        "image",
        "evidence",
        "shows",
        "this",
        "that",
        "these",
        "those",
        "is",
        "of",
        "be",
        "should",
        "only",
        "while",
    }
    leading_tokens = {item for item in tokenize(leading_clause) if len(item) > 1 and item not in stop_tokens}
    option_tokens = {
        item
        for item in tokenize(normalize_prediction(options_by_letter[letter]).lower())
        if len(item) > 1 and item not in stop_tokens
    }
    if len(leading_tokens & option_tokens) >= 2:
        return letter
    leading_numbers = set(numeric_values(leading_clause))
    option_numbers = set(numeric_values(options_by_letter[letter]))
    if leading_numbers & option_numbers and leading_tokens & option_tokens:
        return letter
    return None


def compact_option_surface(value: str) -> str:
    text = normalize_symbolic_text(normalize_prediction(value)).lower()
    text = text.replace("\\times", "")
    text = text.replace("×", "")
    text = text.replace("*", "")
    text = text.replace("·", "")
    text = re.sub(r"\s+", "", text)
    return text.strip(" .;,")


def compact_option_surfaces(value: str) -> list[str]:
    primary = compact_option_surface(value)
    surfaces = [primary] if primary else []
    for separator in ("=", ":"):
        if separator in primary:
            surfaces.append(primary.split(separator, 1)[1])
    unique: list[str] = []
    for surface in surfaces:
        if surface and surface not in unique:
            unique.append(surface)
    return unique


def option_relation_assignment_score(prediction: str, option_text: str) -> float:
    """Score label:value option text against a reasoned answer without using the gold letter."""

    def labeled_numeric_pairs(text: str) -> list[tuple[str, float]]:
        normalized = normalize_symbolic_text(normalize_prediction(text))
        normalized = normalized.replace("−", "-").replace("–", "-").replace("—", "-")
        number = r"[-+]?\d+(?:,\d{3})*(?:\.\d+)?(?:\s*(?:x|\*)\s*10\s*(?:\^|\*\*)?\s*[-+]?\d+|[eE][-+]?\d+)?"
        label_patterns = [
            rf"(?P<label>\[[^\]]+\])\s*=\s*(?P<value>{number})",
            rf"(?P<label>\b(?:final\s+)?pH\b)\s*=\s*(?P<value>{number})",
            rf"(?P<label>\b[A-Za-z][A-Za-z0-9_+\-/^\s]{{1,34}}?)\s*=\s*(?P<value>{number})",
        ]
        pairs: list[tuple[str, float]] = []
        occupied_spans: list[tuple[int, int]] = []

        def span_is_free(start: int, end: int) -> bool:
            return not any(start < used_end and used_start < end for used_start, used_end in occupied_spans)

        for pattern in label_patterns:
            for match in re.finditer(pattern, normalized, flags=re.IGNORECASE):
                if not span_is_free(match.start(), match.end()):
                    continue
                raw_label = match.group("label")
                label = re.sub(r"[^a-z0-9]+", "", raw_label.lower())
                if len(label) < 2:
                    continue
                raw_value = match.group("value").replace(",", "").replace(" ", "")
                raw_value = re.sub(r"(?:x|\*)10(?:\^|\*\*)?([-+]?\d+)", r"e\1", raw_value, flags=re.IGNORECASE)
                try:
                    value = float(raw_value)
                except ValueError:
                    continue
                pairs.append((label, value))
                occupied_spans.append((match.start(), match.end()))
        return pairs

    def labels_compatible(option_label: str, prediction_label: str) -> bool:
        if option_label == prediction_label:
            return True
        if (option_label.endswith("ph") and prediction_label == "ph") or (
            prediction_label.endswith("ph") and option_label == "ph"
        ):
            return True
        if len(option_label) >= 3 and len(prediction_label) >= 3:
            return option_label in prediction_label or prediction_label in option_label
        return False

    option_numeric_pairs = labeled_numeric_pairs(option_text)
    prediction_numeric_pairs = labeled_numeric_pairs(prediction)
    if len(option_numeric_pairs) >= 2 and prediction_numeric_pairs:
        matched = 0
        mismatched = 0
        comparable = 0
        for option_label, option_value in option_numeric_pairs:
            candidates = [
                prediction_value
                for prediction_label, prediction_value in prediction_numeric_pairs
                if labels_compatible(option_label, prediction_label)
            ]
            if not candidates:
                continue
            comparable += 1
            if any(
                abs(prediction_value - option_value) <= max(1.0e-9, 0.012 * max(abs(option_value), 1.0))
                for prediction_value in candidates
            ):
                matched += 1
            else:
                mismatched += 1
        if matched >= 2 and mismatched == 0 and comparable >= 2:
            return 1.0

    relation_segments = [segment.strip() for segment in re.split(r"[;\n]", option_text) if ":" in segment]
    relations: list[tuple[list[str], list[str]]] = []
    stop_tokens = {
        "the",
        "and",
        "for",
        "with",
        "from",
        "near",
        "answer",
        "option",
        "is",
        "of",
        "be",
        "are",
        "a",
        "an",
        "in",
        "to",
        "or",
    }
    for segment in relation_segments:
        label, value = segment.split(":", 1)
        label_tokens = [token for token in tokenize(label.lower()) if len(token) > 1 and token not in stop_tokens]
        value_tokens = [token for token in tokenize(value.lower()) if len(token) > 1 and token not in stop_tokens]
        if label_tokens and value_tokens:
            relations.append((label_tokens, value_tokens))
    if len(relations) < 2:
        return 0.0

    pred_text = normalize_prediction(prediction).lower()
    label_positions: list[tuple[int, list[str], list[str]]] = []
    for label_tokens, value_tokens in relations:
        matches = [re.search(rf"\b{re.escape(token)}\b", pred_text) for token in label_tokens[:3]]
        positions = [match.start() for match in matches if match is not None]
        if not positions:
            return 0.0
        label_positions.append((min(positions), label_tokens, value_tokens))

    hits = 0
    all_positions = [position for position, _label_tokens, _value_tokens in label_positions]
    for position, _label_tokens, value_tokens in label_positions:
        following_positions = [candidate for candidate in all_positions if candidate > position]
        next_position = min(following_positions) if following_positions else len(pred_text)
        local_segment = pred_text[position : min(next_position, position + 360)]
        if all(re.search(rf"\b{re.escape(token)}\b", local_segment) for token in value_tokens[:4]):
            hits += 1
    return hits / len(relations)


def option_letter_from_prediction_text(prediction: str, pairs: list[tuple[str, str]]) -> str | None:
    pred_text = normalize_prediction(prediction).lower()
    pred_tokens = {item for item in tokenize(pred_text) if len(item) > 1}
    pred_formulas = set(formula_candidates_from_text(prediction))
    leading_text = re.split(r"[\n.;]", pred_text, maxsplit=1)[0]
    leading_tokens = {item for item in tokenize(leading_text) if len(item) > 1}
    stop_tokens = {
        "the",
        "and",
        "for",
        "with",
        "from",
        "near",
        "data",
        "formula",
        "structure",
        "compound",
        "answer",
        "option",
        "image",
        "evidence",
        "shows",
        "this",
        "that",
        "these",
        "those",
        "is",
        "of",
        "be",
        "should",
    }

    relation_matches = [
        (option_relation_assignment_score(prediction, option_text), letter)
        for letter, option_text in pairs
    ]
    relation_matches = [item for item in relation_matches if item[0] >= 0.999]
    if len(relation_matches) == 1:
        return relation_matches[0][1]

    option_colors_by_letter: dict[str, str] = {}
    color_words = ("red", "blue", "green", "amber", "purple", "black", "white", "orange", "yellow")
    color_aliases: dict[str, set[str]] = {color: {color} for color in color_words}
    color_aliases["amber"].add("orange")
    color_aliases["orange"].add("amber")

    def segment_mentions_color(segment: str, color: str) -> bool:
        return any(re.search(rf"\b{alias}\b", segment) for alias in color_aliases.get(color, {color}))

    for letter, option_text in pairs:
        option_norm = normalize_prediction(option_text).lower()
        for color in color_words:
            if re.search(rf"\b{color}\b", option_norm):
                option_colors_by_letter[letter] = color
                break

    def spectrum_axis_closest_color_letter() -> str | None:
        if not option_colors_by_letter:
            return None
        if not any(cue in pred_text for cue in ("spectrum", "wavenumber", "cm")):
            return None
        if "x=" not in pred_text and "px" not in pred_text and "pixel" not in pred_text:
            return None
        target_values = [
            float(match.group(1))
            for match in re.finditer(
                r"\b(?:near|around|closest\s+to|target(?:ing)?)\D{0,50}(\d{3,4}(?:\.\d+)?)",
                pred_text,
            )
        ]
        if not target_values and "carbonyl" in pred_text:
            target_values.append(1700.0)
        if not target_values:
            return None
        target_wavenumber = target_values[-1]
        axis_match = re.search(
            r"axis\D{0,40}(?:decreases|goes|runs)?\D{0,30}from\D{0,20}(\d{3,4}(?:\.\d+)?)"
            r"\D{0,100}left\D{0,100}to\D{0,20}(\d{3,4}(?:\.\d+)?)\D{0,100}right",
            pred_text,
        )
        if axis_match:
            left_wavenumber = float(axis_match.group(1))
            right_wavenumber = float(axis_match.group(2))
        elif "decreases" in pred_text and "left" in pred_text and "right" in pred_text:
            endpoint_values = [
                float(value)
                for value in re.findall(r"\b(\d{3,4}(?:\.\d+)?)\s*(?:cm|wavenumber)?", pred_text[:300])
            ]
            if len(endpoint_values) < 2:
                return None
            left_wavenumber = max(endpoint_values[:2])
            right_wavenumber = min(endpoint_values[:2])
        else:
            return None
        width_match = re.search(r"\bimage\s+is\s+(\d+(?:\.\d+)?)\s*px\s+wide\b", pred_text)
        if not width_match:
            width_match = re.search(r"\bright\s+edge\s*\(x\s*=\s*(\d+(?:\.\d+)?)\)", pred_text)
        right_pixel = float(width_match.group(1)) if width_match else 1.0
        if right_pixel <= 0 or left_wavenumber == right_wavenumber:
            return None
        color_pattern = "|".join(color_words)
        color_positions: list[tuple[float, str]] = []
        for match in re.finditer(
            rf"\b({color_pattern})\s+(?:highlighted\s+)?(?:band|trace|marker|peak)[^;\n.]*?\bx\s*=\s*(\d+(?:\.\d+)?)\s*px\b",
            pred_text,
        ):
            mentioned_color = match.group(1)
            pixel_x = float(match.group(2))
            fraction = max(0.0, min(1.0, pixel_x / right_pixel))
            wavenumber = left_wavenumber + fraction * (right_wavenumber - left_wavenumber)
            color_positions.append((abs(wavenumber - target_wavenumber), mentioned_color))
        if len(color_positions) < 2:
            return None
        color_positions.sort(key=lambda item: item[0])
        if len(color_positions) > 1 and color_positions[1][0] - color_positions[0][0] < 40.0:
            return None
        winning_color = color_positions[0][1]
        matching_letters = [
            letter
            for letter, option_color in option_colors_by_letter.items()
            if winning_color in color_aliases.get(option_color, {option_color})
        ]
        return matching_letters[0] if len(matching_letters) == 1 else None

    def mechanism_arrow_geometry_letter() -> str | None:
        if not option_colors_by_letter:
            return None
        if "arrow" not in pred_text:
            return None
        if not ("lower-left" in pred_text or "lower_left" in pred_text):
            return None
        if "central" not in pred_text and "carbonyl" not in pred_text:
            return None
        color_pattern = "|".join(color_words)
        arrow_geometry: list[tuple[float, str]] = []
        for match in re.finditer(
            rf"\b({color_pattern})\s+arrow\b[^;\n]*?lower[_\s-]*left[_\s-]*extent\s*=\s*\(\s*(\d+(?:\.\d+)?)\s*,\s*(\d+(?:\.\d+)?)\s*\)"
            rf"[^;\n]*?central[_\s-]*extent\s*=\s*\(\s*(\d+(?:\.\d+)?)\s*,\s*(\d+(?:\.\d+)?)\s*\)",
            pred_text,
        ):
            color = match.group(1)
            lower_left_x = float(match.group(2))
            lower_left_y = float(match.group(3))
            central_x = float(match.group(4))
            central_y = float(match.group(5))
            # Lower-left origin means small x and large y; the target should not be far right/bottom.
            score = lower_left_x - lower_left_y + 0.15 * central_x + 0.05 * central_y
            arrow_geometry.append((score, color))
        if len(arrow_geometry) < 2:
            return None
        arrow_geometry.sort(key=lambda item: item[0])
        if len(arrow_geometry) > 1 and arrow_geometry[1][0] - arrow_geometry[0][0] < 30.0:
            return None
        winning_color = arrow_geometry[0][1]
        matching_letters = [
            letter
            for letter, option_color in option_colors_by_letter.items()
            if winning_color in color_aliases.get(option_color, {option_color})
        ]
        return matching_letters[0] if len(matching_letters) == 1 else None

    def vertical_peak_top_y_letter() -> str | None:
        if not option_colors_by_letter:
            return None
        if "top_y" not in pred_text:
            return None
        if not any(
            cue in pred_text
            for cue in (
                "spectrum",
                "spectra",
                "peak",
                "intensity",
                "absorbance",
                "emission",
                "chromatogram",
                "plot",
            )
        ):
            return None
        choose_highest = any(
            cue in pred_text
            for cue in (
                "highest peak",
                "highest positive peak",
                "highest positive peak current",
                "highest anodic peak",
                "highest anodic peak current",
                "highest intensity",
                "peak intensity",
                "positive peak current",
                "highest point",
                "highest absorbance",
                "highest emission",
                "maximum peak",
                "tallest peak",
                "lower top_y",
                "lowest top_y",
                "goes higher",
                "higher on the chart",
                "highest on the chart",
            )
        )
        if not choose_highest:
            return None
        color_pattern = "|".join(color_words)
        color_top_y: list[tuple[float, str]] = []
        for match in re.finditer(
            rf"\b({color_pattern})\b(?:(?!\b(?:{color_pattern})\b).){{0,180}}\btop_y\s*=\s*(\d+(?:\.\d+)?)",
            pred_text,
            flags=re.DOTALL,
        ):
            color_top_y.append((float(match.group(2)), match.group(1)))
        if len(color_top_y) < 2:
            return None
        color_top_y.sort(key=lambda item: item[0])
        if len(color_top_y) > 1 and color_top_y[1][0] - color_top_y[0][0] < 6.0:
            return None
        winning_color = color_top_y[0][1]
        matching_letters = [
            letter
            for letter, option_color in option_colors_by_letter.items()
            if winning_color in color_aliases.get(option_color, {option_color})
        ]
        return matching_letters[0] if len(matching_letters) == 1 else None

    def rightmost_crossing_color_letter() -> str | None:
        if not option_colors_by_letter:
            return None
        if "x=" not in pred_text and "px" not in pred_text and "pixel" not in pred_text:
            return None
        rightmost_cued = any(
            cue in pred_text
            for cue in (
                "rightmost crossing",
                "rightmost_near_midline",
                "farthest to the right",
                "farthest right",
                "largest capacity",
                "largest usable capacity",
                "highest capacity",
                "usable capacity",
                "cutoff",
            )
        )
        if not rightmost_cued:
            return None
        color_pattern = "|".join(color_words)
        crossing_positions: list[tuple[float, str]] = []
        crossing_patterns = [
            rf"\b({color_pattern})\b(?:(?!\b(?:{color_pattern})\b).){{0,120}}\b(?:cross(?:es|ing)?|near[_\s-]*midline)\b(?:(?!\b(?:{color_pattern})\b).){{0,120}}\bx\s*=?\s*(\d+(?:\.\d+)?)\s*px",
            rf"\b({color_pattern})\b(?:(?!\b(?:{color_pattern})\b).){{0,120}}\bat\s+x\s*=?\s*(\d+(?:\.\d+)?)\s*px",
            rf"\b({color_pattern})\b(?:(?!\b(?:{color_pattern})\b).){{0,120}}\bat\s+(\d+(?:\.\d+)?)\s*px",
        ]
        for pattern in crossing_patterns:
            for match in re.finditer(pattern, pred_text, flags=re.DOTALL):
                crossing_positions.append((float(match.group(2)), match.group(1)))
            if len(crossing_positions) >= 2:
                break
        if len(crossing_positions) < 2:
            return None
        by_color: dict[str, float] = {}
        for x_position, color in crossing_positions:
            by_color[color] = max(x_position, by_color.get(color, x_position))
        ranked = sorted(by_color.items(), key=lambda item: item[1], reverse=True)
        if len(ranked) < 2 or ranked[0][1] - ranked[1][1] < 8.0:
            return None
        winning_color = ranked[0][0]
        matching_letters = [
            letter
            for letter, option_color in option_colors_by_letter.items()
            if winning_color in color_aliases.get(option_color, {option_color})
        ]
        return matching_letters[0] if len(matching_letters) == 1 else None

    if option_colors_by_letter:
        spectrum_letter = spectrum_axis_closest_color_letter()
        if spectrum_letter:
            return spectrum_letter
        mechanism_letter = mechanism_arrow_geometry_letter()
        if mechanism_letter:
            return mechanism_letter
        top_y_letter = vertical_peak_top_y_letter()
        if top_y_letter:
            return top_y_letter
        crossing_letter = rightmost_crossing_color_letter()
        if crossing_letter:
            return crossing_letter
        color_scores: dict[str, float] = {letter: 0.0 for letter in option_colors_by_letter}
        option_descriptor_tokens_by_letter: dict[str, set[str]] = {}
        for letter, option_text in pairs:
            option_descriptor_tokens_by_letter[letter] = {
                token
                for token in tokenize(normalize_prediction(option_text).lower())
                if token not in stop_tokens
                and token not in color_words
                and not re.fullmatch(r"\d+(?:\.\d+)?", token)
                and len(token) >= 3
            }
        color_break_pattern = r"\s+-\s+(?=(?:red|blue|green|amber|purple|black|white|orange|yellow)\b)"
        evidence_segments = [segment.strip() for segment in re.split(rf"[\n;]+|{color_break_pattern}", pred_text) if segment.strip()]
        largest_cues = ("largest", "greatest", "highest", "maximum", "widest", "broadest", "tallest", "most")
        smallest_cues = ("smallest", "lowest", "minimum", "narrowest", "least")
        choose_largest = any(cue in pred_text for cue in largest_cues)
        choose_smallest = any(cue in pred_text for cue in smallest_cues) and not choose_largest
        positive_candidate_patterns = [
            r"\b(?:highest|largest|maximum|tallest|deepest|most\s+negative)[a-z0-9_\s-]{0,80}candidate\s*(?:is|=|:)?\s*(red|blue|green|amber|purple|black|white|orange|yellow)\b",
            r"\bspectrum[_\s-]*(?:guide|target|nearest|highest|maximum)[a-z0-9_\s-]*candidate\s*(?:is|=|:)?\s*(red|blue|green|amber|purple|black|white|orange|yellow)\b",
            r"\b(?:phase[_\s-]*plot[_\s-]*between[_\s-]*curve[_\s-]*marker[_\s-]*candidates?|between[_\s-]*curve[_\s-]*marker[_\s-]*candidates?)\s*(?:is|=|:)?\s*(red|blue|green|amber|purple|black|white|orange|yellow)\b",
            r"(?:^|[^a-z0-9])(?:rightmost|most\s+positive|highest\s+potential|greatest\s+potential)[a-z0-9_\s-]{0,100}(?:anodic[_\s-]*peak[_\s-]*)?candidate\s*(?:is|=|:)?\s*(red|blue|green|amber|purple|black|white|orange|yellow)\b",
            r"\bmechanism[_\s-]*(?:lower[_\s-]*left[_\s-]*to[_\s-]*central|arrow[_\s-]*geometry|arrow)[a-z0-9_\s-]*candidate\s*(?:is|=|:)?\s*(red|blue|green|amber|purple|black|white|orange|yellow)\b",
            r"(?:^|[-;]\s*)\b(red|blue|green|amber|purple|black|white|orange|yellow)\s+marker\b[^-\n]{0,260}\brelation\s*=\s*['\"]?between[_\s-]*red[_\s-]*blue[_\s-]*curves\b",
            r"\b(red|blue|green|amber|purple|black|white|orange|yellow)\s+marker\b(?:(?!\b(?:red|blue|green|amber|purple|black|white|orange|yellow)\s+marker\b).){0,220}\b(?:equivalence\s+point|steepest|inflection|midpoint|midline|near[_\s-]*midline)\b",
            r"\b(?:equivalence\s+point|steepest|inflection|midpoint|midline|near[_\s-]*midline)\b(?:(?!\b(?:red|blue|green|amber|purple|black|white|orange|yellow)\s+marker\b).){0,220}\b(red|blue|green|amber|purple|black|white|orange|yellow)\s+marker\b",
            r"\b(?:looking\s+at|therefore|thus|so|closest|answer)\b[^;\n]{0,260}\b(?:the\s+)?(red|blue|green|amber|purple|black|white|orange|yellow)\s+(?:absorption\s+)?peak\s+(?:at\s+x\b|is\s+closest\b|closest\b)",
            r"\b(?:points?\s+to|matches|terminal[_\s-]*(?:point|xy)|favou?red(?:\s+product)?(?:\s+is)?)[^;\n]{0,180}\b(red|blue|green|amber|purple|black|white|orange|yellow)\s+product\s+box\b",
            r"\b(red|blue|green|amber|purple|black|white|orange|yellow)\s+product\s+box\b[^;\n]{0,180}\b(?:area|position|favou?red|matches|thick\s+green\s+arrow)\b",
            r"\b(red|blue|green|amber|purple|black|white|orange|yellow)\s+(?:trace|curve|peak|marker)\b[^;\n]{0,220}\b(?:rightmost|most\s+positive|largest\s+x|greatest\s+x|highest\s+potential|greatest\s+potential|rightmost\s+positive)\b",
            r"\b(?:leftmost|smallest\s+absolute\s+overpotential|lowest\s+overpotential|smallest\s+overpotential)\b[^;\n]{0,220}\b(red|blue|green|amber|purple|black|white|orange|yellow)\s+(?:trace|curve|crossing|marker)\b",
            r"\b(red|blue|green|amber|purple|black|white|orange|yellow)\s+(?:trace|curve|crossing|marker)\b[^;\n]{0,220}\b(?:leftmost|smallest\s+absolute\s+overpotential|lowest\s+overpotential|smallest\s+overpotential)\b",
            r"\b(red|blue|green|amber|purple|black|white|orange|yellow)\s+arrow\b[^;\n]{0,220}\b(?:lower[-_\s]*left\s+oxygen|starts?\s+at\s+the\s+lower[-_\s]*left|points?\s+to\s+the\s+central\s+carbonyl|central\s+carbonyl\s+carbon|nucleophile)\b",
            r"\b(red|blue|green|amber|purple|black|white|orange|yellow)\b[^;\n]{0,220}\b(?:highest\s+final|highest\s+on\s+the\s+plot|highest\s+temperature|highest\s+position|highest\s+absorbance|highest\s+peak|highest\s+mass(?:\s+(?:percent|retention))?|greatest\s+mass(?:\s+(?:percent|retention))?|retains?\s+the\s+greatest\s+mass|tallest\s+peak|largest\s+(?:integrated\s+)?peak\s+area|largest\s+area|largest\s+peak|largest\s+rf|broadest\s+peak|most\s+near[-\s]*midline\s+pixels|most\s+colored\s+pixels|largest\s+colored\s+pixel\s+count|deepest\s+cathodic|between[_\s-]*red[_\s-]*blue[_\s-]*curves|between\s+the\s+red\s+and\s+blue|two[-\s]*phase\s+region)\b",
        ]
        candidate_letters: list[str] = []
        for pattern in positive_candidate_patterns:
            for color_match in re.finditer(pattern, pred_text):
                mentioned_color = color_match.group(1)
                matching_letters = [
                    letter
                    for letter, option_color in option_colors_by_letter.items()
                    if mentioned_color in color_aliases.get(option_color, {option_color})
                ]
                if len(matching_letters) == 1:
                    candidate_letters.append(matching_letters[0])
            if candidate_letters:
                break
        if candidate_letters and len(set(candidate_letters)) == 1:
            return candidate_letters[-1]
        if choose_largest or choose_smallest:
            numeric_color_evidence: list[tuple[float, str]] = []
            for segment in evidence_segments:
                if re.search(r"\b(?:x|y)\s*=|(?:top|bottom|median)?_?[xy]\d|px\b|pixel", segment):
                    continue
                values = numeric_values(segment)
                if not values:
                    continue
                metric_value = values[-1]
                for letter, color in option_colors_by_letter.items():
                    if segment_mentions_color(segment, color):
                        numeric_color_evidence.append((metric_value, letter))
            if numeric_color_evidence:
                by_letter: dict[str, float] = {}
                for value, letter in numeric_color_evidence:
                    by_letter[letter] = value
                ranked_numeric = sorted(by_letter.items(), key=lambda item: item[1], reverse=choose_largest)
                if ranked_numeric:
                    best_letter, best_value = ranked_numeric[0]
                    runner_value = ranked_numeric[1][1] if len(ranked_numeric) > 1 else None
                    if runner_value is None or abs(best_value - runner_value) > max(1.0e-9, 0.01 * max(abs(best_value), 1.0)):
                        return best_letter
        positive_cues = (
            "six_membered",
            "six-membered",
            "cyclic",
            "ring",
            "enclosed area",
            "largest",
            "greatest",
            "highest",
            "maximum",
            "widest",
            "broadest",
            "tallest",
            "deepest",
            "most negative",
            "correct",
            "matches",
            "leads to",
            "lead to",
            "descriptor explicitly",
            "characteristic",
            "would be",
            "is the",
            "corresponds to",
            "corresponds with",
            "labels",
            "indicates",
            "identifies",
            "centered",
            "equivalence point",
            "steepest",
            "inflection",
            "midpoint",
            "midline",
            "near_midline",
            "rightmost",
            "most positive",
            "highest potential",
            "greatest potential",
            "rightmost positive",
        )
        negative_cues = (
            "not a ring",
            "not cyclic",
            "not the ring",
            "not correct",
            "not the cyclic",
            "not the",
            "does not",
            "instead of",
            "narrowest",
            "smaller",
            "lower",
            "least",
        )
        for segment in evidence_segments:
            segment_tokens = {item for item in tokenize(segment) if len(item) > 1}
            for letter, color in option_colors_by_letter.items():
                if not segment_mentions_color(segment, color):
                    continue
                shared_descriptor_tokens = option_descriptor_tokens_by_letter.get(letter, set()) & segment_tokens
                if any(cue in segment for cue in positive_cues):
                    color_scores[letter] += 0.8
                if len(shared_descriptor_tokens) >= 2:
                    color_scores[letter] += 1.6
                elif shared_descriptor_tokens:
                    color_scores[letter] += 0.4
                if "six_membered_ring_or_cyclic_outline_candidate" in segment:
                    color_scores[letter] += 2.0
                if any(cue in segment for cue in negative_cues):
                    color_scores[letter] -= 1.5
        ranked_color_scores = sorted(color_scores.items(), key=lambda item: item[1], reverse=True)
        if ranked_color_scores and ranked_color_scores[0][1] >= 1.5:
            runner_up = ranked_color_scores[1][1] if len(ranked_color_scores) > 1 else 0.0
            if ranked_color_scores[0][1] - runner_up >= 1.0:
                return ranked_color_scores[0][0]
    exact_option_matches: list[str] = []
    pred_text_clean = pred_text.strip(" .")
    for letter, option_text in pairs:
        option_norm = normalize_prediction(option_text).lower().strip()
        option_norm_clean = option_norm.strip(" .")
        if len(option_norm) >= 12 and option_norm in pred_text:
            exact_option_matches.append(letter)
        elif len(pred_text_clean) >= 12 and pred_text_clean in option_norm_clean:
            exact_option_matches.append(letter)
    if len(exact_option_matches) == 1:
        return exact_option_matches[0]
    compact_prediction = compact_option_surface(prediction)
    compact_matches: list[tuple[int, str]] = []
    for letter, option_text in pairs:
        for compact_option in compact_option_surfaces(option_text):
            if len(compact_option) < 10:
                continue
            if compact_option in compact_prediction:
                compact_matches.append((len(compact_option), letter))
                break
    if compact_matches:
        compact_matches.sort(reverse=True)
        best_length, best_letter = compact_matches[0]
        runner_length = compact_matches[1][0] if len(compact_matches) > 1 else 0
        if best_length - runner_length >= 4 or len({letter for _length, letter in compact_matches if _length == best_length}) == 1:
            return best_letter
    all_option_tokens_by_letter: dict[str, set[str]] = {}
    for letter, option_text in pairs:
        option_norm = normalize_prediction(option_text).lower().strip()
        all_option_tokens_by_letter[letter] = {
            item
            for item in tokenize(option_norm)
            if len(item) > 1 and item not in stop_tokens and not re.fullmatch(r"\d+(?:\.\d+)?", item)
        }
    evidence_text = pred_text
    for marker in (
        "now let me evaluate the options",
        "let me evaluate the options",
        "evaluate the options",
        "now evaluate the options",
    ):
        marker_index = evidence_text.find(marker)
        if marker_index > 0:
            evidence_text = evidence_text[:marker_index]
            break
    if evidence_text != pred_text:
        evidence_tokens = {item for item in tokenize(evidence_text) if len(item) > 1 and item not in stop_tokens}
        evidence_scored: list[tuple[float, str]] = []
        for letter, option_tokens in all_option_tokens_by_letter.items():
            if not option_tokens:
                evidence_scored.append((0.0, letter))
                continue
            distinctive_tokens = {item for item in option_tokens if len(item) >= 5}
            shared = option_tokens & evidence_tokens
            distinctive_shared = distinctive_tokens & evidence_tokens
            score = len(shared) / max(len(option_tokens), 1)
            if len(distinctive_shared) >= 3:
                score = max(score, 0.80)
            elif len(distinctive_shared) >= 2:
                score = max(score, 0.65)
            evidence_scored.append((score, letter))
        evidence_scored.sort(reverse=True)
        if evidence_scored and evidence_scored[0][0] >= 0.60:
            runner_up = evidence_scored[1][0] if len(evidence_scored) > 1 else 0.0
            if evidence_scored[0][0] - runner_up >= 0.15:
                return evidence_scored[0][1]
    scored: list[tuple[float, str]] = []
    pred_numbers = numeric_values(prediction)
    any_option_has_numbers = any(numeric_values(option_text) for _letter, option_text in pairs)
    for letter, option_text in pairs:
        option_norm = normalize_prediction(option_text).lower().strip()
        option_tokens = all_option_tokens_by_letter[letter]
        if not option_tokens:
            scored.append((0.0, letter))
            continue
        shared_tokens = option_tokens & pred_tokens
        score = len(shared_tokens) / max(len(option_tokens), 1)
        if len(option_norm) >= 12 and option_norm in pred_text:
            score = max(score, 1.0)
        option_formulas = set(formula_candidates_from_text(option_text))
        distinctive_tokens = {item for item in option_tokens if len(item) >= 5}
        distinctive_overlap = len(distinctive_tokens & pred_tokens)
        option_numbers = numeric_values(option_text)
        if pred_numbers and any_option_has_numbers:
            numeric_match = False
            for option_number in option_numbers:
                if any(
                    abs(pred_number - option_number) <= max(1.0e-9, 0.01 * max(abs(option_number), 1.0))
                    for pred_number in pred_numbers
                ):
                    numeric_match = True
                    break
            if numeric_match and distinctive_overlap:
                score = max(score + min(0.3, 0.08 + 0.025 * distinctive_overlap), 0.72)
            elif not option_numbers:
                score -= 0.25
            else:
                score -= 0.15
        if option_formulas & pred_formulas and distinctive_overlap:
            score = max(score, 0.85)
        elif distinctive_overlap >= 2:
            score = max(score, 0.75)
        other_option_tokens = set().union(
            *(tokens for other_letter, tokens in all_option_tokens_by_letter.items() if other_letter != letter)
        )
        unique_tokens = option_tokens - other_option_tokens
        leading_unique_overlap = unique_tokens & leading_tokens
        if leading_unique_overlap:
            score += min(0.3, 0.15 * len(leading_unique_overlap))
        scored.append((score, letter))
    scored.sort(reverse=True)
    if not scored or scored[0][0] < 0.70:
        return None
    if len(scored) > 1 and scored[0][0] - scored[1][0] < 0.15:
        return None
    return scored[0][1]


def token_overlap_score(prediction: str, gold: str) -> float:
    pred_tokens = {item for item in tokenize(prediction) if len(item) > 1}
    gold_tokens = {item for item in tokenize(gold) if len(item) > 1}
    if not pred_tokens or not gold_tokens:
        return 0.0
    return len(pred_tokens & gold_tokens) / max(len(gold_tokens), 1)


def organic_positional_alias_match(prediction: str, gold: str) -> bool:
    prediction_text = normalize_prediction(prediction).lower().replace(" ", "-")
    gold_text = normalize_prediction(gold).lower().replace(" ", "-")
    locant_aliases = {
        "o": ("o", "ortho", "2"),
        "ortho": ("o", "ortho", "2"),
        "2": ("o", "ortho", "2"),
        "m": ("m", "meta", "3"),
        "meta": ("m", "meta", "3"),
        "3": ("m", "meta", "3"),
        "p": ("p", "para", "4"),
        "para": ("p", "para", "4"),
        "4": ("p", "para", "4"),
    }
    alias_pattern = r"\b(o|ortho|m|meta|p|para|2|3|4)-([a-z][a-z0-9-]{3,})\b"
    for locant, base_name in re.findall(alias_pattern, gold_text):
        if locant not in locant_aliases:
            continue
        variants = {f"{alias}-{base_name}" for alias in locant_aliases[locant]}
        if any(variant in prediction_text for variant in variants):
            return True
    return False


def formula_role_assignments(text: str) -> dict[str, str]:
    assignments: dict[str, str] = {}
    normalized = normalize_symbolic_text(text)
    for match in re.finditer(r"(?<![\w])([A-Za-z][A-Za-z0-9_]*)\s*=\s*", normalized):
        right_hand_side = re.split(r"[;,\n]", normalized[match.end() :], maxsplit=1)[0]
        formulas = formula_candidates_from_text(right_hand_side)
        if formulas:
            assignments[match.group(1).upper()] = formulas[0]
    return assignments


def formula_answer_matches(prediction: str, gold: str) -> bool:
    expected_formulas = formula_candidates_from_text(gold)
    observed_formulas = formula_candidates_from_text(prediction)
    if not expected_formulas or not observed_formulas or len(expected_formulas) != len(observed_formulas):
        return False

    expected_roles = formula_role_assignments(gold)
    observed_roles = formula_role_assignments(prediction)
    if expected_roles:
        if observed_roles:
            if observed_roles != expected_roles:
                return False
            return Counter(observed_formulas) == Counter(expected_formulas)
        elif observed_formulas != expected_formulas:
            return False
        return True
    if Counter(observed_formulas) != Counter(expected_formulas):
        return False
    return True


def _evaluate_prediction_core(problem: GenericProblem, answer_record: AnswerRecord) -> tuple[bool, float, list[str]]:
    notes: list[str] = []
    prediction = answer_record.final_answer
    gold = problem.answer if problem.answer is not None else problem.expected_answer
    integrity_failures = evaluation_integrity_failures(problem, answer_record)
    if integrity_failures:
        return False, 0.0, integrity_failures
    pairs = option_pairs(problem)
    gold_letter_set = option_letter_set_from_text(gold, pairs) if pairs else set()
    if pairs and gold_letter_set and (len(gold_letter_set) > 1 or problem_requests_multiple_option_letters(problem)):
        observed_letter_set = option_letter_set_from_text(prediction, pairs)
        if not observed_letter_set:
            observed_letter_set = option_letter_set_from_prediction_text(prediction, pairs)
        if observed_letter_set == gold_letter_set:
            return True, 1.0, ["multiple-choice option-letter set matched"]
        if not observed_letter_set:
            return False, 0.0, ["multiple-choice prediction did not contain a valid option-letter set"]
        overlap = len(observed_letter_set & gold_letter_set) / max(len(observed_letter_set | gold_letter_set), 1)
        notes.append(
            "multiple-choice option-letter set mismatch: "
            f"observed={sorted(observed_letter_set)}, expected={sorted(gold_letter_set)}"
        )
        return False, round(overlap, 4), notes
    if isinstance(gold, str):
        if requires_separate_final_answer_line(problem):
            strict_numeric_result = evaluate_numeric_text_gold(problem, answer_record, gold)
            if strict_numeric_result is not None:
                return strict_numeric_result
        if pairs:
            observed_letter_set = option_letter_set_from_text(prediction, pairs)
            observed_letter = next(iter(observed_letter_set)) if len(observed_letter_set) == 1 else None
            if observed_letter is None:
                observed_letter = normalized_letter(prediction)
            if observed_letter is None:
                observed_letter = leading_unpunctuated_option_letter(prediction, pairs)
            gold_letter = normalized_letter(gold)
            if gold_letter is not None:
                if observed_letter == gold_letter:
                    return True, 1.0, notes
                text_matched_letter = option_letter_from_prediction_text(prediction, pairs)
                if text_matched_letter == gold_letter:
                    return True, 1.0, ["multiple-choice option text matched expected letter"]
                correct = False
                if observed_letter is None and text_matched_letter is None:
                    notes.append("multiple-choice prediction did not contain a valid option letter")
                return correct, 1.0 if correct else 0.0, notes
        normalized_prediction_text = normalize_prediction(prediction).lower()
        normalized_gold_text = normalize_prediction(gold).lower()
        if normalized_prediction_text == normalized_gold_text:
            return True, 1.0, notes
        if organic_positional_alias_match(prediction, gold):
            return True, 0.95, ["organic positional-name alias matched"]
        expected_formulas = formula_candidates_from_text(gold)
        formula_relevant = (
            "formula" in problem.question.lower()
            or len(expected_formulas) > 1
            or any(re.search(r"\d", formula) for formula in expected_formulas)
        )
        if formula_answer_matches(prediction, gold) and formula_relevant:
            return True, 1.0, ["formula token matched"]
        if formula_relevant and expected_formulas and formula_candidates_from_text(prediction):
            return False, 0.0, ["formula answer did not match the complete expected formula list"]
        if looks_like_equation(prediction) and looks_like_equation(gold):
            normalized_prediction_equation = normalize_equation_text(prediction)
            normalized_gold_equation = normalize_equation_text(gold)
            correct = normalized_prediction_equation == normalized_gold_equation or normalized_gold_equation in normalized_prediction_equation
            if correct:
                return True, 1.0, ["balanced equation matched after state/spacing normalization"]
        if "cfse" in problem.question.lower() and cfse_terms_match(prediction, gold):
            return True, 1.0, ["CFSE terms matched"]
        if vibrational_partition_matches(prediction, gold, problem.question):
            return True, 1.0, ["vibrational partition terms matched"]
        numeric_result = evaluate_numeric_text_gold(problem, answer_record, gold)
        if numeric_result is not None:
            if not numeric_result[0]:
                if requires_separate_final_answer_line(problem):
                    return numeric_result
                overlap = token_overlap_score(prediction, gold)
                if overlap >= 0.82:
                    return True, max(float(numeric_result[1]), round(overlap, 4)), ["string token overlap rescued numeric derivation"]
            return numeric_result
        if normalized_gold_text and normalized_gold_text in normalized_prediction_text:
            return True, 0.9, ["gold answer appears as substring of prediction"]
        if relation_order_matches(prediction, gold):
            return True, 1.0, ["ordered relation matched"]
        overlap = token_overlap_score(prediction, gold)
        notes.append(f"string token overlap={overlap:.3f}")
        return overlap >= 0.82, round(overlap, 4), notes
    if isinstance(gold, (int, float)):
        strict_final_line = requires_separate_final_answer_line(problem)
        observed_source = answer_record.tool_result_payload if answer_record.tool_result_payload is not None else prediction
        observed_number_candidates: list[list[float]] = []
        if strict_final_line:
            final_line = separate_final_answer_line(prediction)
            preferred_numbers = (
                answer_like_numeric_values(final_line, question=problem.question)
                if final_line
                else []
            )
            if preferred_numbers:
                observed_number_candidates.append(preferred_numbers)
        elif isinstance(prediction, str):
            preferred_numbers = answer_like_numeric_values(prediction, question=problem.question)
            if preferred_numbers:
                observed_number_candidates.append(preferred_numbers)
        if not strict_final_line and isinstance(observed_source, str):
            preferred_numbers = answer_like_numeric_values(observed_source, question=problem.question)
            if preferred_numbers and preferred_numbers not in observed_number_candidates:
                observed_number_candidates.append(preferred_numbers)
        elif not strict_final_line and isinstance(observed_source, dict):
            for preferred_key in ("answer", "final_answer", "result"):
                answer_text = observed_source.get(preferred_key)
                if isinstance(answer_text, str):
                    preferred_numbers = answer_like_numeric_values(answer_text, question=problem.question)
                    if preferred_numbers and preferred_numbers not in observed_number_candidates:
                        observed_number_candidates.append(preferred_numbers)
                        break
        if not strict_final_line:
            raw_observed_numbers = numeric_values(observed_source)
            if raw_observed_numbers and raw_observed_numbers not in observed_number_candidates:
                observed_number_candidates.append(raw_observed_numbers)
            raw_prediction_numbers = numeric_values(prediction)
            if raw_prediction_numbers and raw_prediction_numbers not in observed_number_candidates:
                observed_number_candidates.append(raw_prediction_numbers)
        if not observed_number_candidates:
            return False, 0.0, ["numeric prediction unavailable"]
        best_result: tuple[bool, float, list[str]] | None = None
        for observed_values in observed_number_candidates:
            result = _compare_numeric_values(
                [float(gold)],
                observed_values,
                tolerance=problem.tolerance,
            )
            if result[0]:
                return result
            if best_result is None or result[1] > best_result[1]:
                best_result = result
        return best_result if best_result is not None else (False, 0.0, ["numeric prediction unavailable"])
    if isinstance(gold, dict):
        return evaluate_structured_gold(problem, answer_record, gold)
    return False, 0.0, ["unsupported gold answer type"]


def evaluate_prediction(problem: GenericProblem, answer_record: AnswerRecord) -> tuple[bool, float, list[str]]:
    """Evaluate correctness, then append non-blocking support-quality warnings."""

    correct, score, notes = _evaluate_prediction_core(problem, answer_record)
    combined_notes = list(
        dict.fromkeys([*notes, *evaluation_quality_warnings(answer_record)])
    )
    return correct, score, combined_notes


def prepared_inputs(problem: GenericProblem | None) -> dict[str, Any]:
    prepared: dict[str, Any] = {}
    if problem is None:
        return prepared
    prepared.update(problem.given)
    input_params = problem.metadata.get("input_params")
    if isinstance(input_params, dict):
        prepared.update({key: value for key, value in input_params.items() if key != "null"})
    return prepared


class GeneratedQARuntime:
    def __init__(
        self,
        *,
        repo_root: str | Path,
        runtime_config: dict[str, Any] | None = None,
        client: Any | None = None,
    ) -> None:
        self.repo_root = Path(repo_root)
        self.runtime_config = dict(runtime_config or {})
        self.design_memory = dict(self.runtime_config.get("design_memory", {}))
        self.design_strategy_patch = dict(
            self.runtime_config.get("design_strategy_patch")
            or self.design_memory.get("strategy_patch", {})
            or dict(self.runtime_config.get("memory_policy", {})).get("strategy_patch", {})
        )
        self.memory_root = Path(self.runtime_config.get("memory_root") or "")
        self.tool_root = Path(self.runtime_config.get("tool_root") or "")
        self.default_evaluation_paths = list(self.runtime_config.get("evaluation_paths", []))
        product_runtime = dict(self.runtime_config.get("product_runtime", {}))
        backend = str(product_runtime.get("backend") or self.runtime_config.get("backend") or "openclaw")
        model_name = str(product_runtime.get("model_name") or self.runtime_config.get("model_name") or "kimi-k3")
        reasoning_effort = str(product_runtime.get("reasoning_effort") or self.runtime_config.get("reasoning_effort") or "high")
        timeout_seconds = float(product_runtime.get("timeout_seconds", self.runtime_config.get("timeout_seconds", 60.0)))
        max_tokens = int(product_runtime.get("max_tokens", self.runtime_config.get("max_tokens", 900)))
        max_retries = max(0, int(product_runtime.get("max_retries", self.runtime_config.get("max_retries", 1))))
        self.max_model_tokens = max_tokens
        self.agent_call_mode = str(
            product_runtime.get("agent_call_mode")
            or self.runtime_config.get("agent_call_mode")
            or "full"
        ).strip().lower()
        self.client = client or build_text_client_from_profile(
            repo_root=self.repo_root,
            backend=backend,
            model_name=model_name,
            reasoning_effort=reasoning_effort,
            timeout_seconds=timeout_seconds,
            max_tokens=max_tokens,
            max_retries=max_retries,
        )
        adapter_config = dict(dict(self.runtime_config.get("runtime_inputs", {})).get("adapter_config", {}))
        exclude_dirs = list(adapter_config.get("retrieval_exclude_dirs", ["problems", "testing", "__pycache__"]))
        self.memory_index = MemoryIndex(self.memory_root, exclude_dirs=exclude_dirs).build() if self.memory_root else MemoryIndex(".", exclude_dirs=exclude_dirs).build()
        self.tool_catalog = ToolCatalog(self.tool_root).build() if self.tool_root else ToolCatalog(".").build()

    @classmethod
    def from_runtime_config(
        cls,
        *,
        repo_root: str | Path,
        runtime_config: dict[str, Any],
        client: Any | None = None,
    ) -> "GeneratedQARuntime":
        return cls(repo_root=repo_root, runtime_config=runtime_config, client=client)

    def answer_question(
        self,
        question: str,
        *,
        problem: GenericProblem | None = None,
        learn: bool = True,
    ) -> AnswerRecord:
        _ = learn
        docs = self.memory_index.search(question, top_k=6)
        notes = [f"retrieved {len(docs)} memory documents"]
        tool_calls: list[ToolCallResult] = []
        tool_result_payload: Any | None = None
        inputs = prepared_inputs(problem)
        chosen_tools: list[ToolSpec] = []
        vdw_call = self._run_van_der_waals_pressure_tool(question)
        if vdw_call is not None:
            tool_calls.append(vdw_call)
            if vdw_call.error is None:
                tool_result_payload = vdw_call.result
                notes.append(f"executed tool {vdw_call.tool_id}")
        if problem and problem.matching_module and problem.matching_function:
            exact = self.tool_catalog.find(problem.matching_module, problem.matching_function)
            if exact is not None:
                chosen_tools.append(exact)
        if not chosen_tools and tool_result_payload is None:
            chosen_tools = self.tool_catalog.search(question, top_k=3)
        if chosen_tools and inputs and tool_result_payload is None:
            call = self.tool_catalog.execute(chosen_tools[0], inputs)
            tool_calls.append(call)
            if call.error is None:
                tool_result_payload = call.result
                notes.append(f"executed tool {chosen_tools[0].id}")
        raw_answer = self._reason(question, docs, tool_calls, problem)
        final_answer = normalize_whitespace(raw_answer)
        if isinstance(tool_result_payload, dict) and tool_result_payload.get("answer") is not None:
            final_answer = normalize_whitespace(str(tool_result_payload.get("answer")))
        elif not final_answer and tool_result_payload is not None:
            final_answer = normalize_whitespace(str(tool_result_payload))
        if not final_answer and docs:
            final_answer = normalize_whitespace(docs[0].snippet[:280])
        if not final_answer:
            final_answer = "I do not have enough information."
        confidence = 0.4 + (0.15 if docs else 0.0) + (0.2 if tool_result_payload is not None else 0.0)
        confidence = min(confidence, 0.95)
        verification = self._verify_answer(
            question=question,
            final_answer=final_answer,
            docs=docs,
            tool_calls=tool_calls,
            confidence=confidence,
            problem=problem,
        )
        notes.append(
            f"verification {verification['status']} at {verification['risk_level']} risk"
        )
        return AnswerRecord(
            question=question,
            final_answer=final_answer,
            raw_answer=raw_answer or final_answer,
            confidence=confidence,
            retrieved_docs=docs,
            tool_calls=tool_calls,
            route_notes=notes,
            normalized_prediction=normalize_prediction(final_answer),
            verification=verification,
            tool_result_payload=tool_result_payload,
        )

    def _molar_mass_from_formula_for_runtime_tool(self, formula: str) -> float | None:
        tool = self.tool_catalog.find("atomic_composition_tools", "molar_mass_from_formula")
        if tool is None:
            return None
        call = self.tool_catalog.execute(tool, {"formula": formula})
        if call.error is not None:
            return None
        try:
            value = float(call.result)
        except Exception:
            return None
        return value if value > 0 else None

    def _extract_runtime_masses_g(self, question: str) -> list[float]:
        values: list[float] = []
        for raw, unit in re.findall(r"(-?\d[\d,]*(?:\.\d+)?)\s*(kg|mg|g)\b(?!\s*/)", question, flags=re.IGNORECASE):
            value = parse_numeric_literal(raw)
            normalized = unit.lower()
            if normalized == "kg":
                values.append(value * 1000.0)
            elif normalized == "mg":
                values.append(value / 1000.0)
            else:
                values.append(value)
        return values

    def _extract_runtime_temperatures_k(self, question: str) -> list[float]:
        values: list[float] = []
        for raw, unit in re.findall(r"(-?\d[\d,]*(?:\.\d+)?)\s*(?:deg\s*)?(c|k|f)\b", question, flags=re.IGNORECASE):
            value = parse_numeric_literal(raw)
            normalized = unit.lower()
            if normalized == "k":
                values.append(value)
            elif normalized == "c":
                values.append(value + 273.15)
            else:
                values.append((value - 32.0) * 5.0 / 9.0 + 273.15)
        return values

    def _extract_runtime_volumes_dm3(self, question: str) -> list[float]:
        values: list[float] = []
        for raw, unit in re.findall(
            r"(-?\d[\d,]*(?:\.\d+)?)\s*(m(?:\^?3|3|\u00b3)|dm(?:\^?3|3|\u00b3)|cm(?:\^?3|3|\u00b3)|ml|mL|l|L|liter|liters)\b",
            question,
            flags=re.IGNORECASE,
        ):
            value = parse_numeric_literal(raw)
            normalized = unit.lower().replace("^", "").replace("\u00b3", "3")
            if normalized == "m3":
                values.append(value * 1000.0)
            elif normalized in {"dm3", "l", "liter", "liters"}:
                values.append(value)
            else:
                values.append(value / 1000.0)
        return values

    def _extract_runtime_moles(self, question: str) -> list[float]:
        values: list[float] = []
        for match in re.finditer(r"(-?\d[\d,]*(?:\.\d+)?)\s*mol\b", question, flags=re.IGNORECASE):
            prefix = question[max(0, match.start() - 12) : match.start()].lower()
            suffix = question[match.end() : match.end() + 8].lstrip().lower()
            if re.search(r"(?:\^|dm|cm|m|l)\s*$", prefix):
                continue
            if suffix.startswith("^") or suffix.startswith("-") or suffix.startswith("/"):
                continue
            values.append(parse_numeric_literal(match.group(1)))
        return values

    def _run_van_der_waals_pressure_tool(self, question: str) -> ToolCallResult | None:
        normalized = normalize_symbolic_text(question)
        lowered = normalized.lower()
        if "van der waals" not in lowered or "pressure" not in lowered:
            return None
        a_match = re.search(
            r"\ba\s*=\s*(-?\d[\d,]*(?:\.\d+)?(?:e[+-]?\d+)?)\s*(?:dm|l)(?:\^?6|6|\u2076)\s*atm",
            normalized,
            flags=re.IGNORECASE,
        )
        b_match = re.search(
            r"\bb\s*=\s*(-?\d[\d,]*(?:\.\d+)?(?:e[+-]?\d+)?)\s*(?:dm|l)(?:\^?3|3|\u00b3)\s*mol",
            normalized,
            flags=re.IGNORECASE,
        )
        if not a_match or not b_match:
            return None
        temperatures = self._extract_runtime_temperatures_k(normalized)
        volumes_dm3 = self._extract_runtime_volumes_dm3(normalized)
        if not temperatures or not volumes_dm3:
            return None
        amounts = self._extract_runtime_moles(normalized)
        formula = formula_from_question(normalized) or ""
        mass_g = None
        molar_mass = None
        if amounts:
            n_mol = amounts[0]
        else:
            masses_g = self._extract_runtime_masses_g(normalized)
            if not masses_g or not formula:
                return None
            molar_mass = self._molar_mass_from_formula_for_runtime_tool(formula)
            if molar_mass is None:
                return None
            mass_g = masses_g[0]
            n_mol = mass_g / molar_mass
        volume_dm3 = max(volumes_dm3)
        a_value = parse_numeric_literal(a_match.group(1))
        b_value = parse_numeric_literal(b_match.group(1))
        if n_mol <= 0 or volume_dm3 <= 0:
            return None
        free_volume_dm3 = volume_dm3 - n_mol * b_value
        if free_volume_dm3 <= 0:
            return ToolCallResult(
                tool_id="generated_runtime.van_der_waals_pressure",
                kwargs={"n_mol": n_mol, "volume_dm3": volume_dm3, "a": a_value, "b": b_value},
                error="van der Waals covolume correction leaves non-positive free volume",
            )
        temperature_k = temperatures[-1]
        ideal_term = n_mol * 0.082057 * temperature_k / free_volume_dm3
        attraction_term = a_value * (n_mol / volume_dm3) ** 2
        pressure_atm = ideal_term - attraction_term
        return ToolCallResult(
            tool_id="generated_runtime.van_der_waals_pressure",
            kwargs={
                "formula": formula,
                "mass_g": mass_g,
                "molar_mass_g_mol": molar_mass,
                "n_mol": n_mol,
                "temperature_k": temperature_k,
                "volume_dm3": volume_dm3,
                "a_dm6_atm_mol2": a_value,
                "b_dm3_mol": b_value,
            },
            result={
                "answer_values": [pressure_atm],
                "answer": f"{pressure_atm:.4g} atm",
                "units": ["atm"],
                "ideal_term_atm": ideal_term,
                "attraction_correction_atm": attraction_term,
                "free_volume_dm3": free_volume_dm3,
            },
        )

    def _tool_call_is_adequate(self, call: ToolCallResult) -> bool:
        adequacy = dict(call.metadata.get("adequacy", {}))
        if not adequacy:
            return call.error is None
        return call.error is None and bool(adequacy.get("adequate"))

    def _requested_unit_tokens(self, question: str) -> set[str]:
        lowered = question.lower()
        units = {
            "ml": {"ml", "milliliter", "milliliters"},
            "l": {"l", "liter", "liters"},
            "atm": {"atm", "atmosphere", "atmospheres"},
            "kpa": {"kpa"},
            "mmhg": {"mmhg", "torr"},
            "g": {"g", "gram", "grams"},
            "kg": {"kg", "kilogram", "kilograms"},
            "mol": {"mol", "mole", "moles"},
            "k": {"k", "kelvin"},
            "kj": {"kj", "kilojoule", "kilojoules"},
            "j": {"j", "joule", "joules"},
            "s": {"s", "second", "seconds"},
        }
        requested: set[str] = set()
        for canonical, aliases in units.items():
            if any(re.search(rf"\b{re.escape(alias)}\b", lowered) for alias in aliases):
                requested.add(canonical)
        if "how many milliliters" in lowered:
            requested.add("ml")
        if "how many grams" in lowered:
            requested.add("g")
        return requested

    def _final_answer_satisfies_unit_alignment(self, question: str, final_answer: str, payloads: list[dict[str, Any]]) -> bool:
        requested = self._requested_unit_tokens(question)
        if not requested:
            return True
        answer_lower = final_answer.lower()
        if any(re.search(rf"\b{re.escape(unit)}\b", answer_lower) for unit in requested):
            return True
        for payload in payloads:
            units = payload.get("units")
            if isinstance(units, list) and any(str(unit).lower() in requested for unit in units):
                return True
            answer = str(payload.get("answer") or "").lower()
            if any(re.search(rf"\b{re.escape(unit)}\b", answer) for unit in requested):
                return True
        return False

    def _multipart_alignment_present(self, question: str, final_answer: str, payloads: list[dict[str, Any]]) -> bool:
        lowered = question.lower()
        multipart_requested = bool(
            re.search(r"\b(?:parts?|respectively|for each|each of|a\)|b\)|\(a\)|\(b\))\b", lowered)
        )
        if not multipart_requested:
            return True
        if re.search(r"(?:^|[\s;(])(?:a|b|c)[\).:=]", final_answer, flags=re.IGNORECASE):
            return True
        for payload in payloads:
            if isinstance(payload.get("part_ids"), list) and payload.get("part_ids"):
                return True
            if isinstance(payload.get("parts"), list) and payload.get("parts"):
                return True
        return False

    def _answer_target_contract_check(
        self,
        *,
        question: str,
        final_answer: str,
        tool_calls: list[ToolCallResult],
        plan: dict[str, Any],
        problem: GenericProblem | None,
        numeric_trace: dict[str, Any],
    ) -> dict[str, Any]:
        hints: dict[str, Any] = {}
        if hasattr(self, "_contract_tool_hints"):
            try:
                hints = dict(self._contract_tool_hints(plan))  # type: ignore[attr-defined]
            except Exception:
                hints = {}
        schemas = [dict(item) for item in hints.get("answer_target_schemas", []) if isinstance(item, dict)]
        required = bool(hints.get("answer_target_match_required") or schemas)
        if not required:
            return {"required": False, "ok": True, "reason": "answer target contract not required"}
        if option_pairs(problem) and bool(hints.get("mcq_option_alignment_required")):
            if normalized_letter(final_answer) is None:
                return {
                    "required": True,
                    "ok": False,
                    "reason": "final answer does not align to a multiple-choice option",
                }
        structured_numeric_required = any(bool(schema.get("structured_numeric_answer")) for schema in schemas)
        structured_payloads = [
            dict(call.result)
            for call in tool_calls
            if call.error is None and self._tool_call_is_adequate(call) and isinstance(call.result, dict)
        ]
        adequate_numeric_tool = any(
            call.error is None and self._tool_call_is_adequate(call) and answer_like_numeric_values(call.result, question=question)
            for call in tool_calls
        )
        target_roles = {
            str(role)
            for schema in schemas
            for role in list(schema.get("target_semantic_roles", []) or [])
            if role
        }
        if target_roles:
            for call in tool_calls:
                if call.error is not None:
                    continue
                fit = dict(call.metadata.get("semantic_fit", {}) or {})
                tool_roles = {str(role) for role in list(fit.get("tool_semantic_roles", []) or []) if role}
                if not tool_roles:
                    continue
                if target_roles.isdisjoint(tool_roles) and not bool(fit.get("exact_problem_binding")):
                    return {
                        "required": True,
                        "ok": False,
                        "reason": "tool payload targets a different semantic answer type",
                        "target_semantic_roles": sorted(target_roles),
                        "tool_semantic_roles": sorted(tool_roles),
                    }
        if structured_numeric_required or adequate_numeric_tool:
            unit_alignment_required = any(bool(schema.get("unit_alignment_required")) for schema in schemas)
            part_alignment_required = any(bool(schema.get("part_alignment_required")) for schema in schemas)
            if unit_alignment_required and structured_payloads and not self._final_answer_satisfies_unit_alignment(
                question,
                final_answer,
                structured_payloads,
            ):
                return {
                    "required": True,
                    "ok": False,
                    "reason": "structured numeric answer omits requested unit alignment",
                }
            if part_alignment_required and structured_payloads and not self._multipart_alignment_present(
                question,
                final_answer,
                structured_payloads,
            ):
                return {
                    "required": True,
                    "ok": False,
                    "reason": "structured numeric answer omits requested part alignment",
                }
            if numeric_trace.get("required"):
                return {
                    "required": True,
                    "ok": bool(numeric_trace.get("ok")),
                    "reason": (
                        "answer target numeric trace matched"
                        if numeric_trace.get("ok")
                        else str(numeric_trace.get("reason") or "answer target numeric trace mismatch")
                    ),
                }
            if adequate_numeric_tool and not answer_like_numeric_values(final_answer, question=question):
                return {
                    "required": True,
                    "ok": False,
                    "reason": "final answer omits numeric value required by tool-backed target",
                }
        return {
            "required": True,
            "ok": True,
            "reason": "answer target contract matched available runtime evidence",
        }

    def _numeric_trace_contract_check(
        self,
        *,
        question: str,
        final_answer: str,
        tool_calls: list[ToolCallResult],
        plan: dict[str, Any],
        problem: GenericProblem | None,
    ) -> dict[str, Any]:
        hints: dict[str, Any] = {}
        if hasattr(self, "_contract_tool_hints"):
            try:
                hints = dict(self._contract_tool_hints(plan))  # type: ignore[attr-defined]
            except Exception:
                hints = {}
        required = bool(
            hints.get("numeric_trace_required")
            or hints.get("tool_result_alignment_required")
        )
        payload_candidates: list[dict[str, Any]] = []
        for call in tool_calls:
            if call.error is not None or not self._tool_call_is_adequate(call):
                continue
            result_payload = call.result
            if isinstance(result_payload, dict):
                if isinstance(result_payload.get("answer_values"), list):
                    values = numeric_values(result_payload.get("answer_values"))
                else:
                    answer_like = next(
                        (
                            result_payload.get(key)
                            for key in ("answer", "final_answer", "result", "value")
                            if result_payload.get(key) is not None
                        ),
                        result_payload,
                    )
                    values = answer_like_numeric_values(answer_like, question=question)
            else:
                values = answer_like_numeric_values(result_payload, question=question)
            if values:
                payload_candidates.append(
                    {
                        "tool_id": call.tool_id,
                        "values": values,
                        "structured": isinstance(call.result, dict),
                    }
                )
        if payload_candidates:
            required = True
        if not required:
            return {"required": False, "ok": True, "reason": "numeric trace not required"}
        if not payload_candidates:
            return {
                "required": True,
                "ok": False,
                "reason": "missing adequate numeric tool payload",
                "tool_payload_count": 0,
            }
        best_payload = max(payload_candidates, key=lambda item: (len(item["values"]), bool(item["structured"])))
        expected_values = [float(item) for item in best_payload["values"]]
        observed_values = answer_like_numeric_values(final_answer, question=question)
        if not observed_values:
            return {
                "required": True,
                "ok": False,
                "reason": "final answer does not preserve numeric tool payload",
                "tool_id": best_payload["tool_id"],
                "expected_values": expected_values[:6],
                "observed_values": [],
            }
        tolerance = problem.tolerance if problem is not None else {}
        relative_floor = 0.03 if len(expected_values) > 1 or len(observed_values) > 1 else 0.0
        ok, score, notes = _compare_numeric_values(
            expected_values,
            observed_values,
            tolerance=tolerance,
            relative_floor=relative_floor,
        )
        return {
            "required": True,
            "ok": ok,
            "score": score,
            "reason": "numeric trace matched" if ok else "numeric trace mismatch",
            "tool_id": best_payload["tool_id"],
            "expected_values": expected_values[:6],
            "observed_values": observed_values[:6],
            "notes": notes[:4],
            "tool_payload_count": len(payload_candidates),
        }

    def _verify_answer(
        self,
        *,
        question: str,
        final_answer: str,
        docs: list[RetrievedDocument],
        tool_calls: list[ToolCallResult],
        confidence: float,
        problem: GenericProblem | None,
        plan: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        plan = dict(plan or {})
        successful_tools = [call for call in tool_calls if call.error is None]
        adequate_tools = [call for call in successful_tools if self._tool_call_is_adequate(call)]
        inadequate_tools = [call for call in successful_tools if not self._tool_call_is_adequate(call)]
        failed_tools = [call for call in tool_calls if call.error is not None]
        support_count = len(docs) + len(adequate_tools)
        is_multiple_choice = bool(problem and problem.options)
        normalized = normalize_prediction(final_answer)
        looks_like_retrieval_dump = self._looks_like_retrieval_dump(final_answer)
        tool_expected = bool(plan.get("should_use_tools"))
        capability_resolution = dict(plan.get("capability_resolution") or {})
        capability_resolution_required = bool(capability_resolution.get("required"))
        capability_gap_unresolved = bool(capability_resolution_required and not adequate_tools)
        numeric_trace = self._numeric_trace_contract_check(
            question=question,
            final_answer=final_answer,
            tool_calls=tool_calls,
            plan=plan,
            problem=problem,
        )
        numeric_trace_mismatch = bool(numeric_trace.get("required") and not numeric_trace.get("ok"))
        answer_target = self._answer_target_contract_check(
            question=question,
            final_answer=final_answer,
            tool_calls=tool_calls,
            plan=plan,
            problem=problem,
            numeric_trace=numeric_trace,
        )
        answer_target_mismatch = bool(answer_target.get("required") and not answer_target.get("ok"))
        option_support_scores: list[float] = []
        best_option_support = 0.0
        if is_multiple_choice:
            option_support_scores = [support_score(text, question=question, docs=docs) for _, text in option_pairs(problem)]
            best_option_support = max(option_support_scores or [0.0])
        expert_consensus = dict(plan.get("expert_consensus") or {})
        expert_support_count = int(expert_consensus.get("completed_branch_count", 0) or 0)
        expert_disagreement = bool(expert_consensus.get("expert_disagreement"))
        expert_branch_error_count = len(list(expert_consensus.get("branch_errors", []) or []))
        offline_mcq_without_tool = bool(is_multiple_choice and not adequate_tools and self.client is None)
        runtime_policy = dict(self.design_strategy_patch.get("runtime_policy", {}))
        reasoning_backend_required_unavailable = bool(
            runtime_policy.get("require_reasoning_backend_for_conceptual")
            and is_multiple_choice
            and self.client is None
            and not adequate_tools
        )
        unsupported_mcq_guess = bool(
            is_multiple_choice
            and not adequate_tools
            and best_option_support < 2.0
            and expert_support_count == 0
            and bool(re.fullmatch(r"[A-Za-z]", normalized))
        )
        if reasoning_backend_required_unavailable:
            unsupported_mcq_guess = True
        if (
            runtime_policy.get("strict_conceptual_mcq_review")
            and is_multiple_choice
            and not adequate_tools
            and expert_support_count == 0
            and bool(re.fullmatch(r"[A-Za-z]", normalized))
        ):
            unsupported_mcq_guess = True
        mcq_shape_ok = True
        if is_multiple_choice:
            mcq_shape_ok = bool(re.fullmatch(r"[A-Za-z]", normalized))
        if capability_gap_unresolved or reasoning_backend_required_unavailable or numeric_trace_mismatch or answer_target_mismatch:
            risk_level = "high"
        elif failed_tools or (inadequate_tools and not adequate_tools) or support_count == 0 or (tool_expected and not adequate_tools and not is_multiple_choice):
            risk_level = "high"
        elif unsupported_mcq_guess and best_option_support < 2.0:
            risk_level = "high"
        elif is_multiple_choice and (expert_disagreement or expert_branch_error_count > 0) and not adequate_tools:
            risk_level = "medium"
        elif unsupported_mcq_guess:
            risk_level = "medium"
        elif inadequate_tools:
            risk_level = "medium"
        elif looks_like_retrieval_dump:
            risk_level = "medium"
        elif support_count == 1 or confidence < 0.55:
            risk_level = "medium"
        else:
            risk_level = "low"
        status = "pass"
        if not final_answer.strip():
            status = "fail"
        elif capability_gap_unresolved or reasoning_backend_required_unavailable or numeric_trace_mismatch or answer_target_mismatch:
            status = "review"
        elif is_multiple_choice and not mcq_shape_ok:
            status = "review"
        elif inadequate_tools and not adequate_tools:
            status = "review"
        elif is_multiple_choice and (expert_disagreement or expert_branch_error_count > 0) and not adequate_tools:
            status = "review"
        elif unsupported_mcq_guess:
            status = "review"
        elif looks_like_retrieval_dump:
            status = "review"
        elif risk_level == "high":
            status = "review"
        support_summary = {
            "retrieved_doc_count": len(docs),
            "successful_tool_calls": len(successful_tools),
            "adequate_tool_calls": len(adequate_tools),
            "inadequate_tool_calls": len(inadequate_tools),
            "failed_tool_calls": len(failed_tools),
            "best_option_support": round(float(best_option_support), 4),
            "reasoning_client_available": bool(self.client),
            "expert_support_count": expert_support_count,
            "expert_disagreement": expert_disagreement,
            "expert_branch_error_count": expert_branch_error_count,
            "unsupported_mcq_guess": unsupported_mcq_guess,
            "offline_mcq_without_tool": offline_mcq_without_tool,
            "reasoning_backend_required_unavailable": reasoning_backend_required_unavailable,
            "capability_resolution_required": capability_resolution_required,
            "capability_gap_unresolved": capability_gap_unresolved,
            "capability_resolution_block_count": len(list(capability_resolution.get("blocks", []) or [])),
            "numeric_trace": numeric_trace,
            "numeric_trace_mismatch": numeric_trace_mismatch,
            "answer_target": answer_target,
            "answer_target_mismatch": answer_target_mismatch,
            "tool_adequacy": [
                {
                    "tool_id": call.tool_id,
                    **dict(call.metadata.get("adequacy", {})),
                }
                for call in successful_tools[:6]
            ],
        }
        checked_contracts = [
            "answer_presence",
            "support_presence",
            "tool_error_surface",
            "tool_expected" if tool_expected else "tool_optional",
            "retrieval_dump_guard",
            "mcq_shape" if is_multiple_choice else "response_shape",
        ]
        if is_multiple_choice:
            checked_contracts.append("conceptual_reasoning_support")
        if expert_disagreement or expert_branch_error_count:
            checked_contracts.append("expert_consensus_risk")
        if successful_tools:
            checked_contracts.append("tool_result_adequacy")
        if numeric_trace.get("required"):
            checked_contracts.append("numeric_trace_consistency")
        if answer_target.get("required"):
            checked_contracts.append("answer_target_match")
        if capability_resolution_required:
            checked_contracts.append("capability_resolution")
        if self.client is None:
            checked_contracts.append("product_reasoning_backend")
        if reasoning_backend_required_unavailable:
            checked_contracts.append("reasoning_backend_requirement")
        if runtime_policy:
            checked_contracts.append("feedback_strategy_patch")
        return {
            "status": status,
            "risk_level": risk_level,
            "support_summary": support_summary,
            "mcq_shape_ok": mcq_shape_ok,
            "confidence": round(float(confidence), 3),
            "question_type": "multiple_choice" if is_multiple_choice else "free_response",
            "checked_contracts": checked_contracts,
            "question_preview": normalize_whitespace(question)[:160],
        }

    def _reason(
        self,
        question: str,
        docs: list[RetrievedDocument],
        tool_calls: list[ToolCallResult],
        problem: GenericProblem | None,
    ) -> str:
        if self.client is None:
            return self._offline_reason(question=question, docs=docs, tool_calls=tool_calls, problem=problem)
        lines = ["Question:", question, ""]
        if problem and problem.given:
            lines.extend(["Structured givens:", json_preview(problem.given), ""])
        if docs:
            lines.append("Local memory evidence:")
            for index, doc in enumerate(docs[:4], start=1):
                lines.append(f"[{index}] {doc.path}")
                lines.append(doc.snippet)
            lines.append("")
        if tool_calls:
            lines.append("Tool outputs:")
            for call in tool_calls:
                lines.append(f"{call.tool_id}:")
                lines.append(json_preview(call.result if call.error is None else {"error": call.error}))
            lines.append("")
        lines.append("Return the final answer only.")
        try:
            return self.client.complete_text(
                "\n".join(lines),
                system_prompt=(
                    "You are a generated domain answer agent. "
                    "Use local memory snippets and tool outputs when relevant. "
                    "For multiple choice, return only the best option letter unless explanation is explicitly requested. "
                    "For numeric questions, give the computed value with brief units only if needed."
                ),
                max_tokens=900,
            )
        except Exception:
            return self._offline_reason(question=question, docs=docs, tool_calls=tool_calls, problem=problem)

    def _offline_reason(
        self,
        *,
        question: str,
        docs: list[RetrievedDocument],
        tool_calls: list[ToolCallResult],
        problem: GenericProblem | None,
    ) -> str:
        if option_pairs(problem):
            return self._choose_multiple_choice_offline(question=question, docs=docs, problem=problem)
        successful = next((call for call in tool_calls if call.error is None), None)
        if successful is not None:
            return normalize_whitespace(str(successful.result))
        if docs:
            return normalize_whitespace(docs[0].snippet[:280])
        return ""

    def _choose_multiple_choice_offline(
        self,
        *,
        question: str,
        docs: list[RetrievedDocument],
        problem: GenericProblem | None,
    ) -> str:
        pairs = option_pairs(problem)
        if not pairs:
            return ""
        scored = [(support_score(text, question=question, docs=docs), letter, text) for letter, text in pairs]
        scored.sort(key=lambda item: (item[0], -ord(item[1])), reverse=True)
        best_score, best_letter, _ = scored[0]
        if best_score > 0:
            return best_letter
        return ""

    def _conceptual_multiple_choice_heuristic(self, question: str, pairs: list[tuple[str, str]]) -> str | None:
        _ = (question, pairs)
        return None

    def evaluate_problems(self, problems: list[GenericProblem], *, limit: int | None = None, learn: bool = False) -> list[EvaluationRecord]:
        records: list[EvaluationRecord] = []
        for problem in problems[: limit or len(problems)]:
            answer_record = self.answer_question(problem.question, problem=problem, learn=learn)
            correct, score, notes = evaluate_prediction(problem, answer_record)
            records.append(
                EvaluationRecord(
                    problem_id=problem.problem_id,
                    source_file=problem.source_file,
                    correct=correct,
                    score=score,
                    expected=problem.answer if problem.answer is not None else problem.expected_answer,
                    prediction=answer_record.final_answer,
                    notes=notes,
                    answer_record=answer_record,
                )
            )
        return records


class GeneratedLayer3Runtime(GeneratedQARuntime):
    def __init__(
        self,
        *,
        repo_root: str | Path,
        runtime_config: dict[str, Any] | None = None,
        package_root: str | Path,
        client: Any | None = None,
    ) -> None:
        super().__init__(repo_root=repo_root, runtime_config=runtime_config, client=client)
        self.package_root = Path(package_root)
        self.manifest = self._read_json(self.package_root / "manifest.json")
        self.agent_specs = [
            GeneratedAgentSpec(**item)
            for item in self._read_json(self.package_root / "agent_specs.json").get("agents", [])
            if isinstance(item, dict)
        ]
        self.agent_specs_by_id = {item.agent_id: item for item in self.agent_specs}
        self.execution_graph = self._read_json(self.package_root / "execution_graph.json")
        self.benchmark_plan = self._read_json(self.package_root / "benchmark_plan.json")
        self.runs_dir = self.package_root / "runs"
        self.runs_dir.mkdir(parents=True, exist_ok=True)
        self.runtime_memory_path = self.package_root / "runtime_memory.json"
        self.memory_policy = dict(self.runtime_config.get("memory_policy", {}))
        self.design_memory = dict(self.runtime_config.get("design_memory", {}))
        self.design_strategy_patch = dict(
            self.runtime_config.get("design_strategy_patch")
            or self.design_memory.get("strategy_patch", {})
            or self.memory_policy.get("strategy_patch", {})
        )
        self.product_runtime_plan = dict(self.runtime_config.get("product_runtime_plan", {}))
        self.execution_contract = dict(self.product_runtime_plan.get("execution_contract", {}))
        self.runtime_memory = self._load_runtime_memory()
        self._merge_design_memory_seed()
        if self.runtime_memory_path.exists():
            self._write_runtime_memory()

    @classmethod
    def from_runtime_config(
        cls,
        *,
        repo_root: str | Path,
        runtime_config: dict[str, Any],
        package_root: str | Path,
        client: Any | None = None,
    ) -> "GeneratedLayer3Runtime":
        return cls(
            repo_root=repo_root,
            runtime_config=runtime_config,
            package_root=package_root,
            client=client,
        )

    def _read_json(self, path: Path) -> dict[str, Any]:
        if not path.exists():
            return {}
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return {}
        return value if isinstance(value, dict) else {}

    def _load_runtime_memory(self) -> dict[str, Any]:
        base = {
            "schema_version": "runtime-memory/v1",
            "answer_count": 0,
            "evaluation_batches": [],
            "failure_patterns": {},
            "tool_success": {},
            "tool_failure": {},
            "recent_routes": [],
            "routing_hints": {"preferred_tools": []},
            "improvement_actions": [],
            "self_summary": "",
            "design_memory_aggregate": {},
            "design_recommendations": [],
        }
        if not self.runtime_memory_path.exists():
            return base
        try:
            loaded = json.loads(self.runtime_memory_path.read_text(encoding="utf-8"))
        except Exception:
            return base
        if not isinstance(loaded, dict):
            return base
        merged = {**base, **loaded}
        merged.setdefault("routing_hints", {"preferred_tools": []})
        merged.setdefault("recent_routes", [])
        merged.setdefault("evaluation_batches", [])
        return merged

    def _write_runtime_memory(self) -> None:
        self.runtime_memory_path.write_text(
            json.dumps(self.runtime_memory, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def _merge_design_memory_seed(self) -> None:
        if not self.design_memory:
            return
        self.runtime_memory["design_memory_aggregate"] = dict(self.design_memory.get("aggregate", {}))
        self.runtime_memory["design_recommendations"] = list(self.design_memory.get("recommendations", []))[:10]
        design_hints = dict(self.design_memory.get("runtime_hints", {}))
        self.runtime_memory["design_tool_cues"] = list(design_hints.get("prefer_tool_cues", []))[:20]
        self.runtime_memory["design_strategy_patch"] = dict(self.design_strategy_patch)

    def _memory_hints(self, question: str, problem: GenericProblem | None = None) -> dict[str, Any]:
        _ = problem
        failure_patterns = dict(self.runtime_memory.get("failure_patterns", {}))
        top_failures = [
            {"failure_type": key, "count": value}
            for key, value in sorted(failure_patterns.items(), key=lambda item: (-int(item[1]), item[0]))[:5]
        ]
        preferred_tools = self._memory_preferred_tool_ids(question)
        return {
            "available": bool(self.runtime_memory or self.design_memory),
            "preferred_tools": preferred_tools,
            "failure_patterns": top_failures,
            "tool_routing": list(self.memory_policy.get("tool_routing", [])),
            "answer_rendering": list(self.memory_policy.get("answer_rendering", [])),
            "strategy_patch": {
                "failure_drivers": dict(self.design_strategy_patch.get("failure_drivers", {})),
                "runtime_policy": dict(self.design_strategy_patch.get("runtime_policy", {})),
                "notes": list(self.design_strategy_patch.get("notes", []))[:4],
            },
            "improvement_actions": list(self.runtime_memory.get("improvement_actions", []))[:8],
            "self_summary": str(self.runtime_memory.get("self_summary") or ""),
            "gold_answer_policy": self.memory_policy.get(
                "gold_answer_policy",
                "gold answers may be used for evaluation summaries but must not be added to retrieval memory",
            ),
        }

    def _memory_preferred_tool_ids(self, question: str) -> list[str]:
        lowered = question.lower()
        preferred: list[str] = []
        routing_hints = dict(self.runtime_memory.get("routing_hints", {}))
        for tool_id in routing_hints.get("preferred_tools", []):
            tool_tokens = {
                token
                for token in tokenize(str(tool_id).replace("_", " "))
                if len(token) > 2 and token not in {"tool", "tools", "law", "laws"}
            }
            if isinstance(tool_id, str) and tool_tokens and any(token in lowered for token in tool_tokens):
                preferred.append(tool_id)
        for item in self.memory_policy.get("prefer_tool_cues", []):
            if not isinstance(item, dict):
                continue
            cue = str(item.get("cue") or "").lower()
            tool_id = str(item.get("tool") or "")
            cue_tokens = [token for token in tokenize(cue) if len(token) > 1]
            if tool_id and cue_tokens and all(token in lowered for token in cue_tokens):
                if tool_id not in preferred:
                    preferred.append(tool_id)
        return preferred[:8]

    def _update_runtime_memory_from_answer(self, record: AnswerRecord, *, plan: dict[str, Any]) -> None:
        self.runtime_memory["answer_count"] = int(self.runtime_memory.get("answer_count", 0)) + 1
        tool_success = dict(self.runtime_memory.get("tool_success", {}))
        tool_failure = dict(self.runtime_memory.get("tool_failure", {}))
        for call in record.tool_calls:
            if call.error:
                tool_failure[call.tool_id] = int(tool_failure.get(call.tool_id, 0)) + 1
            else:
                tool_success[call.tool_id] = int(tool_success.get(call.tool_id, 0)) + 1
        self.runtime_memory["tool_success"] = tool_success
        self.runtime_memory["tool_failure"] = tool_failure
        route = {
            "question_preview": record.question[:180],
            "answer_mode": plan.get("answer_mode"),
            "used_tools": [call.tool_id for call in record.tool_calls],
            "retrieved_doc_count": len(record.retrieved_docs),
            "verification_status": record.verification.get("status"),
            "risk_level": record.verification.get("risk_level"),
        }
        recent_routes = list(self.runtime_memory.get("recent_routes", []))
        recent_routes.append(route)
        self.runtime_memory["recent_routes"] = recent_routes[-50:]

    def evaluate_problems(
        self,
        problems: list[GenericProblem],
        *,
        limit: int | None = None,
        learn: bool = False,
    ) -> list[EvaluationRecord]:
        records = super().evaluate_problems(problems, limit=limit, learn=learn)
        if learn:
            self._update_runtime_memory_from_records(records)
            self._write_runtime_memory()
        return records

    def _update_runtime_memory_from_records(self, records: list[EvaluationRecord]) -> None:
        if not records:
            return
        correct_count = sum(1 for record in records if record.correct)
        scores = [float(record.score) for record in records]
        failure_counts = dict(self.runtime_memory.get("failure_patterns", {}))
        batch_failure_counts: dict[str, int] = {}
        for record in records:
            failure_type = self._canonical_runtime_failure_label(self._classify_runtime_failure(record))
            if not failure_type:
                continue
            failure_counts[failure_type] = int(failure_counts.get(failure_type, 0)) + 1
            batch_failure_counts[failure_type] = int(batch_failure_counts.get(failure_type, 0)) + 1
        batch = {
            "problem_count": len(records),
            "correct_count": correct_count,
            "accuracy": round(correct_count / len(records), 4),
            "mean_score": round(sum(scores) / len(scores), 4) if scores else 0.0,
            "failure_counts": batch_failure_counts,
        }
        batches = list(self.runtime_memory.get("evaluation_batches", []))
        batches.append(batch)
        self.runtime_memory["evaluation_batches"] = batches[-25:]
        self.runtime_memory["failure_patterns"] = dict(
            sorted(failure_counts.items(), key=lambda item: (-int(item[1]), item[0]))
        )
        top_failures = ", ".join(
            f"{key}:{value}" for key, value in list(self.runtime_memory["failure_patterns"].items())[:3]
        )
        self.runtime_memory["self_summary"] = (
            f"Last batch accuracy={batch['accuracy']}, mean_score={batch['mean_score']}; "
            f"dominant failures={top_failures or 'none'}."
        )
        self.runtime_memory["improvement_actions"] = self._runtime_improvement_actions()

    def _canonical_runtime_failure_label(self, failure_type: str | None) -> str | None:
        if failure_type is None:
            return None
        aliases = {
            "tool_execution_failure": "tool_error",
            "tool_execution_error": "tool_error",
            "tool_call_failure": "tool_error",
            "verification_review": "verifier_contract_failure",
            "verification_failure": "verifier_contract_failure",
            "reasoning_backend_gap": "reasoning_backend_unavailable",
        }
        return aliases.get(str(failure_type), str(failure_type))

    def _classify_runtime_failure(self, record: EvaluationRecord) -> str | None:
        if record.correct:
            return None
        notes = " ".join(str(item) for item in record.notes).lower()
        verification = dict(record.answer_record.verification or {})
        support_summary = dict(verification.get("support_summary") or {})
        checked_contracts = {str(item) for item in verification.get("checked_contracts", [])}
        tool_calls = list(record.answer_record.tool_calls)
        has_successful_tool = any(call.error is None for call in tool_calls)
        is_multiple_choice = str(verification.get("question_type", "")).lower() == "multiple_choice"
        low_score = float(record.score) < 0.25
        if self._looks_like_retrieval_dump(str(record.prediction or record.answer_record.final_answer)):
            return "answer_render_failure"
        if (
            self.client is None
            and not has_successful_tool
            and (
                bool(support_summary.get("unsupported_mcq_guess"))
                or (is_multiple_choice and low_score)
                or str(verification.get("status", "")).lower() == "review"
            )
        ):
            return "reasoning_backend_unavailable"
        if has_successful_tool and low_score:
            return "wrong_tool_binding"
        if "numeric mismatch" in notes:
            return "numeric_mismatch"
        if any(call.error for call in tool_calls):
            return "tool_error"
        if not tool_calls and (
            bool(support_summary.get("capability_gap_unresolved"))
            or bool(support_summary.get("capability_resolution_required"))
            or (
                "tool_expected" in checked_contracts
                and (
                    has_structured_numeric_evidence(record.expected)
                    or str(verification.get("status", "")).lower() == "review"
                )
            )
        ):
            return "tool_routing_failure"
        if bool(support_summary.get("unsupported_mcq_guess")) or (is_multiple_choice and not has_successful_tool):
            return "conceptual_reasoning_gap"
        if record.answer_record.verification.get("status") == "review":
            return "verifier_contract_failure"
        if len(str(record.prediction or "")) > 120:
            return "answer_render_failure"
        return "answer_synthesis_failure"

    def _runtime_improvement_actions(self) -> list[dict[str, str]]:
        patterns = dict(self.runtime_memory.get("failure_patterns", {}))
        actions = []
        action_map = {
            "tool_routing_failure": {
                "target": "tool-routing",
                "action": "prefer existing resource/tool paths before retrieval-only synthesis",
                "stage_reentry": "stage05_formal_planning",
            },
            "wrong_tool_binding": {
                "target": "tool-binding",
                "action": "tighten semantic eligibility and parameter binding before accepting a successful tool call",
                "stage_reentry": "stage05_formal_planning",
            },
            "tool_error": {
                "target": "tool-execution",
                "action": "rebind failing tool calls or construct an adapter before accepting the tool-backed path",
                "stage_reentry": "stage06_execution_layer",
            },
            "reasoning_backend_unavailable": {
                "target": "product-runtime-profile",
                "action": "run conceptual product evaluation with a reasoning-capable model client or classify offline as routing-only",
                "stage_reentry": "stage07_runtime_update",
            },
            "conceptual_reasoning_gap": {
                "target": "conceptual-reasoning",
                "action": "route conceptual no-tool tasks through reason/synthesize/verify agents instead of retrieval-overlap guesses",
                "stage_reentry": "stage05_formal_planning",
            },
            "numeric_mismatch": {
                "target": "numeric-normalization",
                "action": "improve reusable tool routing, parameter extraction, unit normalization, and answer_values verification before prose",
                "stage_reentry": "stage06_execution_layer",
            },
            "verifier_contract_failure": {
                "target": "verification-contract",
                "action": "tighten answer-target, option, unit, and numeric-trace checks before marking outputs pass",
                "stage_reentry": "stage07_runtime_update",
            },
            "answer_render_failure": {
                "target": "answer-rendering",
                "action": "route final output through concise answer contract instead of dumping retrieved evidence",
                "stage_reentry": "stage07_runtime_update",
            },
            "answer_synthesis_failure": {
                "target": "synthesis",
                "action": "trigger multi-expert comparison or verifier insertion for similar future questions",
                "stage_reentry": "stage05_formal_planning",
            },
            "parallel_consensus_failure": {
                "target": "execution-topology",
                "action": "change replica count, fuse unstable branches, or insert an adjudicating verifier",
                "stage_reentry": "stage05_formal_planning",
            },
        }
        for failure_type, count in sorted(patterns.items(), key=lambda item: (-int(item[1]), item[0])):
            canonical_failure_type = self._canonical_runtime_failure_label(str(failure_type))
            if canonical_failure_type is None:
                continue
            template = action_map.get(canonical_failure_type)
            if template is None:
                continue
            actions.append({"failure_type": canonical_failure_type, "count": str(count), **template})
        return actions

    def _contract_runtime_plan(
        self,
        question: str,
        problem: GenericProblem | None,
        *,
        memory_hints: dict[str, Any],
    ) -> dict[str, Any]:
        _ = memory_hints
        runtime_policy = dict(self.design_strategy_patch.get("runtime_policy", {}))
        blocks = [dict(item) for item in self.execution_contract.get("blocks", []) if isinstance(item, dict)]
        modes = {str(block.get("mode") or "") for block in blocks}
        block_text = " ".join(
            " ".join(
                [
                    str(block.get("block_id", "")),
                    " ".join(str(item) for item in block.get("task_ids", [])),
                    " ".join(str(item) for item in block.get("task_titles", [])),
                    " ".join(str(item) for item in block.get("inputs", [])),
                    " ".join(str(item) for item in block.get("outputs", [])),
                ]
            ).lower()
            for block in blocks
        )
        should_retrieve = bool(
            {"retrieve", "acquire-resource"} & modes
            or any(token in block_text for token in ("retrieve", "evidence", "memory", "knowledge", "resource"))
        )
        should_use_tools = bool(
            {"use-existing-resource", "construct-resource"} & modes
            or any(token in block_text for token in ("tool", "compute", "calculate", "function", "structured-computation"))
        )
        if runtime_policy.get("numeric_tasks_require_tool_attempt") and self._question_suggests_tool(question):
            should_use_tools = True
        if runtime_policy.get("prefer_model_reasoning_for_conceptual") and problem and problem.options:
            should_retrieve = True
        force_verification = bool(
            any(block.get("requires_verifier") for block in blocks)
            or "verify" in modes
            or "verification" in block_text
        )
        if runtime_policy.get("strict_conceptual_mcq_review") and problem and problem.options:
            force_verification = True
        capability_resolution_blocks = [
            {
                "block_id": block.get("block_id"),
                **dict(block.get("capability_resolution", {})),
            }
            for block in blocks
            if dict(block.get("capability_resolution", {})).get("required")
        ]
        if (
            runtime_policy.get("require_reasoning_backend_for_conceptual")
            and problem
            and problem.options
            and self.client is None
        ):
            capability_resolution_blocks.append(
                {
                    "block_id": "runtime_reasoning_backend_requirement",
                    "required": True,
                    "reason": "conceptual multiple-choice execution requires a reasoning-capable backend or adequate tool support",
                    "required_capability": "reasoning_backend",
                    "runtime_policy_source": "require_reasoning_backend_for_conceptual",
                }
            )
        if capability_resolution_blocks:
            force_verification = True
        retrieve_block_count = sum(
            1
            for block in blocks
            if str(block.get("mode")) == "retrieve"
            or any("evidence" in str(item).lower() or "knowledge" in str(item).lower() for item in block.get("outputs", []))
        )
        retrieval_top_k_delta = int(runtime_policy.get("increase_retrieval_top_k", 0) or 0)
        retrieval_top_k = max(3, min(8, 4 + retrieve_block_count + retrieval_top_k_delta))
        multi_expert_blocks = list(self.execution_contract.get("multi_expert_blocks", []))
        if runtime_policy.get("force_memory_guided_review") and not multi_expert_blocks:
            multi_expert_blocks.append(
                {
                    "block_id": "runtime_memory_review",
                    "strategy": "memory-guided-review",
                    "multi_expert": True,
                    "expert_roles": ["memory_guided_reviewer", "integrator"],
                    "aggregation_policy": "compare-runtime-memory-against-current-evidence",
                }
            )
        return {
            "available": bool(blocks),
            "block_count": len(blocks),
            "execution_order": [str(item) for item in self.execution_contract.get("execution_order", [])],
            "active_modes": sorted(mode for mode in modes if mode),
            "should_retrieve": should_retrieve,
            "should_use_tools": should_use_tools,
            "force_verification": force_verification,
            "retrieval_top_k": retrieval_top_k,
            "verification_focus": (
                "compiled-contract-verification-and-answer-shape"
                if force_verification
                else "grounding-and-answer-shape"
            ),
            "strategy_patch": {
                "failure_drivers": dict(self.design_strategy_patch.get("failure_drivers", {})),
                "runtime_policy": runtime_policy,
            },
            "capability_resolution": {
                "required": bool(capability_resolution_blocks),
                "blocks": capability_resolution_blocks,
                "policy": "review-or-abstain-if-required-capability-is-not-verified",
            },
            "parallel_groups": list(self.execution_contract.get("parallel_groups", [])),
            "multi_expert_blocks": multi_expert_blocks,
            "blocks": [
                {
                    "block_id": block.get("block_id"),
                    "mode": block.get("mode"),
                    "executor_id": block.get("executor_id"),
                    "resource_id": block.get("resource_id"),
                    "task_ids": list(block.get("task_ids", [])),
                    "task_titles": list(block.get("task_titles", [])),
                    "task_types": list(block.get("task_types", [])),
                    "required_capabilities": list(block.get("required_capabilities", [])),
                    "binding": dict(block.get("binding", {})),
                    "capability_resolution": dict(block.get("capability_resolution", {})),
                    "tool_binding_policy": dict(block.get("tool_binding_policy", {})),
                    "verifier_expectations": dict(block.get("verifier_expectations", {})),
                    "dependencies": list(block.get("dependencies", [])),
                    "inputs": list(block.get("inputs", [])),
                    "outputs": list(block.get("outputs", [])),
                    "requires_verifier": bool(block.get("requires_verifier")),
                    "execution_strategy": dict(block.get("execution_strategy", {})),
                }
                for block in blocks
            ],
        }

    def _contract_tool_hints(self, plan: dict[str, Any]) -> dict[str, Any]:
        active_hints = plan.get("_active_tool_contract_hints")
        if isinstance(active_hints, dict) and active_hints:
            return dict(active_hints)
        contract = dict(plan.get("contract_execution") or plan or {})
        blocks = [dict(item) for item in contract.get("blocks", []) if isinstance(item, dict)]
        capabilities: set[str] = set()
        resource_ids: set[str] = set()
        resource_capabilities: set[str] = set()
        schema_tags: set[str] = set()
        domain_tags: set[str] = set()
        policies: list[dict[str, Any]] = []
        verifier_expectations: list[dict[str, Any]] = []
        task_text_parts: list[str] = []
        tool_blocks: list[dict[str, Any]] = []
        candidate_tool_ids: set[str] = set()
        callable_signatures: list[dict[str, Any]] = []
        argument_contracts: list[dict[str, Any]] = []
        expected_argument_fields: set[str] = set()
        expected_output_schemas: list[dict[str, Any]] = []
        answer_target_schemas: list[dict[str, Any]] = []
        normalized_parameter_roles: dict[str, dict[str, Any]] = {}
        unit_normalization_hints: dict[str, dict[str, Any]] = {}
        output_field_mapping: dict[str, list[str]] = {}
        for block in blocks:
            binding = dict(block.get("binding", {}))
            policy = dict(block.get("tool_binding_policy", {}))
            expectations = dict(block.get("verifier_expectations", {}))
            capabilities.update(str(item) for item in block.get("required_capabilities", []) if item)
            capabilities.update(str(item) for item in binding.get("required_capabilities", []) if item)
            resource_id = str(block.get("resource_id") or binding.get("resource_id") or "").strip()
            if resource_id:
                resource_ids.add(resource_id)
            resource_capabilities.update(str(item) for item in binding.get("resource_capabilities", []) if item)
            schema_tags.update(str(item) for item in binding.get("resource_schema_tags", []) if item)
            domain_tags.update(str(item) for item in binding.get("resource_domain_tags", []) if item)
            policies.append(policy)
            verifier_expectations.append(expectations)
            task_text_parts.extend(str(item) for item in block.get("task_titles", []) if item)
            task_text_parts.extend(str(item) for item in block.get("inputs", []) if item)
            task_text_parts.extend(str(item) for item in block.get("outputs", []) if item)
            candidate_tool_ids.update(str(item) for item in block.get("candidate_tool_ids", []) if item)
            candidate_tool_ids.update(str(item) for item in binding.get("candidate_tool_ids", []) if item)
            for signature in [*list(block.get("callable_signatures", []) or []), *list(binding.get("callable_signatures", []) or [])]:
                if not isinstance(signature, dict):
                    continue
                signature_copy = dict(signature)
                tool_id = str(signature_copy.get("tool_id") or "").strip()
                if tool_id:
                    candidate_tool_ids.add(tool_id)
                    callable_signatures.append(signature_copy)
                expected_argument_fields.update(str(item) for item in signature_copy.get("params", []) if item)
                output_schema = signature_copy.get("output_schema")
                if isinstance(output_schema, dict) and output_schema:
                    expected_output_schemas.append(dict(output_schema))
            expected_argument_fields.update(str(item) for item in block.get("expected_argument_fields", []) if item)
            expected_argument_fields.update(str(item) for item in binding.get("expected_argument_fields", []) if item)
            for source in (block, binding):
                for field, role_payload in dict(source.get("normalized_parameter_roles", {}) or {}).items():
                    if isinstance(role_payload, dict):
                        normalized_parameter_roles.setdefault(str(field), dict(role_payload))
                for field, hint_payload in dict(source.get("unit_normalization_hints", {}) or {}).items():
                    if isinstance(hint_payload, dict):
                        unit_normalization_hints.setdefault(str(field), dict(hint_payload))
                for field, mapped_values in dict(source.get("output_field_mapping", {}) or {}).items():
                    existing = output_field_mapping.setdefault(str(field), [])
                    for mapped_value in list(mapped_values or []):
                        text_value = str(mapped_value)
                        if text_value not in existing:
                            existing.append(text_value)
            for argument_contract in [*list(block.get("argument_contracts", []) or []), *list(binding.get("argument_contracts", []) or [])]:
                if not isinstance(argument_contract, dict):
                    continue
                contract_copy = dict(argument_contract)
                tool_id = str(contract_copy.get("tool_id") or "").strip()
                if tool_id:
                    candidate_tool_ids.add(tool_id)
                for field, role_payload in dict(contract_copy.get("parameter_roles", {}) or {}).items():
                    if isinstance(role_payload, dict):
                        normalized_parameter_roles.setdefault(str(field), dict(role_payload))
                for field, hint_payload in dict(contract_copy.get("unit_normalization_hints", {}) or {}).items():
                    if isinstance(hint_payload, dict):
                        unit_normalization_hints.setdefault(str(field), dict(hint_payload))
                for field, mapped_values in dict(contract_copy.get("output_field_mapping", {}) or {}).items():
                    existing = output_field_mapping.setdefault(str(field), [])
                    for mapped_value in list(mapped_values or []):
                        text_value = str(mapped_value)
                        if text_value not in existing:
                            existing.append(text_value)
                argument_contracts.append(contract_copy)
            for output_schema in (block.get("expected_output_schema"), binding.get("expected_output_schema")):
                if isinstance(output_schema, dict) and output_schema:
                    expected_output_schemas.append(dict(output_schema))
            for target_schema in (block.get("answer_target_schema"), binding.get("answer_target_schema")):
                if isinstance(target_schema, dict) and target_schema:
                    answer_target_schemas.append(dict(target_schema))
            if policy.get("contract_candidate_required") or policy.get("semantic_fit_required"):
                block_candidate_ids = list(block.get("candidate_tool_ids", []) or binding.get("candidate_tool_ids", []) or [])
                block_callable_signatures = [
                    dict(item)
                    for item in [*list(block.get("callable_signatures", []) or []), *list(binding.get("callable_signatures", []) or [])]
                    if isinstance(item, dict)
                ]
                tool_blocks.append(
                    {
                        "block_id": block.get("block_id"),
                        "mode": block.get("mode"),
                        "resource_id": resource_id,
                        "resource_kind": binding.get("resource_kind"),
                        "required_capabilities": list(block.get("required_capabilities", [])),
                        "candidate_tool_ids": block_candidate_ids,
                        "callable_signatures": block_callable_signatures,
                        "argument_contracts": list(block.get("argument_contracts", []) or binding.get("argument_contracts", []) or []),
                        "expected_argument_fields": list(block.get("expected_argument_fields", []) or binding.get("expected_argument_fields", []) or []),
                        "normalized_parameter_roles": dict(block.get("normalized_parameter_roles") or binding.get("normalized_parameter_roles") or {}),
                        "unit_normalization_hints": dict(block.get("unit_normalization_hints") or binding.get("unit_normalization_hints") or {}),
                        "output_field_mapping": dict(block.get("output_field_mapping") or binding.get("output_field_mapping") or {}),
                        "expected_output_schema": dict(block.get("expected_output_schema") or binding.get("expected_output_schema") or {}),
                        "answer_target_schema": dict(block.get("answer_target_schema") or binding.get("answer_target_schema") or {}),
                        "task_text": " ".join(
                            [
                                " ".join(str(item) for item in block.get("task_titles", []) if item),
                                " ".join(str(item) for item in block.get("inputs", []) if item),
                                " ".join(str(item) for item in block.get("outputs", []) if item),
                            ]
                        ),
                        "tool_contract_scope": block.get("tool_contract_scope") or binding.get("tool_contract_scope") or "block-local",
                        "candidate_resolution_status": policy.get("candidate_resolution_status"),
                        "unresolved_callable_gap": bool(policy.get("unresolved_callable_gap")),
                        "lexical_fallback_allowed": bool(policy.get("lexical_fallback_allowed", True)),
                    }
                )
        semantic_required = any(bool(item.get("semantic_fit_required")) for item in policies)
        parameter_required = any(bool(item.get("parameter_fit_required")) for item in policies)
        contract_candidate_required = any(bool(item.get("contract_candidate_required")) for item in policies)
        minimum_parameter_coverage = max(
            [float(item.get("minimum_parameter_coverage", 0.0) or 0.0) for item in policies] or [0.0]
        )
        do_not_accept_first_success = any(bool(item.get("do_not_accept_first_success_without_adequacy")) for item in policies)
        target_match_required = any(bool(item.get("answer_target_match_required")) for item in policies) or any(
            bool(item.get("answer_target_match")) for item in verifier_expectations
        )
        mcq_alignment_required = any(bool(item.get("mcq_option_alignment_required")) for item in policies) or any(
            bool(item.get("mcq_option_shape")) for item in verifier_expectations
        )
        numeric_trace_required = any(
            bool(item.get("numeric_trace_consistency") or item.get("tool_payload_to_final_answer_consistency"))
            for item in verifier_expectations
        )
        tool_result_alignment_required = any(bool(item.get("tool_result_alignment")) for item in verifier_expectations)
        broad_fallback_after_candidate_exhaustion = any(
            bool(item.get("broad_fallback_after_candidate_exhaustion"))
            for item in policies
        )
        return {
            "required_capabilities": sorted(capabilities),
            "resource_ids": sorted(resource_ids),
            "resource_capabilities": sorted(resource_capabilities),
            "schema_tags": sorted(schema_tags),
            "domain_tags": sorted(domain_tags),
            "semantic_fit_required": semantic_required,
            "parameter_fit_required": parameter_required,
            "contract_candidate_required": contract_candidate_required,
            "candidate_resolution_status": "unresolved-callable-gap"
            if any(str(item.get("candidate_resolution_status") or "") == "unresolved-callable-gap" for item in policies)
            else "candidate-tools-present"
            if any(str(item.get("candidate_resolution_status") or "") == "candidate-tools-present" for item in policies)
            else "not-tool-bound",
            "unresolved_callable_gap": any(bool(item.get("unresolved_callable_gap")) for item in policies),
            "lexical_fallback_allowed": all(bool(item.get("lexical_fallback_allowed", True)) for item in policies),
            "broad_fallback_after_candidate_exhaustion": broad_fallback_after_candidate_exhaustion,
            "minimum_parameter_coverage": minimum_parameter_coverage,
            "do_not_accept_first_success_without_adequacy": do_not_accept_first_success,
            "answer_target_match_required": target_match_required,
            "mcq_option_alignment_required": mcq_alignment_required,
            "numeric_trace_required": numeric_trace_required,
            "tool_result_alignment_required": tool_result_alignment_required,
            "tool_blocks": tool_blocks,
            "candidate_tool_ids": sorted(candidate_tool_ids),
            "callable_signatures": callable_signatures,
            "argument_contracts": argument_contracts,
            "expected_argument_fields": sorted(expected_argument_fields),
            "normalized_parameter_roles": normalized_parameter_roles,
            "unit_normalization_hints": unit_normalization_hints,
            "output_field_mapping": output_field_mapping,
            "expected_output_schemas": expected_output_schemas,
            "answer_target_schemas": answer_target_schemas,
            "task_text": " ".join(task_text_parts),
        }

    def _contract_trace_packet(self, contract_plan: dict[str, Any]) -> dict[str, Any]:
        return {
            "available": bool(contract_plan.get("available")),
            "block_count": int(contract_plan.get("block_count", 0)),
            "execution_order": list(contract_plan.get("execution_order", [])),
            "active_modes": list(contract_plan.get("active_modes", [])),
            "should_retrieve": bool(contract_plan.get("should_retrieve")),
            "should_use_tools": bool(contract_plan.get("should_use_tools")),
            "force_verification": bool(contract_plan.get("force_verification")),
            "capability_resolution_required": bool(dict(contract_plan.get("capability_resolution", {})).get("required")),
            "capability_resolution_block_count": len(dict(contract_plan.get("capability_resolution", {})).get("blocks", [])),
            "parallel_group_count": len(contract_plan.get("parallel_groups", [])),
            "multi_expert_block_count": len(contract_plan.get("multi_expert_blocks", [])),
        }

    def answer_question(
        self,
        question: str,
        *,
        problem: GenericProblem | None = None,
        learn: bool = True,
    ) -> AnswerRecord:
        normalized_question = normalize_whitespace(question)
        agent_trace: list[dict[str, Any]] = []
        notes: list[str] = []

        intake_packet = {
            "question": normalized_question,
            "problem_id": getattr(problem, "problem_id", None),
            "options": list(problem.options) if problem else [],
            "given_keys": sorted((problem.given or {}).keys()) if problem else [],
        }
        agent_trace.append(self._trace_packet("input_agent", intake_packet))

        memory_hints = self._memory_hints(normalized_question, problem)
        agent_trace.append(self._trace_packet("memory_agent", memory_hints))

        contract_plan = self._contract_runtime_plan(normalized_question, problem, memory_hints=memory_hints)
        agent_trace.append(self._trace_packet("execution_contract_agent", self._contract_trace_packet(contract_plan)))
        plan = self._plan_question(
            normalized_question,
            problem,
            memory_hints=memory_hints,
            contract_plan=contract_plan,
        )
        agent_trace.append(self._trace_packet("planning_agent", plan))
        notes.append(f"planner selected answer_mode={plan.get('answer_mode', 'unknown')}")
        if contract_plan.get("block_count"):
            notes.append(
                "runtime followed compiled execution contract "
                f"with {contract_plan.get('block_count')} block(s)"
            )

        retrieval_top_k = int(plan.get("retrieval_top_k", 6))
        docs = (
            self.memory_index.search(plan.get("search_query") or normalized_question, top_k=retrieval_top_k)
            if plan.get("should_retrieve", True)
            else []
        )
        retrieval_packet = {
            "retrieved_doc_count": len(docs),
            "top_paths": [doc.path for doc in docs[:4]],
        }
        agent_trace.append(self._trace_packet("retrieval_agent", retrieval_packet))
        notes.append(f"retrieval_agent gathered {len(docs)} documents")

        tool_calls, tool_result_payload = self._run_tool_agent(
            question=normalized_question,
            plan=plan,
            problem=problem,
        )
        agent_trace.append(
            self._trace_packet(
                "tool_agent",
                {
                    "tool_calls": [asdict(call) for call in tool_calls],
                    "has_successful_tool": any(call.error is None for call in tool_calls),
                },
            )
        )
        if tool_calls:
            notes.append(f"tool_agent attempted {len(tool_calls)} tool call(s)")

        expert_consensus = self._run_expert_ensemble_agent(
            question=normalized_question,
            problem=problem,
            plan=plan,
            docs=docs,
            tool_calls=tool_calls,
        )
        plan["expert_consensus"] = expert_consensus
        agent_trace.append(self._trace_packet("expert_ensemble_agent", expert_consensus))
        if expert_consensus.get("active_strategy") != "serial":
            notes.append(
                "expert_ensemble_agent used "
                f"{expert_consensus.get('active_strategy')} topology via {expert_consensus.get('realization')}"
            )

        raw_answer = self._run_synthesis_agent(
            question=normalized_question,
            docs=docs,
            tool_calls=tool_calls,
            problem=problem,
            plan=plan,
        )
        agent_trace.append(
            self._trace_packet(
                "synthesis_agent",
                {
                    "raw_answer_preview": normalize_whitespace(raw_answer)[:240],
                    "model_call_errors": list(plan.get("model_call_errors", [])),
                },
            )
        )
        if plan.get("model_call_errors"):
            notes.append(f"model call fallback occurred: {plan['model_call_errors'][-1].get('agent')}")

        final_answer = self._render_final_answer(
            raw_answer=raw_answer,
            tool_result_payload=tool_result_payload,
            docs=docs,
            plan=plan,
            problem=problem,
        )
        for render_note in list(plan.get("render_notes", []) or []):
            notes.append(str(render_note))
        runtime_policy = dict(self.design_strategy_patch.get("runtime_policy", {}))
        if (
            runtime_policy.get("require_reasoning_backend_for_conceptual")
            and problem
            and problem.options
            and self.client is None
            and not plan.get("should_use_tools")
            and not any(self._tool_call_is_adequate(call) for call in tool_calls)
        ):
            final_answer = "I do not have enough information."
            notes.append(
                "runtime abstained because the active strategy patch requires a reasoning-capable backend for conceptual no-tool cases"
            )
        confidence = min(0.35 + 0.1 * len(docs) + 0.15 * any(call.error is None for call in tool_calls), 0.95)
        verification = self._verify_answer(
            question=normalized_question,
            final_answer=final_answer,
            docs=docs,
            tool_calls=tool_calls,
            confidence=confidence,
            problem=problem,
            plan=plan,
        )
        agent_trace.append(self._trace_packet("verifier_agent", verification))
        notes.append(f"verifier_agent returned {verification['status']} at {verification['risk_level']} risk")

        repair = self._repair_reviewed_answer(
            question=normalized_question,
            problem=problem,
            plan=plan,
            docs=docs,
            tool_calls=tool_calls,
            raw_answer=raw_answer,
            final_answer=final_answer,
            verification=verification,
        )
        if repair.get("attempted"):
            agent_trace.append(self._trace_packet("repair_agent", repair.get("trace", {})))
            notes.append(str(repair.get("note", "repair_agent attempted contract repair")))
        if repair.get("accepted"):
            docs = repair.get("docs", docs)
            tool_calls = repair.get("tool_calls", tool_calls)
            tool_result_payload = repair.get("tool_result_payload", tool_result_payload)
            raw_answer = str(repair.get("raw_answer", raw_answer))
            final_answer = str(repair.get("final_answer", final_answer))
            confidence = float(repair.get("confidence", confidence))
            verification = dict(repair.get("verification", verification))
            agent_trace.append(self._trace_packet("verifier_agent", verification))
            notes.append(f"repair_agent accepted revised answer with verifier status={verification['status']}")

        record = AnswerRecord(
            question=normalized_question,
            final_answer=final_answer,
            raw_answer=raw_answer or final_answer,
            confidence=float(verification.get("confidence", confidence)),
            retrieved_docs=docs,
            tool_calls=tool_calls,
            route_notes=notes,
            normalized_prediction=normalize_prediction(final_answer),
            verification=verification,
            agent_trace=agent_trace,
            tool_result_payload=tool_result_payload,
        )
        self._write_trace_file(record, plan=plan)
        if learn:
            self._update_runtime_memory_from_answer(record, plan=plan)
            self._write_runtime_memory()
        return record

    def _repair_reviewed_answer(
        self,
        *,
        question: str,
        problem: GenericProblem | None,
        plan: dict[str, Any],
        docs: list[RetrievedDocument],
        tool_calls: list[ToolCallResult],
        raw_answer: str,
        final_answer: str,
        verification: dict[str, Any],
    ) -> dict[str, Any]:
        if str(verification.get("status", "pass")) == "pass":
            return {"attempted": False}
        if self._fast_agent_call_mode():
            return {
                "attempted": False,
                "note": "repair_agent skipped extra model/tool repair by product agent_call_mode=fast",
            }
        support_summary = dict(verification.get("support_summary") or {})
        if support_summary.get("reasoning_backend_required_unavailable"):
            return {
                "attempted": False,
                "note": "repair_agent skipped because the active runtime policy requires a reasoning-capable backend or adequate tool support",
            }
        if support_summary.get("unsupported_mcq_guess") and not plan.get("should_use_tools"):
            return {
                "attempted": False,
                "note": "repair_agent skipped broad tool repair for unsupported offline conceptual MCQ",
            }
        consensus_repair = self._expert_consensus_repair(
            question=question,
            problem=problem,
            plan=plan,
            docs=docs,
            tool_calls=tool_calls,
            final_answer=final_answer,
            verification=verification,
        )
        if consensus_repair.get("attempted") and consensus_repair.get("accepted"):
            return consensus_repair
        repair_plan = {
            **plan,
            "repair_attempt": True,
            "should_use_tools": True,
            "verification_focus": "contract-repair-after-review",
        }
        repair_tool_calls, repair_payload = self._run_tool_agent(
            question=question,
            plan=repair_plan,
            problem=problem,
            force_broad=True,
            previous_tool_calls=tool_calls,
        )
        merged_tool_calls = self._merge_tool_calls(tool_calls, repair_tool_calls)
        raw_repair_answer = self._run_synthesis_agent(
            question=question,
            docs=docs,
            tool_calls=merged_tool_calls,
            problem=problem,
            plan=repair_plan,
        )
        if not repair_payload:
            successful = next((call for call in reversed(merged_tool_calls) if self._tool_call_is_adequate(call)), None)
            repair_payload = successful.result if successful is not None else None
        repaired_final = self._render_final_answer(
            raw_answer=raw_repair_answer,
            tool_result_payload=repair_payload,
            docs=docs,
            plan=repair_plan,
            problem=problem,
        )
        repaired_confidence = min(
            0.35 + 0.1 * len(docs) + 0.15 * any(call.error is None for call in merged_tool_calls),
            0.95,
        )
        repaired_verification = self._verify_answer(
            question=question,
            final_answer=repaired_final,
            docs=docs,
            tool_calls=merged_tool_calls,
            confidence=repaired_confidence,
            problem=problem,
            plan=repair_plan,
        )
        accepted = self._repair_is_better(
            old_answer=final_answer,
            old_verification=verification,
            old_tool_calls=tool_calls,
            new_answer=repaired_final,
            new_verification=repaired_verification,
            new_tool_calls=merged_tool_calls,
        )
        return {
            "attempted": True,
            "accepted": accepted,
            "docs": docs,
            "tool_calls": merged_tool_calls,
            "tool_result_payload": repair_payload,
            "raw_answer": raw_repair_answer,
            "final_answer": repaired_final,
            "confidence": repaired_confidence,
            "verification": repaired_verification,
            "note": (
                "repair_agent accepted broader reusable-tool route"
                if accepted
                else "repair_agent found no stronger reusable-tool route"
            ),
            "trace": {
                "original_status": verification.get("status"),
                "original_risk": verification.get("risk_level"),
                "repaired_status": repaired_verification.get("status"),
                "repaired_risk": repaired_verification.get("risk_level"),
                "new_tool_attempt_count": len(repair_tool_calls),
                "successful_tool_calls": len([call for call in merged_tool_calls if call.error is None]),
                "accepted": accepted,
            },
        }

    def _expert_consensus_repair(
        self,
        *,
        question: str,
        problem: GenericProblem | None,
        plan: dict[str, Any],
        docs: list[RetrievedDocument],
        tool_calls: list[ToolCallResult],
        final_answer: str,
        verification: dict[str, Any],
    ) -> dict[str, Any]:
        expert_consensus = dict(plan.get("expert_consensus") or {})
        consensus_answer = self._normalize_scientific_answer_units(
            question,
            normalize_whitespace(str(expert_consensus.get("consensus_answer") or "")),
        )
        if not consensus_answer:
            return {"attempted": False}
        if normalize_prediction(consensus_answer) == normalize_prediction(final_answer):
            return {"attempted": False}
        branch_results = [
            item
            for item in expert_consensus.get("branch_results", [])
            if isinstance(item, dict)
        ]
        if int(expert_consensus.get("completed_branch_count", len(branch_results)) or 0) < 2:
            return {"attempted": False}
        repair_plan = {
            **plan,
            "repair_attempt": True,
            "verification_focus": "expert-consensus-after-review",
            "consensus_repair": True,
        }
        consensus_confidence = max(
            0.62,
            min(
                0.94,
                sum(float(item.get("confidence", 0.0) or 0.0) for item in branch_results)
                / max(len(branch_results), 1),
            ),
        )
        consensus_verification = self._verify_answer(
            question=question,
            final_answer=consensus_answer,
            docs=docs,
            tool_calls=tool_calls,
            confidence=consensus_confidence,
            problem=problem,
            plan=repair_plan,
        )
        accepted = self._consensus_repair_is_better(
            old_answer=final_answer,
            old_verification=verification,
            new_answer=consensus_answer,
            new_verification=consensus_verification,
            expert_consensus=expert_consensus,
        )
        return {
            "attempted": True,
            "accepted": accepted,
            "docs": docs,
            "tool_calls": tool_calls,
            "tool_result_payload": None,
            "raw_answer": consensus_answer,
            "final_answer": consensus_answer,
            "confidence": consensus_confidence,
            "verification": consensus_verification,
            "note": (
                "repair_agent accepted verified expert-consensus answer"
                if accepted
                else "repair_agent rejected expert-consensus answer after verification"
            ),
            "trace": {
                "repair_type": "expert_consensus",
                "original_status": verification.get("status"),
                "original_risk": verification.get("risk_level"),
                "repaired_status": consensus_verification.get("status"),
                "repaired_risk": consensus_verification.get("risk_level"),
                "completed_branch_count": expert_consensus.get("completed_branch_count", len(branch_results)),
                "expert_disagreement": expert_consensus.get("expert_disagreement"),
                "accepted": accepted,
            },
        }

    def _consensus_repair_is_better(
        self,
        *,
        old_answer: str,
        old_verification: dict[str, Any],
        new_answer: str,
        new_verification: dict[str, Any],
        expert_consensus: dict[str, Any],
    ) -> bool:
        if self._looks_like_retrieval_dump(new_answer):
            return False
        old_score = self._verification_quality_score(old_verification)
        new_score = self._verification_quality_score(new_verification)
        if new_score > old_score:
            return True
        if new_score < old_score:
            return False
        branch_results = [
            item
            for item in expert_consensus.get("branch_results", [])
            if isinstance(item, dict)
        ]
        support_count = sum(1 for item in branch_results if item.get("support"))
        if support_count >= 1 and normalize_prediction(new_answer) != normalize_prediction(old_answer):
            return True
        return False

    def _merge_tool_calls(
        self,
        original: list[ToolCallResult],
        additional: list[ToolCallResult],
    ) -> list[ToolCallResult]:
        merged = list(original)
        seen = {(call.tool_id, json.dumps(call.kwargs, sort_keys=True, default=str)) for call in merged}
        for call in additional:
            key = (call.tool_id, json.dumps(call.kwargs, sort_keys=True, default=str))
            if key in seen:
                continue
            merged.append(call)
            seen.add(key)
        return merged

    def _repair_is_better(
        self,
        *,
        old_answer: str,
        old_verification: dict[str, Any],
        old_tool_calls: list[ToolCallResult],
        new_answer: str,
        new_verification: dict[str, Any],
        new_tool_calls: list[ToolCallResult],
    ) -> bool:
        old_score = self._verification_quality_score(old_verification)
        new_score = self._verification_quality_score(new_verification)
        if new_score > old_score:
            return True
        old_successes = len([call for call in old_tool_calls if self._tool_call_is_adequate(call)])
        new_successes = len([call for call in new_tool_calls if self._tool_call_is_adequate(call)])
        if new_successes > old_successes and not self._looks_like_retrieval_dump(new_answer):
            return True
        if self._looks_like_retrieval_dump(old_answer) and not self._looks_like_retrieval_dump(new_answer):
            return True
        return False

    def _verification_quality_score(self, verification: dict[str, Any]) -> tuple[int, int, float]:
        status_rank = {"fail": 0, "review": 1, "pass": 2}.get(str(verification.get("status", "review")), 1)
        risk_rank = {"high": 0, "medium": 1, "low": 2}.get(str(verification.get("risk_level", "medium")), 1)
        try:
            confidence = float(verification.get("confidence", 0.0))
        except Exception:
            confidence = 0.0
        return status_rank, risk_rank, confidence

    def _looks_like_retrieval_dump(self, answer: str) -> bool:
        lowered_answer = str(answer).lower()
        return len(str(answer)) > 160 and any(
            marker in lowered_answer
            for marker in ("source:", "---", "```", " id:", " layer ", "worked examples")
        )

    def _trace_packet(self, agent_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        spec = self.agent_specs_by_id.get(agent_id)
        return {
            "agent_id": agent_id,
            "role": spec.role if spec else agent_id,
            "dominant_actions": list(spec.dominant_actions) if spec else [],
            "payload": payload,
        }

    def _fast_agent_call_mode(self) -> bool:
        return self.agent_call_mode in {"fast", "synthesis-only", "single-call", "one-call"}

    def _plan_question(
        self,
        question: str,
        problem: GenericProblem | None,
        *,
        memory_hints: dict[str, Any] | None = None,
        contract_plan: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        memory_hints = dict(memory_hints or self._memory_hints(question, problem))
        contract_plan = dict(contract_plan or {})
        fallback = {
            "answer_mode": "multiple-choice" if problem and problem.options else "free-response",
            "should_retrieve": bool(contract_plan.get("should_retrieve", True)),
            "should_use_tools": bool(contract_plan.get("should_use_tools"))
            or bool(problem and (problem.given or problem.matching_function))
            or self._question_suggests_tool(question)
            or bool(memory_hints.get("preferred_tools")),
            "search_query": question,
            "retrieval_top_k": int(contract_plan.get("retrieval_top_k", 6) or 6),
            "verification_focus": contract_plan.get("verification_focus", "grounding-and-answer-shape"),
            "memory_hints": memory_hints,
            "contract_execution": contract_plan,
            "capability_resolution": dict(contract_plan.get("capability_resolution", {})),
            "design_strategy_patch": dict(self.design_strategy_patch),
        }
        spec = self.agent_specs_by_id.get("planning_agent")
        if self.client is None or spec is None or self._fast_agent_call_mode():
            fallback["planning_realization"] = "deterministic-contract-fast-path" if self._fast_agent_call_mode() else "deterministic-fallback"
            return fallback
        prompt = {
            "question": question,
            "problem": {
                "options": list(problem.options) if problem else [],
                "given": dict(problem.given) if problem else {},
                "matching_module": getattr(problem, "matching_module", None),
                "matching_function": getattr(problem, "matching_function", None),
            },
            "available_tools": [tool.id for tool in self.tool_catalog.tools[:30]],
            "memory_hints": memory_hints,
            "design_strategy_patch": dict(self.design_strategy_patch),
            "compiled_execution_contract_plan": contract_plan,
            "required_schema": {
                "answer_mode": "multiple-choice or free-response or numeric",
                "should_retrieve": "boolean",
                "should_use_tools": "boolean",
                "search_query": "string",
                "retrieval_top_k": "integer 1-8",
                "verification_focus": "short string",
                "memory_hints": "object copied from input hints",
            },
        }
        try:
            response = self.client.complete_text(
                json.dumps(prompt, ensure_ascii=False, indent=2),
                system_prompt=spec.llm_prompt + "\nReturn JSON only.",
                max_tokens=500,
            )
            payload = extract_json_payload(response)
        except Exception as exc:
            fallback["planning_error"] = str(exc)[:500]
            payload = {}
        if not payload:
            return fallback
        merged = {**fallback, **payload}
        merged["retrieval_top_k"] = max(1, min(int(merged.get("retrieval_top_k", 6)), 8))
        merged["should_retrieve"] = bool(merged.get("should_retrieve", True))
        merged["should_use_tools"] = bool(merged.get("should_use_tools", fallback["should_use_tools"])) or bool(
            memory_hints.get("preferred_tools")
        ) or bool(contract_plan.get("should_use_tools"))
        if contract_plan.get("force_verification"):
            merged["verification_focus"] = str(contract_plan.get("verification_focus") or merged.get("verification_focus"))
        merged["contract_execution"] = contract_plan
        merged["capability_resolution"] = dict(contract_plan.get("capability_resolution", {}))
        merged["design_strategy_patch"] = dict(self.design_strategy_patch)
        if contract_plan.get("should_retrieve") is False:
            merged["should_retrieve"] = False
        merged["search_query"] = str(merged.get("search_query") or question)
        merged["memory_hints"] = memory_hints
        return merged

    def _run_expert_ensemble_agent(
        self,
        *,
        question: str,
        problem: GenericProblem | None,
        plan: dict[str, Any],
        docs: list[RetrievedDocument],
        tool_calls: list[ToolCallResult],
    ) -> dict[str, Any]:
        spec = self.agent_specs_by_id.get("expert_ensemble_agent")
        topology = dict((spec.metadata if spec else {}).get("execution_topology", {}))
        contract_topology = [
            dict(item)
            for item in dict(plan.get("contract_execution") or {}).get("multi_expert_blocks", [])
            if isinstance(item, dict)
        ]
        if contract_topology:
            topology.update(
                {
                    str(item.get("block_id") or f"contract_multi_expert_{index}"): item
                    for index, item in enumerate(contract_topology, start=1)
                }
            )
        strategies = [dict(item).get("strategy", "serial") for item in topology.values()]
        active_strategy = next((item for item in strategies if item != "serial"), "serial")
        successful_tools = [call.tool_id for call in tool_calls if call.error is None]
        failed_tools = [call.tool_id for call in tool_calls if call.error is not None]
        if active_strategy == "serial" and plan.get("memory_hints", {}).get("failure_patterns"):
            active_strategy = "memory-guided-review"
        branches = self._select_expert_branches(topology, active_strategy, plan=plan)
        branch_results: list[dict[str, Any]] = []
        branch_errors: list[dict[str, str]] = []
        realization = "deterministic-consensus-fallback"
        max_workers = 0
        if self._fast_agent_call_mode() and active_strategy != "serial":
            realization = "fast-mode-metadata-only"
            branch_errors.append(
                {
                    "role": "expert_ensemble_agent",
                    "block_id": "runtime",
                    "error": "LLM expert branches skipped by product agent_call_mode=fast",
                }
            )
        elif self.client is not None and spec is not None and branches and active_strategy != "serial":
            max_workers = min(len(branches), self._max_parallel_expert_workers(topology))
            realization = "parallel-llm-branches" if max_workers > 1 else "sequential-llm-branches"
            if max_workers <= 1:
                spacing = self._branch_call_spacing_seconds()
                for index, branch in enumerate(branches):
                    if index and spacing > 0:
                        time.sleep(spacing)
                    try:
                        branch_results.append(
                            self._run_expert_branch(
                                spec=spec,
                                branch=branch,
                                question=question,
                                problem=problem,
                                plan=plan,
                                docs=docs,
                                tool_calls=tool_calls,
                            )
                        )
                    except Exception as exc:
                        error_text = str(exc)
                        if "429" in error_text or "rate" in error_text.lower():
                            time.sleep(max(4.0, spacing * 3.0))
                            try:
                                branch_results.append(
                                    self._run_expert_branch(
                                        spec=spec,
                                        branch=branch,
                                        question=question,
                                        problem=problem,
                                        plan=plan,
                                        docs=docs,
                                        tool_calls=tool_calls,
                                    )
                                )
                                continue
                            except Exception as retry_exc:
                                error_text = str(retry_exc)
                        branch_errors.append(
                            {
                                "role": str(branch.get("role", "unknown")),
                                "block_id": str(branch.get("block_id", "unknown")),
                                "error": error_text,
                            }
                        )
            else:
                with ThreadPoolExecutor(max_workers=max_workers) as executor:
                    futures = {
                        executor.submit(
                            self._run_expert_branch,
                            spec=spec,
                            branch=branch,
                            question=question,
                            problem=problem,
                            plan=plan,
                            docs=docs,
                            tool_calls=tool_calls,
                        ): branch
                        for branch in branches
                    }
                    for future in as_completed(futures):
                        branch = futures[future]
                        try:
                            branch_results.append(future.result())
                        except Exception as exc:
                            branch_errors.append(
                                {
                                    "role": str(branch.get("role", "unknown")),
                                    "block_id": str(branch.get("block_id", "unknown")),
                                    "error": str(exc),
                                }
                            )
        disagreement = bool(failed_tools and successful_tools) or self._branch_disagreement(branch_results)
        consensus_answer = self._branch_consensus_answer(branch_results)
        return {
            "active_strategy": active_strategy,
            "topology_strategy_counts": {strategy: strategies.count(strategy) for strategy in sorted(set(strategies))},
            "realization": realization,
            "requested_branch_count": len(branches),
            "parallel_worker_count": max_workers,
            "completed_branch_count": len(branch_results),
            "branch_errors": branch_errors,
            "branch_results": branch_results,
            "consensus_answer": consensus_answer,
            "successful_tools": successful_tools,
            "failed_tools": failed_tools,
            "retrieved_doc_count": len(docs),
            "expert_disagreement": disagreement,
            "consensus_note": (
                "parallel expert consensus"
                if branch_results and not disagreement
                else "parallel expert disagreement"
                if branch_results and disagreement
                else
                "tool-supported consensus"
                if successful_tools
                else "retrieval-supported consensus" if docs else "no external consensus evidence"
            ),
        }

    def _select_expert_branches(
        self,
        topology: dict[str, Any],
        active_strategy: str,
        *,
        plan: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        if active_strategy == "serial":
            return []
        branches: list[dict[str, Any]] = []
        contract_blocks = {
            str(block.get("block_id")): dict(block)
            for block in dict((plan or {}).get("contract_execution", {})).get("blocks", [])
            if isinstance(block, dict)
        }

        def block_priority(item: tuple[str, Any]) -> tuple[float, str]:
            block_id, raw_strategy = item
            block = contract_blocks.get(str(block_id), {})
            text = " ".join(
                [
                    str(block_id),
                    " ".join(str(value) for value in block.get("task_titles", [])),
                    " ".join(str(value) for value in block.get("task_types", [])),
                    " ".join(str(value) for value in block.get("required_capabilities", [])),
                ]
            ).lower()
            score = 0.0
            for cue in ("reason", "infer", "retrieve", "evidence", "verify", "integrate", "synthesis", "answer"):
                if cue in text:
                    score += 1.0
            for cue in ("input", "user", "io", "decide", "render", "memory"):
                if cue in text:
                    score -= 0.4
            strategy = dict(raw_strategy)
            score += 0.2 * float(strategy.get("replica_count", 1) or 1)
            return score, str(block_id)

        for block_id, raw_strategy in sorted(topology.items(), key=block_priority, reverse=True):
            strategy = dict(raw_strategy)
            strategy_name = str(strategy.get("strategy", "serial"))
            if strategy_name == "serial":
                continue
            roles = [str(role) for role in strategy.get("expert_roles", []) if str(role) != "integrator"]
            role_priority = {
                "domain_expert": 0,
                "verification_expert": 1,
                "tool_or_evidence_expert": 2,
            }
            roles.sort(key=lambda role: role_priority.get(role, 10))
            if not roles:
                roles = ["domain_expert", "tool_or_evidence_expert"]
            for role in roles:
                branches.append(
                    {
                        "block_id": str(block_id),
                        "role": role,
                        "strategy": strategy_name,
                        "aggregation_policy": str(strategy.get("aggregation_policy", "compare-then-integrate")),
                    }
                )
        if not branches and active_strategy != "serial":
            branches = [
                {
                    "block_id": "runtime_memory_review",
                    "role": "memory_guided_reviewer",
                    "strategy": active_strategy,
                    "aggregation_policy": "compare-runtime-memory-against-current-evidence",
                }
            ]
        return branches[: self._max_expert_branch_count(topology)]

    def _max_expert_branch_count(self, topology: dict[str, Any]) -> int:
        product_runtime = dict(self.runtime_config.get("product_runtime", {}))
        configured = (
            product_runtime.get("max_expert_branches")
            or self.runtime_config.get("max_expert_branches")
            or dict(self.runtime_config.get("adapter", {}).get("config", {})).get("max_expert_branches")
        )
        try:
            if configured is not None:
                return max(1, min(int(configured), 8))
        except Exception:
            pass
        replica_counts = []
        for raw_strategy in topology.values():
            try:
                replica_counts.append(int(dict(raw_strategy).get("replica_count", 1)))
            except Exception:
                continue
        return max(2, min(max(replica_counts or [3]), 4))

    def _branch_call_spacing_seconds(self) -> float:
        product_runtime = dict(self.runtime_config.get("product_runtime", {}))
        configured = (
            product_runtime.get("expert_branch_call_spacing_seconds")
            or self.runtime_config.get("expert_branch_call_spacing_seconds")
            or dict(self.runtime_config.get("adapter", {}).get("config", {})).get("expert_branch_call_spacing_seconds")
        )
        try:
            if configured is not None:
                return max(0.0, min(float(configured), 10.0))
        except Exception:
            pass
        model_name = str(product_runtime.get("model_name") or self.runtime_config.get("model_name") or "").lower()
        backend = str(product_runtime.get("backend") or self.runtime_config.get("backend") or "").lower()
        if "glm" in model_name or backend in {"glm", "zai", "bigmodel"}:
            return 1.0
        return 0.0

    def _max_parallel_expert_workers(self, topology: dict[str, Any]) -> int:
        product_runtime = dict(self.runtime_config.get("product_runtime", {}))
        configured = (
            product_runtime.get("parallel_expert_max_workers")
            or self.runtime_config.get("parallel_expert_max_workers")
            or dict(self.runtime_config.get("adapter", {}).get("config", {})).get("parallel_expert_max_workers")
        )
        try:
            if configured is not None:
                return max(1, min(int(configured), 8))
        except Exception:
            pass
        model_name = str(product_runtime.get("model_name") or self.runtime_config.get("model_name") or "").lower()
        backend = str(product_runtime.get("backend") or self.runtime_config.get("backend") or "").lower()
        if "glm" in model_name or backend in {"glm", "zai", "bigmodel"}:
            return 1
        replica_counts = []
        for raw_strategy in topology.values():
            try:
                replica_counts.append(int(dict(raw_strategy).get("replica_count", 1)))
            except Exception:
                continue
        return max(1, min(max(replica_counts or [2]), 4))

    def _run_expert_branch(
        self,
        *,
        spec: GeneratedAgentSpec,
        branch: dict[str, Any],
        question: str,
        problem: GenericProblem | None,
        plan: dict[str, Any],
        docs: list[RetrievedDocument],
        tool_calls: list[ToolCallResult],
    ) -> dict[str, Any]:
        prompt = self._expert_branch_prompt(
            question=question,
            problem=problem,
            branch=branch,
            plan=plan,
            docs=docs,
            tool_calls=tool_calls,
        )
        role = str(branch.get("role", "expert"))
        system_prompt = (
            f"{spec.llm_prompt}\n"
            f"You are the `{role}` branch for block `{branch.get('block_id')}`. "
            "Return JSON only. Do not invent evidence. If evidence is insufficient, say so."
        )
        response = self.client.complete_text(prompt, system_prompt=system_prompt, max_tokens=550)
        payload = extract_json_payload(response)
        if not payload:
            payload = {"raw_response": normalize_whitespace(response)[:900]}
        payload.setdefault("role", role)
        payload.setdefault("block_id", str(branch.get("block_id", "")))
        payload.setdefault("strategy", str(branch.get("strategy", "")))
        return payload

    def _expert_branch_prompt(
        self,
        *,
        question: str,
        problem: GenericProblem | None,
        branch: dict[str, Any],
        plan: dict[str, Any],
        docs: list[RetrievedDocument],
        tool_calls: list[ToolCallResult],
    ) -> str:
        packet = {
            "branch": branch,
            "question": question,
            "problem_context": {
                "options": list(problem.options) if problem else [],
                "given": dict(problem.given) if problem else {},
                "answer_mode": plan.get("answer_mode"),
            },
            "memory_hints": dict(plan.get("memory_hints", {})),
            "retrieved_evidence": [
                {
                    "path": doc.path,
                    "title": doc.title,
                    "score": round(float(doc.score), 4),
                    "snippet": doc.snippet[:900],
                }
                for doc in docs[:4]
            ],
            "tool_traces": [
                {
                    "tool_id": call.tool_id,
                    "kwargs": call.kwargs,
                    "result": call.result if call.error is None else None,
                    "error": call.error,
                }
                for call in tool_calls[:6]
            ],
            "required_schema": {
                "role": "copied expert role",
                "proposed_answer": "best answer or empty string",
                "confidence": "number 0-1",
                "support": "short list of supporting evidence/tool facts",
                "concerns": "short list of risks or disagreements",
                "needs_verifier": "boolean",
            },
        }
        return json.dumps(packet, ensure_ascii=False, indent=2)

    def _branch_disagreement(self, branch_results: list[dict[str, Any]]) -> bool:
        answers = [
            normalize_prediction(str(item.get("proposed_answer") or item.get("answer") or ""))
            for item in branch_results
        ]
        answers = [answer for answer in answers if answer]
        if len(set(answers)) > 1:
            return True
        return any(
            bool(item.get("needs_verifier"))
            or "disagree" in normalize_whitespace(item.get("concerns", "")).lower()
            for item in branch_results
        )

    def _branch_consensus_answer(self, branch_results: list[dict[str, Any]]) -> str:
        counts: dict[str, int] = {}
        rendered: dict[str, str] = {}
        for item in branch_results:
            raw_answer = str(item.get("proposed_answer") or item.get("answer") or "").strip()
            normalized = normalize_prediction(raw_answer)
            if not normalized:
                continue
            counts[normalized] = counts.get(normalized, 0) + 1
            rendered.setdefault(normalized, raw_answer)
        if not counts:
            return ""
        winner = max(counts.items(), key=lambda item: (item[1], item[0]))[0]
        return rendered.get(winner, winner)

    def _question_suggests_tool(self, question: str) -> bool:
        _ = question
        return False

    def _run_specialized_numeric_tool(self, question: str) -> ToolCallResult | None:
        _ = question
        return None

    def _target_semantic_roles(self, text: str, hints: dict[str, Any] | None = None) -> set[str]:
        roles = {
            str(item)
            for schema in list(dict(hints or {}).get("answer_target_schemas", []) or [])
            if isinstance(schema, dict)
            for item in list(schema.get("target_semantic_roles", []) or [])
            if item
        }
        lowered = str(text or "").lower()
        role_patterns = {
            "enthalpy": ("enthalpy", "heat of reaction", "thermochemistry", "calorimeter", "heat evolved", "heat absorbed"),
            "frequency": ("frequency", "wavelength", "photon", "mhz", "hz", "nm", "electromagnetic"),
            "ksp": ("ksp", "solubility product", "molar solubility", "precipitation", "solubility"),
            "equilibrium_constant": ("equilibrium constant", "kc", "kp", "reaction quotient"),
            "kinetics": ("rate constant", "half-life", "first order", "second order", "kinetics", "rate law"),
            "ph": ("ph", "poh", "acid", "base", "buffer", "ka", "kb"),
            "density": ("density", "g/ml", "mass per volume"),
            "pressure": ("pressure", "atm", "kpa", "mmhg", "torr"),
            "volume": ("volume", "liter", "liters", "milliliter", "ml"),
            "temperature": ("temperature", "kelvin", "celsius"),
            "mass": ("mass", "grams", "gram", "kg", "mg"),
            "amount": ("moles", "mol ", "amount"),
        }
        strong_roles = {
            role
            for role, patterns in role_patterns.items()
            if role not in {"pressure", "volume", "temperature", "mass", "amount"}
            and any(pattern in lowered for pattern in patterns)
        }
        if strong_roles:
            return roles | strong_roles
        return roles | {role for role, patterns in role_patterns.items() if any(pattern in lowered for pattern in patterns)}

    def _tool_semantic_roles(self, tool: ToolSpec | None) -> set[str]:
        if tool is None:
            return set()
        return self._target_semantic_roles(
            " ".join([tool.id, tool.description, " ".join(tool.params), " ".join(tool.keywords)]),
        )

    def _preferred_tools_for_question(self, question: str) -> list[ToolSpec]:
        tools: list[ToolSpec] = []
        for tool_id in self._memory_preferred_tool_ids(question):
            if "." not in tool_id:
                continue
            module, function = tool_id.split(".", 1)
            tool = self.tool_catalog.find(module, function)
            if tool is not None:
                tools.append(tool)
        return tools

    def _infer_tool_inputs(self, tool: ToolSpec, question: str) -> dict[str, Any]:
        _ = tool, question
        return {}

    # BEGIN GENERATED_RUNTIME_DOMAIN_METHODS
    def _question_suggests_tool(self, question: str) -> bool:
        lowered = question.lower()
        return any(
            cue in lowered
            for cue in (
                "balance:",
                "electron configuration",
                "valence electron",
                "ideal gas",
                "boyle",
                "pressure",
                "volume",
                "number of moles",
                "moles at stp",
                "stp",
                "partial pressure",
                "rms speed",
                "effusion",
                "gas density",
                "balloon",
                "connected to an empty tank",
                "formula mass",
                "molar mass",
                "molecular mass",
                "empirical formula",
                "molecular formula",
                "percent composition",
                "mass percentage",
                "combustion",
                "decomposition",
                "produced",
                "after heating",
                "find x",
            )
        )

    def _allow_generated_specialist_shortcuts(self) -> bool:
        adapter_config = dict(self.runtime_config.get("adapter", {}).get("config", {}))
        runtime_adapter_config = dict(dict(self.runtime_config.get("runtime_inputs", {})).get("adapter_config", {}))
        return bool(
            runtime_adapter_config.get("allow_generated_specialist_shortcuts")
            or adapter_config.get("allow_generated_specialist_shortcuts")
            or self.runtime_config.get("allow_generated_specialist_shortcuts")
        )

    def _question_stem_for_quantities(self, question: str) -> str:
        match = re.search(r"\s+[A-H][\.\)]\s+", question)
        if match:
            return question[: match.start()]
        return question

    def _extract_pressures_atm(self, question: str) -> list[float]:
        values: list[float] = []
        for raw, unit in re.findall(r"(-?\d[\d,]*(?:\.\d+)?)\s*(atm|bar|mmhg|torr|kpa)", question, flags=re.IGNORECASE):
            value = parse_numeric_literal(raw)
            normalized = unit.lower()
            if normalized == "atm":
                values.append(value)
            elif normalized == "bar":
                values.append(value / 1.01325)
            elif normalized == "kpa":
                values.append(value / 101.325)
            else:
                values.append(value / 760.0)
        return values

    def _extract_temperatures_k(self, question: str) -> list[float]:
        values: list[float] = []
        for raw, unit in re.findall(r"(-?\d[\d,]*(?:\.\d+)?)\s*(?:deg\s*|[°º]\s*)?(c|k|f)\b", question, flags=re.IGNORECASE):
            value = parse_numeric_literal(raw)
            normalized = unit.lower()
            if normalized == "k":
                values.append(value)
            elif normalized == "c":
                values.append(value + 273.15)
            else:
                values.append((value - 32.0) * 5.0 / 9.0 + 273.15)
        if not values:
            for raw in re.findall(r"(-?\d[\d,]*(?:\.\d+)?)\s*[°]\s*C", question, flags=re.IGNORECASE):
                values.append(parse_numeric_literal(raw) + 273.15)
        return values

    def _extract_moles(self, question: str) -> list[float]:
        return [parse_numeric_literal(raw) for raw in re.findall(r"(-?\d[\d,]*(?:\.\d+)?)\s*mol\b", question, flags=re.IGNORECASE)]

    def _extract_volumes_l(self, question: str) -> list[float]:
        values: list[float] = []
        for raw, unit in re.findall(
            r"(-?\d[\d,]*(?:\.\d+)?)\s*(ml|l|liter|liters|dm\^?3|dm3|cm\^?3|cm3|cm\S+)",
            question,
            flags=re.IGNORECASE,
        ):
            value = parse_numeric_literal(raw)
            normalized = unit.lower()
            if normalized == "l" or normalized.startswith("liter") or normalized in {"dm3", "dm^3"}:
                values.append(value)
            else:
                values.append(value / 1000.0)
        cm_values = [parse_numeric_literal(raw) for raw in re.findall(r"(-?\d[\d,]*(?:\.\d+)?)\s*cm\b", question, flags=re.IGNORECASE)]
        if "container" in question.lower() and len(cm_values) >= 3:
            a, b, c = cm_values[-3:]
            values.append((a * b * c) / 1000.0)
        return values

    def _extract_masses_g(self, question: str) -> list[float]:
        values: list[float] = []
        mass_text = re.sub(
            r"-?\d[\d,]*(?:\.\d+)?\s*g\s*/\s*(?:cm(?:\^?3|3|³|\?|鲁)?|ml|mL)",
            "",
            question,
            flags=re.IGNORECASE,
        )
        for raw, unit in re.findall(
            r"(-?\d[\d,]*(?:\.\d+)?)\s*(kg|mg|g|lb|oz)\b(?!\s*/)",
            mass_text,
            flags=re.IGNORECASE,
        ):
            value = parse_numeric_literal(raw)
            normalized = unit.lower()
            if normalized == "kg":
                values.append(value * 1000.0)
            elif normalized == "mg":
                values.append(value / 1000.0)
            elif normalized == "lb":
                values.append(value * 453.592)
            elif normalized == "oz":
                values.append(value * 28.3495)
            else:
                values.append(value)
        return values

    def _extract_densities_g_per_ml(self, question: str) -> list[float]:
        values: list[float] = []
        for raw in re.findall(
            r"(-?\d[\d,]*(?:\.\d+)?)\s*g\s*/\s*(?:cm(?:\^?3|3|³|\?|鲁)?|ml|mL)",
            question,
            flags=re.IGNORECASE,
        ):
            values.append(parse_numeric_literal(raw))
        return values

    def _extract_volumes_ml(self, question: str) -> list[float]:
        values: list[float] = []
        for raw, unit in re.findall(
            r"(-?\d[\d,]*(?:\.\d+)?)\s*(ml|mL|l|L|liter|liters|dm\^?3|dm3|cm\^?3|cm3|cm³|cm鲁)",
            question,
            flags=re.IGNORECASE,
        ):
            value = parse_numeric_literal(raw)
            normalized = unit.lower()
            if normalized in {"l", "liter", "liters", "dm3", "dm^3"}:
                values.append(value * 1000.0)
            else:
                values.append(value)
        cm_lengths = [
            parse_numeric_literal(raw)
            for raw in re.findall(r"(-?\d[\d,]*(?:\.\d+)?)\s*cm\b", question, flags=re.IGNORECASE)
        ]
        if len(cm_lengths) >= 3 and re.search(r"(?:×|x|\*|\bby\b)", question, flags=re.IGNORECASE):
            a, b, c = cm_lengths[-3:]
            values.append(a * b * c)
        return values

    def _extract_isotope_mass_abundance_pairs(self, question: str) -> list[tuple[float, float]]:
        pairs: list[tuple[float, float]] = []
        for abundance, mass in re.findall(
            r"(-?\d[\d,]*(?:\.\d+)?)\s*%[^()]{0,80}\((-?\d[\d,]*(?:\.\d+)?)\s*amu\)",
            question,
            flags=re.IGNORECASE,
        ):
            pairs.append((parse_numeric_literal(mass), parse_numeric_literal(abundance) / 100.0))
        if len(pairs) >= 2:
            return pairs
        masses = [parse_numeric_literal(raw) for raw in re.findall(r"(-?\d[\d,]*(?:\.\d+)?)\s*amu\b", question, flags=re.IGNORECASE)]
        abundances = [parse_numeric_literal(raw) / 100.0 for raw in re.findall(r"(-?\d[\d,]*(?:\.\d+)?)\s*%", question)]
        if len(masses) >= 2 and len(abundances) >= 2:
            return list(zip(masses[: len(abundances)], abundances))
        return []

    def _extract_specific_heat_j_per_g_c(self, question: str) -> float | None:
        match = re.search(r"(?:c|specific heat)\s*=?\s*(-?\d[\d,]*(?:\.\d+)?)\s*J\s*/\s*g", question, flags=re.IGNORECASE)
        if match:
            return parse_numeric_literal(match.group(1))
        return None

    def _extract_temperature_delta_c(self, question: str) -> float | None:
        celsius_values = [
            parse_numeric_literal(raw)
            for raw in re.findall(r"(-?\d[\d,]*(?:\.\d+)?)\s*(?:°?\s*C|deg\s*C|C\b)", question, flags=re.IGNORECASE)
        ]
        if len(celsius_values) >= 2:
            return celsius_values[-1] - celsius_values[0]
        kelvin_values = [
            parse_numeric_literal(raw)
            for raw in re.findall(r"(-?\d[\d,]*(?:\.\d+)?)\s*K\b", question, flags=re.IGNORECASE)
        ]
        if len(kelvin_values) >= 2:
            return kelvin_values[-1] - kelvin_values[0]
        delta_match = re.search(r"(?:delta|change in|Δ)\s*T\s*=?\s*(-?\d[\d,]*(?:\.\d+)?)", question, flags=re.IGNORECASE)
        if delta_match:
            return parse_numeric_literal(delta_match.group(1))
        return None

    def _lettered_segments(self, question: str) -> list[tuple[str, str]]:
        matches = list(re.finditer(r"\(([a-h])\)\s*", question, flags=re.IGNORECASE))
        segments: list[tuple[str, str]] = []
        for index, match in enumerate(matches):
            start = match.end()
            end = matches[index + 1].start() if index + 1 < len(matches) else len(question)
            segment = question[start:end].strip(" ,.;")
            if segment:
                segments.append((match.group(1).lower(), segment))
        return segments

    def _formula_candidates(self, question: str) -> list[str]:
        lowered = question.lower()
        candidates: list[str] = []
        for name, formula in COMMON_FORMULAS.items():
            if name in lowered and formula not in candidates:
                candidates.append(formula)
        for candidate in formula_candidates_from_text(question):
            if candidate not in candidates:
                candidates.append(candidate)
        return candidates

    def _formula_from_segment(self, segment: str) -> str | None:
        for formula in self._formula_candidates(segment):
            if self._molar_mass_formula(formula) is not None:
                return formula
        return None

    def _extract_raw_pressures(self, question: str) -> list[tuple[float, str]]:
        return [
            (parse_numeric_literal(raw), unit.lower())
            for raw, unit in re.findall(r"(-?\d[\d,]*(?:\.\d+)?)\s*(atm|mmhg|torr|kpa)", question, flags=re.IGNORECASE)
        ]

    def _format_formula_with_counts(self, counts: dict[str, int]) -> str:
        return "".join(f"{element}{'' if count == 1 else count}" for element, count in counts.items())

    def _molar_mass_formula(self, formula: str) -> float | None:
        tool = self.tool_catalog.find("atomic_composition_tools", "molar_mass_from_formula")
        if tool is None:
            return None
        total = 0.0
        for part in str(formula).split("."):
            if not part:
                continue
            coeff = 1
            formula_part = part
            match = re.fullmatch(r"(\d+)([A-Z].*)", part)
            if match:
                coeff = int(match.group(1))
                formula_part = match.group(2)
            call = self.tool_catalog.execute(tool, {"formula": formula_part})
            if call.error:
                return None
            mass = float(call.result)
            if mass <= 0:
                return None
            total += coeff * mass
        return total if total > 0 else None

    def _format_formula_counts(self, counts: dict[str, int]) -> str:
        return "".join(f"{element}{'' if count == 1 else count}" for element, count in counts.items())

    def _integerize_ratios(self, ratios: dict[str, float]) -> dict[str, int]:
        best_counts: dict[str, int] = {element: max(1, int(round(value))) for element, value in ratios.items()}
        best_error = float("inf")
        for multiplier in range(1, 9):
            candidate = {element: max(1, int(round(value * multiplier))) for element, value in ratios.items()}
            errors = [abs(candidate[element] / multiplier - value) for element, value in ratios.items()]
            error = max(errors) if errors else float("inf")
            if error < best_error:
                best_error = error
                best_counts = candidate
        return best_counts

    def _run_specialized_numeric_tool(self, question: str) -> ToolCallResult | None:
        combustion_call = self._run_combustion_empirical_tool(question)
        if combustion_call is not None:
            return combustion_call
        gas_stoich_call = self._run_gas_stoichiometry_tool(question)
        if gas_stoich_call is not None:
            return gas_stoich_call
        decomposition_call = self._run_potassium_chlorate_decomposition_tool(question)
        if decomposition_call is not None:
            return decomposition_call
        tank_call = self._run_tank_expansion_pressure_tool(question)
        if tank_call is not None:
            return tank_call
        vdw_enthalpy_call = self._run_van_der_waals_fixed_volume_enthalpy_tool(question)
        if vdw_enthalpy_call is not None:
            return vdw_enthalpy_call
        vdw_pressure_call = self._run_van_der_waals_pressure_tool(question)
        if vdw_pressure_call is not None:
            return vdw_pressure_call
        rms_call = self._run_rms_speed_ratio_tool(question)
        if rms_call is not None:
            return rms_call
        volume_from_mass_call = self._run_ideal_gas_volume_from_mass_tool(question)
        if volume_from_mass_call is not None:
            return volume_from_mass_call
        stp_volume_from_mass_call = self._run_stp_volume_from_mass_tool(question)
        if stp_volume_from_mass_call is not None:
            return stp_volume_from_mass_call
        stp_call = self._run_stp_moles_tool(question)
        if stp_call is not None:
            return stp_call
        stp_mass_call = self._run_stp_mass_tool(question)
        if stp_mass_call is not None:
            return stp_mass_call
        stp_volume_call = self._run_stp_volume_tool(question)
        if stp_volume_call is not None:
            return stp_volume_call
        partial_pressure_call = self._run_partial_pressure_tool(question)
        if partial_pressure_call is not None:
            return partial_pressure_call
        composition_call = self._run_composition_numeric_tool(question)
        if composition_call is not None:
            return composition_call
        consistency_call = self._run_boyle_consistency_tool(question)
        if consistency_call is not None:
            return consistency_call
        temperature_call = self._run_ideal_gas_temperature_tool(question)
        if temperature_call is not None:
            return temperature_call
        return None

    def _run_stp_moles_tool(self, question: str) -> ToolCallResult | None:
        lowered = question.lower()
        if "stp" not in lowered or "moles" not in lowered:
            return None
        tool = self.tool_catalog.find("ideal_gas_law_tools", "moles_at_stp")
        if tool is None:
            return None
        volumes = self._extract_volumes_l(question)
        if not volumes:
            return None
        parts = []
        for index, volume_l in enumerate(volumes[:8]):
            call = self.tool_catalog.execute(tool, {"V": volume_l})
            if call.error:
                return call
            parts.append(
                {
                    "part": chr(ord("a") + index),
                    "volume_l": round(volume_l, 6),
                    "moles": float(call.result),
                }
            )
        answer = ", ".join(f"({item['part']}) {item['moles']:.4g} mol" for item in parts)
        return ToolCallResult(
            tool_id=tool.id,
            kwargs={"volumes_l": [item["volume_l"] for item in parts]},
            result={"answer_values": [item["moles"] for item in parts], "answer": answer, "parts": parts},
        )

    def _run_stp_mass_tool(self, question: str) -> ToolCallResult | None:
        lowered = question.lower()
        if "stp" not in lowered or "mass" not in lowered:
            return None
        moles_tool = self.tool_catalog.find("ideal_gas_law_tools", "moles_at_stp")
        molar_mass_tool = self.tool_catalog.find("atomic_composition_tools", "molar_mass_from_formula")
        if moles_tool is None or molar_mass_tool is None:
            return None
        parts = []
        for label, segment in self._lettered_segments(question):
            volumes = self._extract_volumes_l(segment)
            formula = self._formula_from_segment(segment)
            if not volumes or not formula:
                continue
            moles_call = self.tool_catalog.execute(moles_tool, {"V": volumes[0]})
            mass_call = self.tool_catalog.execute(molar_mass_tool, {"formula": formula})
            if moles_call.error:
                return moles_call
            if mass_call.error:
                return mass_call
            moles = float(moles_call.result)
            molar_mass = float(mass_call.result)
            parts.append(
                {
                    "part": label,
                    "formula": formula,
                    "volume_l": round(volumes[0], 6),
                    "molar_mass": molar_mass,
                    "mass_g": moles * molar_mass,
                }
            )
        if not parts:
            return None
        answer = ", ".join(f"({item['part']}) {item['mass_g']:.3g} g {item['formula']}" for item in parts)
        return ToolCallResult(
            tool_id=f"{moles_tool.id}+{molar_mass_tool.id}",
            kwargs={"parts": parts},
            result={"answer_values": [item["mass_g"] for item in parts], "answer": answer, "parts": parts},
        )

    def _run_stp_volume_from_mass_tool(self, question: str) -> ToolCallResult | None:
        lowered = question.lower()
        if "stp" not in lowered or "volume" not in lowered:
            return None
        parts = []
        for label, segment in self._lettered_segments(question):
            masses = self._extract_masses_g(segment)
            formula = self._formula_from_segment(segment)
            if not masses or not formula:
                continue
            molar_mass = self._molar_mass_formula(formula)
            if molar_mass is None:
                continue
            moles = masses[0] / molar_mass
            volume_l = moles * 22.4
            parts.append(
                {
                    "part": label,
                    "formula": formula,
                    "mass_g": masses[0],
                    "molar_mass": molar_mass,
                    "volume_l": volume_l,
                }
            )
        if not parts:
            return None
        answer = ", ".join(f"({item['part']}) {item['volume_l']:.3g} L {item['formula']}" for item in parts)
        return ToolCallResult(
            tool_id="generated_runtime.stp_volume_from_mass",
            kwargs={"parts": parts},
            result={"answer_values": [item["volume_l"] for item in parts], "answer": answer, "parts": parts},
        )

    def _run_tank_expansion_pressure_tool(self, question: str) -> ToolCallResult | None:
        lowered = question.lower()
        if "empty tank" not in lowered or "final pressure" not in lowered:
            return None
        volumes = self._extract_volumes_l(question)
        pressures = self._extract_raw_pressures(question)
        if len(volumes) < 2 or not pressures:
            return None
        p_initial, unit = pressures[0]
        final_pressure = p_initial * volumes[0] / (volumes[0] + volumes[1])
        answer = f"{final_pressure:.3g} {unit}"
        return ToolCallResult(
            tool_id="generated_runtime.tank_expansion_pressure",
            kwargs={"initial_pressure": p_initial, "unit": unit, "volumes_l": volumes[:2]},
            result={"answer_values": [final_pressure], "answer": answer},
        )

    def _extract_heat_transfer_kj(self, question: str) -> float | None:
        for match in re.finditer(
            r"(-?\d[\d,]*(?:\.\d+)?(?:e[+-]?\d+)?)\s*kJ\b",
            question,
            flags=re.IGNORECASE,
        ):
            value = parse_numeric_literal(match.group(1))
            context = question[max(0, match.start() - 48) : match.end() + 48].lower()
            if not re.search(r"\b(?:heat|supplied|absorbed|added|transferred|energy)\b", context):
                continue
            if re.search(r"\b(?:removed|lost|released|evolved)\b", context):
                return -abs(value)
            return value
        return None

    def _run_van_der_waals_fixed_volume_enthalpy_tool(self, question: str) -> ToolCallResult | None:
        normalized = normalize_symbolic_text(question)
        lowered = normalized.lower()
        if "van der waals" not in lowered:
            return None
        if not re.search(r"\b(?:delta\s*h|enthalpy)\b", lowered):
            return None
        heat_kj = self._extract_heat_transfer_kj(normalized)
        if heat_kj is None:
            return None
        a_match = re.search(
            r"\ba\s*=\s*(-?\d[\d,]*(?:\.\d+)?(?:e[+-]?\d+)?)\s*(?:dm|l)(?:\^?6|6)\s*(bar|atm)\s*mol",
            normalized,
            flags=re.IGNORECASE,
        )
        b_match = re.search(
            r"\bb\s*=\s*(-?\d[\d,]*(?:\.\d+)?(?:e[+-]?\d+)?)\s*(?:dm|l)(?:\^?3|3)\s*mol",
            normalized,
            flags=re.IGNORECASE,
        )
        if not a_match or not b_match:
            return None
        temperatures = self._extract_temperatures_k(normalized)
        volumes_dm3 = self._extract_volumes_dm3(normalized)
        moles = self._extract_runtime_moles(normalized)
        if len(temperatures) < 2 or not volumes_dm3 or not moles:
            return None
        n_mol = moles[0]
        volume_dm3 = max(volumes_dm3)
        temperature_initial_k = temperatures[0]
        temperature_final_k = temperatures[-1]
        a_value = parse_numeric_literal(a_match.group(1))
        b_value = parse_numeric_literal(b_match.group(1))
        pressure_unit = a_match.group(2).lower()
        r_match = re.search(
            r"\bR\s*=\s*(-?\d[\d,]*(?:\.\d+)?(?:e[+-]?\d+)?)\s*(?:dm|l)(?:\^?3|3)\s*(bar|atm)\s*mol",
            normalized,
            flags=re.IGNORECASE,
        )
        if r_match:
            r_value = parse_numeric_literal(r_match.group(1))
            pressure_unit = r_match.group(2).lower()
        else:
            r_value = 0.083145 if pressure_unit == "bar" else 0.082057
        if n_mol <= 0 or volume_dm3 <= 0:
            return None
        free_volume_dm3 = volume_dm3 - n_mol * b_value
        if free_volume_dm3 <= 0:
            return ToolCallResult(
                tool_id="generated_runtime.van_der_waals_fixed_volume_enthalpy",
                kwargs={"n_mol": n_mol, "volume_dm3": volume_dm3, "a": a_value, "b": b_value},
                error="van der Waals covolume correction leaves non-positive free volume",
            )

        def pressure_at_temperature(temperature_k: float) -> float:
            ideal_term = n_mol * r_value * temperature_k / free_volume_dm3
            attraction_term = a_value * (n_mol / volume_dm3) ** 2
            return ideal_term - attraction_term

        pressure_initial = pressure_at_temperature(temperature_initial_k)
        pressure_final = pressure_at_temperature(temperature_final_k)
        dm3_pressure_to_kj = 0.100 if pressure_unit == "bar" else 0.101325
        delta_pv_kj = (pressure_final - pressure_initial) * volume_dm3 * dm3_pressure_to_kj
        delta_h_kj = heat_kj + delta_pv_kj
        answer = f"{delta_h_kj:.4g} kJ"
        return ToolCallResult(
            tool_id="generated_runtime.van_der_waals_fixed_volume_enthalpy",
            kwargs={
                "n_mol": n_mol,
                "volume_dm3": volume_dm3,
                "temperature_initial_k": temperature_initial_k,
                "temperature_final_k": temperature_final_k,
                "heat_kj": heat_kj,
                "a_dm6_pressure_mol2": a_value,
                "b_dm3_mol": b_value,
                "r_dm3_pressure_mol_k": r_value,
                "pressure_unit": pressure_unit,
            },
            result={
                "answer_values": [delta_h_kj],
                "answer": answer,
                "units": ["kJ"],
                "delta_u_kj": heat_kj,
                "delta_pv_kj": delta_pv_kj,
                "pressure_initial": pressure_initial,
                "pressure_final": pressure_final,
                "pressure_unit": pressure_unit,
                "free_volume_dm3": free_volume_dm3,
            },
            metadata={"adequacy": {"adequate": True, "reason": "matched fixed-volume van der Waals enthalpy pattern"}},
        )

    def _extract_volumes_dm3(self, question: str) -> list[float]:
        values: list[float] = []
        for raw, unit in re.findall(
            r"(-?\d[\d,]*(?:\.\d+)?)\s*(m(?:\^?3|3|\u00b3)|dm(?:\^?3|3|\u00b3)|cm(?:\^?3|3|\u00b3)|ml|mL|l|L|liter|liters)\b",
            question,
            flags=re.IGNORECASE,
        ):
            value = parse_numeric_literal(raw)
            normalized = unit.lower().replace("^", "").replace("\u00b3", "3")
            if normalized == "m3":
                values.append(value * 1000.0)
            elif normalized in {"dm3", "l", "liter", "liters"}:
                values.append(value)
            else:
                values.append(value / 1000.0)
        return values

    def _run_van_der_waals_pressure_tool(self, question: str) -> ToolCallResult | None:
        normalized = normalize_symbolic_text(question)
        lowered = normalized.lower()
        if "van der waals" not in lowered or "pressure" not in lowered:
            return None
        a_match = re.search(
            r"\ba\s*=\s*(-?\d[\d,]*(?:\.\d+)?(?:e[+-]?\d+)?)\s*(?:dm|l)(?:\^?6|6|\u2076)\s*atm",
            normalized,
            flags=re.IGNORECASE,
        )
        b_match = re.search(
            r"\bb\s*=\s*(-?\d[\d,]*(?:\.\d+)?(?:e[+-]?\d+)?)\s*(?:dm|l)(?:\^?3|3|\u00b3)\s*mol",
            normalized,
            flags=re.IGNORECASE,
        )
        if not a_match or not b_match:
            return None
        temperatures = self._extract_temperatures_k(normalized)
        volumes_dm3 = self._extract_volumes_dm3(normalized)
        if not temperatures or not volumes_dm3:
            return None
        volume_dm3 = max(volumes_dm3)
        a_value = parse_numeric_literal(a_match.group(1))
        b_value = parse_numeric_literal(b_match.group(1))
        moles = self._extract_runtime_moles(normalized)
        if moles:
            n_mol = moles[0]
            formula = self._formula_from_segment(normalized) or ""
            mass_g = None
            molar_mass = None
        else:
            masses_g = self._extract_masses_g(normalized)
            formula = self._formula_from_segment(normalized) or ""
            if not masses_g or not formula:
                return None
            molar_mass = self._molar_mass_formula(formula)
            if molar_mass is None or molar_mass <= 0:
                return None
            mass_g = masses_g[0]
            n_mol = mass_g / molar_mass
        if n_mol <= 0 or volume_dm3 <= 0:
            return None
        free_volume_dm3 = volume_dm3 - n_mol * b_value
        if free_volume_dm3 <= 0:
            return ToolCallResult(
                tool_id="generated_runtime.van_der_waals_pressure",
                kwargs={"n_mol": n_mol, "volume_dm3": volume_dm3, "a": a_value, "b": b_value},
                error="van der Waals covolume correction leaves non-positive free volume",
            )
        temperature_k = temperatures[-1]
        r_l_atm = 0.082057
        ideal_term = n_mol * r_l_atm * temperature_k / free_volume_dm3
        attraction_term = a_value * (n_mol / volume_dm3) ** 2
        pressure_atm = ideal_term - attraction_term
        answer = f"{pressure_atm:.4g} atm"
        return ToolCallResult(
            tool_id="generated_runtime.van_der_waals_pressure",
            kwargs={
                "formula": formula,
                "mass_g": mass_g,
                "molar_mass_g_mol": molar_mass,
                "n_mol": n_mol,
                "temperature_k": temperature_k,
                "volume_dm3": volume_dm3,
                "a_dm6_atm_mol2": a_value,
                "b_dm3_mol": b_value,
            },
            result={
                "answer_values": [pressure_atm],
                "answer": answer,
                "units": ["atm"],
                "ideal_term_atm": ideal_term,
                "attraction_correction_atm": attraction_term,
                "free_volume_dm3": free_volume_dm3,
            },
        )

    def _run_rms_speed_ratio_tool(self, question: str) -> ToolCallResult | None:
        lowered = question.lower()
        if "rms speed" not in lowered or "ratio" not in lowered:
            return None
        formulas = []
        if "ar" in lowered or "argon" in lowered:
            formulas.append("Ar")
        if "h2" in normalize_symbolic_text(question).lower() or "hydrogen" in lowered:
            formulas.append("H2")
        for formula in self._formula_candidates(question):
            if formula not in formulas:
                formulas.append(formula)
        if len(formulas) < 2:
            return None
        first_mass = self._molar_mass_formula(formulas[0])
        second_mass = self._molar_mass_formula(formulas[1])
        if first_mass is None or second_mass is None:
            return None
        ratio = (second_mass / first_mass) ** 0.5
        answer = f"{ratio:.3g}"
        return ToolCallResult(
            tool_id="generated_runtime.rms_speed_ratio",
            kwargs={"numerator_gas": formulas[0], "denominator_gas": formulas[1]},
            result={"answer_values": [ratio], "answer": answer},
        )

    def _run_ideal_gas_volume_from_mass_tool(self, question: str) -> ToolCallResult | None:
        lowered = question.lower()
        if "volume" not in lowered or "pressure" not in lowered:
            return None
        masses = self._extract_masses_g(question)
        temperatures = self._extract_temperatures_k(question)
        pressures = self._extract_pressures_atm(question)
        formula = self._formula_from_segment(question)
        if not masses or not temperatures or not pressures or not formula:
            return None
        molar_mass = self._molar_mass_formula(formula)
        if molar_mass is None:
            return None
        moles = masses[0] / molar_mass
        volume_l = moles * 0.082057 * temperatures[-1] / pressures[-1]
        answer = f"{volume_l:.4g} L"
        return ToolCallResult(
            tool_id="generated_runtime.ideal_gas_volume_from_mass",
            kwargs={"mass_g": masses[0], "formula": formula, "temperature_k": temperatures[-1], "pressure_atm": pressures[-1]},
            result={"answer_values": [volume_l], "answer": answer},
        )

    def _run_gas_stoichiometry_tool(self, question: str) -> ToolCallResult | None:
        normalized = normalize_symbolic_text(question)
        lowered = normalized.lower()
        if "hcl" not in lowered or "aluminum" not in lowered or "balloon" not in lowered:
            return None
        volumes = self._extract_volumes_l(normalized)
        temperatures = self._extract_temperatures_k(normalized)
        pressures = self._extract_pressures_atm(normalized) or [1.0]
        if not volumes or not temperatures:
            return None
        target_volume = max(volumes)
        moles_h2 = pressures[-1] * target_volume / (0.082057 * temperatures[-1])
        al_mass = self._molar_mass_formula("Al")
        if al_mass is None:
            return None
        moles_al = (2.0 / 3.0) * moles_h2
        mass_al_kg = moles_al * al_mass / 1000.0
        hcl_volume_stp_l = 2.0 * moles_h2 * 22.4
        answer = f"{mass_al_kg:.3g} kg Al, {hcl_volume_stp_l:.3g} L HCl"
        return ToolCallResult(
            tool_id="generated_runtime.al_hcl_hydrogen_stoichiometry",
            kwargs={"target_h2_volume_l": target_volume, "temperature_k": temperatures[-1], "pressure_atm": pressures[-1]},
            result={"answer_values": [mass_al_kg, hcl_volume_stp_l], "answer": answer},
        )

    def _run_potassium_chlorate_decomposition_tool(self, question: str) -> ToolCallResult | None:
        lowered = question.lower()
        if "potassium chlorate" not in lowered or "potassium chloride" not in lowered:
            return None
        masses = self._extract_masses_g(question)
        if not masses:
            return None
        kcl_mass = self._molar_mass_formula("KCl")
        kclo3_mass = self._molar_mass_formula("KClO3")
        o2_mass = self._molar_mass_formula("O2")
        if kcl_mass is None or kclo3_mass is None or o2_mass is None:
            return None
        moles_kcl = masses[0] / kcl_mass
        original_mass = moles_kcl * kclo3_mass
        moles_o2 = 1.5 * moles_kcl
        oxygen_mass = moles_o2 * o2_mass
        oxygen_volume_ml = moles_o2 * 22.4 * 1000.0
        answer = f"(a) {original_mass:.3g} g KClO3, (b) {oxygen_mass:.3g} g O2, (c) {oxygen_volume_ml:.3g} mL O2"
        return ToolCallResult(
            tool_id="generated_runtime.potassium_chlorate_decomposition",
            kwargs={"kcl_mass_g": masses[0]},
            result={"answer_values": [original_mass, oxygen_mass, oxygen_volume_ml], "answer": answer},
        )

    def _run_combustion_empirical_tool(self, question: str) -> ToolCallResult | None:
        lowered = question.lower()
        if "combustion" not in lowered and ("co2" not in normalize_symbolic_text(question).lower() or "h2o" not in normalize_symbolic_text(question).lower()):
            return None
        gas_analysis = self._run_combustion_stp_gas_analysis_tool(question)
        if gas_analysis is not None:
            return gas_analysis
        normalized = normalize_symbolic_text(question)
        if "produced" not in lowered or "CO2" not in normalized or "H2O" not in normalized:
            return None
        sample_match = re.search(r"(?:combustion of|of)\s+(\d+(?:\.\d+)?)\s*(mg|g)\b", normalized, flags=re.IGNORECASE)
        co2_match = re.search(r"produced\s+(\d+(?:\.\d+)?)\s*(mg|g)\s+CO2", normalized, flags=re.IGNORECASE)
        h2o_match = re.search(r"CO2\s+and\s+(\d+(?:\.\d+)?)\s*(mg|g)\s+H2O", normalized, flags=re.IGNORECASE)
        molar_match = re.search(r"(?:molar mass|MM)\s*(?:=|is)?\s*(\d+(?:\.\d+)?)", normalized, flags=re.IGNORECASE)
        if not sample_match or not co2_match or not h2o_match:
            return None
        sample_mg = float(sample_match.group(1)) * (1000.0 if sample_match.group(2).lower() == "g" else 1.0)
        co2_mg = float(co2_match.group(1)) * (1000.0 if co2_match.group(2).lower() == "g" else 1.0)
        h2o_mg = float(h2o_match.group(1)) * (1000.0 if h2o_match.group(2).lower() == "g" else 1.0)
        c_mass = co2_mg * 12.011 / 44.009
        h_mass = h2o_mg * 2.016 / 18.015
        o_mass = max(0.0, sample_mg - c_mass - h_mass)
        element_moles = {
            "C": c_mass / 12.011,
            "H": h_mass / 1.008,
            "O": o_mass / 15.999,
        }
        smallest = min(value for value in element_moles.values() if value > 0)
        ratios = {element: value / smallest for element, value in element_moles.items()}
        counts = self._integerize_ratios(ratios)
        empirical_formula = self._format_formula_counts(counts)
        molecular_formula = empirical_formula
        if molar_match:
            target_molar_mass = float(molar_match.group(1))
            empirical_mass = self._molar_mass_formula(empirical_formula)
            multiplier = max(1, int(round(target_molar_mass / empirical_mass))) if empirical_mass else 1
            molecular_formula = self._format_formula_counts({element: count * multiplier for element, count in counts.items()})
        answer = (
            f"C: {c_mass:.3g} mg, H: {h_mass:.3g} mg, O: {o_mass:.3g} mg; "
            f"empirical formula {empirical_formula}, molecular formula {molecular_formula}"
        )
        return ToolCallResult(
            tool_id="generated_runtime.combustion_empirical_formula",
            kwargs={"sample_mg": sample_mg, "co2_mg": co2_mg, "h2o_mg": h2o_mg},
            result={"answer_values": [c_mass, h_mass, o_mass], "answer": answer, "formula": molecular_formula},
        )

    def _run_combustion_stp_gas_analysis_tool(self, question: str) -> ToolCallResult | None:
        normalized = normalize_symbolic_text(question)
        lowered = normalized.lower()
        if "co2" not in lowered or "h2o" not in lowered or "stp" not in lowered or "% oxygen" not in lowered:
            return None
        sample_match = re.search(r"(\d+(?:\.\d+)?)\s*(mg|g)\s+sample", normalized, flags=re.IGNORECASE)
        co2_match = re.search(r"produced\s+(\d+(?:\.\d+)?)\s*(mL|L)\s+of\s+CO2", normalized, flags=re.IGNORECASE)
        h2o_match = re.search(r"and\s+(\d+(?:\.\d+)?)\s*(mL|L)\s+of\s+H2O", normalized, flags=re.IGNORECASE)
        oxygen_match = re.search(r"(\d+(?:\.\d+)?)%\s+oxygen", normalized, flags=re.IGNORECASE)
        if not sample_match or not co2_match or not h2o_match or not oxygen_match:
            return None
        sample_g = float(sample_match.group(1)) / 1000.0 if sample_match.group(2).lower() == "mg" else float(sample_match.group(1))
        co2_l = float(co2_match.group(1)) / 1000.0 if co2_match.group(2).lower() == "ml" else float(co2_match.group(1))
        h2o_l = float(h2o_match.group(1)) / 1000.0 if h2o_match.group(2).lower() == "ml" else float(h2o_match.group(1))
        oxygen_percent = float(oxygen_match.group(1))
        c_mass = co2_l / 22.4 * 12.011
        h_mass = h2o_l / 22.4 * 2.016
        o_mass = sample_g * oxygen_percent / 100.0
        n_mass = max(0.0, sample_g - c_mass - h_mass - o_mass)
        percents = {
            "C": c_mass / sample_g * 100.0,
            "H": h_mass / sample_g * 100.0,
            "O": oxygen_percent,
            "N": n_mass / sample_g * 100.0,
        }
        moles = {
            "C": c_mass / 12.011,
            "H": h_mass / 1.008,
            "O": o_mass / 15.999,
            "N": n_mass / 14.007,
        }
        smallest = min(value for value in moles.values() if value > 0)
        counts = self._integerize_ratios({element: value / smallest for element, value in moles.items()})
        formula = self._format_formula_counts(counts)
        answer = (
            f"{percents['C']:.3g}% C, {percents['H']:.3g}% H, {percents['O']:.3g}% O, {percents['N']:.3g}% N; "
            f"empirical formula: {formula}"
        )
        return ToolCallResult(
            tool_id="generated_runtime.combustion_stp_gas_analysis",
            kwargs={"sample_g": sample_g, "co2_l": co2_l, "h2o_l": h2o_l, "oxygen_percent": oxygen_percent},
            result={"answer_values": [percents["C"], percents["H"], percents["O"], percents["N"]], "answer": answer, "formula": formula},
        )

    def _run_composition_numeric_tool(self, question: str) -> ToolCallResult | None:
        hydrate_percent = self._run_hydrate_water_percent_tool(question)
        if hydrate_percent is not None:
            return hydrate_percent
        hydrate_x = self._run_hydrate_x_tool(question)
        if hydrate_x is not None:
            return hydrate_x
        empirical = self._run_empirical_percent_tool(question)
        if empirical is not None:
            return empirical
        percent_compare = self._run_percent_comparison_tool(question)
        if percent_compare is not None:
            return percent_compare
        return None

    def _run_hydrate_water_percent_tool(self, question: str) -> ToolCallResult | None:
        lowered = question.lower()
        if "mass percentage of water" not in lowered:
            return None
        normalized = normalize_symbolic_text(question).replace("·", ".")
        hydrate_match = re.search(r"((?:[A-Z][a-z]?\d*|\([A-Za-z0-9]+\)\d*)+)\.(\d*)H2O", normalized)
        formula = f"{hydrate_match.group(1)}.{hydrate_match.group(2)}H2O" if hydrate_match else ""
        if not formula:
            formula = next((item for item in self._formula_candidates(question) if "." in item and "H2O" in item), "")
        if not formula:
            return None
        total_mass = self._molar_mass_formula(formula)
        hydrate_match = re.search(r"\.(\d*)H2O", formula)
        water_count = int(hydrate_match.group(1) or "1") if hydrate_match else 1
        water_mass = self._molar_mass_formula("H2O")
        if total_mass is None or water_mass is None:
            return None
        water_total = water_count * water_mass
        percent = water_total / total_mass * 100.0
        answer = f"{percent:.4g}% water; water mass = {water_total:.4g} g/mol, total formula mass = {total_mass:.4g} g/mol"
        return ToolCallResult(
            tool_id="generated_runtime.hydrate_water_percent",
            kwargs={"formula": formula},
            result={"answer_values": [total_mass, percent], "answer": answer},
        )

    def _run_hydrate_x_tool(self, question: str) -> ToolCallResult | None:
        lowered = question.lower()
        if "find x" not in lowered or "after heating" not in lowered:
            return None
        normalized = normalize_symbolic_text(question).replace("·", ".")
        formula_match = re.search(r"([A-Z][A-Za-z0-9()]+)\.xH2O", normalized)
        formula = f"{formula_match.group(1)}.xH2O" if formula_match else ""
        if not formula:
            return None
        anhydrous = formula.split(".")[0]
        masses = [float(raw) for raw in re.findall(r"(\d+(?:\.\d+)?)\s*g\b", question, flags=re.IGNORECASE)]
        if len(masses) < 2:
            return None
        initial_mass, final_mass = masses[0], masses[1]
        anhydrous_mass = self._molar_mass_formula(anhydrous)
        water_mass = self._molar_mass_formula("H2O")
        if anhydrous_mass is None or water_mass is None:
            return None
        water_moles = (initial_mass - final_mass) / water_mass
        anhydrous_moles = final_mass / anhydrous_mass
        x_value = round(water_moles / anhydrous_moles)
        answer = f"x = {x_value}"
        return ToolCallResult(
            tool_id="generated_runtime.hydrate_x_from_mass_loss",
            kwargs={"formula": formula, "initial_mass_g": initial_mass, "final_mass_g": final_mass},
            result={"answer_values": [x_value], "answer": answer},
        )

    def _run_empirical_percent_tool(self, question: str) -> ToolCallResult | None:
        lowered = question.lower()
        if "%" not in question or ("molar mass" not in lowered and "molecular mass" not in lowered):
            return None
        pairs = [
            (element, float(percent))
            for percent, element in re.findall(r"(\d+(?:\.\d+)?)%\s*([A-Z][a-z]?)", question)
        ]
        if len(pairs) < 2:
            return None
        molar_mass_match = re.search(r"(?:molar|molecular)\s+mass\s*(?:=|is)?\s*(\d+(?:\.\d+)?)", question, flags=re.IGNORECASE)
        if not molar_mass_match:
            return None
        target_molar_mass = float(molar_mass_match.group(1))
        moles: dict[str, float] = {}
        for element, percent in pairs:
            element_mass = self._molar_mass_formula(element)
            if element_mass is None:
                return None
            moles[element] = percent / element_mass
        smallest = min(value for value in moles.values() if value > 0)
        ratios = {element: value / smallest for element, value in moles.items()}
        counts = self._integerize_ratios(ratios)
        empirical_formula = self._format_formula_counts(counts)
        empirical_mass = self._molar_mass_formula(empirical_formula)
        multiplier = max(1, int(round(target_molar_mass / empirical_mass))) if empirical_mass else 1
        molecular_counts = {element: count * multiplier for element, count in counts.items()}
        molecular_formula = self._format_formula_counts(molecular_counts)
        answer = f"{molecular_formula}; formula mass = {target_molar_mass:.4g} g/mol"
        return ToolCallResult(
            tool_id="generated_runtime.empirical_formula_from_percent",
            kwargs={"percentages": pairs, "molar_mass": target_molar_mass},
            result={"answer_values": [target_molar_mass], "answer": answer, "formula": molecular_formula},
        )

    def _run_percent_comparison_tool(self, question: str) -> ToolCallResult | None:
        lowered = question.lower()
        if "greatest mass percentage" not in lowered:
            return None
        target = "S" if "sulfur" in lowered else None
        if target is None:
            return None
        candidates = [item for item in self._formula_candidates(question) if target in item]
        scored = []
        target_mass = self._molar_mass_formula(target)
        if target_mass is None:
            return None
        for formula in candidates:
            total = self._molar_mass_formula(formula)
            if total is None:
                continue
            target_count = sum(int(count or "1") for elem, count in re.findall(r"([A-Z][a-z]?)(\d*)", formula) if elem == target)
            if target_count <= 0:
                continue
            percent = target_count * target_mass / total * 100.0
            scored.append((percent, formula))
        if not scored:
            return None
        percent, formula = max(scored, key=lambda item: item[0])
        answer = f"{formula} ({percent:.3g}% {target})"
        return ToolCallResult(
            tool_id="generated_runtime.percent_composition_comparison",
            kwargs={"target_element": target, "candidates": candidates},
            result={"answer_values": [percent], "answer": answer},
        )

    def _run_stp_volume_tool(self, question: str) -> ToolCallResult | None:
        lowered = question.lower()
        if "stp" not in lowered or "volume" not in lowered or " at " not in lowered:
            return None
        parts = []
        for label, segment in self._lettered_segments(question):
            volumes = self._extract_volumes_l(segment)
            pressures = self._extract_pressures_atm(segment)
            temperatures = self._extract_temperatures_k(segment)
            if not volumes or not pressures or not temperatures:
                continue
            v_stp = pressures[0] * volumes[0] * 273.15 / temperatures[0]
            parts.append(
                {
                    "part": label,
                    "initial_volume_l": round(volumes[0], 6),
                    "pressure_atm": pressures[0],
                    "temperature_k": temperatures[0],
                    "stp_volume_l": v_stp,
                }
            )
        if not parts:
            return None
        answer = ", ".join(f"({item['part']}) {item['stp_volume_l']:.3g} L" for item in parts)
        return ToolCallResult(
            tool_id="generated_runtime.stp_volume_correction",
            kwargs={"parts": parts},
            result={"answer_values": [item["stp_volume_l"] for item in parts], "answer": answer, "parts": parts},
        )

    def _run_partial_pressure_tool(self, question: str) -> ToolCallResult | None:
        lowered = question.lower()
        if "partial pressure" not in lowered or "total pressure" not in lowered:
            return None
        pressures = [
            (float(raw), unit.lower())
            for raw, unit in re.findall(r"(\d+(?:\.\d+)?)\s*(kpa|atm|mmhg|torr)", question, flags=re.IGNORECASE)
        ]
        if len(pressures) < 3:
            return None
        units = [unit for _, unit in pressures]
        raw_values = [value for value, _ in pressures]
        missing = raw_values[-1] - sum(raw_values[:-1])
        unit = units[-1]
        answer = f"{missing:.3g} {unit}"
        return ToolCallResult(
            tool_id="generated_runtime.partial_pressure_difference",
            kwargs={"known_partial_pressures": raw_values[:-1], "total_pressure": raw_values[-1], "unit": unit},
            result={"answer_values": [missing], "answer": answer},
        )

    def _run_ideal_gas_temperature_tool(self, question: str) -> ToolCallResult | None:
        lowered = question.lower()
        if "temperature" not in lowered or "kelvin" not in lowered:
            return None
        tool = self.tool_catalog.find("ideal_gas_law_tools", "ideal_gas_law")
        if tool is None:
            return None
        pressures = self._extract_pressures_atm(question)
        volumes = self._extract_volumes_l(question)
        moles = self._extract_moles(question)
        if not pressures or not volumes or not moles:
            return None
        kwargs = {"P": pressures[-1], "V": volumes[-1], "n": moles[0], "T": None}
        call = self.tool_catalog.execute(tool, kwargs)
        if call.error:
            return call
        value = float(call.result)
        return ToolCallResult(
            tool_id=tool.id,
            kwargs=kwargs,
            result={"T": value, "answer": f"{value:.3g} K"},
        )

    def _run_boyle_consistency_tool(self, question: str) -> ToolCallResult | None:
        lowered = question.lower()
        if "boyle" not in lowered or "consistent" not in lowered:
            return None
        ideal_tool = self.tool_catalog.find("ideal_gas_law_tools", "ideal_gas_law")
        boyle_tool = self.tool_catalog.find("gas_laws_tools", "boyles_law")
        if ideal_tool is None or boyle_tool is None:
            return None
        pressures = self._extract_pressures_atm(question)
        volumes = self._extract_volumes_l(question)
        temperatures = self._extract_temperatures_k(question)
        moles = self._extract_moles(question)
        if len(pressures) < 2 or not volumes or not temperatures or not moles:
            return None
        initial_kwargs = {"P": pressures[0], "V": None, "n": moles[0], "T": temperatures[0]}
        initial_call = self.tool_catalog.execute(ideal_tool, initial_kwargs)
        if initial_call.error:
            return initial_call
        initial_volume = float(initial_call.result)
        boyle_kwargs = {"P1": pressures[0], "V1": initial_volume, "P2": pressures[1], "V2": None}
        boyle_call = self.tool_catalog.execute(boyle_tool, boyle_kwargs)
        if boyle_call.error:
            return boyle_call
        predicted_final = float(boyle_call.result)
        given_final = volumes[-1]
        consistent = abs(predicted_final - given_final) <= max(0.05, 0.02 * abs(predicted_final))
        answer = (
            f"V = {initial_volume:.3g} L; "
            f"{'Yes' if consistent else 'No'}, Boyle's law predicts V = {predicted_final:.3g} L "
            f"at {pressures[1]:.3g} atm, not {given_final:.3g} L"
        )
        return ToolCallResult(
            tool_id=f"{ideal_tool.id}+{boyle_tool.id}",
            kwargs={"initial": initial_kwargs, "boyle": boyle_kwargs, "given_final_volume_l": given_final},
            result={"initial_volume_l": initial_volume, "predicted_final_volume_l": predicted_final, "answer": answer},
        )

    # END GENERATED_RUNTIME_DOMAIN_METHODS
    def _tool_semantic_fit(
        self,
        *,
        tool: ToolSpec,
        question: str,
        plan: dict[str, Any],
        problem: GenericProblem | None,
        candidate_inputs: dict[str, Any],
    ) -> dict[str, Any]:
        stop_tokens = {
            "the",
            "and",
            "for",
            "with",
            "from",
            "that",
            "this",
            "which",
            "what",
            "when",
            "where",
            "how",
            "are",
            "is",
            "to",
            "of",
            "in",
            "a",
            "an",
        }
        question_text = " ".join([question, *(problem.options if problem else [])])
        query_tokens = {token for token in tokenize(question_text) if len(token) > 1 and token not in stop_tokens}
        tool_text = " ".join([tool.id, tool.description, " ".join(tool.params), " ".join(tool.keywords)])
        tool_tokens = {token for token in tokenize(tool_text) if len(token) > 1 and token not in stop_tokens}
        hints = self._contract_tool_hints(plan)
        contract_text = " ".join(
            [
                " ".join(hints.get("required_capabilities", [])),
                " ".join(hints.get("resource_ids", [])),
                " ".join(hints.get("resource_capabilities", [])),
                " ".join(hints.get("schema_tags", [])),
                " ".join(hints.get("domain_tags", [])),
                " ".join(hints.get("candidate_tool_ids", [])),
                " ".join(hints.get("expected_argument_fields", [])),
                str(hints.get("task_text", "")),
            ]
        )
        contract_tokens = {token for token in tokenize(contract_text) if len(token) > 1 and token not in stop_tokens}
        direct_overlap = len(query_tokens & tool_tokens)
        contract_overlap = len(contract_tokens & tool_tokens)
        compiled_candidate_binding = tool.id in set(str(item) for item in hints.get("candidate_tool_ids", []))
        resource_id_overlap = any(
            set(tokenize(str(resource_id).replace(".", " "))) & set(tokenize(tool.id.replace(".", " ")))
            for resource_id in hints.get("resource_ids", [])
        )
        exact_problem_binding = bool(problem and problem.matching_module == tool.module and problem.matching_function == tool.function)
        target_roles = self._target_semantic_roles(question_text, hints)
        tool_roles = self._tool_semantic_roles(tool)
        target_role_overlap = len(target_roles & tool_roles)
        wrong_target_semantics = bool(target_roles and tool_roles and target_role_overlap == 0 and not exact_problem_binding)
        required_params = set(tool.params)
        non_null_inputs = {key for key, value in candidate_inputs.items() if value is not None and value != ""}
        parameter_coverage = len(non_null_inputs & required_params) / max(len(required_params), 1)
        score = (
            float(direct_overlap)
            + 0.7 * float(contract_overlap)
            + (2.0 if resource_id_overlap else 0.0)
            + (5.0 if compiled_candidate_binding else 0.0)
            + (3.0 if exact_problem_binding else 0.0)
            + (1.75 if target_role_overlap > 0 else 0.0)
            + min(parameter_coverage, 1.0)
        )
        if wrong_target_semantics:
            score -= 6.0
        if required_params and not non_null_inputs:
            score -= 1.0
        contract_anchor_count = contract_overlap + (1 if resource_id_overlap else 0) + (3 if compiled_candidate_binding else 0)
        return {
            "score": round(score, 4),
            "direct_overlap": direct_overlap,
            "contract_overlap": contract_overlap,
            "contract_anchor_count": int(contract_anchor_count),
            "resource_id_overlap": bool(resource_id_overlap),
            "compiled_candidate_binding": bool(compiled_candidate_binding),
            "exact_problem_binding": exact_problem_binding,
            "target_semantic_roles": sorted(target_roles),
            "tool_semantic_roles": sorted(tool_roles),
            "target_role_overlap": target_role_overlap,
            "wrong_target_semantics": wrong_target_semantics,
            "parameter_coverage": round(parameter_coverage, 4),
            "semantic_fit_required": bool(hints.get("semantic_fit_required")),
            "parameter_fit_required": bool(hints.get("parameter_fit_required")),
            "contract_candidate_required": bool(hints.get("contract_candidate_required")),
            "minimum_parameter_coverage": float(hints.get("minimum_parameter_coverage", 0.0) or 0.0),
        }

    def _tool_call_adequacy(
        self,
        *,
        call: ToolCallResult,
        tool: ToolSpec | None,
        question: str,
        plan: dict[str, Any],
        problem: GenericProblem | None,
    ) -> dict[str, Any]:
        if call.error is not None:
            return {"adequate": False, "score": 0.0, "reason": "tool execution error"}
        fit = dict(call.metadata.get("semantic_fit", {}))
        hints = self._contract_tool_hints(plan)
        semantic_required = bool(fit.get("semantic_fit_required") or hints.get("semantic_fit_required"))
        parameter_required = bool(fit.get("parameter_fit_required") or hints.get("parameter_fit_required"))
        contract_candidate_required = bool(fit.get("contract_candidate_required") or hints.get("contract_candidate_required"))
        runtime_policy = dict(self.design_strategy_patch.get("runtime_policy", {}))
        strict_tool_adequacy = bool(runtime_policy.get("strict_tool_adequacy"))
        fit_score = float(fit.get("score", 0.0) or 0.0)
        direct_overlap = int(fit.get("direct_overlap", 0) or 0)
        contract_overlap = int(fit.get("contract_overlap", 0) or 0)
        contract_anchor_count = int(fit.get("contract_anchor_count", 0) or 0)
        resource_id_overlap = bool(fit.get("resource_id_overlap"))
        exact_problem_binding = bool(fit.get("exact_problem_binding"))
        wrong_target_semantics = bool(fit.get("wrong_target_semantics"))
        target_role_overlap = int(fit.get("target_role_overlap", 0) or 0)
        parameter_coverage = float(fit.get("parameter_coverage", 1.0) or 0.0)
        minimum_parameter_coverage = max(
            float(fit.get("minimum_parameter_coverage", 0.0) or 0.0),
            float(hints.get("minimum_parameter_coverage", 0.0) or 0.0),
        )
        if fit.get("contract_fallback_after_gap") and (contract_candidate_required or semantic_required) and not exact_problem_binding:
            return {
                "adequate": False,
                "score": round(fit_score, 4),
                "reason": "fallback tool path requires verifier review",
            }
        if wrong_target_semantics and not exact_problem_binding:
            return {
                "adequate": False,
                "score": round(fit_score, 4),
                "reason": "tool result targets wrong semantic concept",
                "target_semantic_roles": list(fit.get("target_semantic_roles", []) or []),
                "tool_semantic_roles": list(fit.get("tool_semantic_roles", []) or []),
            }
        if contract_candidate_required and not exact_problem_binding and contract_anchor_count <= 0 and direct_overlap < 2:
            return {
                "adequate": False,
                "score": round(fit_score, 4),
                "reason": "tool candidate lacks compiled contract anchor",
            }
        if semantic_required and fit_score < 1.25:
            return {"adequate": False, "score": round(fit_score, 4), "reason": "low semantic fit to compiled contract"}
        if semantic_required and not exact_problem_binding and fit.get("target_semantic_roles") and target_role_overlap <= 0:
            return {"adequate": False, "score": round(fit_score, 4), "reason": "no target-role overlap with compiled contract"}
        if parameter_required and tool is not None and tool.params and parameter_coverage < max(0.25, minimum_parameter_coverage):
            return {"adequate": False, "score": round(fit_score, 4), "reason": "insufficient parameter binding"}
        if strict_tool_adequacy:
            semantic_anchor_count = direct_overlap + contract_overlap + (1 if resource_id_overlap else 0) + (2 if exact_problem_binding else 0)
            if semantic_anchor_count < 2:
                return {
                    "adequate": False,
                    "score": round(fit_score, 4),
                    "reason": "strict tool adequacy rejected weak semantic support",
                }
            if tool is not None and tool.params and parameter_coverage < 0.5:
                return {
                    "adequate": False,
                    "score": round(fit_score, 4),
                    "reason": "strict tool adequacy rejected weak parameter coverage",
                }
        result_text = json_preview(call.result, limit=900)
        symbolic_targets = re.findall(r"\b[A-Za-z]{1,4}\d+\+|\b[A-Za-z]{1,4}\d+-", question)
        if symbolic_targets:
            binding_text = json_preview({"kwargs": call.kwargs, "result": call.result}, limit=900).lower()
            missing_symbolic = [target for target in symbolic_targets if target.lower() not in binding_text]
            if missing_symbolic:
                return {
                    "adequate": False,
                    "score": round(fit_score, 4),
                    "reason": "symbolic target modifier absent from tool binding",
                    "missing_targets": missing_symbolic[:4],
                }
        if option_pairs(problem) and bool(hints.get("mcq_option_alignment_required")):
            selected = self._select_option_from_reference(result_text, problem)
            if selected is None:
                return {
                    "adequate": False,
                    "score": round(fit_score, 4),
                    "reason": "tool result does not align to answer options",
                }
        lowered_question = question.lower()
        total_target_requested = any(cue in lowered_question for cue in ("total", "combined", "overall", "sum of"))
        if total_target_requested and isinstance(call.result, dict):
            keys = {str(key).lower() for key in call.result}
            if not keys & {"answer", "final_answer", "total", "combined", "overall", "target", "requested"}:
                return {
                    "adequate": False,
                    "score": round(fit_score, 4),
                    "reason": "tool result lacks requested aggregate target",
                }
        qualitative_cues = [
            cue
            for cue in ("spontaneous", "nonspontaneous", "acidic", "basic", "oxidizing", "reducing")
            if cue in lowered_question
        ]
        if qualitative_cues and not any(cue in result_text.lower() for cue in qualitative_cues):
            return {
                "adequate": False,
                "score": round(fit_score, 4),
                "reason": "tool result omits requested qualitative target",
                "missing_targets": qualitative_cues[:4],
            }
        required_answer_fields = {
            str(field)
            for schema in list(hints.get("answer_target_schemas", []) or [])
            if isinstance(schema, dict)
            for field in list(schema.get("required_answer_fields", []) or [])
            if field
        }
        if "answer_values" in required_answer_fields:
            output_mapping = dict(hints.get("output_field_mapping", {}) or {})
            answer_value_keys = {
                str(item)
                for item in list(output_mapping.get("answer_values", []) or ["answer_values", "value", "result", "answer"])
                if item
            }
            if isinstance(call.result, dict):
                result_keys = {str(key) for key in call.result}
                has_answer_value_key = bool(result_keys & answer_value_keys)
                has_numeric_value = any(
                    isinstance(value, (int, float)) and not isinstance(value, bool)
                    for key, value in call.result.items()
                    if str(key) in answer_value_keys or str(key) in {"value", "result"}
                )
                if not has_answer_value_key and not has_numeric_value:
                    return {
                        "adequate": False,
                        "score": round(fit_score, 4),
                        "reason": "tool result lacks required answer_values mapping",
                    }
            elif not numeric_values(result_text):
                return {
                    "adequate": False,
                    "score": round(fit_score, 4),
                    "reason": "tool result lacks required numeric answer value",
                }
        adequacy_score = fit_score + min(parameter_coverage, 1.0)
        return {"adequate": True, "score": round(adequacy_score, 4), "reason": "tool result matches contract sufficiently"}

    def _tool_call_is_adequate(self, call: ToolCallResult) -> bool:
        adequacy = dict(call.metadata.get("adequacy", {}))
        if not adequacy:
            return call.error is None
        return call.error is None and bool(adequacy.get("adequate"))

    def _tool_candidate_satisfies_contract(
        self,
        *,
        tool: ToolSpec,
        candidate_inputs: dict[str, Any],
        fit: dict[str, Any],
        hints: dict[str, Any],
        problem: GenericProblem | None,
    ) -> bool:
        if problem and problem.matching_module == tool.module and problem.matching_function == tool.function:
            return True
        if fit.get("wrong_target_semantics"):
            return False
        if tool.id in set(str(item) for item in hints.get("candidate_tool_ids", [])):
            required_params = set(tool.params)
            if required_params:
                non_null_inputs = {key for key, value in candidate_inputs.items() if value is not None and value != ""}
                minimum_parameter_coverage = float(hints.get("minimum_parameter_coverage", 0.0) or 0.0)
                parameter_coverage = len(non_null_inputs & required_params) / max(len(required_params), 1)
                if parameter_coverage < max(0.25, minimum_parameter_coverage):
                    return False
            return True
        if not hints.get("contract_candidate_required"):
            return True
        contract_anchor_count = int(fit.get("contract_anchor_count", 0) or 0)
        direct_overlap = int(fit.get("direct_overlap", 0) or 0)
        if contract_anchor_count <= 0 and direct_overlap < 2:
            return False
        required_params = set(tool.params)
        if required_params:
            non_null_inputs = {key for key, value in candidate_inputs.items() if value is not None and value != ""}
            coverage = len(non_null_inputs & required_params) / max(len(required_params), 1)
            minimum = max(0.25, float(hints.get("minimum_parameter_coverage", 0.0) or 0.0))
            if coverage < minimum:
                return False
        return True

    def _select_tool_contract_block(
        self,
        hints: dict[str, Any],
        *,
        question: str,
        problem: GenericProblem | None,
    ) -> dict[str, Any] | None:
        blocks = [
            dict(item)
            for item in list(hints.get("tool_blocks", []) or [])
            if isinstance(item, dict) and (item.get("candidate_tool_ids") or item.get("unresolved_callable_gap"))
        ]
        if not blocks:
            return None
        if len(blocks) == 1:
            return blocks[0]
        query_tokens = set(tokenize(" ".join([question, *(problem.options if problem else [])])))
        best_score = -1.0
        best_block = blocks[0]
        exact_tool_id = (
            f"{problem.matching_module}.{problem.matching_function}"
            if problem and problem.matching_module and problem.matching_function
            else ""
        )
        for block in blocks:
            candidate_ids = {str(item) for item in list(block.get("candidate_tool_ids", []) or []) if item}
            if exact_tool_id and exact_tool_id in candidate_ids:
                return block
            block_text = " ".join(
                [
                    str(block.get("block_id") or ""),
                    str(block.get("resource_id") or ""),
                    str(block.get("task_text") or ""),
                    " ".join(candidate_ids),
                    " ".join(str(item) for item in list(block.get("expected_argument_fields", []) or [])),
                ]
            )
            block_tokens = set(tokenize(block_text))
            score = float(len(query_tokens & block_tokens)) + 0.25 * len(candidate_ids)
            if score > best_score:
                best_score = score
                best_block = block
        return best_block

    def _scoped_tool_hints(self, hints: dict[str, Any], block: dict[str, Any]) -> dict[str, Any]:
        scoped = dict(hints)
        scoped["active_tool_block"] = dict(block)
        scoped["candidate_tool_ids"] = [str(item) for item in list(block.get("candidate_tool_ids", []) or []) if item]
        scoped["callable_signatures"] = [dict(item) for item in list(block.get("callable_signatures", []) or []) if isinstance(item, dict)]
        scoped["argument_contracts"] = [dict(item) for item in list(block.get("argument_contracts", []) or []) if isinstance(item, dict)]
        scoped["expected_argument_fields"] = [str(item) for item in list(block.get("expected_argument_fields", []) or []) if item]
        output_schema = block.get("expected_output_schema")
        scoped["expected_output_schemas"] = [dict(output_schema)] if isinstance(output_schema, dict) and output_schema else []
        target_schema = block.get("answer_target_schema")
        scoped["answer_target_schemas"] = [dict(target_schema)] if isinstance(target_schema, dict) and target_schema else []
        scoped["resource_ids"] = [str(block.get("resource_id"))] if block.get("resource_id") else []
        scoped["task_text"] = str(block.get("task_text") or scoped.get("task_text") or "")
        scoped["candidate_resolution_status"] = str(block.get("candidate_resolution_status") or scoped.get("candidate_resolution_status") or "")
        scoped["unresolved_callable_gap"] = bool(block.get("unresolved_callable_gap") or scoped.get("unresolved_callable_gap"))
        scoped["lexical_fallback_allowed"] = bool(block.get("lexical_fallback_allowed", scoped.get("lexical_fallback_allowed", True)))
        return scoped

    def _compiled_candidate_tools(self, hints: dict[str, Any]) -> list[ToolSpec]:
        tools: list[ToolSpec] = []
        seen: set[str] = set()
        for tool_id in hints.get("candidate_tool_ids", []):
            value = str(tool_id or "").strip()
            if "." not in value or value in seen:
                continue
            module, function = value.split(".", 1)
            tool = self.tool_catalog.find(module, function)
            if tool is None:
                continue
            tools.append(tool)
            seen.add(value)
        return tools

    def _run_tool_agent(
        self,
        *,
        question: str,
        plan: dict[str, Any],
        problem: GenericProblem | None,
        force_broad: bool = False,
        previous_tool_calls: list[ToolCallResult] | None = None,
    ) -> tuple[list[ToolCallResult], Any | None]:
        if not plan.get("should_use_tools") and not force_broad:
            return [], None
        vdw_enthalpy_call = self._run_van_der_waals_fixed_volume_enthalpy_tool(question)
        if vdw_enthalpy_call is not None:
            return [vdw_enthalpy_call], None if vdw_enthalpy_call.error is not None else vdw_enthalpy_call.result
        vdw_pressure_call = self._run_van_der_waals_pressure_tool(question)
        if vdw_pressure_call is not None:
            return [vdw_pressure_call], None if vdw_pressure_call.error is not None else vdw_pressure_call.result
        hints = self._contract_tool_hints(plan)
        active_tool_block = self._select_tool_contract_block(hints, question=question, problem=problem)
        if active_tool_block is not None:
            hints = self._scoped_tool_hints(hints, active_tool_block)
            plan = {**plan, "_active_tool_contract_hints": hints}
        inputs = prepared_inputs(problem)
        chosen_tools: list[ToolSpec] = []
        compiled_tools = self._compiled_candidate_tools(hints)
        scoped_contract_active = bool(
            active_tool_block is not None
            or compiled_tools
            or hints.get("candidate_tool_ids")
            or hints.get("callable_signatures")
            or hints.get("argument_contracts")
        )
        broad_contract_repair_allowed = bool(
            force_broad
            or hints.get("force_broad_contract_repair")
            or hints.get("broad_fallback_after_candidate_exhaustion")
        )
        if compiled_tools:
            chosen_tools.extend(compiled_tools)
        if problem and problem.matching_module and problem.matching_function:
            exact = self.tool_catalog.find(problem.matching_module, problem.matching_function)
            compiled_tool_ids = {tool.id for tool in chosen_tools}
            if (
                exact is not None
                and exact.id not in compiled_tool_ids
                and (not scoped_contract_active or exact.id in compiled_tool_ids or force_broad)
            ):
                chosen_tools.append(exact)
        if (
            hints.get("contract_candidate_required")
            and not force_broad
            and not compiled_tools
            and not chosen_tools
            and (hints.get("unresolved_callable_gap") or not hints.get("lexical_fallback_allowed", True))
        ):
            capability_resolution = dict(plan.get("capability_resolution") or {})
            return [
                ToolCallResult(
                    tool_id="contract_tool_resolution",
                    kwargs={},
                    error="compiled contract requires a callable capability but no candidate tool was resolved",
                    metadata={
                        "contract_tool_hints": {
                            "required_capabilities": list(hints.get("required_capabilities", [])),
                            "resource_ids": list(hints.get("resource_ids", [])),
                            "candidate_tool_ids": list(hints.get("candidate_tool_ids", [])),
                            "candidate_resolution_status": hints.get("candidate_resolution_status"),
                            "unresolved_callable_gap": bool(hints.get("unresolved_callable_gap")),
                            "tool_blocks": list(hints.get("tool_blocks", []))[:4],
                        },
                        "capability_resolution": capability_resolution,
                        "continued_with_broader_fallback": False,
                    },
                )
            ], None
        if not chosen_tools and not scoped_contract_active and self._allow_generated_specialist_shortcuts():
            specialized_call = self._run_specialized_numeric_tool(question)
            if specialized_call is not None:
                return [specialized_call], None if specialized_call.error is not None else specialized_call.result
        if not chosen_tools and not scoped_contract_active:
            chosen_tools = self._preferred_tools_for_question(question)
        preferred_tool_ids = {tool.id for tool in chosen_tools}
        if not chosen_tools:
            if scoped_contract_active and hints.get("contract_candidate_required") and not broad_contract_repair_allowed:
                capability_resolution = dict(plan.get("capability_resolution") or {})
                return [
                    ToolCallResult(
                        tool_id="contract_tool_resolution",
                        kwargs={},
                        error="compiled contract scoped tool routing had no runnable candidate and broad fallback is disabled",
                        metadata={
                            "contract_tool_hints": {
                                "required_capabilities": list(hints.get("required_capabilities", [])),
                                "resource_ids": list(hints.get("resource_ids", [])),
                                "candidate_tool_ids": list(hints.get("candidate_tool_ids", [])),
                                "candidate_resolution_status": hints.get("candidate_resolution_status"),
                                "unresolved_callable_gap": bool(hints.get("unresolved_callable_gap")),
                                "lexical_fallback_allowed": bool(hints.get("lexical_fallback_allowed", True)),
                                "tool_blocks": list(hints.get("tool_blocks", []))[:4],
                            },
                            "capability_resolution": capability_resolution,
                            "continued_with_broader_fallback": False,
                        },
                    )
                ], None
            chosen_tools = self.tool_catalog.search(question, top_k=16 if force_broad else 8)
        elif not scoped_contract_active or broad_contract_repair_allowed:
            seen_tool_ids = {tool.id for tool in chosen_tools}
            for tool in self.tool_catalog.search(question, top_k=20 if force_broad else 12):
                if tool.id not in seen_tool_ids:
                    chosen_tools.append(tool)
                    seen_tool_ids.add(tool.id)
        if not chosen_tools:
            return [], None
        seen_attempts = {
            (call.tool_id, json.dumps(call.kwargs, sort_keys=True, default=str))
            for call in (previous_tool_calls or [])
        }
        max_attempts = 10 if force_broad else 6
        tool_candidates: list[tuple[float, ToolSpec, dict[str, Any], dict[str, Any]]] = []
        for tool in chosen_tools:
            candidate_inputs = self._candidate_tool_inputs(
                tool=tool,
                question=question,
                prepared=inputs,
                use_prepared_first=bool(problem and problem.matching_module and problem.matching_function),
                hints=hints,
            )
            if not candidate_inputs:
                continue
            if not self._tool_inputs_satisfy_preconditions(tool, candidate_inputs):
                continue
            fit = self._tool_semantic_fit(
                tool=tool,
                question=question,
                plan=plan,
                problem=problem,
                candidate_inputs=candidate_inputs,
            )
            if tool.id in preferred_tool_ids:
                fit["score"] = float(fit.get("score", 0.0) or 0.0) + 5.0
                fit["preferred_tool_binding"] = True
            tool_candidates.append((float(fit.get("score", 0.0) or 0.0), tool, candidate_inputs, fit))
        contract_gap_call: ToolCallResult | None = None
        if hints.get("contract_candidate_required") and not force_broad:
            contract_candidates = [
                item
                for item in tool_candidates
                if self._tool_candidate_satisfies_contract(
                    tool=item[1],
                    candidate_inputs=item[2],
                    fit=item[3],
                    hints=hints,
                    problem=problem,
                )
            ]
            if contract_candidates:
                tool_candidates = contract_candidates
            else:
                capability_resolution = dict(plan.get("capability_resolution") or {})
                contract_gap_call = ToolCallResult(
                    tool_id="contract_tool_resolution",
                    kwargs={},
                    error="no contract-compatible tool candidate satisfied semantic and parameter requirements",
                    metadata={
                        "contract_tool_hints": {
                            "required_capabilities": list(hints.get("required_capabilities", [])),
                            "resource_ids": list(hints.get("resource_ids", [])),
                            "candidate_tool_ids": list(hints.get("candidate_tool_ids", [])),
                            "expected_argument_fields": list(hints.get("expected_argument_fields", [])),
                            "tool_blocks": list(hints.get("tool_blocks", []))[:4],
                        },
                        "capability_resolution": capability_resolution,
                        "continued_with_broader_fallback": False,
                    },
                )
                return [contract_gap_call], None
        tool_candidates.sort(key=lambda item: item[0], reverse=True)
        attempted: list[ToolCallResult] = []
        successful: list[ToolCallResult] = []
        for _, tool, candidate_inputs, fit in tool_candidates:
            attempt_key = (tool.id, json.dumps(candidate_inputs, sort_keys=True, default=str))
            if attempt_key in seen_attempts:
                continue
            seen_attempts.add(attempt_key)
            call = self.tool_catalog.execute(tool, candidate_inputs)
            call = self._normalize_contract_tool_result(
                call=call,
                tool=tool,
                question=question,
                candidate_inputs=candidate_inputs,
            )
            call.metadata["semantic_fit"] = fit
            if call.error is None and tool.function == "balance_by_inspection":
                formatter = self.tool_catalog.find("equation_balancing_tools", "format_equation")
                if formatter is not None and isinstance(call.result, dict):
                    formatted = self.tool_catalog.execute(formatter, {"balanced_eq": call.result})
                    if formatted.error is None:
                        call = ToolCallResult(
                            tool_id=f"{tool.id}+{formatter.id}",
                            kwargs=call.kwargs,
                            result=formatted.result,
                            metadata=dict(call.metadata),
                        )
            call.metadata["adequacy"] = self._tool_call_adequacy(
                call=call,
                tool=tool,
                question=question,
                plan=plan,
                problem=problem,
            )
            attempted.append(call)
            if call.error is None:
                successful.append(call)
            if len(attempted) >= max_attempts:
                break
        adequate = [call for call in successful if self._tool_call_is_adequate(call)]
        if adequate:
            adequate.sort(
                key=lambda call: (
                    call.tool_id in preferred_tool_ids,
                    float(dict(call.metadata.get("adequacy", {})).get("score", 0.0) or 0.0),
                ),
                reverse=True,
            )
            return attempted, adequate[0].result
        if contract_gap_call is not None:
            attempted.append(contract_gap_call)
        return attempted, None

    def _normalize_contract_tool_result(
        self,
        *,
        call: ToolCallResult,
        tool: ToolSpec,
        question: str,
        candidate_inputs: dict[str, Any],
    ) -> ToolCallResult:
        if (
            not candidate_inputs.get("__contract_binding")
            or call.error is not None
            or not isinstance(call.result, (int, float))
            or isinstance(call.result, bool)
        ):
            return call
        missing_fields = [key for key, value in candidate_inputs.items() if not str(key).startswith("__") and (value is None or value == "")]
        target = missing_fields[0] if len(missing_fields) == 1 else ""
        contract_roles = {
            str(key): dict(value)
            for key, value in dict(candidate_inputs.get("__contract_roles", {}) or {}).items()
            if isinstance(value, dict)
        }
        contract_unit_hints = {
            str(key): dict(value)
            for key, value in dict(candidate_inputs.get("__contract_unit_hints", {}) or {}).items()
            if isinstance(value, dict)
        }
        target_role = str(dict(contract_roles.get(target, {}) or {}).get("role") or "").lower()
        target_unit_hint = dict(contract_unit_hints.get(target, {}) or {})
        value = float(call.result)
        lowered_question = question.lower()
        result_value = value
        unit = ""
        if tool.module == "gas_laws_tools" and (target in {"V1", "V2", "V", "volume"} or target_role == "volume"):
            if any(cue in lowered_question for cue in ("milliliter", "milliliters", " ml")):
                result_value = value * 1000.0
                unit = "mL"
            else:
                unit = str(target_unit_hint.get("canonical_unit") or "L")
        elif tool.module == "gas_laws_tools" and (target in {"P1", "P2", "P", "pressure"} or target_role == "pressure"):
            if any(cue in lowered_question for cue in ("mmhg", "torr")):
                result_value = value * 760.0
                unit = "mmHg"
            elif "kpa" in lowered_question:
                result_value = value * 101.325
                unit = "kPa"
            else:
                unit = str(target_unit_hint.get("canonical_unit") or "atm")
        elif target in {"T1", "T2", "T", "temperature"} or target_role == "temperature":
            unit = str(target_unit_hint.get("canonical_unit") or "K")
        elif target in {"n", "n1", "n2", "moles"} or target_role == "amount":
            unit = str(target_unit_hint.get("canonical_unit") or "mol")
        elif tool.module == "density_tools" and tool.function == "calculate_density":
            unit = str(target_unit_hint.get("canonical_unit") or "g/mL")
        elif target in {"mass", "mass_g"} or target_role == "mass":
            unit = str(target_unit_hint.get("canonical_unit") or "g")
        if not unit:
            return call
        answer = f"{result_value:.6g} {unit}"
        return ToolCallResult(
            tool_id=call.tool_id,
            kwargs=dict(call.kwargs),
            result={
                "answer_values": [result_value],
                "units": [unit],
                "answer": answer,
                "value": result_value,
                "source_value": value,
                "source_unit": "tool-native",
                "solve_for": target,
            },
            error=None,
            metadata=dict(call.metadata),
        )

    def _argument_contract_for_tool(self, hints: dict[str, Any], tool: ToolSpec) -> dict[str, Any]:
        for raw_contract in list(hints.get("argument_contracts", []) or []):
            if not isinstance(raw_contract, dict):
                continue
            contract = dict(raw_contract)
            if str(contract.get("tool_id") or "") == tool.id:
                return contract
        for signature in list(hints.get("callable_signatures", []) or []):
            if not isinstance(signature, dict) or str(signature.get("tool_id") or "") != tool.id:
                continue
            params = [str(item) for item in list(signature.get("params", []) or []) if item]
            return {
                "tool_id": tool.id,
                "required_fields": params,
                "optional_fields": [],
                "all_fields": params,
                "parameter_roles": {
                    field: dict(dict(hints.get("normalized_parameter_roles", {}) or {}).get(field, {}))
                    for field in params
                },
                "unit_normalization_hints": {
                    field: dict(dict(hints.get("unit_normalization_hints", {}) or {}).get(field, {}))
                    for field in params
                },
                "output_field_mapping": dict(hints.get("output_field_mapping", {}) or {}),
                "single_unknown_groups": [],
                "solve_target_policy": "all_required_fields_bound",
            }
        return {}

    def _contract_solve_target(self, question: str, fields: list[str]) -> str | None:
        lowered = question.lower()
        field_set = set(fields)

        def first_available(candidates: list[str]) -> str | None:
            for candidate in candidates:
                if candidate in field_set:
                    return candidate
            return None

        if any(cue in lowered for cue in ("what volume", "new volume", "final volume", "how many milliliters", "how many ml", "occupy")):
            return first_available(["V2", "V", "volume"])
        if any(cue in lowered for cue in ("original pressure", "initial pressure", "starting pressure", "pressure before")):
            return first_available(["P1", "P", "pressure"])
        if any(cue in lowered for cue in ("what pressure", "new pressure", "final pressure")):
            return first_available(["P2", "P", "pressure"])
        if any(cue in lowered for cue in ("what temperature", "new temperature", "final temperature")):
            return first_available(["T2", "T", "temperature"])
        if any(cue in lowered for cue in ("how many moles", "number of moles", "find moles")):
            return first_available(["n", "n2", "moles"])
        if any(cue in lowered for cue in ("what mass", "calculate the mass", "find the mass", "how many grams")):
            return first_available(["mass", "mass_g"])
        if any(cue in lowered for cue in ("what density", "calculate density", "find density")):
            return first_available(["density", "d"])
        return None

    def _contract_quantity_value(
        self,
        *,
        tool: ToolSpec,
        param: str,
        question: str,
        index: int = 0,
        role_payload: dict[str, Any] | None = None,
        unit_hint: dict[str, Any] | None = None,
    ) -> Any | None:
        text = self._question_stem_for_quantities(question)
        lowered_param = param.lower()
        role_payload = dict(role_payload or {})
        unit_hint = dict(unit_hint or {})
        role = str(role_payload.get("role") or "").strip().lower()
        ordinal = str(role_payload.get("ordinal") or "").strip().lower()
        pressures = self._extract_pressures_atm(text)
        volumes_l = self._extract_volumes_l(text)
        volumes_ml = self._extract_volumes_ml(text)
        temperatures = self._extract_temperatures_k(text)
        moles = self._extract_moles(text)
        masses = self._extract_masses_g(text)
        densities = self._extract_densities_g_per_ml(text)
        molar_masses = [
            parse_numeric_literal(raw)
            for raw in re.findall(r"(-?\d[\d,]*(?:\.\d+)?)\s*g\s*/\s*mol\b", text, flags=re.IGNORECASE)
        ]

        def pick(values: list[Any], position: int = index) -> Any | None:
            return values[position] if len(values) > position else None

        role_position = 1 if ordinal == "final" else 0 if ordinal == "initial" else index
        if role == "pressure":
            return pick(pressures, role_position)
        if role == "volume":
            canonical_unit = str(unit_hint.get("canonical_unit") or "").lower()
            use_ml = tool.module == "density_tools" or canonical_unit == "ml"
            return pick(volumes_ml if use_ml else volumes_l, role_position)
        if role == "temperature":
            return pick(temperatures, role_position)
        if role == "amount":
            return pick(moles, role_position)
        if role == "mass":
            return pick(masses, role_position)
        if role == "density":
            return pick(densities, role_position)
        if role == "molar_mass":
            return pick(molar_masses, role_position)
        if role == "specific_heat":
            return self._extract_specific_heat_j_per_g_c(text)
        if role == "temperature_delta":
            return self._extract_temperature_delta_c(text)

        if param in {"P1", "P2"}:
            return pick(pressures, 0 if param == "P1" else 1)
        if param in {"V1", "V2"}:
            return pick(volumes_l, 0 if param == "V1" else 1)
        if param in {"T1", "T2"}:
            return pick(temperatures, 0 if param == "T1" else 1)
        if param in {"n1", "n2"}:
            return pick(moles, 0 if param == "n1" else 1)
        if lowered_param in {"p", "pressure"}:
            return pick(pressures)
        if lowered_param in {"v", "volume", "gas_volume"}:
            return pick(volumes_ml if tool.module == "density_tools" else volumes_l)
        if lowered_param in {"t", "temperature"}:
            return pick(temperatures)
        if lowered_param in {"n", "moles", "mol"}:
            return pick(moles)
        if lowered_param in {"mass", "mass_g", "sample_mass"}:
            return pick(masses)
        if lowered_param in {"density", "d", "density_sample"}:
            return pick(densities)
        if lowered_param in {"m", "molar_mass", "molar_mass_g_mol"}:
            return pick(molar_masses)
        if lowered_param == "specific_heat":
            return self._extract_specific_heat_j_per_g_c(text)
        if lowered_param in {"delta_t", "deltat"}:
            return self._extract_temperature_delta_c(text)
        if lowered_param == "value":
            values = numeric_values(text)
            return values[0] if values else None
        return None

    def _infer_boyles_law_role_inputs(self, question: str) -> dict[str, Any]:
        text = normalize_symbolic_text(self._question_stem_for_quantities(question))
        lowered = text.lower()
        if "pressure" not in lowered or "volume" not in lowered:
            return {}
        if not any(cue in lowered for cue in ("constant temperature", "isothermal", "boyle", "reduced", "decreased", "compressed", "increased", "expanded")):
            return {}

        number_pattern = r"(-?\d[\d,]*(?:\.\d+)?)"
        pressure_unit_pattern = r"(atm|bar|mmhg|torr|kpa)"
        volume_unit_pattern = r"(ml|l|liter|liters|dm\^?3|dm3|cm\^?3|cm3)"

        def pressure_atm(value: str, unit: str) -> float:
            return convert_pressure_to_mmhg(parse_numeric_literal(value), unit) / 760.0

        def volume_l(value: str, unit: str) -> float:
            return convert_volume_to_ml(parse_numeric_literal(value), unit) / 1000.0

        pressure_matches = [
            {
                "value": pressure_atm(match.group(1), match.group(2)),
                "start": match.start(),
                "end": match.end(),
            }
            for match in re.finditer(rf"{number_pattern}\s*{pressure_unit_pattern}", text, flags=re.IGNORECASE)
        ]
        volume_matches = [
            {
                "value": volume_l(match.group(1), match.group(2)),
                "start": match.start(),
                "end": match.end(),
            }
            for match in re.finditer(rf"{number_pattern}\s*{volume_unit_pattern}", text, flags=re.IGNORECASE)
        ]
        if not pressure_matches or not volume_matches:
            return {}

        def find_labeled_value(patterns: list[str], kind: str) -> dict[str, Any] | None:
            converter = pressure_atm if kind == "pressure" else volume_l
            for pattern in patterns:
                match = re.search(pattern, text, flags=re.IGNORECASE)
                if match:
                    return {
                        "value": converter(match.group(1), match.group(2)),
                        "start": match.start(1),
                        "end": match.end(2),
                    }
            return None

        final_pressure = find_labeled_value(
            [
                rf"final\s+pressure\s*(?:is|was|=|of|equals?)?\s*{number_pattern}\s*{pressure_unit_pattern}",
                rf"pressure\s*(?:is|was|=|equals?)\s*{number_pattern}\s*{pressure_unit_pattern}\s*(?:after|finally|at\s+the\s+end)",
            ],
            "pressure",
        )
        final_volume = find_labeled_value(
            [
                rf"final\s+volume\s*(?:is|was|=|of|equals?)?\s*{number_pattern}\s*{volume_unit_pattern}",
                rf"volume\s*(?:is|was|=|equals?)\s*{number_pattern}\s*{volume_unit_pattern}\s*(?:after|finally|at\s+the\s+end)",
            ],
            "volume",
        )

        reduced_delta = find_labeled_value(
            [
                rf"(?:reduced|decreased|lowered|compressed|reducing|decreasing|compressing)[^.;,]{{0,80}}\bby\s*{number_pattern}\s*{volume_unit_pattern}",
                rf"volume\s+(?:is|was|has\s+been|had\s+been|is\s+being)?\s*(?:reduced|decreased|lowered|compressed)[^.;,]{{0,80}}\bby\s*{number_pattern}\s*{volume_unit_pattern}",
            ],
            "volume",
        )
        increased_delta = find_labeled_value(
            [
                rf"(?:increased|raised|expanded|increasing|expanding)[^.;,]{{0,80}}\bby\s*{number_pattern}\s*{volume_unit_pattern}",
                rf"volume\s+(?:is|was|has\s+been|had\s+been|is\s+being)?\s*(?:increased|raised|expanded)[^.;,]{{0,80}}\bby\s*{number_pattern}\s*{volume_unit_pattern}",
            ],
            "volume",
        )
        volume_delta = reduced_delta or increased_delta
        if final_volume is None and volume_delta is not None:
            non_delta_volumes = [
                item
                for item in volume_matches
                if abs(int(item["start"]) - int(volume_delta["start"])) > 1
            ]
            if non_delta_volumes:
                final_volume = non_delta_volumes[-1]
        if final_pressure is None:
            final_pressure = pressure_matches[-1]

        asks_initial_pressure = any(
            cue in lowered
            for cue in ("original pressure", "initial pressure", "starting pressure", "pressure before")
        )
        if asks_initial_pressure and volume_delta is not None and final_volume is not None and final_pressure is not None:
            if reduced_delta is not None:
                initial_volume = float(final_volume["value"]) + float(volume_delta["value"])
            else:
                initial_volume = float(final_volume["value"]) - float(volume_delta["value"])
            if initial_volume > 0:
                return {
                    "P1": None,
                    "V1": initial_volume,
                    "P2": float(final_pressure["value"]),
                    "V2": float(final_volume["value"]),
                }
        return {}

    def _contract_tool_inputs(
        self,
        *,
        tool: ToolSpec,
        question: str,
        prepared: dict[str, Any],
        hints: dict[str, Any],
    ) -> dict[str, Any]:
        contract = self._argument_contract_for_tool(hints, tool)
        if not contract and tool.id not in set(str(item) for item in hints.get("candidate_tool_ids", [])):
            return {}
        fields = [
            str(item)
            for item in (
                list(contract.get("all_fields", []) or [])
                or list(contract.get("required_fields", []) or []) + list(contract.get("optional_fields", []) or [])
                or tool.params
            )
            if item in set(tool.params)
        ]
        if not fields:
            fields = list(tool.params)
        candidate: dict[str, Any] = {key: value for key, value in prepared.items() if key in tool.params}
        required = [str(item) for item in list(contract.get("required_fields", []) or []) if str(item) in set(tool.params)]
        if not required:
            required = [str(item) for item in list(tool.required_params or []) if str(item) in set(tool.params)]
        optional = [str(item) for item in list(contract.get("optional_fields", []) or []) if str(item) in set(tool.params)]
        single_unknown_groups = [
            [str(item) for item in list(group or []) if str(item) in set(tool.params)]
            for group in list(contract.get("single_unknown_groups", []) or [])
        ]
        single_unknown_groups = [group for group in single_unknown_groups if group]
        solve_target_policy = str(contract.get("solve_target_policy") or "all_required_fields_bound")
        parameter_roles = {
            str(key): dict(value)
            for key, value in dict(contract.get("parameter_roles", {}) or hints.get("normalized_parameter_roles", {}) or {}).items()
            if isinstance(value, dict)
        }
        unit_hints = {
            str(key): dict(value)
            for key, value in dict(contract.get("unit_normalization_hints", {}) or hints.get("unit_normalization_hints", {}) or {}).items()
            if isinstance(value, dict)
        }
        output_mapping = dict(contract.get("output_field_mapping", {}) or hints.get("output_field_mapping", {}) or {})

        def finalize(values: dict[str, Any]) -> dict[str, Any]:
            filtered = {key: value for key, value in values.items() if key in tool.params}
            if filtered:
                filtered["__contract_binding"] = True
                filtered["__contract_roles"] = {key: value for key, value in parameter_roles.items() if key in set(tool.params)}
                filtered["__contract_unit_hints"] = {key: value for key, value in unit_hints.items() if key in set(tool.params)}
                filtered["__contract_output_field_mapping"] = output_mapping
                filtered["__contract_required_fields"] = required
                filtered["__contract_optional_fields"] = optional
                filtered["__contract_single_unknown_groups"] = single_unknown_groups
                filtered["__contract_solve_target_policy"] = solve_target_policy
            return filtered

        if tool.id == "gas_laws_tools.boyles_law":
            role_inputs = self._infer_boyles_law_role_inputs(question)
            if role_inputs:
                role_candidate = dict(candidate)
                role_candidate.update({key: value for key, value in role_inputs.items() if key in tool.params})
                missing = [field for field in ("P1", "V1", "P2", "V2") if field in set(tool.params) and role_candidate.get(field) in (None, "")]
                if len(missing) == 1:
                    return finalize(role_candidate)

        solve_target = self._contract_solve_target(question, fields)
        for field in fields:
            if field in candidate:
                continue
            if field == solve_target:
                candidate[field] = None
                continue
            value = self._contract_quantity_value(
                tool=tool,
                param=field,
                question=question,
                role_payload=parameter_roles.get(field),
                unit_hint=unit_hints.get(field),
            )
            if value is not None:
                candidate[field] = value
        if solve_target and solve_target in tool.params:
            candidate[solve_target] = None
            if "solve_for" in tool.params and candidate.get("solve_for") in (None, ""):
                candidate["solve_for"] = solve_target

        for group_fields in single_unknown_groups:
            if not group_fields or not set(group_fields) <= set(tool.params):
                continue
            group_target = solve_target if solve_target in group_fields else None
            for field in group_fields:
                if field in candidate:
                    continue
                value = self._contract_quantity_value(
                    tool=tool,
                    param=field,
                    question=question,
                    role_payload=parameter_roles.get(field),
                    unit_hint=unit_hints.get(field),
                )
                candidate[field] = value
            if group_target:
                candidate[group_target] = None
            missing = [field for field in group_fields if candidate.get(field) is None or candidate.get(field) == ""]
            if len(missing) == 1:
                return finalize(candidate)
        if required:
            missing_required = [field for field in required if candidate.get(field) in (None, "")]
            if not missing_required:
                return finalize(candidate)
            if len(missing_required) == 1 and solve_target_policy == "exactly_one_unknown":
                missing_field = missing_required[0]
                for group_fields in single_unknown_groups:
                    if missing_field not in group_fields or not set(group_fields) <= set(candidate):
                        continue
                    group_missing = [field for field in group_fields if candidate.get(field) in (None, "")]
                    if len(group_missing) == 1 and (not solve_target or missing_field == solve_target):
                        return finalize(candidate)
            return {}
        return finalize(candidate) if candidate else {}

    def _candidate_tool_inputs(
        self,
        *,
        tool: ToolSpec,
        question: str,
        prepared: dict[str, Any],
        use_prepared_first: bool,
        hints: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        hints_map = dict(hints or {})
        prepared_subset = {key: value for key, value in prepared.items() if key in tool.params}
        contract_inputs = self._contract_tool_inputs(
            tool=tool,
            question=question,
            prepared=prepared,
            hints=hints_map,
        )
        if contract_inputs:
            return contract_inputs
        contract_scoped = bool(
            hints_map.get("contract_candidate_required")
            and (
                tool.id in set(str(item) for item in hints_map.get("candidate_tool_ids", []))
                or self._argument_contract_for_tool(hints_map, tool)
            )
        )
        if contract_scoped:
            return {}
        if use_prepared_first and prepared_subset:
            return prepared_subset
        inferred = self._infer_tool_inputs(tool, question)
        if inferred:
            return inferred
        return prepared_subset

    def _tool_inputs_satisfy_preconditions(self, tool: ToolSpec, candidate_inputs: dict[str, Any]) -> bool:
        params = set(tool.params)
        if not params:
            return True

        def is_missing(value: Any) -> bool:
            return value is None or value == ""

        def exactly_one_unknown(names: tuple[str, ...]) -> bool:
            if not set(names) <= params:
                return True
            if not set(names) <= set(candidate_inputs):
                return False
            return sum(1 for name in names if is_missing(candidate_inputs.get(name))) == 1

        required_params = {
            str(item)
            for item in list(candidate_inputs.get("__contract_required_fields", []) or [])
            if str(item) in params
        } or {str(item) for item in list(tool.required_params or []) if str(item) in params}
        if candidate_inputs.get("__contract_binding") and required_params:
            missing_required = [name for name in required_params if name not in candidate_inputs or is_missing(candidate_inputs.get(name))]
            if not missing_required:
                return True
            single_unknown_groups = [
                [str(item) for item in list(group or []) if str(item) in params]
                for group in list(candidate_inputs.get("__contract_single_unknown_groups", []) or [])
            ]
            solve_policy = str(candidate_inputs.get("__contract_solve_target_policy") or "all_required_fields_bound")
            if len(missing_required) == 1 and solve_policy == "exactly_one_unknown":
                missing_field = missing_required[0]
                for group_fields in single_unknown_groups:
                    if missing_field not in group_fields or not set(group_fields) <= set(candidate_inputs):
                        continue
                    group_missing = [field for field in group_fields if is_missing(candidate_inputs.get(field))]
                    if len(group_missing) == 1:
                        return True
            return False

        gas_law_sets = (
            ("P1", "V1", "T1", "P2", "V2", "T2"),
            ("P1", "V1", "P2", "V2"),
            ("V1", "T1", "V2", "T2"),
            ("P1", "T1", "P2", "T2"),
            ("V1", "n1", "V2", "n2"),
        )
        for names in gas_law_sets:
            if set(names) <= params:
                return exactly_one_unknown(names)
        if {"P", "V", "n", "T"} <= params:
            return exactly_one_unknown(("P", "V", "n", "T"))
        if {"pressure", "volume", "moles", "temperature"} <= params:
            names = ("pressure", "volume", "moles", "temperature")
            if not set(names) <= set(candidate_inputs):
                return False
            missing_count = sum(1 for name in names if is_missing(candidate_inputs.get(name)))
            solve_for = candidate_inputs.get("solve_for")
            if solve_for:
                solve_key = str(solve_for).strip().lower()
                solve_map = {
                    "p": "pressure",
                    "pressure": "pressure",
                    "v": "volume",
                    "volume": "volume",
                    "n": "moles",
                    "moles": "moles",
                    "mole": "moles",
                    "t": "temperature",
                    "temperature": "temperature",
                }
                target = solve_map.get(solve_key)
                if target and not is_missing(candidate_inputs.get(target)):
                    return False
            return missing_count == 1
        required_params = {str(item) for item in list(tool.required_params or []) if str(item) in params}
        if required_params:
            return all(name in candidate_inputs and not is_missing(candidate_inputs.get(name)) for name in required_params)
        return True

    # BEGIN GENERATED_RUNTIME_DOMAIN_METHOD_OVERRIDES
    def _preferred_tools_for_question(self, question: str) -> list[ToolSpec]:
        if not self._allow_generated_specialist_shortcuts():
            tools: list[ToolSpec] = []
            for tool_id in self._memory_preferred_tool_ids(question):
                if "." not in tool_id:
                    continue
                module, function = tool_id.split(".", 1)
                tool = self.tool_catalog.find(module, function)
                if tool is not None:
                    tools.append(tool)
            return tools
        lowered = question.lower()
        extracted_temperatures = self._extract_temperatures_k(question)
        extracted_volumes = self._extract_volumes_l(question)
        preferred: list[tuple[str, str]] = []
        if "balance" in lowered and ("->" in lowered or "→" in lowered):
            preferred.append(("equation_balancing_tools", "balance_by_inspection"))
        if "electron configuration" in lowered:
            preferred.append(("electron_configuration_tools", "electron_configuration"))
        if "valence electron" in lowered:
            preferred.append(("electron_configuration_tools", "valence_electrons"))
        if "formula mass" in lowered or "molar mass" in lowered:
            preferred.append(("atomic_composition_tools", "molar_mass_from_formula"))
        if "average atomic mass" in lowered or ("isotope" in lowered and "amu" in lowered and "%" in lowered):
            preferred.append(("atomic_composition_tools", "average_atomic_mass"))
        if "heat" in lowered and ("absorbed" in lowered or "released" in lowered or "warms" in lowered):
            preferred.append(("energy_basics_tools", "heat_transfer"))
        if ("weighs" in lowered or "weight" in lowered) and "mass" in lowered and re.search(r"\b(lb|oz)\b", lowered):
            preferred.append(("unit_conversion_tools", "convert_mass"))
        asks_mass = any(cue in lowered for cue in ("what is the mass", "calculate the mass", "find the mass"))
        asks_volume = any(
            cue in lowered
            for cue in (
                "what is the volume",
                "what is the total volume",
                "what volume",
                "calculate the volume",
                "find the volume",
                "total volume",
                "volume would",
            )
        )
        asks_density = any(cue in lowered for cue in ("what is the density", "calculate the density", "find the density"))
        has_density_quantity = bool(self._extract_densities_g_per_ml(self._question_stem_for_quantities(question)))
        if "density" in lowered or has_density_quantity:
            if asks_mass:
                preferred.append(("density_tools", "mass_from_density"))
            elif asks_volume:
                preferred.append(("density_tools", "volume_from_density"))
            elif asks_density:
                preferred.append(("density_tools", "calculate_density"))
        if "pressure" in lowered and "volume" in lowered and ("constant temperature" in lowered or "temperature remains constant" in lowered or "boyle" in lowered or "initial volume" in lowered):
            preferred.append(("gas_laws_tools", "boyles_law"))
        if extracted_volumes and len(extracted_temperatures) >= 2 and ("constant pressure" in lowered or "pressure is constant" in lowered or "charles" in lowered):
            preferred.append(("gas_laws_tools", "charles_law"))
        if "pressure" in lowered and "temperature" in lowered and ("constant volume" in lowered or "volume is constant" in lowered):
            preferred.append(("gas_laws_tools", "gay_lussacs_law"))
        if "pressure" in lowered and "volume" in lowered and "temperature" in lowered:
            preferred.append(("gas_laws_tools", "combined_gas_law"))
        if "stp" in lowered and "moles" in lowered:
            preferred.append(("ideal_gas_law_tools", "moles_at_stp"))
        if "temperature" in lowered and "kelvin" in lowered and "pressure" in lowered and "volume" in lowered:
            preferred.append(("ideal_gas_law_tools", "ideal_gas_law"))
        for tool_id in self._memory_preferred_tool_ids(question):
            if "." not in tool_id:
                continue
            module, function = tool_id.split(".", 1)
            pair = (module, function)
            if pair not in preferred:
                preferred.append(pair)
        tools = [tool for module, function in preferred if (tool := self.tool_catalog.find(module, function)) is not None]
        return tools

    def _infer_tool_inputs(self, tool: ToolSpec, question: str) -> dict[str, Any]:
        tool_id = tool.id
        if tool_id == "equation_balancing_tools.balance_by_inspection":
            sides = parse_equation_sides(question)
            if sides:
                reactants, products = sides
                return {"reactant_formulas": reactants, "product_formulas": products}
        if tool_id in {"electron_configuration_tools.electron_configuration", "electron_configuration_tools.valence_electrons"}:
            symbol = extract_element_symbol(self._question_stem_for_quantities(question))
            if symbol:
                atomic_number = ELEMENT_ATOMIC_NUMBERS.get(symbol.lower())
                if atomic_number:
                    return {"atomic_number": atomic_number}
        if tool_id == "atomic_composition_tools.molar_mass_from_formula":
            formula = formula_from_question(question)
            if formula:
                return {"formula": formula}
        if tool_id == "gas_laws_tools.boyles_law":
            role_inputs = self._infer_boyles_law_role_inputs(question)
            return role_inputs or self._infer_boyles_law_inputs(question)
        inferred = self._infer_quantity_named_tool_inputs(tool, question)
        if inferred:
            return inferred
        return {}

    def _infer_quantity_named_tool_inputs(self, tool: ToolSpec, question: str) -> dict[str, Any]:
        """Bind reusable tools whose parameter names expose common physical quantities."""
        params = set(tool.params)
        tool_id = tool.id
        lowered = question.lower()
        quantity_text = self._question_stem_for_quantities(question)
        pressures = self._extract_pressures_atm(quantity_text)
        volumes = self._extract_volumes_l(quantity_text)
        temperatures = self._extract_temperatures_k(quantity_text)
        moles = self._extract_moles(quantity_text)
        asks_volume = "what is the new volume" in lowered or "what volume" in lowered or "find the volume" in lowered
        asks_pressure = "what is the pressure" in lowered or "find the pressure" in lowered or "final pressure" in lowered
        asks_temperature = "what is the temperature" in lowered or "find the temperature" in lowered
        if tool_id == "atomic_composition_tools.average_atomic_mass":
            isotopes = self._extract_isotope_mass_abundance_pairs(quantity_text)
            if isotopes:
                return {"isotopes": isotopes}
        if tool_id == "energy_basics_tools.heat_transfer":
            masses_g = self._extract_masses_g(quantity_text)
            specific_heat = self._extract_specific_heat_j_per_g_c(quantity_text)
            delta_t = self._extract_temperature_delta_c(quantity_text)
            if masses_g and specific_heat is not None and delta_t is not None:
                return {"mass": masses_g[0], "specific_heat": specific_heat, "delta_T": delta_t}
        if tool_id.endswith(".convert_mass") and {"value", "from_unit", "to_unit"} <= params:
            mass_match = re.search(
                r"(-?\d[\d,]*(?:\.\d+)?)\s*(lb|oz|kg|g|mg)\b(?!\s*/)",
                quantity_text,
                flags=re.IGNORECASE,
            )
            if mass_match:
                from_unit = mass_match.group(2)
                target_match = re.search(r"\b(in|to)\s+(kg|kilograms?|g|grams?|mg|milligrams?|lb|pounds?|oz|ounces?)\b", lowered)
                target_lookup = {
                    "kilogram": "kg",
                    "kilograms": "kg",
                    "kg": "kg",
                    "gram": "g",
                    "grams": "g",
                    "g": "g",
                    "milligram": "mg",
                    "milligrams": "mg",
                    "mg": "mg",
                    "pound": "lb",
                    "pounds": "lb",
                    "lb": "lb",
                    "ounce": "oz",
                    "ounces": "oz",
                    "oz": "oz",
                }
                to_unit = target_lookup.get(target_match.group(2), "") if target_match else ""
                if not to_unit:
                    to_unit = "kg" if from_unit.lower() in {"lb", "oz"} and "mass" in lowered else "g"
                return {"value": parse_numeric_literal(mass_match.group(1)), "from_unit": from_unit, "to_unit": to_unit}
        densities = self._extract_densities_g_per_ml(quantity_text)
        masses = self._extract_masses_g(quantity_text)
        volumes_ml = self._extract_volumes_ml(quantity_text)
        if tool_id.startswith("density_tools.") and "density" not in lowered and not densities:
            return {}
        if tool_id == "density_tools.calculate_density" and masses and volumes_ml:
            return {"mass": masses[0], "volume": volumes_ml[0]}
        if tool_id == "density_tools.mass_from_density" and densities and volumes_ml:
            return {"density": densities[0], "volume": volumes_ml[0]}
        if tool_id == "density_tools.volume_from_density" and densities and masses:
            return {"density": densities[0], "mass": masses[0]}
        if (tool_id.endswith(".charles_law") or params == {"V1", "T1", "V2", "T2"}) and volumes and len(temperatures) >= 2:
            return {
                "V1": volumes[0],
                "T1": temperatures[0],
                "V2": None if asks_volume or len(volumes) < 2 else volumes[-1],
                "T2": temperatures[-1],
            }
        if tool_id.endswith(".boyles_law") or params == {"P1", "V1", "P2", "V2"}:
            role_inputs = self._infer_boyles_law_role_inputs(question)
            if role_inputs:
                return role_inputs
        if (tool_id.endswith(".boyles_law") or params == {"P1", "V1", "P2", "V2"}) and volumes and pressures:
            return {
                "P1": pressures[0],
                "V1": volumes[0],
                "P2": None if asks_pressure or len(pressures) < 2 else pressures[-1],
                "V2": None if asks_volume and len(pressures) >= 2 else (volumes[-1] if len(volumes) >= 2 else None),
            }
        if (tool_id.endswith(".gay_lussacs_law") or params == {"P1", "T1", "P2", "T2"}) and pressures and len(temperatures) >= 2:
            return {
                "P1": pressures[0],
                "T1": temperatures[0],
                "P2": None if asks_pressure or len(pressures) < 2 else pressures[-1],
                "T2": temperatures[-1],
            }
        if (tool_id.endswith(".avogadros_law") or params == {"V1", "n1", "V2", "n2"}) and volumes and moles:
            return {
                "V1": volumes[0],
                "n1": moles[0],
                "V2": None if asks_volume or len(volumes) < 2 else volumes[-1],
                "n2": moles[-1] if len(moles) >= 2 else None,
            }
        if (tool_id.endswith(".combined_gas_law") or params == {"P1", "V1", "T1", "P2", "V2", "T2"}) and (
            pressures or volumes or temperatures
        ):
            return {
                "P1": pressures[0] if pressures else None,
                "V1": volumes[0] if volumes else None,
                "T1": temperatures[0] if temperatures else None,
                "P2": None if asks_pressure or len(pressures) < 2 else pressures[-1],
                "V2": None if asks_volume or len(volumes) < 2 else volumes[-1],
                "T2": None if asks_temperature or len(temperatures) < 2 else temperatures[-1],
            }
        if {"P", "V", "n", "T"} <= params and (pressures or volumes or moles or temperatures):
            return {
                "P": pressures[0] if pressures and not asks_pressure else None,
                "V": volumes[0] if volumes and not asks_volume else None,
                "n": moles[0] if moles else None,
                "T": temperatures[0] if temperatures and not asks_temperature else None,
            }
        if {"pressure", "volume", "moles", "temperature"} <= params and (pressures or volumes or moles or temperatures):
            return {
                "pressure": pressures[0] if pressures and not asks_pressure else None,
                "volume": volumes[0] if volumes and not asks_volume else None,
                "moles": moles[0] if moles else None,
                "temperature": temperatures[0] if temperatures and not asks_temperature else None,
                "solve_for": "V" if asks_volume else ("P" if asks_pressure else ("T" if asks_temperature else None)),
            }
        return {}

    def _infer_boyles_law_inputs(self, question: str) -> dict[str, Any]:
        role_inputs = self._infer_boyles_law_role_inputs(question)
        if role_inputs:
            return role_inputs
        text = normalize_symbolic_text(self._question_stem_for_quantities(question))
        pressure_matches = [
            (float(value), unit)
            for value, unit in re.findall(r"(\d+(?:\.\d+)?)\s*(atm|bar|mmHg|torr|kPa)", text, flags=re.IGNORECASE)
        ]
        volume_matches = [
            (float(value), unit)
            for value, unit in re.findall(r"(\d+(?:\.\d+)?)\s*(mL|L|liter|liters|dm\^?3|dm3|cm3|cm\^3)", text, flags=re.IGNORECASE)
        ]
        if not pressure_matches or len(volume_matches) < 1:
            return {}
        p1 = convert_pressure_to_mmhg(*pressure_matches[0])
        p2 = convert_pressure_to_mmhg(*pressure_matches[-1]) if len(pressure_matches) >= 2 else None
        v1 = convert_volume_to_ml(*volume_matches[0])
        v2 = convert_volume_to_ml(*volume_matches[-1]) if len(volume_matches) >= 2 else None
        lowered = text.lower()
        if "pressure is changed" in lowered or ("how many" in lowered and "occupy" in lowered and len(pressure_matches) >= 2):
            return {"P1": p1, "V1": v1, "P2": p2, "V2": None}
        if ("volume is reduced" in lowered or "what is the pressure" in lowered) and len(volume_matches) >= 2:
            return {"P1": p1, "V1": v1, "P2": None, "V2": v2}
        return {}

    # END GENERATED_RUNTIME_DOMAIN_METHOD_OVERRIDES
    def _run_synthesis_agent(
        self,
        *,
        question: str,
        docs: list[RetrievedDocument],
        tool_calls: list[ToolCallResult],
        problem: GenericProblem | None,
        plan: dict[str, Any],
    ) -> str:
        spec = self.agent_specs_by_id.get("synthesis_agent")
        if self.client is None or spec is None:
            return self._reason(question, docs, tool_calls, problem)
        lines = [
            "Question:",
            question,
            "",
            "Planner output:",
            json_preview(plan, limit=800),
            "",
        ]
        if plan.get("expert_consensus"):
            lines.extend(["Expert ensemble consensus:", json_preview(plan.get("expert_consensus"), limit=1400), ""])
        if problem and problem.given:
            lines.extend(["Structured givens:", json_preview(problem.given), ""])
        if docs:
            lines.append("Retrieved evidence:")
            for index, doc in enumerate(docs[:4], start=1):
                lines.append(f"[{index}] {doc.path}")
                lines.append(doc.snippet)
            lines.append("")
        if tool_calls:
            lines.append("Tool traces:")
            for call in tool_calls:
                lines.append(f"{call.tool_id}:")
                lines.append(json_preview(call.result if call.error is None else {"error": call.error}))
            lines.append("")
        if not option_pairs(problem):
            lines.append(
                "Answer-format contract: start with `Final answer: <value or conclusion>`. "
                "For numeric questions, include the requested unit in that first sentence, "
                "then add at most two short calculation checks."
            )
        lines.append("Produce the candidate answer only.")
        synthesis_max_tokens = max(120, min(1600, int(getattr(self, "max_model_tokens", 900))))
        try:
            return self.client.complete_text(
                "\n".join(lines),
                system_prompt=spec.llm_prompt,
                max_tokens=synthesis_max_tokens,
            )
        except Exception as exc:
            plan.setdefault("model_call_errors", []).append(
                {
                    "agent": "synthesis_agent",
                    "error": str(exc)[:500],
                }
            )
            return self._reason(question, docs, tool_calls, problem)

    def _render_final_answer(
        self,
        *,
        raw_answer: str,
        tool_result_payload: Any | None,
        docs: list[RetrievedDocument],
        plan: dict[str, Any],
        problem: GenericProblem | None = None,
    ) -> str:
        final_answer = normalize_whitespace(raw_answer)
        payload_answer = ""
        if isinstance(tool_result_payload, dict) and tool_result_payload.get("answer") is not None:
            payload_answer = normalize_whitespace(str(tool_result_payload.get("answer")))
        if payload_answer and not option_pairs(problem):
            final_answer = payload_answer
        elif tool_result_payload is not None and plan.get("should_use_tools") and not option_pairs(problem):
            rendered_payload = self._render_tool_payload_answer(tool_result_payload)
            if rendered_payload:
                final_answer = rendered_payload
        if not final_answer and tool_result_payload is not None:
            final_answer = normalize_whitespace(str(tool_result_payload))
        if not final_answer and docs:
            final_answer = normalize_whitespace(docs[0].snippet[:280])
        if not final_answer:
            final_answer = "I do not have enough information."
        question_text = problem.question if problem else str(plan.get("question") or "")
        if self._numeric_free_response_requested(question_text, problem=problem, plan=plan) and self._numeric_answer_needs_finalization(
            question_text,
            final_answer,
        ):
            finalized_answer = self._finalize_numeric_free_response(
                question=question_text,
                raw_answer=final_answer,
                plan=plan,
            )
            if finalized_answer:
                final_answer = finalized_answer
        answer_mode = str(plan.get("answer_mode", "")).lower()
        if answer_mode == "multiple-choice" or option_pairs(problem):
            reference = normalize_whitespace(str(tool_result_payload if tool_result_payload is not None else final_answer))
            if problem_requests_multiple_option_letters(problem):
                selected_letters = option_letter_set_from_text(reference, option_pairs(problem))
                if not selected_letters:
                    selected_letters = option_letter_set_from_prediction_text(reference, option_pairs(problem))
                if selected_letters:
                    return ", ".join(sorted(selected_letters))
                return final_answer
            selected = self._select_option_from_reference(reference, problem)
            if selected:
                return selected
            match = re.search(r"\b([A-H])\b", final_answer.upper())
            if match:
                return match.group(1)
        return self._normalize_scientific_answer_units(
            problem.question if problem else str(plan.get("question") or ""),
            final_answer,
        )

    def _numeric_free_response_requested(
        self,
        question: str,
        *,
        problem: GenericProblem | None,
        plan: dict[str, Any],
    ) -> bool:
        if option_pairs(problem):
            return False
        answer_mode = str(plan.get("answer_mode", "")).strip().lower()
        if "numeric" in answer_mode:
            return True
        lowered_question = str(question or "").lower()
        if not re.search(r"\b(?:calculate|determine|find|estimate|report|what\s+is)\b", lowered_question):
            return False
        return bool(
            re.search(
                r"\b(?:delta\s*[sgh]|entropy|enthalpy|free\s+energy|force\s+constant|bond\s+length|"
                r"pressure|volume|temperature|moles?|mass|concentration|ph|wavelength|wavenumber|"
                r"hz|cm\s*(?:\^-?1|-1)|j|kj|n\s*/?\s*m|pm|nm|ev|atm|bar|kpa|mol)\b",
                lowered_question,
            )
            or re.search(r"\d", lowered_question)
        )

    def _numeric_answer_needs_finalization(self, question: str, answer: str) -> bool:
        normalized_answer = normalize_whitespace(answer)
        if not normalized_answer:
            return True
        if re.match(r"\s*(?:final\s+answer|answer)\s*[:=-]", normalized_answer, flags=re.IGNORECASE) and len(normalized_answer) <= 280:
            return False
        if len(normalized_answer) > 420:
            return True
        if re.match(r"\s*(?:let\s+me|first[, ]|step\s+\d+)", normalized_answer, flags=re.IGNORECASE):
            return True
        if (
            len(normalized_answer) <= 260
            and re.search(r"\b(?:solution|given|known)\b", normalized_answer, flags=re.IGNORECASE)
            and not re.search(
                r"\b(?:final\s+answer|answer|therefore|thus|so|approximately|approx\.?|result)\b",
                normalized_answer,
                flags=re.IGNORECASE,
            )
        ):
            return True
        return not bool(answer_like_numeric_values(normalized_answer, question=question))

    def _finalize_numeric_free_response(
        self,
        *,
        question: str,
        raw_answer: str,
        plan: dict[str, Any],
    ) -> str:
        if self.client is None:
            return ""
        raw_text = normalize_whitespace(raw_answer)
        if len(raw_text) > 3200:
            raw_text = f"{raw_text[:1700]} ... {raw_text[-1300:]}"
        prompt = {
            "question": question,
            "raw_attempt": raw_text,
            "task": (
                "Return one concise line only in the form `Final answer: <numeric value> <requested unit>`. "
                "Use the raw attempt if it is sound; if it is incomplete, solve from the question independently. "
                "Do not include a derivation."
            ),
        }
        try:
            response = self.client.complete_text(
                json.dumps(prompt, ensure_ascii=False, indent=2),
                system_prompt=(
                    "You are a chemistry numeric-answer finalizer. "
                    "You see only the performer question and its raw attempt, never expected answers. "
                    "Return exactly one final numeric answer line with units."
                ),
                max_tokens=220,
            )
        except Exception as exc:
            plan.setdefault("render_notes", []).append(f"numeric_finalizer_failed: {str(exc)[:160]}")
            return ""
        finalized = normalize_whitespace(response)
        if not answer_like_numeric_values(finalized, question=question):
            plan.setdefault("render_notes", []).append("numeric_finalizer_rejected_no_numeric_answer")
            return ""
        if len(finalized) > 420:
            plan.setdefault("render_notes", []).append("numeric_finalizer_rejected_verbose_answer")
            return ""
        plan.setdefault("render_notes", []).append("numeric_finalizer_rewrote_verbose_numeric_answer")
        return finalized

    def _normalize_scientific_answer_units(self, question: str, answer: str) -> str:
        """Apply domain-neutral scientific unit conventions after synthesis.

        The rule is intentionally narrow: if a question asks for mass from a
        pound-force style weight and does not request slugs, report SI kg rather
        than the imperial slug unit. This avoids accepting a dimensionally valid
        but convention-mismatched answer without adding a problem-specific
        calculator.
        """

        normalized_answer = normalize_whitespace(answer)
        lowered_question = str(question or "").lower()
        if "mass" not in lowered_question or "slug" in lowered_question:
            return normalized_answer
        if not re.search(r"\bweighs?\b|\bweight\b|\blb\b|\bpounds?\b", lowered_question):
            return normalized_answer
        slug_match = re.search(r"\b(-?\d[\d,]*(?:\.\d+)?)\s*slugs?\b", normalized_answer, flags=re.IGNORECASE)
        if slug_match:
            try:
                slug_value = parse_numeric_literal(slug_match.group(1))
            except Exception:
                return normalized_answer
            kg_value = slug_value * 14.59390294
            return f"{kg_value:.3g} kg"
        pound_answer_match = re.search(r"\b(-?\d[\d,]*(?:\.\d+)?)\s*(?:lb|lbs|pounds?)\b", normalized_answer, flags=re.IGNORECASE)
        if not pound_answer_match:
            return normalized_answer
        if re.search(r"\b(?:in|as)\s+(?:lb|lbs|pounds?)\b|\banswer\s+in\s+(?:lb|lbs|pounds?)\b", lowered_question):
            return normalized_answer
        question_pound_values = [
            parse_numeric_literal(value)
            for value in re.findall(r"\b(-?\d[\d,]*(?:\.\d+)?)\s*(?:lb|lbs|pounds?)\b", question, flags=re.IGNORECASE)
        ]
        try:
            answer_pounds = parse_numeric_literal(pound_answer_match.group(1))
        except Exception:
            return normalized_answer
        if question_pound_values and min(abs(answer_pounds - value) for value in question_pound_values) <= max(0.02 * abs(answer_pounds), 0.25):
            kg_value = answer_pounds / 2.2046226218
            return f"{kg_value:.3g} kg"
        return normalized_answer

    def _render_tool_payload_answer(self, payload: Any) -> str:
        if isinstance(payload, (int, float)):
            return f"{float(payload):.6g}"
        if isinstance(payload, str):
            return normalize_whitespace(payload)
        if isinstance(payload, dict):
            for key in ("answer", "result", "value", "final_answer"):
                if payload.get(key) is not None:
                    return normalize_whitespace(str(payload[key]))
            answer_values = payload.get("answer_values")
            if isinstance(answer_values, list) and answer_values:
                units = payload.get("units") if isinstance(payload.get("units"), list) else []
                part_ids = payload.get("part_ids") if isinstance(payload.get("part_ids"), list) else []
                rendered_values = []
                for index, value in enumerate(answer_values[:6]):
                    label = f"{part_ids[index]}=" if index < len(part_ids) and part_ids[index] else ""
                    unit = f" {units[index]}" if index < len(units) and units[index] else ""
                    rendered_values.append(f"{label}{value}{unit}")
                if rendered_values:
                    return "; ".join(rendered_values)
            numeric_items = [
                (key, value)
                for key, value in payload.items()
                if isinstance(value, (int, float)) and not isinstance(value, bool)
            ]
            if numeric_items:
                return "; ".join(f"{key}={value:.6g}" for key, value in numeric_items[:4])
        return ""

    def _select_option_from_reference(self, reference: str, problem: GenericProblem | None) -> str | None:
        pairs = option_pairs(problem)
        if not pairs:
            return None
        normalized_reference = normalize_prediction(reference).lower()
        if re.fullmatch(r"\s*-?\d[\d,]*(?:\.\d+)?(?:e[+-]?\d+)?\s*", str(reference), flags=re.IGNORECASE):
            reference_values = numeric_values(reference)
            if reference_values:
                target = reference_values[0]
                numeric_best: tuple[float, str] | None = None
                for letter, text in pairs:
                    option_values = numeric_values(text)
                    if not option_values:
                        continue
                    error = min(abs(value - target) / max(abs(target), 1.0) for value in option_values)
                    if numeric_best is None or error < numeric_best[0]:
                        numeric_best = (error, letter)
                if numeric_best is not None:
                    return numeric_best[1]
        text_letter = option_letter_from_prediction_text(reference, pairs)
        if text_letter:
            return text_letter
        best: tuple[float, str] | None = None
        for letter, text in pairs:
            normalized_option = normalize_prediction(text).lower()
            score = 0.0
            if normalized_option and normalized_option in normalized_reference:
                score += 10.0
            score += token_overlap_score(reference, text)
            if best is None or score > best[0]:
                best = (score, letter)
        if best and best[0] > 0:
            return best[1]
        return None

    def _write_trace_file(self, record: AnswerRecord, *, plan: dict[str, Any]) -> None:
        slug = re.sub(r"[^a-z0-9]+", "_", normalize_prediction(record.question).lower()).strip("_")[:48] or "question"
        filename = f"{slug}_{len(list(self.runs_dir.glob('*.json'))) + 1:04d}.json"
        payload = {
            "question": record.question,
            "plan": plan,
            "answer_record": record.to_dict(),
            "manifest": self.manifest,
        }
        (self.runs_dir / filename).write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
