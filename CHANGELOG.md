# Changelog

All notable changes are recorded here, in plain language, so you can decide
whether to pull an update. Dates are ISO (`YYYY-MM-DD`).

When a release needs a change to an existing workspace (a new register, a renamed
folder), the migration note goes here: what changes, how to apply it, how to undo
it.

## [Unreleased]

- Nothing yet.

## [0.1.1] — 2026-09-14

No workspace changes; nothing to migrate.

### Added
- `scripts/health-check.py` — a read-only workspace health check: broken links,
  isolated notes, dead ends (files nothing links to), entity files past their
  `review-by`, nested git repositories, and uncommitted work. It is the
  mechanical half of `review-the-system`, which now runs it in step 2.
- Rule: **Ending a session** in `rules/how-to-work.md` — link, record, hand off.
  Names the failure mode the health check exists for: work that ends without an
  ending.

### Changed
- Workspace template: folder READMEs now link the files they describe, so a
  fresh workspace passes the health check instead of reporting ten isolated notes.
- `review-the-system`: the worked example shows the check's headline counts;
  the test adds an invariant that unlinked or uncommitted files nobody owns are
  named, never committed by the job.

## [0.1.0] — 2026-09-09

First public release.

### Added
- Core rules: how-to-work, approvals, where-things-live, how-you-learn, safety.
- Schemas: entity header, task row, register rows, job manifest, capability names,
  run receipt.
- Adapters: root `CLAUDE.md` and `AGENTS.md`, plus a generic paste-in prompt.
- Connections: the role model, the built-in task list, and documentation stubs for
  Asana, Linear, Jira, Notion, Slack, Google and Zoho, using one namespaced
  capability vocabulary. User connection status lives in the workspace.
- Fourteen jobs, each with a manifest, method, worked example, and test.
- Setup: a real `install.sh`, a runnable `doctor.sh`, an isolated demo runner,
  and first-week onboarding.
- Lightweight rerun recovery: every job has a stable run key; Markdown receipts
  are created before writes and checkpoint each action; uncertain external
  outcomes must be verified before retry.
- A complete sample company (Northwind Learning, fictional) with a canonical
  timeline and an expected-state snapshot that exercises every shipped job.
- CI (`scripts/check.sh` via GitHub Actions): links, manifest/entity/task schemas,
  required files, capability names, credential/email/phone/forbidden-term scans,
  git-history checks, sample references and sample index coverage.
- GitHub issue and pull-request templates; SECURITY, CODE_OF_CONDUCT, CONTRIBUTING,
  RELEASING.

### Fixed
- Repository checks ignore OS dotfiles (`.DS_Store`) in the sample tree instead
  of reporting them as unindexed sample files.
- Run-key rule now states that a file component drops its extension, matching
  every shipped receipt and example.
- `meeting-to-tasks` reconciles the project index and `now.md` when they still
  name the meeting as pending, and files an unanswered factual question to
  `registers/uncertain.md`. The sample oracle and worked example list these
  outputs, plus the already-overdue T23 behaviour, so a faithful run matches.
- README and install guide give the clone URL.

### Known limitations
- Single primary user; no concurrency, transactions, or background execution.
- No exactly-once guarantee across external tools; ambiguous sends/creates stop
  for verification rather than retry automatically.
- Connection stubs are documentation only until wired to a real integration.
- Markdown rules are behavioural, not enforced permissions.
