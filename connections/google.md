---
roles:
  - docs
  - sheets
  - calendar
  - mail
provides:
  - doc.read
  - doc.create
  - sheet.read
  - sheet.write
  - calendar.read
  - mail.read
  - mail.send
---

# Connection: Google Workspace

Fills the **docs** role. This is a documentation stub: it describes how Google Workspace is
used and what it can provide when connected. Whether it's actually wired up is
your runtime state — record that in `workspace/connections.md` (status
`documented` / `connected` / `verified`), not here.

## What the assistant may read

Docs, Sheets, Calendar events and Gmail threads the job needs — scoped to the specific file, event or thread. Mail is read only with explicit scope (see safety.md).

## What the assistant may write

Draft a doc or a mail; propose a calendar event — always with a yes. Never send mail, never edit financial figures in a sheet, without an explicit instruction.

## Fields that matter

Google covers several roles at once. Treat each as its own role with its own approval line. Keep file and event URLs for linking back.

## Quirks worth knowing

Gmail and shared drives can expose far more than the job needs — always scope to the specific thread or file. A shared doc's edit is visible to collaborators immediately.

## Approval

Reading is scoped to what a job needs. Any write to Google Workspace lands on other people's
screens, so it always needs a yes — see [../rules/what-needs-my-approval.md](../rules/what-needs-my-approval.md).
