# How to do it

Read the rules first. Pick the mode (see [modes.md](modes.md)).

## Run identity

The run key is the goal quarter plus the mode plus its period (`set` uses the
quarter itself; `track` the month; `assemble` the reporting week or month), so a
monthly track and a weekly assemble never collide.

## The shared method

1. **Read `org/goals.md`** — the quarter's goals, each with an owner and a
   measure. If it doesn't exist yet, `set` builds it.
2. **Read the numbers** from the sheets source, scoped to what the goals measure.
3. **Do the mode's work** — set, track, or assemble.
4. **Write the goals file or the pack.** Editing `org/goals.md` is internal and
   free; writing a figure back into a shared spreadsheet needs a yes.
5. **Say what's off-plan and why**, not just the number. A number without a "so
   what" isn't a report.
