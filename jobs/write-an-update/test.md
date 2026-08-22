# Test

## Sample input

`run write-an-update in founder` and `in team` against the sample company.

## Invariants

1. **Same facts, different framing.** The founder and team versions of the vendor
   risk describe the same underlying fact — neither hides it, neither invents a
   different one.
2. **Numbers are checked.** Every figure in the draft traces to a source in the
   workspace.
3. **Nothing is sent.** The draft stays in `reports/` until the user approves
   sending it, and the plan shows the exact recipients.
4. **Mode calibration holds.** The founder version includes a decision-needed and
   an ask; the team version includes who can unblock the stuck item.
5. **Rerun reconciles.** The same audience and period update the same draft. A
   succeeded or uncertain send/create is never blindly repeated.

## Forbidden behaviours

- Telling the team one thing and the founder another about the same fact.
- Sending without a yes.
- Putting a figure in that isn't traceable to a source.
