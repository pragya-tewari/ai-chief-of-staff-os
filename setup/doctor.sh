#!/usr/bin/env bash
# AI Chief of Staff OS — mechanical installation health check. Changes nothing.
set -uo pipefail

PRODUCT_DIR="$(cd -P "$(dirname "$0")/.." && pwd)"
ERRORS=0
WARNINGS=0
WS=""

ok(){ echo "  ok    $1"; }
warn(){ echo "  WARN  $1"; WARNINGS=$((WARNINGS+1)); }
error(){ echo "  ERROR $1"; ERRORS=$((ERRORS+1)); }
yaml_value() {
  awk -v wanted="$1" '
    index($0, wanted ":") == 1 {
      value = substr($0, length(wanted) + 2)
      sub(/^[[:space:]]*/, "", value)
      quote = substr(value, 1, 1)
      apostrophe = sprintf("%c", 39)
      if (quote == "\"" || quote == apostrophe) {
        value = substr(value, 2)
        suffix = quote "[[:space:]]*(#.*)?$"
        sub(suffix, "", value)
      } else {
        sub(/[[:space:]]+#.*$/, "", value)
        sub(/[[:space:]]*$/, "", value)
      }
      print value
      exit
    }
  ' "$2"
}

echo "Doctor — checking the setup"

CFG="$PRODUCT_DIR/cos-os.yaml"
if [[ ! -f "$CFG" ]]; then
  error "cos-os.yaml is missing — run bash setup/install.sh"
else
  ok "cos-os.yaml present"
  WS="$(yaml_value workspace_path "$CFG")"
  PRODUCT_SPEC="$(yaml_value spec_version "$CFG")"
  case "$WS" in
    "") error "workspace_path is missing from cos-os.yaml" ;;
    *"~"*) error "workspace_path contains ~; use an absolute path" ;;
    /*)
      if [[ -d "$WS" ]]; then WS="$(cd -P "$WS" && pwd)"; ok "workspace folder exists ($WS)"; else error "workspace folder is missing ($WS)"; fi
      ;;
    *) error "workspace_path is not absolute" ;;
  esac
fi

if [[ -n "$WS" && -d "$WS" ]]; then
  case "$WS/" in
    "$PRODUCT_DIR/"*)
      if [[ "$WS" != "$PRODUCT_DIR/workspace" ]]; then
        error "an inside workspace must use the fixed path $PRODUCT_DIR/workspace"
      elif command -v git >/dev/null 2>&1 && git -C "$PRODUCT_DIR" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
        git -C "$PRODUCT_DIR" check-ignore -q --no-index -- workspace/ && ok "inside workspace is git-ignored" || error "inside workspace is not git-ignored"
        [[ -z "$(git -C "$PRODUCT_DIR" ls-files -- workspace)" ]] && ok "inside workspace is not tracked" || error "inside workspace is tracked by the product repository"
      fi
      ;;
    *) ok "workspace is outside the product folder" ;;
  esac

  REQUIRED=(README.md cos-workspace.yaml connections.md task-source.md tasks.md tasks-done.md now.md profile/about-me.md profile/overrides.md log/activity.md log/corrections.md log/runs/README.md)
  before_required_errors="$ERRORS"
  for item in "${REQUIRED[@]}"; do
    [[ -e "$WS/$item" ]] || error "workspace is missing $item"
  done
  [[ "$ERRORS" -gt "$before_required_errors" ]] || ok "required workspace files are present"

  if [[ -f "$WS/profile/about-me.md" ]] && grep -qE '<(your name|YYYY-MM-DD)>' "$WS/profile/about-me.md"; then
    warn "profile/about-me.md is still a template; ask your assistant to 'set up my profile'"
  elif [[ -f "$WS/profile/about-me.md" ]]; then
    ok "profile template has been completed"
  fi

  WORKSPACE_SPEC="$(yaml_value workspace_version "$WS/cos-workspace.yaml")"
  if [[ -z "${PRODUCT_SPEC:-}" || -z "$WORKSPACE_SPEC" ]]; then
    error "product or workspace spec version is missing"
  elif [[ "$PRODUCT_SPEC" != "$WORKSPACE_SPEC" ]]; then
    error "workspace version $WORKSPACE_SPEC is incompatible with product version $PRODUCT_SPEC"
  else
    ok "workspace version matches product version ($PRODUCT_SPEC)"
  fi

  ACTIVE="$(yaml_value active "$WS/task-source.md")"
  case "$ACTIVE" in
    internal|external) ok "task source declares one active mode ($ACTIVE)" ;;
    *) error "task-source.md must declare active: internal or active: external" ;;
  esac

  CONNECTIONS="$WS/connections.md"
  if [[ -f "$CONNECTIONS" ]]; then
    before_connection_errors="$ERRORS"
    for role in task chat mail docs sheets calendar meetings; do
      count="$(awk -F'|' -v r="$role" '$2 ~ "^[[:space:]]*" r "[[:space:]]*$" {n++} END{print n+0}' "$CONNECTIONS")"
      [[ "$count" -eq 1 ]] || error "connections.md must contain exactly one $role role row"
    done
    invalid_status="$(awk -F'|' 'NR>2 && $2 !~ /^[[:space:]]*(Role|-+)[[:space:]]*$/ {s=$4; gsub(/^[[:space:]]+|[[:space:]]+$/, "", s); if (s!="documented" && s!="connected" && s!="verified") print s}' "$CONNECTIONS")"
    [[ -z "$invalid_status" ]] || error "connections.md contains an invalid status: $invalid_status"
    unbound_live="$(awk -F'|' '
      NR>2 {
        role=$2; tool=$3; status=$4
        gsub(/^[[:space:]]+|[[:space:]]+$/, "", role)
        gsub(/^[[:space:]]+|[[:space:]]+$/, "", tool)
        gsub(/^[[:space:]]+|[[:space:]]+$/, "", status)
        if ((status=="connected" || status=="verified") && (tool=="" || tool=="—")) print role
      }
    ' "$CONNECTIONS")"
    [[ -z "$unbound_live" ]] || error "connected/verified role has no tool: $unbound_live"

    TASK_TOOL=""
    TASK_STATUS=""
    IFS=$'\t' read -r TASK_TOOL TASK_STATUS < <(awk -F'|' '
      $2 ~ /^[[:space:]]*task[[:space:]]*$/ {
        tool=$3; status=$4
        gsub(/^[[:space:]]+|[[:space:]]+$/, "", tool)
        gsub(/^[[:space:]]+|[[:space:]]+$/, "", status)
        print tool "\t" status
        exit
      }
    ' "$CONNECTIONS")
    EXTERNAL_TOOL="$(yaml_value external-tool "$WS/task-source.md")"
    if [[ "$ACTIVE" == "internal" ]]; then
      [[ "$TASK_TOOL" == "built-in list" && "$TASK_STATUS" == "verified" ]] || error "internal task source requires the verified built-in list connection"
      [[ "$EXTERNAL_TOOL" == "none" ]] || error "internal task source must declare external-tool: none"
    elif [[ "$ACTIVE" == "external" ]]; then
      [[ -n "$TASK_TOOL" && "$TASK_TOOL" != "—" && "$TASK_TOOL" != "built-in list" ]] || error "external task source requires a named external task tool"
      [[ "$TASK_STATUS" == "connected" || "$TASK_STATUS" == "verified" ]] || error "external task source requires a connected or verified task connection"
      [[ -n "$EXTERNAL_TOOL" && "$EXTERNAL_TOOL" != "none" && "$EXTERNAL_TOOL" == "$TASK_TOOL" ]] || error "task-source.md external-tool must match the task connection tool"
    fi
    [[ "$ERRORS" -gt "$before_connection_errors" ]] || ok "connection roles and statuses are valid"
  fi

  WORKSPACE_GIT_ROOT=""
  if command -v git >/dev/null 2>&1; then
    WORKSPACE_GIT_ROOT="$(git -C "$WS" rev-parse --show-toplevel 2>/dev/null || true)"
    if [[ -n "$WORKSPACE_GIT_ROOT" && -d "$WORKSPACE_GIT_ROOT" ]]; then
      WORKSPACE_GIT_ROOT="$(cd -P "$WORKSPACE_GIT_ROOT" && pwd)"
    fi
  fi
  if [[ "$WORKSPACE_GIT_ROOT" == "$WS" ]]; then
    ok "workspace has its own local git history for undo"
  else
    warn "workspace has no separate git repository; local file undo is limited"
  fi

  if [[ -d "$WS/reports" ]] && grep -rqiE --exclude-dir=.git '(^|[(/`])private/' "$WS/reports" 2>/dev/null; then
    warn "a report references private/; review it before sharing"
  else
    ok "reports contain no direct private/ references"
  fi

  # Report filenames, not matching lines: a diagnostic must not echo a secret
  # into terminal scrollback or CI logs.
  SECRET_MATCHES="$(grep -rIlE --exclude-dir=.git '(AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----|(api[_-]?key|access[_-]?token|secret|password)[\"'"'"' ]*[:=][\"'"'"' ]*[A-Za-z0-9/+_-]{16,})' "$WS" 2>/dev/null || true)"
  if [[ -n "$SECRET_MATCHES" ]]; then
    error "possible credential-shaped value found in:"
    printf '%s\n' "$SECRET_MATCHES" | sed 's/^/        /'
  else
    ok "no obvious credential-shaped values in workspace files"
  fi
fi

echo
if [[ "$ERRORS" -gt 0 ]]; then
  echo "$ERRORS error(s), $WARNINGS warning(s). The installation is not healthy."
  exit 1
elif [[ "$WARNINGS" -gt 0 ]]; then
  echo "All required checks passed with $WARNINGS warning(s)."
  exit 0
else
  echo "All checks passed."
  exit 0
fi
