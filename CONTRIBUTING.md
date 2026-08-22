# Contributing

Thanks for wanting to help. This project stays useful only if it stays small and
readable, so contributions are held to that standard: plain language, one clear
job per file, no machinery a chief of staff couldn't read.

## The two easy contributions

**A connection file** — a maintainer-owned capability guide for a tool that
isn't covered yet. Copy an existing file in [connections/](connections/), declare
the role and standard `provides` capabilities, then document fields,
permissions and quirks. Do not add a user's connection status or account scope;
that runtime state belongs in their private `workspace/connections.md`. A
connection file is documentation, not a live integration — see
[connections/README.md](connections/README.md).

**A new job** — a recipe for recurring chief-of-staff work not already covered.
Copy the shape of an existing job in [jobs/](jobs/) and include every file the
format asks for, including a `test.md`. Read [jobs/README.md](jobs/README.md)
first. Before you add a job, check [docs/job-ideas.md](docs/job-ideas.md) — it
may already be parked there with a reason.

One mechanical step people miss: the repository checks pin the job list. When you
add or rename a job, also register it in `scripts/validate.py` — the expected job
count and the per-job dedup-key map — or `bash scripts/check.sh` will fail. That
pinning is deliberate: it stops a job and its run-key contract drifting apart.

## The rules every contribution follows

- **Plain text, human-readable.** If a file only makes sense to a machine, it
  will be sent back.
- **One home per fact.** Don't duplicate content across files; link instead.
- **Roles, not brands.** Jobs and rules never name a specific tool. Tool
  specifics live in `connections/`.
- **A job ships with a test.** `test.md` carries a sample input, the invariants
  that must hold, and the behaviours that are forbidden. See any job for the
  shape.
- **Original or clearly licensed.** Example content and prompts you contribute
  must be your own or under a compatible licence.

## How to propose it

Open a pull request. Small and focused beats large and sweeping. If you're not
sure whether an idea fits, open an issue first and ask — there are issue
templates for a new connection, a new job, and a rule that produced a bad
output.

## Writing style

Match the house style: lead with the point, use plain words, vary sentence
length, cut adjectives that add nothing. If a sentence sounds like a brochure,
rewrite it.
