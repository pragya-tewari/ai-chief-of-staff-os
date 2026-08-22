---
job: prepare-a-meeting
spec-version: "0.1"
reads:
  - org/cadence.md
  - org/decision-rights.md
  - people/
  - projects/
  - task-source
  - registers/questions.md
  - meetings/
  - decisions/
writes-internal:
  - reports/
  - log/activity.md
  - log/runs/
external-capabilities:
  - calendar.read
  - task.read
  - chat.send
  - mail.send
approval-actions:
  - external-write
  - tell-a-person
dedup-key: meeting-id-or-person+meeting-date+mode
supports-dry-run: true
---
