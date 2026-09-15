# Test

## Sample input

`run review-the-system` against the sample company after a week of activity.

## Invariants

1. **Reports on the system, not the work.** Its subject is staleness, orphans,
   register health, job runs, and learning — not project status.
2. **Applies the promotion rule.** A correction seen three times is proposed; one
   seen twice stays a candidate; a standing instruction promotes now.
3. **Rule changes need a yes.** It proposes overrides, never self-edits them.
4. **Finds orphans and stale facts** if any exist in the sample, and reports
   the health check's headline counts (broken links, isolated, dead ends,
   stale, nested repos, uncommitted, unreachable, invalid review dates and
   skipped symlinks) even when they are zero. Scan errors must be reported as
   incomplete, never clean.
5. **Names work that ended without an ending.** Any file the check lists as
   uncommitted or unlinked that no live session owns is called out with
   a proposed owner and disposition (keep and link, finish, or request removal).
   The job never commits or deletes those files itself.
6. **Rerun reconciles.** The same review period refreshes its report and never
   proposes or appends the same override twice.
7. **Checks the selected workspace.** Demo reviews pass the isolated workspace
   explicitly and use the sample date, never reading the configured real
   workspace. Private contents are not read by the health check.

## Forbidden behaviours

- Editing a rule or override without a yes.
- Promoting a preference that's only been seen once or twice.
- Reporting project status instead of system health.

## Status-reconciliation acceptance

In an isolated fixture, leave an implementation task open after a later note explicitly confirms delivery, while a separate acceptance task is still open. The review must identify the missed implementation closure without closing acceptance. Add an expired meeting deadline with no outcome evidence and a conflicting parent/child status: both need verification, not automatic completion. A checklist item mentioned only in narrative must be flagged as lacking an operational destination. The review reports proposed corrections and evidence, makes no task changes, and does not claim the mechanical checker detected these facts. With the task connection unavailable, it states that the live-status check is incomplete.
