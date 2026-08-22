---
job: goals-and-numbers
spec-version: "0.1"
reads:
  - org/goals.md
  - projects/
  - sheets (numbers source)
  - task-source
writes-internal:
  - org/goals.md
  - reports/
  - log/activity.md
  - log/runs/
external-capabilities:
  - sheet.read
  - sheet.write
  - task.read
approval-actions:
  - sensitive-read
  - sheet-write

dedup-key: goal-quarter+mode+period
supports-dry-run: true
---
