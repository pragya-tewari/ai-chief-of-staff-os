---
job: people-moves
spec-version: "0.1"
reads:
  - people/
  - projects/
  - task-source
  - org/roles.md
writes-internal:
  - people/
  - reports/
  - tasks
  - log/activity.md
  - log/runs/
external-capabilities:
  - task.update
  - task.assign
  - chat.send
  - task.read
  - mail.send
approval-actions:
  - external-write
  - tell-a-person
  - private-write
dedup-key: person-move-id
supports-dry-run: true
---
