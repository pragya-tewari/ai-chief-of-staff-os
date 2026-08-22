#!/usr/bin/env bash
# Mechanical repository and history checks. No AI job is executed here; prose
# job tests remain human acceptance scenarios.
set -uo pipefail
cd "$(dirname "$0")/.."

FAIL=0
section(){ echo; echo "== $1 =="; }
fail(){ echo "  FAIL $1"; FAIL=1; }
ok(){ echo "  ok   $1"; }

section "structure, schemas, links, and sample consistency"
python3 scripts/validate.py || FAIL=1

section "shell script syntax"
if bash -n setup/install.sh setup/doctor.sh setup/demo.sh scripts/check.sh; then
  ok "shell scripts parse"
else
  fail "shell syntax error"
fi

section "no symlinks in the public tree"
SYMLINKS="$(find . \( -path './.git' -o -path './workspace' \) -prune -o -type l -print)"
if [[ -n "$SYMLINKS" ]]; then
  printf '%s\n' "$SYMLINKS" | sed 's/^/  FAIL /'
  fail "symlink present"
else
  ok "no symlinks"
fi

scan_tree() {
  grep -rniE "$1" \
    --exclude-dir=.git \
    --exclude-dir=workspace \
    --exclude='cos-os.yaml' \
    --exclude='check.sh' \
    --exclude='validate.py' \
    --include='*.md' --include='*.txt' --include='*.yaml' --include='*.yml' --include='*.sh' \
    . 2>/dev/null | grep -vE '^\./scripts/(check\.sh|validate\.py):' || true
}

tree_files() {
  cut -d: -f1 | sort -u
}

section "credential-shaped values"
CREDENTIALS="$(scan_tree '(AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----|(api[_-]?key|access[_-]?token|secret|password)[\"'"'"' ]*[:=][\"'"'"' ]*[A-Za-z0-9/+_-]{16,})' | tree_files)"
if [[ -n "$CREDENTIALS" ]]; then
  printf '%s\n' "$CREDENTIALS" | sed 's/^/  /'
  fail "possible credential in current tree"
else
  ok "no obvious credential-shaped values"
fi

section "email, phone, workspace-ID, and forbidden-term patterns"
EMAILS="$(scan_tree '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}' | grep -viE '(you@|example\.com|\.invalid)' | tree_files || true)"
PHONES="$(scan_tree '(^|[^0-9])\+?[0-9][0-9 ()-]{8,}[0-9]([^0-9]|$)' | grep -vE '[0-9]{4}-[0-9]{2}-[0-9]{2}' | tree_files || true)"
WORKSPACE_IDS="$(scan_tree '(^|[^0-9])[0-9]{16,}([^0-9]|$)' | tree_files)"
FORBIDDEN="$(scan_tree '(prj-tfr|future-?ready|gennext|university[ -]?profile)' | tree_files)"
[[ -z "$EMAILS" ]] || { printf '%s\n' "$EMAILS" | sed 's/^/  /'; fail "non-example email address present"; }
[[ -z "$PHONES" ]] || { printf '%s\n' "$PHONES" | sed 's/^/  /'; fail "phone-number pattern present"; }
[[ -z "$WORKSPACE_IDS" ]] || { printf '%s\n' "$WORKSPACE_IDS" | sed 's/^/  /'; fail "long workspace-ID pattern present"; }
[[ -z "$FORBIDDEN" ]] || { printf '%s\n' "$FORBIDDEN" | sed 's/^/  /'; fail "forbidden internal term present"; }
[[ -n "$EMAILS$PHONES$WORKSPACE_IDS$FORBIDDEN" ]] || ok "no blocked public-data patterns"

section "git history contains no blocked terms"
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  HISTORY_BAD=""
  while IFS= read -r commit; do
    blocked="$(git grep -I -l -i -E '(prj-tfr|future-?ready|gennext|university[ -]?profile|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----|(api[_-]?key|access[_-]?token|secret|password)["'"'"' ]*[:=]["'"'"' ]*[A-Za-z0-9/+_-]{16,})' "$commit" -- '*.md' '*.txt' '*.yaml' '*.yml' '*.sh' ':(exclude)scripts/check.sh' ':(exclude)scripts/validate.py' 2>/dev/null || true)"
    emails="$(git grep -I -n -i -E '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}' "$commit" -- '*.md' '*.txt' '*.yaml' '*.yml' '*.sh' ':(exclude)scripts/check.sh' ':(exclude)scripts/validate.py' 2>/dev/null | grep -viE '(you@|example\.com|\.invalid)' | cut -d: -f1-2 | sort -u || true)"
    phones="$(git grep -I -n -E '(^|[^0-9])\+?[0-9][0-9 ()-]{8,}[0-9]([^0-9]|$)' "$commit" -- '*.md' '*.txt' '*.yaml' '*.yml' 2>/dev/null | grep -vE '[0-9]{4}-[0-9]{2}-[0-9]{2}' | cut -d: -f1-2 | sort -u || true)"
    workspace_ids="$(git grep -I -l -E '(^|[^0-9])[0-9]{16,}([^0-9]|$)' "$commit" -- '*.md' '*.txt' '*.yaml' '*.yml' 2>/dev/null || true)"
    matches="${blocked}${emails}${phones}${workspace_ids}"
    if [[ -n "$matches" ]]; then
      HISTORY_BAD="${HISTORY_BAD}${matches}"$'\n'
    fi
  done < <(git rev-list --all)
  if [[ -n "$HISTORY_BAD" ]]; then
    printf '%s' "$HISTORY_BAD" | sed 's/^/  /'
    fail "blocked term or credential exists in git history"
  else
    ok "all reachable commits are clean"
  fi
else
  fail "repository is not under git; history cannot be checked"
fi

echo
if [[ "$FAIL" -eq 0 ]]; then
  echo "ALL CHECKS PASSED"
else
  echo "CHECKS FAILED"
fi
exit "$FAIL"
