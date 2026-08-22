---
job: run-a-sweep
spec-version: "0.1"
reads:
  - task-source
  - projects/
  - people/
  - registers/questions.md
  - registers/uncertain.md
  - decisions/
writes-internal:
  - reports/
  - log/activity.md
  - log/runs/
external-capabilities:
  - task.read
approval-actions: []
dedup-key: sweep-period+mode
supports-dry-run: true
---
