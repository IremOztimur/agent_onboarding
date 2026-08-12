# Agent Markdown Layer

A small starting skeleton for a new project you will build together with a
coding agent. Copy it, fill it in, delete what you do not use.

## When to use it

Take it when a repository will be worked on with a coding agent across more than
a few sessions — that is when an agent re-deriving the stack, the test command,
and last month's rejected idea starts costing real time.

Skip it for a throwaway script or a spike you will delete. Take the pieces you
need: `AGENTS.md` alone is most of the value, and every other file here earns its
place only once a specific problem shows up.

## Principle

**Load permanent context always, everything else on demand — and prefer a check
over a sentence.**

`AGENTS.md` is paid for on every request, so it holds only what is true for every
task: what the project is, how to run and test it, and the few rules that must
never break. Depth lives in `docs/guides/`, in-flight work in `docs/plans/`,
settled arguments in `DECISIONS.md`. Anything a linter can enforce is a linter
rule, not a paragraph.

## Layout

```
AGENTS.md            the constitution — vendor-neutral, ~60 lines, always loaded
CLAUDE.md            @AGENTS.md — a pointer, never a fork
DECISIONS.md         what was decided and rejected, with reasons

.agents/skills/      procedures the harness does not already own: plan, commit
.claude/skills/      symlinks into .agents/skills — never copies
.claude/settings.json  format-on-write hook + read-only command allowlist

docs/guides/         durable depth, one file per area, read when that area is touched
docs/plans/          dated plans for multi-session work, deleted on completion

checks/              linter + pre-commit starters
```

## Start a new project

1. `git clone git@github.com:IremOztimur/markdown_layer.git <new-project>` then
   `cd <new-project> && rm -rf .git && git init`
2. **Write `AGENTS.md` by hand.** Fill the Project and Commands sections first —
   they carry most of the value. Leave a rule out rather than guessing at it;
   an unfilled `{{TOKEN}}` is an instruction to follow nonsense.
3. Adopt the checks: copy `checks/python/*` into place and
   `uv run pre-commit install --hook-type pre-commit --hook-type commit-msg`.
4. Point `.claude/hooks/format.sh` at your formatter.
5. Ask an agent: *"What does this project do and how do I run its tests?"*
   If it cannot answer from `AGENTS.md` alone, that file is not done yet.

Add `DECISIONS.md` entries as you make real choices, a guide when a section of
`AGENTS.md` grows past ~40 lines, and a directory `AGENTS.md` when a rule only
applies there.

**Write a skill only when it overrides a harness default or encodes a convention
the harness cannot guess.** Re-teaching something the agent already does — how to
plan, how to review a diff — produces a weaker copy of a built-in that drifts
further behind with every release. `commit` exists because the harness injects a
`Co-authored-by` trailer this repository does not want, and because branch and
push policy are per-project. That is the bar.
