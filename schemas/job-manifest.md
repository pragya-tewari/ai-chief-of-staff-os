# Schema: job manifest

Every job folder has a `manifest.md` — a short frontmatter block that lets a run
be checked and lets the assistant refuse an action a connection can't actually
do. It is the machine-checkable summary of what the prose files say.

```
---
job: meeting-to-tasks
spec-version: "0.1"
reads:
  - registers/meetings.md
  - people/
  - projects/
  - task-source
writes-internal:
  - meetings/
  - registers/
  - tasks
  - projects/
  - log/activity.md
  - log/runs/
external-capabilities:
  - task.create        # only used when an external task tool is the live source
approval-actions:
  - external-write
  - tell-a-person
  - decision-record
  - private-write
dedup-key: meeting-source-id
supports-dry-run: true
---
```

## The fields

| Field | What it is |
|---|---|
| `job` | The job's folder name |
| `spec-version` | Which format version it targets |
| `reads` | What it reads — so a reviewer can see its footprint |
| `writes-internal` | Every workspace destination it writes without asking, including the runtime's `log/activity.md` and `log/runs/` checkpoints |
| `external-capabilities` | Every external capability the job may use, from [capabilities.md](capabilities.md). Check only the capability for the particular external read/write in the plan; unavailable optional actions do not block local work |
| `approval-actions` | The kinds of action in this job that need a yes |
| `dedup-key` | The concrete source/scope identity used with the job name to form a stable run key. `none` is not valid; every job must define how it recognises the same logical run |
| `supports-dry-run` | Always `true` — every job can show its plan and write nothing |

## Why it exists

Prose tells a human how the job works. The manifest lets the assistant check,
before each external action, whether the selected live connection can do that
specific action. If `task.create` is unavailable, an external task creation
stops and is reported; local analysis, drafts, and the verified built-in task
list remain available. A job is never blocked merely because a different,
unused destination such as mail is not connected.

## Run-key rule

Normalize the `dedup-key` value into a filesystem-safe slug and prefix it with
the job name. For example, `meeting-to-tasks` plus source
`transcript-3-vendor-escalation` becomes
`meeting-to-tasks--transcript-3-vendor-escalation`. A periodic job uses its
declared scope and period; a second run for that same scope updates/reconciles the
existing output. Deliberately sending or creating something again requires an
explicit instruction and a new `--attempt-N` run key linked to the earlier
receipt. The canonical component/action normalization rules live in
[run-receipt.md](run-receipt.md).
