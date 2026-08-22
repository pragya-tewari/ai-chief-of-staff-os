#!/usr/bin/env bash
# AI Chief of Staff OS — installer.
# Creates a private workspace, writes local config, optionally initializes a
# workspace git repository, and verifies the installation with the doctor.
set -euo pipefail

PRODUCT_DIR="$(cd -P "$(dirname "$0")/.." && pwd)"
DEFAULT_OUTSIDE_WS="$HOME/chief-of-staff-workspace"
INSIDE=false

usage() {
  echo "Usage: bash setup/install.sh [--inside]"
  echo "  --inside  use the fixed, git-ignored path <product>/workspace"
}

case "${1:-}" in
  "") ;;
  --inside) INSIDE=true ;;
  -h|--help) usage; exit 0 ;;
  *) echo "Unknown option: $1"; usage; exit 2 ;;
esac
[[ $# -le 1 ]] || { usage; exit 2; }

echo "AI Chief of Staff OS — install"
echo "Product folder: $PRODUCT_DIR"
echo

# Collapse every "." and ".." component of an absolute path as pure text, so a
# path like /a/missing/../../b cannot dodge the boundary check via components
# that do not exist yet. Nothing is created here.
lexical_normalize() {
  local input="$1" part out=""
  local IFS=/
  for part in $input; do
    case "$part" in
      ""|".") ;;
      "..") out="${out%/*}" ;;
      *) out="$out/$part" ;;
    esac
  done
  printf '%s\n' "${out:-/}"
}

# Resolve a path whose target may not exist yet, without creating anything:
# first collapse "." and ".." lexically, then walk up to the deepest existing
# ancestor, canonicalize it (resolving symlinks), and re-append the remainder.
# Nothing is written until the privacy boundary has been checked.
resolve_new_path() {
  local raw="$1" existing remainder=""
  case "$raw" in
    "~") raw="$HOME" ;;
    "~/"*) raw="$HOME/${raw#~/}" ;;
    "~"*) echo "Paths such as ~other-user are not supported; use an absolute path." >&2; return 1 ;;
  esac
  case "$raw" in
    /*) ;;
    *) raw="$(pwd -P)/$raw" ;;
  esac
  raw="$(lexical_normalize "$raw")"
  existing="$raw"
  while [[ ! -d "$existing" && "$existing" != "/" ]]; do
    remainder="$(basename "$existing")${remainder:+/$remainder}"
    existing="$(dirname "$existing")"
  done
  existing="$(cd -P "$existing" && pwd)"
  if [[ -n "$remainder" ]]; then
    printf '%s/%s\n' "${existing%/}" "$remainder"
  else
    printf '%s\n' "$existing"
  fi
}

if [[ "$INSIDE" == true ]]; then
  WS="$PRODUCT_DIR/workspace"
  echo "Inside mode selected: $WS"
else
  read -r -p "Where should your private workspace live? [$DEFAULT_OUTSIDE_WS] " WS_INPUT
  WS_INPUT="${WS_INPUT:-$DEFAULT_OUTSIDE_WS}"
  WS="$(resolve_new_path "$WS_INPUT")"
fi

case "$WS/" in
  "$PRODUCT_DIR/"*) IS_INSIDE=true ;;
  *) IS_INSIDE=false ;;
esac

if [[ "$INSIDE" == false && "$IS_INSIDE" == true ]]; then
  echo "Refusing to create the workspace inside the product folder."
  echo "Choose a sibling path, or use --inside for the fixed product/workspace path."
  exit 1
fi

if [[ "$INSIDE" == true && "$WS" != "$PRODUCT_DIR/workspace" ]]; then
  echo "Inside mode is restricted to $PRODUCT_DIR/workspace."
  exit 1
fi

if [[ "$INSIDE" == true ]] && command -v git >/dev/null 2>&1 && git -C "$PRODUCT_DIR" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  if ! git -C "$PRODUCT_DIR" check-ignore -q --no-index -- workspace/; then
    echo "Refusing inside install: product/workspace is not ignored by git."
    exit 1
  fi
fi

# Every answer is collected and validated BEFORE anything is created, so a
# failed input never leaves a half-built workspace behind.

# The workspace path cannot contain a newline, quote or backslash because it is
# written as a double-quoted YAML scalar. These are unusual path characters.
[[ "$WS" != *$'\n'* && "$WS" != *'"'* && "$WS" != *'\\'* ]] || { echo "Workspace path cannot contain a quote, backslash or newline."; exit 1; }

# Refuse to overwrite an existing, non-empty workspace.
if [[ -e "$WS" && -n "$(ls -A "$WS" 2>/dev/null)" ]]; then
  echo "A non-empty folder already exists at $WS — not overwriting it."
  echo "Move it aside or choose another path, then re-run."
  exit 1
fi

# Select the adapter and timezone (validated before any file is written).
read -r -p "Which assistant do you use? [claude/agents/generic] (claude) " ASSISTANT
ASSISTANT="${ASSISTANT:-claude}"
case "$ASSISTANT" in
  claude|agents|generic) ;;
  *) echo "Assistant must be claude, agents, or generic. Nothing was created; re-run to try again."; exit 1 ;;
esac
TZDEFAULT="$( (readlink /etc/localtime 2>/dev/null | sed 's#.*/zoneinfo/##') || true )"
TZDEFAULT="${TZDEFAULT:-UTC}"
read -r -p "Your timezone? [$TZDEFAULT] " TZ
TZ="${TZ:-$TZDEFAULT}"
[[ -n "$TZ" && "$TZ" != *$'\n'* && "$TZ" != *'"'* && "$TZ" != *'\\'* ]] || { echo "Invalid timezone value. Nothing was created; re-run to try again."; exit 1; }
if [[ -d /usr/share/zoneinfo && ! -e "/usr/share/zoneinfo/$TZ" ]]; then
  echo "Note: '$TZ' is not in this system's zoneinfo — double-check the spelling (e.g. Asia/Kolkata)."
fi

# All inputs are valid. Now create the workspace.
mkdir -p "$WS"
cp -R "$PRODUCT_DIR/setup/workspace-template/." "$WS/"
cp "$PRODUCT_DIR/rules/about-me.template.md" "$WS/profile/about-me.md"
echo "Created workspace at $WS"

# Stamp the workspace-owned version file.
NOW="$(date +%Y-%m-%d)"
tmp="$(mktemp)"
sed "s/^created_at: .*/created_at: \"$NOW\"/" "$WS/cos-workspace.yaml" > "$tmp"
mv "$tmp" "$WS/cos-workspace.yaml"
tmp="$(mktemp)"
sed "s/^switched: .*/switched: \"$NOW\"/" "$WS/task-source.md" > "$tmp"
mv "$tmp" "$WS/task-source.md"
{
  printf 'spec_version: "0.1"\n'
  printf 'workspace_path: "%s"\n' "$WS"
  printf 'assistant: "%s"\n' "$ASSISTANT"
  printf 'timezone: "%s"\n' "$TZ"
  printf 'date_format: "YYYY-MM-DD"\n'
} > "$PRODUCT_DIR/cos-os.yaml"
echo "Wrote $PRODUCT_DIR/cos-os.yaml"

# A local commit gives undo. Backup requires the user to add and push a private
# remote; do not imply that `git init` alone is a backup.
read -r -p "Put the workspace under git for local undo? [Y/n] " GITYES
GITYES="${GITYES:-Y}"
if [[ "$GITYES" =~ ^[Yy] ]]; then
  if command -v git >/dev/null 2>&1; then
    (
      cd "$WS"
      git init -q
      git add -A
      git -c user.name="Chief of Staff OS" \
          -c user.email="local@chief-of-staff-os.invalid" \
          commit -q -m "Initial workspace"
    )
    echo "Workspace initialized as a git repo with a first local commit."
    echo "Add a private remote separately if you want an off-device backup."
  else
    echo "Git is not installed; continuing without workspace version control."
  fi
fi

echo
if ! bash "$PRODUCT_DIR/setup/doctor.sh"; then
  echo
  echo "Installation was created but did not pass verification. Fix the errors above before using real data."
  exit 1
fi

echo
if [[ "$ASSISTANT" == "generic" ]]; then
  echo "Done. Start each session by pasting adapters/generic-prompt.md into your assistant."
else
  echo "Done. Your assistant reads CLAUDE.md / AGENTS.md at $PRODUCT_DIR."
fi
echo "Run 'bash setup/demo.sh' for an isolated sample-company prompt."
echo "Then follow setup/first-week.md."
