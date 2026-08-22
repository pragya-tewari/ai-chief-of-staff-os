---
role: chat
provides:
  - chat.read
  - chat.send
---

# Connection: Slack

Fills the **chat** role. This is a documentation stub: it describes how Slack is
used and what it can provide when connected. Whether it's actually wired up is
your runtime state — record that in `workspace/connections.md` (status
`documented` / `connected` / `verified`), not here.

## What the assistant may read

Messages in the specific channels or DMs a job needs, to gather context. Not a blanket read of the whole workspace.

## What the assistant may write

Post a message or reply — always with a yes. Never post to a broad channel without seeing the exact text approved first.

## Fields that matter

Channel IDs and names matter; confirm the right channel for a given kind of update and record it. Keep permalinks when a message needs to be referenced later.

## Quirks worth knowing

A message is public the moment it's posted and hard to unsend. Show the exact text and the exact channel in the plan before sending.

## Approval

Reading is scoped to what a job needs. Any write to Slack lands on other people's
screens, so it always needs a yes — see [../rules/what-needs-my-approval.md](../rules/what-needs-my-approval.md).
