# Decisions

<!-- Decisions about this repository: the plugin and the template it ships.
     A project's own decisions go in its copy of
     plugin/template/planning/DECISIONS.md, which starts empty.
     Append-only. Supersede, never delete. -->

## Decided

**Write a skill only when it overrides a harness default or encodes a
convention the harness can't guess.**
Re-teaching something the agent already does, like how to plan or how to
review a diff, produces a weaker copy of a built-in that drifts further behind
with every release. `commit` clears the bar because the harness injects a
`Co-authored-by` trailer projects may not want, and branch and push policy are
per-project. `test` clears it because tier policy is per-project. The
`setup-*` skills clear it because "ask, never guess, when filling a template"
is a convention no harness default encodes.

**Review is an `AGENTS.md` workflow line that points at `/code-review`, not a
new skill.**
The harness ships `/code-review`; a custom review skill would duplicate a
harness default and drift out of date (see the bar above). Repo-specific
invariants a generic reviewer can't infer from the diff belong in
`docs/guides/review.md`.

**Testing gets a project-owned `test` skill; verification stays with the
`verifier` agent.**
Running tests is a harness default. Which tier a change needs, what may be
mocked, when a live smoke is armed, and when an eval must be re-run against
its baseline are per-project policy no harness can guess. That clears the
bar. The skill reads `docs/guides/testing.md` and holds no values itself.

**Plans are kept and closed, not deleted.**
The AI-Native SDLC Playbook keeps the plan as part of the audit trail: the
intent, the plan, the diff and the review together show what was asked, what
was decided and who approved it. A closed plan carries `Status: done` and the
PR link.

**The plugin asks; the template holds the answers.**
How an agent works is a team's methodology. A skill that prescribes it
imports someone else's culture, and a plugin update would change it silently
in every project. So the plugin holds only skills that ask and never guess,
plus `init`, which copies files and decides nothing. Everything that states a
way of working ships in the template as a default the project owns. A skill
never holds a per-project value.

**The template installs by module, sized to the project.**
Copying everything gave a CLI a `DESIGN.md` and a script a plan directory,
and every unfilled file is a `{{TOKEN}}` the agent may follow. `init` asks
the project's size and surfaces and copies only `core` plus the modules that
apply. `review` is never installed up front; it earns its place after a
generic reviewer misses something.

**Product intent lives in `INTENT.md`; a plan's intent is change-level.**
Restating the product's problem in every plan drifts. The plan says what this
change does and links the `INTENT.md` section it serves. Success criteria in
`INTENT.md` are measurable so tests and evals can be written against them.

**Evals ship only for projects with LLM or agent behavior.**
Deterministic code is tested, not evaluated. Non-deterministic behavior needs
repeated runs, graders and a baseline, and that machinery is weight a
library does not need.

**Personal tools are slots, not defaults.**
The default workflow names places ("your design board"), not products.
`setup-workflow` writes in the tools a project actually uses.

## Superseded

- ~~Verification and review are `AGENTS.md` workflow lines that point at
  existing tools, not new skills.~~ 2026-10-16, split into the review and
  testing decisions above: testing policy turned out to be per-project.
- ~~Delete plans when the work lands.~~ Replaced by "plans are kept and
  closed": the plan is part of the audit trail.
