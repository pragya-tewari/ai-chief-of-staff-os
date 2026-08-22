---
job: capacity-and-headcount
spec-version: "0.1"
reads:
  - people/
  - org/roles.md
  - org/portfolio-map.md
  - projects/
  - sheets (budget source)
writes-internal:
  - reports/
  - log/activity.md
  - log/runs/
external-capabilities:
  - sheet.read
approval-actions:
  - sensitive-read

dedup-key: as-of-date+scope
supports-dry-run: true
---
