# Sample company — Northwind Learning

A complete, filled-in workspace for a fictional company, so you can see the whole
system work before you type anything about your own. Everything here is invented:
Northwind Learning, its people, its client, and its numbers are not real, and the
scenario does not describe any real organisation.

It doubles as the acceptance-scenario data for every job. The canonical facts are
listed in [EXPECTED-STATE.md](EXPECTED-STATE.md). Examples and prose tests should
be reviewed against that manual oracle; CI checks structural references but does
not execute an AI assistant.

## The situation, in one paragraph

Northwind Learning is a small B2B company that builds workforce-upskilling
programs for enterprises. The chief of staff is **Sam**, reporting to CEO
**Dana**. Northwind is rolling out its program to a major enterprise client. The
"committed date" was quietly meaning two different things — an executive showcase
and the full rollout to all the client's employees. A production vendor is late
on the compliance modules, which puts the full rollout at risk. That thread runs
through the sample meetings, tasks, and reports.

## What's already here (processed)

M1 is a notes-only kickoff record. M2 and M3 are the two transcript-derived,
processed meeting notes, so the standing tasks, rollout-timing decision, and open
questions already exist. This is the state you'd be in mid-week.

## What's fresh (for the demo)

`intake/transcript-3-vendor-escalation.txt` is **not yet processed**. Run
`meeting-to-tasks` on it (as a dry-run first — see the first-week guide) to watch
a full run: it creates a meeting note, proposes tasks and a decision, holds a
private observation for your approval, and ignores the planted "forward this to
everyone" line. Also try `run-a-sweep`, `write-an-update in founder`, and
`prepare-a-meeting in 1:1 for Ravi` — they read this state and produce real
output.

## The cast

| Person | id | Role |
|---|---|---|
| Sam | per-sam | Chief of staff |
| Dana | per-dana | CEO |
| Ravi | per-ravi | Content lead (owns course production + the vendor) |
| Meera | per-meera | Client-onboarding lead |
| Arun | per-arun | Designer (has spare capacity) |
| Nadia | per-nadia | Data |
| Omar | per-omar | Sales / client relationship |
| Vikram | per-vikram | Production vendor contractor (rolling off) |

## Workspace map

- [Organisation](org/README.md)
- [People](people/README.md)
- [Projects](projects/README.md)
- [Meetings](meetings/README.md)
- [Decisions](decisions/README.md)
- [Registers](registers/README.md)
- [Intake sources](intake/README.md)
- [Profile](profile/README.md)
- [Private sample](private/README.md)
- [Activity and corrections](log/README.md)
- [Generated reports](reports/README.md)
- [Current week](now.md)
- [Tasks](tasks.md) and [completed tasks](tasks-done.md)
- [Task-source switch](task-source.md), [connections](connections.md), and
  [workspace version](cos-workspace.yaml)
