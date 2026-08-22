---
role: task
provides:
  - task.read
  - task.create
  - task.update
  - task.assign
---

# Connection: Jira

Fills the **task** role. This is a documentation stub: it describes how Jira is
used and what it can provide when connected. Whether it's actually wired up is
your runtime state — record that in `workspace/connections.md` (status
`documented` / `connected` / `verified`), not here.

## What the assistant may read

Issues, assignees, due dates, statuses, and the project/board they live on. Only the project a job needs.

## What the assistant may write

Create and update issues and transitions — always with a yes.

## Fields that matter

Map Jira fields to the task-row schema: summary (task), assignee (owner), due date, status. Jira statuses are workflow-specific — record which map to the six task-row statuses. Keep the issue key and URL.

## Quirks worth knowing

Transitions are constrained by the workflow, so a status you want may not be reachable in one step. Confirm the workflow once. Read the issue back after any transition.

## Approval

Reading is scoped to what a job needs. Any write to Jira lands on other people's
screens, so it always needs a yes — see [../rules/what-needs-my-approval.md](../rules/what-needs-my-approval.md).
