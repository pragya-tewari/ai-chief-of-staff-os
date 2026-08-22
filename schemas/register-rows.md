# Schema: register rows

Registers are the running ledgers the assistant maintains as it works. Four of
them, each a single table. Each row has a stable ID so other files can point at
it in plain text without a link.

## `meetings.md` — the duplicate gate

| Field | What it is |
|---|---|
| `id` | `M1`, `M2` … |
| `date` | ISO date of the meeting |
| `title` | Short name |
| `source` | The transcript file or tool ID, used to detect a re-run |
| `processed` | `no` · `partial` · `yes`. `partial` means the run's receipt still has planned, failed or uncertain actions (e.g. approvals pending); `yes` only when that receipt is complete. If a row says `yes` but its receipt is incomplete, the receipt wins |
| `outputs` | Where the extraction went (links) |

## `questions.md` — open questions

| Field | What it is |
|---|---|
| `id` | `Q1`, `Q2` … |
| `question` | The open question, in one line |
| `who can answer` | The person who can settle it |
| `raised` | ISO date |
| `status` | `open` · `answered` · `dropped` |

## `uncertain.md` — extracted but not confirmed

| Field | What it is |
|---|---|
| `id` | `U1`, `U2` … |
| `item` | The unclear thing — a garbled line, an inference, an ambiguous ask |
| `source` | Where it came from |
| `status` | `open` · `resolved` (promote to a question or a fact when resolved) |

## `comms.md` — messages sent or drafted

| Field | What it is |
|---|---|
| `id` | `C1`, `C2` … |
| `to` | Who it went to |
| `what` | One-line summary of the message |
| `date` | ISO date |
| `status` | `draft` · `sent` |

## The ID rule

`M`, `Q`, `U`, `C` plus a number. Plain text, never links, never reused.
