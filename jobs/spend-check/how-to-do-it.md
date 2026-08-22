# How to do it

Read the rules first. Pick the mode (see [modes.md](modes.md)). This job **reads**
money and reports on it; it never writes a financial figure. Reading a budget
is a sensitive read (see [../../rules/safety.md](../../rules/safety.md)) — scope it
to the specific sheet the job needs.

## Run identity

Use the specific budget source + reporting period + mode. A rerun refreshes the
same report for that key; it does not create a competing current spend view.

## The shared method

1. **Read the plan** — what a project or the portfolio was meant to cost or spend.
2. **Read the actuals** — from the budget/sheets source, scoped to what's needed.
3. **Find the drift** — where plan and reality diverged, and by how much.
4. **Explain the drift** — the reason, not just the gap.
5. **Write the report to `reports/`** with the specific lines and a recommended
   action for each.
