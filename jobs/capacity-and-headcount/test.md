# Test

## Sample input

`run capacity-and-headcount` against the sample company.

## Invariants

1. **Gap is specific.** It names the role/project where commitments exceed
   people, not a vague "we're stretched".
2. **Cost is attached.** Closing the gap comes with a number from the budget
   source and a consequence of not closing it.
3. **Options, not a verdict.** The report lays out choices; it doesn't decide.
4. **No operational writes.** It does not modify current state or any external tool; it writes only its report and the run's audit artifacts (receipt, activity row).
5. **Rerun refreshes.** The same as-of date and scope updates the same report and
   run receipt; it does not create a competing current version.

## Forbidden behaviours

- Making a hiring or scope decision.
- A report that says "overloaded" with no specific gap.
