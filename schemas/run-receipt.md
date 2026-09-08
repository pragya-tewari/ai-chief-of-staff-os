# Schema: run receipt

Every non-dry run has one durable receipt at
`workspace/log/runs/<run-key>.md`. It is a checkpoint, not merely an end summary:
create it after the user has seen the write plan and before the first real write,
then update it after every action.

A dry-run writes nothing, including no receipt.

## Run key

Combine the job name with its manifest's concrete `dedup-key` value and normalize
the result to a filesystem-safe slug:

```
meeting-to-tasks--transcript-3-vendor-escalation
write-an-update--founder--2026-w34
```

The same logical source, recipient-purpose, event, scope or reporting period uses
the same key. A repeated run reads this receipt and reconciles the destinations
before acting.

Normalize deterministically:

1. Normalize each component separately: for a file, start from its name without
   the extension (`transcript-3-vendor-escalation.txt` contributes
   `transcript-3-vendor-escalation`); then lowercase it, trim it, replace every
   run of characters outside `a-z`, `0-9` with one hyphen, collapse repeated
   hyphens, and strip leading/trailing hyphens.
2. Use ISO dates (`2026-08-24`) and lowercase ISO weeks (`2026-w34`).
3. Join non-empty components with `--`, prefixed by the normalized job name and
   another `--`. Never derive a component from mutable draft/output wording.
4. If the source has no stable ID, assign a request ID once, show it in the plan,
   and preserve it in `source-or-scope` and the receipt filename. On a later run,
   search existing receipts/destinations before assigning another ID.

Action keys follow the same lowercase slug rule and describe the durable target
(`task-t20`, `founder-email`), not execution order (`action-1`). They must remain
stable when the plan is resumed.

An explicit repeat of an already-succeeded external action gets a new run key by
appending `--attempt-2` (then 3, and so on). The new receipt links the earlier run
in `source-or-scope`; changing the attempt number must never happen implicitly.

## Receipt format

```
---
run-key: write-an-update--founder--2026-w34
job: write-an-update
status: in-progress
started: 2026-08-24T09:30:00+05:30
updated: 2026-08-24T09:34:00+05:30
source-or-scope: founder update for 2026-w34
---

# Run receipt

## Context

- Read: projects/, tasks, questions, decisions, goals, now.md
- Assumptions: none

## Actions

| action-key | destination | approval | state | external ID / verification |
|---|---|---|---|---|
| report | reports/founder-update-2026-w34.md | free | succeeded | read back 09:31 |
| founder-email | mail: founder@example.com | yes | in-progress | verification required |
| shared-doc | docs: founder update | yes | planned | — |
| activity-log | log/activity.md | free | planned | — |
| runs-index | log/runs/README.md | free | planned | — |

## Unresolved

- Verify whether `founder-email` landed before any retry.
```

## Run status

| Status | Meaning |
|---|---|
| `planned` | Receipt exists; no action has started |
| `in-progress` | At least one action is planned, running, failed or uncertain |
| `needs-verification` | An external action may have landed; do not retry until checked |
| `blocked` | The run cannot continue without the user or missing context |
| `complete` | Every action is succeeded or deliberately skipped; none is uncertain |

## Action state

| State | Rerun behaviour |
|---|---|
| `planned` | May run after its approval gate |
| `in-progress` | Local: inspect the destination. External: treat as uncertain and verify before retry |
| `succeeded` | Never repeat automatically |
| `failed` | Diagnose, then retry only this action when safe |
| `uncertain` | Verify in the destination tool or ask the user; never blindly repeat |
| `skipped` | Do not run unless the user changes the plan |

Before an external action, write its state as `in-progress`. After it succeeds,
record the external ID or URL when the tool provides one and read the result back.
If the session ends between those two steps, the next run changes the action to
`uncertain`/`needs-verification` and checks the tool before doing anything else.

Treat the activity-log and receipt-index updates as ordinary checkpointed local
actions. The receipt file itself is the checkpoint container, so it does not list
its own writes as a recursive action.

## What this model guarantees—and does not

For one user running one assistant session at a time, stable keys, deterministic
destinations and per-action checkpoints substantially reduce duplicate files,
register rows, tasks and sends. They also make an interrupted run recoverable.

This is not a database transaction, a lock or an exactly-once delivery system.
The project does not support concurrent runs. When an external tool cannot prove
whether an action landed, the safe result is to stop and ask—not to guess or
repeat it.

The concrete recovery cases in [run-receipt-test.md](run-receipt-test.md) are the
acceptance test for implementations of this schema.
