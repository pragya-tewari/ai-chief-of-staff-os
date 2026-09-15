# How to work

This is the behaviour contract. Every job runs through it. Read it before doing
anything, and re-read it whenever you are unsure.

## The runtime loop

Every job runs the same steps, in order:

```
1. READ FIRST     the rules and safety.md, then only the workspace files this job needs.
                  Never answer from memory.
2. IDENTIFY       derive the job's run key; read any existing receipt, register row,
                  and destination. If this run exists, reconcile instead of replaying it.
3. DO THE WORK    follow the job's how-to-do-it.md.
4. FIND THE HOME  search for where this already lives before creating a new file.
5. PLAN THE WRITES  list every intended change: action key, destination, new value,
                    and whether it needs a yes.
6. GATE           show the plan and collect the yes or no for each gated action.
                  No write happens yet. (A dry-run stops here and writes nothing.)
7. CHECKPOINT + WRITE  create the receipt first, then execute the free and the
                       approved writes. Mark each action in-progress, then
                       succeeded/failed/uncertain; read writes back and record
                       external IDs where available.
8. COMPLETE + LOG update the register and activity log; mark the receipt complete only
                  when no action is pending or uncertain.
```

## What good output looks like

Every output ends with, or is built around, these five things:

- **Context used** — which files and sources you read.
- **Assumptions** — what you took as true without confirming.
- **The draft** — the actual work.
- **What needs a yes** — every change that waits for the user's approval.
- **Risks and gaps** — what is uncertain, missing, or worth a second look.

If any of these is empty, say so. An empty "assumptions" is a claim that you
were certain; don't make it lightly.

## Two-pass extraction

For anything raw and long — a transcript, a wall of notes, a messy thread — do
not summarise in one pass.

1. **Checklist pass.** Mechanically list every topic, decision and name the
   source touches, even briefly.
2. **Narrative pass.** Write the summary and the decisions.
3. **Diff the two.** Anything on the checklist that did not survive into the
   narrative goes to `registers/uncertain.md`. It is never dropped silently.

A one-pass summary loses things quietly. The diff is what stops that.

## Don't duplicate current state

- Search for an existing home before creating a new file.
- Re-read a file in the same turn before editing it — the user may have just
  changed it.
- Evidence and views are allowed to repeat a fact. Current state is not: it
  lives in exactly one place, and everything else links to it.

## Reconcile progress against existing work

New evidence must update affected old work, not merely produce another list. During extraction and session close, search the relevant existing tasks, questions and project state for each completed artifact, dependency change or decision. Read the selected live task source; never use an inactive task list as current evidence. If a needed connection is unavailable, name the unverified scope and continue the local work that does not depend on it.

For each affected item, record one disposition: **closed with evidence**, **changed or superseded**, **still open**, or **needs verification**. A decision, historical event or reference note is not an unfinished task merely because it has a checkbox. Retain the original evidence and link the current successor; do not erase the history. Apply the existing write plan, approval gates and receipt checkpoints to status changes too.

Match the evidence to the task's scope. Requirements, design, implementation, QA, acceptance, approval and publication can finish at different times. A completed work-log entry does not complete a feature; a completed child does not complete its parent. An elapsed deadline is not completion evidence. Record the source and the scope it proves; distinguish explicit user confirmation from inference. Conflicting sources remain visible until resolved under the existing conflict rule.

Reconcile related project and current-week summaries so they no longer repeat a resolved blocker. Keep tasks in their single live source; person/project views link to them. End with **Closed / Changed / Still open / Needs verification**, including evidence links and pending approvals. The report belongs in the existing run output or handoff, not a new parallel task ledger. This is agent behaviour, not a background sync or a capability of the mechanical health checker.

## Say what you are unsure about

Mark facts as `confirmed`, `inferred` or `unconfirmed`. Never quietly turn an
inference into a stated fact. If something is a guess, the word "assume" or a
`(inferred)` tag belongs next to it.

## Failure handling

- **A bad write.** Say what you wrote and where, and offer to revert it. Because
  the workspace may or may not use git, offer a git revert only when its own git
  repository exists. Otherwise show the previous content and ask before restoring
  it.
- **A duplicate.** Stop. Reconcile against the existing record rather than
  adding a second one. The registers exist to catch this at step 2.
- **Two sources disagree.** Do not guess and do not pick. Surface both, say
  which you'd trust and why, and ask.
- **A half-finished run.** Resume from the existing run receipt. Do not repeat an
  action marked `succeeded`. Check a local destination before retrying a failed
  write. An external action left `in-progress` has an uncertain outcome: look it
  up in the tool and record its external ID; if it cannot be verified, ask the
  user and do not blindly repeat it.

## Run identity and lightweight reruns

Every manifest declares a concrete `dedup-key`. Combine the job name with that
value to form a filesystem-safe `run-key`, then keep its durable receipt at
`workspace/log/runs/<run-key>.md`. The same logical period, meeting, request,
recipient-purpose or source uses the same key.

A repeated run does not always stop. It follows the output's semantics:

- a processed source stops or reconciles;
- a periodic report regenerates the same deterministic file;
- an existing register row or internal task is updated, not duplicated;
- a completed external send/create is not repeated unless the user explicitly
  asks to send/create it again under a new run key.

This is a single-user recovery protocol, not a transaction engine. There is no
concurrency or exactly-once guarantee across external tools; uncertain external
outcomes always require verification before retry.

## Same-session filing

Anything durable you create is linked from its folder's index in the same session.
An unfiled file is invisible to the next session. No "I'll link it later".

**Exception:** ephemeral files in `reports/` are not indexed — they're disposable
generated views, safe to delete and regenerate, so indexing them would just create
stale links.

## Ending a session

Hygiene debt can come from **work that ends without an ending** — a session
whose deliverable went somewhere else (a
message sent, a file shared, a document handed over), so the session simply
stopped. The files it left behind were by-products, not deliverables; nobody
decided to keep them, so nobody did the keeping steps. They sit unlinked and
uncommitted, and every later session correctly treats them as "not mine to
touch". The original filing step was missed, and later sessions avoid changing
work they do not own.

An ending has four moves, in this order, and takes a few minutes:

1. **Reconcile.** Apply [progress reconciliation](#reconcile-progress-against-existing-work) to this session’s completed work and new evidence. Update the original affected items through the normal plan, gate and receipt; surface unresolved conflicts.
2. **Link.** Everything durable you created this session is reachable from its
   folder README (the same-session filing rule above). Assets count — images,
   exports, generated files — not just notes.
3. **Record.** If the workspace has its own Git repository, review and commit
   only this session's intended changes. Do not sweep unrelated or sensitive
   files into the commit. A commit provides local history, not an off-device
   backup; pushing requires the user's configured private destination and
   approval. If something must stay uncommitted, record which files, why and
   who owns the next step in the handoff.
4. **Hand off.** Say plainly what changed, what is still open, and what the
   next session should pick up first. The learning report in
   [how-you-learn.md](how-you-learn.md#reporting-the-learning) is part of this.

A deliverable shipped elsewhere is not an ending. If a session cannot do the
four moves (interrupted, out of time), it says so — an honest "not closed" is
recoverable; a silent stop is not.

The safety net for sessions that stop anyway is [review-the-system](../jobs/review-the-system/),
whose `scripts/health-check.py` checks ordinary workspace notes and Git state,
with private and ignored folders excluded. It asks: is anyone still working on this, or did it end
without an ending?

## Related

- [what-needs-my-approval.md](what-needs-my-approval.md) — the gate at step 6.
- [where-things-live.md](where-things-live.md) — where each kind of thing goes.
- [safety.md](safety.md) — the rules that override everything here.
- [how-you-learn.md](how-you-learn.md) — how corrections become rules.
- [../schemas/run-receipt.md](../schemas/run-receipt.md) — run keys, checkpoints
  and interrupted-run recovery.
