# Evals

<!-- Fill with /agent-onboarding:setup-testing or by hand. Delete this
     comment once the claim and criteria are real. -->

Tests assert deterministic code. Evals measure what a model or agent
produces: many cases, several runs each, graded, compared with a baseline.

## Claim

{{What a passing run is evidence for, in one sentence. e.g. "The support
agent resolves refund requests correctly with the production prompt and
tools, at most 10 turns per case."}}

## Success criteria

Copied from `INTENT.md` § Success criteria. Machine-readable thresholds live
in `criteria.json`; keep the two in sync.

| Criterion | What passes | Threshold |
|---|---|---|
| {{name}} | {{the outcome that counts}} | {{e.g. 0.90}} |

## Commands

| Task | Command |
|---|---|
| self-test the harness, offline | `python evals/run.py --dry-run` |
| run against the real system | `python evals/run.py` |
| accept a run as the new baseline | `python evals/run.py --update-baseline` |

Wire `evals/target.py` to the real entry point before the first real run.

## Cases

`cases/*.jsonl`, one JSON object per line:

```json
{"id": "refund-001", "criterion": "task_fidelity", "tags": ["happy"],
 "input": {"message": "..."},
 "grader": {"type": "env_state", "expected": {"refund_count": 1}, "reference": {"refund_count": 1}}}
```

- `criterion` names a key in `criteria.json`.
- `tags`: `happy`, `edge`, `adversarial`, `ambiguous`, `tool`. Every
  criterion has edge cases, and both directions: a case where the agent
  should act and one where it should not.
- `grader.reference` is a known-good answer. `--dry-run` checks that it
  passes its own grader, and that an empty answer does not.
- Write cases from real use where possible. Do not copy them from public
  benchmarks.

## Graders

In order of preference (`graders.py`):

| Type | Use for |
|---|---|
| `env_state` | agents: the environment ended in the expected state |
| `exact`, `contains`, `regex`, `json_fields` | outputs code can check |
| `llm_rubric` | judgment code cannot make. Needs `rubric`, and `EVAL_GRADER_MODEL` set to a model other than the one under test |
| `human` | calibrating `llm_rubric`: hand-grade about 20 cases and compare before trusting it |

## Rules

- A run is evidence about this system with this prompt, tools, harness and
  budget. Change any of them and the old baseline no longer compares.
- Changing `baseline.json` is its own commit, with the reason.
- Read the sample in each report before trusting the score.
- An LLM failure seen in use becomes a case here.
