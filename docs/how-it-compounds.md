# How it compounds

A notes folder gets bigger. This gets *better* with use. Four things write back
into what the assistant reads next time.

| Every time you… | It writes to | So next time… |
|---|---|---|
| have a meeting | `meetings/` + `people/` + tasks | it already knows who owes what; you never re-brief it |
| settle something | `decisions/` | the same argument doesn't come back in six weeks |
| correct its writing or filing | `log/corrections.md` — and, once repeated or stated as a standing rule, `profile/overrides.md` | it makes that mistake once, not forever |
| do the same thing three times | a drafted playbook, then a job | it becomes a one-line request, not a re-explanation |

## The loop

```
you use it  →  it writes things down  →  you correct it  →  the rules update  →  using it is easier
     ▲                                                                                    │
     └────────────────────────────────────────────────────────────────────────────────────┘
```

## Why accumulation alone isn't enough

Piling up notes doesn't compound — it just grows, and eventually rots. Three
things stop the rot and turn accumulation into compounding:

- **Freshness on every entity file** (`last-confirmed`, `review-by`). Old files get
  flagged stale instead of asserted, so the system doesn't get more confidently
  wrong as it ages.
- **The weekly `review-the-system` job**, which reads the logs and reports what's
  stale, orphaned, or repeating. Reflection, not just accumulation.
- **Proactive checks** (`run-a-sweep`), which are only possible because people,
  projects and tasks are structured, not a pile of meeting notes.

Proactivity isn't a personality. It's scheduled queries over structured memory.
That's why the entity files and the registers matter more than any single job.
