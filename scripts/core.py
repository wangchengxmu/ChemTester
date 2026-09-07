from __future__ import annotations

import base64
import json
import multiprocessing
import os
import re
import threading
import time
import urllib.request
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import Any

from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion


class APILimitError(RuntimeError):
    pass


def _windows_user_environment_variable(name: str) -> str | None:
    if os.name != "nt":
        return None
    try:
        import winreg

        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as key:
            value, _ = winreg.QueryValueEx(key, name)
    except (FileNotFoundError, OSError):
        return None
    text = str(value).strip()
    return text or None


def _process_or_windows_user_environment(name: str) -> str | None:
    value = os.getenv(name)
    if value:
        return value
    return _windows_user_environment_variable(name)


def is_api_limit_error(exc: Exception) -> bool:
    text = str(exc).lower()
    markers = [
        "429",
        "rate limit",
        "quota",
        "insufficient",
        "balance",
        "credit",
        "billing",
        "too many requests",
        "resource exhausted",
        "frequency limit",
        "余额",
        "限额",
        "配额",
        "超限",
        "额度",
    ]
    return any(marker in text for marker in markers)


@dataclass(slots=True)
class ModelConfig:
    model: str
    base_url: str | None = None
    api_key: str | None = None
    default_headers: dict[str, str] | None = None
    temperature: float = 0.0
    max_tokens: int = 1024
    timeout: float = 180.0
    max_retries: int = 3
    retry_wait_seconds: float = 2.0
    min_request_interval_seconds: float = 0.0
    thinking_type: str | None = None
    empty_retry_max_tokens: int | None = None
    max_question_seconds: float | None = None
    hard_timeout_seconds: float | None = None
    system_prompt: str | None = None
    fallback_disable_thinking: bool = False
    fallback_max_tokens: int | None = None
    api_limit_cooldown_seconds: float = 60.0

    @classmethod
    def from_env(
        cls,
        model: str | None = None,
        base_url: str | None = None,
        api_key: str | None = None,
        temperature: float = 0.0,
        max_tokens: int = 1024,
        timeout: float = 180.0,
        max_retries: int = 3,
        retry_wait_seconds: float = 2.0,
        min_request_interval_seconds: float | None = None,
        thinking_type: str | None = None,
        empty_retry_max_tokens: int | None = None,
        max_question_seconds: float | None = None,
        hard_timeout_seconds: float | None = None,
        system_prompt: str | None = None,
        fallback_disable_thinking: bool = False,
        fallback_max_tokens: int | None = None,
        api_limit_cooldown_seconds: float = 60.0,
    ) -> "ModelConfig":
        resolved_model = model or os.getenv("MODEL_NAME", "")
        lowered_model = resolved_model.lower()
        model_prefers_kimi = lowered_model.startswith("kimi")
        model_prefers_glm = lowered_model.startswith("glm")

        if base_url:
            resolved_base_url = base_url
        elif model_prefers_kimi:
            resolved_base_url = (
                _process_or_windows_user_environment("KIMI_API_BASE")
                or _process_or_windows_user_environment("MOONSHOT_API_BASE")
                or "https://api.moonshot.cn/v1"
            )
        elif model_prefers_glm:
            resolved_base_url = os.getenv("GLM_API_BASE") or os.getenv("OPENAI_BASE_URL")
        else:
            resolved_base_url = os.getenv("OPENAI_BASE_URL") or os.getenv("GLM_API_BASE")

        if api_key:
            resolved_api_key = api_key
        else:
            prefers_kimi_key = model_prefers_kimi
            prefers_glm_key = model_prefers_glm
            if resolved_base_url:
                lowered = resolved_base_url.lower()
                prefers_kimi_key = prefers_kimi_key or "moonshot" in lowered or "kimi" in lowered
                prefers_glm_key = (
                    prefers_glm_key
                    or "bigmodel" in lowered
                    or "z.ai" in lowered
                    or "glm" in lowered
                )

            if prefers_kimi_key:
                resolved_api_key = (
                    _process_or_windows_user_environment("KIMI_API_KEY")
                    or _process_or_windows_user_environment("MOONSHOT_API_KEY")
                )
            elif prefers_glm_key:
                resolved_api_key = (
                    os.getenv("GLM_API_KEY")
                    or os.getenv("ZAI_API_KEY")
                    or os.getenv("ZHIPUAI_API_KEY")
                    or os.getenv("OPENAI_API_KEY")
                )
            else:
                resolved_api_key = (
                    os.getenv("OPENAI_API_KEY")
                    or os.getenv("ZAI_API_KEY")
                    or os.getenv("ZHIPUAI_API_KEY")
                    or os.getenv("GLM_API_KEY")
                )

        return cls(
            model=resolved_model,
            base_url=resolved_base_url,
            api_key=resolved_api_key,
            default_headers=None,
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=timeout,
            max_retries=max_retries,
            retry_wait_seconds=retry_wait_seconds,
            min_request_interval_seconds=(
                float(min_request_interval_seconds)
                if min_request_interval_seconds is not None
                else float(
                    os.getenv("MIN_REQUEST_INTERVAL_SECONDS")
                    or os.getenv("GLM_MIN_REQUEST_INTERVAL_SECONDS")
                    or 0.0
                )
            ),
            thinking_type=thinking_type,
            empty_retry_max_tokens=empty_retry_max_tokens,
            max_question_seconds=max_question_seconds,
            hard_timeout_seconds=hard_timeout_seconds,
            system_prompt=system_prompt,
            fallback_disable_thinking=fallback_disable_thinking,
            fallback_max_tokens=fallback_max_tokens,
            api_limit_cooldown_seconds=api_limit_cooldown_seconds,
        )


def _chat_completion_worker(
    config_payload: dict[str, Any],
    request_kwargs: dict[str, Any],
    result_queue: Any,
) -> None:
    try:
        client = OpenAI(
            api_key=config_payload.get("api_key") or "EMPTY",
            base_url=config_payload.get("base_url"),
            default_headers=config_payload.get("default_headers"),
            max_retries=0,
        )
        response = client.chat.completions.create(**request_kwargs)
        result_queue.put({"ok": True, "response": response.model_dump()})
    except Exception as exc:  # pragma: no cover - worker path
        result_queue.put({"ok": False, "error": repr(exc)})


class OpenAICompatibleClient:
    def __init__(self, config: ModelConfig) -> None:
        if not config.model:
            raise ValueError("Model name is required. Pass --model or set MODEL_NAME.")
        self.config = config
        self._request_lock = threading.Lock()
        self._last_request_ts = 0.0
        self.client = OpenAI(
            api_key=config.api_key or "EMPTY",
            base_url=config.base_url,
            default_headers=config.default_headers,
            max_retries=0,
        )

    def complete_text(
        self,
        user_prompt: str,
        *,
        system_prompt: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> str:
        messages: list[dict[str, Any]] = []
        effective_system = system_prompt if system_prompt is not None else self.config.system_prompt
        if effective_system:
            messages.append({"role": "system", "content": effective_system})
        messages.append({"role": "user", "content": user_prompt})
        return self.complete_messages(messages, temperature=temperature, max_tokens=max_tokens)

    def complete_multimodal(
        self,
        user_prompt: str,
        image: Any,
        *,
        media_type: str = "image/jpeg",
        system_prompt: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> str:
        messages: list[dict[str, Any]] = []
        effective_system = system_prompt if system_prompt is not None else self.config.system_prompt
        if effective_system:
            messages.append({"role": "system", "content": effective_system})

        image_b64 = image_to_base64(image, media_type=media_type)
        messages.append(
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": user_prompt},
                    {"type": "image_url", "image_url": {"url": f"data:{media_type};base64,{image_b64}"}},
                ],
            }
        )
        return self.complete_messages(messages, temperature=temperature, max_tokens=max_tokens)

    def complete_messages(
        self,
        messages: list[dict[str, Any]],
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> str:
        return self._chat(messages, temperature=temperature, max_tokens=max_tokens)

    def _chat(
        self,
        messages: list[dict[str, Any]],
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> str:
        started_at = time.monotonic()
        requested_max_tokens = self.config.max_tokens if max_tokens is None else max_tokens
        request_profiles: list[tuple[int, str | None]] = [(requested_max_tokens, self.config.thinking_type)]
        if (
            self.config.empty_retry_max_tokens is not None
            and self.config.empty_retry_max_tokens > requested_max_tokens
        ):
            request_profiles.append((self.config.empty_retry_max_tokens, self.config.thinking_type))
        if self.config.fallback_disable_thinking and self.config.thinking_type == "enabled":
            fallback_budget = self.config.fallback_max_tokens or requested_max_tokens
            request_profiles.append((fallback_budget, "disabled"))

        last_error: Exception | None = None
        fallback_reasoning: str = ""

        for profile_index, (budget, thinking_type) in enumerate(request_profiles, start=1):
            for attempt in range(1, self.config.max_retries + 1):
                if self._question_budget_exhausted(started_at):
                    break
                try:
                    self._throttle()
                    effective_timeout = self.config.timeout
                    remaining_budget = self._remaining_question_seconds(started_at)
                    if remaining_budget is not None:
                        effective_timeout = min(effective_timeout, max(1.0, remaining_budget))
                    request_kwargs: dict[str, Any] = {
                        "model": self.config.model,
                        "messages": messages,
                        "temperature": self.config.temperature if temperature is None else temperature,
                        "max_tokens": budget,
                        "timeout": effective_timeout,
                    }
                    if thinking_type:
                        request_kwargs["extra_body"] = {"thinking": {"type": thinking_type}}
                    response = self._create_chat_completion(request_kwargs)
                    message = response.choices[0].message
                    finish_reason = getattr(response.choices[0], "finish_reason", None)
                    content = message.content
                    reasoning_content = getattr(message, "reasoning_content", None)
                    if isinstance(reasoning_content, str) and reasoning_content.strip():
                        fallback_reasoning = reasoning_content.strip()

                    if content is None:
                        content = ""
                    if isinstance(content, str):
                        stripped = content.strip()
                    else:
                        parts = []
                        for item in content:
                            if isinstance(item, dict) and item.get("type") == "text":
                                parts.append(str(item.get("text", "")))
                            elif hasattr(item, "type") and getattr(item, "type", None) == "text":
                                parts.append(str(getattr(item, "text", "")))
                        stripped = "\n".join(part.strip() for part in parts if part.strip())

                    if stripped:
                        return stripped

                    is_last_profile = profile_index == len(request_profiles)
                    if not is_last_profile and finish_reason == "length":
                        sleep_seconds = self._retry_sleep_seconds(RuntimeError("empty content after token exhaustion"), attempt)
                        if self._question_budget_exhausted(started_at, extra_seconds=sleep_seconds):
                            break
                        time.sleep(sleep_seconds)
                        break

                    if is_last_profile and fallback_reasoning:
                        return fallback_reasoning
                    last_error = RuntimeError(
                        f"Model returned empty visible content (finish_reason={finish_reason}, thinking={thinking_type or 'default'}, max_tokens={budget})"
                    )
                    break
                except Exception as exc:  # pragma: no cover - network path
                    last_error = exc
                    if is_api_limit_error(exc):
                        last_error = APILimitError(str(exc))
                        if attempt == self.config.max_retries:
                            break
                        sleep_seconds = self._retry_sleep_seconds(exc, attempt)
                        if self._question_budget_exhausted(started_at, extra_seconds=sleep_seconds):
                            break
                        time.sleep(sleep_seconds)
                        continue
                    if attempt == self.config.max_retries:
                        break
                    sleep_seconds = self._retry_sleep_seconds(exc, attempt)
                    if self._question_budget_exhausted(started_at, extra_seconds=sleep_seconds):
                        break
                    time.sleep(sleep_seconds)
            if self._question_budget_exhausted(started_at):
                break
        if fallback_reasoning:
            return fallback_reasoning
        if isinstance(last_error, APILimitError):
            raise last_error
        raise RuntimeError(f"Model call failed after {self.config.max_retries} attempts: {last_error}")

    def _create_chat_completion(self, request_kwargs: dict[str, Any]) -> Any:
        if os.name == "nt":
            return self.client.chat.completions.create(**request_kwargs)
        hard_timeout = self.config.hard_timeout_seconds
        request_timeout = request_kwargs.get("timeout")
        if request_timeout is not None:
            hard_timeout = min(hard_timeout, float(request_timeout)) if hard_timeout else float(request_timeout)
        if not hard_timeout or hard_timeout <= 0:
            return self.client.chat.completions.create(**request_kwargs)

        ctx = multiprocessing.get_context("spawn")
        result_queue = ctx.Queue()
        config_payload = {
            "api_key": self.config.api_key,
            "base_url": self.config.base_url,
            "default_headers": self.config.default_headers,
        }
        proc = ctx.Process(target=_chat_completion_worker, args=(config_payload, request_kwargs, result_queue))
        proc.start()
        proc.join(hard_timeout)
        if proc.is_alive():
            proc.terminate()
            proc.join()
            raise TimeoutError(f"Model call exceeded hard timeout of {hard_timeout} seconds")
        if result_queue.empty():
            raise RuntimeError(f"Model subprocess exited without returning a result (exit code {proc.exitcode})")
        payload = result_queue.get()
        if not payload.get("ok"):
            raise RuntimeError(payload.get("error", "Unknown subprocess model call failure"))
        return ChatCompletion.model_validate(payload["response"])

    def _question_budget_exhausted(self, started_at: float, *, extra_seconds: float = 0.0) -> bool:
        budget = self.config.max_question_seconds
        if not budget or budget <= 0:
            return False
        return (time.monotonic() - started_at + extra_seconds) >= budget

    def _remaining_question_seconds(self, started_at: float) -> float | None:
        budget = self.config.max_question_seconds
        if not budget or budget <= 0:
            return None
        return max(0.0, budget - (time.monotonic() - started_at))

    def _throttle(self) -> None:
        interval = max(0.0, float(self.config.min_request_interval_seconds))
        if interval <= 0:
            return
        with self._request_lock:
            now = time.time()
            wait = interval - (now - self._last_request_ts)
            if wait > 0:
                time.sleep(wait)
            self._last_request_ts = time.time()

    def _retry_sleep_seconds(self, exc: Exception, attempt: int) -> float:
        if is_api_limit_error(exc):
            return max(self.config.api_limit_cooldown_seconds * attempt, self.config.retry_wait_seconds * (2**attempt))
        text = str(exc).lower()
        if "429" in text or "rate limit" in text or "速率限制" in text:
            return max(self.config.retry_wait_seconds * (2**attempt), 15.0)
        return self.config.retry_wait_seconds * attempt


def make_openclaw_client(
    *,
    model: str = "openclaw:main",
    base_url: str | None = None,
    api_key: str | None = None,
    temperature: float = 0.0,
    max_tokens: int = 1024,
    timeout: float = 180.0,
    max_retries: int = 3,
    retry_wait_seconds: float = 2.0,
    min_request_interval_seconds: float | None = None,
    thinking_type: str | None = None,
    max_question_seconds: float | None = None,
    hard_timeout_seconds: float | None = None,
    fallback_disable_thinking: bool = False,
    fallback_max_tokens: int | None = None,
    api_limit_cooldown_seconds: float = 60.0,
) -> OpenAICompatibleClient:
    resolved_base_url = base_url or os.getenv("OPENCLAW_OPENAI_BASE_URL") or "http://127.0.0.1:18789/v1"
    resolved_api_key = api_key or os.getenv("OPENCLAW_GATEWAY_TOKEN")
    config = ModelConfig(
        model=model,
        base_url=resolved_base_url,
        api_key=resolved_api_key,
        temperature=temperature,
        max_tokens=max_tokens,
        timeout=timeout,
        max_retries=max_retries,
        retry_wait_seconds=retry_wait_seconds,
        min_request_interval_seconds=min_request_interval_seconds or 0.0,
        thinking_type=thinking_type,
        max_question_seconds=max_question_seconds,
        hard_timeout_seconds=hard_timeout_seconds,
        fallback_disable_thinking=fallback_disable_thinking,
        fallback_max_tokens=fallback_max_tokens,
        api_limit_cooldown_seconds=api_limit_cooldown_seconds,
    )
    return OpenAICompatibleClient(config)


def make_openai_client(
    *,
    model: str | None = None,
    base_url: str | None = None,
    api_key: str | None = None,
    temperature: float = 0.0,
    max_tokens: int = 1024,
    timeout: float = 180.0,
    max_retries: int = 3,
    retry_wait_seconds: float = 2.0,
    min_request_interval_seconds: float | None = None,
    thinking_type: str | None = None,
    empty_retry_max_tokens: int | None = None,
    max_question_seconds: float | None = None,
    hard_timeout_seconds: float | None = None,
    system_prompt: str | None = None,
    fallback_disable_thinking: bool = False,
    fallback_max_tokens: int | None = None,
    api_limit_cooldown_seconds: float = 60.0,
) -> OpenAICompatibleClient:
    return OpenAICompatibleClient(
        ModelConfig.from_env(
            model=model,
            base_url=base_url,
            api_key=api_key,
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=timeout,
            max_retries=max_retries,
            retry_wait_seconds=retry_wait_seconds,
            min_request_interval_seconds=min_request_interval_seconds,
            thinking_type=thinking_type,
            empty_retry_max_tokens=empty_retry_max_tokens,
            max_question_seconds=max_question_seconds,
            hard_timeout_seconds=hard_timeout_seconds,
            system_prompt=system_prompt,
            fallback_disable_thinking=fallback_disable_thinking,
            fallback_max_tokens=fallback_max_tokens,
            api_limit_cooldown_seconds=api_limit_cooldown_seconds,
        )
    )


def ensure_dir(path: str | Path) -> Path:
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def find_repo_root(
    start: str | Path,
    *,
    required_markers: tuple[str, ...] = ("scripts", "configs"),
) -> Path:
    start_path = Path(start).resolve()
    for candidate in [start_path, *start_path.parents]:
        if all((candidate / marker).exists() for marker in required_markers):
            return candidate
    raise RuntimeError("Could not locate repository root.")


def download_file(url: str, destination: str | Path, *, force: bool = False) -> Path:
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() and not force:
        return destination
    with urllib.request.urlopen(url, timeout=120) as response, destination.open("wb") as handle:
        handle.write(response.read())
    return destination


def read_json(path: str | Path) -> Any:
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def read_json_if_exists(
    path: str | Path,
    *,
    default: Any | None = None,
    encoding: str = "utf-8-sig",
) -> Any:
    path = Path(path)
    if not path.exists():
        return default
    with path.open("r", encoding=encoding) as handle:
        return json.load(handle)


def write_json(path: str | Path, data: Any) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)


def read_jsonl(path: str | Path) -> list[dict[str, Any]]:
    path = Path(path)
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def write_jsonl(path: str | Path, rows: list[dict[str, Any]]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False))
            handle.write("\n")


def safe_model_name(model_name: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", model_name).strip("_") or "model"


def parse_csv(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def normalize_whitespace(text: str) -> str:
    return " ".join(str(text).strip().split())


def first_nonempty_line(text: str) -> str:
    for line in str(text).splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return ""


def strip_wrapper(text: str) -> str:
    value = str(text).strip()
    if value.startswith("```") and value.endswith("```"):
        value = value.strip("`").strip()
    if ":" in value:
        prefix, suffix = value.split(":", 1)
        if prefix.strip().lower() in {"answer", "final answer", "response", "output"}:
            return suffix.strip()
    return value


def image_to_base64(image: Any, *, media_type: str = "image/jpeg") -> str:
    if isinstance(image, (bytes, bytearray)):
        return base64.b64encode(image).decode("utf-8")
    if isinstance(image, str):
        with open(image, "rb") as handle:
            return base64.b64encode(handle.read()).decode("utf-8")

    pil_image = image
    if getattr(pil_image, "mode", None) != "RGB":
        pil_image = pil_image.convert("RGB")

    fmt = "PNG" if media_type.endswith("png") else "JPEG"
    buffer = BytesIO()
    pil_image.save(buffer, format=fmt, quality=95)
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def maybe_import_rdkit() -> Any | None:
    try:
        from rdkit import Chem  # type: ignore

        return Chem
    except Exception:
        return None
