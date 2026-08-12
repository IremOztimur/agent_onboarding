#!/bin/sh
# PostToolUse hook: format and lint the file the agent just wrote.
#
# Claude Code passes the tool payload as JSON on stdin; the written path is
# .tool_input.file_path. Exit 0 = silent success. Exit 2 = stderr is fed back to
# the agent to fix. Keep it fast: this runs after every edit.
#
# Point the cases below at this project's formatter, then delete the rest.
set -eu

payload=$(cat)
if command -v jq >/dev/null 2>&1; then
  file=$(printf '%s' "$payload" | jq -r '.tool_input.file_path // empty')
else
  file=$(printf '%s' "$payload" |
    sed -n 's/.*"file_path"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -n1)
fi

[ -n "${file:-}" ] && [ -f "$file" ] || exit 0

case "$file" in
  *.py)
    command -v uv >/dev/null 2>&1 || exit 0
    uv run ruff --version >/dev/null 2>&1 || exit 0  # ruff not installed here
    uv run ruff format -- "$file" >/dev/null 2>&1 || true
    if ! out=$(uv run ruff check --fix -- "$file" 2>&1); then
      printf 'ruff reported problems in %s:\n%s\n' "$file" "$out" >&2
      exit 2
    fi
    ;;
  # *.ts|*.tsx|*.js|*.jsx)
  #   npx --no-install prettier --write "$file" >/dev/null 2>&1 || true
  #   ;;
  *) exit 0 ;;
esac
