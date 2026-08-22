# Modes

| Mode | When | What it does |
|---|---|---|
| `set` | start of a quarter | Turns intent into goals: each gets an owner, a measure, and a target. Writes `org/goals.md` |
| `track` | monthly | Checks each goal against its measure, flags drift, says what's at risk and what would get it back |
| `assemble` | weekly / monthly | Builds the numbers pack: the recurring figures, what changed, what's off-plan, and what needs an explanation before someone asks |

Reporting jobs (`write-an-update`) report *against* the goals this job maintains.
Without goals, "on track" has no track.
