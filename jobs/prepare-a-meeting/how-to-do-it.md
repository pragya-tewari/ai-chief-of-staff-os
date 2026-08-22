# How to do it

Read the rules first. Then pick the mode (see [modes.md](modes.md)) and follow
the shared method below.

## Run identity

Use the calendar event ID when available; otherwise use person/group + meeting
date + mode. A rerun refreshes the same prep pack for that meeting instead of
creating another current pack. Sending an agenda is a separate action and follows
the receipt's external-action verification rule.

## The shared method

1. **Name the meeting and its people.** Who's in the room, what each owns (from
   `people/` and `org/`).
2. **What changed since last time.** Read the last meeting note for this group
   and the current project status. Summarise what moved.
3. **What's owed, both ways.** Filter the task source: what these people owe, and
   what the user owes them. Write the filtered view to `reports/`.
4. **What needs deciding.** Pull open questions (`registers/questions.md`) and
   any decision that's ripe, with who holds the decision right
   (`org/decision-rights.md`).
5. **What to raise.** The two or three things the user should make sure to say.
6. **Assemble the pack** in `reports/`, in the shape the mode asks for.

Everything here reads and writes only to the user's own `reports/`. Nothing goes
to another person. If the mode calls for sending an agenda out, that is a
separate, approved step.
