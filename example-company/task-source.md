---
active: internal
external-tool: none
switched: 2026-08-01
---

# Task source

ACTIVE:   tasks.md  (the built-in list)
INACTIVE: no external tool connected

Rules for any assistant reading this workspace:
- Read and write tasks only in the ACTIVE source.
- Never read the INACTIVE source as current state. It is history, not truth.
- Do not sync between the two. One is live, the other is frozen.
- Changing the active source is a decision the user makes explicitly, never a job.
