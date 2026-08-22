---
job: protect-the-calendar
spec-version: "0.1"
reads:
  - calendar
  - org/goals.md
  - org/cadence.md
writes-internal:
  - reports/
  - log/activity.md
  - log/runs/
external-capabilities:
  - calendar.read
approval-actions: []
dedup-key: calendar-scope+date-range
supports-dry-run: true
---
