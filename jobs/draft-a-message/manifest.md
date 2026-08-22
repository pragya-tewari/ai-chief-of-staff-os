---
job: draft-a-message
spec-version: "0.1"
reads:
  - people/
  - profile/about-me.md
  - profile/overrides.md
  - projects/
  - registers/comms.md
writes-internal:
  - reports/
  - registers/comms.md
  - log/activity.md
  - log/runs/
external-capabilities:
  - chat.send
  - mail.send
approval-actions:
  - external-write
  - tell-a-person
dedup-key: recipient+purpose+source-id
supports-dry-run: true
---
