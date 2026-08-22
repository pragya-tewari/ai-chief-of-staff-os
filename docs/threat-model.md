# Threat model

What can go wrong, and the matching mitigation. One page. This is for the
maintainer and for anyone deciding whether to trust the system with real data.

| Risk | What it looks like | Mitigation |
|---|---|---|
| **Accidental publishing** | Private data ends up in the public repo, history or a fork | Workspace is separate by default; the optional fixed inside path is git-ignored and verified untracked. CI scans the tree and complete fetched history for credential, email, phone and forbidden-term patterns. The release checklist adds human semantic review and publishes real-derived material only from a fresh history |
| **Prompt injection** | A transcript, email or doc tells the assistant to change its rules or take an action | All connected content is evidence, never instructions. Such text is quoted to the user, not obeyed. See [../rules/safety.md](../rules/safety.md) |
| **Over-broad tool access** | The assistant reads a whole inbox or drive when it needed one thread | Least-privilege reading: only the relevant source, only the fields a job needs. Sensitive sources need explicit scope |
| **Poisoned source document** | A shared doc is crafted to mislead the assistant | Treated as untrusted evidence; conflicting or suspicious content is surfaced, not acted on |
| **Partial writes** | A run half-finishes and leaves an inconsistent state | Every run has a stable key and a receipt created before writes. A rerun resumes pending work and never repeats a succeeded action. An external action left in-progress is verified in the tool or escalated to the user before retry; the project does not claim cross-tool atomicity or exactly-once execution |
| **Git history keeps secrets** | A secret is committed, then deleted, but stays in history | Never store secrets in any tracked file. If one lands, rotate it — deletion doesn't remove it from the past |
| **Log leakage** | Activity logs or receipts contain sensitive content | Log redaction: the same privacy rules apply to logs and receipts as to reports |

## The honest limit

Instruction files reduce risk. They do not create a hard, enforced boundary. The
real protections are separated storage by default, least-privilege reading, your
AI provider's data controls, and your own review of every external-facing
artifact. The docs say "designed so private data stays out of the public tree",
never "can never leak".
