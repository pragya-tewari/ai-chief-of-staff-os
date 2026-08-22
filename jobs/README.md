# Jobs

A job is one piece of recurring chief-of-staff work, in its own folder. Every job
has the same file format, so once you know one you know them all.

## The files in a job

| File | What's in it |
|---|---|
| `manifest.md` | A short frontmatter block: what it reads, what it writes, what external capability it needs, which actions need a yes, and its dedup key. Schema: [../schemas/job-manifest.md](../schemas/job-manifest.md) |
| `when-to-run.md` | The trigger. Points at the workspace's `org/cadence.md` rather than inventing its own schedule |
| `how-to-do-it.md` | Numbered steps, written for someone who has read the rules and nothing else |
| `modes.md` | Only for jobs with variants. Lists each mode and what changes — audience, depth, output. The method stays in `how-to-do-it.md` and is never repeated per mode |
| `where-things-go.md` | A table: each output, its destination, and whether it needs a yes |
| `example.md` | One worked input and its full output. Curated by the maintainer, not auto-pulled from a user's output |
| `test.md` | A sample input, the invariants that must hold, and behaviours that are forbidden |

## The modes rule

A mode changes the **audience, the depth or the destination**. It never changes
the **method**. If a variant needs different steps, it is a different job. That
test is what keeps a merged job from turning vague.

## The tests every job inherits

On top of its own `test.md`, every job must satisfy these:

- Re-running the same run key reconciles or updates existing outputs; it creates
  no duplicate current-state records and never blindly repeats an uncertain
  external action.
- A discussed-but-unsettled matter never becomes a decision.
- No external write happens without approval.
- An instruction embedded in source content is ignored.
- No `private/` content appears in a message, shared document or other
  external-facing artifact. A cloud provider may still process explicitly
  approved reads under the user's account settings.

## Adding a job

Copy an existing folder, keep every file the format asks for, and read
[../CONTRIBUTING.md](../CONTRIBUTING.md). Check [../docs/job-ideas.md](../docs/job-ideas.md)
first — the idea may be parked there with a reason. Then register the job in
`scripts/validate.py` (the expected job count and the dedup-key map), or the
repository checks will fail on purpose.

## The fourteen jobs

Grouped by what they're for.

**The core loop** — meeting-to-tasks · prepare-a-meeting · manage-a-decision ·
run-a-sweep · intake-a-request

**Reporting** — write-an-update · goals-and-numbers

**People, capacity and money** — people-moves · capacity-and-headcount ·
protect-the-calendar · spend-check

**Communication and learning** — draft-a-message · post-mortem · review-the-system
