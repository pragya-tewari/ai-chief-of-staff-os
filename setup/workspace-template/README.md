# Your workspace

This folder is your private data. It is separate from the product repo by
default; in optional inside mode it sits at the fixed, git-ignored `workspace/`
path and must remain untracked. Back it up somewhere you control.

## The one-page model

Three kinds of thing live here:

- **Evidence** — the raw source is immutable. Notes in `meetings/` are derived
  interpretations and may be corrected with a dated change note.
- **Current state** — what's true now (`people/`, `projects/`, `decisions/`,
  `tasks.md`). Each fact lives in exactly one place.
- **Views** — convenient renderings like "what does Ravi owe me" (`reports/`).
  Generated on demand, safe to delete and regenerate.

## The folders

| Folder | What's in it |
|---|---|
| `profile/` | Who you are and how you work (`about-me.md`), and your learned rule changes (`overrides.md`) |
| `now.md` | This week: what's live, at risk, needs you |
| `task-source.md` | Which task system is live — exactly one |
| `tasks.md` / `tasks-done.md` | Your built-in task list and its archive |
| `org/` | How the organisation is shaped: portfolio, roles, decision rights, cadence, goals |
| `people/` | One file per person |
| `projects/` | One folder per project |
| `meetings/` | One correctable derived note per meeting; raw sources remain immutable |
| `decisions/` | One file per settled decision |
| `registers/` | The running ledgers |
| `reports/` | Generated views — not canonical, safe to delete |
| `private/` | People-sensitive material — never copied into an external-facing output |
| `log/` | What the assistant did and learned, including per-run recovery checkpoints under `log/runs/` |

## The privacy boundary, in one line

Anything in `private/` requires your permission to read and never appears in an
external-facing output. A cloud assistant still processes any file you approve
it to read under that provider's settings. Everything sent to another person or
written to an external tool waits for your yes. Read
`rules/safety.md` in the product folder (its location is set in `cos-os.yaml`) once
before feeding it real data.
