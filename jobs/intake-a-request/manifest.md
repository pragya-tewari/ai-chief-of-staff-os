---
job: intake-a-request
spec-version: "0.1"
reads:
  - org/goals.md
  - projects/
  - task-source
  - org/decision-rights.md
writes-internal:
  - reports/
  - tasks
  - registers/questions.md
  - log/activity.md
  - log/runs/
external-capabilities:
  - task.create
  - chat.send
  - mail.send
  - task.read
approval-actions:
  - external-write
  - tell-a-person
dedup-key: request-id
supports-dry-run: true
---
