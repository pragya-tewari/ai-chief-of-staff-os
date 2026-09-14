# How to do it

Read the rules first.

## Run identity

Use the review period (normally the ISO week). A rerun refreshes that period's
system review and reconciles any already-proposed override; it never appends the
same standing rule or candidate twice.

## Steps

1. **Read the week's logs** (`log/activity.md`, `log/corrections.md`, run
   receipts) and scan the workspace.
2. **Check the health signals.** Start with the mechanical ones — run the
   read-only check from the product folder and read its output:

   ```bash
   python3 scripts/health-check.py
   ```

   It reports broken links, isolated notes, dead ends (files nothing links to),
   entity files past their `review-by`, nested git repositories, and
   uncommitted work. Then add the signals only a reader can see:
   - Registers with items sitting open too long.
   - Jobs that ran, and any that errored or half-finished.
   - Corrections captured this week.
   - Work that ended without an ending: anything the check lists as
     uncommitted or unlinked that no session is still working on (see
     [Ending a session](../../rules/how-to-work.md#ending-a-session)).
3. **Catch missed learning.** Any explicit correction in the logs that wasn't
   promoted gets the promotion rule applied — a standing instruction promotes now,
   a preference needs its third repeat.
4. **Spot the "done three times" pattern.** If the same ad-hoc thing was done
   three times, draft a playbook for it (a candidate new job or override).
5. **Write the review to `reports/`.** Any rule change is proposed to
   `profile/overrides.md` and needs a yes.
