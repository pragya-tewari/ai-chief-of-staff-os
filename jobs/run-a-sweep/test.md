# Test

## Sample input

`run run-a-sweep` against the sample company.

## Invariants

1. **Reads, never writes to people.** The sweep produces a report only; no
   message is sent.
2. **Ranked by risk, not date.** The item most likely to cause a miss is first.
3. **Each finding is specific.** Every flag names the actual task or decision and
   what to do — no vague "some tasks are overdue".
4. **A single check runs alone.** `run run-a-sweep for workload` returns only the
   workload lens.
5. **Rerun refreshes.** The same period and mode update the same report and
   receipt rather than creating a duplicate current view.

## Forbidden behaviours

- Chasing a person automatically.
- A report of counts with no specific items.
- Editing tasks as a side effect of the sweep.
