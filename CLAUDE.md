# CLAUDE.md — boot file for AI Chief of Staff OS

You are running the AI Chief of Staff OS. Follow these files exactly.

## Boot (do this first, every session)

1. **Find the workspace.** Read `cos-os.yaml` in this folder. Its `workspace_path`
   is the user's private data folder (separate from this repo by default, or the
   fixed ignored `workspace/` path in inside mode). If `cos-os.yaml` is missing,
   tell the user to run `setup/install.sh` and stop.
2. **Load the rules, in order:** `rules/safety.md`, `rules/how-to-work.md`,
   `rules/what-needs-my-approval.md`, `rules/where-things-live.md`,
   `rules/how-you-learn.md`. Then the
   user's `profile/about-me.md` and `profile/overrides.md` from the workspace.
3. **Never answer from memory.** Read first.

## Running a job

The user says: **"run <job-name> on <input>"**, optionally **"in <mode>"**, or
adds **"as a dry-run"** to plan without writing.

Open `jobs/<job-name>/`, read its `manifest.md` and prose files (and `modes.md`
if present), then follow the runtime loop in `rules/how-to-work.md`. Before a
non-dry run, read `schemas/run-receipt.md`; when writing a structured
destination (an entity, a task row, a register row), follow its schema file in
`schemas/`. Before any
external action, check the matching item in the job manifest's
`external-capabilities` against the live status in the workspace's
`connections.md`. Check only the particular action being planned. If it is
unavailable, stop that action and continue the job's local work; do not require
every listed capability to be connected.

## Setting up the profile

When the user says **"set up my profile"**, read
`rules/about-me.template.md`, ask the nine questions in `setup/install.md`, and
complete every placeholder. Set `last-confirmed` to today, `review-by` to
30 days later and `confidence` to `confirmed`. Show the complete
proposed `profile/about-me.md` write. Write it only after the user confirms the
answers, and read the file back to verify it.

## Isolated demo runs

When a prompt says **"use <path> as the workspace for this demo run only"**, use
that exact path for all job reads and writes in that run. Do not read or write the
workspace in `cos-os.yaml`, and do not combine facts from the two workspaces.

Companion guidance: [adapters/claude.md](adapters/claude.md).
