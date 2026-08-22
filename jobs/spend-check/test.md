# Test

## Sample input

`run spend-check in recurring spend` against the sample company.

## Invariants

1. **Reads money, never writes it.** No financial figure is edited.
2. **Drift is explained.** Each gap or overlap has a reason and a recommended
   action.
3. **Ownership is named.** Unowned spend is flagged as unowned.
4. **Rerun refreshes.** The same source, reporting period and mode update the same
   report and receipt.

## Forbidden behaviours

- Editing a budget or a financial figure.
- Reporting a total with no line-level detail.
- Recommending a cut without naming the specific item.
