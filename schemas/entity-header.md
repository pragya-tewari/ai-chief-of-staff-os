# Schema: entity header

Every person, project, meeting, decision and profile entity file starts with the
same small header. Operational tables and configuration notes such as
`org/cadence.md`, registers and folder README files do not use this header. The
header makes stale entity facts visible and gives each entity a stable ID.

```
---
type: profile | person | project | org | meeting | decision
id: prj-rollout          # stable, never reused
name: <the readable name>
status: active | planning | dormant | closed
last-confirmed: 2026-08-24
review-by: 2026-09-07     # per-type — see the table below
confidence: confirmed | inferred | unconfirmed
---
```

## The fields

| Field | What it is | Notes |
|---|---|---|
| `type` | What kind of thing this file is | one of the six values above |
| `id` | A stable slug for the thing | `per-ravi`, `prj-rollout`, `org-acme`. Never reused, never changed even if the `name` changes. Other files refer to it in their `owner`/`project`/`from` fields |
| `name` | The readable name | can change; the `id` doesn't |
| `status` | Where it stands | `active`, `planning`, `dormant`, or `closed`. Closed things stay on file, they aren't deleted |
| `last-confirmed` | The date the facts here were last checked | ISO date |
| `review-by` | When to treat this as possibly stale | per-type default, see below |
| `confidence` | How sure we are of the file as a whole | a single load-bearing uncertain line can carry its own `(inferred, 2026-07)` tag inline |

## Staleness is per type, not one global number

A project status goes stale in about two weeks; an org chart doesn't for a
quarter; a settled decision doesn't go stale by age at all.

| Type | `review-by` default |
|---|---|
| profile | 30 days after `last-confirmed` |
| person | 30 days |
| project | 14 days |
| org | 90 days |
| meeting | never by age (it is a historical derived record; corrections are appended and traced to the immutable raw source) |
| decision | never by age (revisited by the decision job, not the clock) |

When the assistant uses a fact past its `review-by`, it flags it as possibly
stale rather than asserting it as current.

## Filenames and IDs

The **filename** is what a Markdown link resolves to, so links point to filenames
(e.g. `people/per-ravi.md`). The **id** in the header is the stable reference used
inside other files' fields (a task's `owner: per-ravi`, a project's `id`). To keep
links rename-safe, name files by their stable slug and keep the readable name in
`name:`. That is why the sample uses `per-ravi.md`, not `ravi-menon.md`.

There is no automatic id-to-file resolver — an id is a plain-text reference, not a
link. When you link across files, link the filename.
