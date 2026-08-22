---
role: task
provides:
  - task.read
  - task.create
  - task.update
  - task.assign
---

# Connection: Asana

Fills the **task** role. This is a documentation stub: it describes how Asana is
used and what it can provide when connected. Whether it's actually wired up is
your runtime state — record that in `workspace/connections.md` (status
`documented` / `connected` / `verified`), not here.

## What the assistant may read

Tasks, owners, due dates, sections, and project/board structure. Only the boards a job needs — not the whole workspace.

## What the assistant may write

Create and update tasks, set owners and dates — always with a yes. Never change an owner or bulk-change more than 10 tasks without an explicit instruction.

## Fields that matter

Map Asana fields to the task-row schema: task name, assignee (owner), due date, and a custom field or section for status. Keep `external_id` and `external_url` so the workspace can link back.

## Exercised end-to-end

The maintainer exercised this connection end-to-end on 2026-08-24 against a live
Asana workspace, through an assistant-side MCP connection: a scoped `task.read`,
a gated `task.create` (read back by external ID), a gated `task.update` (read
back), and cleanup — with the workspace's internal `tasks.md` frozen and
untouched throughout, and the doctor accepting the external switch. Your own
setup still starts as `documented` in `workspace/connections.md` until *your*
assistant's connection is wired up and you have tested a read and a write.

## Quirks worth knowing

Custom fields and section names vary per workspace, so confirm them once and record the mapping here. A write can silently land on the wrong task after a bulk reorder — read the task back after writing.

## Approval

Reading is scoped to what a job needs. Any write to Asana lands on other people's
screens, so it always needs a yes — see [../rules/what-needs-my-approval.md](../rules/what-needs-my-approval.md).
