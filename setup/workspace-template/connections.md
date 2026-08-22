# Connections (your runtime status)

Which tool fills each role, whether it's actually wired up, and the account it
points at. This is *your* state — it lives here in the workspace, not in the
product files. Update it as you connect tools.

| Role | Tool | Status | Account / scope |
|---|---|---|---|
| task | built-in list | verified | workspace/tasks.md |
| chat | — | documented | — |
| mail | — | documented | — |
| docs | — | documented | — |
| sheets | — | documented | — |
| calendar | — | documented | — |
| meetings | — | documented | — |

Status values: `documented` (not wired up) · `connected` (assistant can reach it)
· `verified` (the relevant real actions have been tested). Before a planned
external action, the assistant uses this table to find the live tool and its
product connection file to check the capability for that action. An unavailable
optional action does not block the job's local work.
