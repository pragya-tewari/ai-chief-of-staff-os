---
job: post-mortem
spec-version: "0.1"
reads:
  - projects/
  - meetings/
  - decisions/
  - task-source
writes-internal:
  - reports/
  - profile/overrides.md
  - decisions/
  - tasks
  - log/activity.md
  - log/runs/
external-capabilities:
  - task.create
  - chat.send
  - task.read
  - task.update
  - mail.send
  - doc.create
approval-actions:
  - decision-record
  - tell-a-person
  - rule-change
  - external-write
dedup-key: incident-id
supports-dry-run: true
---
