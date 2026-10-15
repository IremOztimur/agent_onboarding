---
name: setup-workflow
description: "Write this project's docs/guides/workflow.md from the human's own way of working, through a short Q&A. Read before running /setup-workflow."
---

# Setup Workflow

`docs/guides/workflow.md` says how a change goes from idea to merged PR: how
requirements are read, when work starts, what is checked, and when it counts
as done. That is the human's methodology, not yours. Your job is to write it
down in their words. Never fill a step with a practice they did not state.

## Steps

1. Read the current `docs/guides/workflow.md`. If it is the shipped default
   (it credits the AI-Native SDLC Playbook and has a "Not yet" section), tell
   the human there are two options: keep the default as it is, or write their
   own. Do not show the default's answers while asking; they anchor the
   answers.
2. Read `AGENTS.md`, `INTENT.md`, `DECISIONS.md`, `docs/guides/testing.md`,
   and the project skills in `.agents/skills/`. Do not ask about what they
   already say. Point to it.
3. Ask in this order, in small batches, never every question at once:
   - **Intent**: Where does work come from (an idea, an issue, a bug)? What
     do you need to know before anything is designed? Which questions should
     the agent ask you?
   - **Design**: What needs a design before code, and what does not? Where do
     designs live (a board, a file, nowhere)? Who settles open questions?
   - **Plan**: When may the agent start editing files? What must a plan name?
     Which changes are small enough to skip the plan?
   - **Build**: What does the agent run while it works? What may it never
     change to make a check pass?
   - **Test**: What proves a change works, by size of change? Which tier
     runs when, and who arms the live one? For LLM behavior, when do evals
     run? (If `docs/guides/testing.md` answers this, point to it.)
   - **Done**: Who reviews it, against what? Who approves the merge?
   - **Learn**: What happens when the agent makes the same mistake twice?
     Where do rules and checks go?
   - **Tools**: Which tools does each step use, if any (issue tracker, notes,
     design board, UI tool, codebase map)? Write in only what they name. The
     default's `{{slots}}` that get no answer are deleted with their sentence.
4. Answer unknown or "it depends" → write that step as an open question in
   the file, not a guess.
5. Write the file with one section per step, plus a loop table with these
   columns: Loop, Trigger, Verify, Stop, Memory. Fill a cell only from what
   the human said. An empty cell is honest.
6. Every check named in the file must exist as a command in `AGENTS.md` or
   in `checks/`. If it does not, list it at the end under "Not enforced yet".
7. Show the human the finished file and ask what is wrong before you save.
   Keep their wording. Do not polish it into yours.
