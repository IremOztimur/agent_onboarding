---
name: init
description: "Install the agent-onboarding template into this project, sized to it: asks the project's shape and copies only the modules that apply. Run once per project, before the setup-* skills."
---

# Init

Copy the template into the current project, only the parts that fit. This
skill decides nothing about how the project works; it picks files. Every file
it copies belongs to the project afterwards.

The template lives next to this skill: `<this skill's base directory>/../../template/`.
Each subdirectory is a module whose contents map onto the project root.

## Modules

| Module | Installs | When |
|---|---|---|
| `core` | `AGENTS.md`, `CLAUDE.md`, `INTENT.md`, `commit` skill, `.claude/settings.json`, format hook, `checks/README.md` | always, except a script |
| `testing` | `docs/guides/testing.md`, `test` skill, `verifier` agent, `tests/live_smoke.md` | small and up |
| `planning` | `plan` skill, `docs/plans/`, `docs/guides/workflow.md`, `DECISIONS.md` | multi-session work |
| `evals` | `evals/` harness | any part of the product runs an LLM or an agent loop |
| `design` | `DESIGN.md`, `checks/design/` | there is a UI |
| `lang-python`, `lang-node` | `checks/<lang>/` pre-commit starters | per language |
| `review` | `docs/guides/review.md` | never at init: offer it after a generic reviewer misses something |

A script gets `AGENTS.md` and `CLAUDE.md` only: Project and Commands, nothing else.

## Steps

1. **Look before asking.** Read lockfiles and manifests (`package.json`,
   `pyproject.toml`, `go.mod`, `Cargo.toml`, `Gemfile`), the top-level
   layout, and imports of model SDKs (`anthropic`, `openai`, agent
   frameworks) or UI frameworks. Read `.agents/onboarding.json` if it exists:
   the project was initialised before, so offer to add modules instead.
2. **Ask the shape in one batch**, proposing what you found:
   - Size: a script, small (a few sessions), or multi-session work?
   - Surfaces: UI, backend/API, CLI or library, LLM or agent behavior?
     (more than one is fine)
   - Language(s)?
   Confirm the module list from the table above and let the human add or
   drop any module before copying.
3. **Check for conflicts.** For every file a module would write, check
   whether it exists. Never overwrite. List the conflicts, and for each ask:
   keep theirs, take the template's, or merge (show the difference first).
4. **Copy** each module's tree into the project root (`cp -R
   <template>/<module>/. ./`, minus conflicts kept as theirs). Then recreate
   the skill links, because symlinks may not survive the plugin cache:
   for every directory in `.agents/skills/`, `ln -s ../../.agents/skills/<name>
   .claude/skills/<name>` if missing.
5. **Trim to what was installed.**
   - In `AGENTS.md`, delete every line ending in `<!-- module: x -->` whose
     module was not installed, then strip the marker from the lines that
     remain. Delete the header comment's paragraph about markers.
   - In `docs/guides/testing.md`, delete the Evals section if `evals` was
     not installed.
   - In `INTENT.md`, delete "Why an agent" and "Loop contract" if the
     project has no LLM or agent behavior.
   - In `.claude/hooks/format.sh`, uncomment the case for each installed
     language and the UI case if `design` was installed; delete the cases for
     languages the project does not use.
   - In `checks/README.md`, delete the Design section if `design` was not
     installed.
6. **Record the shape** in `.agents/onboarding.json`:
   `{"size": "...", "surfaces": [...], "languages": [...], "modules": [...]}`.
   Later `setup-*` skills read it to know which sections apply.
7. **Report** the files written, the conflicts and how each was settled, and
   the next steps, in order: `/agent-onboarding:setup-intent`, then
   `setup-agents`, then `setup-testing` (if `testing` was installed), then
   `setup-workflow` (if `planning` was installed). Do not run them unasked.
