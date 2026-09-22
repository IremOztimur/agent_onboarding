# Decisions

<!-- Append-only. One entry per real choice — if it was obvious, it was not a
     decision. The reason is the load-bearing part: without it the entry reads
     as arbitrary and gets re-argued. Supersede, never delete. -->

## Decided

**Verification and review are `AGENTS.md` workflow lines that point at existing
tools, not new skills.**
The harness already runs a verify-iterate loop and ships `/code-review`; a
custom skill for either would duplicate a harness default and drift out of
date (see the "write a skill only when..." bar in `README.md`). The actual
gap was connective tissue: a rule naming the check and requiring green before
"done" is reported, and a pointer to run `/code-review` before a PR.
Repo-specific invariants a generic reviewer can't infer from the diff belong
in `docs/guides/review.md`, not a bespoke review skill.

## Rejected

- **{{The attractive idea that keeps coming back}}** — {{the concrete reason it fails here}}

## Superseded

- ~~{{old decision}}~~ — {{YYYY-MM-DD}}, replaced by {{new}}: {{why it changed}}

## Open

- {{question}} — settled by {{what evidence would decide it}}
