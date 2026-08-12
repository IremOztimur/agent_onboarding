# Checks

**Prefer a check over a sentence.** Agents treat instructions in context as
advisory; a rule that fails the commit is not optional. Before writing a rule
into `AGENTS.md`, ask whether a linter or a dependency contract can enforce it —
if so, write the check and leave one line of prose so the agent can plan against it.

Checks are not tests. Tests protect code that changes; checks constrain what an
agent is allowed to write, so their value scales with sessions, not codebase size.

## Common invariant → mechanism

| Invariant | Mechanism |
|---|---|
| Module / layer boundaries | `import-linter` (py), `dependency-cruiser` (ts), `depguard` (go) |
| Forbidden dependency in a package | `import-linter` forbidden contract |
| Type hints / docstrings required | `ruff` `ANN`, `D` |
| Commit message format | `commitlint` on `commit-msg` |
| No commits on protected branches | `no-commit-to-branch` hook |
| Secrets not committed | `detect-private-key`, `gitleaks` |
| Generated file stays in sync | regenerate, then `git diff --exit-code` |
| Lockfile current | `uv lock --check` / `--frozen-lockfile` |

## Day one

Formatter + linter, then `pre-commit` with the protected-branch guard, secret
detection, and commitlint. Encode the rule from `AGENTS.md` as a dependency
contract as soon as there is an architecture to protect.

```bash
cp checks/python/pre-commit-config.yaml .pre-commit-config.yaml
# merge checks/python/pyproject.snippet.toml into pyproject.toml
uv run pre-commit install --hook-type pre-commit --hook-type commit-msg
```

Delete rules you are not willing to keep green. A permanently red check teaches
agents to bypass the whole suite.
