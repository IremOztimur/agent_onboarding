---
name: setup-review
description: "Fill this project's docs/guides/review.md through a short Q&A — read before running /setup-review"
---

# Setup Review

Fill `docs/guides/review.md` with what a generic reviewer (`/code-review`)
can't infer from a diff alone. Don't restate architecture and don't invent
an invariant to fill space — an empty section is honest, a fabricated one
isn't.

## Steps

1. Read the current `docs/guides/review.md`.
2. Ask, briefly:
   - Anything that's broken before that a diff-level review wouldn't have
     caught (a bug whose fix wasn't visible from the changed file alone)?
   - Any invariant that only shows up across files, not inside one?
   - Anything that looks wrong to a generic reviewer on purpose — a settled
     choice a reviewer might re-litigate? If it's recorded in
     `DECISIONS.md`, link it instead of re-explaining it.
3. Human has none yet → leave `## Invariants` and `## Do not flag` empty
   rather than inventing content. This file earns its place once a real
   invariant exists.
4. Write only what the human confirms; each invariant names the failure
   mode, not just the rule.
