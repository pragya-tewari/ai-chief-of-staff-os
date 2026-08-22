# Architecture

One page. How the parts fit.

## The two folders

```
ai-chief-of-staff-os/        the product — rules, jobs, connections. You pull updates.
chief-of-staff-workspace/    your data — notes, people, projects, tasks. Separate by default.
```

They sit side by side by default. `cos-os.yaml` (in the product folder,
git-ignored) points at the workspace. The optional weaker inside mode is confined
to the product's ignored `workspace/` path.

## The flow, when something happens

```
something happens            a meeting, an email, a request
      │
      ▼
1. READ the rules + only the workspace files this job needs   (never from memory)
      │
      ▼
2. IDENTIFY the run          stable key + existing receipt/register/destination
      │
      ▼
3. RUN the job               the recipe in jobs/<name>/
      │
      ▼
4. FILE into the workspace   raw evidence immutable · derived notes correctable · state once
      │
      ▼
5. PLAN + GATE               show every action key; dry-run stops here
      │
      ▼
6. CHECKPOINT + WRITE        create receipt first; verify each local/external action
      │
      ▼
7. COMPLETE + LOG            resume pending work; verify uncertain sends before retry
```

## The four kinds of file

- **Rules** (`rules/`) — how the assistant behaves. Maintainer-owned; your
  changes live in `workspace/profile/overrides.md`.
- **Jobs** (`jobs/`) — recipes for recurring work. One per folder, same format.
- **Connections** (`connections/`) — maintainer-owned capability guides. The
  user's live role, tool, status and scope mapping lives in
  `workspace/connections.md`.
- **Memory** (`workspace/`) — everything the assistant learns and files.

## The three ideas that make it an OS, not a notes folder

1. **Approval by destination.** Recording is free; telling another person needs a
   yes. See [../rules/what-needs-my-approval.md](../rules/what-needs-my-approval.md).
2. **One home per fact.** Current state lives once; everything links. Evidence
   and views may repeat; current state may not.
3. **Corrections compound.** Every correction is captured, and the ones you repeat
   become rules. See [../rules/how-you-learn.md](../rules/how-you-learn.md).

The run receipt is a Markdown recovery checkpoint, not a transaction engine. The
system supports one user and one active assistant session; it does not promise
cross-tool atomicity or exactly-once delivery.
