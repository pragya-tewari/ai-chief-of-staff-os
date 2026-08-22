---
role: task
provides:
  - task.read
  - task.create
  - task.update
  - task.assign
---

# Connection: the built-in task list

The one connection the system fills itself. When you have no external task tool —
or don't want to use one — your tasks live in a plain Markdown table in your
workspace, and every job treats it exactly as it would treat Asana or Linear. It
is `verified` by definition because the system supplies it; the installer records
that status in `workspace/connections.md`.

## Where it lives

- `workspace/tasks.md` — the live list.
- `workspace/tasks-done.md` — closed and cancelled tasks.
- `workspace/task-source.md` — the switch that says which task system is live.

## The row format

Defined in [../schemas/task-row.md](../schemas/task-row.md): `id`, `task`, `type`,
`owner`, `project`, `due`, `status`, `waiting on`, `from` — nine fields, the same
shape every external tool uses, so you can export to one later without a rebuild.

## What each job does with it

- **Writes rows:** `meeting-to-tasks`, `intake-a-request`.
- **Reads and filters:** `run-a-sweep`, `write-an-update`, `prepare-a-meeting`.
- **A per-person or per-project view** ("what does Ravi owe me") is a filter of
  this table written to `workspace/reports/`. Never stored on the person file.

## Approval

Writing a row into your own `tasks.md` is free — it's your own record. **Telling a
person about their task** (in chat or email) always needs a yes, exactly as it
would with an external tool. Recording is not telling.

## Switching to an external tool later

1. Mark `tasks.md` inactive with a dated header.
2. Export the open rows to the new tool.
3. Update `task-source.md` and `workspace/connections.md`.
4. Log the switch.

Nothing is deleted and nothing is synced. The old list becomes frozen history.

## Honest limits

Nobody else can update their own tasks here, nothing notifies anyone, and there is
no phone app. This is your record of what you're owed and what you promised — not
a shared team board. If your team needs a shared board, connect a real tool and
let this step aside.
