# How to do it

Read the rules first, and read the user's `profile/about-me.md` and
`profile/overrides.md` — this job must sound like them, not like an assistant.

## Run identity

Use recipient + message purpose + the source request/thread ID as the run key.
On a rerun, update the same draft and comms-register row. A send marked succeeded
is never repeated automatically; an in-progress send is verified in the selected
mail/chat tool or escalated to the user before any retry.

## Steps

1. **Who's it to, and what's the real point.** Strip it to the one thing that
   must land.
2. **Read the audience.** From `people/`, use only facts and the person's stated
   collaboration preferences. If private stakeholder context could materially
   help, name the exact private file and ask before reading it. Never copy a
   private observation or identifying detail into the draft; it may inform a
   safer approach only after permission.
3. **Pick the register.** Warm, firm, formal, brief — matched to the person and
   the point.
4. **Draft it in the user's voice.** Plain, direct, short paragraphs. Lead with
   the point or the ask. No throat-clearing, no brochure language.
5. **Flag the risk.** If a line could be turned against the user, say so and
   offer a safer version.
6. **Write to `reports/`, log it in `comms.md`.** Sending needs a yes, and the
   user sees the exact text and recipient first.
