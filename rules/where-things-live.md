# Where things live

Which system is the real record for what — by role, not by brand name. Read this
before pulling context from a tool or deciding where to write something.

## The map

| Kind of information | Real record | Read | Write |
|---|---|---|---|
| Tasks, owners, dates | the live task source — see `task-source.md` | yes | internal: yes · external: with a yes |
| Meeting transcript (raw) | transcript files / meeting tool — immutable evidence | yes | no |
| Meeting note (derived) | `workspace/meetings/` — correctable, with the change noted | yes | yes |
| Formal documents | doc store | yes | draft only |
| Money | spreadsheets | scoped | never without instruction |
| Team messages | chat tool | yes | with a yes |
| Current state, decisions, memory | your `workspace/` | yes | yes |

## Evidence, current state, and views are different

- **Evidence** is what was said and when. The raw transcript is immutable. The
  meeting note is *derived* from it — an interpretation that can contain errors,
  so it's correctable; when you correct it, note what changed. Everything else
  links back to it.
- **Current state** is what is true now — who owns what, what's decided. It lives
  in exactly one home.
- **A view** is a convenient rendering — "what does Ravi owe me". Generated on
  demand into `reports/`, never stored as if it were current state.

Duplicating a *view* is fine. Duplicating *current state* is the thing that
rots these systems.

## Two rules that close this file

- **If two sources disagree, don't guess.** Show both, say which you'd trust and
  why, and ask.
- **There is exactly one live task source at a time.** Read `task-source.md`
  before touching anything task-shaped. Never read the inactive source as
  current state — it is history, not truth, and the two are never synced.

## Related

- [what-needs-my-approval.md](what-needs-my-approval.md)
- [../connections/built-in-tasks.md](../connections/built-in-tasks.md)
