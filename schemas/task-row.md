# Schema: task row

The built-in task list, `workspace/tasks.md`, is one table. Every row has these
**nine** fields.

| Field | What it is | Values |
|---|---|---|
| `id` | Stable task ID | `T1`, `T2` … never reused |
| `task` | What to do, one line | starts with a verb |
| `type` | What kind of task | `commitment` · `follow-up` · `waiting` · `decision-action` |
| `owner` | Who owns it | a person `id`; `me` is an alias for the profile owner's own person id — prefer the explicit id, as the sample does (`per-sam`) |
| `project` | Which project | a project `id`, or blank |
| `due` | When it's due | an ISO date, or blank if genuinely undated |
| `status` | Where it stands | `todo` · `doing` · `blocked` · `waiting-on` · `done` · `cancelled` |
| `waiting on` | What it's stuck behind | a person, a thing, or blank (its dependency) |
| `from` | Where it came from | a meeting id (`M7`), another stable source id (a request, incident or people-move), or `user` for something you added directly |

## Example table

```
| id | task | type | owner | project | due | status | waiting on | from |
|----|------|------|-------|---------|-----|--------|------------|------|
| T21 | Send revised content scope to the vendor | commitment | per-ravi | prj-rollout | 2026-08-26 | todo | — | M3 |
| T15 | Confirm the renewal terms draft | commitment | per-omar | prj-renewal | 2026-08-29 | blocked | legal review | M2 |
| T16 | Rewrite the client welcome sequence | follow-up | per-meera | prj-onb | — | todo | — | M2 |
```

## Two rules

- **Closed and cancelled rows move to `tasks-done.md`** so the live file stays
  readable.
- **A task lives in one place only.** "What does Ravi owe me" is a filter of this
  table written to `reports/`, never a copy kept on Ravi's person file.

## Using an external task tool instead

These nine fields are the *shape* of a task, but an external tool needs a few
more to stay in step. When the live source is Asana, Linear or Jira, the
connection file maps these fields to the tool's and adds:

- `external_id` — the task's ID in the external tool.
- `external_url` — a link back to it.
- `provider` — which tool it lives in.

The connection file (`connections/<tool>.md`) holds that mapping. The built-in
list needs none of it, because the row *is* the task.
