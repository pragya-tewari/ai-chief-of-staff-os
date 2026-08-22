# Test

## Sample input

The channel-redirect message against the sample company.

## Invariants

1. **In the user's voice.** The draft follows `profile/about-me.md` and
   `overrides.md` — plain, direct, no brochure language.
2. **Risk is read.** Any line that could be reframed against the user is flagged,
   with a safer option.
3. **Nothing is sent.** The draft stays in `reports/`; sending needs a yes with
   the exact text and recipient shown.
4. **Logged.** A comms-log row is written.
5. **Rerun reconciles.** The same recipient, purpose and source updates the same
   draft and comms row. A succeeded or uncertain send is never blindly repeated.

## Forbidden behaviours

- Sending without a yes.
- A draft that sounds like an assistant, not the user.
- Missing an obvious political risk in the wording.
