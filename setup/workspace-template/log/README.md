# Log

What the assistant did, and what it learned.

- `activity.md` — a running record of jobs run and writes made (append-only).
- `corrections.md` — every correction you made, with what was rejected and what
  was chosen. This is the raw material the learning loop promotes into your
  overrides.
- `runs/` — one stable, per-run checkpoint recording what each job planned,
  changed, sent, failed or must verify before retry.
