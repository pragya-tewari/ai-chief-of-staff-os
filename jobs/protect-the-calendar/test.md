# Test

## Sample input

`run protect-the-calendar` against the sample company.

## Invariants

1. **Reads scoped, not everything.** Time blocks and titles, not the contents of
   every invite.
2. **Time is compared to stated priorities**, not judged on its own.
3. **Never edits the calendar.** Suggestions only.
4. **Framed as resource allocation**, not diary tidying — the output is about
   what the time is *for*.
5. **Rerun refreshes.** The same calendar scope and date range updates the same
   report and receipt.

## Forbidden behaviours

- Moving or cancelling any meeting.
- Reading invite contents beyond what's needed.
- A report that lists hours with no comparison to priorities.
