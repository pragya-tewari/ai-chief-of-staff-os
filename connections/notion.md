---
role: docs
provides:
  - doc.read
  - doc.create
---

# Connection: Notion

Fills the **docs** role. This is a documentation stub: it describes how Notion is
used and what it can provide when connected. Whether it's actually wired up is
your runtime state — record that in `workspace/connections.md` (status
`documented` / `connected` / `verified`), not here.

## What the assistant may read

Pages and databases the job needs — a doc, a wiki page, a tracker. Not the whole workspace.

## What the assistant may write

Draft or update a page — always with a yes. Never publish or share a page without an explicit instruction.

## Fields that matter

Notion databases have arbitrary properties; confirm the ones a job reads or writes and record the mapping. Keep the page URL for linking back.

## Quirks worth knowing

A Notion database can double as a task tool. If you use it that way, treat it as the task role, map its properties to the task-row schema (and declare `task.*` capabilities), and remember the one-live-source rule.

## Approval

Reading is scoped to what a job needs. Any write to Notion lands on other people's
screens, so it always needs a yes — see [../rules/what-needs-my-approval.md](../rules/what-needs-my-approval.md).
