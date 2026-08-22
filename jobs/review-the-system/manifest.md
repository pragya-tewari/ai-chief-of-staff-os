---
job: review-the-system
spec-version: "0.1"
reads:
  - log/
  - registers/
  - people/
  - projects/
  - decisions/
  - task-source
writes-internal:
  - reports/
  - profile/overrides.md
  - log/activity.md
  - log/runs/
external-capabilities:
  - task.read
approval-actions:
  - rule-change
dedup-key: review-period
supports-dry-run: true
---
