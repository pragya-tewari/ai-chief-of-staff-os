# Schema: capability names

One namespaced vocabulary, used the same way in two places:
- a connection file declares which capabilities a tool **provides**;
- a job manifest declares which capabilities it **may use** (`external-capabilities`).

Before an external action, the assistant checks the capability for **that planned
action** against the selected tool's documented capabilities and the live status
in `workspace/connections.md`. A manifest lists every capability the job may use;
it is not a requirement that every listed tool be connected before the local
part of the job can run.

If a capability is unavailable, only that external action stops. The job
continues with its local analysis and draft wherever possible. For example, a
`meeting-to-tasks` run can write to the built-in task list without chat or mail
being connected.

## The vocabulary

| Capability | Meaning |
|---|---|
| `task.read` | read tasks, owners, dates |
| `task.create` | create a task |
| `task.update` | change a task's fields |
| `task.assign` | change a task's owner |
| `calendar.read` | read calendar events and time |
| `sheet.read` | read a spreadsheet |
| `sheet.write` | write a cell in a spreadsheet |
| `chat.read` | read chat messages, scoped to what a job needs |
| `chat.send` | post a chat message |
| `mail.read` | read mail, only with explicit scope (see safety) |
| `mail.send` | send an email |
| `meeting.read` | read a meeting recording or transcript |
| `doc.read` | read a document |
| `doc.create` | draft or update a document |

Do not invent new names. Adding one is a change to this file.

## The rule of least capability

A job declares only capabilities it may actually use. At runtime, check only the
capability matching the specific source or destination in the plan. A job that
reads money declares `sheet.read` and marks it a sensitive read (see
[../rules/safety.md](../rules/safety.md)).
