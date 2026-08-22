# Connections

The rules and jobs never name a brand. They name a **role** — "the task tool",
"chat", "docs". This folder maps roles to the tools you actually use.

## The most important thing to understand

**A connection file is documentation, not a live integration.**

A Markdown file can describe a tool's fields, permissions and quirks. It cannot
provide the actual reading and writing — that comes from your assistant's own
connection to the tool (an MCP server, a plugin, a CLI).

So a connection file has two immutable, maintainer-owned parts:
- what role it fills;
- the capabilities it **provides** when connected, from the standard vocabulary in
  [../schemas/capabilities.md](../schemas/capabilities.md).

```
role: task            # or `roles:` as a list, for a tool that fills several
provides:
  - task.read
  - task.create
  - task.update
```

## Your live status lives in the workspace, not here

Whether a tool is actually wired up, and to which account, is *your* runtime
state — so it lives in your workspace at `workspace/connections.md`, not in these
tracked product files. That keeps the product checkout clean and keeps your
account details out of the repo. Your file records, per role: the tool, its status
(`documented` / `connected` / `verified`), and the account or scope. In the Tool
cell, name the connection file the tool maps to (`google`, `asana`, `built-in
list`) — never a free-form display name — so there is no guessing which guide
applies. A tool that fills several roles (Google, Zoho) appears on each of its
role rows with the same name.

A job's manifest lists every external capability it may use. Before each planned
external action, the assistant identifies that action's role, looks up the live
tool and status in `workspace/connections.md`, then checks the matching product
connection file's `provides` list. If the tool cannot perform that action, the
action stops and is reported; unrelated local work continues.

## The roles

See [roles.md](roles.md). In short: task, chat, mail, docs, sheets, calendar,
meetings.

## The task role is special

It is the one role the system can fill itself. [built-in-tasks.md](built-in-tasks.md)
provides the full set of task capabilities, verified, because the system supplies
it. That keeps every job's wording identical whichever source is live.

## One live task source, always

Whichever task tool you use, only one is live at a time. The other is marked
inactive in `workspace/task-source.md` and in a dated header on the unused file.
No syncing, no merging, no "check both". This is the one place a careless
assistant could corrupt your record, so it is stated everywhere it matters.

## Adding a tool

Copy an existing file, fill in the role, `provides` capabilities, fields and
quirks. That's also the easiest way to contribute — see
[../CONTRIBUTING.md](../CONTRIBUTING.md).
