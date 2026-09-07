"""Bounded, complete Markdown evidence shared by retrieval and model prompts."""

from __future__ import annotations

import re

from scripts.design.generated_runtime_support import RetrievedDocument


MAX_EVIDENCE_CHARS = 3200
TOTAL_EVIDENCE_CHARS = 6400


def strip_frontmatter(text: str) -> str:
    return re.sub(r"\A\ufeff?---\s*\n.*?\n---\s*(?:\n|$)", "", text, count=1, flags=re.S).strip()


def has_substantive_evidence(text: str) -> bool:
    """Reject metadata/navigation stubs, not short equations or scientific tables."""
    for raw in strip_frontmatter(text).splitlines():
        line = raw.strip()
        if not line or re.match(r"^#{1,6}\s", line):
            continue
        if re.match(r"^(?:[-*>]\s*)?\[?(?:\*\*)?(?:source(?:\s+url)?|url|citation|license|author|L[1-4])(?:\*\*)?\s*:", line, re.I):
            continue
        if re.match(r"^(?:scrape|fetch|download|extraction)(?:\s+\w+){0,2}\s*(?:error|failed|failure)\b", line, re.I):
            continue
        if re.fullmatch(r"(?:home|back|next|previous|contents|table of contents|sign in|log in|page not found|access denied|403 forbidden|404 not found)[.!]?", line, re.I):
            continue
        navigation = re.sub(r"^[-*>]\s*", "", line)
        if re.fullmatch(r"(?:search this book|download (?:page|full book) \(?pdf\)?|(?:downloads|resources|reference|tools|help) expand_more|periodic table|physics constants|scientific calculator|reference & cite|get help|feedback|readability|this action is not available\.?|L[1-4] link)", navigation, re.I):
            continue
        # Linked page titles, image links and bare URLs alone are not evidence.
        line = re.sub(r"!?\[[^\]]*\]\([^)]*\)|https?://\S+|<[^>]+>", "", line)
        line = re.sub(r"^\s*(?:[-*>+]\s+|\d+[.)]\s+)", "", line).strip(" |:-`$#")
        if re.search(r"[A-Za-z0-9\u0080-\uffff]", line):
            return True
    return False


def evidence_warning(text: str, *, max_chars: int = MAX_EVIDENCE_CHARS) -> str | None:
    if not has_substantive_evidence(text):
        return "non_substantive_reference_resource"
    if len(text) > max_chars:
        return "complete_evidence_exceeds_budget"
    return None


def evidence_sections(text: str) -> list[tuple[str, str]]:
    """Keep heading subtrees atomic, with ancestor definitions and document guards.

    Oversized packets are omitted by the caller, never sliced. Child packets retain
    parent introductions (often units/definitions) and explicit guard sections.
    """
    text = strip_frontmatter(text)
    lines = text.splitlines(keepends=True)
    headings: list[tuple[int, int, str]] = []
    offset = 0
    fence = ""
    for line in lines:
        marker = re.match(r"^\s*(`{3,}|~{3,})", line)
        if marker:
            token = marker.group(1)
            if not fence:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = ""
        elif not fence:
            match = re.match(r"^(#{1,6})\s+(.+)", line)
            if match:
                headings.append((offset, len(match.group(1)), match.group(2).strip()))
        offset += len(line)
    if not headings:
        return [("", text)] if has_substantive_evidence(text) else []

    ends = [next((pos for pos, level, _ in headings[i + 1:] if level <= depth), len(text))
            for i, (_, depth, _) in enumerate(headings)]
    parents = [next((j for j in range(i - 1, -1, -1)
                     if headings[j][1] < depth and ends[j] > start), None)
               for i, (start, depth, _) in enumerate(headings)]
    guard_ids = [i for i, (_, _, title) in enumerate(headings)
                 if re.search(r"\b(guards?|assumptions?|limitations?|validity|units?(?!\s+cell\b)|cautions?|warnings?)\b", title, re.I)]
    packets = []
    for i, (start, depth, title) in enumerate(headings):
        own = text[start:ends[i]].strip()
        if not has_substantive_evidence(own):
            continue
        spans = [(0, headings[0][0])] if headings[0][0] else []
        for j, (pos, level, _) in enumerate(headings[:i]):
            if level < depth and ends[j] > start:
                intro_end = headings[j + 1][0]
                intro = text[pos:intro_end]
                if re.search(r"[=|$]|\b(?:units?|definitions?|defined|denotes?|where|assum\w*|valid\w*|only|must|pressure|temperature|concentration)\b", intro, re.I):
                    spans.append((pos, intro_end))
                else:
                    spans.append((pos, text.find("\n", pos) + 1))
        spans.append((start, ends[i]))
        ancestors = {i, parents[i]}
        ancestor = parents[i]
        while ancestor is not None:
            ancestors.add(ancestor)
            ancestor = parents[ancestor]
        spans.extend((headings[j][0], ends[j]) for j in guard_ids
                     if parents[j] in ancestors)
        # Merge overlapping source spans so guards already in a subtree appear once.
        merged: list[tuple[int, int]] = []
        for left, right in sorted(spans):
            if merged and left <= merged[-1][1]:
                merged[-1] = (merged[-1][0], max(right, merged[-1][1]))
            else:
                merged.append((left, right))
        packets.append((title, "\n\n".join(text[a:b].strip() for a, b in merged if text[a:b].strip())))
    return packets


def select_evidence_documents(
    docs: list[RetrievedDocument],
    *,
    max_documents: int = 5,
    total_chars: int = TOTAL_EVIDENCE_CHARS,
) -> tuple[list[RetrievedDocument], list[dict[str, str]]]:
    accepted: list[RetrievedDocument] = []
    warnings: list[dict[str, str]] = []
    used = 0
    seen: set[str] = set()
    for doc in docs:
        if doc.path in seen:
            continue
        warning = evidence_warning(doc.snippet)
        if warning is None and (len(accepted) >= max_documents or used + len(doc.snippet) > total_chars):
            warning = "complete_evidence_exceeds_prompt_budget"
        if warning:
            warnings.append({"path": doc.path, "title": doc.title, "warning": warning})
            continue
        seen.add(doc.path)
        accepted.append(doc)
        used += len(doc.snippet)
    return accepted, warnings
