# AGENTS.md — boot file for AI Chief of Staff OS

You are running the AI Chief of Staff OS. Follow these files exactly.

## Boot (every session)

1. **Find the workspace.** Read `cos-os.yaml`; its `workspace_path` is the user's
   private data folder (separate from this repo by default, or the fixed ignored
   `workspace/` path in inside mode). If it's missing, tell the user to run
   `setup/install.sh` and stop.
2. **Load the rules, in order:** `rules/safety.md`, `rules/how-to-work.md`,
   `rules/what-needs-my-approval.md`, `rules/where-things-live.md`,
   `rules/how-you-learn.md`. Then the
   user's `profile/about-me.md` and `profile/overrides.md` from the workspace.
3. **Never act from memory.** Read first.

## Running a job

The user says "run <job-name> on <input>", optionally "in <mode>", or adds "as a
dry-run" to plan without writing. Open `jobs/<job-name>/`, read its `manifest.md`
and prose files, and follow the runtime loop in `rules/how-to-work.md`. Before a
non-dry run, read `schemas/run-receipt.md`; when writing a structured destination
(an entity, a task row, a register row), follow its schema file in `schemas/`.
Check the
manifest's `external-capabilities` against the workspace's `connections.md`
before an external action. Check only the capability for that planned action. If
it is unavailable, stop that action and continue local work; do not require every
listed capability to be connected.

## Setting up the profile

When the user says "set up my profile", read `rules/about-me.template.md`, ask
the nine questions in `setup/install.md`, and complete every placeholder. Set
`last-confirmed` to today, `review-by` to 30 days later and `confidence`
to `confirmed`. Show the complete proposed `profile/about-me.md` write, and
write only after the user confirms it. Read the file back after writing.

## Isolated demo runs

When the prompt says "use <path> as the workspace for this demo run only", use
that exact path for every read and write in the run. Do not read or write the
workspace in `cos-os.yaml`, and never combine the demo with the user's workspace.

Companion guidance: [adapters/agents.md](adapters/agents.md).
