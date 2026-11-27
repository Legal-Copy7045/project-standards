#!/usr/bin/env bash
# Installs the owner's defaults into ~/.claude for a Claude Code session (run by the cloud environment's setup script,
# or by hand): the standard and its templates in ~/.claude/standards, the owner-defaults block in ~/.claude/CLAUDE.md
# (between markers, so it is replaced, never duplicated) and the global skills in ~/.claude/skills.
# Usage: bash install.sh [standards checkout] (default: the directory this script is in). Idempotent.
set -euo pipefail
src="$(cd "${1:-$(dirname "$0")}" && pwd)"
dest="$HOME/.claude"
mkdir -p "$dest/skills"
if [ "$src" != "$dest/standards" ]; then
  rm -rf "$dest/standards.new" && cp -r "$src" "$dest/standards.new" && rm -rf "$dest/standards.new/.git"
  rm -rf "$dest/standards" && mv "$dest/standards.new" "$dest/standards"
fi
f="$dest/CLAUDE.md"; touch "$f"
sed -i '/^<!-- owner-defaults:start -->$/,/^<!-- owner-defaults:end -->$/d' "$f"
{ echo "<!-- owner-defaults:start -->"; cat "$src/claude/CLAUDE.md"; echo "<!-- owner-defaults:end -->"; } >> "$f"
for s in "$src"/claude/skills/*/; do
  n="$(basename "$s")"; rm -rf "$dest/skills/$n"; cp -r "$s" "$dest/skills/$n"
done
echo "project standard $(cat "$src/VERSION") installed: $(ls "$src/claude/skills" | tr '\n' ' ')"
