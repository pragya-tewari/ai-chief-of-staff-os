# Supported assistants

Which assistants this has been used with, and how well. Honest labels:
`reference` means it's the setup the system was designed and manually exercised
against; `should work` means the adapter exists but it hasn't been fully
exercised. Nothing here is claimed as automatically tested — the checks that run
in CI are the mechanical ones (links, schemas, secrets), not a live assistant.

| Assistant | Adapter | Status | Notes |
|---|---|---|---|
| Claude Code | [../adapters/claude.md](../adapters/claude.md) | reference | Reads files and the workspace directly; the setup the system was built against |
| Claude (chat) | [../adapters/claude.md](../adapters/claude.md) | should work | You paste files it asks for; slower but the same system |
| Assistants reading `AGENTS.md` | [../adapters/agents.md](../adapters/agents.md) | should work | Depends on the runtime's file access |
| Any capable chat assistant | [../adapters/generic-prompt.md](../adapters/generic-prompt.md) | should work | You attach/paste the files each job needs; it returns proposed content for you to save |

## What an assistant needs to run this

- Either read files in the product/workspace folders directly, or accept the
  required files as attachments/pasted text and return proposed file content.
- Follow multi-step instructions from a Markdown file.
- Ideally, a real connection to your external tools (task tool, chat, docs) — see
  [../connections/](../connections/). Without one, the built-in task list and
  local jobs still work fully for file-aware assistants. Paste-in assistants can
  analyse and draft but cannot themselves persist local writes.

The installer supports macOS and Linux. Windows users need WSL or a compatible
Bash environment; assistant compatibility does not imply a native Windows setup
script.

## Adding one

Write an adapter — copy an existing one in [../adapters/](../adapters/). Its core
is three things — find the workspace, load the rules, define how a job starts —
plus the shared contracts an adapter must carry: profile setup, isolated demo
handling, the per-action capability check, and the run-receipt schema for non-dry
runs. Then add a row here with an honest status.
