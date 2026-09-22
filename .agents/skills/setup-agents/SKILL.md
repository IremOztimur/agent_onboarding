---
name: setup-agents
description: "Fill this project's AGENTS.md through a short Q&A instead of hand-editing {{TOKEN}}s — read before running /setup-agents"
---

# Setup Agents

Fill `AGENTS.md` through conversation instead of hand-editing `{{TOKEN}}`s.
An unfilled token is better than a guessed one — never invent an answer.

## Steps

1. Read the current `AGENTS.md`. If a section already holds real content
   (not a `{{TOKEN}}`), leave it — do not overwrite a human's existing
   answer.
2. Before asking Stack or Commands, check the repo for what's derivable —
   lockfiles (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`,
   `Gemfile`), scripts (`package.json` scripts, `Makefile`, `justfile`), and
   any CI config. Propose what you find and ask the human to confirm or
   correct it. Don't ask a question you can answer yourself; don't silently
   trust what you found either.
3. Ask in this order, in small batches — never every question at once:
   - **Project**: what this does, who it's for, what it deliberately does
     NOT do (one paragraph).
   - **Stack**: language + version, framework, datastore, package manager.
   - **Layout**: only directories an `ls` wouldn't already explain.
   - **Commands**: install, run locally, test — all, test — one,
     lint + format, typecheck. Confirm the exact invocation; never invent
     one — the template already forbids that.
   - **Rules**: the one rule that, if broken, means the design is wrong,
     and why. Ask for a second only if the human has one ready.
   - **Protected branch**: the `{{main}}` token in `## Git` — confirm the
     integration branch name (main/master/dev). If it isn't `main`, also
     fill the matching placeholder in the "Protected branches" section of
     `.agents/skills/commit/SKILL.md` (`{{main / master / dev — set per
     project}}`), so the two files stay consistent.
4. Answer unknown → leave that `{{TOKEN}}` in place and say so. Do not fill
   it with a plausible-sounding guess.
5. Write answers into `AGENTS.md` in place, keep the file under ~60 lines,
   and delete the top guidance comment once every section you asked about
   is resolved — leave the comment if tokens remain.
6. Leave `## Workflow`, `## Reporting`, and `## Where to look` as the
   template already has them; they are shared defaults, not per-project
   answers.
