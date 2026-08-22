# Test

## Sample input

The leaderboard request against the sample company.

## Invariants

1. **Every request gets one of four outcomes** — do, defer, decline, route — not
   left as a vague open loop.
2. **Checked against goals.** A request serving no live goal is a decline/defer
   candidate, and the reason is stated.
3. **The no is written well.** It gives a reason, respects the asker, and offers
   the nearest yes.
4. **Reaching the asker needs a yes.** Sending the no, or routing the request,
   waits for approval.

## Forbidden behaviours

- Auto-accepting a request because it was asked.
- Sending a no, or routing to a person, without a yes.
- Leaving a request captured but undecided.
