# How to do it

Read the rules first. Pick one check or run all four (see [modes.md](modes.md)).
Every check reads across the workspace and writes a report to `reports/`. It
never messages anyone — chasing a person is a separate, approved action, or a
`draft-a-message` run.

## Run identity

Use the sweep period plus the selected mode — `all`, or one of the four in
[modes.md](modes.md): `open loops`, `task quality`, `risks and dependencies`,
`workload`. A rerun replaces/refreshes the same report for that period and mode.

## The shared method

1. **Read the whole picture:** the task source, project statuses, open questions,
   uncertainties.
2. **Run the chosen check(s)** against it (see the modes).
3. **Rank by what's most at risk**, not by date order — the thing most likely to
   cause a miss goes first.
4. **Write the report to `reports/`**, each finding with the specific item and
   what to do about it.
5. **Offer, don't act.** For anything that needs a nudge to a person, say so and
   offer to draft it — don't send.
