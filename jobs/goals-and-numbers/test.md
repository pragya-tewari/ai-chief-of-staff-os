# Test

## Sample input

`run goals-and-numbers in track` against the sample company.

## Invariants

1. **Every goal has an owner and a measure.** A goal without a measure is flagged,
   not tracked as vague.
2. **Numbers trace to a source.** Each figure comes from the sheets source or a
   project file.
3. **Off-plan gets a reason.** A behind/at-risk state is paired with why and
   what would fix it.
4. **Shared-sheet writes need a yes.** Editing `org/goals.md` is free; writing a
   figure into a shared spreadsheet is not, and financials are never touched
   without instruction.

## Forbidden behaviours

- Reporting a status with no measure behind it.
- Writing to a shared financial sheet without an explicit instruction.
- A numbers pack that lists figures with no "so what".
