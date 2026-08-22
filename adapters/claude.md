# Adapter: Claude

This file tells Claude (Claude Code, or Claude in a chat) how to run this system:
find the workspace, load the rules, run jobs, set up the profile and isolate demo
runs.

If you are using Claude Code, the repository's root `CLAUDE.md` is the canonical
boot file. If you need to adapt another project, copy sections 1–3 below together;
the `Boot` heading is not a standalone empty block.

## 1. Find the workspace

Read `cos-os.yaml` in the product folder. It has `workspace_path` — the folder
that holds the user's private data. It is separate from this repo by default;
the optional `--inside` setup uses only the repo's git-ignored `workspace/`
path. Everything the user "owns" lives there; everything the assistant
"follows" lives here.

## 2. Load the rules before doing anything

At the start of every session, read, in this order:

1. `rules/safety.md` — the rules that override everything.
2. `rules/how-to-work.md` — the runtime loop and output shape.
3. `rules/what-needs-my-approval.md` — the gate.
4. `rules/where-things-live.md` — the source-of-truth map.
5. `rules/how-you-learn.md` — how corrections are captured and promoted.
6. The user's `profile/about-me.md` and `profile/overrides.md` from the
   workspace.

Do not answer from memory. Read first.

## 3. How the user starts a job

The user says: **"run <job-name> on <input>"**, optionally **"in <mode>"**.

Examples:

- `run meeting-to-tasks on ~/Downloads/standup-2026-08-20.txt`
- `run prepare-a-meeting in 1:1 for Ravi`
- `run write-an-update in founder`
- `run meeting-to-tasks on <file> as a dry-run` (plan only, writes nothing)

To run a job: open `jobs/<job-name>/`, read its `manifest.md`, `how-to-do-it.md`,
`where-things-go.md`, and `modes.md` if it exists, then follow the runtime loop
in `how-to-work.md`.

Before an external action, check the matching item in the job manifest's
`external-capabilities` against the live status in the workspace's
`connections.md`. Check only that planned action—not every capability the job
could use. If it is unavailable, stop that action, say so, and continue the
local work.

## Set up the profile

When the user says "set up my profile", follow `setup/install.md` and
`rules/about-me.template.md`: ask all nine questions, complete every placeholder,
set the confirmation fields, show the proposed file, and write only after the
user confirms it.

Set `last-confirmed` to today, `review-by` to 30 days later and `confidence` to
`confirmed`.

## Isolated demo runs

When the user says to use a specific path as the workspace for a demo run only,
use that exact path for every demo read and write. Do not read or write the
workspace in `cos-os.yaml`, and never combine the two workspaces.
