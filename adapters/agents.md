# Adapter: AGENTS.md convention

Many coding assistants and agent runtimes read a file called `AGENTS.md` at the
root of a project. To use this system with one of them, copy this content into an
`AGENTS.md` at the root of the product folder.

It covers workspace discovery, rule loading, job execution, profile setup and
isolated demos.

## Find the workspace

Read `cos-os.yaml`. Its `workspace_path` points at the user's private data
folder. It is separate from this repo by default; the optional `--inside` setup
uses only the repo's git-ignored `workspace/` path.

## Load the rules first

Before acting, read in order: `rules/safety.md`, `rules/how-to-work.md`,
`rules/what-needs-my-approval.md`, `rules/where-things-live.md`,
`rules/how-you-learn.md`, then the user's `profile/about-me.md` and
`profile/overrides.md` from the workspace. Never act from memory.

## Run a job

The user says "run <job-name> on <input>", optionally "in <mode>", or adds "as a
dry-run" to plan without writing.

Open `jobs/<job-name>/`, read its `manifest.md` and prose files, and follow the
runtime loop in `rules/how-to-work.md`. Before an external action, check only the
matching capability in the manifest against the live status in the workspace's
`connections.md`. An unavailable optional action stops; the job's local work
continues.

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

## Note on tools

This convention assumes the runtime can read files in the repo and the
workspace. External tools (a task tool, chat, docs) work only if the runtime has
a real connection to them — see `connections/`. A connection file is
documentation; the actual read/write comes from the runtime's own integration.
