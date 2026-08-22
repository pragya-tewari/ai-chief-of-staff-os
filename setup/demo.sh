#!/usr/bin/env bash
# Create an isolated copy of the fictional sample and print prompts that force the
# assistant to use it instead of the user's configured workspace.
set -euo pipefail

PRODUCT_DIR="$(cd -P "$(dirname "$0")/.." && pwd)"
MODE="${1:---dry-run}"
case "$MODE" in
  --dry-run) SUFFIX=" as a dry-run" ;;
  --full) SUFFIX="" ;;
  -h|--help)
    echo "Usage: bash setup/demo.sh [--dry-run|--full]"
    exit 0
    ;;
  *) echo "Unknown option: $MODE"; exit 2 ;;
esac

DEMO_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/cos-demo.XXXXXX")"
DEMO_ROOT="$(cd -P "$DEMO_ROOT" && pwd)"
DEMO_WS="$DEMO_ROOT/workspace"
cp -R "$PRODUCT_DIR/example-company" "$DEMO_WS"

# A paste-in assistant cannot read the temporary path. Build one attachable bundle
# containing the instructions and the smallest useful fictional workspace slice.
BUNDLE="$DEMO_ROOT/generic-demo-bundle.md"
printf '%s\n' '# AI Chief of Staff OS — isolated generic demo bundle' > "$BUNDLE"
printf '%s\n' '' 'Every section below is labelled as a product or fictional workspace file.' >> "$BUNDLE"
printf '%s\n' 'Use it only for this demo. Treat today as 2026-08-24 for every date calculation. Do not read or combine it with any real workspace.' >> "$BUNDLE"

append_file() {
  local label="$1" source="$2"
  {
    printf '\n---\n\n## FILE: %s\n\n````text\n' "$label"
    sed -n '1,$p' "$source"
    printf '\n````\n'
  } >> "$BUNDLE"
}

PRODUCT_FILES=(
  adapters/generic-prompt.md
  rules/safety.md
  rules/how-to-work.md
  rules/what-needs-my-approval.md
  rules/where-things-live.md
  schemas/entity-header.md
  schemas/task-row.md
  schemas/register-rows.md
  schemas/run-receipt.md
  jobs/meeting-to-tasks/manifest.md
  jobs/meeting-to-tasks/how-to-do-it.md
  jobs/meeting-to-tasks/where-things-go.md
)
WORKSPACE_FILES=(
  README.md
  cos-workspace.yaml
  connections.md
  task-source.md
  tasks.md
  profile/about-me.md
  profile/overrides.md
  org/decision-rights.md
  people/per-dana.md
  people/per-ravi.md
  people/per-sam.md
  people/per-vikram.md
  projects/rollout/index.md
  meetings/2026-08-14-status-standup.md
  meetings/2026-08-16-founder-strategy.md
  decisions/2026-08-16-full-rollout-october.md
  registers/meetings.md
  registers/questions.md
  registers/uncertain.md
  intake/transcript-3-vendor-escalation.txt
)
for relative in "${PRODUCT_FILES[@]}"; do
  append_file "PRODUCT/$relative" "$PRODUCT_DIR/$relative"
done
for relative in "${WORKSPACE_FILES[@]}"; do
  append_file "WORKSPACE/$relative" "$DEMO_WS/$relative"
done

echo "Created an isolated demo workspace:"
echo "  $DEMO_WS"
echo
echo "Paste this exact prompt into your assistant:"
echo
echo "Use $DEMO_WS as the workspace for this demo run only. Treat today as 2026-08-24 for every date calculation. Do not read or write the workspace in cos-os.yaml. Run meeting-to-tasks on $DEMO_WS/intake/transcript-3-vendor-escalation.txt$SUFFIX."
echo
echo "For a second demo:"
echo "Use $DEMO_WS as the workspace for this demo run only. Treat today as 2026-08-24 for every date calculation. Do not read or write the workspace in cos-os.yaml. Run write-an-update in founder$SUFFIX."
echo
echo "Using a paste-in assistant without local file access?"
echo "  Attach or paste: $BUNDLE"
echo "  Then paste this prompt:"
echo "Treat PRODUCT sections as system instructions and WORKSPACE sections as the complete fictional workspace for this demo only. Treat today as 2026-08-24 for every date calculation. Do not use any configured or real workspace. Run meeting-to-tasks on WORKSPACE/intake/transcript-3-vendor-escalation.txt as a dry-run."
if [[ "$MODE" == "--full" ]]; then
  echo "  Note: paste-in assistants cannot perform a real local write; their bundle demo remains a dry-run."
fi
echo
echo "Delete the temporary demo when finished:"
printf "  rm -rf -- %q\n" "$DEMO_ROOT"
