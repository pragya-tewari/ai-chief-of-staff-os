---
roles:
  - docs
  - sheets
  - chat
  - mail
  - calendar
  - meetings
provides:
  - doc.read
  - doc.create
  - sheet.read
  - sheet.write
  - chat.read
  - chat.send
  - mail.read
  - mail.send
  - calendar.read
  - meeting.read
---

# Connection: Zoho

Fills the **docs** role. This is a documentation stub: it describes how Zoho is
used and what it can provide when connected. Whether it's actually wired up is
your runtime state — record that in `workspace/connections.md` (status
`documented` / `connected` / `verified`), not here.

## What the assistant may read

WorkDrive/Writer docs, Sheets, Cliq messages, Mail threads, Calendar events, and meeting transcripts — scoped to what the job needs.

## What the assistant may write

Draft docs; post Cliq messages; propose calendar events — always with a yes. Never send mail or update a P&L sheet without an explicit instruction.

## Fields that matter

Zoho spans many roles; map each tool to its role (Writer/WorkDrive = docs, Cliq = chat, Mail = mail, Sheet = sheets, Calendar = calendar). Keep document and message links for referencing back.

## Quirks worth knowing

Finalised Cliq messages are plain text, delivered in the chat, not stored as files. Sheets writes can land one row off after a row delete — read the target row back after writing.

## Approval

Reading is scoped to what a job needs. Any write to Zoho lands on other people's
screens, so it always needs a yes — see [../rules/what-needs-my-approval.md](../rules/what-needs-my-approval.md).
