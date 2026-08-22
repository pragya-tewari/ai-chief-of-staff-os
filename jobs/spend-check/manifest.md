---
job: spend-check
spec-version: "0.1"
reads:
  - projects/
  - sheets (budget source)
  - org/portfolio-map.md
writes-internal:
  - reports/
  - log/activity.md
  - log/runs/
external-capabilities:
  - sheet.read
approval-actions:
  - sensitive-read

dedup-key: source+reporting-period+mode
supports-dry-run: true
---
