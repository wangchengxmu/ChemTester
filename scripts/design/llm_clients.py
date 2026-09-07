from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from typing import Any

from openai import OpenAI

from scripts.core import ModelConfig, OpenAICompatibleClient, find_repo_root, make_openclaw_client


ROOT = find_repo_root(Path(__file__).resolve())


def normalize_reasoning_effort(reasoning_effort: str | None) -> str:
    value = str(reasoning_effort or "high").strip().lower()
    return value if value in {"minimal", "low", "medium", "high", "xhigh"} else "high"


def reasoning_effort_to_thinking_type(reasoning_effort: str | None) -> str | None:
    value = normalize_reasoning_effort(reasoning_effort)
    if value in {"medium", "high", "xhigh"}:
        return "enabled"
    if value in {"minimal", "low"}:
        return "disabled"
    return None


def openai_compatible_request_controls(
    model_name: str,
    reasoning_effort: str | None,
) -> tuple[float, str | None]:
    if str(model_name or "").strip().lower() == "kimi-k3":
        return 1.0, reasoning_effort_to_thinking_type(reasoning_effort)
    return 0.0, reasoning_effort_to_thinking_type(reasoning_effort)


def codex_code_mode_host_path(executable: str | Path) -> Path:
    return Path(executable).with_name("codex-code-mode-host.exe")


def _windows_codex_candidates() -> list[Path]:
    candidates: list[Path] = []

    def add(candidate: Path | None) -> None:
        if candidate is None:
            return
        expanded = candidate.expanduser()
        if expanded not in candidates:
            candidates.append(expanded)

    override = os.environ.get("CHEMTESTER_CODEX_EXECUTABLE")
    add(Path(override) if override else None)

    local_bin = Path(os.environ.get("LOCALAPPDATA", "")) / "OpenAI/Codex/bin"
    add(local_bin / "codex.exe")
    if local_bin.is_dir():
        versioned_directories = sorted(
            (path for path in local_bin.iterdir() if path.is_dir()),
            key=lambda path: path.stat().st_mtime_ns,
            reverse=True,
        )
        for directory in versioned_directories:
            add(directory / "codex.exe")

    add(
        Path(os.environ.get("APPDATA", ""))
        / "npm/node_modules/@openai/codex/node_modules/@openai/"
        "codex-win32-x64/vendor/x86_64-pc-windows-msvc/bin/codex.exe"
    )
    discovered = shutil.which("codex.exe") or shutil.which("codex")
    add(Path(discovered) if discovered else None)
    return candidates


def codex_base_command(*, require_code_mode_host: bool = False) -> list[str]:
    if os.name == "nt":
        checked: list[str] = []
        for candidate in _windows_codex_candidates():
            checked.append(str(candidate))
            if not candidate.is_file():
                continue
            if require_code_mode_host and not codex_code_mode_host_path(candidate).is_file():
                continue
            return [str(candidate.resolve())]
        requirement = (
            " with an adjacent codex-code-mode-host.exe"
            if require_code_mode_host
            else ""
        )
        checked_text = "; ".join(checked) or "no candidates"
        raise FileNotFoundError(
            f"Codex CLI executable{requirement} not found. Checked: {checked_text}. "
            "Set CHEMTESTER_CODEX_EXECUTABLE to a complete Codex installation."
        )
    return ["codex"]


class CodexCliTextClient:
    def __init__(
        self,
        *,
        repo_root: str | Path,
        model_name: str,
        reasoning_effort: str,
        timeout_seconds: float = 180.0,
        isolated_workspace: bool = False,
    ) -> None:
        candidate = Path(repo_root).resolve()
        candidate = candidate if candidate.is_dir() else candidate.parent
        self.repo_root = find_repo_root(candidate)
        self.model_name = model_name
        self.reasoning_effort = normalize_reasoning_effort(reasoning_effort)
        self.timeout_seconds = timeout_seconds
        self.isolated_workspace = bool(isolated_workspace)

    def complete_text(
        self,
        user_prompt: str,
        *,
        system_prompt: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> str:
        _ = temperature
        _ = max_tokens
        prompt = self._compose_prompt(user_prompt, system_prompt=system_prompt)
        return self._run_completion(prompt, image_paths=[])

    def complete_multimodal(
        self,
        user_prompt: str,
        *,
        image: str | Path,
        media_type: str | None = None,
        system_prompt: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> str:
        _ = media_type
        _ = temperature
        _ = max_tokens
        image_path = Path(image).resolve()
        if not image_path.is_file():
            raise FileNotFoundError(f"Codex image input is unavailable: {image_path}")
        prompt = self._compose_prompt(user_prompt, system_prompt=system_prompt)
        return self._run_completion(prompt, image_paths=[image_path])

    def _run_completion(self, prompt: str, *, image_paths: list[Path]) -> str:
        fd, output_name = tempfile.mkstemp(prefix="codex_text_", suffix=".txt")
        os.close(fd)
        output_path = Path(output_name)
        temporary_workspace: tempfile.TemporaryDirectory[str] | None = None
        try:
            run_root = self.repo_root
            if self.isolated_workspace:
                temporary_workspace = tempfile.TemporaryDirectory(
                    prefix="chemtester_codex_isolated_"
                )
                run_root = Path(temporary_workspace.name)
            command = [
                *codex_base_command(),
                "exec",
                "--ignore-user-config",
                "--ephemeral",
                "--model",
                self.model_name,
                "-c",
                f'model_reasoning_effort="{self.reasoning_effort}"',
                "--cd",
                str(run_root),
                "--sandbox",
                "read-only",
                "--skip-git-repo-check",
                "--output-last-message",
                str(output_path),
            ]
            for image_path in image_paths:
                command.extend(["--image", str(image_path)])
            command.append("-")
            stdout = ""
            stderr = ""
            try:
                completed = subprocess.run(
                    command,
                    cwd=str(run_root),
                    input=prompt,
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    timeout=self.timeout_seconds,
                    shell=False,
                )
                stdout = completed.stdout
                stderr = completed.stderr
                output_text = output_path.read_text(encoding="utf-8").strip()
                if completed.returncode != 0 and not output_text:
                    raise RuntimeError(
                        f"Codex CLI text client failed with code {completed.returncode}.\nstdout:\n{stdout}\n\nstderr:\n{stderr}"
                    )
            except subprocess.TimeoutExpired as exc:
                stdout = exc.stdout or ""
                stderr = exc.stderr or ""
                if not output_path.exists():
                    raise RuntimeError(
                        f"Codex CLI text client timed out before writing output.\nstdout:\n{stdout}\n\nstderr:\n{stderr}"
                    )
            output_text = output_path.read_text(encoding="utf-8").strip()
            if not output_text:
                raise RuntimeError("Codex CLI text client returned no final response.")
            return output_text
        finally:
            output_path.unlink(missing_ok=True)
            if temporary_workspace is not None:
                temporary_workspace.cleanup()

    def _compose_prompt(self, user_prompt: str, *, system_prompt: str | None) -> str:
        if not system_prompt:
            return str(user_prompt)
        return (
            "Follow the system instructions exactly.\n\n"
            "SYSTEM INSTRUCTIONS\n"
            f"{system_prompt}\n\n"
            "USER REQUEST\n"
            f"{user_prompt}\n"
        )


class ResponsesTextClient:
    def __init__(
        self,
        *,
        model_name: str,
        reasoning_effort: str,
        timeout_seconds: float = 180.0,
        max_output_tokens: int = 900,
    ) -> None:
        config = ModelConfig.from_env(model=model_name, timeout=timeout_seconds)
        if not config.api_key:
            raise ValueError("No API key available for the responses client.")
        self.client = OpenAI(
            api_key=config.api_key,
            base_url=config.base_url,
            default_headers=config.default_headers,
            max_retries=0,
        )
        self.model_name = model_name
        self.reasoning_effort = normalize_reasoning_effort(reasoning_effort)
        self.timeout_seconds = timeout_seconds
        self.max_output_tokens = max_output_tokens

    def complete_text(
        self,
        user_prompt: str,
        *,
        system_prompt: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> str:
        response = self.client.responses.create(
            model=self.model_name,
            reasoning={"effort": self.reasoning_effort},
            instructions=system_prompt or "",
            input=user_prompt,
            temperature=0.0 if temperature is None else temperature,
            max_output_tokens=max_tokens or self.max_output_tokens,
            timeout=self.timeout_seconds,
        )
        output_text = getattr(response, "output_text", "") or ""
        if output_text.strip():
            return output_text.strip()
        for item in getattr(response, "output", []) or []:
            content = getattr(item, "content", None) or item.get("content", [])
            for part in content:
                if getattr(part, "type", None) == "output_text":
                    text = getattr(part, "text", "")
                    if str(text).strip():
                        return str(text).strip()
                if isinstance(part, dict) and part.get("type") == "output_text" and str(part.get("text", "")).strip():
                    return str(part.get("text", "")).strip()
        raise RuntimeError("Responses API client returned no visible text.")


def build_text_client_from_profile(
    *,
    repo_root: str | Path,
    backend: str,
    model_name: str,
    reasoning_effort: str,
    timeout_seconds: float = 180.0,
    max_tokens: int = 900,
    max_retries: int = 2,
    isolated_workspace: bool = False,
) -> Any | None:
    normalized_backend = str(backend or "").strip().lower()
    if normalized_backend in {"offline", "none", "heuristic", "disabled"}:
        return None
    temperature, thinking_type = openai_compatible_request_controls(model_name, reasoning_effort)
    if normalized_backend in {"codex", "codex-cli"}:
        return CodexCliTextClient(
            repo_root=repo_root,
            model_name=model_name,
            reasoning_effort=reasoning_effort,
            timeout_seconds=timeout_seconds,
            isolated_workspace=isolated_workspace,
        )
    if normalized_backend == "openclaw":
        try:
            return make_openclaw_client(
                model=model_name,
                max_tokens=max_tokens,
                timeout=timeout_seconds,
                max_retries=max_retries,
                thinking_type=thinking_type,
            )
        except Exception:
            return None
    if normalized_backend in {"responses", "openai-responses"}:
        try:
            return ResponsesTextClient(
                model_name=model_name,
                reasoning_effort=reasoning_effort,
                timeout_seconds=timeout_seconds,
                max_output_tokens=max_tokens,
            )
        except Exception:
            return None
    if normalized_backend in {"openai-compatible", "chat-completions", "chat", "glm", "zai", "bigmodel"}:
        config = ModelConfig.from_env(
            model=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=timeout_seconds,
            max_retries=max_retries,
            thinking_type=thinking_type,
        )
        if not config.api_key:
            return None
        try:
            return OpenAICompatibleClient(config)
        except Exception:
            return None
    try:
        return ResponsesTextClient(
            model_name=model_name,
            reasoning_effort=reasoning_effort,
            timeout_seconds=timeout_seconds,
            max_output_tokens=max_tokens,
        )
    except Exception:
        config = ModelConfig.from_env(
            model=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=timeout_seconds,
            max_retries=max_retries,
            thinking_type=thinking_type,
        )
        if not config.api_key:
            return None
        try:
            return OpenAICompatibleClient(config)
        except Exception:
            return None
