# Eval report — {date} @ {sha}

## Claim

<!-- Copy from evals/README.md: what this run is evidence for. -->
See `evals/README.md` § Claim.

## Configuration

{config}

## Scores

{scores}

Errors, refusals and runs stopped at a bound are counted separately and are
not in the pass rate. A difference smaller than the confidence interval is
noise.

## Verdict

{verdict}

## Validity checks

Fill these in before trusting the score. `transcripts.jsonl` holds every
attempt.

- [ ] **Shortcuts (reward hacking).** Read the passes below: did each one do the
      work, or satisfy the grader some other way (copied text from the input,
      gamed a lenient regex, talked the LLM grader into it)?
- [ ] **Broken cases.** Read the failures below: could anything have passed?
      Wrong reference, ambiguous prompt, missing file, flaky tool.
- [ ] **Refusals.** Are refusals hiding failures, or failures hiding refusals?
- [ ] **Contamination.** Are the cases new and private, not copied from a
      public benchmark the model may have seen?
- [ ] **Config matches production.** Same prompt, tools, model and harness as
      what users run.

### Sample to read

{sample}
