# Agent Markdown Layer

A starting skeleton for a project you build together with a coding agent
across many sessions.

Copy it. Fill in `AGENTS.md`. Delete what you don't use.

## The problem

**Without it:** four sessions in, the agent still asks what the test command is.
**With it:** session one already knows, because `AGENTS.md` said so.

Nobody wants to re-explain the same handful of facts every week. Write them
down once.

## Quickstart

1. Clone it and drop the git history.
   ```
   git clone git@github.com:IremOztimur/markdown_layer.git <new-project>
   cd <new-project> && rm -rf .git && git init
   ```
2. Fill `AGENTS.md`. Run `/setup-agents` to fill it through conversation, or
   write it by hand. Either way, the Project and Commands sections carry most
   of the value. Leave a rule out rather than guess at it. An unfilled
   `{{TOKEN}}` is an instruction to follow nonsense.
3. Adopt the checks. Copy `checks/python/*` into place, then run:
   ```
   uv run pre-commit install --hook-type pre-commit --hook-type commit-msg
   ```
4. Point `.claude/hooks/format.sh` at your formatter.
5. Ask an agent what the project does and how to run its tests. If it can't
   answer from `AGENTS.md` alone, the file isn't done yet.

The rest is on demand, not day one. Run `/setup-design` once there's UI work
to do. Run `/setup-review` once a generic reviewer has missed something a
project invariant would have caught.

Add a `DECISIONS.md` entry each time you make a real choice. Add a guide once
a section of `AGENTS.md` passes about 40 lines. Add a directory `AGENTS.md`
once a rule only applies there.

## Layout

```
AGENTS.md            the constitution: vendor-neutral, about 60 lines, always loaded
CLAUDE.md            @AGENTS.md, a pointer, never a fork
DECISIONS.md         what was decided and rejected, with reasons
DESIGN.md            visual identity for agent-built UI: tokens, rules, banned patterns

.agents/skills/      procedures the harness doesn't already own: plan, commit,
                     setup-agents, setup-design, setup-review
.claude/skills/      symlinks into .agents/skills, never copies
.claude/settings.json  format-on-write hook plus a read-only command allowlist

docs/guides/         durable depth, one file per area, read when that area is touched
docs/plans/          dated plans for multi-session work, deleted on completion

checks/              pre-commit starters: python lint, DESIGN.md slop-check
```

## Principle

**Load what's always true into context. Load everything else on demand.
Prefer a check over a sentence.**

`AGENTS.md` is paid for on every request. It holds only what's true for every
task:

- what the project is
- how to run it and test it
- the rules that must never break

Depth lives in `docs/guides/`. In-flight work lives in `docs/plans/`. Settled
arguments live in `DECISIONS.md`. Anything a linter can enforce becomes a
linter rule, not a paragraph.

This isn't a house preference. It matches how the underlying tooling actually
behaves, and how its own maintainers say to use it. See References.

## When to use it

Take it when a repository will be worked on with a coding agent for more than
a few sessions. Skip it for a throwaway script or a spike you'll delete.

Take pieces, not the whole thing. `AGENTS.md` does most of the work here.
Every other file earns its place once a specific problem shows up, not
before.

**Write a skill only when it overrides a harness default or encodes a
convention the harness can't guess.** Re-teaching something the agent already
does, like how to plan or how to review a diff, produces a weaker copy of a
built-in that drifts further behind with every release. `commit` exists
because the harness injects a `Co-authored-by` trailer this repository
doesn't want, and because branch and push policy are per-project.
`setup-agents`/`setup-design`/`setup-review` exist because "ask, never guess,
when filling a template" is a convention no harness default encodes. That's
the bar.

## References

- [agents.md](https://agents.md/): the open AGENTS.md convention. This repo
  didn't invent the format, it fills in the file the convention defines.
- [Claude Code memory docs](https://docs.anthropic.com/en/docs/claude-code/memory):
  confirms `CLAUDE.md` and its `@import`s load into every session. "Always
  loaded" above isn't a metaphor.
- [Writing a good CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md)
  (HumanLayer): the rationale behind the Principle. Keep the always-loaded
  file universal. Prefer a deterministic check over an instruction. Push
  task-specific depth into files referenced by `file:line`, not pasted in.
- [Architectural Decision Records](https://adr.github.io/): the convention
  `DECISIONS.md` borrows. Decision plus reason. Append-only. Superseded,
  never deleted.
- [Claude Code Skills](https://code.claude.com/docs/en/skills): the feature
  `.agents/skills` and `.claude/skills` build on.

## License

Apache-2.0. See `LICENSE`.
