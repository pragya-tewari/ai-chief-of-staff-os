# Changelog

All notable changes are recorded here, in plain language, so you can decide
whether to pull an update. Dates are ISO (`YYYY-MM-DD`).

When a release needs a change to an existing workspace (a new register, a renamed
folder), the migration note goes here: what changes, how to apply it, how to undo
it.

## [Unreleased]

- Nothing yet.

## [0.1.0] — 2026-08-23

First public-ready build.

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

### Known limitations
- Single primary user; no concurrency, transactions, or background execution.
- No exactly-once guarantee across external tools; ambiguous sends/creates stop
  for verification rather than retry automatically.
- Connection stubs are documentation only until wired to a real integration.
- Markdown rules are behavioural, not enforced permissions.
