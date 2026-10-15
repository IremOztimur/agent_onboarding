# Testing

<!-- How this project proves a change works. Fill it with
     /agent-onboarding:setup-testing or by hand. The rules are defaults the
     project owns: edit them, and delete what you will not keep green.
     Delete the Evals section if no part of the product runs an LLM. -->

A change is done when the tier its test plan names is green, and the output is
in the report. Tests protect code that changes; checks (`checks/`) constrain
what may be written. This file is about tests.

## Tiers

| Tier | What it proves | Command | Runs |
|---|---|---|---|
| unit | {{one module's behavior, offline, no network}} | `{{...}}` | every change |
| integration | {{the seams: real database, real filesystem, real API}} | `{{...}}` | {{when a seam changes, and before a PR}} |
| live | {{the system against production-like services}} | `tests/live_smoke.md` | only when a human arms it |

Mark integration tests so the default command skips them
({{e.g. `@pytest.mark.integration`, a `*.int.test.ts` suffix}}). A test that
needs a secret or the network is never in the unit tier.

## Rules

1. **A bug starts with a failing test.** Write it, watch it fail for the
   reason the bug describes, then fix the code.
2. **Never weaken a test to make it pass.** Deleting an assert, loosening an
   expected value, or adding `skip`/`xfail`/`.only` is a decision, not a fix.
   If a test is wrong, say so in the report and leave the change to a human.
   This is the code version of reward hacking: green without the behavior.
3. **Test behavior through the public seam,** not private helpers. A refactor
   that keeps behavior should not break a test.
4. **Fixtures come from reality.** {{Where: captured API payloads in
   `tests/fixtures/`, a seeded database, recorded runs.}} A hand-written
   fixture tests your guess about the API.
5. **Mock only what you do not own,** and only at the boundary:
   {{what may be mocked here, e.g. the payment provider, the clock}}. Never
   mock the module under test or your own code one call down.
6. **Pin both directions of a contract.** If "missing means violated" and
   "unset means unknown", there is a test for each, so neither drifts.
7. **One test per success criterion** in `INTENT.md` that code can check. A
   criterion with no test is listed under "Not checked yet".
8. **A flaky test is a bug.** Quarantine it with an issue link; never retry
   it until it passes.

## Live smoke

`tests/live_smoke.md` is a checklist a human arms, not an automated test. It
lists the preconditions, the exact budget (money, rate limits, accounts), the
steps, and what is recorded. The agent never runs it on its own initiative.

## Evals

<!-- module: evals. Only for behavior an LLM or agent produces. -->

Behavior a model produces is not deterministic, so it is evaluated, not
asserted: many cases, run several times, graded, and compared with a
baseline. The harness lives in `evals/`; `evals/README.md` holds the claim it
tests and the success criteria from `INTENT.md`.

- **Grade the outcome.** For an agent, check the end state of the
  environment (the record written, the file changed, the order placed), not
  what the transcript says it did.
- **Prefer code graders.** Exact match, schema, state check. Use an LLM grader
  only for judgment code cannot make, with a written rubric, a different model
  from the one under test, and an empirical answer (`correct`/`incorrect` or
  1–5). Calibrate it against about 20 hand-graded cases before trusting it.
- **Volume over polish.** Many automatically graded cases beat a few
  hand-graded ones. Every criterion has edge cases: empty, too long,
  ambiguous, adversarial, irrelevant.
- **Run N times** (default {{5}}) and report the pass rate, not one lucky run.
- **Compare with the baseline.** A drop past {{threshold}} on any criterion
  fails the run. A deliberate change to the baseline is its own commit, with
  the reason.
- **Read the transcripts.** Each run, open a sample of passing and failing
  cases and check for shortcuts: a grader fooled, an answer copied from the
  case, a broken case that nothing could pass, a refusal scored as a failure.
- **Keep cases private and new.** A case copied from a public benchmark may
  already be in the model's training data.
- **Bound every run:** max turns, tokens, and wall-clock time. A run that hits
  a bound is recorded as such, not retried until it passes.
- **Each tool gets cases** with malformed arguments and edge inputs. A tool
  the model misuses is fixed in the tool, not in the prompt.

## Not checked yet

- {{criterion or rule with no test, and why}}
