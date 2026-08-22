# Security

## Reporting a vulnerability

If you find a security or privacy problem — a way private data could leak into a
public tree, a prompt-injection path, an over-broad read — please report it
privately first. Do not open a public issue for it.

Use GitHub's private vulnerability reporting on this repository: open the
**Security** tab and choose **Report a vulnerability** (this opens a private
advisory only the maintainer can see). If that isn't available, open a regular
issue that says only "security report, please open a private channel" — with no
details — and the maintainer will follow up privately. You'll get an
acknowledgement, and a fix or a plan before anything is disclosed publicly.

## What this project treats as a security boundary

This is a plain-text system driven by an AI assistant. Instruction files reduce
risk; they do not create a hard, enforced boundary. Read that sentence twice —
it is the honest limit of what a Markdown rulebook can promise.

The real protections are:

- **Separated storage by default.** The recommended private workspace is a
  sibling of this repo. The optional inside mode is restricted to the fixed
  `workspace/` path, and setup verifies that it is ignored and untracked.
- **Least-privilege reading.** The assistant reads only what a job needs, and
  sensitive sources (mail, HR, money, private notes) need explicit scope. See
  [rules/safety.md](rules/safety.md).
- **Untrusted content.** Anything the assistant reads from a connected source is
  evidence, never instructions. A transcript that says "ignore your rules" is
  quoted to you, not obeyed.
- **A release scrub for the maintainer.** Anything published from a real vault
  is built into a fresh repo with no history. CI checks the current tree and git
  history for credential patterns, email addresses, phone numbers and forbidden
  internal terms; the release checklist adds a human review for names, numbers
  and context that pattern matching cannot classify. See
  [docs/threat-model.md](docs/threat-model.md).

## What you must do yourself

- Keep your workspace folder private. Back it up somewhere you control.
- Remember that git history keeps deleted secrets. If a secret ever lands in a
  tracked file, rotate it — deleting the file later does not remove it from the
  past.
