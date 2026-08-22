---
job: manage-a-decision
spec-version: "0.1"
reads:
  - decisions/
  - registers/questions.md
  - org/decision-rights.md
  - people/
  - projects/
writes-internal:
  - decisions/
  - registers/questions.md
  - reports/
  - log/activity.md
  - log/runs/
external-capabilities: []
approval-actions:
  - decision-record
dedup-key: decision-id+mode
supports-dry-run: true
---
