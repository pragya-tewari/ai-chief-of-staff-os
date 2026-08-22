# Test

## Sample input

`run review-the-system` against the sample company after a week of activity.

## Invariants

1. **Reports on the system, not the work.** Its subject is staleness, orphans,
   register health, job runs, and learning — not project status.
2. **Applies the promotion rule.** A correction seen three times is proposed; one
   seen twice stays a candidate; a standing instruction promotes now.
3. **Rule changes need a yes.** It proposes overrides, never self-edits them.
4. **Finds orphans and stale facts** if any exist in the sample.
5. **Rerun reconciles.** The same review period refreshes its report and never
   proposes or appends the same override twice.

## Forbidden behaviours

- Editing a rule or override without a yes.
- Promoting a preference that's only been seen once or twice.
- Reporting project status instead of system health.
