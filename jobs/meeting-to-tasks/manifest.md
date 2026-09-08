---
job: meeting-to-tasks
spec-version: "0.1"
reads:
  - registers/meetings.md
  - registers/uncertain.md
  - people/
  - projects/
  - org/portfolio-map.md
  - now.md
  - task-source
writes-internal:
  - meetings/
  - registers/meetings.md
  - registers/uncertain.md
  - registers/questions.md
  - people/
  - projects/
  - now.md
  - tasks
  - log/activity.md
  - log/runs/
writes-external:
  - task tool (only when external is the live source)
  - chat / mail (only to tell a person)
external-capabilities:
  - task.create
  - chat.send
  - mail.send
  - task.read
  - task.update
approval-actions:
  - external-write
  - tell-a-person
  - decision-record
  - private-write
dedup-key: meeting-source-id
supports-dry-run: true
---
