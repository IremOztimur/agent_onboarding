"""Graders for eval cases.

Each grader takes the case's grader spec and the target's result, and returns
a Grade. Prefer the code graders; use `llm_rubric` only for judgment code
cannot make. `human` marks a case for hand grading: it is reported, never
scored, and exists to calibrate `llm_rubric`.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class Grade:
    passed: bool | None  # None: not scored (human review, grader error)
    reason: str


def _text(result: dict[str, Any]) -> str:
    output = result.get("output", "")
    return output if isinstance(output, str) else json.dumps(output, sort_keys=True)


def exact(spec: dict[str, Any], result: dict[str, Any]) -> Grade:
    got, want = _text(result).strip().lower(), str(spec["expected"]).strip().lower()
    return Grade(got == want, f"expected {want!r}, got {got[:120]!r}")


def contains(spec: dict[str, Any], result: dict[str, Any]) -> Grade:
    text = _text(result).lower()
    missing = [s for s in spec["expected"] if s.lower() not in text]
    forbidden = [s for s in spec.get("forbidden", []) if s.lower() in text]
    ok = not missing and not forbidden
    return Grade(ok, f"missing {missing}, forbidden present {forbidden}")


def regex(spec: dict[str, Any], result: dict[str, Any]) -> Grade:
    ok = re.search(spec["pattern"], _text(result), re.MULTILINE) is not None
    return Grade(ok, f"pattern {spec['pattern']!r} {'matched' if ok else 'not found'}")


def json_fields(spec: dict[str, Any], result: dict[str, Any]) -> Grade:
    """Output parses as a JSON object with the required keys and values."""
    output = result.get("output")
    try:
        data = output if isinstance(output, dict) else json.loads(output)
    except (TypeError, ValueError) as exc:
        return Grade(False, f"output is not JSON: {exc}")
    missing = [k for k in spec.get("required", []) if k not in data]
    wrong = {k: data.get(k) for k, v in spec.get("equals", {}).items() if data.get(k) != v}
    return Grade(not missing and not wrong, f"missing {missing}, wrong {wrong}")


def env_state(spec: dict[str, Any], result: dict[str, Any]) -> Grade:
    """The environment ended in the expected state. Grades the outcome, not the transcript."""
    state = result.get("state") or {}
    wrong = {k: state.get(k) for k, v in spec["expected"].items() if state.get(k) != v}
    return Grade(not wrong, f"state differs at {wrong}" if wrong else "state matches")


GRADER_PROMPT = """You are grading one output against a rubric.

<rubric>
{rubric}
</rubric>

<input>
{input}
</input>

<output>
{output}
</output>

Think it through, then answer with exactly one of <result>correct</result> or
<result>incorrect</result>, followed by one sentence of reason."""


def llm_rubric(spec: dict[str, Any], result: dict[str, Any]) -> Grade:
    """LLM-graded against a written rubric. Use a different model from the one under test."""
    try:
        import anthropic
    except ImportError:
        return Grade(None, "llm_rubric needs the `anthropic` package")
    model = os.environ.get("EVAL_GRADER_MODEL")
    if not model:
        return Grade(None, "set EVAL_GRADER_MODEL to a model other than the one under test")
    client = anthropic.Anthropic()
    prompt = GRADER_PROMPT.format(
        rubric=spec["rubric"], input=json.dumps(result.get("input")), output=_text(result)
    )
    message = client.messages.create(
        model=model,
        max_tokens=16000,
        thinking={"type": "adaptive"},  # reason before the verdict
        messages=[{"role": "user", "content": prompt}],
    )
    if message.stop_reason != "end_turn":
        return Grade(None, f"grader stopped with {message.stop_reason}")
    text = "".join(b.text for b in message.content if b.type == "text")
    verdict = re.search(r"<result>\s*(correct|incorrect)\s*</result>", text, re.IGNORECASE)
    if not verdict:
        return Grade(None, f"grader gave no verdict: {text[:200]!r}")
    return Grade(verdict.group(1).lower() == "correct", text[verdict.end():].strip()[:200])


def human(spec: dict[str, Any], result: dict[str, Any]) -> Grade:
    return Grade(None, "needs human grading")


GRADERS: dict[str, Callable[[dict[str, Any], dict[str, Any]], Grade]] = {
    "exact": exact,
    "contains": contains,
    "regex": regex,
    "json_fields": json_fields,
    "env_state": env_state,
    "llm_rubric": llm_rubric,
    "human": human,
}


def grade(spec: dict[str, Any], result: dict[str, Any]) -> Grade:
    grader = GRADERS.get(spec.get("type", ""))
    if grader is None:
        return Grade(None, f"unknown grader {spec.get('type')!r}")
    try:
        return grader(spec, result)
    except Exception as exc:  # a broken grader is reported, never scored as a pass
        return Grade(None, f"grader error: {exc}")
