---
role: task
provides:
  - task.read
  - task.create
  - task.update
  - task.assign
---

# Connection: Linear

Fills the **task** role. This is a documentation stub: it describes how Linear is
used and what it can provide when connected. Whether it's actually wired up is
your runtime state — record that in `workspace/connections.md` (status
`documented` / `connected` / `verified`), not here.

## What the assistant may read

Issues, assignees, due dates, states, projects and cycles. Only the team a job needs.

## What the assistant may write

Create and update issues, set assignees and states — always with a yes.

## Fields that matter

Map Linear fields to the task-row schema: title (task), assignee (owner), due date, state (status). Keep the issue identifier and URL for linking back.

## Quirks worth knowing

States are per-team and customisable, so confirm which map to todo/doing/blocked/done. Linear automation can move issues — read a state back after setting it.

## Approval

Reading is scoped to what a job needs. Any write to Linear lands on other people's
screens, so it always needs a yes — see [../rules/what-needs-my-approval.md](../rules/what-needs-my-approval.md).
