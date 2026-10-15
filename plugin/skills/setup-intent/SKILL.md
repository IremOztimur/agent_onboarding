---
name: setup-intent
description: "Fill this project's INTENT.md through a short Q&A: the problem, outcome, users, measurable success criteria, invariants, non-goals, and for agent projects why an agent and the loop contract. Read before running /setup-intent."
---

# Setup Intent

`INTENT.md` says why the project exists and what "working" means. It is the
human's product judgment, not yours. Write it down in their words; never fill
a section with a plausible guess. An open question is honest, an invented
answer is not.

## Steps

1. Read `INTENT.md` and `.agents/onboarding.json`. Skip any section that
   already holds real content. Read the README and any existing spec, issue,
   or notes the human points at, and propose what they already answer.
2. Ask only the sections the project's shape needs, in small batches:
   - **Every project:** Problem (what is wrong today, for whom, how they cope
     now), Outcome (what exists when this works), Non-goals.
   - **Small and up:** Users (who, in what situation, what they already
     know), Success criteria, Invariants, Constraints, Open questions.
   - **LLM or agent behavior:** Why an agent, then the Loop contract.
3. **Success criteria must be measurable.** Push back on "fast", "accurate",
   "good UX": ask for the number, the data it is measured on, and the
   threshold. If the human does not know the threshold yet, write the
   criterion with `threshold: open` and add the question to Open questions.
   Ask, for each one, what will check it: a test, an eval, or nothing yet.
4. **Invariants are properties that hold in every version**, not features.
   Ask: what, if it ever happened, would mean the design is wrong? Ask for the
   failure it prevents.
5. **Why an agent:** ask what needs a model's decision, and what must stay
   deterministic. If the honest answer is "a fixed sequence of steps", say
   that a workflow or plain code may be simpler, and record the human's
   choice either way. For the Loop contract, ask each field: Trigger, Work,
   Verify (the ground truth checked at each step), Memory, Stop (including
   the bounds: max turns, tokens, time, and when it hands back to a human).
6. Unknown or "it depends" → Open questions, with what would settle it.
7. Show the finished file and ask what is wrong before saving. Keep their
   wording. Set `Status` and `Last revised`, and delete the template
   guidance comments for every section that is resolved.
8. Tell the human what flows from it: the most important invariant goes into
   `AGENTS.md` `## Rules` (`setup-agents` will propose it), and every
   criterion becomes a test or an eval (`setup-testing`).
