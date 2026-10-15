"""The system under evaluation. Wire `run` to the real thing.

`run` gets one case's input and the run budget, and returns a dict:

    output:     what the system answered (str or JSON-able)
    state:      the environment after the run, for `env_state` graders
    transcript: the steps taken (messages, tool calls), for review
    usage:      {"input_tokens": int, "output_tokens": int, "turns": int}
    stopped:    None, or the bound that ended the run ("max_turns", ...)

Run it the way it runs for users: the same prompt, tools and harness. An
eval of a stripped-down setup measures a different system.
"""

from __future__ import annotations

from typing import Any


def run(case_input: dict[str, Any], budget: dict[str, int]) -> dict[str, Any]:
    raise NotImplementedError(
        "Wire evals/target.py to the system under test, or run with --dry-run."
    )
