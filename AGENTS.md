# Agent Instructions

## Project

Agent Onboarding is a Claude Code plugin plus a modular template that
onboards a coding agent to a project. The plugin's skills ask the human and
write their answers into template files; `init` copies only the modules a
project needs. It deliberately does not prescribe a methodology: every way
of working ships as a default the project owns.

**Layout:**
- `plugin/skills/`: plugin skills (`init`, `setup-*`). They ask; they never hold a per-project value.
- `plugin/template/<module>/`: files copied into a project; each module's tree maps onto the project root.
- `DECISIONS.md`: decisions about this repo. `plugin/template/planning/DECISIONS.md` ships empty.

## Commands

| Task | Command |
|---|---|
| eval harness self-test | `python3 -I plugin/template/evals/evals/run.py --dry-run` |
| slop-check rules | `node plugin/template/design/checks/design/slop-check.mjs --rules` |
| no personal or repo values in the template | `grep -rnE "Miro|Figma|Canva|Graphify|Notion|agent_onboarding" plugin/template` (expect no output) |
| validate the plugin | `claude plugin validate .` |

## Rules

1. **Nothing in `plugin/template/` may hold this repo's own decisions,
   tools, or values.** It is copied into other people's projects; a value
   here becomes everyone's default.
2. **A plugin skill asks; it never guesses.** Unknown answers stay a
   `{{TOKEN}}` or an open question.
3. **A new skill clears the "write a skill only when..." bar in
   `DECISIONS.md`**, and the reason goes there too.
4. **A line in `plugin/template/core/AGENTS.md` that belongs to a module ends
   in `<!-- module: x -->`**, so `init` can remove it.
5. **Small diffs.** No new files as a side effect.

## Git

Conventional Commits. Never push unless asked. Protected branch: `main`.
