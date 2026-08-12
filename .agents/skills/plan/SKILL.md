---
name: plan
description: "Read this skill when planning a change in this repository — where the plan file goes, what it must contain, and when it gets deleted"
---

# Plan

The harness already has a planning mode. This is only the repository's
convention for the artifact it leaves behind.

Applies to work spanning more than one session. Shorter work needs no file.

1. **Check `DECISIONS.md` first.** Do not propose something already rejected there.
2. **Write the plan to `docs/plans/YYYY-MM-<slug>.md`.** The date prefix is how
   staleness becomes visible without opening the file.
3. **Include a `Done when:` line** — a command and its expected output, not "when
   it feels complete". A plan without an observable completion condition lets an
   agent declare victory at the point it stopped typing.
4. **Reference, do not paste.** `src/x.py:120`, never a copied snippet; the copy
   is stale on the next commit.
5. **Delete the plan when the work lands.** What survives graduates: durable
   knowledge to `docs/guides/`, choices to `DECISIONS.md`.
