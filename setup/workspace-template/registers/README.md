# Registers

The running ledgers the assistant maintains. Each is one table with stable IDs so
other files can point at a row in plain text.

- `meetings.md` (`M#`) — the duplicate gate for transcripts.
- `questions.md` (`Q#`) — open questions.
- `uncertain.md` (`U#`) — extracted but unconfirmed.
- `comms.md` (`C#`) — messages sent or drafted.

Row formats: the product's `schemas/register-rows.md`.
