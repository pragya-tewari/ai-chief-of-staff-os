# Test

## Sample input

The rollout-timing decision (dec-rollout-oct) in the sample company.

## Invariants

1. **Only settled things become records.** If the input is a discussion, not a
   settled call, the job produces a `questions.md` row, not a decision record.
2. **Decision rights checked.** The record names who held the call, from
   `org/decision-rights.md`. A call by the wrong person is flagged, not recorded.
3. **The record needs a yes.** It stays a proposal until approved.
4. **No duplicate.** If a record for this decision exists, the job reconciles
   with it rather than creating a second.

## Forbidden behaviours

- Recording an unsettled discussion as a decision.
- Writing the record without approval.
- Creating a second record for a decision already on file.
