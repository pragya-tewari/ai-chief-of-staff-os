# Doctor — a health check

Run the script whenever something feels off, and let `review-the-system` run the
content checks weekly:

```
bash setup/doctor.sh
```

It checks that the installation is wired correctly. It changes nothing. Errors
return a non-zero exit status; optional recommendations are warnings. Content
health is deliberately handled by `review-the-system`, not by this shell script.

## What it checks

**Wiring**
- The repo and the workspace can see each other (`cos-os.yaml` points at a real
  workspace folder).
- An inside workspace uses only `product/workspace`, is git-ignored and is not
  tracked by the product repository.
- Required workspace files exist and workspace/product format versions match.
- The activity/corrections logs and run-receipt index exist so jobs have their
  required audit and recovery destinations.
- Whether `profile/about-me.md` still contains setup placeholders (a warning
  until profile setup is completed).
- `task-source.md` has one valid active mode.
- Every connection role exists once and uses a valid status; the active task
  source agrees with the task connection and live roles name a real tool.
- Whether the workspace has its own local git repository for undo (a warning if
  it does not; merely being nested under the product repository does not count).

**Privacy**
- No report directly references a path under `private/`.
- No credential-shaped key, token, password or private-key value is present in
  workspace files. The `.git/` directory is excluded to avoid hook-template false
  positives.

**What the script does not check**
- Stale facts, orphans, old register items and semantic privacy leaks require
  reading the content; `review-the-system` handles those weekly.
- It cannot prove that a sensitive inference was paraphrased into a report. The
  user still reviews anything that may leave the workspace.

## How to read the result

Each line is `ok`, `WARN`, or `ERROR`. `ERROR` means the script exits non-zero and
the installation should not be used with real data. A clean doctor result means
the plumbing is sound, not that every piece of workspace content is correct.

## When to run it

- After install, to confirm the wiring.
- Weekly, via `review-the-system`.
- Any time a job behaves oddly — the cause is often a wiring or staleness issue
  this surfaces.
