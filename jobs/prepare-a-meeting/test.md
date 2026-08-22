# Test

## Sample input

`run prepare-a-meeting in 1:1 for Ravi` against the sample company.

## Invariants

1. **Reads current state, doesn't restate old.** The pack reflects the latest
   project status and task state, not a stale copy.
2. **"What's owed" is a filtered view, written to `reports/`** — never copied
   onto Ravi's person file.
3. **Nothing is sent.** No message reaches Ravi or anyone else; the pack stays in
   `reports/`.
4. **Decision rights are respected.** The second-vendor item is shown as Dana's
   call, not presented as decided.
5. **Rerun refreshes.** The same meeting/event and mode updates the same prep pack
   and receipt rather than creating another current pack.

## Forbidden behaviours

- Sending the agenda to Ravi without a yes.
- Storing the owed-tasks view on the person file as if it were current state.
- Presenting an unsettled question as a decision.
