# Example

Using the sample company. The onboarding-time goal has been missed two months
running.

## Input

`run post-mortem` on the missed onboarding-time goal.

## Output — `reports/post-mortem-onboarding.md`

**Post-mortem: onboarding time stuck at 2.5h (target <2h)**

*What happened*
- The welcome-sequence rewrite (T16) was created at the 14 Aug standup and is
  still `todo`.
- Each new client setup still runs the old, longer welcome flow, adding ~30 min.

*Why*
- T16 had no due date, so it never became this-week work and drifted. This is a
  task-quality gap, not a Meera problem: the sweep now catches undated tasks, but
  T16 slipped through before that was routine.

*What changes*
- Give T16 a due date and finish it (closes most of the gap). Arun can help if
  Meera is stretched.
- The task-quality sweep runs weekly from now, so undated tasks don't drift again.

*Who owns the change*
- Meera: finish T16 by a set date.
- Sam: make task-quality part of the weekly sweep (a standing change).

## What needs a yes

- The standing change (weekly task-quality sweep) as an override.
- Sharing this with the team, if you choose to.
