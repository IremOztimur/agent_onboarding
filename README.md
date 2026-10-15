# Agent Onboarding

**Make any repo agent-ready in ten minutes, without adopting someone else's process.**

A Claude Code plugin that interviews you about your project and writes the
files your coding agent reads: what the project is, how to run and test it,
the rules that must never break. It installs only what your project needs,
and every file it writes is yours to edit.

## Why

| Without it | With it |
|---|---|
| Session four, the agent still asks for the test command | Session one knows it, because `AGENTS.md` says so |
| "Done!", with no proof | "Done" means the test tier ran green, with the output pasted |
| A failing test gets "fixed" by skipping it | A weakened test is flagged as a finding, not merged |
| A one-file CLI gets a full-stack scaffold | A script gets one file; a big app gets the full set |
| A prompt change ships on vibes | LLM behavior is evaluated against a baseline before it ships |

## Quickstart

```
/plugin marketplace add IremOztimur/agent_onboarding
/plugin install agent-onboarding@agent-onboarding
```

Then, inside your project:

```
/agent-onboarding:init            # looks at the repo, asks its shape, installs what fits
/agent-onboarding:setup-intent    # what the product is for, and what "working" means
/agent-onboarding:setup-agents    # commands, stack, the rules that must not break
/agent-onboarding:setup-testing   # test tiers, fixtures, and evals for LLM features
```

Each skill asks a few questions and writes the answers down. It never
guesses: an answer you don't have stays a visible `{{TOKEN}}`, not a
plausible invention. `init` never overwrites an existing file.

**Done when:** a fresh agent session can tell you what the project does and
how to test it, from the files alone.

## What lands in your repo

`init` picks modules from your project's shape. Re-run it to add one later.

| Your project | You get |
|---|---|
| A script | `AGENTS.md` |
| Small, a few sessions | + `INTENT.md`, `docs/guides/testing.md`, `commit` and `test` skills, a `verifier` agent, a format hook |
| Multi-session work | + `plan` skill, `docs/plans/`, `docs/guides/workflow.md`, `DECISIONS.md` |
| Has a UI | + `DESIGN.md` and a check that blocks generic AI-look UI patterns |
| Runs an LLM or an agent | + `evals/`: cases, graders, a runner, a baseline |

The key files:

- **`AGENTS.md`**: loaded on every request, so it holds only what's always
  true: the project, its commands, its rules. Works with any agent that reads
  [AGENTS.md](https://agents.md/).
- **`INTENT.md`**: why the project exists and its success criteria, written
  so a test or an eval can check them.
- **`docs/guides/testing.md`**: which tests a change needs, what may be
  mocked, and the rule the agent can't break: never weaken a test to pass.
- **`evals/`**: for LLM features. Runs each case several times, grades the
  outcome (code graders first, an LLM judge only when needed), compares
  against a baseline, and self-tests offline with `--dry-run`.

## How it works

1. **It asks, you answer.** How your agent works is your methodology. The
   plugin only asks questions; the answers and defaults live in your repo,
   and a plugin update never changes them.
2. **Always-true goes in context, the rest on demand.** `AGENTS.md` stays
   short. Depth lives in `docs/guides/`, plans in `docs/plans/`, settled
   arguments in `DECISIONS.md`.
3. **A check beats a sentence.** Anything a tool can enforce becomes a hook
   or a pre-commit check, not a line the agent may ignore.

The default workflow, which you can keep, edit, or replace with
`/agent-onboarding:setup-workflow`:

**Intent → Design → Plan → Build → Test → Review → Learn**

Each step leaves a file the next one reads. You decide at the gates; the
agent works between them. The same mistake twice becomes a rule or a check.

## FAQ

**Will it overwrite my files?** No. `init` lists every conflict and asks:
keep yours, take the template's, or merge.

**Do I need Claude Code?** For the interview skills, yes. The files
themselves are vendor-neutral; to use them with another agent, copy the
modules from `plugin/template/` by hand (see `AGENTS.md` comments for the
`module:` markers to trim).

**How is this different from Spec Kit or Superpowers?** Those give you a
process. This one writes down yours, sized to the project, and adds a real
eval harness for LLM features.

**Is it worth it for a tiny project?** For a throwaway script, `init`
installs one file. Skip it entirely for code you'll delete this week.

## All skills

| Skill | Writes |
|---|---|
| `init` | the modules that fit your project |
| `setup-intent` | `INTENT.md` |
| `setup-agents` | `AGENTS.md` |
| `setup-testing` | `docs/guides/testing.md`, `evals/` |
| `setup-workflow` | `docs/guides/workflow.md`, your own loop |
| `setup-design` | `DESIGN.md` |
| `setup-review` | `docs/guides/review.md`, invariants a diff review can't see |

## Built on

[AI-Native SDLC Playbook](https://academy.claude.com/courses/ai-native-sdlc-playbook/introduction) ·
[Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) ·
[Define success criteria and build evaluations](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests) ·
[Trustworthy third party evaluations](https://openai.com/index/trustworthy-third-party-evaluations-foundations/) ·
[agents.md](https://agents.md/) ·
[Writing a good CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md) ·
[ADRs](https://adr.github.io/)

Design decisions for this repo, with reasons: [`DECISIONS.md`](DECISIONS.md).

## License

Apache-2.0
