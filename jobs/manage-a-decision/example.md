# Example

Mode: `record`. The full rollout has just been moved to October in the founder
strategy call. Writing the decision record.

Note: in the sample this decision is already on file (dec-rollout-oct from M3), so
a real run here demonstrates the no-duplicate path — it reconciles with the
existing record rather than writing a second. The record below is what the
`record` mode produces when a decision is first written down.

## Input

`run manage-a-decision in record` — the rollout-timing decision from the 16 Aug
call.

## Output — decision record (waits for a yes)

`decisions/2026-08-16-full-rollout-october.md`

```
---
type: decision
id: dec-rollout-oct
name: Full rollout moves to October
status: active
last-confirmed: 2026-08-16
review-by: never
confidence: confirmed
---

# Full rollout moves to October

**Decided:** 16 Aug 2026, founder strategy call (M3).
**By:** Dana (CEO holds rollout timing — org/decision-rights.md).

**What was decided:** the full rollout to all the client's employees moves to
October. The executive showcase stays on the committed date.

**Why:** "the committed date" had been conflated — an executive showcase and a
full rollout on the same date. The vendor's compliance modules can't be done in
time for a full rollout by the committed date.

**What was rejected:** holding the committed date and rolling out incomplete
content. Rejected because a rollout missing the compliance modules would cost more
client trust than the delay.
```

## What needs a yes

The record (when first written). In the sample it already exists, so the run
reconciles instead of creating a duplicate.
