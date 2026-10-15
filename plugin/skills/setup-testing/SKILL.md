---
name: setup-testing
description: "Fill this project's docs/guides/testing.md (and evals/ for LLM projects) through a short Q&A: test tiers and their commands, what may be mocked, fixtures, live smoke, and eval criteria, graders and baseline. Read before running /setup-testing."
---

# Setup Testing

`docs/guides/testing.md` is the project's policy for proving a change works.
The rules in it are shipped defaults the project owns; the tiers, commands,
fixtures and thresholds are the human's answers. Never invent a command or a
threshold.

## Steps

1. Read `docs/guides/testing.md`, `.agents/onboarding.json`, `INTENT.md`
   (§ Success criteria), and the Commands table in `AGENTS.md`. Look at the
   repo for what is derivable: the test runner and its config, existing
   markers, a `tests/fixtures/` directory, CI jobs. Propose what you found
   and ask the human to confirm it.
2. Ask in small batches:
   - **Tiers:** which exist today (unit, integration, live), the exact
     command for each, and how integration tests are marked so the default
     command skips them. A tier that does not exist yet stays a
     `{{TOKEN}}`; say so.
   - **Boundaries:** what may be mocked (only things the project does not
     own), and where fixtures come from (captured payloads, a seeded
     database, recordings).
   - **Live smoke:** does anything touch a real service, money, or a shared
     account? If yes, fill `tests/live_smoke.md`: preconditions, budget, the
     arm word, steps, where results go. If no, delete that file and the
     section.
   - **Rules:** walk through the default rules in the file and ask which to
     keep, change, or delete. Do not argue for a default the human rejects.
3. **If `evals/` exists**, also ask:
   - **Claim:** what a passing run is evidence for, in one sentence.
   - **Criteria:** take each LLM-facing success criterion from `INTENT.md`,
     with its threshold, into `evals/criteria.json` and the README table. A
     criterion with no threshold stays open; do not choose one.
   - **Grading:** for each criterion, can code check it (state, exact,
     schema)? If not, the rubric, in the human's words, and which model
     grades (a different one from the model under test).
   - **Runs:** reps per case (default 5), budget per attempt (turns,
     tokens, seconds), and the regression tolerance.
   - **Target:** where the real entry point is, so `evals/target.py` can be
     wired to it. Offer to wire it; do not change the product code to make it
     testable without asking.
   - **First cases:** ask for real examples, including edge cases and one
     where the agent should not act. Write them to `evals/cases/` with a
     `reference` each, and delete the example cases. Then run
     `python evals/run.py --dry-run` and show the output.
4. Write the commands into the `AGENTS.md` Commands table (`test — all`,
   `test — one`, `test — integration`, `eval`). Never write a command the
   human did not confirm.
5. Any criterion or rule with no test or eval behind it goes under
   "Not checked yet" in `testing.md`.
6. Show the finished files and ask what is wrong before saving. Keep their
   wording.
