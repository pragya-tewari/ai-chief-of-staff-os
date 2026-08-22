# AI Chief of Staff OS

**A local-first operating system for organisational coordination — the chief-of-staff job, run through an AI assistant.**

It is plain Markdown, start to finish: rules the assistant follows, recipes for
the work you do every week, and a filing system for what it learns. You can open
any file and read it. The project itself has no app, server, account or database
(your AI provider and any tools you connect are separate — see Limitations).

Most "AI chief of staff" projects manage *your* inbox and *your* day. This one
helps you **track, coordinate and follow up on work across the organisation** —
who owes what, what the founder needs to see, whether the team is using the
system — and it never touches another person's screen without your say-so. That
last part is the point.

---

## What makes it different

- **It coordinates work across the org, not your inbox.** Portfolio governance,
  meetings into decisions and tasks, reporting up, demand management, spend
  against plan, people moves.
- **Nothing is sent to a person or an external tool without your yes.** Writing
  into your own notes is free; anything that reaches another person or another
  tool always asks first. (Your workspace content is processed by whichever AI
  provider you run this with — see Limitations.)
- **It gets better because you correct it.** Every correction is captured, and
  the ones you repeat become rules.

---

## How it works, in one picture

```
something happens          →  a meeting, an email, a request
   → the assistant READS the rules and only the files it needs
   → it runs a JOB           (a recipe for this kind of work)
   → it reads and files into your WORKSPACE   (your private memory)
   → it shows you a PLAN and waits for your YES on anything external
   → it creates/updates a RUN RECEIPT before real writes
   → it writes to your TOOLS  (task tool, chat, docs) only after the yes
   → it checkpoints each action; uncertain external results are verified before retry
```

See [docs/architecture.md](docs/architecture.md) for the one-page version, and
[docs/how-it-compounds.md](docs/how-it-compounds.md) for why it gets sharper
with use.

---

## The two folders

The safest default keeps the product and your content side by side:

```
ai-chief-of-staff-os/          this repo — the system. You pull updates to it.
chief-of-staff-workspace/      your private data. A separate folder by default.
```

That separation lets you take updates without a merge conflict on your notes and
keeps company internals out of a public fork. The installer also offers a weaker
`--inside` option at the fixed, git-ignored `product/workspace` path; see the
limitations in [setup/install.md](setup/install.md) before choosing it.

---

## Install in five minutes

1. Clone this repo.
2. Run the installer — see [setup/install.md](setup/install.md). It creates and
   verifies your workspace (separate from the repo by default).
3. Try it on the sample company before you touch your own data —
   see [setup/first-week.md](setup/first-week.md).

---

## The jobs

Each job is a folder in [jobs/](jobs/). One recipe, one worked example, one test.

| Job | What it does |
|---|---|
| [meeting-to-tasks](jobs/meeting-to-tasks/how-to-do-it.md) | Transcript in, decisions and tasks out, filed and routed |
| [prepare-a-meeting](jobs/prepare-a-meeting/how-to-do-it.md) | The pack before any meeting: what changed, what's owed, what to raise |
| [manage-a-decision](jobs/manage-a-decision/how-to-do-it.md) | Frame it, align on it, record it, revisit it |
| [write-an-update](jobs/write-an-update/how-to-do-it.md) | One set of facts, calibrated for team, leads, founder, board or company |
| [run-a-sweep](jobs/run-a-sweep/how-to-do-it.md) | Open loops, task quality, risks, workload — across the whole portfolio |
| [intake-a-request](jobs/intake-a-request/how-to-do-it.md) | Someone asks for something: capture, decide, and write the no well |
| [goals-and-numbers](jobs/goals-and-numbers/how-to-do-it.md) | Set quarterly goals, track them, assemble the numbers against them |
| [spend-check](jobs/spend-check/how-to-do-it.md) | Where plan and money drifted apart, and what recurring spend runs quietly |
| [people-moves](jobs/people-moves/how-to-do-it.md) | Someone joins, leaves or changes role |
| [capacity-and-headcount](jobs/capacity-and-headcount/how-to-do-it.md) | Who we have, who we need, what it costs |
| [protect-the-calendar](jobs/protect-the-calendar/how-to-do-it.md) | Where the leader's time went against stated priorities |
| [draft-a-message](jobs/draft-a-message/how-to-do-it.md) | Stakeholder communication in your voice, risk read before sending |
| [post-mortem](jobs/post-mortem/how-to-do-it.md) | After a miss: what happened, why, what changes, who owns it |
| [review-the-system](jobs/review-the-system/how-to-do-it.md) | Weekly: what's mis-filed, stale, unowned, and what you corrected |

All fourteen ship in v0.1.0. The changelog records what each release adds —
see [CHANGELOG.md](CHANGELOG.md).

---

## An honest limit

The built-in task list is *your* record of what you're owed and what you
promised. It is not a shared team board — nobody else updates it and it notifies
no one. If your team lives in Asana or Linear, connect that instead and the
built-in list steps aside. Only one task source is ever live at a time. See
[connections/built-in-tasks.md](connections/built-in-tasks.md).

---

## Limitations (read these)

Honest about what v0.1 is and isn't:

- **One primary user.** No concurrency, no multi-agent locking, no atomic
  transactions. Run one assistant session at a time.
- **Rerun protection is procedural, not exactly-once infrastructure.** Stable
  run keys and per-action receipts reconcile interrupted work, but an uncertain
  external action must be checked in its tool or escalated to you before retry.
- **Exactly one live task source.** The built-in list *or* one external tool,
  never both — the other is frozen history.
- **The built-in task list is your own record**, not a shared team board. Nobody
  else updates it and it notifies no one.
- **No background execution or reminders** unless your assistant/runtime provides
  them. Jobs run when you run them.
- **The rules are behavioural instructions, not enforced permissions.** They
  reduce risk; they are not a hard security boundary. See [SECURITY.md](SECURITY.md).
- **Cloud-model privacy depends on your provider.** Workspace content you have the
  assistant read is processed by your AI provider under your account's settings —
  retention, training and region are outside this project's control. "No account"
  means *this project* has no server or account; your AI provider and external
  tools may still require one.
- **Large workspaces** may exceed the model's context; scope what a job reads.
- **Supported installer platforms:** macOS and Linux. On Windows, use WSL or a
  compatible Bash environment; native PowerShell installation is not shipped in
  v0.1.

These are acceptable v0.1 limitations. They're listed so the system looks as
trustworthy as it is.

---

## Who made this

Built and maintained by Pragya Tewari. Contributions welcome — see
[CONTRIBUTING.md](CONTRIBUTING.md). Security reports: [SECURITY.md](SECURITY.md).

MIT licensed.
