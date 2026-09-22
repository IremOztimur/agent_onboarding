# Agent Instructions

<!-- Fill every {{TOKEN}}, delete what does not apply, delete this line. Keep
     under ~60 lines: this file is loaded on every request. Depth goes to
     docs/guides/<area>.md. -->

## Project

{{ONE PARAGRAPH: what this does, who it is for, and what it deliberately does NOT do.}}

**Stack:** {{language + version, framework, datastore, package manager}}
**Layout:** {{only the non-obvious directories, one line each — skip what `ls` answers}}

## Commands

| Task | Command |
|---|---|
| install | `{{...}}` |
| run locally | `{{...}}` |
| test — all | `{{...}}` |
| test — one | `{{...}}` |
| lint + format | `{{...}}` |
| typecheck | `{{...}}` |

Never invent an invocation. If a command is missing here, ask for it, then add it.

## Rules

1. **{{The one rule that, if broken, means the design is wrong.}}**
   {{Why, in one sentence.}} <!-- enforced by: {{check, or `nothing yet`}} -->
2. **{{Rule.}}** {{Why.}}
3. **Small diffs.** Do not rewrite, reorganize, or reformat code the task did not require.
4. **No new files as a side effect.** No extra README, summary, or report unless asked.

## Workflow

- Non-trivial change: plan first (`/plan`), agree on it, then implement.
- Read the guide for an area before changing it; update that guide when behavior changes.
- State assumptions when a requirement has two readings. Push back when a simpler
  design or an existing pattern solves it better.
- Style is the linter's job. Run the lint command; do not hand-police formatting.
- The worktree may hold human edits. Inspect current content before editing and
  preserve unrelated changes.
- Before reporting a change done, run the test and lint commands above and reach
  green; if a check fails or can't run, say so instead of reporting done.
- Before opening a PR, run `/code-review` at the level the change warrants.

## Reporting

Say only what you verified, and name the evidence — command, exit status, test count, SHA.
`written` → `tests pass` → `merged` → `deployed` are separate claims; none implies the next.
If a check was skipped or failed, say so plainly. Your own second pass is not verification.

## Git

Conventional Commits. No trailers, ever. Never commit ordinary work on {{main}} —
branch first. Never push unless asked, every time.
Full procedure: `.agents/skills/commit/SKILL.md`.

## Where to look

| For | Read |
|---|---|
| what was decided or rejected, and why | `DECISIONS.md` |
| visual identity and banned UI patterns — read before any UI work | `DESIGN.md` |
| depth on {{area}} | `docs/guides/{{area}}.md` |
| work in flight | `docs/plans/` |

Directory-scoped rules live in `<dir>/AGENTS.md` and apply to everything under it.
