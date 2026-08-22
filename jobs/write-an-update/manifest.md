---
job: write-an-update
spec-version: "0.1"
reads:
  - projects/
  - task-source
  - registers/questions.md
  - decisions/
  - goals (org/goals.md)
  - now.md
writes-internal:
  - reports/
  - log/activity.md
  - log/runs/
external-capabilities:
  - chat.send
  - mail.send
  - doc.create
  - task.read
approval-actions:
  - external-write
  - tell-a-person
dedup-key: audience+reporting-period
supports-dry-run: true
---
